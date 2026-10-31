"""Originality check for an audit batch (simple style): every regenerated old row (2_new_rows.json, against the book and the
question it replaces) and every new question (3_json_import_payload.json, against the book) must pass
claude/tools/originality.check_question(simple=True). Usage: python gate_check.py 1 2 3"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from originality import Book, check_question, measures  # noqa: E402

book = Book(os.path.join(HERE, "pdf_text.txt"))
bad = total = 0
for n in map(int, sys.argv[1:]):
    folder = os.path.join(os.environ.get("PROFIT_RULE_ROOT") or HERE, f"rule{n:02d}")
    rows = {r["id"]: r for r in json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))["rows"]}
    orig = dict(rows)
    p = os.path.join(folder, "0_original_rows.json")      # rows moved from another rule: gate against the text before any rewording
    if os.path.exists(p):
        orig.update({r["id"]: r for r in json.load(open(p, encoding="utf-8"))["rows"]})
    items = []
    p = os.path.join(folder, "2_new_rows.json")
    if os.path.exists(p):
        for x in json.load(open(p, encoding="utf-8")):
            items.append((x["id"], x["new"].get("question", rows[x["id"]]["question"]), orig[x["id"]]["question"]))
    p = os.path.join(folder, "3_json_import_payload.json")
    if os.path.exists(p):
        for i, q in enumerate(json.load(open(p, encoding="utf-8"))["questions"], 1):
            items.append((f"new{i}", q["question"], None))
    for key, q, old in items:
        total += 1
        probs = check_question(q, book, old, simple=True)
        if probs:
            bad += 1
            print(f"FAIL Rule {n} {key}: {measures(q, book, old)} {probs}")
print(f"gate: {total - bad} of {total} pass")
sys.exit(1 if bad else 0)
