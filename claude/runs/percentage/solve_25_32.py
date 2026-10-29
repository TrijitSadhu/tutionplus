"""Independent solvers for Percentage Rules 25-32. The population rules read each year's change (with its sign) from the
question and run the town year by year, solving for an earlier population as a linear function; the males/females rule
tries every possible number of males; the price rule searches the consumption that keeps the bill unchanged - never
through the rule formulas gen_25_32.py uses."""
import re
from fractions import Fraction as F
from validate import numbers
from solve_1_8 import NUM, others, pcts, unknown


def yearly_changes(q):
    """Signed percentages in reading order; a bare 'and by 20%' keeps the last verb's direction."""
    sign, out = 1, []
    for m in re.finditer(rf"(increas|decreas|grow|fall|rise)\w*|({NUM})(?:\\\))?\s*(?:\\%|%)", q):
        if m.group(1):
            sign = 1 if m.group(1) in ("increas", "grow", "rise") else -1
        elif re.search(r"\d", m.group(2)):
            out.append(sign * numbers(m.group(2))[0])
    return out


def run_years(p, changes):
    for c in changes:
        p = p + p * c / 100
    return p


def solve_years(k, q):
    changes = yearly_changes(q)
    size = max(others(q))
    if re.search(r"years ago|beginning of the first year", q):
        return ("number", unknown(lambda p: run_years(p, changes), size))
    return ("number", run_years(size, changes))


def solve31(k, q):
    x, y = pcts(q)[:2]                                            # males' rate first, then females'
    rest = others(q)
    P1, P2 = rest[0], rest[-1]
    hits = [m for m in range(int(P1) + 1) if m * (1 + x / 100) + (P1 - m) * (1 + y / 100) == P2]
    assert len(hits) == 1, (q, hits)
    m, f = F(hits[0]), P1 - hits[0]
    if "ratio" in q:
        return ("ratio", m / f)
    return ("number", m if "number of males" in q else f)


def solve32(k, q):
    r = pcts(q)[0]
    bill = F(100) * 100                                           # price 100, consumption 100
    c = unknown(lambda c: (100 + r) * c, bill)
    return ("number", 100 - c)


solve25 = solve26 = solve27 = solve28 = solve29 = solve30 = solve_years
