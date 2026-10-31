# Saves ruleNN/3_json_import_payload.json as a JsonImport and inserts it exactly like the admin's Insert button
# (conflict scan, then BulkImporter.import_data) with the given form date, then re-reads every row.
import json, os, re
from datetime import date, time as time_cls
from django.contrib.auth import get_user_model
from genai.bulk_import import BulkImporter
from genai.models import JsonImport
from bank.models import math, rule_math

ROOT = globals().get("ROOT", r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\simple_interest")   # misc/ for the Miscellaneous run
N, DAY, DO_INSERT = globals()["N"], globals()["DAY"], globals().get("DO_INSERT", False)
folder = os.path.join(ROOT, f"rule{N:02d}")
assert " 0 failed" in open(os.path.join(folder, "4_validation_report.txt"), encoding="utf-8").readline()
payload = json.load(open(os.path.join(folder, "3_json_import_payload.json"), encoding="utf-8"))
text = json.dumps(payload, indent=2, ensure_ascii=False)
rule = f"Rule {N}"
card = rule_math.objects.filter(chapter="simple_interest", rule_name=rule).first()
already = [q["question"][:60] for q in payload["questions"] if math.objects.filter(question=q["question"]).exists()]
conflicts = BulkImporter(table_name="math", json_data=text, form_date=DAY, form_time=time_cls(10, 0, 0)).scan_math_conflicts(payload)
dupe_ji = [ji.pk for ji in JsonImport.objects.filter(to_table="math") if (ji.json_data or "").strip() == text.strip()]
card_note = (f"card #{card.id} same as payload card: {card.rule_html == payload['rules_html'][0]['rule_html']}" if card
             else "no card yet - the import creates it")
print(f"{rule}: {len(payload['questions'])} questions | {card_note} "
      f"| conflicts: {len(conflicts)} | already in math: {already} | identical JsonImports: {dupe_ji}")
assert not conflicts and not already and not dupe_ji

if DO_INSERT:
    user = get_user_model().objects.get(username="biswajit688813")
    ji = JsonImport.objects.create(to_table="math", json_data=text, created_by=user)
    before = math.objects.count()
    result = BulkImporter(table_name="math", json_data=ji.json_data, form_date=DAY, form_time=time_cls(10, 0, 0)).import_data(resolutions={})
    print(f"JsonImport #{ji.pk} inserted: created {result['created']}, updated {result['updated']}, errors {result['errors']}, "
          f"skipped cards {len(result.get('skipped_rules') or [])}, math rows {before} -> {math.objects.count()}")
    card = rule_math.objects.get(chapter="simple_interest", rule_name=rule)
    print(f"card #{card.id} {rule} stored, equal to payload card: {card.rule_html == payload['rules_html'][0]['rule_html']}")
    bad = []
    for q in payload["questions"]:
        m = math.objects.get(question=q["question"])
        diffs = [f for f in ("a", "b", "c", "d", "solution", "rule_based_explanation", "shortcut", "exam_and_year") if getattr(m, f) != q[f]]
        if m.ans != q["correct_answer"] or m.rule_id != card.id or m.chapter != "simple_interest" or m.day != DAY:
            diffs.append("ans/rule/chapter/day")
        if diffs:
            bad.append((m.id, diffs))
    ids = sorted(math.objects.filter(question__in=[q["question"] for q in payload["questions"]]).values_list("id", flat=True))
    print(f"re-read {len(ids)} rows (ids {ids[0]}-{ids[-1]}) | mismatches: {bad or 'none'}")
