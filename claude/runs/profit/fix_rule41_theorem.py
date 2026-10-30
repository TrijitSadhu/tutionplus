# Rule 41 (2026-10-30): the Theorem's two cost-price formulas were on one display line, wider than the solution box. gen_41.py
# now puts them on two lines; this writes the regenerated solution of row 335 and of the 5 new questions, and the card, to the DB.
# Backs up first; refuses any row whose other fields differ from the applied files. Inputs: DO_UPDATE.
import json, os
from django.db import transaction
from bank.models import math, rule_math

HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\profit"
BACKUP = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\profit_rule41_before_theorem_split.json"
CARD_ID = 292
folder = os.path.join(HERE, "rule41")
old_rows = json.load(open(os.path.join(folder, "2_new_rows.json"), encoding="utf-8"))
payload = json.load(open(os.path.join(folder, "3_json_import_payload.json"), encoding="utf-8"))
card_html = json.load(open(os.path.join(folder, "3_rule_card.json"), encoding="utf-8"))["rule_html"]

plan = {}
for x in old_rows:
    r = math.objects.get(pk=x["id"])
    for f, v in x["new"].items():
        if f not in ("solution", "rule_id") and getattr(r, f) != v:
            raise SystemExit(f"row {r.id}: {f} differs from the applied file - stop")
    plan[r.id] = x["new"]["solution"]
for q in payload["questions"]:
    r = math.objects.get(chapter="profit_n_loss", question=q["question"])
    assert r.rule_id == CARD_ID and r.shortcut == q["shortcut"] and r.rule_based_explanation == q["rule_based_explanation"], r.id
    plan[r.id] = q["solution"]
card = rule_math.objects.get(pk=CARD_ID)
assert card.rule_name == "Rule 41" and card.chapter == "profit_n_loss"
print("rows:", sorted(plan), "| card", CARD_ID)

if globals().get("DO_UPDATE"):
    assert not os.path.exists(BACKUP), "backup exists - never overwrite"
    json.dump({"rows": {i: math.objects.get(pk=i).solution for i in plan}, "card": card.rule_html},
              open(BACKUP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    with transaction.atomic():
        for i, s in plan.items():
            math.objects.filter(pk=i).update(solution=s)
        rule_math.objects.filter(pk=CARD_ID).update(rule_html=card_html)
    ok = all(math.objects.get(pk=i).solution == s for i, s in plan.items()) and rule_math.objects.get(pk=CARD_ID).rule_html == card_html
    print("backup:", BACKUP, "| updated and re-read equal:", ok)
