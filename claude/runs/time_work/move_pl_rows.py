# Moves the 10 profit-and-loss questions (946-955) that were filed under time_n_work to profit_n_loss (rule-less, as all
# profit_n_loss rows are today), backs the rows and the page counters up first, then sets both chapters' page counters
# to ceil(questions / 5). DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from django.db import transaction
from bank.models import math, total_math

DO_UPDATE = globals().get("DO_UPDATE", False)
IDS = list(range(946, 956))
BACKUP = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_946_955_before_move_to_profit_n_loss.json"
rows = list(math.objects.filter(id__in=IDS).order_by("id"))
assert len(rows) == 10 and all(m.chapter == "time_n_work" and m.rule_id is None for m in rows), [(m.id, m.chapter, m.rule_id) for m in rows]
t = total_math.objects.get(id=2)
tw_after = math.objects.filter(chapter="time_n_work").count() - 10
pl_after = math.objects.filter(chapter="profit_n_loss").count() + 10
print(f"move {IDS[0]}-{IDS[-1]} -> profit_n_loss | time_n_work pages {t.total_time_n_work_page} -> {(tw_after + 4) // 5} "
      f"| profit_n_loss pages {t.total_profit_n_loss_page} -> {(pl_after + 4) // 5}")
if DO_UPDATE:
    assert not os.path.exists(BACKUP), BACKUP
    data = json.loads(serializers.serialize("json", rows))
    data.append({"total_math_id": 2, "total_time_n_work_page": t.total_time_n_work_page, "total_profit_n_loss_page": t.total_profit_n_loss_page})
    json.dump(data, open(BACKUP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    with transaction.atomic():
        n = math.objects.filter(id__in=IDS, chapter="time_n_work").update(chapter="profit_n_loss")
        t.total_time_n_work_page = (tw_after + 4) // 5
        t.total_profit_n_loss_page = (pl_after + 4) // 5
        t.save(update_fields=["total_time_n_work_page", "total_profit_n_loss_page"])
    t.refresh_from_db()
    print(f"backup: {BACKUP} | moved {n} rows | time_n_work {math.objects.filter(chapter='time_n_work').count()} questions, "
          f"{t.total_time_n_work_page} pages | profit_n_loss {math.objects.filter(chapter='profit_n_loss').count()} questions, {t.total_profit_n_loss_page} pages")
