"""Independent Rule 28 solver for the reworded rows: follows the liquid one draw at a time (no power formula). Reads the
amount and the draw from the first two numbers, or the fraction from a word (one-third, one-tenth, ...), and the number of
draws from "<word> times in all". What is asked: "removed" -> part removed; "at first" -> left : original; "ratio" ->
liquid : water; otherwise the amount left."""
import re
from fractions import Fraction as F
from validate import numbers

FRAC = {"one-half": F(1, 2), "one-third": F(1, 3), "one-fourth": F(1, 4), "one-fifth": F(1, 5), "one-sixth": F(1, 6),
        "one-tenth": F(1, 10), "one-twentieth": F(1, 20)}
TIMES = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6}


def solve(rid, q):
    try:
        n = TIMES[re.search(r"\b(\w+) times in all", q)[1].lower()]
        frac = next((v for w, v in FRAC.items() if w in q.lower()), None)
        x, y = (F(1), frac) if frac is not None else numbers(q)[:2]
        left = x
        for _ in range(n):
            left -= left * y / x
        if "removed" in q:
            return ("number", 1 - left / x)
        if "at first" in q:
            return ("ratio", left / x)
        if re.search(r"\bratio\b", q):
            return ("ratio", left / (x - left))
        return ("number", left)
    except Exception:
        return ("unsolved", q[:40])
