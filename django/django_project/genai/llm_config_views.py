"""
LLM Configuration UI — read/write the active .env and hot-reload genai.config.
Accessible at /genai/admin/llm-config/
"""

import os
import re
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

# ── .env helpers ──────────────────────────────────────────────────────────────

def _env_paths():
    """
    Returns info about the two .env files in the project.
    genai/config.py loads the ROOT .env (3 levels up from this file).
    """
    here = os.path.dirname(os.path.abspath(__file__))   # …/genai
    root_env  = os.path.normpath(os.path.join(here, '../../../.env'))
    genai_env = os.path.join(here, '.env')
    return [
        {'label': 'Root .env', 'path': root_env,  'active': True},
        {'label': 'genai/.env', 'path': genai_env, 'active': False},
    ]


def _read_env(path):
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith('#') and '=' in s:
                k, _, v = s.partition('=')
                result[k.strip()] = v.strip()
    return result


def _write_env_keys(path, updates):
    """Update specific KEY=VALUE lines; preserve comments and unrelated keys. Append new keys."""
    lines = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    updated = set()
    new_lines = []
    for line in lines:
        s = line.strip()
        if s and not s.startswith('#') and '=' in s:
            key = s.split('=', 1)[0].strip()
            if key in updates:
                new_lines.append(f'{key}={updates[key]}\n')
                updated.add(key)
                continue
        new_lines.append(line if line.endswith('\n') else line + '\n')

    for key, val in updates.items():
        if key not in updated:
            new_lines.append(f'{key}={val}\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def _hot_reload(env_path):
    """Re-read the .env and patch genai.config module vars in-process."""
    from dotenv import load_dotenv
    load_dotenv(env_path, override=True)
    import genai.config as cfg
    cfg.GROQ_API_KEY          = os.getenv('GROQ_API_KEY', cfg.GROQ_API_KEY)
    cfg.GROQ_MODEL            = os.getenv('GROQ_MODEL', cfg.GROQ_MODEL)
    cfg.GROQ_TEMPERATURE      = float(os.getenv('GROQ_TEMPERATURE', str(cfg.GROQ_TEMPERATURE)))
    cfg.GROQ_MAX_OUTPUT_TOKENS= int(os.getenv('GROQ_MAX_OUTPUT_TOKENS', str(cfg.GROQ_MAX_OUTPUT_TOKENS)))
    cfg.GEMINI_API_KEY        = os.getenv('GEMINI_API_KEY', cfg.GEMINI_API_KEY)
    cfg.GEMINI_MODEL          = os.getenv('GEMINI_MODEL', cfg.GEMINI_MODEL)
    cfg.GEMINI_TEMPERATURE    = float(os.getenv('GEMINI_TEMPERATURE', str(cfg.GEMINI_TEMPERATURE)))
    cfg.GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_OUTPUT_TOKENS', str(cfg.GEMINI_MAX_OUTPUT_TOKENS)))
    cfg.OPENAI_API_KEY        = os.getenv('OPENAI_API_KEY', cfg.OPENAI_API_KEY)
    cfg.OPENAI_MODEL          = os.getenv('OPENAI_MODEL', cfg.OPENAI_MODEL)
    cfg.DEFAULT_LLM_PROVIDER  = os.getenv('DEFAULT_LLM_PROVIDER', cfg.DEFAULT_LLM_PROVIDER)


# ── Model catalogues ──────────────────────────────────────────────────────────

GROQ_MODELS = [
    ('qwen/qwen3-32b',           'Qwen3-32B',          '32 768 ctx · best for long Bengali/Hindi'),
    ('llama-3.3-70b-versatile',  'Llama-3.3 70B',      '128 k ctx · versatile & fast'),
    ('llama3-70b-8192',          'Llama3 70B',          '8 192 ctx'),
    ('llama3-8b-8192',           'Llama3 8B',           '8 192 ctx · ultra-fast'),
    ('gemma2-9b-it',             'Gemma2 9B',           '8 192 ctx'),
    ('mixtral-8x7b-32768',       'Mixtral 8x7B',        '32 768 ctx'),
    ('openai/gpt-oss-120b',      'GPT-OSS 120B',        '4 096 ctx · causes 413 on long text'),
]
GEMINI_MODELS = [
    ('gemini-2.0-flash',   'Gemini 2.0 Flash',   'Fast, 1M ctx'),
    ('gemini-1.5-flash',   'Gemini 1.5 Flash',   'Fast, 1M ctx'),
    ('gemini-1.5-pro',     'Gemini 1.5 Pro',     'Best quality, 2M ctx'),
]
OPENAI_MODELS = [
    ('gpt-4o',        'GPT-4o',        '128 k ctx'),
    ('gpt-4-turbo',   'GPT-4 Turbo',   '128 k ctx'),
    ('gpt-4',         'GPT-4',         '8 k ctx'),
    ('gpt-3.5-turbo', 'GPT-3.5 Turbo', '16 k ctx'),
]

SAVE_KEYS = [
    'DEFAULT_LLM_PROVIDER',
    'GROQ_API_KEY', 'GROQ_MODEL', 'GROQ_TEMPERATURE', 'GROQ_MAX_OUTPUT_TOKENS',
    'GEMINI_API_KEY', 'GEMINI_MODEL', 'GEMINI_TEMPERATURE', 'GEMINI_MAX_OUTPUT_TOKENS',
    'OPENAI_API_KEY', 'OPENAI_MODEL', 'OPENAI_TEMPERATURE',
]


# ── Views ─────────────────────────────────────────────────────────────────────

@staff_member_required
def llm_config_view(request):
    paths     = _env_paths()
    active    = next(p for p in paths if p['active'])
    current   = _read_env(active['path'])
    error_msg = None
    ok_msg    = None

    if request.method == 'POST':
        updates = {}
        for key in SAVE_KEYS:
            val = request.POST.get(key, '').strip()
            if val != '':
                updates[key] = val
        try:
            _write_env_keys(active['path'], updates)
            _hot_reload(active['path'])
            ok_msg = 'Configuration saved and hot-reloaded successfully.'
            current = _read_env(active['path'])   # re-read for display
        except Exception as exc:
            error_msg = f'Save failed: {exc}'

    return render(request, 'genai/admin/llm_config.html', {
        'title':        'LLM Configuration',
        'active_env':   active,
        'all_envs':     paths,
        'current':      current,
        'groq_models':  GROQ_MODELS,
        'gemini_models':GEMINI_MODELS,
        'openai_models':OPENAI_MODELS,
        'ok_msg':       ok_msg,
        'error_msg':    error_msg,
    })


@staff_member_required
def llm_test_view(request):
    """AJAX: ping the active model with a tiny prompt and return result."""
    provider = request.GET.get('provider', 'groq')
    try:
        from genai.config import (GROQ_API_KEY, GROQ_MODEL,
                                   GEMINI_API_KEY, GEMINI_MODEL,
                                   OPENAI_API_KEY, OPENAI_MODEL)
        if provider == 'groq':
            from groq import Groq
            from bank.admin_translate_views import _build_groq_kwargs
            client = Groq(api_key=GROQ_API_KEY)
            kwargs = _build_groq_kwargs(GROQ_MODEL, 'Reply with exactly: OK', override_max_tokens=10)
            resp = client.chat.completions.create(**kwargs)
            return JsonResponse({'ok': True, 'model': GROQ_MODEL,
                                 'reply': resp.choices[0].message.content.strip()})
        elif provider == 'gemini':
            import google.generativeai as gai
            gai.configure(api_key=GEMINI_API_KEY)
            m = gai.GenerativeModel(GEMINI_MODEL)
            resp = m.generate_content('Reply with exactly: OK')
            return JsonResponse({'ok': True, 'model': GEMINI_MODEL, 'reply': resp.text.strip()})
        elif provider == 'openai':
            import openai
            openai.api_key = OPENAI_API_KEY
            resp = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{'role': 'user', 'content': 'Reply with exactly: OK'}],
                max_tokens=5)
            return JsonResponse({'ok': True, 'model': OPENAI_MODEL,
                                 'reply': resp.choices[0].message.content.strip()})
        else:
            return JsonResponse({'ok': False, 'error': 'Unknown provider'})
    except Exception as exc:
        return JsonResponse({'ok': False, 'error': str(exc)})
