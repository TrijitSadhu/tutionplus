"""Independent Rule 2 solver: reads the numbers from each question and solves it from total cost and total
selling value (cost * (100 + p) = 100 * sale), never through the rule's fraction."""
import re
from fractions import Fraction as F


def nums(q):
    q = re.sub(r"(\d+)\\frac\{(\d+)\}\{(\d+)\}", lambda m: str(F(int(m[1])) + F(int(m[2]), int(m[3]))).replace("/", "÷"), q)
    out = []
    for t in re.findall(r"\d+(?:\.\d+)?(?:÷\d+)?", q):
        a, _, b = t.partition("÷")
        out.append(F(a) / (F(b) if b else 1))
    return out


def solve(rid, q):
    v = nums(q)
    gain = (lambda p: F(100 + p, 100))
    if rid in (836, "E7", "E8"):                     # x per kg (unknown kg), n kg at y, sold at z, gain p
        x, n, y, z, *rest = v
        p = rest[0] if rest else F(0)
        if "neither gain nor loss" in q:
            p = F(0)
        # cost: x*m + y*n ; sale: z*(m + n) ; sale*100 = cost*(100+p)  ->  linear in m
        m = (y * n * gain(p) - z * n) / (z - x * gain(p))
        return ("number", m)
    if rid in ("E1", "E2", "E4", "E9"):              # m kg at x, n kg at y, gain p -> selling price
        m, x, n, y, p = v
        return ("number", (m * x + n * y) * gain(p) / (m + n))
    if rid == "E3":                                  # m at x, n at unknown, sold at z with gain p
        m, x, n, z, p = v
        sale = z * (m + n)
        return ("number", (sale / gain(p) - m * x) / n)
    if rid in ("E5", "E6"):                          # ratio first : second, sold at z with gain p
        x, y, z, p = v
        # one kg of first and k kg of second: (x + y k) * gain = z (1 + k)
        k = (x * gain(p) - z) / (z - y * gain(p))
        return ("ratio", 1 / k)
    raise KeyError(rid)
