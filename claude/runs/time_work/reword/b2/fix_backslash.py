# One-off fix (2026-10-29): rows 203 and 1263 were applied with doubled backslashes in the question (\\( \\frac \\)), so the
# fraction showed as raw LaTeX. Sets their question to the corrected value in reword/b2/rule06/2_new_rows.json (generated from
# the fixed gen_b2.py), after a JSON backup of the two rows. Refuses to run if the stored text is not the doubled version.
# DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from bank.models import math

DO_UPDATE = globals().get("DO_UPDATE", False)
HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\time_work\reword\b2"
BACKUP = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\math_203_1263_before_backslash_fix.json"
B = chr(92)
new = {x["id"]: x["new"]["question"] for x in json.load(open(os.path.join(HERE, "rule06", "2_new_rows.json"), encoding="utf-8"))
       if x["id"] in (203, 1263)}
rows = list(math.objects.filter(id__in=new))
for m in rows:
    assert B * 2 + "frac" in m.question and B * 2 not in new[m.id], m.id
    assert m.question.replace(B * 2, B) == new[m.id], (m.id, m.question, new[m.id])
    print(m.id, "stored:", m.question[:70], "\n      fixed: ", new[m.id][:70])
if DO_UPDATE:
    assert not os.path.exists(BACKUP), BACKUP
    open(BACKUP, "w", encoding="utf-8").write(serializers.serialize("json", rows, indent=2))
    for m in rows:
        m.question = new[m.id]
        m.save(update_fields=["question"])
    print("backup:", BACKUP, "| re-read equal:", all(math.objects.get(id=i).question == q for i, q in new.items()))
