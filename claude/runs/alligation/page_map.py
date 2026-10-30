# Read-only: which rule each chapter page shows (same ordering as the site: day, id; 5 per page),
# and how many questions per rule carry the Traditional Method.
from collections import OrderedDict
from bank.models import math


def run():
    qs = list(math.objects.filter(chapter="alligation_n_mixture").select_related("rule").order_by("day", "id"))
    print("questions", len(qs), "| pages", (len(qs) + 4) // 5)
    runs = []
    for i, m in enumerate(qs):
        r = m.rule.rule_name if m.rule else "(no rule)"
        if runs and runs[-1][0] == r:
            runs[-1][2] = i // 5 + 1
            runs[-1][3] += 1
        else:
            runs.append([r, i // 5 + 1, i // 5 + 1, 1])
    for r, a, b, n in runs:
        print(f"  pages {a:2}-{b:2}: {r} x{n}")
    per = OrderedDict()
    for m in qs:
        r = m.rule.rule_name if m.rule else "(no rule)"
        t = per.setdefault(r, [0, 0])
        t[0] += 1
        t[1] += "Traditional Method :" in (m.solution or "")
    print("Traditional Method per rule:", ", ".join(f"{r} {t[1]}/{t[0]}" for r, t in sorted(per.items(), key=lambda kv: int(kv[0].split()[-1]) if kv[0][0] == "R" else 0)))


run()
