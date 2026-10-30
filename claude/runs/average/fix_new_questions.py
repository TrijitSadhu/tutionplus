# Writes regenerated explanation fields of already-inserted NEW questions to the DB (2026-10-30: Rule 78's two "cost per kg"
# questions had LaTeX outside \( \) in a step). Matches each payload question to its DB row by the question text; refuses any row
# whose question, options or key differ from the payload. Backs up the changed rows first. Inputs: RULE, BACKUP, DO_UPDATE.
import json, os
from django.db import transaction
from bank.models import math

HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\average"
RULE, BACKUP = globals()["RULE"], globals()["BACKUP"]
payload = json.load(open(os.path.join(HERE, f"rule{RULE}", "3_json_import_payload.json"), encoding="utf-8"))
FIELDS = ("solution", "rule_based_explanation", "shortcut")
plan = {}
for q in payload["questions"]:
    r = math.objects.get(chapter="average", question=q["question"])
    assert r.rule.rule_name == f"Rule {RULE}", r.id
    assert [getattr(r, k) for k in "abcd"] == [q[k] for k in "abcd"] and r.ans == q["correct_answer"], f"row {r.id} options / key differ"
    new = {f: q[f] for f in FIELDS if getattr(r, f) != q[f]}
    if new:
        plan[r.id] = new
print("rows to update:", {i: sorted(v) for i, v in plan.items()})
if globals().get("DO_UPDATE") and plan:
    assert not os.path.exists(BACKUP), "backup exists - never overwrite"
    json.dump({i: {f: getattr(math.objects.get(pk=i), f) for f in FIELDS} for i in plan}, open(BACKUP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    with transaction.atomic():
        for i, new in plan.items():
            math.objects.filter(pk=i).update(**new)
    ok = all(getattr(math.objects.get(pk=i), f) == v for i, new in plan.items() for f, v in new.items())
    print("backup:", BACKUP, "| updated and re-read equal:", ok)
