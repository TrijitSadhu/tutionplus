# Sets total_math (row 2).total_percentage_page to ceil(questions / 5) so the pager's "Next" reaches the last page.
# Prints the old value (the backup) first. DO_UPDATE=False = dry run.
from bank.models import math, total_math

DO_UPDATE = globals().get("DO_UPDATE", False)
n = math.objects.filter(chapter="percentage").count()
t = total_math.objects.get(id=2)
want = (n + 4) // 5
print(f"percentage questions: {n} | total_percentage_page: {t.total_percentage_page} -> {want}")
new_rows = math.objects.filter(id__in=[1663, 1664, 1665, 1666]).order_by("id")
print("new rows (id, ans, time, day, rule):", [(m.id, m.ans, m.time, str(m.day), m.rule.rule_name) for m in new_rows])
if DO_UPDATE and t.total_percentage_page != want:
    t.total_percentage_page = want
    t.save(update_fields=["total_percentage_page"])
    print("saved:", total_math.objects.get(id=2).total_percentage_page)
