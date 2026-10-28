# Read-only: are the 10 profit-and-loss rows filed under time_n_work (946-955) already in profit_n_loss?
import re
from bank.models import math

norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>", " ", s or "").lower())
pl = list(math.objects.filter(chapter="profit_n_loss"))
pl_q = {norm(m.question): m.id for m in pl}
print("profit_n_loss questions:", len(pl), "| rules:", len({m.rule_id for m in pl if m.rule_id}))
for m in math.objects.filter(id__in=range(946, 956)).order_by("id"):
    same = pl_q.get(norm(m.question))
    near = [p.id for p in pl if norm(m.question)[:40] == norm(p.question)[:40]]
    print(m.id, m.chapter, "rule", m.rule_id, "day", m.day, "| identical in profit_n_loss:", same, "| same opening:", near[:5],
          "|", re.sub(r"\s+", " ", m.question)[:70])
