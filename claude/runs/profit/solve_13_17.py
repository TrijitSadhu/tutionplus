"""Independent solvers for Profit and Loss Rules 13-17. Each reads the per cents and the money from the question: Rule 13 searches
the marked price that leaves the wanted profit after the discount; Rules 14-16 search the first cost that, pushed forward through
every sale with its own profit or loss word, ends at the price paid; Rule 17 pushes Rs 100 through both sales - never through the
rule formulas gen_13_17.py uses."""
import re
from fractions import Fraction as F

WORDS = {"three": 3, "two": 2}


def pcts(q):
    return [F(x) for x in re.findall(r"(\d+(?:\.\d+)?)%", q)]


def rs(q):
    return [F(x) for x in re.findall(r"Rs (\d+(?:\.\d+)?)", q)]


def changes(q):
    """Signed per cents in the order the article travels: the word before each per cent says profit (gain) or loss."""
    out = []
    for m_ in re.finditer(r"(\d+(?:\.\d+)?)%", q):
        before = q[:m_.start()]
        last = max((before.rfind(w), s) for w, s in (("profit", 1), ("gain", 1), ("loss", -1), ("los", -1)))
        out.append(last[1] * F(m_.group(1)))
    m_ = re.search(r"(three|two) (?:shops|owners|dealers)", q)
    if m_ and len(out) == 1:
        out = out * WORDS[m_.group(1)]
    return out


def push(c, ch):
    for p in ch:
        c = c + c * p / 100
    return c


def search(ok, step=F(1, 100), top=200000):
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def make(n):
    def solve(k, q):
        try:
            if n == 13:
                ps = pcts(q)
                disc = [F(x) for x in re.findall(r"(\d+(?:\.\d+)?)% (?:discount|off)", q)] or \
                       [F(x) for x in re.findall(r"discount of (\d+(?:\.\d+)?)%", q)] or [F(x) for x in re.findall(r"(?:give|gives|giving|allows) (\d+(?:\.\d+)?)%", q)]
                d = disc[0]
                profit = [p for p in ps if p != d][0] if len(set(ps)) > 1 else d
                g = lambda u: (100 + u) * (100 - d) / 100 - (100 + profit)     # mark-up u -> price after the discount, linear in u
                return ("number", -g(F(0)) / (g(F(1)) - g(F(0))))
            if n == 17:
                return ("number", push(F(100), pcts(q)[:2]) - 100)
            ch = changes(q)
            if n == 14 and "cooker" in q:                     # the last seller's profit is stated after his price
                ch = changes(q)
            X = rs(q)[-1]
            f = lambda c: push(c, ch) - X                     # the final price is linear in the first cost: solve from two trial costs
            return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
        except Exception:
            return ("unsolved", q[:40])
    return solve
