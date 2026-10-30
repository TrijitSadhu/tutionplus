"""Independent solver for Profit and Loss Rules 25-30. Reads x, X, y[, z] from the question, takes the direction of each per cent
from its own word (profit / gain or loss / lost), solves "first sale +/- X = second sale" for the cost price (linear in the cost,
from two trial costs) and then prices the article as the question asks - never through the rule formulas gen_25_30.py uses."""
import re
from fractions import Fraction as F
from sent_25_30 import KIND


def make(n):
    def solve(k, q):
        try:
            v = [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]
            x, X, y = v[:3]
            z = v[3] if len(v) > 3 else None
            words = re.findall(r"(profit|gain|loss|lost|lose)", q)
            if len(words) >= 2:
                s1 = 1 if words[0] in ("profit", "gain") else -1
                s2 = 1 if words[1] in ("profit", "gain") else -1
            else:                                            # "makes 8% ... makes 28%": the rule's story says which way
                s1, s2 = (1 if KIND[n][0] else -1), (1 if KIND[n][1] else -1)
            sign = -1 if re.search(r"Rs \d+ less|\d+ less,", q) else 1
            f = lambda c: c * (1 + s1 * x / 100) + sign * X - c * (1 + s2 * y / 100)
            cp = -f(F(0)) / (f(F(1)) - f(F(0)))
            if z is None:
                return ("pair", (cp, cp * (1 + s1 * x / 100)))
            spz = cp * (1 + z / 100)
            return ("pair", (spz, cp)) if re.search(r"(what did|also find|find its cost|and what|and the cost)", q, re.I) else ("number", spz)
        except Exception:
            return ("unsolved", q[:40])
    return solve
