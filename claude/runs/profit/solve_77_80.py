"""Independent solver for Profit and Loss Rules 77-80 (one solve() for the four, told apart by their words). None uses the rule
formulas: 77 takes a cost of 100; 78 prices a stock of 1200 (or the stated kg at a trial cost per kg) part by part; 79 and 80 take a
selling price of 100 (79's selling price question by trial costs)."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def parts_of(q):
    fr = [F(int(a), int(b)) for a, b in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)]
    rates = [F(t) * (1 if w == "gain" else -1) for w, t in re.findall(r"a (gain|loss) of " + NUM + "%", q)]
    return fr + [1 - sum(fr)], rates


def solve(k, q):
    try:
        if "times the old price" in q:                                      # Rule 77
            x = F(re.search(r"profit of " + NUM + "%", q).group(1))
            n = F(re.search(r"to (\d+) times", q).group(1))
            return ("number", (100 + x) * n - 100)
        if "Had he sold all of it" in q:                                    # Rule 78, cost per kg
            W = F(re.search(r"buys (\d+) kg", q).group(1))
            fr, rates = parts_of(q)
            r = rates[-1]                                                   # the single rate is named last
            rates = rates[:-1]
            D = F(re.search(r"Rs " + NUM + " more", q).group(1))
            def extra(c):                                                   # money lost by not selling all at r%
                cost = W * c
                parts = sum(cost * f * x / 100 for f, x in zip(fr, rates))
                return cost * r / 100 - parts - D
            return ("number", lin(extra))
        if "on all of it" in q:                                              # Rule 78, result on the whole
            fr, rates = parts_of(q)
            whole = F(1200)
            net = sum(whole * f * x / 100 for f, x in zip(fr, rates))
            return ("signed", net / whole * 100)
        x = F(re.search(NUM + "% of the selling price", q).group(1))
        if "Find the selling price" in q:                                   # Rule 79, selling price from the cost
            C = F(re.search(r"Rs " + NUM, q).group(1))
            return ("number", lin(lambda s: s - s * x / 100 - C))
        sp = F(100)
        if "profit as" in q:                                                # Rule 79: the cost is what is left after the profit
            cp = sp - sp * x / 100
            return ("number", (sp - cp) / cp * 100)
        cp = sp + sp * x / 100                                              # Rule 80: the cost is the price plus the loss
        return ("number", (cp - sp) / cp * 100)
    except Exception:
        return ("unsolved", q[:40])
