"""Quick originality check of draft questions before they go into a gen_bN.py plan.
Usage: python try_q.py <batch folder> <drafts.py>   (drafts.py defines DRAFTS = {row id: question})"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(TW, "..", "..", "tools"))
from originality import Book, check_question, measures  # noqa: E402

book = Book(os.path.join(TW, "pdf_text.txt"))
old = {}
for f in glob.glob(os.path.join(HERE, sys.argv[1], "rule*", "0_current_rows.json")):
    for r in json.load(open(f, encoding="utf-8"))["rows"]:
        old[r["id"]] = r["question"]
g = {}
exec(open(sys.argv[2], encoding="utf-8").read(), g)
bad = 0
for rid, q in g["DRAFTS"].items():
    p = check_question(q, book, old[rid])
    bad += bool(p)
    print(("OK  " if not p else "BAD ") + str(rid), measures(q, book, old[rid]), p or "")
print(f"{len(g['DRAFTS']) - bad} of {len(g['DRAFTS'])} pass")
