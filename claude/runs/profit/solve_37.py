"""Independent solver for Profit and Loss Rule 37, keyed by row id / payload key. Puts a price on each article (Re 1 of cost),
works out what the articles really sell for from the question's own statement, and compares - not through the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        v = [F(t) for t in re.findall(r"\d+", q)]
        if k == 331:                                   # selling a/b of the stock brings in the cost of all of it
            a, b = v[:2]
            sp_all = 1 / (a / b)                       # stock costs Rs 1; that fraction sells for Rs 1, so all of it sells for 1/(a/b)
            return ("number", (sp_all - 1) * 100)
        if k == "r37_e4":                              # selling N metres gains the cost of n metres
            N, n = v[:2]
            return ("number", n / N * 100)
        if k in ("r37_e2", "r37_e6"):                  # sells y for the money (cost) of x
            y, x = v[:2]
        else:                                          # cost of x = selling price of y
            x, y = v[:2]
        cost_each, sale_each = F(1), x / y             # x articles cost Rs x and that is the price of y articles
        return ("number", (sale_each - cost_each) * 100 / cost_each)
    except Exception:
        return ("unsolved", q[:40])
