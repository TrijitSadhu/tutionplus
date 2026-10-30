"""Independent solver for Profit and Loss Rules 69-72 (one solve() for the four, told apart by their words). None uses the rule
formulas: 69 and 70 solve a linear equation from two trial values (the selling price / the first article's cost); 71 finds the rupee
profit on the first sale and the cost that makes the same rupee loss; 72 works on a marked price of 100."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve(k, q):
    try:
        if "per cent of the selling price" in q:                            # Rule 69
            pc = [F(t) for t in re.findall(NUM + "%", q)]
            x, y = (pc[0], pc[0]) if "each makes" in q else pc[:2]
            A = F(re.search(r"Rs " + NUM + " more", q).group(1))
            # first person's profit is x% of S; the second's cost is S/(1 + y/100)
            return ("number", lin(lambda S: S * x / 100 - (S - S / (1 + y / 100)) - A))
        if "cost price of the first is the same as the selling price of the second" in q:     # Rule 70
            A = F(re.search(r"Rs " + NUM, q).group(1))
            x = F(re.search(r"loss of " + NUM + "%", q).group(1))
            y = F(re.search(r"gain of " + NUM + "%", q).group(1))
            c = lin(lambda c: c * (1 - x / 100) + c - A)                    # c = cost of the first = price of the second
            sold = c * (1 - x / 100) + c
            cost = c + c / (1 + y / 100)
            return ("signed", sold - cost)
        if "neither profit nor loss" in q:                                  # Rule 71
            A = F(re.search(r"Rs " + NUM, q).group(1))
            x = F(re.search(r"profit of " + NUM + "%", q).group(1))
            y = F(re.search(r"loss of " + NUM + "%", q).group(1))
            gain = A - lin(lambda c: c * (1 + x / 100) - A)
            return ("number", lin(lambda c: c * y / 100 - gain))
        x1, P, x2 = [F(t) for t in re.findall(NUM + "%", q)][:3]          # Rule 72
        cost = (100 - x1) / (1 + P / 100)
        return ("number", ((100 - x2) - cost) / cost * 100)
    except Exception:
        return ("unsolved", q[:40])
