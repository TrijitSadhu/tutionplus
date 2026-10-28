# Math question bank: how the work is done (handoff notes)

Written 2026-10-28 at the end of a long session, so that a new chat can continue the same work straight away.
The owner works chapter by chapter: audit the existing questions of a chapter against the book PDF, fix them,
add the Traditional Method, add what is missing, then push to the live site when asked.

---

## 1. Project and environment

- Django 3.0 site, PostgreSQL. Repo root: `C:\Users\newwe\Desktop\tution\tutionplus`, Django project in `django/django_project`.
- **Always use the venv Python directly**: `env/Scripts/python.exe` (activating with bash picks the wrong Python).
  Add `-X utf8` (emoji prints in the code crash cp1252 otherwise).
- Run a script against the DB: `cd django/django_project && ../../env/Scripts/python.exe -X utf8 manage.py shell -c "exec(open(r'PATH').read(), {})"`.
  The `{}` is required (list comprehensions in an exec'd script lose their scope otherwise). Inputs are passed in that dict,
  e.g. `{'IDS': [...], 'DO_UPDATE': True}`. Filter the startup noise with `| grep -vE "^\[(CONFIG|OK)\]"`.
- Local dev server: the Browser pane config `.claude/launch.json` → name `django` (`runserver 8000 --noreload`, `-X utf8`).
  `--noreload` means **restart the server after any code change**.
- Local DB: `post` (PostgreSQL 12, user postgres; password is in Django settings, never print it).
- PDFs of the book ("Practice Book on Quicker Maths"): `C:\Users\newwe\Desktop\prompt for tutionplus\math\14\m tyra\`
  (e.g. `Alligation.pdf`, `Time and Distance.pdf`, `Time and Wor.pdf`, `Percentage.pdf`, `profit.pdf`, ...).
  The Read tool cannot render PDF pages here (no poppler): render with PyMuPDF (`fitz`, installed in env) to PNG at ~110 dpi and
  read the PNGs. The text layer garbles formulas, so read rules/answers from the images.

### Live server (only when the user asks to push)
- The server address, SSH alias, app/backup paths and the live database name are in **`claude/LIVE_SERVER.local.md`**
  (local only, not in git - the repo is public). Below, `LIVE_DB` = the live database (not `post`), `LIVE_BACKUP_DIR` = the server
  backup folder; the SSH alias `tutionplus-vps` is defined in the local SSH config.
- Code reaches live automatically: push to `main` on GitHub → GitHub Actions deploy (git reset, pip, migrate, collectstatic, restart).
  Check the deployed commit as shown in the local file.
- Nightly 02:00 backup on the server in `LIVE_BACKUP_DIR`.

---

## 2. Rules the owner set (follow them)

- **Local is the master copy.** Do all content work locally. Push to live **only when the user says so**, and never copy the
  whole DB to live again (it would wipe live users). Use the selective sync in section 6.
- **Back up before changing anything**: `claude/tools/backup_db.py` (full pg_dump to `db_backups/post_<date>.backup`), and the
  apply scripts also write per-row JSON backups to `claude/backups/`. Never overwrite an earlier backup.
- **Show the result** after each batch (what changed, keys fixed, checks passed) and let the user decide the next batch.
- Commit selectively. **Never commit**: `DEPLOYMENT_GUIDE.md` (secrets), `env/`, `db_backups/`, `claude/backups/`,
  book text or page images (`claude/runs/*/pages`, `pdf_text.txt`, `claude/test_run_chapter20`), `.claude/launch.json`.
  Ask before committing/pushing; the user usually says "commit and push".
- Never type passwords; if the user pastes credentials, do not use them.

---

## 3. Data model (what to touch)

- `bank.math` (table `bank_math`): `question`, `a`..`d` (`e` unused), `ans` (1-4), `solution`, `rule_based_explanation`,
  `shortcut`, `llm_used`, `rule` (FK → `rule_math`), `chapter` (e.g. `alligation_n_mixture`), `day`, `time` (seconds), `from_json`,
  `difficult_level` (mostly a meaningless default "easy"; do not change it - mock tests may use it).
- `bank.rule_math`: `chapter`, `rule_name` ("Rule N" - always this form), `rule_html` (the rule card). Translations in `rule_math_translation`.
- `bank.total_math` (row id 2): `total_<chapter>_page` = number of pages of the chapter. **The pager's "Next" stops here**, so after
  adding questions set it to `ceil(questions / 5)` (5 per page).
- `genai.JsonImport` (`to_table='math'`, `json_data` = `{"rules_html": [{chapter, rule_name, rule_html}], "questions": [...]}`) and
  `genai.MathPromptTemplate` (prompts: **#9** "time and distance_detail method + theorem" = default, **#10** "alligation and mixture_detail method + theorem").
- Chapter page view `bank/views.py` `math_all`: orders by **rule number** (digits of rule_name), then day, id; rule-less questions last
  (commit fa24e274). Template `bank/templates/home/math.html`; timer uses `{{math.time|default:30}}` (commit 0d0ffbff).
- Inserting questions: `genai.bulk_import.BulkImporter(table_name='math', json_data=..., form_date=..., form_time=...)` →
  `scan_math_conflicts(payload)` then `import_data(resolutions={})` - exactly what the admin "Insert" button does. It links questions to an
  **existing** card only if the payload's `rule_html` is identical to the stored one (otherwise it keeps the old card and reports a conflict);
  a missing card is created. It now also sets `time` via `estimate_math_seconds`.

---

## 4. The per-chapter workflow (what was done for Time and Distance and Alligation)

1. **Inventory**: questions per rule, questions with no rule card, which have a Traditional Method, rule cards present
   (script pattern: `claude/runs/alligation/page_map.py`, `claude/tools/chapter_inspect.py`, set CH to the chapter code).
2. **Book map**: render the chapter PDF, list which page each Rule is on, count each rule's worked example(s) + exercises, read the book answers.
3. **Prompt**: make a chapter version of prompt #9 (see `claude/runs/alligation/make_prompt.py`: keeps the shared text, swaps the chapter-specific
   visual / Traditional-Method / worked-example / JSON `chapter` sections, adds chapter traps). Save as a new `MathPromptTemplate`, **not default**,
   stored with `\r\n` line endings like the others.
4. **Rule by rule (batches of ~4-10 rules)**:
   - Dump rows: `claude/runs/alligation/dump_rows.py` (IDS, RULE, OUT_DIR) → `ruleNN/0_current_rows.json`.
   - Compare with the book: link old unlinked questions (often the book's worked examples) to their rule; note book exercises with no
     reworded copy in the DB → **add them** as new questions with changed numbers (prompt rule: digits must change, wording rewritten).
   - Re-solve every question by hand first, then with an **independent solver** (`ruleNN/solve.py`, or `solve_11_18.py` / `solve_19_28.py`):
     reads the numbers from the question text and solves by a different method (simulation, brute force, linear solve) - never the rule formula.
   - **Regenerate** solution / rule_based_explanation / shortcut with a generator (`rule01/gen.py`, `gen_5_10.py`, `gen_11_18.py`, `gen_19_28.py`,
     `rule29/gen.py`) using `claude/runs/alligation/common.py` + `claude/runs/td_new/gen_common.py`. Layout (prompt #9/#10):
     `<b>Theorem :</b>` + formula, `<hr>`, `<b>Traditional Method :</b>` (genuine first-principles solution, no rule), `<hr>`,
     `<b>Using the Specified Rule :</b>` steps, `<b>Verification:</b> Both methods give the same result.`, `∴ <b>Final Answer: ...</b>`.
     Shortcut = "Applying the specified Rule:" box; rbe = "Using the specified Rule:<br><b>Step 1:</b>...".
   - Validate: `claude/runs/alligation/validate.py N ...` (independent answer = generator answer, exactly one option holds it, key fixed if wrong,
     section order, HTML/LaTeX balance, no raw `<` in math, no LLM draft text like "Wait"/"mistakenly", Final Answer shows the value
     (ratios checked in order). New questions in `3_json_import_payload.json` + `3_answers.json` must already have the right key.
   - **Mutation-test** the validator on a copy (break an answer / key / ratio order / card) and confirm it fails.
   - Apply: `apply_rows.py` (RUN_DIR, LABEL, DO_UPDATE; row JSON backup, refuses rows changed since the dump), cards with `apply_cards.py`
     (replace/create, placeholder `NEW_RULE_N` → real id), card fixes `fix_card_escaping.py` (cards pasted as escaped JSON) and
     `fix_card_stray.py` (LaTeX outside `\( \)`), new questions with `save_and_insert.py` (N, DAY; saves JsonImport then inserts).
   - Check the pages: `claude/tools/check_order.py` (crawls the local site: every question once, rule order never goes back) and a browser look.
5. **After the chapter**: set `total_<chapter>_page`, report, wait for "push to live".

### Gotchas found (they cost time once)
- A raw `<` inside math in HTML (`\(x<z\)`) is read by the browser as a tag → write `\lt` / `\gt`.
- Consecutive `\[ ... \]` render on one line on this site → `common.tidy()` adds `<br>` after each display block.
- Git-Bash heredocs collapse `\\` → write any file containing regex/LaTeX backslashes with the Write tool, not `cat <<EOF`.
- Python 3.11: no backslash inside f-string `{...}` expressions (use a variable such as `TIMES = chr(92) + 'times'`).
- Substring traps in solvers: "ope**ratio**n" contains "ratio" → use `\b` word boundaries.
- Old/LLM data problems seen: keys always on option a, options copied from the book while numbers were changed, LLM thinking text left in
  solutions, cards stored as escaped JSON (`\"`, `\\(`), wrong variable definitions in a card, duplicate questions.
- Empty `time` used to break the timer (`timer(...,None,...)`); times are now 20 s easy / 30 s medium / 45 s hard from
  `estimate_math_seconds` (`claude/tools/time_score.py`, `apply_times.py`).
- The page always draws a 5th option from `math.e`: `''` gives an empty radio, NULL prints the word "None" (looks like an answer) → set `e = ''`
  on old rows (`claude/runs/time_work/fix_empty_e.py`).
- Solvers that turn number words into digits trip on "**Two** women, ...", "The **three** men together ..." → read digits only for those rows.
- `divmod` floors negatives, so a mixed-number formatter prints -21/2 as "-11 1/2" → format the absolute value and add the sign.
- Re-running an earlier generator after changing shared helpers can silently change applied rows → check with `compare_applied.py`.
- The book's printed shortcuts are not always right (Time and Work Rule 32 p-formula; some printed answers): trust the independent solver.

---

## 5. Status at handoff (2026-10-28)

- **Time and Distance** (`time_n_distance`, PDF "Time and Distance.pdf" / Chapter 18): Rules 1-49 done (audit + Traditional Method + new
  Rules 31-49), on live. 35 old rule-less questions now show last (pages 46-52). Work folders: `claude/runs/td_audit`, `claude/runs/td_new`.
- **Alligation** (`alligation_n_mixture`, `Alligation.pdf`): Rules 1-29 done, 169 questions, 29 cards, prompt #10, JsonImports #164-#172,
  page counter 34, **on live**. Work folder: `claude/runs/alligation` (one `ruleNN/` per rule).
- **Time and Work** (`time_n_work`, `Time and Wor.pdf` = book Chapter 15, pages 359-390): Rules 1-40 + the 18 Miscellaneous problems done
  and **on live** (pushed 2026-10-28 with the selective sync: 328 rows = 312 math, 7 cards, page counters, JsonImports #173-#179, prompt #11;
  live dump before the push `db_backups/live/tutionplus_before_time_work_sync_2026-10-28.backup`; SQL builder `claude/runs/time_work/build_sync.py`;
  live page check `claude/runs/time_work/live_check.py`). **Baseline for the next push: `db_backups/post_2026-10-28_2050.backup`** (local = live then). 302 questions, all linked to a rule, all with Theorem + Traditional Method + Specified
  Rule; 40 cards (Rule 32 "alternate days" card #139 created - built on counting two-day cycles, because the book's "nearest whole number
  p" shortcut is wrong for some numbers); prompt **#11** "time and work_detail method + theorem" (not default); JsonImports #173-#179
  (20 new questions: missing book exercises with changed numbers + Misc M4); page counter **61**. 15 wrong keys fixed (1322-1325, 1373-1376,
  232, 234, 250, 255, 268, and 261/262 which held `ans = 5`); cards fixed for Rules 1, 4, 19, 30, 33, 37; OCR/typo fixes in the 2018 book
  copies (181-277, e.g. 214 "13 men" -> "30 men", 275 lost "1/3"); empty option e set to '' (NULL printed "None"). The Miscellaneous rows
  are linked to the rule they use (Rules 1, 4, 6, 8, 9, 14, 28, 31). Work folder `claude/runs/time_work`: `book_map.json`, one `ruleNN/`
  per rule, `misc/ruleNN/` for the Miscellaneous run, generators `gen_1_4.py` ... `gen_36_40.py`, `gen_misc.py`, solvers `solve_*.py`,
  `validate.py` (also handles triples A/B/C, clock times as pairs, algebraic answers evaluated at x = 7, y = 3), `mutation_test.py`,
  `misc_check.py`, `compare_applied.py` (DB still equals every applied 2_new_rows.json). Last local backup: `db_backups/post_2026-10-28_2036.backup`.
- **Profit and Loss** got the 10 profit questions that had been filed under Time and Work (946-955, moved 2026-10-28, rule-less, not audited);
  its page counter is now 35 (on live). Its old rows still show many "None" 5th options (139 on live) and display math in options (79) - fix
  them when that chapter is audited (same treatment as Time and Work: `fix_empty_e.py`, inline fractions).
- **Timers**: every question has a time, on live.
- Open items the user has not decided: Alligation question 1074 duplicates 1071; Alligation Rule 28 answers mostly on option a
  (also noted earlier for Time and Distance Rules 15 and 18); the 5 "Miscellaneous" problems after Alligation Rule 29 are not added;
  one old question has a 1-second time; Hindi translation of Alligation Rule 1 card uses `$...$` math which the site does not render.
  Time and Work 239 and 244 are the same Rule 31 question (book prints it twice) - the user chose to **keep both**. Many Time and Work
  answer keys are on option a (Rules 3, 5, 9, 14) - all checked correct, left as they are.
- Other chapters with many questions still in the old style (no Traditional Method): `profit_n_loss`, `percentage`,
  `permutation_combination`, `average`, `ratio_n_proportion`, `simple_interest`, `pipe_cistern`, `partnership`, `compound_interest`,
  `problem_on_age`, `boats_n_stream`, `volume_n_surface_area`, `simplification`.

---

## 6. Pushing to live safely (when asked)

1. Back up live: `pg_dump -Fc` of `LIVE_DB` into `LIVE_BACKUP_DIR/<name>.dump` (exact command in `claude/LIVE_SERVER.local.md`),
   copy it to `db_backups/live/<name>.backup` (the `.backup` extension keeps it out of git).
2. Baseline = the last **local** backup taken right after the previous push, when local and live matched. Restore it into a scratch DB with
   `claude/tools/restore_baseline.py` (SRC, TARGET). The tools below expect the scratch DB name `post_baseline_0045`.
3. `claude/tools/threeway.py`: hashes every row (md5 of `to_jsonb`, timezone UTC) in baseline / local / live and classifies:
   push (changed only locally), keep live (changed only on live), CONFLICT (both) → stop and ask on any conflict.
4. `claude/tools/build_sync.py` (whole rows: `UPDATE ... FROM jsonb_populate_record` / `INSERT ... SELECT * FROM jsonb_populate_record`,
   then `setval`) - or a narrow SQL like `build_time_sync.py` when only one column changed. Check the push list is only what you expect.
5. Rehearse: restore the live dump on the server into `tutionplus_synctest` and `tutionplus_reference`, run the SQL with
   `psql -v ON_ERROR_STOP=1 --single-transaction`, then `claude/tools/verify_sync.py` (TARGET, REFERENCE): pushed rows must equal local,
   every other row unchanged.
6. Run verify_sync against live with the reference to prove live has not drifted, apply to `tutionplus` in one transaction, verify again,
   then crawl live pages (`check_order.py` with the live URL, `crawl_none.py`). Drop the scratch DBs afterwards.

---

## 7. Where things are

- Scripts: `claude/tools/` (backup, restore, three-way sync, page checks, timers, older Time and Distance insert/verify helpers) and
  `claude/runs/alligation/` (chapter workflow: dump, generators, solvers, validator, apply, cards, prompt builder).
- Backups: `db_backups/` (full local dumps, newest last), `db_backups/live/` (live dumps), `claude/backups/` (per-row JSON before each change).
- General project notes: `claude/PROJECT_OVERVIEW.md`.
