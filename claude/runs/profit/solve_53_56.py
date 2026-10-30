"""Independent solver for Profit and Loss Rules 53-56 (one solve() for all four, told apart by the question's words). None uses the
rule formulas:
- 53: tries every whole-rupee price of one A, takes B from the total cost, and keeps the one that gives the stated gain / loss;
- 54: tries N = 1, 2, ... of each kind until the money lost (or gained) is the stated amount;
- 55: works on a cost of Rs 100 (mark up, take the discount off); the mark-up from two trial values, the cost by scaling;
- 56: tries every whole-rupee cost of A until the loss on A equals the gain on B."""
import re
from fractions import Fraction as F


def n_(t):
    return F(t)


def solve(k, q):
    try:
        if "neither gains nor loses" in q:                                  # Rule 56
            P = n_(re.search(r"Rs (\d+)", q).group(1))
            x = n_(re.search(r"loss of (\d+(?:\.\d+)?)%", q).group(1))
            y = n_(re.search(r"gain of (\d+(?:\.\d+)?)%", q).group(1))
            for a in range(1, int(P)):
                if F(a) * x == (P - a) * y:
                    return ("pair", (F(a), P - a))
            return ("unsolved", "no cost")
        if "a rupee" in q and "How many" in q:                              # Rule 54
            x, y = [n_(t) for t in re.findall(r"at (\d+) a rupee", q)][:2]
            s = re.search(r"sells them at (\d+) (?:a rupee|for (\d+) rupees)", q)
            z = n_(s.group(1)) / (n_(s.group(2)) if s.group(2) else 1)
            w, L = re.search(r"makes a (loss|gain) of Rs (\d+)", q).groups()
            for N in range(1, 50000):
                lost = N / x + N / y - 2 * N / z
                if (lost if w == "loss" else -lost) == n_(L):
                    return ("number", F(2 * N))
            return ("unsolved", "no count")
        if "marks" in q or "marked price" in q:                            # Rule 55
            pc = [n_(t) for t in re.findall(r"(\d+(?:\.\d+)?)%", q)]
            if "By what per cent should it raise" in q:                              # mark-up needed: price on a cost of 100, linear in x
                y, z = pc[:2]
                f = lambda x: (100 + x) * (100 - y) / 100 - 100 - z
                return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
            x = pc[0]
            if "paise in a rupee" in q:
                y = n_(re.search(r"(\d+) paise", q).group(1))
            elif "On a bill" in q:
                B, D = [n_(t) for t in re.findall(r"Rs (\d+(?:\.\d+)?)", q)][:2]
                y = D / B * 100
            else:
                y = pc[1]
            sp = (100 + x) * (100 - y) / 100                                # selling price on a cost of 100
            if "find its cost price" in q:
                S = n_(re.search(r"for Rs (\d+(?:\.\d+)?)", q).group(1))
                return ("number", S / sp * 100)
            return ("signed" if "gain or loss" in q else "number", sp - 100)
        # Rule 53
        n, mm = [n_(t) for t in re.search(r"(\d+) \w+(?: \w+)? and (\d+) \w+", q).groups()]
        P = n_(re.search(r"Rs (\d+)", q).group(1))
        rates = [(w, n_(t)) for w, t in re.findall(r"(profit|loss) of (\d+(?:\.\d+)?)%", q)][:2]
        sold = re.search(r"sells them for Rs (\d+)", q)
        if sold:
            X = n_(sold.group(1)) - P
        else:
            wX, X = re.search(r"overall (gain|loss) is Rs (\d+)", q).groups()
            X = n_(X) * (-1 if wX == "loss" else 1)
        (wa, x), (wb, y) = rates
        x, y = x * (-1 if wa == "loss" else 1), y * (-1 if wb == "loss" else 1)
        for a in range(1, int(P / n) + 1):
            b = (P - n * a) / mm
            if b > 0 and n * a * x / 100 + mm * b * y / 100 == X:
                a = F(a)
                if "for all the" in q:
                    return ("pair", (n * a, mm * b))
                if "and of one" in q:
                    return ("pair", (a, b))
                return ("number", a)
        return ("unsolved", "no price")
    except Exception:
        return ("unsolved", q[:40])
