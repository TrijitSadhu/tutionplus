"""Independent solver for P&C rewording batch 1, keyed by row id. Reads the numbers from the question and counts by brute
force: every number written with the allowed digits, every way of posting / giving out, every selection of people or
fruit, every order of the blocks on the shelf - never through the formulas gen_*.py use."""
import re
from fractions import Fraction as F
from itertools import combinations, permutations, product


def ints(q):
    return [int(x) for x in re.findall(r"\d+", q)]


def digits(q):
    m = re.search(r"digits ([\d,\s]+and \d)", q)
    return sorted(set(int(x) for x in re.findall(r"\d", m[1])))


def made(ds, lengths, repeat=False):
    for L in lengths:
        for t in (product(ds, repeat=L) if repeat else permutations(ds, L)):
            if t[0] != 0:
                yield int("".join(map(str, t)))


def group_count(people, size, ok):
    return sum(1 for g in combinations(range(sum(people)), size) if ok(sum(1 for x in g if x < people[0])))


def solve(rid, q):
    try:
        if rid == 846:
            return ("number", F(sum(1 for _ in made(digits(q), [3]))))
        if rid in (2060, 2061):
            lo, hi = map(int, re.search(r"greater than (\d+) and less than (\d+)", q).groups())
            return ("number", F(sum(1 for x in made(digits(q), range(1, 5)) if lo < x < hi)))
        if rid == 2062:
            return ("number", F(sum(1 for x in made(digits(q), [3]) if x % 2 == 0)))
        if rid == 2063:
            lo = int(re.search(r"greater than (\d+)", q)[1])
            return ("number", F(sum(1 for x in made(digits(q), [3]) if x > lo)))
        if rid == 2064:
            ds = digits(q)
            return ("number", F(sum(1 for x in made(ds, range(1, len(ds) + 1)) if x > 0) + (0 if 0 not in ds else 0)))
        if rid == 847:                                   # letters, post boxes
            letters, boxes = ints(q)[:2]
            return ("number", F(sum(1 for _ in product(range(boxes), repeat=letters))))
        if rid == 2065:                                  # three prizes among N girls
            girls = ints(q)[0]
            return ("number", F(sum(1 for _ in product(range(girls), repeat=3))))
        if rid == 2068:                                  # four-digit numbers, digits may repeat
            return ("number", F(sum(1 for _ in made(digits(q), [4], repeat=True))))
        if rid == 2107:                                  # 12 books: singles + sets kept together
            total, singles, *sets = ints(q)[:6]
            assert singles + sum(sets) == total
            units = sum(1 for _ in permutations(range(singles + len(sets))))
            inside = 1
            for s in sets:
                inside *= sum(1 for _ in permutations(range(s)))
            return ("number", F(units * inside))
        if rid == 856:
            n = int(re.search(r"polygon of (\d+) sides", q)[1])
            return ("number", F(sum(1 for _ in combinations(range(n), 3))))
        if rid in (866, 2153):                           # From a A and b B, pick n with exactly one A
            a, b, n = ints(q)[:3]
            return ("number", F(group_count((a, b), n, lambda k: k == 1)))
        if rid == 2152:                                  # team of n from a boys and b girls, exactly r boys
            n, a, b, r = ints(q)[:4]
            return ("number", F(group_count((a, b), n, lambda k: k == r)))
        if rid == 2154:                                  # a players, b coaches, group of n, exactly r players
            a, b, n, r = ints(q)[:4]
            return ("number", F(group_count((a, b), n, lambda k: k == r)))
        if rid == 2190:                                  # group of n from a doctors, b nurses, at least one doctor
            n, a, b = ints(q)[:3]
            return ("number", F(group_count((a, b), n, lambda k: k >= 1)))
        if rid == 2191:                                  # a girls, b boys, team of n, at least one girl
            a, b, n = ints(q)[:3]
            return ("number", F(group_count((a, b), n, lambda k: k >= 1)))
        if rid == 2192:                                  # committee of n from a men and b women, at least r men
            n, a, b, r = ints(q)[:4]
            return ("number", F(group_count((a, b), n, lambda k: k >= r)))
        if rid in (867, 2156):                           # alike fruits / marbles of three kinds: take some
            x, y, z = ints(q)[:3]
            return ("number", F(sum(1 for c in product(range(x + 1), range(y + 1), range(z + 1)) if any(c))))
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
