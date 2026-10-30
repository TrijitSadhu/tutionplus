# Read-only: dump chosen time_n_distance math rows (by id) + one rule card to <OUT_DIR>/0_current_rows.json.
import json, os
from bank.models import math, rule_math

IDS, RULE, OUT_DIR = globals()["IDS"], globals()["RULE"], globals()["OUT_DIR"]
FIELDS = ("question", "a", "b", "c", "d", "e", "ans", "solution", "rule_based_explanation", "shortcut",
          "llm_used", "exam_and_year", "difficult_level", "validation_status", "question_image", "solution_image",
          "rule_id", "day", "from_json")
rows = list(math.objects.filter(chapter="time_n_distance", id__in=IDS).order_by("id"))
assert len(rows) == len(IDS), sorted(set(IDS) - {r.id for r in rows})
card = rule_math.objects.filter(chapter="time_n_distance", rule_name=RULE).first()
os.makedirs(OUT_DIR, exist_ok=True)
dump = {"rule_card": card and {"id": card.id, "rule_html": card.rule_html},
        "rows": [{"id": r.id, **{f: (str(getattr(r, f)) if f.endswith("image") or f == "day" else getattr(r, f)) for f in FIELDS}} for r in rows]}
json.dump(dump, open(os.path.join(OUT_DIR, "0_current_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(RULE, "rows:", [r.id for r in rows], "| card id", card and card.id)
for r in rows:
    s = r.solution or ""
    print(f"--- {r.id} ans={r.ans} rule={r.rule_id} | hr={s.count('<hr>')} Ans:={s.count('<b>Ans :</b>')} final={s.count('Final Answer')} trad={'Traditional' in s} theorem={'Theorem' in s} len={len(s)} | rbe={len(r.rule_based_explanation or '')} sc={len(r.shortcut or '')}")
    print(f"    Q: {r.question[:200]}")
    print(f"    a={r.a!r} b={r.b!r} c={r.c!r} d={r.d!r} e={r.e!r}")
