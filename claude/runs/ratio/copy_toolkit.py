"""One-off: copies the Average audit toolkit into this folder with the chapter switched to ratio_n_proportion (no DB access).
Refuses to overwrite a file that already exists here. Usage: python copy_toolkit.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "average")
FILES = ["common.py", "dump_rows.py", "apply_rows.py", "apply_cards.py", "save_and_insert.py", "save_page_counters.py", "validate.py",
         "mutation_test.py", "compare_applied.py", "gate_check.py", "gen_common.py", "helpers.py", "fix_new_questions.py"]
SWAPS = [('chapter="average"', 'chapter="ratio_n_proportion"'), ('CHAPTER = "average"', 'CHAPTER = "ratio_n_proportion"'),
         ('== "average"', '== "ratio_n_proportion"'), ('!= "average"', '!= "ratio_n_proportion"'),
         ("claude\\runs\\average", "claude\\runs\\ratio"), ("math_average_", "math_ratio_"),
         ("total_average_page", "total_ratio_n_proportion_page"), ('"average questions:"', '"ratio_n_proportion questions:"'),
         ("dump chosen average math rows", "dump chosen ratio_n_proportion math rows"),
         ("Shared helpers for the Average generators", "Shared helpers for the Ratio and Proportion generators")]
for f in FILES:
    dst = os.path.join(HERE, f)
    assert not os.path.exists(dst), dst
    s = open(os.path.join(SRC, f), encoding="utf-8").read()
    for a, b in SWAPS:
        s = s.replace(a, b)
    left = [ln.strip() for ln in s.splitlines() if "average" in ln.lower()]
    open(dst, "w", encoding="utf-8").write(s)
    print(f"{f}: copied" + (f" | lines still saying average: {left}" if left else ""))
