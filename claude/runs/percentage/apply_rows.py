# Applies <RUN_DIR>/2_new_rows.json to bank.math: every field listed under "new" (solution, rule_based_explanation,
# shortcut, ans, rule_id, llm_used, and question/options when they are fixed). Backs the rows up to
# claude/backups first, refuses rows that changed since they were dumped, one transaction. DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from django.db import transaction
from bank.models import math

RUN_DIR, LABEL = globals()["RUN_DIR"], globals()["LABEL"]
DO_UPDATE = globals().get("DO_UPDATE", False)
BACKUP = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_percentage_{LABEL}_before_regenerate.json"
new_rows = json.load(open(os.path.join(RUN_DIR, "2_new_rows.json"), encoding="utf-8"))
assert all("ans" in n["new"] for n in new_rows), "run validate.py first"
rows = {m.id: m for m in math.objects.filter(id__in=[n["id"] for n in new_rows])}
assert len(rows) == len(new_rows)
stale = [n["id"] for n in new_rows if any(getattr(rows[n["id"]], f) != n["old"][f] for f in n["new"])]
assert not stale, f"rows changed since they were dumped - not updating: {stale}"
keys = [(n["id"], n["old"]["ans"], n["new"]["ans"]) for n in new_rows if n["new"]["ans"] != n["old"]["ans"]]
links = sum(n["old"]["rule_id"] != n["new"]["rule_id"] for n in new_rows)
edits = [(n["id"], f) for n in new_rows for f in n["new"] if f in ("question", "a", "b", "c", "d") and n["new"][f] != n["old"][f]]
print(f"{len(new_rows)} rows unchanged since dump | key fixes: {keys} | rows getting a rule card: {links} | question/option edits: {edits}")

if DO_UPDATE:
    assert not os.path.exists(BACKUP), f"{BACKUP} exists - not overwriting an earlier backup"
    with open(BACKUP, "w", encoding="utf-8") as fh:
        fh.write(serializers.serialize("json", list(rows.values()), indent=2))
    print("backup written:", BACKUP)
    with transaction.atomic():
        for n in new_rows:
            m = rows[n["id"]]
            for f, v in n["new"].items():
                setattr(m, f, v)
            m.save(update_fields=[f if f != "rule_id" else "rule" for f in n["new"]])
    ok = sum(all(getattr(math.objects.get(pk=n["id"]), f) == v for f, v in n["new"].items()) for n in new_rows)
    print(f"updated and re-read: {ok}/{len(new_rows)} rows hold the new values")
