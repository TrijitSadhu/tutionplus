"""
Admin actions for the math table:

  1. modify_language          — rephrase text to be copyright-free (no DB update to translation)
  2. validation_check         — verify answer by calculation, display OK / NOT OK (read-only)
  3. validate_math            — verify + fix answer/solution, update validation_status
  4. modify_language_validate — do both of the above with DB updates

All four run in background threads and share the same live-progress UI as the
translation tool.
"""

import os
import threading
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render

# ─── shared job store (same process as translate jobs) ───────────────────────
_ACTION_JOBS: dict = {}
_ACTION_LOCK = threading.Lock()


# ─── LLM helpers (reuse config reload from translate views) ──────────────────

def _get_client_and_model():
    from bank.admin_translate_views import _reload_config
    from groq import Groq
    cfg = _reload_config()
    return Groq(api_key=cfg.GROQ_API_KEY), cfg.GROQ_MODEL


def _llm(client, model, prompt: str) -> str:
    """Raw LLM call; returns stripped text."""
    from bank.admin_translate_views import _build_groq_kwargs
    resp = client.chat.completions.create(**_build_groq_kwargs(model, prompt))
    return resp.choices[0].message.content.strip()


def _llm_json(client, model, prompt: str) -> dict:
    """LLM call that expects a JSON dict response."""
    from bank.admin_translate_views import _build_groq_kwargs, _extract_json
    resp = client.chat.completions.create(**_build_groq_kwargs(model, prompt))
    raw = resp.choices[0].message.content.strip()
    return _extract_json(raw)


# ─── prompts ─────────────────────────────────────────────────────────────────

_MODIFY_LANG_PROMPT = """\
You are an expert question writer. Rewrite the following math question text so it \
is completely original and copyright-free while preserving the exact same \
mathematical meaning, numbers, and correct answer.

Rules:
- Keep ALL numbers, units, and math symbols EXACTLY unchanged.
- Keep HTML tags unchanged if any.
- Rewrite only the wording/phrasing; do NOT change the answer.
- Return ONLY valid JSON with the same keys as the input. No extra text.

Input JSON:
{payload}"""

_VALIDATE_PROMPT = """\
You are a strict math validator. Given the following math question and its \
answer options, calculate the correct answer by working through the math step by step.

Question: {question}
Options:
  1) {a}
  2) {b}
  3) {c}
  4) {d}
  5) {e}
Currently stored correct answer index (1-based): {ans}

Respond ONLY with valid JSON (no prose, no markdown):
{{
  "correct_index": <1-5, integer>,
  "is_correct": <true or false>,
  "working": "<brief step-by-step calculation>",
  "corrected_solution": "<rewritten solution matching the calculations>"
}}"""


# ─── per-question workers ─────────────────────────────────────────────────────

_TEXT_FIELDS = ['question', 'a', 'b', 'c', 'd', 'e', 'solution', 'shortcut', 'extra',
                'rule_based_explanation']


def _do_modify_language(client, model, q, update_db: bool) -> dict:
    """
    Rephrase all text fields of q to be copyright-free.
    Returns {'fields': {key: new_value}, 'modified': bool}.
    If update_db is True, saves the math row directly.
    """
    import json as _json
    from bank.admin_translate_views import _translate_fields

    payload = {k: getattr(q, k) or '' for k in _TEXT_FIELDS}
    import json as _json2

    # Non-empty fields only — skip blank ones so prompt stays small
    payload_nonempty = {k: v for k, v in payload.items() if v}
    payload_str = _json2.dumps(payload_nonempty, ensure_ascii=False)

    def _copyright_free_call(fields_dict):
        p_str = _json2.dumps(fields_dict, ensure_ascii=False)
        prompt = (
            'Rewrite every text value to be copyright-free while keeping the '
            'mathematical meaning, numbers, units and HTML tags EXACTLY as they are. '
            'Return ONLY valid JSON with the same keys. No markdown.\n\n'
            'Input JSON:\n' + p_str
        )
        return _llm_json(client, model, prompt)

    _MAX = 2500
    if len(payload_str) <= _MAX:
        # Single call for the whole question
        result = _copyright_free_call(payload_nonempty)
    else:
        # Split short / long fields to stay under token limit
        short = {k: payload[k] for k in ['question', 'a', 'b', 'c', 'd', 'e'] if payload.get(k)}
        long  = {k: payload[k] for k in ['solution', 'shortcut', 'extra', 'rule_based_explanation'] if payload.get(k)}
        r1 = _copyright_free_call(short) if short else {}
        r2 = _copyright_free_call(long)  if long  else {}
        result = {**r1, **r2}

    if update_db:
        for k in _TEXT_FIELDS:
            if result.get(k):
                setattr(q, k, result[k])
        q.save(update_fields=_TEXT_FIELDS)

    return result


def _do_validate(client, model, q, update_db: bool) -> dict:
    """
    Ask the LLM to calculate the correct answer.
    If update_db is True and the answer is wrong, fix ans/solution and set validation_status.
    Returns {'is_correct': bool, 'correct_index': int, 'working': str, 'corrected_solution': str}.
    """
    prompt = _VALIDATE_PROMPT.format(
        question=q.question,
        a=q.a or '', b=q.b or '', c=q.c or '',
        d=q.d or '', e=q.e or '',
        ans=q.ans,
    )
    result = _llm_json(client, model, prompt)
    is_correct = bool(result.get('is_correct', True))

    if update_db:
        updates = {'validation_status': 'validated'}
        if not is_correct:
            updates['ans'] = int(result.get('correct_index', q.ans))
            if result.get('corrected_solution'):
                updates['solution'] = result['corrected_solution']
        from bank.models import math as Math
        Math.objects.filter(pk=q.pk).update(**updates)

    return result


# ─── background runners ───────────────────────────────────────────────────────

def _job_update(job_id, done=None, err_inc=0, msg=None):
    with _ACTION_LOCK:
        job = _ACTION_JOBS[job_id]
        if done is not None:
            job['done'] = done
        job['errors'] += err_inc
        if msg:
            job['log'].append(msg)


def _run_action(job_id, math_ids, mode):
    """
    mode: 'modify_language' | 'validation_check' | 'validate_math' | 'both'
    """
    from bank.models import math as Math

    try:
        client, model = _get_client_and_model()
    except Exception as e:
        with _ACTION_LOCK:
            _ACTION_JOBS[job_id]['log'].append('LLM init error: ' + str(e))
            _ACTION_JOBS[job_id]['errors'] += len(math_ids)
            _ACTION_JOBS[job_id]['done'] = len(math_ids)
            _ACTION_JOBS[job_id]['done_flag'] = True
        return

    questions = list(Math.objects.filter(id__in=math_ids))

    for i, q in enumerate(questions):
        try:
            parts = []

            if mode in ('modify_language', 'both'):
                update_db = (mode == 'both')
                lang_result = _do_modify_language(client, model, q, update_db=update_db)
                if update_db:
                    parts.append('lang saved')
                else:
                    # Store full field-by-field comparison in job for the preview UI
                    comparison = {}
                    for k in _TEXT_FIELDS:
                        orig = getattr(q, k) or ''
                        new_val = lang_result.get(k) or ''
                        if orig:
                            comparison[k] = {'orig': orig, 'new': new_val}
                    with _ACTION_LOCK:
                        _ACTION_JOBS[job_id]['previews'][str(q.id)] = comparison
                    parts.append('preview ready')

            if mode == 'validation_check':
                res = _do_validate(client, model, q, update_db=False)
                status = 'OK' if res.get('is_correct') else 'NOT OK'
                working = res.get('working', '')[:80]
                parts.append(f'{status} — ans={q.ans}, calc={res.get("correct_index")} | {working}')

            if mode == 'validate_math':
                res = _do_validate(client, model, q, update_db=True)
                if res.get('is_correct'):
                    parts.append('validated OK (no change)')
                else:
                    parts.append(
                        f'fixed: ans {q.ans}→{res.get("correct_index")} | '
                        + res.get('working', '')[:60]
                    )

            if mode == 'both':
                res = _do_validate(client, model, q, update_db=True)
                if res.get('is_correct'):
                    parts.append('validated OK')
                else:
                    parts.append(f'fixed ans→{res.get("correct_index")}')

            _job_update(job_id, done=i + 1,
                        msg='OK id=' + str(q.id) + ' | ' + ' | '.join(parts))

        except Exception as e:
            _job_update(job_id, done=i + 1, err_inc=1,
                        msg='ERR id=' + str(q.id) + ' — ' + str(e)[:120])

    with _ACTION_LOCK:
        _ACTION_JOBS[job_id]['done_flag'] = True


# ─── Django action launchers ──────────────────────────────────────────────────

def _start_action_job(request, queryset, mode):
    from django.http import HttpResponseRedirect
    ids = [str(q.id) for q in queryset]
    job_id = str(uuid.uuid4())
    with _ACTION_LOCK:
        _ACTION_JOBS[job_id] = {
            'total': len(ids),
            'done': 0,
            'errors': 0,
            'done_flag': False,
            'log': [],
            'mode': mode,
            'previews': {},
        }
    threading.Thread(
        target=_run_action,
        args=(job_id, ids, mode),
        daemon=True,
    ).start()
    return HttpResponseRedirect('action-progress/?job_id=' + job_id)


def action_modify_language(modeladmin, request, queryset):
    """Rephrase questions to be copyright-free (preview only, no DB save)."""
    return _start_action_job(request, queryset, 'modify_language')

action_modify_language.short_description = 'Modify language (copyright-free rewrite)'


def action_validation_check(modeladmin, request, queryset):
    """Check answer by calculation — shows OK / NOT OK without changing anything."""
    return _start_action_job(request, queryset, 'validation_check')

action_validation_check.short_description = 'Validation check (read-only)'


def action_validate_math(modeladmin, request, queryset):
    """Calculate correct answer; fix ans/solution & mark validated if wrong."""
    return _start_action_job(request, queryset, 'validate_math')

action_validate_math.short_description = 'Validate math (calculate & update)'


def action_modify_and_validate(modeladmin, request, queryset):
    """Rephrase to copyright-free AND validate/fix answer — both saved to DB."""
    return _start_action_job(request, queryset, 'both')

action_modify_and_validate.short_description = 'Modify language + Validate math (both saved)'


# ─── progress views ───────────────────────────────────────────────────────────

_MODE_LABELS = {
    'modify_language': 'Modify Language',
    'validation_check': 'Validation Check',
    'validate_math': 'Validate Math',
    'both': 'Modify Language + Validate Math',
}


@staff_member_required
def action_save_preview(request):
    """Save the rephrased fields from a modify_language preview to the DB."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    job_id  = request.POST.get('job_id', '')
    math_id = request.POST.get('math_id', '')
    with _ACTION_LOCK:
        job        = _ACTION_JOBS.get(job_id, {})
        comparison = dict(job.get('previews', {}).get(str(math_id), {}))
    if not comparison:
        return JsonResponse({'error': 'Preview not found'}, status=404)
    from bank.models import math as Math
    updates = {k: v['new'] for k, v in comparison.items() if k in _TEXT_FIELDS and v.get('new')}
    if updates:
        Math.objects.filter(pk=math_id).update(**updates)
    return JsonResponse({'ok': True, 'saved_fields': list(updates.keys())})


@staff_member_required
def action_save_as_new(request):
    """
    Create a brand-new math row using the rephrased fields from the preview,
    copying all other fields (chapter, ans, images, etc.) from the original.
    Sets source_math = original so the lineage is tracked.
    Returns {'ok': True, 'new_id': <id>} — caller shows a link.
    Can be called multiple times to create multiple variants.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    job_id  = request.POST.get('job_id', '')
    math_id = request.POST.get('math_id', '')
    with _ACTION_LOCK:
        job        = _ACTION_JOBS.get(job_id, {})
        comparison = dict(job.get('previews', {}).get(str(math_id), {}))
    if not comparison:
        return JsonResponse({'error': 'Preview not found'}, status=404)

    from bank.models import math as Math
    try:
        original = Math.objects.get(pk=math_id)
    except Math.DoesNotExist:
        return JsonResponse({'error': 'Original question not found'}, status=404)

    # Clone: set pk=None to force INSERT
    original.pk = None
    original.id = None
    original.source_math_id = int(math_id)
    original.translated_language = ''   # fresh copy

    # Apply all rephrased fields from the preview
    for k, v in comparison.items():
        if k in _TEXT_FIELDS and v.get('new'):
            setattr(original, k, v['new'])

    original.save()
    return JsonResponse({'ok': True, 'new_id': original.pk})


@staff_member_required
def math_variants_view(request, math_id):
    """
    Shows a comparison table: the original question + all its saved variants
    (rows where source_math_id = math_id).
    URL:  /admin/bank/math/<id>/variants/
    """
    from bank.models import math as Math
    try:
        original = Math.objects.get(pk=math_id)
    except Math.DoesNotExist:
        return render(request, 'admin/bank/math/math_variants.html',
                      {'error': f'Question id={math_id} not found'})

    variants = list(Math.objects.filter(source_math_id=math_id).order_by('pk'))
    all_rows = [original] + variants

    # Build a field matrix for the template
    display_fields = [
        ('id',        'ID'),
        ('question',  'Question'),
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'),
        ('ans',       'Ans'),
        ('solution',  'Solution'),
        ('shortcut',  'Shortcut'),
        ('extra',     'Extra'),
        ('rule_based_explanation', 'Rule-based Explanation'),
    ]
    rows = []
    for field_name, label in display_fields:
        cells = [str(getattr(q, field_name) or '') for q in all_rows]
        rows.append({'label': label, 'cells': cells})

    return render(request, 'admin/bank/math/math_variants.html', {
        'original': original,
        'variants': variants,
        'all_rows': all_rows,
        'rows': rows,
        'math_id': math_id,
    })


@staff_member_required
def action_progress_view(request):
    job_id = request.GET.get('job_id', '')
    with _ACTION_LOCK:
        job = _ACTION_JOBS.get(job_id)
    if not job:
        return render(request, 'admin/bank/math/action_progress.html',
                      {'error': 'Job not found: ' + job_id})
    mode_label = _MODE_LABELS.get(job.get('mode', ''), job.get('mode', ''))
    return render(request, 'admin/bank/math/action_progress.html', {
        'job_id': job_id,
        'mode_label': mode_label,
        'total': job['total'],
    })


@staff_member_required
def action_progress_poll(request):
    job_id = request.GET.get('job_id', '')
    with _ACTION_LOCK:
        job = dict(_ACTION_JOBS.get(job_id, {}))
    if not job:
        return JsonResponse({'error': 'not found'}, status=404)
    return JsonResponse({
        'total': job['total'],
        'done': job['done'],
        'errors': job['errors'],
        'done_flag': job['done_flag'],
        'log': job['log'],
        'previews': job.get('previews', {}),
    })
