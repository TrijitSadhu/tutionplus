"""Independent solver for Profit and Loss Rules 57-60 (one solve() for the four, told apart by their words). None uses the rule
formulas: 57 tries counts n = X, X - 1/4, ... until selling n a rupee gives the gain; 58/59 find the cost from two trial costs
(linear) and then price or compare in rupees; spoiled stock is counted as 100 quintals of which some are thrown away; 60 works on a
list price of Rs 100."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve(k, q):
    try:
        if "list price" in q:                                               # Rule 60
            x, y = [F(t) for t in re.findall(NUM + "%", q)][:2]
            cost = 100 - x
            if "above the price he paid" in q:
                return ("number", cost * (100 + y) / 100 - 100)
            return ("number", (100 + y - cost) / cost * 100)
        if "a rupee" in q and "How many" in q:                              # Rule 57
            X = F(re.search(r"(\d+) (?:a rupee|\w+ for one rupee)", q).group(1))
            x = F(re.search(r"loses " + NUM + "%", q).group(1))
            y = F(re.search(r"gain(?: of)? " + NUM + "%", q).group(1))
            cost = (F(1) / X) / (1 - x / 100)                               # cost of one article
            n = X
            while n > 0:
                if (F(1) / n) / cost - 1 == y / 100:
                    return ("number", n)
                n -= F(1, 4)
            return ("unsolved", "no count")
        if "spoiled" in q:                                                  # Rule 59, spoiled stock
            A = F(re.search(r"Rs " + NUM, q).group(1))
            s, y = [F(t) for t in re.findall(NUM + "%", q)][:2]
            outlay, left = 100 * A, 100 - s                                 # 100 quintals bought
            return ("number", outlay * (1 + y / 100) / left)
        rs = [F(t) for t in re.findall(r"Rs " + NUM, q)]
        frac = re.search(r"\\frac\{1\}\{(\d+)\}", q)
        if frac:
            x = F(100) / int(frac.group(1))
            loss = "loses" in q
        elif re.search(NUM + r"% is lost", q):
            x, loss = F(re.search(NUM + r"% is lost", q).group(1)), True
        else:                                                               # the first rate named is the one he got
            w, x = re.search(r"\b(gain|gains|profit|loss|loses) (?:of )?" + NUM + "%", q).groups()
            x, loss = F(x), w in ("loss", "loses")
        sign = -1 if loss else 1
        kg = re.findall(r"(\d+) kg", q)
        A = rs[0] / int(kg[0]) if kg else rs[0]
        cp = lin(lambda c: c * (1 + sign * x / 100) - A)                    # cost of one (per kg when sold by weight)
        if "gain or lose" in q or "gain or loss" in q:
            B = rs[1] / int(kg[1]) if kg else rs[1]
            return ("signed", (B - cp) / cp * 100)
        y = F(re.findall(NUM + "%", q)[-1])
        new = cp * (1 + y / 100)
        if "By how much" in q:
            return ("pair", (new - rs[0], new))
        return ("number", new)
    except Exception:
        return ("unsolved", q[:40])
