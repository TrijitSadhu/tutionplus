"""Simple-style pass (owner, 2026-10-29): the reworded questions read too hard, so each applied row of reword/<batch> gets its
question sentence put back into the book's easy pattern, with the job/object changed and the new numbers kept (simple/<batch>_
sentences.py, SIMPLE = {row id: sentence}). Options, key and explanations stay as applied; only question + llm_used change.
Writes simple/<batch>/ruleNN/ (0_current_rows.json = the original book dump, so the gate compares with the book question;
2_new_rows.json = the applied entry with the simple question; solve.py). Check: `python reword_check.py simple/<batch>`.
Usage: python simple/make_simple.py <batch>"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/simple
SRC = os.path.join(os.path.dirname(HERE), sys.argv[1])                 # reword/<batch>
OUT = os.path.join(HERE, sys.argv[1])
NOTE = "question put in the book's simple style (job changed, new numbers kept) by Claude Opus 5.5 (2026-10-29)"
g = {}
exec(open(os.path.join(HERE, f"{sys.argv[1]}_sentences.py"), encoding="utf-8").read(), g)
SIMPLE = g["SIMPLE"]

done = set()
for d in sorted(x for x in os.listdir(SRC) if x.startswith("rule")):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for f in ("0_current_rows.json", "solve.py"):
        shutil.copy(os.path.join(SRC, d, f), os.path.join(OUT, d, f))
    rows = json.load(open(os.path.join(SRC, d, "2_new_rows.json"), encoding="utf-8"))
    for x in rows:
        x["new"]["question"] = SIMPLE[x["id"]]
        llm = x["new"].get("llm_used", x["old"]["llm_used"]) or ""
        x["new"]["llm_used"] = llm if NOTE in llm else llm + "; " + NOTE
        done.add(x["id"])
    json.dump(rows, open(os.path.join(OUT, d, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"{d}: {len(rows)} questions in the simple style")
assert done == set(SIMPLE), sorted(done ^ set(SIMPLE))
