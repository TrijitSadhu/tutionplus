# Read-only: for every applied rewording batch (reword/<batch>/ruleNN/2_new_rows.json), checks the DB still holds the "new"
# values - so a regenerated batch file can not silently differ from what was applied. BATCHES = ["b1", "b2", ...].
import glob, json, os
from bank.models import math

HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\percentage\reword"
for b in globals().get("BATCHES", ["b1"]):
    n, diff = 0, []
    for f in sorted(glob.glob(os.path.join(HERE, b, "rule*", "2_new_rows.json"))):
        for x in json.load(open(f, encoding="utf-8")):
            n += 1
            m = math.objects.get(pk=x["id"])
            diff += [(x["id"], k) for k, v in x["new"].items() if getattr(m, k) != v]
    print(f"{b}: {n} rows | fields differing from the DB: {diff or 'none'}")
