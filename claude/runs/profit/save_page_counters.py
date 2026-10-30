# total_math.save() recomputes EVERY chapter's page counter from the question counts (bank/models.py). Saves row 2 once,
# prints each counter that changed, and keeps the old values in claude/backups first. DO_UPDATE=False = dry run.
import json, os
from bank.models import math, total_math

DO_UPDATE = globals().get("DO_UPDATE", False)
BACKUP = globals()["BACKUP"]
t = total_math.objects.get(id=2)
names = [f.name for f in t._meta.fields if f.name.endswith("_page")]
before = {k: getattr(t, k) for k in names}
print("profit_n_loss questions:", math.objects.filter(chapter="profit_n_loss").count(), "| total_profit_n_loss_page:", t.total_profit_n_loss_page)
if DO_UPDATE:
    assert not os.path.exists(BACKUP), BACKUP
    json.dump(before, open(BACKUP, "w", encoding="utf-8"), indent=1)
    t.save()
    t.refresh_from_db()
    print("backup:", BACKUP)
    print("counters changed:", {k: (before[k], getattr(t, k)) for k in names if before[k] != getattr(t, k)})
