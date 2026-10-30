"""Independent solver for Profit and Loss Rules 49 and 50: reads the counts and the 'so many a rupee' rates, then counts the money -
for Rule 50 it buys k articles at each rate for k = 1..lcm and checks the per cent is the same, then compares the takings with the
cost. Returns a signed per cent (positive = profit); not the rule formulas."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        if "the same number" in q:                         # Rule 50
            x, y = [F(t) for t in re.findall(r"at (\d+) a rupee", q)][:2]
            sale = re.search(r"sells them at (\d+) (?:a rupee|for (\d+) rupees)", q)
            z = F(sale.group(1)) / (F(sale.group(2)) if sale.group(2) else 1)
            seen = set()
            for n in (1, 2, 3, int(x * y)):                # any equal count gives the same per cent
                cost = n / x + n / y
                seen.add((2 * n / z - cost) / cost * 100)
            assert len(seen) == 1
            return ("signed", seen.pop())
        mm, x, nn, y, z = [F(t) for t in re.findall(r"\d+", q)][:5]   # Rule 49: m at x, n at y, all at z
        cost = sum(F(1) / x for _ in range(int(mm))) + sum(F(1) / y for _ in range(int(nn)))   # article by article
        takings = (mm + nn) / z
        return ("signed", (takings - cost) / cost * 100)
    except Exception:
        return ("unsolved", q[:40])
