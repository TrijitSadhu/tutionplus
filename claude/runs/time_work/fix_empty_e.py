# The page always draws a 5th option from math.e: '' shows an empty radio, NULL prints the word "None".
# Sets e = '' on the given rows where e is NULL (backup to claude/backups first). DO_UPDATE=False = dry run.
import os
from django.core import serializers
from bank.models import math

IDS, LABEL, DO_UPDATE = globals()["IDS"], globals()["LABEL"], globals().get("DO_UPDATE", False)
BACKUP = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_time_work_{LABEL}_before_empty_e.json"
rows = list(math.objects.filter(id__in=IDS, chapter="time_n_work", e__isnull=True).order_by("id"))
print(f"{len(rows)} of {len(IDS)} rows have e = NULL: {[m.id for m in rows]}")
if DO_UPDATE and rows:
    assert not os.path.exists(BACKUP), BACKUP
    open(BACKUP, "w", encoding="utf-8").write(serializers.serialize("json", rows, indent=2))
    n = math.objects.filter(id__in=[m.id for m in rows]).update(e="")
    print("backup:", BACKUP, "| updated:", n, "| still NULL:", math.objects.filter(id__in=IDS, e__isnull=True).count())
