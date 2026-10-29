"""LaTeX builders shared by the Permutation and Combination generators (factorials, nPr, nCr, products, case tables)."""
from fractions import Fraction as F
from math import comb, factorial, perm

from common import rbe, shortcut, solution


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb, fin), shortcut=shortcut(sc, fin))


def num(v):
    return ("number", F(v))


def I(s):
    """Inline math."""
    return rf"\({s}\)"


def D(s):
    """Display math."""
    return rf"\[ {s} \]"


def nP(n, r):
    return rf"{{}}^{{{n}}}P_{{{r}}}"


def nC(n, r):
    return rf"{{}}^{{{n}}}C_{{{r}}}"


def times(*parts):
    return r" \times ".join(str(p) for p in parts)


def falling(n, r):
    """n, n-1, ..., n-r+1 (the r factors of nPr)."""
    return list(range(n, n - r, -1))


def falling_tex(n, r):
    return times(*falling(n, r)) if r > 0 else "1"


def fin(expr, v):
    """Final Answer text: the expression and its value (or the value alone)."""
    return I(f"{expr} = {v}") if str(expr) != str(v) else I(v)


def factorise(v):
    """2^{3}\\times 3\\times 5 for 120."""
    out, d, x = [], 2, v
    while d * d <= x:
        k = 0
        while x % d == 0:
            x //= d
            k += 1
        if k:
            out.append(f"{d}^{{{k}}}" if k > 1 else str(d))
        d += 1
    if x > 1:
        out.append(str(x))
    return times(*out)


__all__ = ["F", "comb", "factorial", "perm", "result", "num", "I", "D", "nP", "nC", "times", "falling", "falling_tex", "fin", "factorise"]
