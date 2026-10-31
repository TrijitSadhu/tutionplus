"""Shared helpers for the Simple Interest generators: the result dict, number formatters and option builders (answer positions rotate
a, b, c, d so the keys are spread)."""
from fractions import Fraction as F

from common import money, rbe, shortcut, solution, tex  # noqa: F401

POS = [1, 2, 3, 4, 3, 1, 4, 2]
_k = [0]


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb, fin), shortcut=shortcut(sc, fin))


def m(v):
    return money(F(v))


def U(v, unit=""):
    """A value with its unit, e.g. \\(55\\) marks, Rs \\(325\\)."""
    v = F(v)
    if unit == "Rs":
        return rf"Rs \({m(v)}\)"
    return rf"\({tex(v)}\)" + (f" {unit}" if unit else "")


def place(right, wrong):
    pos = POS[_k[0] % len(POS)]
    _k[0] += 1
    o = list(wrong)[:3]
    o.insert(pos - 1, right)
    assert len(set(o)) == 4, o
    return o, pos


def nopts(v, unit=""):
    v = F(v)
    step = max(1, abs(v) // 10) if v.denominator == 1 else F(1, 2)
    wrong = [v + step, v - step, v + 2 * step] if v - step > 0 else [v + step, v + 2 * step, v + 3 * step]
    return place(U(v, unit), [U(w, unit) for w in wrong])
