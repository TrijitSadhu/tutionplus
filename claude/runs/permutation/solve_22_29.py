"""Independent solvers for Permutation and Combination Rules 22-29 (book Combination Rules 9-16). Each reads the numbers from
the question text and COUNTS: distinct lines (a line through collinear points is stored once as the set of its points),
ordered sender/receiver pairs, pass/fail and attempt/skip patterns, real committees and words, fruit choices, shares
given out one person at a time, and identical things shared out (a memoised count over the persons) - never the formulas
gen_22_29.py uses."""
import re
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product

from solve_1_7 import WORDS, count, ints


def sel(n, r):
    return count(combinations(range(n), r))


def solve22(k, q):
    n, m = ints(q)[:2]
    line = frozenset(range(m))                                   # points 0..m-1 are collinear
    lines = {line if {a, b} <= line else frozenset((a, b)) for a, b in combinations(range(n), 2)}
    return ("number", F(len(lines)))


def solve23(k, q):
    m = re.search(r"delivers (\d+) cards", q)
    if m:
        C = int(m[1])
        return ("number", F(next(n for n in range(2, 100) if count(permutations(range(n), 2)) == C)))
    n = int(re.search(r"there are (\d+) students", q)[1])
    return ("number", F(count(permutations(range(n), 2))))       # (sender, receiver) pairs


def solve24(k, q):
    n = int(re.search(r"each of (\d+) subjects", q)[1])
    return ("number", F(sum(1 for s in product((0, 1), repeat=n) if any(s))))       # 1 = failed in that subject


def solve25(k, q):
    n = ints(q)[0]
    return ("number", F(sum(1 for s in product((0, 1), repeat=n) if any(s))))       # 1 = attempted / invited


def solve26(k, q):
    m = re.search(r"From (\d+) officers and (\d+) jawans, in how many ways can (\d+) be chosen to include exactly (\w+) officer", q)
    if m:
        off, jaw, n = int(m[1]), int(m[2]), int(m[3])
        r = 1 if m[4] == "one" else int(m[4])
        return ("number", F(sum(1 for g in combinations(range(off + jaw), n) if sum(x < off for x in g) == r)))
    if "consonants" in q:
        c, v, rc, rv = ints(q)[:4]
        letters = [("c", i) for i in range(c)] + [("v", i) for i in range(v)]
        return ("number", F(sum(1 for w in permutations(letters, rc + rv) if sum(x[0] == "c" for x in w) == rc)))
    if "at least one boy" in q:
        boys, girls = ints(q)[:2]
        n = WORDS[re.search(r"(\w+) children are to be selected", q)[1]]
        return ("number", F(sum(1 for g in combinations(range(boys + girls), n) if any(x < boys for x in g))))
    m = re.search(r"group of (\d+) men and (\d+) women be made out of a total of (\d+) men and (\d+) women", q) or \
        re.search(r"There are (\d+) men and (\d+) women and you need to form a committee of (\d+) men and (\d+) women", q)
    if m:
        a, b, c, d = map(int, m.groups())
        if "group of" in q:
            need_m, need_w, men, women = a, b, c, d
        else:
            men, women, need_m, need_w = a, b, c, d
        return ("number", F(sum(1 for g in combinations(range(men + women), need_m + need_w) if sum(x < men for x in g) == need_m)))
    m = re.search(r"(\d+) red, (\d+) white and (\d+) blue balls", q)
    balls = ["r"] * int(m[1]) + ["w"] * int(m[2]) + ["b"] * int(m[3])
    return ("number", F(sum(1 for t in combinations(range(len(balls)), 3) if len({balls[i] for i in t}) == 3)))


def solve27(k, q):
    m = re.search(r"(\d+) oranges, (\d+) apples,? (?:and )?(\d+) mangoes(?: and the remaining (\d+) fruits are of different kinds)?", q)
    x, y, z = int(m[1]), int(m[2]), int(m[3])
    n = int(m[4] or 0)
    choices = product(range(x + 1), range(y + 1), range(z + 1), *[(0, 1)] * n)
    return ("number", F(sum(1 for c in choices if any(c))))


def deal(things, shares, size):
    """Ways to give `size` things to each of `shares` named persons, one person after another (count the picks at each step)."""
    if shares == 0:
        return 1
    return count(combinations(range(things), size)) * deal(things - size, shares - 1, size)


def solve28(k, q):
    m = re.search(r"(\d+) different things be divided into (\w+) sets, each having (\d+) things", q)
    if m:                                                        # unnamed sets: the set holding the smallest thing left is picked each time
        N, size = int(m[1]), int(m[3])

        def sets(left):
            return 1 if left == 0 else count(combinations(range(left - 1), size - 1)) * sets(left - size)
        return ("number", F(sets(N)))
    N, persons = ints(q)[:2]
    return ("number", F(deal(N, persons, N // persons)))


def solve29(k, q):
    n, r = ints(q)[:2]

    @lru_cache(None)
    def ways(left, persons):                                     # the first person takes 0..left, the rest share what is left
        if persons == 1:
            return 1
        return sum(ways(left - a, persons - 1) for a in range(left + 1))
    return ("number", F(ways(n, r)))
