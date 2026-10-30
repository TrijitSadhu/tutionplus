"""Independent solver for the Profit and Loss Miscellaneous rows, keyed by row id; reads the numbers from the question in order and
works each problem out from first principles (costs and takings in rupees, trial values, small searches) - not the rule formulas."""
import re
from fractions import Fraction as F


def nums(q):
    fr = [F(int(a), int(b)) for a, b in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)]
    q = re.sub(r"\\frac\{\d+\}\{\d+\}", " FRAC ", q)
    out, fi = [], 0
    for t in re.findall(r"FRAC|\d+(?:\.\d+)?", q):
        if t == "FRAC":
            out.append(fr[fi]); fi += 1
        else:
            out.append(F(t))
    return out


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve(k, q):
    try:
        v = nums(q)
        if k in (382, 385):                                      # price, profit %, count, total / each
            A, x, N, B = v[:4]
            cost = A / (1 + x / 100)
            each = B / N if k == 382 else B
            return ("signed", (each - cost) / cost * 100)
        if k == 383:                                             # two discounts, price paid
            d1, d2, paid = v[:3]
            return ("number", lin(lambda p: p * (1 - d1 / 100) * (1 - d2 / 100) - paid))
        if k == 384:
            n, rate, extra, mp, d = v[:5]
            cost, take = n * rate + extra, sum(mp * (1 - d / 100) for _ in range(int(n)))
            return ("number", (take - cost) / cost * 100)
        if k == 386:                                             # try whole-rupee prices of a cup
            a1, b1, S1, a2, b2, S2 = v[:6]
            for c in range(1, int(S1)):
                p = (S1 - a1 * c) / b1
                if a2 * c + b2 * p == S2:
                    return ("number", c - p)
            return ("unsolved", "no price")
        if k == 387:
            x, kk = v[:2]
            sp = F(100); cp = sp - sp * x / 100
            return ("number", kk / 100 * cp / sp * 100)
        if k == 388:
            A, x, y = v[:3]
            cost = lin(lambda c: c * (1 - x / 100) - A)
            return ("number", cost * (1 + y / 100) - A)
        if k == 389:
            hi, lo = v[:2]
            return ("number", lin(lambda c: (hi - c) - (c - lo)))
        if k == 390:
            g, D, g2 = v[:3]
            return ("number", lin(lambda c: c * (1 + g / 100) - c * (1 - g2 / 100) - D))
        if k == 391:
            q1, r1, q2, r2, s = v[:5]
            return ("signed", (q1 + q2) * s - (q1 * r1 + q2 * r2))
        if k == 392:
            up, down = v[:2]
            before = F(1) * 100
            after = (1 + up / 100) * (100 - down)
            return ("signed", (after - before) / before * 100)
        if k == 393:
            kk, rs, each, profit = v[:4]
            n = 0
            while n < 100000:
                n += 1
                if n * each - n * rs / kk == profit:
                    return ("number", F(n))
            return ("unsolved", "no count")
        if k == 394:
            f, up = v[:2]
            sp = F(100)
            cost, take = f * sp, sp * (1 + up / 100)
            return ("number", (take - cost) / cost * 100)
        if k == 395:
            q1, r1, q2, r2, g = v[:5]
            return ("number", (q1 * r1 + q2 * r2) / (q1 + q2) * (1 + g / 100))
        if k == 396:
            S, p = v[:2]
            return ("number", lin(lambda c: (c - S) - c * p / 100))
        if k == 397:
            C, x, y = v[:3]
            return ("number", C * (1 - x / 100) * (1 - y / 100))
        if k == 398:
            x, S, y = v[:3]
            cost = lin(lambda c: c * (1 + y / 100) - S)
            mp = lin(lambda p: p * (1 - x / 100) - cost)
            return ("number", mp - cost)
        if k == 399:
            price = F(100)
            for d in v[:3]:
                price -= price * d / 100
            return ("number", 100 - price)
        if k == 400:
            d1, d2, D = v[:3]
            return ("number", lin(lambda M: M * (1 - d1 / 100) - M * (1 - d2 / 100) - D))
        if k == 401:
            y, x = v[:2]
            printed = F(100)
            cost = printed * (1 - x / 100) / (1 + y / 100)
            r = cost / printed
            return ("ratio", r)
        if k == 402:
            d1, d2, D = v[:3]
            lp = lin(lambda L: L * (d2 - d1) / 100 - D)
            return ("number", lp * (1 - d1 / 100))
        if k == 403:
            c, more, R, kk = v[:4]
            for cents in range(1, 100000):                       # try old prices in paise
                p = F(cents, 100)
                if R / (p * (1 - c / 100)) - R / p == more:
                    return ("number", p * kk)
            return ("unsolved", "no price")
        if k == 404:
            x, A, y = v[:3]
            cost = lin(lambda c: c * (1 - x / 100) - A)
            return ("number", cost * (1 + y / 100))
        return ("unsolved", "unknown row")
    except Exception:
        return ("unsolved", q[:40])
