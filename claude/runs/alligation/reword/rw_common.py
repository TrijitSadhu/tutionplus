"""Shared helpers for the rewording batches (reword/bN/gen_bN.py): options with plausible wrong answers, and the step that
turns one plan entry into a 2_new_rows.json entry."""
import json, os, sys
from fractions import Fraction as F

TW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TW)
from common import regen_entry, tex  # noqa: E402

NOTE = "question reworded (fresh wording + all-new numbers, checked against the book) by Claude Opus 5.5 (2026-10-29)"
POS = [2, 4, 1, 3, 3, 1, 4, 2, 1, 3, 2, 4]          # where the right option goes, cycled over the rows


def wrong_values(v):
    """Three distinct, positive, plausible wrong answers near v."""
    v = F(v)
    if v.denominator == 1:
        step = max(2, int(v) // 4)
        cands = [v + step, v - step, 2 * v, v + 1, v - 1, v * F(3, 2), v + 2 * step]
    else:
        cands = [v + 1, v - 1, 2 * v, v + F(1, 2), v * F(3, 2)]
    out = []
    for c in cands:
        if c > 0 and c != v and c not in out:
            out.append(c)
    return out[:3]


def options(answer, unit, pos, labels=("A", "B")):
    """answer = ('number' | 'triple' | 'pair' | 'ratio', value); labels name the two parts of a pair answer."""
    kind, val = answer
    if kind == "triple":
        a, b, c = val
        fmt = lambda t: rf"A \({tex(t[0])}\) {unit}, B \({tex(t[1])}\) {unit}, C \({tex(t[2])}\) {unit}"
        wrong = [(b, a, c), (2 * a, 2 * b, 2 * c), (c, b, a), (a / 2, b / 2, c / 2)]
        right, others = fmt((a, b, c)), [fmt(w) for w in dict.fromkeys(w for w in wrong if w != (a, b, c))][:3]
    elif kind == "pair":
        a, b = (F(x) for x in val)
        fmt = lambda t: rf"{labels[0]} \({tex(t[0])}\) {unit}, {labels[1]} \({tex(t[1])}\) {unit}"
        wrong = [(b, a), (2 * a, b), (a, 2 * b), (a + 1, b + 1)]
        right, others = fmt((a, b)), [fmt(w) for w in dict.fromkeys(w for w in wrong if w != (a, b))][:3]
    elif kind == "ratio":
        p, q = (int(x) for x in val)
        cands = [(q, p), (p + 1, q), (p, q + 1), (p + 2, q), (2 * p + 1, q), (p + 1, q + 2), (p + 3, q)]
        seen, others = {F(p, q), F(1)}, []                  # wrong ratios in lowest terms, never 1 : 1
        for c in cands:
            r = F(*c)
            if r not in seen:
                seen.add(r)
                others.append(f"{r.numerator} : {r.denominator}")
        right, others = f"{p} : {q}", others[:3]
    else:
        one = {"days": "day", "hours": "hour", "men": "man", "trees": "tree"}
        fmt = lambda v: rf"\({tex(v)}\) {one.get(unit, unit) if v == 1 else unit}"
        right = fmt(val)
        others = [fmt(w) for w in wrong_values(val)]
    opts = list(others)
    opts.insert(pos - 1, right)
    return dict(zip("abcd", opts))


def write_batch(here, plan):
    """plan: rule -> [(row id, question, generator call, unit[, pair labels])]; writes each ruleNN/2_new_rows.json.
    unit may instead be a ready {a, b, c, d} options dict (clock times, dates); validate.py then finds and sets the key."""
    k = 0
    for n, rows_plan in plan.items():
        folder = os.path.join(here, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(p[0] for p in rows_plan), (n, sorted(set(rows) ^ {p[0] for p in rows_plan}))
        out = []
        for entry in rows_plan:
            rid, question, fn, unit = entry[:4]
            labels = entry[4] if len(entry) > 4 else ("A", "B")
            r = rows[rid]
            assert r["rule_id"] == dump["rule_card"]["id"]
            g = fn()
            llm = r["llm_used"] or ""
            opts = unit if isinstance(unit, dict) else options(g["answer"], unit, POS[k % len(POS)], labels)
            extra = {"question": question, **opts, "e": "",
                     "llm_used": llm if NOTE in llm else (llm + "; " if llm else "") + NOTE}
            k += 1
            extra = {key: v for key, v in extra.items() if v != r[key]}
            out.append(regen_entry(r, g, r["rule_id"], extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows reworded")
