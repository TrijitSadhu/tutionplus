# Applies reword/simple/<BATCH>/ruleNN/2_new_rows.json: only question and llm_used change. Refuses any row whose stored question,
# key or llm_used is not the value applied from reword/<BATCH> (the row changed since), and any entry whose options/key/explanations
# differ from that applied entry. JSON backup of the rows first (never overwritten), one transaction. DO_UPDATE=False = dry run.
import glob, json, os
from django.core import serializers
from django.db import transaction
from bank.models import math

BATCH = globals()["BATCH"]
DO_UPDATE = globals().get("DO_UPDATE", False)
RW = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\time_work\reword"
BACKUP = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_time_work_simple_{BATCH}_before.json"
src = {x["id"]: x["new"] for f in glob.glob(os.path.join(RW, BATCH, "rule*", "2_new_rows.json"))
       for x in json.load(open(f, encoding="utf-8"))}
new = {x["id"]: x["new"] for f in glob.glob(os.path.join(RW, "simple", BATCH, "rule*", "2_new_rows.json"))
       for x in json.load(open(f, encoding="utf-8"))}
assert set(new) == set(src), sorted(set(new) ^ set(src))
for i in new:
    assert {k: v for k, v in new[i].items() if k not in ("question", "llm_used")} == \
           {k: v for k, v in src[i].items() if k not in ("question", "llm_used")}, f"row {i}: more than the question changed"
rows = {m.id: m for m in math.objects.filter(id__in=new)}
stale = [i for i in new if any(getattr(rows[i], f) != src[i][f] for f in ("question", "ans", "llm_used"))]
assert not stale, f"rows changed since {BATCH} was applied - not updating: {stale}"
print(f"{BATCH}: {len(new)} rows match what was applied; questions to change: {sum(new[i]['question'] != src[i]['question'] for i in new)}")

if DO_UPDATE:
    assert not os.path.exists(BACKUP), f"{BACKUP} exists - not overwriting an earlier backup"
    open(BACKUP, "w", encoding="utf-8").write(serializers.serialize("json", list(rows.values()), indent=2))
    print("backup written:", BACKUP)
    with transaction.atomic():
        for i, m in rows.items():
            m.question, m.llm_used = new[i]["question"], new[i]["llm_used"]
            m.save(update_fields=["question", "llm_used"])
    ok = sum(all(getattr(math.objects.get(pk=i), f) == new[i][f] for f in new[i]) for i in new)
    print(f"updated and re-read: {ok}/{len(new)} rows hold the simple-style values")
