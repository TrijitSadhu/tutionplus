"""Independent solver for Time & Distance rewording batch 5 (the old rule-less rows), keyed by row id. Reads the numbers from the
question in order and finds the answer by unit counting, km-by-km simulation, or searching for the value that makes the story's
own times agree - never through the rule formulas gen_b5.py uses."""
from fractions import Fraction as F
from validate import numbers


def search(ok, step=F(1, 20), top=5000):
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def solve(rid, q):
    try:
        v = numbers(q)
        if rid == 801:                                 # minutes, km/hr
            mins, s = v[:2]
            return ("number", s / 60 * mins)           # km per minute, times the minutes
        if rid == 802:                                 # km, km/hr
            D, s = v[:2]
            return ("number", search(lambda t: s * t == D, F(1, 4), 500))
        if rid == 803:                                 # km, hours
            D, t = v[:2]
            return ("number", search(lambda s: s * t == D, F(1, 2), 2000))
        if rid == 804:                                 # km/hr -> m/sec
            return ("number", v[0] * 1000 / 3600)
        if rid == 805:                                 # m/sec -> km/hr
            return ("number", v[0] * 3600 / 1000)
        if rid == 806:                                 # equal legs at x and y: take each leg 1 km
            x, y = v[:2]
            return ("number", 2 / (1 / x + 1 / y))
        if rid == 807:                                 # out x, average A: return speed
            x, A = v[:2]
            return ("number", search(lambda y: 2 / (1 / x + 1 / y) == A, F(1, 4), 1000))
        if rid == 808:                                 # km/hr, rest minutes after every km, km in all: walk it km by km
            x, rest, y = v[:3]
            t = F(0)
            for k in range(1, int(y) + 1):
                t += 60 / x
                if k < y:
                    t += rest
            return ("pair", (F(int(t) // 60), t - 60 * (int(t) // 60)))
        if rid == 809:                                 # x, late min, y, early min
            x, l, y, e = v[:4]
            return ("number", search(lambda D: D / x - D / y == (l + e) / 60))
        if rid == 810:                                 # x, late min, faster by inc, still late min
            x, l1, inc, l2 = v[:4]
            return ("number", search(lambda D: D / x - D / (x + inc) == (l1 - l2) / 60))
        if rid in (811, 831):                          # there at x, back at y, T hours in all
            x, y, T = v[:3]
            return ("number", search(lambda D: D / x + D / y == T))
        if rid == 812:                                 # T hours, first half at a, second half at b
            T, a, b = v[:3]
            return ("number", search(lambda D: D / 2 / a + D / 2 / b == T, F(1, 2), 5000))
        if rid in (813, 814):                          # D, clock of P's start, x, clock of Q's start, y
            D, c1, x, c2, y = v[:5]
            # hours after P's vehicle starts until the two have covered D together (Q's one moves from c2 on)
            T = search(lambda T: x * T + y * (T - (c2 - c1)) == D and T >= c2 - c1, F(1, 60), 100)
            return ("number", x * T)
        if rid == 815:                                 # fraction of usual speed, minutes late
            p, d = v[:2]
            return ("number", search(lambda T: T / p - T == d, F(1, 4), 1000))
        if rid == 816:                                 # x, clock, y, later clock - same direction
            x, c1, y, c2 = v[:4]
            T = search(lambda T: y * T == x * (T + c2 - c1), F(1, 60), 100)
            return ("number", y * T)
        if rid == 825:                                 # walk + ride = x, walk both ways = x + t
            x, t = v[:2]
            R = search(lambda R: 2 * (x - R) == x + t, F(1, 4), 100)
            return ("number", 2 * R)
        if rid == 826:                                 # A x hours, B starts t later, B y hours: parts of the road
            x, t, y = v[:3]
            return ("number", search(lambda T: T / x + (T - t) / y == 1, F(1, 60), 100))
        if rid == 827:                                 # A x hours, B starts t earlier, B y hours
            x, t, y = v[:3]
            return ("number", search(lambda T: T / x + (T + t) / y == 1, F(1, 60), 100))
        if rid == 828:                                 # minutes at speed, new minutes
            m1, s1, m2 = v[:3]
            return ("number", search(lambda s: s * m2 == s1 * m1, F(1, 4), 1000))
        if rid == 829:                                 # no-stop x, with-stop y
            x, y = v[:2]
            return ("number", search(lambda m: x * (60 - m) / 60 == y, F(1, 4), 60))
        if rid == 830:                                 # D, T, part done, part of time used
            D, T, p, qq = v[:4]
            return ("number", search(lambda s: s * T * (1 - qq) == D * (1 - p), F(1, 10), 500))
        if rid == 832:                                 # D, T, fraction of train time saved, hours early
            D, T, f, e = v[:4]
            tr = search(lambda t: f * t == e, F(1, 100), 100)
            va = D / (T - e)
            air = va * (T - tr)
            return ("ratio", air / (D - air))
        if rid == 833:                                 # minutes late, D, faster by p
            mins, D, p = v[:3]
            return ("number", search(lambda s: D / s - D / (s + p) == mins / 60, F(1, 4), 5000))
        if rid == 834:                                 # hours early, slower by p, D
            t, p, D = v[:3]
            return ("number", search(lambda s: s > p and D / (s - p) - D / s == t, F(1, 4), 2000))
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
