"""Independent solvers for Permutation and Combination Rules 30-36 (book Combination Rules 17-23) and the Miscellaneous
'at least' committees. They COUNT: vertex quadruples, point pairs and triples, pass/fail and win/loss/draw patterns,
forecasts compared with one fixed actual result, and real committees - never the formulas gen_30_36.py uses."""
import re
from fractions import Fraction as F
from itertools import combinations, product

from solve_1_7 import count, ints
from solve_14_21 import sides_of


def solve30(k, q):
    return ("number", F(count(combinations(range(sides_of(q)), 4))))


def solve31(k, q):
    return ("number", F(count(combinations(range(ints(q)[0]), 2))))


def solve32(k, q):
    return ("number", F(count(combinations(range(ints(q)[0]), 3))))


def solve33(k, q):
    return ("number", F(count(product(("pass", "fail"), repeat=ints(q)[0]))))


def solve34(k, q):
    return ("number", F(count(product(("win", "loss", "draw"), repeat=ints(q)[0]))))


def forecasts(n, results):
    actual = (results[0],) * n                                  # any fixed actual outcome
    allf = list(product(results, repeat=n))
    right = sum(1 for f in allf if all(a == b for a, b in zip(f, actual)))
    wrong = sum(1 for f in allf if all(a != b for a, b in zip(f, actual)))
    return len(allf), right, wrong


def solve35(k, q):
    n = ints(q)[0]
    tot, right, _ = forecasts(n, ("win", "loss"))
    return ("pair", (F(tot), F(right))) if "(ii)" in q else ("number", F(tot))


def solve36(k, q):
    n = ints(q)[0]
    _, right, wrong = forecasts(n, ("win", "loss", "draw"))
    return ("pair", (F(right), F(wrong))) if "(ii)" in q else ("number", F(right))


def solve_misc(k, q):
    m = re.search(r"From (\d+) officers and (\d+) jawans, in how many ways can (\d+) be chosen to include at least one officer", q)
    if m:
        off, jaw, n = map(int, m.groups())
        return ("number", F(sum(1 for g in combinations(range(off + jaw), n) if any(x < off for x in g))))
    men, women, n = (int(x) for x in re.search(r"(\d+) men and (\d+) women a committee of (\d+)", q).groups())
    groups = list(combinations(range(men + women), n))           # persons 0..men-1 are the men
    if "at least one woman" in q:
        return ("number", F(sum(1 for g in groups if any(x >= men for x in g))))
    need = int(re.search(r"at least (\d+) men", q)[1])
    return ("number", F(sum(1 for g in groups if sum(x < men for x in g) >= need)))
