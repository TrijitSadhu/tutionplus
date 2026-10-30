"""Independent solver for Profit and Loss Rules 81-84 (one solve() for the four, told apart by their words). None uses the rule
formulas: 81/82 put a price of Re 1 on each metre and find the cost of the lot from the stated gain / loss; 83 puts a cost of Re 1 on
each metre; 84 works on a cost of 100 (the mark-up from two trial values) or, for the rupee saving, on the marked price."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve(k, q):
    try:
        if "a draper sells" in q.lower():
            N, n = [F(t) for t in re.findall(r"(\d+(?:\.\d+)?) metres", q)][:2]
            if "equal to the cost of" in q:                                 # Rule 83: cost Re 1 a metre
                cost, gain = N, n
                return ("number", gain / cost * 100)
            takings = N                                                     # Rules 81 / 82: price Re 1 a metre
            if "his profit equals" in q:
                cost = takings - n
                return ("number", (takings - cost) / cost * 100)
            cost = takings + n
            return ("number", (cost - takings) / cost * 100)
        if "saves a woman Rs" in q:                                         # Rule 84, rupee saving
            x = F(re.search(NUM + "% discount", q).group(1))
            D = F(re.search(r"Rs " + NUM, q).group(1))
            marked = lin(lambda a: a * x / 100 - D)
            return ("number", marked - D)
        pc = [F(t) for t in re.findall(NUM + "%", q)]
        if "By what per cent above" in q:                                   # Rule 84, mark-up needed
            y, x = pc[:2]
            return ("number", lin(lambda up: (100 + up) * (100 - x) / 100 - (100 + y)))
        if "rate of discount" in q:                                         # Rule 84, discount rate
            up, y = pc[:2]
            return ("number", lin(lambda x: (100 + up) * (100 - x) / 100 - (100 + y)))
        up, x = pc[:2]                                                      # Rule 84, profit
        return ("number", (100 + up) * (100 - x) / 100 - 100)
    except Exception:
        return ("unsolved", q[:40])
