"""Independent solver for Profit and Loss Rules 73-76 (one solve() for the four, told apart by their words). None uses the rule
formulas: 73 tries whole-rupee costs of the first article, takes the second from the first sale and checks the second sale; 74 takes
a cost of 100; 75 tries whole-rupee costs until the two gain per cents differ by d; 76 follows 100 grams bought and sold."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def solve(k, q):
    try:
        if "Had he sold them" in q:                                         # Rule 73
            S1, S2 = [F(t) for t in re.findall(r"Rs " + NUM, q)][:2]
            x, y = [F(t) for t in re.findall(NUM + "%", q)][:2]
            p, r = 1 + x / 100, 1 + y / 100
            for a in range(1, int(S1)):
                b = (S1 - p * a) / r
                if b > 0 and r * a + p * b == S2:
                    return ("pair", (F(a), b))
            return ("unsolved", "no cost")
        if "of its usual price" in q:                                       # Rule 74
            k_ = F(*map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", q).groups()))
            x = F(re.search(r"loss of " + NUM + "%", q).group(1))
            part = 100 - x                                                  # on a cost of 100
            return ("number", part / k_ - 100)
        if "gain per cent would have been" in q:                            # Rule 75
            d = F(re.search(r"would have been " + NUM + " less", q).group(1))
            S2, S1 = [F(t) for t in re.findall(r"Rs " + NUM, q)][:2]
            for c in range(1, int(S2) * 10):
                if ((S2 - c) - (S1 - c)) * 100 / c == d:
                    return ("number", F(c))
            return ("unsolved", "no cost")
        x, y = [F(t) for t in re.findall(NUM + "%", q)][:2]               # Rule 76
        grams_paid_for = F(100)                                             # pays for 100 g, gets more
        grams_got = grams_paid_for * (1 + x / 100)
        takings = grams_got * (1 + y / 100)                                 # charges for more than he hands over
        return ("number", (takings - grams_paid_for) / grams_paid_for * 100)
    except Exception:
        return ("unsolved", q[:40])
