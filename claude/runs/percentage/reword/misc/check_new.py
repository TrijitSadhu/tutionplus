"""Extra checks for the Percentage Miscellaneous run (reword_check.py gates the old rows only): every new question must pass the
simple originality gate against the book, and no field of a new question or a regenerated row may hold LaTeX outside \\( \\) /
\\[ \\] (the Profit validator's stray_tex). Usage: python check_new.py"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PC, "..", "..", "tools"))
sys.path.insert(0, os.path.join(PC, "..", "profit"))
from originality import Book, check_question, measures  # noqa: E402
from validate import stray_tex  # noqa: E402   (claude/runs/profit/validate.py)

book = Book(os.path.join(PC, "pdf_text.txt"))
bad = total = 0
for folder in sorted(glob.glob(os.path.join(HERE, "rule*"))):
    p = os.path.join(folder, "3_json_import_payload.json")
    if os.path.exists(p):
        for q in json.load(open(p, encoding="utf-8"))["questions"]:
            total += 1
            probs = check_question(q["question"], book, None, simple=True)
            if probs:
                bad += 1
                print("GATE", os.path.basename(folder), q["question"][:70], measures(q["question"], book, None), probs)
            for f in ("question", "solution", "rule_based_explanation", "shortcut", "a", "b", "c", "d"):
                if stray_tex(q[f]):
                    bad += 1
                    print("STRAY", os.path.basename(folder), f, q["question"][:50])
    for r in json.load(open(os.path.join(folder, "2_new_rows.json"), encoding="utf-8")):
        for f, v in r["new"].items():
            if isinstance(v, str) and stray_tex(v):
                bad += 1
                print("STRAY row", r["id"], f)
print(f"new questions gated: {total} | problems: {bad}")
sys.exit(1 if bad else 0)
