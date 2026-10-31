"""Formatting and option helpers for the Simple Interest generators: numbers as the questions write them, ratios in lowest
terms, money, and option builders (answer positions rotate a-d through helpers.place)."""
from fractions import Fraction as F
from math import gcd

from common import tex
from helpers import place

B = chr(92)


def nf(v):
    """12, 2.5, 12.96 (terminating decimals with up to 2 places), else a mixed fraction."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    for places in (1, 2):
        if (v * 10 ** places).denominator == 1:
            return f"{float(v):.{places}f}"
    return tex(v)


def M(s):
    return B + "(" + s + B + ")"


def UU(v, unit=""):
    if unit == "Rs":
        return "Rs " + M(nf(v))
    return M(nf(v)) + (f" {unit}" if unit else "")


def low(a, b):
    """a : b in lowest whole terms (a, b may be fractions)."""
    a, b = F(a), F(b)
    s = a.denominator * b.denominator
    x, y = int(a * s), int(b * s)
    g = gcd(x, y)
    return x // g, y // g


def R(a, b):
    return M(f"{a} : {b}")


def answer_json(a):
    return [a[0], [str(x) for x in a[1]] if isinstance(a[1], tuple) else str(a[1])]


def opts(v, unit="", wrong=None):
    v = F(v)
    if wrong is None:
        if v.denominator == 1:
            step = max(1, abs(v) // 10)
        else:
            step = F(1) if v > 2 else F(1, 10) if (v * 100).denominator == 1 else F(1, 2)
        wrong = [v + step, v - step, v + 2 * step] if v - step > 0 else [v + step, v + 2 * step, v + 3 * step]
    return place(UU(v, unit), [UU(w, unit) for w in wrong])


def ratio_opts(a, b, wrong=None):
    if wrong is None:
        cand = [(b, a), (a + 1, b), (a, b + 1), (a + 2, b + 1), (a + 1, b + 2)]
        val = F(a, b)
        wrong, seen = [], {val}
        for p, q in cand:
            if F(p, q) not in seen:
                wrong.append((p, q))
                seen.add(F(p, q))
            if len(wrong) == 3:
                break
    return place(R(a, b), [R(p, q) for p, q in wrong])


def pair_opts(x, y, unit="", wrong=None):
    x, y = F(x), F(y)
    f = (lambda p, q: f"Rs {M(nf(p))} and Rs {M(nf(q))}") if unit == "Rs" else (lambda p, q: f"{M(nf(p))} and {M(nf(q))}" + (f" {unit}" if unit else ""))
    if wrong is None:
        s = max(1, x // 10)
        wrong = []
        for c in [(y, x), (x + s, y - s), (x - s, y + s), (x + 2 * s, y - 2 * s), (x + s, y + s)]:   # first three distinct ones
            if c != (x, y) and c not in wrong:
                wrong.append(c)
        wrong = wrong[:3]
    return place(f(x, y), [f(p, q) for p, q in wrong])


def triple_opts(x, y, z, unit="", wrong=None):
    f = lambda p, q, r: f"{M(nf(p))}, {M(nf(q))} and {M(nf(r))}" + (f" {unit}" if unit else "")
    x, y, z = F(x), F(y), F(z)
    if wrong is None:
        wrong = [(z, y, x), (y, x, z), (x + 10, y - 10, z)]
    return place(f(x, y, z), [f(*w) for w in wrong])


def terms_opts(ts, wrong=None):
    """options for a ratio of 3+ terms: the right order plus orders with two terms swapped / one term changed."""
    ts = list(ts)
    f = lambda t: M(" : ".join(str(x) for x in t))
    if wrong is None:
        a = ts[:]
        a[0], a[1] = a[1], a[0]
        b = ts[:]
        b[-1], b[-2] = b[-2], b[-1]
        c = ts[:]
        c[1] += 1
        wrong = [a, b, c]
    return place(f(ts), [f(w) for w in wrong])
