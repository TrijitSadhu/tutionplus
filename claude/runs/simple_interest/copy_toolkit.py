"""One-off: copies the Ratio and Proportion audit toolkit into this folder with the chapter switched to simple_interest (no DB
access). Refuses to overwrite a file that already exists here. Usage: python copy_toolkit.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "ratio")
B = chr(92)
FILES = ["common.py", "dump_rows.py", "apply_rows.py", "apply_cards.py", "save_and_insert.py", "save_page_counters.py", "validate.py",
         "mutation_test.py", "compare_applied.py", "gate_check.py", "gen_common.py", "helpers.py", "fix_new_questions.py", "fmt.py",
         "make_prompt.py", "save_prompt.py", "prompt9_original.txt"]
SWAPS = [('chapter="ratio_n_proportion"', 'chapter="simple_interest"'), ('CHAPTER = "ratio_n_proportion"', 'CHAPTER = "simple_interest"'),
         ('== "ratio_n_proportion"', '== "simple_interest"'), ('!= "ratio_n_proportion"', '!= "simple_interest"'),
         ("claude" + B + "runs" + B + "ratio", "claude" + B + "runs" + B + "simple_interest"), ("math_ratio_", "math_si_"),
         ("total_ratio_n_proportion_page", "total_simple_interest_page"), ('"ratio_n_proportion questions:"', '"simple_interest questions:"'),
         ("dump chosen ratio_n_proportion math rows", "dump chosen simple_interest math rows"),
         ("Shared helpers for the Ratio and Proportion generators", "Shared helpers for the Simple Interest generators"),
         ("Formatting and option helpers for the Ratio and Proportion generators", "Formatting and option helpers for the Simple Interest generators")]
for f in FILES:
    dst = os.path.join(HERE, f)
    assert not os.path.exists(dst), dst
    s = open(os.path.join(SRC, f), encoding="utf-8").read()
    if f not in ("make_prompt.py", "prompt9_original.txt"):
        for a, b in SWAPS:
            s = s.replace(a, b)
    left = [ln.strip()[:80] for ln in s.splitlines() if "ratio_n_proportion" in ln or (B + "ratio" + chr(34)) in ln]
    open(dst, "w", encoding="utf-8").write(s)
    print(f"{f}: copied" + (f" | still names the ratio chapter: {left}" if left and f not in ("make_prompt.py",) else ""))
