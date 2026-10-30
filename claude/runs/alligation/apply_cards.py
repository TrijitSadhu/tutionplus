# Saves ruleNN/3_rule_card.json cards: replaces an existing card's HTML (backup first) or creates the missing card,
# then swaps the NEW_RULE_N placeholder in ruleNN/2_new_rows.json for the real card id. DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from bank.models import rule_math

ROOT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\alligation"
RULES, DO_UPDATE = globals()["RULES"], globals().get("DO_UPDATE", False)
for n in RULES:
    folder = os.path.join(ROOT, f"rule{n:02d}")
    report = open(os.path.join(folder, "4_validation_report.txt"), encoding="utf-8").readline()
    assert " 0 failed" in report, report
    c = json.load(open(os.path.join(folder, "3_rule_card.json"), encoding="utf-8"))
    existing = rule_math.objects.filter(chapter="alligation_n_mixture", rule_name=c["rule_name"]).first()
    print(f"{c['rule_name']}: {'replace card #%d' % existing.id if existing else 'create new card'} ({len(c['rule_html'])} chars)")
    if not DO_UPDATE:
        continue
    if existing:
        backup = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\rule_math_{existing.id}_before_rule{n}_card.json"
        assert not os.path.exists(backup)
        open(backup, "w", encoding="utf-8").write(serializers.serialize("json", [existing], indent=2))
        existing.rule_html = c["rule_html"]
        existing.save(update_fields=["rule_html"])
        card = existing
        print("   backup:", backup)
    else:
        card = rule_math.objects.create(chapter="alligation_n_mixture", rule_name=c["rule_name"], rule_html=c["rule_html"])
    card.refresh_from_db()
    print(f"   saved card #{card.id}, re-read equal: {card.rule_html == c['rule_html']}")
    path = os.path.join(folder, "2_new_rows.json")
    rows = json.load(open(path, encoding="utf-8"))
    for r in rows:
        if r["new"]["rule_id"] == f"NEW_RULE_{n}":
            r["new"]["rule_id"] = card.id
    json.dump(rows, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
