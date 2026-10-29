"""Independent solvers for Permutation and Combination Rules 14-21 (book Combination Rules 1-8). Each reads the numbers from
the question text and COUNTS the actual selections with itertools.combinations - groups, boxes, vertex triples, vertex
pairs that are not sides, pairs of lines, handshake pairs, committees that contain / avoid the particular members, point
triples that are not all on the line - never the formulas gen_14_21.py uses."""
import re
from fractions import Fraction as F
from itertools import combinations

from solve_1_7 import WORDS, count, ints

POLY = {"pentagon": 5, "hexagon": 6, "septagon": 7, "heptagon": 7, "octagon": 8, "nonagon": 9, "decagon": 10}


def sel(n, r):
    return count(combinations(range(n), r))


def sides_of(q):
    m = re.search(r"polygon of (\d+) sides|\((\d+) sides\)", q)
    if m:
        return int(m[1] or m[2])
    return next(v for k, v in POLY.items() if k in q)


def solve14(k, q):
    m = re.search(r"\{\}\^\{(\d+)\}C_\{(\d*)r(?:\s*\+\s*(\d+))?\} = \{\}\^\{\d+\}C_\{(\d*)r(?:\s*\+\s*(\d+))?\}", q)
    if m:
        n = int(m[1])
        a, b, c, d = int(m[2] or 1), int(m[3] or 0), int(m[4] or 1), int(m[5] or 0)
        rs = [r for r in range(1, n) if a * r + b <= n and c * r + d <= n and a * r + b != c * r + d
              and sel(n, a * r + b) == sel(n, c * r + d)]
        assert len(rs) == 1, rs
        return ("number", F(rs[0]))
    r1, k_, r2, p, qq = (int(x) for x in re.search(r"\{\}\^\{n\}C_\{(\d+)\} : \{\}\^\{n-(\d+)\}C_\{(\d+)\} = (\d+) : (\d+)", q).groups())
    ns = [n for n in range(r1, 30) if n - k_ >= r2 and sel(n, r1) * qq == sel(n - k_, r2) * p]
    assert len(ns) == 1, ns
    return ("number", F(ns[0]))


def solve15(k, q):
    if "a person be selected" in q:
        w, m = ints(q)[:2]
        return ("number", F(len(["w"] * w + ["m"] * m)))
    if "identical balls" in q:                                   # choose which boxes get a ball
        balls, boxes = ints(q)[:2]
        return ("number", F(sel(boxes, balls)))
    if "from 9 men and 6 women" in q or re.search(r"from (\d+) men and (\d+) women", q):
        size, men, women = ints(q)[:3]
        return ("number", F(sel(men + women, size)))
    nums = ints(q)
    if "groups consisting of" in q or "A group consisting" in q:
        return ("number", F(sel(nums[0], nums[1])))
    if "choose" in q and "questions" in q:
        return ("number", F(sel(nums[0], nums[1])))
    if "apples" in q:
        return ("number", F(sel(nums[0], nums[1])))
    if "committee of" in q:
        return ("number", F(sel(nums[0], nums[1])))
    raise ValueError(q)


def solve16(k, q):
    n = sides_of(q)
    return ("number", F(count(combinations(range(n), 3))))     # no three vertices of a polygon are collinear


def solve17(k, q):
    n = ints(q)[0] if "around a circle" in q else sides_of(q)
    adjacent = lambda a, b: (b - a) % n in (1, n - 1)
    return ("number", F(sum(1 for a, b in combinations(range(n), 2) if not adjacent(a, b))))


def solve18(k, q):
    m = re.search(r"Inside it, (\d+) lines are drawn parallel to AB and (\d+) lines parallel to AD", q)
    if m:
        h, v = int(m[1]) + 2, int(m[2]) + 2                      # the sides of ABCD are lines too
    else:
        h, v = ints(q)[:2]
    return ("number", F(sum(1 for _ in combinations(range(h), 2) for _ in combinations(range(v), 2))))


def solve19(k, q):
    m = re.search(r"total (?:number )?of (?:handshakes was )?(\d+)", q) or re.search(r"total of (\d+) handshakes", q)
    if m and "handshakes" in q and ("find the number of persons" in q or "how many members" in q):
        H = int(m[1])
        return ("number", F(next(n for n in range(2, 100) if sel(n, 2) == H)))
    n = ints(q)[0]
    return ("number", F(sel(n, 2)))


def solve20(k, q):
    m = re.search(r"There are (\d+) members in a delegation .*total number of members is (\d+)", q)
    if m:
        size, n = int(m[1]), int(m[2])
        r = 1 if "a particular member" in q else WORDS.get(re.search(r"(\w+) particular members", q)[1]) or int(re.search(r"(\d+) particular members", q)[1])
        special = set(range(r))
        groups = list(combinations(range(n), size))
        inc = sum(1 for g in groups if special <= set(g))
        exc = sum(1 for g in groups if not special & set(g))
        return ("pair", (F(inc), F(exc)))
    size, n = ints(q)[:2]
    r = WORDS[re.search(r"such that (\w+) particular persons", q)[1]]
    return ("number", F(sum(1 for g in combinations(range(n), size) if set(range(r)) <= set(g))))


def solve21(k, q):
    n, m = ints(q)[:2]
    line = set(range(m))                                         # points 0..m-1 are the collinear ones
    return ("number", F(sum(1 for t in combinations(range(n), 3) if not set(t) <= line)))
