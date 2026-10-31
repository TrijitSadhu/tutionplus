# Read-only: for already-applied rule folders, checks the DB rows still equal 2_new_rows.json "new" values
# (so regenerating a folder did not drift from what was applied).
import json, os
from bank.models import math

ROOT = globals().get("ROOT", r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\simple_interest")
for n in globals()["RULES"]:
    p = os.path.join(ROOT, f"rule{n:02d}", "2_new_rows.json")
    if not os.path.exists(p):                       # a rule with new questions only (no old row)
        print(f"Rule {n}: no old rows - skipped")
        continue
    rows = json.load(open(p, encoding="utf-8"))
    diff = [(x["id"], f) for x in rows for f, v in x["new"].items() if getattr(math.objects.get(pk=x["id"]), f) != v]
    print(f"Rule {n}: {len(rows)} rows | fields differing from the DB: {diff or 'none'}")
