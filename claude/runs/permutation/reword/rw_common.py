"""Shared helpers for the P&C rewording batches (reword/bN/gen_bN.py): options with plausible wrong answers, and the step
that turns one plan entry into a 2_new_rows.json entry. Same as claude/runs/alligation/reword/rw_common.py, except that an option
is written by the row's own formatter (P = per cent, Rs = rupees, Num = plain number, ...) instead of a unit word."""
import json, os, sys
from fractions import Fraction as F

PC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PC)
from common import regen_entry  # noqa: E402

NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
        "by Claude Opus 5.5 (2026-10-30)")
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


def options(answer, fmt, pos):
    """answer = ('number', value); fmt writes one value as an option, e.g. P(25) -> \\(25\\%\\)."""
    kind, val = answer
    assert kind == "number", f"give plain options for a {kind} answer"
    opts = [fmt(w) for w in wrong_values(val)]
    opts.insert(pos - 1, fmt(val))
    return dict(zip("abcd", opts))


def write_batch(here, plan):
    """plan: rule -> [(row id, question, generator call, formatter or a ready {a, b, c, d} options dict)];
    writes each ruleNN/2_new_rows.json (validate.py then finds and sets the key)."""
    k = 0
    for n, rows_plan in plan.items():
        folder = os.path.join(here, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(p[0] for p in rows_plan), (n, sorted(set(rows) ^ {p[0] for p in rows_plan}))
        out = []
        for rid, question, fn, fmt in rows_plan:
            r = rows[rid]
            assert r["rule_id"] == dump["rule_card"]["id"], rid
            g = fn()
            llm = r["llm_used"] or ""
            opts = fmt if isinstance(fmt, dict) else options(g["answer"], fmt, POS[k % len(POS)])
            extra = {"question": question, **opts, "e": "",
                     "llm_used": llm if NOTE in llm else (llm + "; " if llm else "") + NOTE}
            k += 1
            extra = {key: v for key, v in extra.items() if v != r[key]}
            out.append(regen_entry(r, g, r["rule_id"], extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows reworded")
