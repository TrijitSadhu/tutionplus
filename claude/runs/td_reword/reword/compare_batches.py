# Read-only: for every applied rewording batch (reword/<batch>/ruleNN/2_new_rows.json), checks the DB still holds the "new"
# values - so a regenerated batch file can not silently differ from what was applied. BATCHES = ["pilot", "b1", ...].
# When reword/simple/<batch> exists (the simple-style pass), that version is the one applied and is checked instead.
import glob, json, os
from bank.models import math

HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\td_reword\reword"
for b in globals().get("BATCHES", ["b1"]):
    simple = os.path.isdir(os.path.join(HERE, "simple", b))
    files = sorted(glob.glob(os.path.join(HERE, "simple", b, "rule*", "2_new_rows.json") if simple else
                             os.path.join(HERE, b, "rule*", "2_new_rows.json")))
    n, diff = 0, []
    for f in files:
        for x in json.load(open(f, encoding="utf-8")):
            n += 1
            m = math.objects.get(pk=x["id"])
            diff += [(x["id"], k) for k, v in x["new"].items() if getattr(m, k) != v]
    print(f"{b}{' (simple style)' if simple else ''}: {n} rows | fields differing from the DB: {diff or 'none'}")
