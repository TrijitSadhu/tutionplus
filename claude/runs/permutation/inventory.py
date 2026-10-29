# Read-only inventory of the permutation_combination chapter: counts, cards, page counter, per-row summary -> inventory.json.
import json, re
from collections import Counter
from bank.models import math, rule_math, total_math

CH = "permutation_combination"
OUT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\permutation\inventory.json"
qs = list(math.objects.filter(chapter=CH).select_related("rule").order_by("id"))
tm = total_math.objects.get(id=2)
print("questions:", len(qs), "| with rule:", sum(1 for m in qs if m.rule_id), "| page counter:", getattr(tm, f"total_{CH}_page", "?"),
      "| needed:", (len(qs) + 4) // 5)
print("cards:", [(c.id, c.rule_name) for c in rule_math.objects.filter(chapter=CH)])
print("days:", sorted(Counter(str(m.day) for m in qs).items()))
print("ans:", sorted(Counter(m.ans for m in qs).items()), "| e NULL:", sum(m.e is None for m in qs),
      "| trad:", sum("traditional" in (m.solution or "").lower() for m in qs), "| from_json:", sum(bool(m.from_json) for m in qs),
      "| display math in options:", sum(any("\\[" in (getattr(m, o) or "") for o in "abcd") for m in qs),
      "| time:", sorted(Counter(m.time for m in qs).items()))
plain = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()
rows = [{"id": m.id, "day": str(m.day), "ans": m.ans, "rule": m.rule and m.rule.rule_name, "q": plain(m.question),
         "opts": [m.a, m.b, m.c, m.d, m.e], "sol_len": len(m.solution or ""), "sol": plain(m.solution)[:300]} for m in qs]
json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for r in rows:
    print(f"{r['id']:5} {r['day']} ans={r['ans']} | {r['q'][:120]} | {[str(o)[:14] for o in r['opts'][:4]]}")
