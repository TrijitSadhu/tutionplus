"""Independent solver for Profit and Loss Rules 65-68 (one solve() for the four, told apart by their words). None uses the rule
formulas: 65 solves "first price + M = price at the higher profit" for the cost (linear, from two trial costs); 66 builds a table of
prices by spreading the one known price along the 'costs as much as' links (a small graph walk); 67 takes an income of 100; 68 works
out both costs from the common selling price and compares in rupees."""
import re
from fractions import Fraction as F

NUM = r"(\d+(?:\.\d+)?|one)"


def num(t):
    return F(1) if t == "one" else F(t)


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def name(w):
    return w[:-1] if w.endswith("s") and w not in ("peas", "beans", "carrots", "nuts") else w


def solve(k, q):
    try:
        if "charges Rs" in q:                                               # Rule 65
            x, y = [F(t) for t in re.findall(r"profit of (\d+(?:\.\d+)?)%", q)][:2]
            M = F(re.search(r"charges Rs (\d+(?:\.\d+)?)", q).group(1))
            cp = lin(lambda c: c * (1 + x / 100) + M - c * (1 + y / 100))
            return ("pair", (cp, cp * (1 + x / 100)))
        if "saves" in q:                                                    # Rule 67
            x, y, z = [F(t) for t in re.findall(r"(\d+(?:\.\d+)?)%", q)][:3]
            old, new = 100 * x / 100, (100 + y) * z / 100
            return ("number", (new - old) / old * 100)
        if "sells two" in q:                                                # Rule 68
            A = F(re.search(r"Rs (\d+(?:\.\d+)?) (?:each|apiece)", q).group(1))
            if "on each" in q:
                p = F(re.search(r"profit of (\d+(?:\.\d+)?)%", q).group(1))
                rates = [p, p]
            else:
                rates = [F(t) * (1 if w == "profit" else -1) for w, t in re.findall(r"a (profit|loss) of (\d+(?:\.\d+)?)%", q)][:2]
            cost = sum(A / (1 + r / 100) for r in rates)
            return ("signed", (2 * A - cost) / cost * 100)
        if "as often as" in q:                                              # Rule 66, shares
            pairs = re.findall(r"([A-D]) gets Rs (\d+(?:\.\d+)?) as often as ([A-D]) gets Rs (\d+(?:\.\d+)?)", q)
            share = {pairs[0][0]: F(re.search(r"If A gets Rs (\d+(?:\.\d+)?)", q).group(1))}
            for _ in range(len(pairs)):
                for X, a, Y, b in pairs:
                    if X in share and Y not in share:
                        share[Y] = share[X] * F(b) / F(a)
            return ("number", share[re.search(r"how much does ([A-D]) get", q).group(1)])
        chain, rest = q.split(". If ")                                      # Rule 66, goods
        links = []
        for part in re.split(r", and |, ", chain):
            ms = re.findall(NUM + r" (?:kg of )?([a-z]+)", part)
            (q1, i1), (q2, i2) = ms[0], ms[-1]
            links.append((num(q1), name(i1), num(q2), name(i2)))
        kq, ki = re.findall(NUM + r" (?:kg of )?([a-z]+)", rest)[0]
        R = F(re.search(r"Rs (\d+(?:\.\d+)?)", rest).group(1))
        aq, ai = re.findall(NUM + r" (?:kg of )?([a-z]+)", rest)[-1]
        price = {name(ki): R / num(kq)}
        for _ in range(len(links)):
            for a, A_, b, B_ in links:                                      # a of A_ cost as much as b of B_
                if A_ in price and B_ not in price:
                    price[B_] = price[A_] * a / b
                if B_ in price and A_ not in price:
                    price[A_] = price[B_] * b / a
        return ("number", price[name(ai)] * num(aq))
    except Exception:
        return ("unsolved", q[:40])
