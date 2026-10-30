"""Independent solver for Profit and Loss Rules 61-64. Rules 61 and 63 use the sentences of Rules 60 / 55 and their solvers
(solve_57_60: list price of 100; solve_53_56: cost of 100, then scaling). Rule 62 follows the money: what A gets, what A pays back.
Rule 64 tries quantities 1, 2, 3, ... until the cost worked out from the losing sale equals the cost from the gaining sale.
None uses the rule formulas."""
import re
from fractions import Fraction as F
import solve_53_56
import solve_57_60

NUM = r"(\d+(?:\.\d+)?)"


def solve(k, q):
    try:
        if "list price" in q:
            return solve_57_60.solve(k, q)
        if "marks" in q:
            return solve_53_56.solve(k, q)
        if "sells it back to A" in q:                                       # Rule 62
            W = F(re.search(r"Rs " + NUM, q).group(1))
            x = F(re.search(r"loss of " + NUM + "%", q).group(1))
            y = F(re.search(r"gain of " + NUM + "%", q).group(1))
            got = W * (1 - x / 100)
            paid = got * (1 + y / 100)
            if "loss per cent and B's gain per cent" in q:
                return ("pair", ((paid - got) / W * 100, (paid - got) / got * 100))
            return ("number", paid - got)
        p1, p2 = [F(t) for t in re.findall(r"at Rs " + NUM, q)][:2]          # Rule 64
        L = F(re.search(r"loss of Rs " + NUM, q).group(1))
        G = F(re.search(r"gain of Rs " + NUM, q).group(1))
        for n in range(1, 100000):
            if p1 * n + L == p2 * n - G:
                return ("number", F(n))
        return ("unsolved", "no quantity")
    except Exception:
        return ("unsolved", q[:40])
