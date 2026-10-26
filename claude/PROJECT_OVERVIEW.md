# TutionPlus — Project Understanding (for Claude)

> Written by Claude on 2026-10-26 after reading the project. Nothing in the
> project was changed. This is a read-only summary to get oriented.

---

## 1. What this project is

**TutionPlus** (repo name `tutionplus`, tagline "ExamsWithAI") is a **Django web
application** for exam/tuition content. Its standout feature is a **GenAI module**
that auto-generates question content (MCQs, descriptive answers, math problems)
from uploaded PDFs and news sources, using LLM APIs.

The part you described — *"upload a math chapter PDF, use a saved prompt, call the
DeepSeek API, send the PDF text, and let DeepSeek do what the prompt instructs"* —
is exactly the **Math PDF → MCQ** pipeline inside the `genai` app.

---

## 2. Tech stack

| Layer | What it uses |
|-------|--------------|
| Framework | Django (very old baseline, `django-admin startproject` from Django 1.8 era, but running newer) |
| Language | Python |
| Database | PostgreSQL (`post` DB) in dev/prod; a SQLite config also exists but unused |
| LLM providers | **DeepSeek**, Groq (default), Gemini, OpenAI, NVIDIA NIM — all pluggable |
| PDF/OCR | PyPDF2, PaddleOCR, EasyOCR, Tesseract, pdf2image |
| Deploy | GitHub Actions → SSH to an Interserver VPS, runs under gunicorn + systemd |
| Front-end | Django templates (admin-driven workflow) |

Most of the AI work is done **through the Django admin** (staff-only), not a public UI.

---

## 3. Where things live (folder map)

```
tutionplus/
├─ .git/                       # git repo, remote = github.com/TrijitSadhu/tutionplus
├─ .github/workflows/deploy.yml  # auto-deploy to VPS on push to main
├─ .env / .env.example / .env.template  # API keys & secrets (gitignored)
├─ .gitignore                  # ignores .env, media, db, pycache, uploaded_pdfs
├─ requirements.txt
├─ (100+ *.md docs)            # feature write-ups / notes (not code)
├─ (many *.py helper scripts)  # one-off test/setup scripts at root
├─ deploy/                     # systemd unit files, deploy helpers
├─ scripts/                    # e.g. backup_db.sh
└─ django/
   └─ django_project/          # <-- the actual Django project
      ├─ manage.py
      ├─ django_project/        # settings, urls, wsgi
      │   ├─ settings.py        # dev settings (DEBUG=True)
      │   └─ settings_production.py
      ├─ bank/                  # question-bank models (math, polity, etc.)
      ├─ students/              # student-facing app
      ├─ mocktest/              # mock test app
      └─ genai/                 # <-- the AI engine (most important app)
          ├─ config.py          # reads .env, defines all LLM settings/keys
          ├─ models.py          # DB models (prompts, logs, generation jobs)
          ├─ admin.py           # admin UI + the per-row "GO" button (79 KB!)
          ├─ views.py           # API + form handlers (44 KB)
          ├─ forms.py           # the math-PDF processing config form (11 fields)
          ├─ urls.py            # genai routes
          ├─ utils/
          │   └─ llm_provider.py  # <-- all LLM API clients (DeepSeek etc.)
          ├─ tasks/
          │   ├─ math_processor.py   # <-- math PDF pipeline + OCR engines (73 KB)
          │   ├─ pdf_processor.py    # generic subject PDF → MCQ
          │   ├─ current_affairs.py  # news scraping → MCQ
          │   └─ task_router.py      # routes a job to the right processor
          ├─ services/          # agentic workflow / job scraping helpers
          └─ uploaded_pdfs/     # uploaded PDFs (gitignored)
```

Note: there is also a folder literally named
`django/django_project/this forlder is a back up of django_project` — a manual backup copy.

---

## 4. How the DeepSeek math-PDF flow actually works

This matches what you described. Step by step:

1. **API keys live in `.env`** at the project root. `genai/config.py` loads it and
   exposes `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL` (default `deepseek-chat`),
   `DEEPSEEK_BASE_URL` (`https://api.deepseek.com`), temperature, max tokens
   (32768), and a 420s timeout.

2. **Provider selection.** `config.py` has `DEFAULT_LLM_PROVIDER` (defaults to
   `groq`, overridable via `.env`). `llm_provider.py` has a `DeepSeekProvider`
   class that talks to DeepSeek using the **OpenAI-compatible** client
   (`OpenAI(api_key=..., base_url="https://api.deepseek.com")`). You pick DeepSeek
   by setting `DEFAULT_LLM_PROVIDER=deepseek` in `.env`.

3. **Saved prompts are stored in the database**, not hard-coded. Two models hold them:
   - `LLMPrompt` — prompts for MCQ / descriptive / rule-extraction, with
     `{title}` and `{content}` placeholders.
   - `MathPromptTemplate` — the reusable extraction prompt for the math JSON
     generation page, with a `{difficulty}` placeholder and an `is_default` flag
     so it auto-fills.

4. **Upload a math chapter PDF.** A `MathProblemGeneration` admin record holds the
   `pdf_file`, optional `chapter`, and `difficulty`. From the admin list, each row
   has a **"GO" button** that opens a configuration form (`forms.py`) with ~11
   options: let the LLM decide chapter/difficulty, which OCR engine(s) to use,
   single page / page range / whole-PDF-in-chunks, etc.

5. **Processing** (`tasks/math_processor.py`, class `MathPDFProcessor`):
   - OCR extracts text from the PDF pages (fallback chain **PaddleOCR → EasyOCR
     → Tesseract**).
   - The extracted **PDF text is combined with the saved prompt** and sent to the
     configured LLM (DeepSeek in your case) via `llm_provider`.
   - DeepSeek returns JSON MCQs; the code parses it (handles markdown-fenced JSON).
   - Results are **saved to the `bank.math` table**; a `ProcessingLog` row tracks
     status, counts, and errors.

So: **PDF → OCR text → (saved prompt + text) → DeepSeek API → JSON MCQs → database.**
That is the core loop you built.

---

## 5. GitHub sync — can Claude push these changes directly?

**Short answer: not automatically right now, and you should be careful before you do.**

Details:

- The repo **is** a git repository. Remote `origin` =
  `https://github.com/TrijitSadhu/tutionplus.git`, tracking branch **`main`**.
- To actually `git commit` + `git push` from *your computer*, Claude needs a working
  shell on your machine. At the moment that shell (the device workspace) **failed to
  start**, so Claude currently can only read/stage/write files on your computer, not
  run git commands there. When that shell is available, Claude can run git for you —
  but the **push itself still uses your GitHub credentials** configured in
  VS Code / git on your machine.
- ⚠️ **Important side effect:** `.github/workflows/deploy.yml` auto-deploys on **every
  push to `main`**. It SSHes into your Interserver VPS, does `git reset --hard`,
  installs requirements, backs up the DB, runs migrations, collects static, and
  restarts gunicorn. So **"sync to GitHub" = "deploy to production."** Don't push
  half-finished work to `main`; use a branch or be sure it's ready.
- ✅ Good news: `.env` (your DeepSeek and other API keys) is in `.gitignore`, so keys
  are **not** pushed to GitHub.

**Recommended ways to sync, in order of safety:**
1. Use VS Code's built-in Source Control (you clearly already use VS Code) — review the
   diff, commit, push. Safest and you stay in control.
2. Ask Claude to do it once the device shell is back — Claude can run `git status`,
   stage specific files, commit with a message, and push. Confirm the branch first.
3. For risky changes, push to a **new branch** (not `main`) to avoid the auto-deploy,
   open a PR, and merge when ready.

---

## 6. Things worth knowing / minor red flags (no action taken)

- `settings.py` has `DEBUG = True`, a hard-coded `SECRET_KEY`, DB password, and an
  email password in plain text. Fine for local dev, but these are sensitive — the
  production file is `settings_production.py`. (Not changing anything, just noting.)
- The project root is very cluttered with 100+ markdown "summary" docs and many
  one-off `test_*.py` / `check_*.py` scripts. They're documentation/scratch, not part
  of the running app.
- `db.sqlite3` at the django root is 0 bytes (PostgreSQL is the real DB).

---

## 7. How to work with Claude from here (first-time notes)

- This folder (`claude/`) is a safe place for Claude's notes and scratch docs.
- Claude can **read and edit files directly on your computer** in this project folder
  while this chat is linked to your machine via the Claude desktop app.
- Claude did **not** implement or change anything for this task — this file is the
  only thing created.
- When you want changes made, just say so; Claude can also run the project's scripts,
  tests, and git — once the on-device shell is back up.
```

Suggested next steps you might ask for:
- "Add DeepSeek as the default provider and show me the exact .env lines."
- "Walk me through math_processor.py's prompt-building code in detail."
- "Help me commit and push safely without triggering the auto-deploy."
```
