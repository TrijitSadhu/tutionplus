"""
Admin views for background math translation with live progress.

URLs (added in bank/urls.py):
  /admin/bank/math/translate-select/   — language picker
  /admin/bank/math/translate-start/    — POST: kicks off background thread
  /admin/bank/math/translate-progress/ — AJAX polling
"""

import json
import os
import threading
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# ── In-process job store (survives for the life of the Django process) ────────
# { job_id: { 'total':int, 'done':int, 'errors':int, 'done_flag':bool, 'log':[] } }
_TRANSLATE_JOBS = {}
_JOBS_LOCK = threading.Lock()

LANG_CHOICES = [
    ('hi', 'Hindi (हिंदी)'),
    ('bn', 'Bengali (বাংলা)'),
    ('ta', 'Tamil (தமிழ்)'),
    ('te', 'Telugu (తెలుగు)'),
    ('mr', 'Marathi (मराठी)'),
]
LANG_NAMES = {code: name for code, name in LANG_CHOICES}


def _extract_json(raw):
    """Extract the first valid JSON object from raw LLM text, ignoring surrounding prose.

    Scans every top-level {...} block in order and returns the first one that
    parses as a dict.  This handles cases where the LLM response contains math
    expressions like {30 + 20} or {4740} before the real JSON object.

    Also falls back to ast.literal_eval so Python-style single-quoted dicts
    (common when rule_html contains HTML with double-quoted attributes) are
    accepted.
    """
    import ast
    import json as _json
    if not raw:
        raise ValueError('Empty response from model')

    pos = 0
    last_candidate = None
    while pos < len(raw):
        start = raw.find('{', pos)
        if start == -1:
            break
        depth = 0
        for i in range(start, len(raw)):
            if raw[i] == '{':
                depth += 1
            elif raw[i] == '}':
                depth -= 1
                if depth == 0:
                    candidate = raw[start:i + 1]
                    last_candidate = candidate
                    # Try strict JSON first
                    try:
                        result = _json.loads(candidate)
                        if isinstance(result, dict):
                            return result
                    except _json.JSONDecodeError:
                        pass
                    # Fall back to Python dict literal (single-quoted keys/values)
                    try:
                        result = ast.literal_eval(candidate)
                        if isinstance(result, dict):
                            return result
                    except Exception:
                        pass
                    # This block wasn't a valid dict; advance and try the next {
                    pos = start + 1
                    break
        else:
            break  # Unmatched '{'; stop searching

    if last_candidate is not None:
        raise ValueError('Invalid JSON in response: ' + repr(last_candidate[:200]))
    raise ValueError('No JSON object in response: ' + repr(raw[:200]))


def _build_groq_kwargs(model, prompt, override_max_tokens=None):
    """Return model-specific kwargs dict for client.chat.completions.create()."""
    if 'qwen' in model.lower():
        return dict(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.6,
            max_completion_tokens=override_max_tokens or 4096,
            top_p=0.95,
            reasoning_effort='default',
            stream=False,
            stop=None,
        )
    return dict(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3,
        max_tokens=override_max_tokens or 8192,
    )


def _groq_call(client, model, prompt):
    """Single Groq API call; returns parsed dict. Raises on empty/bad response."""
    resp = client.chat.completions.create(**_build_groq_kwargs(model, prompt))
    raw = resp.choices[0].message.content.strip()
    return _extract_json(raw)


def _translate_fields(client, model, fields_dict, lang_name, _json, _MAX_CHARS=2500):
    """
    Translate a dict of fields.
    If the combined payload exceeds _MAX_CHARS, falls back to one API call per field
    so that even very long solutions/rule_html never trigger a 413.
    """
    payload_str = _json.dumps(fields_dict, ensure_ascii=False)
    if len(payload_str) <= _MAX_CHARS:
        return _groq_call(client, model, _TRANSLATE_PROMPT.format(
            lang=lang_name, payload=payload_str))
    # Payload too large: translate each non-empty field individually
    result = {}
    for key, value in fields_dict.items():
        if not value:
            result[key] = value
            continue
        single_payload = _json.dumps({key: value}, ensure_ascii=False)
        r = _groq_call(client, model, _TRANSLATE_PROMPT.format(
            lang=lang_name, payload=single_payload))
        result[key] = r.get(key, value)
    return result


_TRANSLATE_PROMPT = (
    'Translate the following fields to {lang}.\n'
    'STRICT RULES:\n'
    '- Translate ONLY human-readable text words.\n'
    '- Keep all HTML tags, numbers, units and math symbols EXACTLY unchanged.\n'
    '- Return ONLY valid JSON with the same keys. No extra text, no markdown.\n\n'
    'Input JSON:\n{payload}'
)

_ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../.env')
)


def _reload_config():
    """
    Re-read the active .env and patch genai.config in-process.
    Called at the start of every translation job so the latest
    model/key choice is always used without a server restart.
    """
    from dotenv import load_dotenv
    load_dotenv(_ENV_PATH, override=True)
    import genai.config as cfg
    cfg.GROQ_API_KEY           = os.getenv('GROQ_API_KEY',           cfg.GROQ_API_KEY)
    cfg.GROQ_MODEL             = os.getenv('GROQ_MODEL',             cfg.GROQ_MODEL)
    cfg.GROQ_TEMPERATURE       = float(os.getenv('GROQ_TEMPERATURE', str(cfg.GROQ_TEMPERATURE)))
    cfg.GROQ_MAX_OUTPUT_TOKENS = int(os.getenv('GROQ_MAX_OUTPUT_TOKENS', str(cfg.GROQ_MAX_OUTPUT_TOKENS)))
    return cfg


def _translate_question(client, model, q, lang_name, _json):
    """
    Translate all text fields of a math question.
    Uses two batches (short / long) and falls back to per-field calls inside
    each batch when the payload would cause a 413 (request too large).
    """
    short_fields = {
        'question': q.question or '',
        'a': q.a or '', 'b': q.b or '', 'c': q.c or '',
        'd': q.d or '', 'e': q.e or '',
    }
    long_fields = {
        'solution': q.solution or '',
        'shortcut': q.shortcut or '',
        'extra': q.extra or '',
        'rule_based_explanation': q.rule_based_explanation or '',
    }
    r1 = _translate_fields(client, model, short_fields, lang_name, _json)
    r2 = _translate_fields(client, model, long_fields, lang_name, _json)
    return {**r1, **r2}


def _run_translation(job_id, math_ids, lang_code):
    """Runs in a background thread. Updates _TRANSLATE_JOBS[job_id] live."""
    import json as _json
    from bank.models import math as Math, math_translation, rule_math_translation

    # Always use the latest .env so UI changes take effect immediately
    cfg = _reload_config()

    def update(done=None, err_inc=0, msg=None):
        with _JOBS_LOCK:
            job = _TRANSLATE_JOBS[job_id]
            if done is not None:
                job['done'] = done
            job['errors'] += err_inc
            if msg:
                job['log'].append(msg)

    try:
        from genai.config import GROQ_API_KEY, GROQ_MODEL
        GROQ_API_KEY = cfg.GROQ_API_KEY
        GROQ_MODEL   = cfg.GROQ_MODEL
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        lang_name = LANG_NAMES.get(lang_code, lang_code)
    except Exception as e:
        with _JOBS_LOCK:
            _TRANSLATE_JOBS[job_id]['log'].append('Groq init error: ' + str(e))
            _TRANSLATE_JOBS[job_id]['errors'] += len(math_ids)
            _TRANSLATE_JOBS[job_id]['done'] = len(math_ids)
            _TRANSLATE_JOBS[job_id]['done_flag'] = True
        return

    questions = list(Math.objects.filter(id__in=math_ids).select_related('rule'))
    translated_rule_ids = set()

    for i, q in enumerate(questions):
        try:
            result = _translate_question(client, GROQ_MODEL, q, lang_name, _json)
            math_translation.objects.update_or_create(
                math=q, language=lang_code,
                defaults={
                    'question': result.get('question', ''),
                    'a': result.get('a', ''), 'b': result.get('b', ''),
                    'c': result.get('c', ''), 'd': result.get('d', ''),
                    'e': result.get('e', ''),
                    'solution': result.get('solution', ''),
                    'shortcut': result.get('shortcut', ''),
                    'extra': result.get('extra', ''),
                    'rule_based_explanation': result.get('rule_based_explanation', ''),
                }
            )
            # Track successfully translated languages on the math row
            q.refresh_from_db(fields=['translated_language'])
            existing = [x.strip() for x in (q.translated_language or '').split(',') if x.strip()]
            if lang_name not in existing:
                existing.append(lang_name)
                Math.objects.filter(pk=q.pk).update(translated_language=', '.join(existing))
            update(done=i + 1, msg='OK: id=' + str(q.id) + ' ' + str(q.chapter))

            # Translate the associated rule (once per unique rule_id)
            if q.rule_id and q.rule_id not in translated_rule_ids:
                translated_rule_ids.add(q.rule_id)
                try:
                    rule_payload = {
                        'rule_html': q.rule.rule_html or '',
                        'rule_text_with_latex': q.rule.rule_text_with_latex or '',
                    }
                    rule_result = _translate_fields(client, GROQ_MODEL, rule_payload, lang_name, _json)
                    rule_math_translation.objects.update_or_create(
                        rule=q.rule, language=lang_code,
                        defaults={
                            'rule_html': rule_result.get('rule_html', ''),
                            'rule_text_with_latex': rule_result.get('rule_text_with_latex', ''),
                        }
                    )
                    update(msg='  RULE OK: rule_id=' + str(q.rule_id))
                except Exception as re:
                    update(msg='  RULE ERR: rule_id=' + str(q.rule_id) + ' — ' + str(re)[:80])

        except Exception as e:
            update(done=i + 1, err_inc=1, msg='ERR: id=' + str(q.id) + ' — ' + str(e)[:120])

    with _JOBS_LOCK:
        _TRANSLATE_JOBS[job_id]['done_flag'] = True


@staff_member_required
def translate_select_view(request):
    """Step 1: Show language picker."""
    ids_str = request.session.get('translate_math_ids', '')
    if not ids_str:
        return redirect('../')  # back to math changelist

    count = len([x for x in ids_str.split(',') if x])
    return render(request, 'admin/bank/math/translate_select.html', {
        'count': count,
        'lang_choices': LANG_CHOICES,
        'ids': ids_str,
        'title': 'Translate Questions',
    })


@staff_member_required
def translate_start_view(request):
    """Step 2: POST — start background thread, redirect to progress page."""
    if request.method != 'POST':
        return redirect('../translate-select/')

    lang_code = request.POST.get('language', '')
    ids_str = request.POST.get('ids', '')

    if lang_code not in dict(LANG_CHOICES):
        return redirect('../translate-select/')

    math_ids = [int(x) for x in ids_str.split(',') if x.strip().isdigit()]
    if not math_ids:
        return redirect('../')

    job_id = str(uuid.uuid4())
    with _JOBS_LOCK:
        _TRANSLATE_JOBS[job_id] = {
            'total': len(math_ids),
            'done': 0,
            'errors': 0,
            'done_flag': False,
            'log': [],
            'lang': LANG_NAMES.get(lang_code, lang_code),
        }

    t = threading.Thread(
        target=_run_translation,
        args=(job_id, math_ids, lang_code),
        daemon=True,
    )
    t.start()

    # Clean session
    request.session.pop('translate_math_ids', None)

    return redirect('../translate-progress/?job=' + job_id)


@staff_member_required
def translate_progress_view(request):
    """Step 3: Progress page (renders template; AJAX polls endpoint below)."""
    job_id = request.GET.get('job', '')
    with _JOBS_LOCK:
        job = dict(_TRANSLATE_JOBS.get(job_id, {}))

    if not job:
        return redirect('../')

    return render(request, 'admin/bank/math/translate_progress.html', {
        'job_id': job_id,
        'job': job,
        'title': 'Translation Progress',
    })


@staff_member_required
def translate_progress_poll(request):
    """AJAX endpoint polled every 2s by the progress page."""
    job_id = request.GET.get('job', '')
    with _JOBS_LOCK:
        job = dict(_TRANSLATE_JOBS.get(job_id, {}))

    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)

    remaining = job['total'] - job['done']
    return JsonResponse({
        'total': job['total'],
        'done': job['done'],
        'errors': job['errors'],
        'remaining': remaining,
        'done_flag': job['done_flag'],
        'lang': job.get('lang', ''),
        'log': job.get('log', [])[-20:],  # last 20 lines
    })
