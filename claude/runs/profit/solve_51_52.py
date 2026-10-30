"""Independent solver for Profit and Loss Rules 51 and 52. Rule 51: reads the total and the two gains and solves "price of A = price of
B" for A's cost (linear, from two trial costs). Rule 52: reads 'A a rupee' and the gain and tries counts n = A, A - 1/2, A - 1, ... until
selling n for a rupee gives exactly that gain. Neither uses the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        if "for a rupee" in q:                              # Rule 52
            A = F(re.search(r"at (\d+) a rupee", q).group(1))
            x = F(re.search(r"profit of (\d+(?:\.\d+)?)%", q).group(1))
            n = A
            while n > 0:
                if (1 / n) / (1 / A) - 1 == x / 100:       # price of one when n sell for Re 1, over its cost
                    return ("number", n)
                n -= F(1, 4)
            return ("unsolved", "no count")
        P = F(re.search(r"Rs (\d+)", q).group(1))
        x, y = [F(t) for t in re.findall(r"gain of (\d+(?:\.\d+)?)%", q)][:2]
        f = lambda c: c * (100 + x) - (P - c) * (100 + y)
        c = -f(F(0)) / (f(F(1)) - f(F(0)))
        return ("pair", (c, P - c))
    except Exception:
        return ("unsolved", q[:40])
