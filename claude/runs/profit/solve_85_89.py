"""Independent solver for Profit and Loss Rules 85-89 (one solve() for the five, told apart by their words). None uses the rule
formulas: 85 on a labelled price of 100; 86 and 88 undo the discount and the profit in rupees (86's cost from two trial costs); 87
rebuilds the company price, then prices the goods; 89 tries counts until selling n a rupee gives the gain."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?)"


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve(k, q):
    try:
        pc = [F(t) for t in re.findall(NUM + "%", q)]
        if "above the labelled price" in q:                                 # Rule 85
            x, y = pc[:2]
            paid, sold = 100 - x, 100 + y
            return ("number", (sold - paid) / paid * 100)
        if "Without the discount it would have made" in q:                  # Rule 86
            A = F(re.search(r"Rs " + NUM, q).group(1))
            x, y = pc[:2]
            lp = A / (1 - x / 100)
            return ("number", lin(lambda c: c * (1 + y / 100) - lp))
        if "company's original price" in q:                                 # Rule 87
            A = F(re.search(r"Rs " + NUM, q).group(1))
            x, y = pc[:2]
            company = lin(lambda p: p * (1 - x / 100) - A)
            return ("number", company * (1 + y / 100))
        if "without the discount?" in q:                                    # Rule 88
            A = F(re.search(r"Rs " + NUM, q).group(1))
            x, y = pc[:2]
            cost, labelled = A / (1 + y / 100), A / (1 - x / 100)
            return ("number", (labelled - cost) / cost * 100)
        X = F(re.search(r"at (\d+) a rupee", q).group(1))                  # Rule 89
        g = pc[0]
        n = X
        while n > 0:
            if (1 / n) / (1 / X) - 1 == g / 100:
                return ("number", n)
            n -= F(1, 4)
        return ("unsolved", "no count")
    except Exception:
        return ("unsolved", q[:40])
