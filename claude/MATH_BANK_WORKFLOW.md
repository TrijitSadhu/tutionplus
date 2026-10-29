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
