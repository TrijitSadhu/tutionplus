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
  live page check `claude/runs/time_work/live_check.py`). Baseline then: `db_backups/post_2026-10-28_2050.backup` (superseded - see Percentage). 302 questions, all linked to a rule, all with Theorem + Traditional Method + Specified
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
- **Percentage** (`percentage`, `Percentage.pdf`, 42 pdf pages = 77 rules + 31 Miscellaneous problems) - **Rules 1-77 on live**
  (pushed 2026-10-29 with the selective sync: 612 rows = 456 math (81 updates, 375 inserts), 77 cards #140-#216, page counter
  95, JsonImports #180-#256, prompt #12; one `django_admin_log` row differed on both sides and was left out (admin history, not
  content); live dump before the push `db_backups/live/tutionplus_before_percentage_sync_2026-10-29.backup`; SQL builder
  `claude/runs/percentage/build_sync.py`; the `bank/models.py` page-counter fix was pushed to GitHub with it).
  Baseline then: `db_backups/post_2026-10-29_1626.backup` (superseded - see Permutation and Combination).
  The Miscellaneous set (rows 662-679 + 13 missing problems) is **not done yet** - local work, next push.
  The chapter had no cards; rows 583-661 copy the book's worked examples, 662-679 copy Miscellaneous problems, 47/56 are 2018 rows.
  Prompt **#12** "percentage_detail method + theorem" (not default). Work folder `claude/runs/percentage` (`book_map.json`, `gen_1_8.py`,
  `solve_1_8.py`, same validate/apply/insert scripts as Time and Work). **Rules 1-8 done** (2026-10-28): cards #140-#147, 16 old rows
  regenerated and linked (keys fixed: 56 -> 5 questions, 596 -> 27%; display math and "o f" OCR cleaned; e = ''), 48 new questions
  (all book exercises of Rules 1-8 with changed numbers) in JsonImports #180-#187, ids 1683-1730. Book misprint: Rule 7 Exr 3 answer (b) is
  wrong (new price is Rs 15). Backup before the batch: `db_backups/post_2026-10-28_2247.backup`.
  **Rules 9-16 done** (2026-10-28, `gen_9_16.py`, `solve_9_16.py`): cards #148-#155, old rows 597-604 regenerated and linked (all keys
  were right; 599/602 options cleaned), 37 new questions in JsonImports #188-#195, ids 1731-1767. Backup before: `post_2026-10-28_2255.backup`.
  184 questions, page counter **37**. **Code bug fixed locally (not committed yet):** `total_math.save()` in `bank/models.py` recomputes
  every chapter's page counter on each save, and the percentage block used the profit_n_loss count (that is why it was 35). Saving
  row 2 now sets the percentage counter correctly (`claude/runs/percentage/save_page_counters.py`). Live still has the bug until it is pushed.
  **Rules 17-24 done** (2026-10-28, `gen_17_24.py`, `solve_17_24.py`): cards #156-#163, old rows 605-612 regenerated and linked (606 had
  no option holding Rs 576 - fixed; 607's "Rs 10001" option replaced), 36 new questions in JsonImports #196-#203, ids 1768-1803.
  Backup before: `post_2026-10-28_2307.backup`. 220 questions, page counter **44**.
  **Rules 25-32 done** (2026-10-28, `gen_25_32.py`, `solve_25_32.py`): cards #164-#171, old rows 613-620 regenerated and linked (all keys
  right; odd distractors 20001/18004/200005 replaced, 620's display-math options made inline), 34 new questions (incl. Rule 27's second
  worked example) in JsonImports #204-#211, ids 1804-1837. Backup before: `post_2026-10-28_2332.backup`. 254 questions, page counter **51**.
  **Rules 33-40 done** (2026-10-28, `gen_33_40.py`, `solve_33_40.py`): cards #172-#179, old rows 621-628 regenerated and linked (625 had no
  option holding "4.5% increase" - fixed; 624/625 options now say Increase/Decrease), 53 new questions (incl. 5 worked examples of Rules
  36-37) in JsonImports #212-#219, ids 1838-1890. `validate.py` got an answer kind **"signed"** (options/answers that say increase/decrease,
  profit/loss; the Final Answer must show the size AND the right direction word) and `mutation_test.py` a matching `m_direction`.
  Backup before: `post_2026-10-28_2341.backup`. 307 questions, page counter **62**.
  **Rules 41-48 done** (2026-10-28, `gen_41_48.py`, `solve_41_48.py`): cards #180-#187, old rows 629-636 regenerated and linked; keys fixed:
  635 (was 31%, right 21%), 634 (no option held 37.5%), 631 (NULL option, none held 6.25% fall), 630 ("8%" vs "-8%" - now "Decrease of 8%");
  Rules 42-47 (effect on a product) are "signed" answers with Increase/Decrease options. 37 new questions (incl. worked examples of Rules 42
  and 48) in JsonImports #220-#227, ids 1891-1927. Book misprint: Rule 48 Exr 4 answer (a) 300 is wrong (250). Backup before:
  `post_2026-10-28_2350.backup`. 344 questions, page counter **69**.
  **Rules 49-56 done** (2026-10-29, `gen_49_56.py`, `solve_49_56.py`): cards #188-#195, old rows 637 (R49 - a copy of Exr 5, not the
  worked example), 638 (R53), 639 (R54), 640 (R55), 641 (R56) regenerated and linked (all keys right); Rules 50-52 had no rows at all.
  44 new questions (incl. worked examples of Rules 49-52) in JsonImports #228-#235, ids 1928-1971. Rule 50 (area error) is "signed" with
  excess/deficit words (added to `validate.py`); `mutation_test.py` skips row mutations for rules with no old rows and gained
  `m_new_answer` / `m_new_option`. Book misprint: Rule 56 Exr 5 numbers are inconsistent (answer not a whole number). Backup before:
  `post_2026-10-29_0001.backup`. 388 questions, page counter **78**.
  **Rules 57-64 done** (2026-10-29, `gen_57_64.py`, `solve_57_64.py`): cards #196-#203, old rows 642-649 regenerated and linked (642 had no
  option holding Rs 25 - fixed; 646's rounded "80.76%" written exactly as 80 10/13%), 31 new questions in JsonImports #236-#243, ids
  1972-2002. Book misprints: Rule 62 Exr 3 and 4 divide by the OLD price (right answers 38 8/9% and 25%). Backup before:
  `post_2026-10-29_0010.backup`. 419 questions, page counter **84**.
  **Rules 65-72 done** (2026-10-29, `gen_65_72.py`, `solve_65_72.py`): cards #204-#211, old rows 650-656 regenerated and linked (all keys right;
  650 had a NULL option, 655's "failed = .., passed = .." options reduced to the pass % asked); Rule 70 had no row. 35 new questions (incl.
  Rule 70's worked example) in JsonImports #244-#251, ids 2003-2037. The book rounds Rule 68 Exr 1 (32.825%) and Rule 69 Exr 1 (27.325%).
  Backup before: `post_2026-10-29_0021.backup`. 454 questions, page counter **91**.
  **Rules 73-77 done** (2026-10-29, `gen_73_77.py`, `solve_73_77.py`): cards #212-#216, old rows 657-661 regenerated and linked (660 had no
  option holding 24 kg - fixed; 657 reworded to ask for both incomes its options give), 20 new questions in JsonImports #252-#256, ids
  2038-2057. Backup before: `post_2026-10-29_0030.backup`. **All 77 rules done:** 474 questions, 154 cards, page counter **95**.
  Left: the 31 Miscellaneous problems (18 in the DB as rule-less rows 662-679, shown last on pages 92-95; 13 not in the DB).
- **Permutation and Combination** (`permutation_combination`, `permutaion combination.pdf` = book Chapter 25, pages 641-661, 21 pdf pages)
  - **in progress, local only**. The book has two series, I. Permutations Rules 1-13 and II. Combinations Rules 1-23; on the site
  they are **Rule 1-13 and Rule 14-36** (site = book Combination rule + 13; the owner chose this 2026-10-29). Miscellaneous: 2
  problems (3 questions). Work folder `claude/runs/permutation` (`book_map.json` has every rule's page, exercise answers, misprints and
  DB copies; `validate.py` here evaluates counting expressions such as `\frac{9!\times 8!}{3!}`, `{}^{15}C_{3}`, `2(4!\times 4!)` exactly
  - `pc_value`; solvers count by brute force / seating-pattern enumeration). Prompt **#13** "permutation combination_detail method +
  theorem" (not default). The 6 profit-and-loss rows 957-962 that were filed here were moved to `profit_n_loss` (now 179 questions,
  page counter 36; backup `claude/backups/math_957_962_before_move_to_profit_n_loss.json`). The chapter had 70 rows (2019), no cards:
  845-873 copy the book's worked examples, 874-914 are general P&C questions from other sources (link each to its nearest rule).
  Book misprints: P Rule 6 Exr 1 (72 -> 84, not an option) and Exr 3 (240234x9! -> 239520x9!); P Rule 10 Exr 1 and 3 say "two
  particular delegates" but answer for 3 and 5; C Rule 7 Exr 2 ("3, 20" -> 15, 20) and Exr 3 (4290 -> 12870); C Rule 5 Exr 2 needs a figure.
  Old rows still to fix in later batches: 862 (40 lines, no option), 905 (25, no option), 875 (number of students lost: 15), 912 = 858.
  **Rules 1-7 done** (2026-10-29, `gen_1_7.py`, `solve_1_7.py`): cards #217-#223, 19 old rows regenerated and linked (845, 885, 891,
  893, 894, 899, 903 / 846, 897, 898, 904, 914 / 847, 887, 902 / 848 / 849 / 850 / 851); key fixed: 894 (ans 5 -> 9900, option added);
  903's duplicate 720 option replaced; `$$` and display math cleaned; e = ''. 25 new questions (book exercises of Rules 1-7 + Rule 4's
  2nd worked example, numbers changed) in JsonImports #257-#263, ids 2058-2082. Backup before: `db_backups/post_2026-10-29_1726.backup`.
  95 questions, page counter **19**.
  **Rules 8-13 done** (2026-10-29, `gen_8_13.py` reuses `gen_1_7.main`; `solve_8_13.py` counts words with a memoised letter-by-letter
  count, circles by seat patterns / rotations, necklaces with bead 0 fixed and one of each mirror pair): cards #224-#229, 16 old rows
  regenerated and linked (852, 901 / 853, 908 / 854, 909 / 888, 890, 892, 895, 896, 907 / 881, 882, 886, 889; all keys were right, options
  written as LaTeX); Rule 8 had no row. 28 new questions (worked examples of Rules 8, 12 (two) and 13 + all exercises, words / numbers
  changed; Rule 10 Exr 1 and 3 rewritten with three / four particular delegates) in JsonImports #264-#269, ids 2083-2110. Backup before:
  `post_2026-10-29_1741.backup`. 123 questions, page counter **25**. Cosmetic: Rule 13's Theorem display formula is a little wider than the
  solution box on desktop (shorten it if the owner wants; the 9 Rule 13 rows and card #229 would need a re-apply).
  **Rules 14-21 done** (= book Combination Rules 1-8; 2026-10-29, `gen_14_21.py`, `solve_14_21.py` counts real selections with
  itertools.combinations): cards #230-#237, 16 old rows regenerated and linked (855, 876, 905, 906 / 856, 911 / 857, 875, 913 / 858, 912 /
  859, 874 / 860, 910 / 861); Rule 14 had no row. Fixed: 905 (key on the empty option e, no option held 25 - added), 875 (number of
  students lost - 15 restored), 855 ("10 identical boxes" -> "10 different boxes", the answer 252 needs it; the book has the same slip).
  912 still duplicates 858 (both kept, owner to decide). 26 new questions (Rule 14's and Rule 18's worked examples + all exercises,
  numbers changed; Rule 18 Exr 2 written without the figure; Rule 20 Exr 2/3 with right answers) in JsonImports #270-#277,
  ids 2111-2136. Backup before: `post_2026-10-29_1759.backup`. 149 questions, page counter **30**.
  **Rules 22-29 done** (= book Combination Rules 9-16; 2026-10-29, `gen_22_29.py`, `solve_22_29.py`): cards #238-#245, 14 old rows
  regenerated and linked (862 / 863 / 864 / 865, 877 / 866, 879, 880, 883, 884, 900 / 867 / 868 / 869). Fixed: 862 (key on the empty
  option e, no option held 40 - added), 864 ("can't student fail"), 868 (display-math options inline). 29 new questions (all exercises,
  numbers changed) in JsonImports #278-#285, ids 2137-2165. `validate.py` gained a **stray-LaTeX check** (`\frac`, `^{`, `{}^` outside
  `\( \)` - an 880 draft had it) and `mutation_test.py` a matching `m_stray`; Rules 1-29 all pass it. Backup before:
  `post_2026-10-29_1809.backup`. 178 questions, page counter **36**.
  **Rules 30-36 + Miscellaneous done - CHAPTER COMPLETE locally** (2026-10-29, `gen_30_36.py`, `solve_30_36.py`): cards #246-#252, old rows
  870, 878, 871, 872, 873 regenerated and linked (keys right); 24 new questions (Rule 31/35/36 worked examples + all exercises, numbers
  changed) in JsonImports #286-#292, ids 2166-2189; the 2 Miscellaneous problems (3 questions, 'at least' committees, numbers changed)
  under Rule 26 in `misc/rule26` (card #242 reused), JsonImport #293, ids 2190-2192. Backup before: `post_2026-10-29_1818.backup`.
  **Final state: 205 questions, 36 cards (#217-#252), every row linked to a rule, Theorem + Traditional Method in every solution,
  e = '' everywhere, no `$$`, answers spread a 51 / b 49 / c 55 / d 50, page counter 41; JsonImports #257-#293; prompt #13.**
  **On live** (pushed 2026-10-29 with the selective sync: 286 rows = 211 math (76 updates incl. the 6 rows moved to profit_n_loss,
  135 inserts), 36 cards, page counters (P&C 41, profit_n_loss 36), JsonImports #257-#293, prompt #13; no conflicts; live dump before the
  push `db_backups/live/tutionplus_before_permutation_sync_2026-10-29.backup`; SQL builder `claude/runs/permutation/build_sync.py`).
  Baseline then: `db_backups/post_2026-10-29_1823.backup` (superseded by `post_2026-10-29_2007.backup`, see the new chapters below).
  Scripts committed in `f86a3496`.
  Open items: 912 duplicates 858 (owner to decide); Rule 13 Theorem display formula slightly wide.
- **Rewording (copyright) - pilot done locally 2026-10-29, not on live:** 10 Time & Work rows (1232, 1255, 1258, 1268, 1292, 1296,
  1306, 1311, 1323, 1397) got a fresh sentence + all-new numbers + new options, explanation regenerated with the same rule generator;
  same row ids / rules. Work area `claude/runs/time_work/reword/` (`gen_reword_pilot.py`, `reword_check.py` = validate with the gate
  on + mutation test incl. m_copy / m_old_number). Gate: `claude/tools/originality.py` (book wording <= 0.35 of 4-word phrases,
  sentence vs the old question <= 0.55, no number > 3 kept from the old question, not the full number set of one book sentence).
  Today 295 of 302 Time & Work questions fail the gate. Backup before: `post_2026-10-29_2014.backup`.
  **Batch 1 done locally** (Rules 1-5, 47 rows; `reword/b1/gen_b1.py`, solver `reword/solve_rw.py` keyed by row id - label-based
  for toys/trees; number sets chosen with `Book.numbers_together` so no book sentence has them). Backup before:
  `post_2026-10-29_2033.backup`. Left: Rules 6-40 (~228 rows) + the Miscellaneous rows (261-277, 1682) in their own batch.
  Pilot moved to `reword/pilot/`; `reword_check.py <batch>` runs validate (gate on) + mutations (incl. m_copy, m_old_number).
  **Batch 2 done locally** (Rules 6-10, 50 rows; `reword/b2/gen_b2.py`; shared option builder `reword/rw_common.py`; solvers for
  men/women/boys/children read numbers by label so sentences can be reordered; `try_q.py` tests draft sentences against the gate
  first). Backup before: `post_2026-10-29_2125.backup`. Slip found and fixed: rows 203 and 1263 were applied with doubled backslashes
  (raw LaTeX on the page) - fixed in the DB (`b2/fix_backslash.py`, backup `claude/backups/math_203_1263_before_backslash_fix.json`)
  and `time_work/validate.py` now fails any doubled backslash (+ mutation `m_double_backslash`). `reword/compare_batches.py`
  confirms the DB equals every applied batch file (pilot 10, b1 47, b2 50 rows). Note: the Theorem lines of some
  rules (e.g. Rule 18) still follow the book's theorem sentence - owner to decide whether to reword those too.
  **Batch 3 done locally** (2026-10-29, Rules 11-20, 51 rows; `reword/b3/gen_b3.py`; batch-3 solver types in `reword/solve_rw.py`,
  label-based `k_faster`/`k_hours`/`k_c13q`/`k_good`/`k_mwb`/`k_builder`, search-based `k_left`/`k_absent`/`k_extra`). All 51 pass the
  gate; validate 0 failed, all mutations caught (pilot/b1/b2 re-checked too). Backup before: `post_2026-10-29_2143.backup`.
  `compare_batches.py` (BATCHES pilot..b3): DB equals all 158 applied rows; no doubled backslash in any time_n_work row; check_order
  OK (302 shown); pages 23-34 have no raw LaTeX or MathJax errors. Left: Rules 21-40 (~127 rows) + the Miscellaneous rows (261-277, 1682).
  **Simple style (owner, 2026-10-29 late: the reworded sentences read "too tough").** The reworded rows keep their new numbers,
  options, keys and explanations; only the question sentence goes back to the book's easy pattern with the job/object changed
  ("If 6 men or 8 women can paint a wall in 35 days, ..."). Gate `originality.check_question(..., simple=True)`: book wording <= 0.70,
  vs the old question <= 0.90, same number rules (a numbers-only copy of the book sentence scores ~0.86/0.97 - all 158 such copies are
  rejected). `validate.GATE_SIMPLE`, set by `reword_check.py simple/<batch>`. Folder `reword/simple/`: `<batch>_sentences.py` (SIMPLE =
  {id: sentence}, numbers in the solver's order), `make_simple.py <batch>`, `apply_simple.py` (BATCH, DO_UPDATE; refuses rows that
  differ from the applied batch, changes question + llm_used only). `compare_batches.py` checks the simple version when it exists.
  **Pilot (10) and batch 1 (47) done** - backup before: `post_2026-10-29_2203.backup`, row backups `math_time_work_simple_<batch>_before.json`.
  **Batches 2 (50) and 3 (51) done** - backup before: `post_2026-10-29_2216.backup`. All 158 reworded rows are now in the simple style;
  compare_batches: DB equals every simple batch file; check_order OK. Write Rules 21-40 and the Miscellaneous rows in the simple
  style directly (gen_bN.py sentences, `reword_check.py` with the simple gate).
  **Batch 4 done locally** (2026-10-29, Rules 21-30, 52 rows; `reword/b4/gen_b4.py`, written in the simple style straight away; a
  `SIMPLE_STYLE` marker file in the batch folder makes `reword_check.py` use the simple gate; each `ruleNN/solve.py` imports the
  original `solve_21_30` solver, so the numbers keep the book's order). Validate 0 failed, all mutations caught. Backup before:
  `post_2026-10-29_2230.backup`. compare_batches (pilot..b4, 210 rows) equal to the DB; check_order OK; pages 35-45 clean.
  Left: Rules 31-40 (74 rows) + the Miscellaneous rows (261-277, 1682).
  **Batch 5 done locally** (2026-10-29, Rules 31-40, 74 rows incl. Claude-added 1668-1681; `reword/b5/gen_b5.py`, simple style,
  SIMPLE_STYLE marker; original `solve_31_35` / `solve_36_40` solvers, so each sentence keeps the phrase they use to tell the types
  apart: "assist", "C finishes it", "helped on every", "C joins A", "joined B", "days less than B", "help of C", "B starts",
  "working together", "B and C start", "together", "In all"). `rw_common.write_batch` now takes a ready options dict in place of the
  unit (Rule 32 clock times and dates). Traps found: `helped31` needs a whole number of k-day cycles; solve32 treats any " am" as a
  clock question (a worker named "Amit" broke it - renamed). 239/244 (same book question, both kept) got different numbers.
  Backup before: `post_2026-10-29_2339.backup`. compare_batches (pilot..b5, 284 rows) equal to the DB; check_order OK; pages 45-61 clean.
  **All 284 regular Time & Work rows are reworded.** Left: the 18 Miscellaneous rows (261-277, 1682).
  **Miscellaneous done locally** (2026-10-29, 18 rows; `reword/misc/gen_misc_rw.py` = the `gen_misc.py` generators rewritten with
  parameters (they had the book's numbers built in), same layout; solver `reword/misc/solve_misc_rw.py` = `solve_misc` + 274 with any
  two fractions + 1682 read as "m4"; SIMPLE_STYLE marker). Backup before: `post_2026-10-29_2355.backup`.
  **TIME & WORK REWORDING COMPLETE (local only):** all 302 rows have a reword note, compare_batches (pilot..misc) equal to the DB,
  check_order OK, all 61 pages have balanced LaTeX, no doubled backslash, no NULL option e.
  **ON LIVE** (pushed 2026-10-30 00:12 with the selective sync: three-way from `post_2026-10-29_2007.backup` gave exactly 302
  bank_math push rows, all time_n_work, no conflicts; SQL builder `reword/build_sync_reword.py` (updates only, refuses anything else);
  rehearsal on tutionplus_synctest 302/302 equal to local, 0 other rows changed; live verified 302/302, 0 other rows changed; live crawl
  `live_check.py` 302 of 302 shown, 0 'None' options; live dump before the push
  `db_backups/live/tutionplus_before_time_work_reword_sync_2026-10-30.backup`; scratch DBs dropped).
  **Baseline for the next push: `db_backups/post_2026-10-30_0013.backup`** (taken right after this push). Scripts not committed yet.
  Next: reword the other audited chapters (Alligation, Time & Distance, Percentage, P&C) the same way, in the simple style.
- **Alligation rewording (2026-10-30, local only):** 134 of the 169 rows fail the simple gate against `alligation/pdf_text.txt`
  (94 wording, 11 book number sets, 29 both); the other 35 already differ from the book and are left as they are.
  Tooling `claude/runs/alligation/reword/` = the Time & Work tools pointed at Alligation (`rw_common.py`, `dump_batch.py`,
  `compare_batches.py`, `try_q.py`, `reword_check.py` - always the simple gate, Time & Work mutations + m_copy / m_old_number /
  m_double_backslash); `alligation/validate.py` got the GATE hook and the doubled-backslash check (Rules 1-29 still pass).
  Each batch rule folder's `solve.py` loads the applied rule solver by absolute path and turns a solver crash into "unsolved"
  (rule02 also maps rows 1641-1649 to their payload keys E1-E9). The solvers are keyed by row id and read numbers in order, so
  the new sentences keep each row's number order (Rule 1 "basic" rows exactly three numbers; Rule 3 only three numbers).
  **Batch 1 done** (Rules 1-5, 45 rows; `reword/b1/gen_b1.py` calls the rule generators with new numbers). Backup before:
  `post_2026-10-30_0029.backup`. compare_batches equal; check_order OK (169 shown); all 34 pages balanced LaTeX.
  Left: Rules 6-29 (89 rows: R6 1, R7-R10 20, R11-R12 2, R13-R16 13, R17 5, R18 1, R19-R22 16, R23-R29 31).
  **Batch 2 done** (Rules 6-16, 36 rows; `reword/b2/gen_b2.py` with the `gen_5_10` / `gen_11_18` builders; sentences keep the
  solver phrases "kilolitre", "water to milk", "each litre", "by bus?" / "by train?", "ratio", "respectively", "chickens and goats",
  "How many rabbits/pigeons"). Backup before: `post_2026-10-30_0036.backup`. compare_batches b1+b2 equal; check_order OK; 34 pages clean.
  Left: Rules 17-29 (53 rows: R17 5, R18 1, R19-R22 16, R23-R29 31).
  **Batch 3 done** (Rules 17-22, 22 rows; `reword/b3/gen_b3.py`; Rule 17 solver reads only a:b ratios or \(p\%\), Rule 19 every
  "<n> litres", plain "p%" and "<n> litres of water is added", Rule 21 "whisky"). Small ratio digits (4-7) often repeat an old
  number or form a book set - searched sets instead. Backup before: `post_2026-10-30_0043.backup`. compare_batches b1-b3 equal;
  check_order OK; 34 pages clean. Left: Rules 23-29 (31 rows).
  **Batch 4 done** (Rules 23-29, 31 rows; `reword/b4/gen_b4.py`; `released` / `capacity` only accept ratios from their own square
  table, so the new ratios come from it; Rule 28 uses a new solver `reword/b4/solve28_rw.py` (draw-by-draw, reads "<word> times in
  all" and fraction words) - the book solver only knew three fraction words and the counts 2/3/5; a helper file must not start with
  "rule" (reword_check takes every rule* entry as a rule folder)). Backup before: `post_2026-10-30_0050.backup`.
  **ALLIGATION REWORDING COMPLETE (local only):** 134 rows reworded in 4 batches; all 169 rows now pass the simple gate against the
  book (0 failing); compare_batches b1-b4 equal to the DB; check_order OK (169 shown); all 34 pages balanced LaTeX. Not on live, not
  committed. The next push = selective sync from baseline `post_2026-10-30_0013.backup` (only alligation_n_mixture math rows expected).
- **Time & Distance rewording - started 2026-10-30, nothing changed in the DB yet.** Book text extracted to
  `claude/runs/td_reword/pdf_text.txt` (never commit). 121 of 260 rows fail the simple gate (59 wording, 39 book number sets,
  23 both; 26 of them rule-less). Unlike Alligation there are NO parameterised generators for Rules 1-30 (the audit only inserted
  hand-written Traditional Methods; `td_new/gen_*.py` have their data built in), so each failing row needs a new builder
  (Theorem reused from the row, Traditional Method + Specified Rule built from the new numbers) and an independent solver.
  Toolkit `claude/runs/td_reword/` set up: `common.py`, `dump_rows.py`, `apply_rows.py`, `validate.py` (copies of the Alligation
  ones, chapter time_n_distance) and `reword/` (rw_common, dump_batch, compare_batches, reword_check, try_q). Batch 1 = Rules 1-3
  (27 rows) dumped to `reword/b1/` - next: write `b1/gen_b1.py` builders + solvers, check, apply. Note: the dump's `rule_card`
  has no `rule_name` key (use the folder's rule number).
  **Batch 1 done locally** (2026-10-30, Rules 1-3, 27 rows; `reword/b1/gen_b1.py` = new builders `dist_st`, `time_ds`, `speed_dt`,
  `kmh_to_ms`, `ms_to_kmh`, `metres_to_kmh`, `compare`, `signal`, `wheel`, `sound`, `prop_dist`, `kmh_min_to_m`, `new_speed`,
  `avg_speed`, `return_speed`, `rests`, `rests_every` (Theorem lines kept, 1442's names its new interval); independent solver
  `reword/b1/solve_b1.py` (metres/seconds, simulated trips, minute-by-minute walking); SIMPLE_STYLE marker; times answered as
  pairs "h hrs m min" written in `\text{}` inside math). Backup before: `post_2026-10-30_0223.backup`. compare_batches equal;
  check_order OK (260 shown); all 52 pages balanced LaTeX. Left: 94 failing rows - Rules 4-11 (21), 14-29 (24), 34-48 (23) and
  the 26 rule-less rows.
  **Batch 2 done** (Rules 4-11, 21 rows; `reword/b2/gen_b2.py`: `late_early`, `still_late`, `there_back`, `halves`, `head_start_meet`,
  `late_start_total` (new Theorem for 1468), `slow_walk`, `catch_up`; solver `b2/solve_b2.py` searches for the distance). Backup
  before: `post_2026-10-30_0231.backup`.
  **Batch 3 done** (Rules 14-29, 23 rows; `reword/b3/gen_b3.py`: `meet_return`, `cross_times` (rule step shows \(\sqrt{b/a} : 1\)),
  `two_speeds_gap`, `round_uniform`, `fog`, `walk_ride`, `cross_after`, `inverse_speed`, `rest_speed`, `ride_walk`, `air_train`,
  `early_slow`; solver `b3/solve_b3.py` - 1487/1488 in two stages, 1520 by a linear root: stepping a solver in small time steps
  was not exact). Backup before: `post_2026-10-30_0238.backup`.
  **Batch 4 done** (Rules 34-48, 24 rows; `reword/b4/gen_b4.py`: `faster_slower`, `avg_dist_time`, `avg_dist_speed`, `avg_time_speed`,
  `faster_time`, `split_two`, `frac_distance`, `thief`, `ratio_times` (pair answer, plain options), `frac_avg`, `hare`; solver
  `b4/solve_b4.py` searches speeds/distances that make the story's times agree, counts leaps). First drafts kept the old sentence
  frame and failed "too close to the old question" - rebuilt the sentence order. Backup before: `post_2026-10-30_0247.backup`.
  **Batch 5 done** (the 26 rule-less 2018 rows 801-816, 825-834; `reword/b5/gen_b5.py` loads the b1-b3 builders and adds
  `meet_later` (R9), `later_faster` (R11), `ride_both` (R20), `meet_second_later` (R21), `halt` (R24), `late_flight` (R28); its own
  write loop links every row to its rule card - 801-805 R1, 806-807 R2, 808 R3, 809 R4, 810 R5, 811 R6, 812 R7, 813 R8, 814 R9,
  815 R10, 816 R11, 825 R20, 826 R21, 827 R22, 828 R23, 829 R24, 830 R25, 831 R26, 832 R27, 833 R28, 834 R29; e = '' (was NULL,
  printed "None"); Theorem + Traditional Method + Specified Rule in each). Old keys that were wrong: 834 pointed at option e and no
  option held the answer (24 km/hr); 831 had two "20 km" options; 813/814 asked "how far and at what time" with time-only options
  (now ask the distance). `td_reword/validate.py` now reports an old key on option e instead of crashing. Backup before:
  `post_2026-10-30_0257.backup`.
  **TIME & DISTANCE REWORDING COMPLETE (local only):** 121 rows reworded in 5 batches; all 260 rows pass the simple gate against the
  book (0 failing); compare_batches b1-b5 equal to the DB; check_order OK (260 shown, rule order never goes back); all 52 pages
  balanced LaTeX, no doubled backslash. Not on live, not committed. Still rule-less and old style (they pass the gate, so left as
  they are - owner to decide): 817-824 and 835, shown last on pages 51-52 with a "None" 5th option (NULL e). 818's key is on
  option e and no option holds the right answer (19.5 km); **835 is a junk test row** ("zzzz..." question, option a "None").
  The next push = selective sync from baseline `post_2026-10-30_0013.backup` (alligation_n_mixture + time_n_distance math rows).
- **Percentage rewording (2026-10-30 early morning, local only - IN PROGRESS):** 312 of 474 rows failed the simple gate against
  `percentage/pdf_text.txt` (mostly the Claude-added rows, which changed the book's numbers but kept its sentences). Tooling
  `claude/runs/percentage/reword/` (rw_common with an option builder that takes the row's formatter P / Rs / Num / ..., dump_batch,
  compare_batches, reword_check, try_q); `percentage/validate.py` got the GATE hook + doubled-backslash check (Rules 1-77 still
  pass) and `mutation_test.m_direction` now also swaps excess/deficit. Each batch calls the gen_X_Y.py builders with new numbers;
  each rule folder's solve.py wraps the original solve_X_Y solver in try/except (a mutated question must count as unsolved, not
  crash the check). Number sets are searched with a scratch grid search against `Book.numbers_together` - the Percentage book is
  dense with round per cents, so most triples of common per cents are a "book set". Solver phrases to keep: see each gen_bN.py
  docstring (e.g. Rule 25-30 verbs grows/rises/falls/increased/decreased - not "rose"/"fell"; plain-digit "x% in excess" for
  Rules 50-52; "gets N marks and fails by M" for Rule 48). Batches applied (backup before each): b1 Rules 2-8 (25 rows,
  `post_2026-10-30_0306`), b2 Rules 12-16 (27, new label solver `b2/solve_b2.py`, `_0313`), b3 Rules 18-24 (23, `_0318`), b4 Rules
  25-32 (31, `_0325`), b5 Rules 33-37 (34, `_0330`), b6 Rules 41-48 (35, extra product contexts fare/wage/rent/crop/shop, `_0336`),
  b7 Rules 49-56 (49, `_0346`), b8 Rules 57-64 (28, sentences in `b8/sent_b8.py`, `_0352`), b9 Rules 65-76 (46, `b9/sent_b9.py`,
  `_0358`). **298 rows reworded; every rule row of Rules 1-77 now passes the gate** (460 of 474 pass); compare_batches b1-b9
  equal to the DB; check_order OK (474 shown); pages 1-91 balanced LaTeX, no "None" option, no doubled backslash.
  **Not reworded on purpose:** the 14 failing rule-less Miscellaneous rows (662-668, 670, 671, 673, 674, 676, 678, 679) - they
  belong to the planned Percentage Miscellaneous job (START_HERE section 1: link to rules, fix keys, add the 13 missing problems,
  owner approval first); several need real fixes (663/664/667 offer "Data inadequate", 673 has "30% of 80" in display math,
  pages 92-95 still show "None" 5th options). Not on live, not committed.
- **P&C rewording COMPLETE (2026-10-30 ~04:10, local only):** 43 of 205 rows failed the simple gate against
  `permutation/pdf_text.txt`; all reworded in 2 batches, **all 205 now pass**. Tooling `claude/runs/permutation/reword/` (copies of
  the Percentage reword tools); `permutation/validate.py` got the GATE hook + doubled-backslash check (Rules 1-36 still pass).
  The gate counts every digit except 1, 2, 3 - including 0 - so the digit questions of Rules 2-3 use digit sets without any old
  digit above 3 and without 0 (Rule 2 case tables written in `b1/gen_b1.py`; 2068 became a plain "4-digit numbers with repeats"
  question because its range form needs 0). b1 = Rules 2, 3, 13, 16, 26, 27 (20 rows, brute-force solver `b1/solve_b1.py` keyed by
  row id; backup before `post_2026-10-30_0408`), b2 = Rules 30, 32-36 (23 rows, original solve_30_36 solvers; `_0411`).
  compare_batches b1-b2 equal; check_order OK (205 shown); all 41 pages balanced LaTeX, no "None" option.
- **ALL FIVE AUDITED CHAPTERS ARE NOW REWORDED** (Time & Work on live; Alligation, Time & Distance, Percentage Rules 1-77 and
  P&C local only). The next push = selective sync from baseline `post_2026-10-30_0013.backup`: expected only bank_math rows of
  alligation_n_mixture, time_n_distance, percentage and permutation_combination (updates, plus the 26 T&D rows that now have a
  rule link). Scripts of all four chapters not committed yet.
- **Profit and Loss audit (`profit_n_loss`, `profit.pdf` = book Chapter 10, 54 pdf pages = 89 rules + Miscellaneous) - STARTED
  2026-10-30 morning, local only.** Inventory: 179 old rows, none linked to a rule, 5 keys on option e (308, 312, 319, 391, 400),
  duplicate pairs 283/918, 285/920, 286/924, 287/923, 288/925, 302/306 (and 282/917, 284/919 near-copies), empty / duplicate
  options in several rows, a stray card **#114 "Rule 29: Early Departure with Reduced Speed"** (a Time & Distance card) filed under
  profit_n_loss and used by nothing - replace or delete it when Profit Rule 29 is done. Work folder `claude/runs/profit`
  (`pdf_text.txt` + `pages/` = book, never commit; toolkit copied from Percentage: common, dump_rows, apply_rows, apply_cards,
  save_and_insert, save_page_counters, validate, mutation_test (m_direction also swaps "a gain"), compare_applied;
  `gate_check.py N...` = the simple originality gate on regenerated rows AND new payload questions). Prompt **#14**
  "profit and loss_detail method + theorem" (from prompt #9 by `make_prompt.py`, not default; adds the simple-style /
  all-new-numbers line). Every old row copies the book, so the audit rewrites it in the simple style with all-new numbers
  straight away (gate on), and new questions (book exercises with no copy) are written the same way.
  **Rules 1-3 done** (`gen_1_3.py`, `solve_1_3.py`): cards #253-#255, 28 old rows (278-289 + 916-931; the duplicate pairs got
  different numbers), 5 new questions (JsonImports #294-#295, ids 2199-2203). Backup before: `post_2026-10-30_0755.backup`.
  **Rules 4-7 done** (`gen_4_7.py`, `solve_4_7.py`): cards #256-#259, 27 old rows (290-293 + 932-954), no new questions (every
  exercise had a copy). Backup before: `post_2026-10-30_0802.backup`. (Its mutation test was finished right after the apply - the
  first run stopped on the missing "a gain" swap; all mutations caught.)
  **Rules 8-12 done** (`gen_8_12.py`, `solve_8_12.py`): cards #260-#264, 8 old rows (294-300, 955), 23 new questions (JsonImports
  #296-#300, ids 2204-2226). Backup before: `post_2026-10-30_0808.backup`. 207 questions, page counter **42**; compare_applied
  Rules 1-12 equal; check_order OK.
  **Rules 13-17 done** (`gen_13_17.py`, `solve_13_17.py` - the chain solvers solve the linear price chain from two trial costs;
  a 10^7-step search was far too slow for the mutation test): cards #265-#269, 11 old rows (301-308; 355-357 are discount /
  mark-up rows that use Rule 13; fixed: 306 had no option holding the answer, 308's key was on option e, 355 had four empty
  options), 20 new questions (JsonImports #301-#305, ids 2227-2246). Backup before: `post_2026-10-30_0826.backup`.
  227 questions, page counter **46**.
  **Rules 18-21 done** (`gen_18_21.py`, `solve_18_21.py`): cards #270-#273, 6 old rows (309-313, 957; 312's key was on option e),
  18 new (JsonImports #306-#309, ids 2247-2264). Backup before: `post_2026-10-30_0831.backup`.
  **Rules 22-24 done** (`gen_22_24.py`, `solve_22_24.py`): cards #274-#276, 7 old rows (314-317, 958-960; 315 was the book's
  "can't be determined" exercise, now solvable with the new numbers; 959 was a garbled Rs 5 copy), 15 new (JsonImports
  #310-#312, ids 2265-2279). The book's "had he bought it at y% less and sold it for Rs X more" frame fails the gate - new
  frames + searched number sets. Backup before: `post_2026-10-30_0837.backup`. 260 questions, page counter 52.
  **Rules 25-30 done** (`gen_25_30.py` + sentences `sent_25_30.py` + PICKS, `solve_25_30.py`): cards #277-#280, **#114** (the stray
  Time & Distance card was REPLACED by the Profit Rule 29 card - backup `claude/backups/rule_math_114_before_rule29_card.json`;
  no row and no translation used it), #281; 7 old rows (318-323, 961; 319's key was on option e), 23 new (JsonImports
  #313-#318, ids 2280-2302). Backup before: `post_2026-10-30_0845.backup`.
  **Rules 31-35 done** (`gen_31_35.py` + `sent_31_35.py`, `solve_31_35.py`): cards #282-#286, 6 old rows (324-328, 962), 20 new
  (JsonImports #319-#323, ids 2303-2322); Rule 35 exercises 3-5 (book pdf page 19) not added yet. Backup before:
  `post_2026-10-30_0851.backup`. **303 questions, page counter 61**; compare_applied Rules 1-35 equal; check_order OK; the 44
  audited pages are clean (balanced LaTeX, no "None", no doubled backslash). Number search: scratch `pf_search.py` + a spec per
  batch (templates, candidate grid, "nice" test) - the Profit book is full of numbers, so most hand-picked sets hit a book passage.
  **Rules 36, 37, 38 done** (one rule per batch: `gen_36.py`/`solve_36.py`, `gen_37.py`/`solve_37.py`, `gen_38.py`/`solve_38.py`;
  the solvers solve the two-item system / price one article at Re 1 / solve the linear cost equation from two trial costs):
  cards #287-#289; old rows 329 (R36), 330 + 331 (R37; 331 is "SP of 9/10 of the stock = CP of all"), 332 (R38); 5 new each
  (JsonImports #324-#326, ids 2323-2337). Backups before: `post_2026-10-30_0856` / `_0900` / `_0903.backup`.
  **318 questions, page counter 64**; compare_applied Rules 1-38 equal; check_order OK (318 shown, rule-less last).
  **Rules 39-45, 47, 48 done** (2026-10-30 09:10-09:39; `gen_39.py`, `gen_40.py`, `gen_41.py`, `gen_42.py`, `gen_43_44.py`
  (= Rules 39/40 with losses, built with `r39`/`r40` and a `theorem` argument), `gen_45.py`, `gen_47_48.py`; solvers `solve_39`
  (two trial values), `solve_40` (signs each part by its profit/loss word), `solve_41`, `solve_42` / `solve_45` / `solve_47_48`
  (real money: cost, takings per part)). Cards #290-#298; old rows 333 (R39), 334 (R40), 335 (R41; asked for both costs but
  its key held one - now pair options), 336 + 337 (R42; **337 had no option holding the right 13%**), 338 (R43), 339 (R44),
  340 (R45), 342 (R47), 343 (R48); new questions 5 + 5 + 5 + 3 + 3 + 5 + 4 + 5 + 5 (JsonImports #327-#335, ids 2338-2377).
  **Rows 338 / 339 moved:** they were first applied under Rules 39 / 40 (same formula), then moved to Rules 43 / 44, whose book
  examples they are; their reworded sentences were kept. `rule43/` and `rule44/` hold `0_original_rows.json` (the text before
  rewording) and `gate_check.py` now gates moved rows against it. `gen_39` / `gen_40` advance the answer-position counter
  `_k` once where the moved row was, so they still reproduce the applied payloads; their `2_new_rows.json` carry the applied
  card ids again (#290, #291). Backups before: `post_2026-10-30_0910` / `_0914` / `_0918` / `_0921` / `_0927` / `_0932` /
  `_0936.backup`. **358 questions, page counter 72**; compare_applied equal for every applied rule; check_order OK.
  **Rule 46 + Rule 35 exercises 3-5 done** (2026-10-30 10:23; `gen_46.py`/`solve_46.py`: card #299, row 341, 5 new (JsonImport
  #336, ids 2378-2382) - the book's example and exercises all ask for a gain, so these do too; `gen_35_extra.py`: 3 new questions
  on the stored card #286 from folder `extra35/rule35/` (JsonImport #337, ids 2383-2385). validate / gate_check / mutation_test
  take `PROFIT_RULE_ROOT=<folder>` to check such a folder; save_and_insert takes `ROOT`. Backup before: `post_2026-10-30_1023.backup`.
  **Rules 49-50 done** (`gen_49_50.py`, `solve_49_50.py` - counts the rupees article by article / for several equal counts):
  cards #300-#301, rows 344 (R49), 345-347 (R50; 347 had two identical "2% profit" options, 346's four options were near-copies),
  5 + 9 new (JsonImports #338-#339, ids 2386-2399); signed answers ("Profit of / Loss of"). Backup before: `post_2026-10-30_1028`.
  **Rules 51-52 done** (`gen_51_52.py`, `solve_51_52.py`): cards #302-#303, rows 348 (R51, two gains, same price - pair answer)
  and 349 (R52, how many a rupee - tries counts until the gain matches), 5 + 4 new (JsonImports #340-#341, ids 2400-2408).
  Backup before: `post_2026-10-30_1033.backup`. **389 questions, page counter 78**; compare_applied Rules 1-52 equal;
  check_order OK; all 78 pages balanced LaTeX, no doubled backslash.
  **Rules 53-56 done** (2026-10-30 10:44; `gen_53_56.py`, `solve_53_56.py` - one solver for the four, told apart by their words:
  R53 tries whole-rupee prices, R54 tries counts, R55 works on a cost of 100, R56 tries costs): cards #304-#307; old rows 350-352
  (R53; **350's key was wrong** - it pointed at "horse Rs 550, ox Rs 350", the right answer was Rs 750 / Rs 300), 353 (R54),
  354 / 358 / 371 (R55; 358's word options "gains / loses" became a signed gain-or-loss question), 359 (R56); new questions 6 + 4 +
  7 + 5 (JsonImports #342-#345, ids 2409-2430): R53 = the book's three loss / profit cases of its Notes + exercises 1, 2 (selling
  price given), 3, 5 (exercise 4 is row 352); R54's exercise 3 is the book's "not possible" trick (the sale gives a gain) - written
  here as a gain question with an answer; R55 = example 2 (mark-up needed) + exercises 1-6. Backup before: `post_2026-10-30_1044`.
  **411 questions, page counter 83**; compare_applied Rules 1-56 equal; check_order OK; all 83 pages balanced LaTeX.
  **Rules 57-60 done** (2026-10-30 10:55; `gen_57_60.py`, `solve_57_60.py` - one solver: R57 tries counts, R58/R59 find the cost
  from two trial costs then price / compare in rupees (per kg when sold by weight), spoiled stock counted on 100 quintals, R60 on a
  list price of 100): cards #308-#311; old rows 360 (R57), 361-363 (R58), 364-367 (R59; **364's key pointed at "Rs 90, Rs 25"
  and no option held the new price Rs 250**; 365 is the book's "10% spoiled" example; 367 "loses 1/7 of his outlay"), 368-369
  (R60; 369 sells above the price paid and asks the profit on the list price - own builder `r60_list`); new questions 5 + 3 + 7
  + 3 (JsonImports #346-#349, ids 2431-2448). Two Rule 59 exercise sentences ("If x% is lost by selling ...") had to be reworded -
  the book's frame scores 0.86-1.0. Backup before: `post_2026-10-30_1055.backup`.
  **429 questions, page counter 86**; compare_applied Rules 1-60 equal; check_order OK; all 86 pages balanced LaTeX.
  **Rules 61-64 done** (2026-10-30 11:25; `gen_61_64.py`, `solve_61_64.py` - R61/R63 reuse the Rule 60 / Rule 55 solvers, R62 follows
  A's money, R64 tries quantities): cards #312-#315; old rows 369 (R61) and 371 (R63) are those rules' book examples - they had been
  filed under Rules 60 and 55 and were **moved** (sentences kept; `rule61/` and `rule63/` hold `0_original_rows.json` with the text
  before rewording); 370 (R62, pair "A loses ..%, B gains ..%"), 372 (R64, milkman); new questions 3 + 4 + 4 + 3 (JsonImports
  #350-#353, ids 2449-2462). gen_53_56 / gen_57_60 got `MOVED` counters (answer positions unchanged) and their old dumps a
  `moved_out` note; the same note was added to the rule39 / rule40 dumps for rows 338 / 339 (validate failed "every dumped row was
  regenerated" there since the morning move - it passes again). All their files still equal the applied ones. Backup before:
  `post_2026-10-30_1125.backup`. **443 questions, page counter 89**; compare_applied Rules 1-64 equal; check_order OK; all 89
  pages balanced LaTeX.
  **Rules 65-68 done** (2026-10-30 13:00; `gen_65_68.py`, `solve_65_68.py` - R65 linear from two trial costs, R66 spreads the one known
  price along the 'costs as much as' links (graph walk; "A gets Rs a as often as B gets Rs b" has its own builder `r66_gets`), R67 on an
  income of 100, R68 both costs from the common price): cards #316-#319; old rows 373 (R65), 374-378 (R66: the two worked examples +
  exercises 1, 2, 5), 379 (R67), 380, 381, 405 (R68: examples 1, 2 and Note 2); new questions 4 + 3 + 3 + 7 (JsonImports #354-#357,
  ids 2463-2479; R68 = Note 3's example + exercises 1-6 - the book's exercise 3 is garbled: its options fit neither its numbers nor
  a profit/loss reading). All old keys were right. Writing a patch script through a bash heredoc turned `\t` / `\f` into tab /
  form-feed again - caught before running; patch with the Edit tool or a quoted python heredoc without backslashes. Backup before:
  `post_2026-10-30_1300.backup`. **460 questions, page counter 92**; compare_applied Rules 1-68 equal; check_order OK; all 92
  pages balanced LaTeX.
  **Rules 69-72 done** (2026-10-30 13:11; `gen_69_72.py`, `solve_69_72.py` - R69 and R70 linear from two trial values, R71 rupee profit
  then the cost with the same rupee loss, R72 on a marked price of 100): cards #320-#323; old rows 406 (R69), 407 (R71), 408 (R72) -
  keys right; Rule 70 had no row; new questions 6 + 6 + 5 + 5 (JsonImports #358-#361, ids 2480-2501; R69 includes the Note's
  same-per-cent example, R70 = the worked example + exercises 1-5, written with signed rupee options "Gain of Rs .. / Loss of Rs .."
  (`rsopts`)). Three card examples first reused book numbers (R69 30%/25%, R70 20%/25%, R72 10%/20%) - changed. Backup before:
  `post_2026-10-30_1311.backup`. **482 questions, page counter 97**; compare_applied Rules 1-72 equal; check_order OK; all 97
  pages balanced LaTeX.
  **Rules 73-76 done** (2026-10-30 13:19; `gen_73_76.py`, `solve_73_76.py` - R73 tries whole-rupee costs, R74 on a cost of 100, R75
  tries costs until the gain per cents differ by d, R76 follows 100 grams bought and sold): cards #324-#327; old rows 409 (R74) and 410
  (R75; **its key pointed at Rs 300, the answer was Rs 200**); Rules 73 and 76 had no row; new questions 3 + 5 + 5 + 6 (JsonImports
  #362-#365, ids 2502-2520). R75's book frame "d% more is gained by selling ... for Rs .. than by selling it for Rs .." scores 0.74-0.78
  against the book - written as "A man sells a .. for Rs S2. Had he sold it for Rs S1, his gain per cent would have been d less.";
  R75's exercise 5 ("not possible") and R73's decimal exercises were written as ordinary solvable questions. Backup before:
  `post_2026-10-30_1319.backup`. **501 questions, page counter 101**; compare_applied Rules 1-76 equal; check_order OK; all 101
  pages balanced LaTeX.
  **Rules 77-80 done** (2026-10-30 13:28; `gen_77_80.py`, `solve_77_80.py` - cost of 100 / a stock of 1200 priced part by part / trial
  cost per kg / selling price of 100): cards #328-#331; no old rows; new questions 5 + 5 + 7 + 6 (JsonImports #366-#369, ids 2521-2543).
  Rule 78 = parts of a stock at gains and losses (the book's example prints "18% loss" though its working gives an 18% gain) and its two
  "had he sold all of it at r% he would have made Rs D more - cost per kg" exercises; Rule 79 exercise 6 asks the selling price.
  **Found in the browser after the apply:** the two Rule 78 cost-per-kg questions (2527, 2528) had a step with LaTeX outside \( \) (raw
  \frac on the page), then a display line wider than the box. `validate.py` now has the P&C **stray-LaTeX check** (`stray_tex`, +
  mutation `m_stray`); Rules 1-80 and extra35 pass it, and a scan of all 501 audited profit_n_loss rows and every card found nothing
  else. Fixed with `fix_new_questions.py` (RULE, BACKUP, DO_UPDATE: writes regenerated solution / rbe / shortcut of inserted new
  questions, matched by question text; refuses changed options / keys) - row backups `claude/backups/profit_rule78_2527_2528_before_*.json`.
  Backups before: `post_2026-10-30_1328` (batch), `_1334`, `_1335` (fixes). **524 questions, page counter 105**; compare_applied
  Rules 1-80 equal; check_order OK; all 105 pages balanced LaTeX.
  **Rules 81-84 done** (2026-10-30 13:38; `gen_81_84.py`, `solve_81_84.py` - Re 1 a metre (price or cost) for 81-83, cost of 100 /
  marked price for 84): cards #332-#335; no old rows; new questions 4 + 5 + 5 + 5 (JsonImports #370-#373, ids 2544-2562); sentences
  "A draper sells N metres of .., and his profit / loss equals what he gets for n metres" (81/82), "his profit is equal to the cost
  of n metres" (83); Rule 84 = the rupee-saving example + mark-up needed (x2), profit, discount rate. All passed the gate first time.
  Backup before: `post_2026-10-30_1338.backup`. **543 questions, page counter 109**; compare_applied Rules 1-84 equal; check_order
  OK; all 109 pages balanced LaTeX and no stray LaTeX (page-level check).
  **Rules 85-89 done - ALL 89 RULES COMPLETE** (2026-10-30 13:46; `gen_85_89.py`, `solve_85_89.py`): cards #336-#340; no old rows;
  new questions 6 + 6 + 5 + 7 + 6 (JsonImports #374-#378, ids 2563-2592). Rules 85 / 88 use the same formula, as do 52 / 89 (the
  book repeats them; each keeps its own card). Backup before: `post_2026-10-30_1346.backup`. **573 questions, page counter 115**;
  compare_applied Rules 1-89 equal; check_order OK; all 115 pages balanced LaTeX and no stray LaTeX.
  **Miscellaneous done - PROFIT AND LOSS CHAPTER COMPLETE locally** (2026-10-30 14:00; `misc/gen_misc.py`, `misc/solve_misc.py` keyed
  by row id): the book's 23 Miscellaneous problems are exactly rows 382-404 (M1 = 382 ... M23 = 404), so nothing was missing. Each row
  is linked to the existing card of the rule it uses (no new card, no JsonImport) and rewritten in the simple style with all-new
  numbers: 391 R1; 384, 394, 395 R2; 389, 396 R3; 403 R4; 393 R7; 392 R18; 390 R20; 383, 397, 399 R21; 386 R53; 382, 385 R58;
  388, 404 R59; 400 R72; 387 R79; 401, 402 R84; 398 R85 (folders `misc/ruleNN/`, checked with `PROFIT_RULE_ROOT=misc`; `m_stray`
  now breaks an old row when a folder has no payload). **Old keys that were wrong:** 388 (key on an empty option; answer Rs 2160),
  391 (key on option e, no option held the Rs 10 gain), 400 (key on option e, no option held Rs 750), 401 (keyed 45:46; answer
  45:56). Number sets searched with scratch `misc_search.py` (small sets kept hitting book passages). Backup before:
  `post_2026-10-30_1400.backup`.
  **Final state: 573 questions, every row linked to a rule (89 cards #253-#340 incl. #114), Theorem + Traditional Method +
  Specified Rule in every solution, no NULL option e, no key on option e, page counter 115; compare_applied (Rules 1-89 + misc)
  equal; check_order OK; all 115 pages balanced LaTeX, no stray LaTeX, no "None" option. JsonImports #294-#378; prompt #14.**
  **ON LIVE (pushed 2026-10-30 14:10, together with the Alligation / Time & Distance / Percentage / P&C rewording)** - selective
  sync: live dump before `db_backups/live/tutionplus_before_five_chapters_sync_2026-10-30.backup` (live ran the same commit
  ae2e4988); baseline `post_2026-10-30_0013.backup` -> three-way: no conflicts; push = 1345 rows: bank_math 775 updates
  (percentage 298, profit_n_loss 179, alligation 134, time_n_distance 121, permutation 43) + 394 inserts (profit_n_loss), 89 cards
  (88 new + #114 replaced, all profit_n_loss), total_math row 2, JsonImports #294-#378, prompt #14; rows changed only on live
  (auth_user 2, django_admin_log 8360/8361, django_migrations 215, one session) left as they are. SQL builder
  `claude/runs/profit/build_sync.py` (five-chapter allow list; `sync_five_chapters.sql` - never commit). Rehearsal on
  tutionplus_synctest: 1345/1345 equal to local, 0 other rows changed; live had not drifted; live verified 1345/1345, 0 other rows
  changed; live crawl (`time_work/live_check.py`, BASE = live URL) all six audited chapters every question once, rule order kept.
  Left "None" options on live are old rows the push did not touch: Alligation 1074 (duplicate of 1071, NULL e), Time & Distance
  817-824 + junk 835, Percentage Misc 662-679 (18). Scratch DBs dropped on the server.
  **Baseline for the next push: `db_backups/post_2026-10-30_1413.backup`** (taken right after this push). Scripts not committed yet.
  Note: `popts` gives duplicate options when the answer is 5% (5+5 = 2x5) - pick other numbers.
  Rule 41 fix after the apply: its Theorem's two formulas were on one display line, cut off at the right of the solution box
  at 800 px -> two lines in `gen_41.py`; `fix_rule41_theorem.py` wrote the new solution of rows 335, 2348-2352 and card #292
  (backup `claude/backups/profit_rule41_before_theorem_split.json`, full backup `post_2026-10-30_0941.backup`). JsonImport #329
  still holds the one-line version (history only). Only pages 48 and 52 were opened in the browser; the other new pages were
  checked by script (balanced LaTeX, no doubled backslash) - a wide formula on them would not show up there.
- **16 new book chapters added to the site code** (2026-10-29, commit `2e05ddc4`, ON LIVE: migration 0039 ran on deploy; live backup
  before it `db_backups/live/tutionplus_before_new_chapters_migration_2026-10-29.backup`). **Baseline for the next push is now
  `db_backups/post_2026-10-29_2007.backup`** (taken after the migration; local and live total_math row 2 identical): `bank.models.NEW_MATH_CHAPTERS` =
  basic_calculation, number_system, hcf_lcm, trains, races_games, clocks, calendar, true_discount, bankers_discount, stocks_shares,
  binary_numbers, logarithm, height_distance, instalments, work_wages, area_perimeter (= Elementary Mensuration I; Mensuration II is the
  existing volume_n_surface_area). They are in MATH_CHAPTER_CHOICES (admin, genai forms), have `total_<ch>` / `total_<ch>_page` columns
  (migration `bank/0039_add_book_math_chapters`, defaults 0 / 1) kept by a loop at the end of `total_math.save()`, display names in
  `views.NEW_MATH_CHAPTER_DISPLAY` (home, rules pages), icons in `math/math_home.html`. URL = code with `-` (`/math/number-system/1/`).
  The math home page now hides chapters with no questions, so a new chapter appears there once it has questions. All have 0 questions.
  On deploy, `migrate` adds the columns on live by itself (no data sync needed for them).
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
