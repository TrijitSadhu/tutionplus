"""Independent solver for Ratio and Proportion Rules 18-25, keyed by row id / payload key; reads the numbers from the question in order.
Efficiency: the job counted in work units a day. Mixtures: the water added (or the milk in the can) is tried in half-litre steps until
the ratio fits. Shares and numbers: the multiplier k is tried 1, 2, 3 ... until the stated difference or the new ratio comes out.
Areas and volumes: squares and cubes of actual lengths are measured. Never the rule formula."""
import re
from fractions import Fraction as F

from solve_1_5 import vals


def two(q):
    return [(int(a), int(b)) for a, b in re.findall(r"(?<![\d:] )(\d+) : (\d+)(?! :)", q)]


def three(q):
    return [tuple(map(int, t)) for t in re.findall(r"(\d+) : (\d+) : (\d+)", q)]


def red(x, y):
    return ("ratio", F(x) / F(y))


def try_k(ok, step=F(1), hi=200000):
    for i in range(1, hi):
        if ok(i * step):
            return i * step
    raise ValueError("no k")


def plain(q, rs):
    """the numbers of the question that are not ratio terms."""
    terms = [t for p in rs for t in p]
    out = list(vals(q))
    for t in terms:
        out.remove(F(t))
    return out


ROWS = {727: 19, 728: 20, 729: 21, 730: 22, 731: 23, 732: 24, 733: 25}


def solve(k, q):
    try:
        r = ROWS[k] if isinstance(k, int) else int(re.match(r"r(\d+)_", k)[1])
        if r == 18:
            days, p = vals(q)[:2]
            a_rate = F(1) / days                                  # part of the job A does in a day
            b_rate = a_rate * (1 + p / 100) if "more efficient" in q else a_rate * (1 - p / 100)
            return ("number", 1 / b_rate)
        rs = two(q)
        if r == 19:
            (a, b), (c, d) = rs[:2]
            x = plain(q, rs[:2])[0]
            milk, water = x * F(a, a + b), x * F(b, a + b)
            return ("number", try_k(lambda w: milk / (water + w) == F(c, d), F(1, 2)))
        if r == 20:
            (a, b), (p, qq) = rs[:2]
            x = plain(q, rs[:2])[0]
            milk = try_k(lambda m: m / (m * F(b, a) + x) == F(p, qq), F(1, 2))
            water = milk * F(b, a)
            if "milk and how much water" in q:
                return ("pair", (milk, water))
            if "at first?" in q and "mixture" in q:
                return ("number", milk + water)
            if "there now" in q:
                return ("number", milk + water + x)
            if "How much milk" in q:
                return ("number", milk)
            return ("number", water)
        if r == 21:
            (a, b) = rs[0]
            diff = plain(q, rs[:1])[0]
            kk = try_k(lambda t: abs(a * t - b * t) == diff)
            last = re.split(r"[.?]\s+", q.strip().rstrip(".?"))[-1]      # the sentence that asks
            if re.search(r"sum|amount", last):
                return ("number", (a + b) * kk)
            return ("number", min(a, b) * kk)
        if r in (22, 23):
            power = 2 if r == 22 else 3
            if "times as long" in q:
                n = int(re.search(r"(\d+) times", q)[1])
                old, new = F(1) ** power, F(n) ** power
                return red(old, new) if "old" in q.split("ratio of the")[-1].split("to")[0] else red(new, old)
            (a, b) = rs[0]
            if "ratio of their sides" in q:                         # areas given
                x = try_k(lambda s: s * s == a)
                y = try_k(lambda s: s * s == b)
                return red(x, y)
            return red(F(a) ** power, F(b) ** power)
        if r in (24, 25):
            t3 = three(q)
            if t3:                                                  # three classes
                parts, new = t3[0], t3[1]
                x = plain(q, [parts, new])[0]
                sign = 1 if "join" in q else -1
                kk = try_k(lambda t: F(parts[0] * t + sign * x, parts[1] * t + sign * x) == F(new[0], new[1]))
                before = sum(parts) * kk
                return ("number", before + 3 * sign * x if "now" in q else before)
            (a, b), (c, d) = rs[:2]
            x = plain(q, rs[:2])[0]
            sign = -1 if re.search(r"taken|subtracted", q) else 1
            kk = try_k(lambda t: a * t + sign * x > 0 and F(a * t + sign * x) / (b * t + sign * x) == F(c, d))
            return ("pair", (a * kk, b * kk))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
