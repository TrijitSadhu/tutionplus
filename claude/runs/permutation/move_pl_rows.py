# Moves the 6 profit-and-loss questions (957-962) that were filed under permutation_combination to profit_n_loss
# (rule-less, as all profit_n_loss rows are today), backs the rows and the page counters up first, then sets both
# chapters' page counters to ceil(questions / 5). Same as claude/runs/time_work/move_pl_rows.py. DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from django.db import transaction
from bank.models import math, total_math

DO_UPDATE = globals().get("DO_UPDATE", False)
IDS = list(range(957, 963))
BACKUP = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_957_962_before_move_to_profit_n_loss.json"
rows = list(math.objects.filter(id__in=IDS).order_by("id"))
assert len(rows) == 6 and all(m.chapter == "permutation_combination" and m.rule_id is None for m in rows), [(m.id, m.chapter, m.rule_id) for m in rows]
for m in rows:
    print(m.id, m.question[:90])
t = total_math.objects.get(id=2)
pc_after = math.objects.filter(chapter="permutation_combination").count() - 6
pl_after = math.objects.filter(chapter="profit_n_loss").count() + 6
print(f"move {IDS[0]}-{IDS[-1]} -> profit_n_loss | permutation_combination pages {t.total_permutation_combination_page} -> {(pc_after + 4) // 5} "
      f"| profit_n_loss pages {t.total_profit_n_loss_page} -> {(pl_after + 4) // 5}")
if DO_UPDATE:
    assert not os.path.exists(BACKUP), BACKUP
    data = json.loads(serializers.serialize("json", rows))
    data.append({"total_math_id": 2, "total_permutation_combination_page": t.total_permutation_combination_page,
                 "total_profit_n_loss_page": t.total_profit_n_loss_page})
    json.dump(data, open(BACKUP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    with transaction.atomic():
        n = math.objects.filter(id__in=IDS, chapter="permutation_combination").update(chapter="profit_n_loss")
        t.total_permutation_combination_page = (pc_after + 4) // 5
        t.total_profit_n_loss_page = (pl_after + 4) // 5
        t.save(update_fields=["total_permutation_combination_page", "total_profit_n_loss_page"])
    t.refresh_from_db()
    print(f"backup: {BACKUP} | moved {n} rows | permutation_combination {math.objects.filter(chapter='permutation_combination').count()} questions, "
          f"{t.total_permutation_combination_page} pages | profit_n_loss {math.objects.filter(chapter='profit_n_loss').count()} questions, "
          f"{t.total_profit_n_loss_page} pages")
