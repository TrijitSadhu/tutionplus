"""Independent solvers for Permutation and Combination Rules 1-7. Each reads the numbers from the question text and COUNTS
by brute force - it lists every arrangement, digit string, assignment or seating pattern and counts the ones that meet the
condition - never through the rule formulas gen_1_7.py uses. Seating problems enumerate the patterns (which seats the
restricted group takes) and multiply by the orders of the people inside each group."""
import re
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import factorial

WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


def ints(q):
    return [int(x) for x in re.findall(r"\d+", q)]


def count(it):
    return sum(1 for _ in it)


def word_num(q, noun):
    m = re.search(rf"(\d+|{'|'.join(WORDS)})\s+(?:[\w.-]+\s+)?{noun}", q)
    t = m.group(1)
    return int(t) if t.isdigit() else WORDS[t]


# ---------------------------------------------------------------- Rule 1
def solve1(k, q):
    m = re.search(r"\{\}\^\{n\}P_\{(\d+)\}\s*=\s*(\d+)", q)
    if m:                                             # find n: try n = r, r+1, ... and count the ordered r-tuples
        r, v = int(m[1]), int(m[2])
        return ("number", F(next(n for n in range(r, 60) if count(permutations(range(n), r)) == v)))
    m = re.search(r"\{\}\^\{(\d+)\}P_\{r\}\s*=\s*(\d+)", q)
    if m:                                             # find r: count ordered r-tuples for r = 0, 1, 2, ...
        n, v = int(m[1]), int(m[2])
        return ("number", F(next(r for r in range(0, 6) if count(permutations(range(n), r)) == v)))
    m = re.search(r"\{\}\^\{(\d+)\}P_\{(\d+)\}", q)
    if m:
        return ("number", F(count(permutations(range(int(m[1])), int(m[2])))))
    m = re.search(r"'([A-Z]+)'", q)
    if m:
        word = m[1]
        size = int(re.search(r"(\d+)-letter", q)[1]) if "-letter" in q else len(word)
        return ("number", F(len(set(permutations(word, size)))))
    if "buses" in q:                                  # (going bus, returning bus) pairs with different buses
        n = ints(q)[0]
        return ("number", F(sum(1 for a, b in product(range(n), repeat=2) if a != b)))
    if "taps" in q:                                   # each man gets a different tap
        men, taps = ints(q)[:2]
        return ("number", F(count(permutations(range(taps), men))))
    raise ValueError(q)


# ---------------------------------------------------------------- Rule 2
def digit_list(q):
    m = re.search(r"digits ([\d,\s]+(?:and \d)?)", q)
    return sorted(set(int(x) for x in re.findall(r"\d", m[1])))


def numbers_from(digits, lengths):
    """Every number written with distinct digits from the list, no leading zero."""
    for L in lengths:
        for t in permutations(digits, L):
            if t[0] != 0 or L == 1 and False:
                yield int("".join(map(str, t)))


def solve2(k, q):
    if "telephone" in q:
        L, start = int(re.search(r"(\d+)-digit", q)[1]), re.search(r"starts with (\d+)", q)[1]
        rest = [d for d in range(10) if str(d) not in start]
        return ("number", F(count(permutations(rest, L - len(start)))))
    if "chairs" in q or "roads" in q:
        a, b = (ints(q)[:2] if "roads" in q else [WORDS[w] for w in re.findall(r"\b(ten|eight)\b", q)])
        return ("number", F(count(product(range(a), range(b)))))
    digits = digit_list(q)
    if q.startswith("What is the sum"):
        return ("number", F(sum(int("".join(map(str, t))) for t in permutations(digits))))
    if "any number of the digits" in q:
        return ("number", F(sum(1 for x in numbers_from(digits, range(1, len(digits) + 1)) if x > 0)))
    m = re.search(r"between (\d+) and (\d+)", q)
    if m:
        lo, hi = int(m[1]), int(m[2])
        return ("number", F(sum(1 for x in numbers_from(digits, range(1, 5)) if lo < x < hi)))
    four = numbers_from(digits, [4])
    if "even" in q:
        return ("number", F(sum(1 for x in four if x % 2 == 0)))
    m = re.search(r"greater than (\d+)", q)
    if m:
        return ("number", F(sum(1 for x in four if x > int(m[1]))))
    return ("number", F(count(four)))


# ---------------------------------------------------------------- Rule 3
def solve3(k, q):
    if "invite" in q:
        friends, servants = word_num(q, "friends"), word_num(q, "servants")
        return ("number", F(count(product(range(servants), repeat=friends))))
    if "coin" in q:
        return ("number", F(count(product("HT", repeat=ints(q)[0]))))
    if "rings of different types" in q:
        rings, fingers = ints(q)[:2]
        return ("number", F(count(product(range(fingers), repeat=rings))))
    if "prizes" in q:
        prizes, boys = ints(q)[:2]
        return ("number", F(count(product(range(boys), repeat=prizes))))
    if "signal" in q:                                 # position 0 = rest; all arms at rest is no signal
        arms, pos = ints(q)[:2]
        return ("number", F(sum(1 for s in product(range(pos), repeat=arms) if any(s))))
    if "lock" in q:
        rings, letters = ints(q)[:2]
        return ("number", F(sum(1 for s in product(range(letters), repeat=rings) if s != (0,) * rings)))
    m = re.search(r"greater than (\d+) but not greater than (\d+)", q)
    lo, hi = int(m[1]), int(m[2])
    allowed = set(str(d) for d in digit_list(q))
    return ("number", F(sum(1 for x in range(lo + 1, hi + 1) if set(str(x)) <= allowed)))


# ---------------------------------------------------------------- Rules 4-7: seating patterns
def patterns(total, k, ok):
    """Number of ways to choose which k of the total seats the special group takes, meeting ok(seats)."""
    return sum(1 for s in combinations(range(total), k) if ok(s))


def no_two_adjacent(s):
    return all(b - a > 1 for a, b in zip(s, s[1:]))


def solve4(k, q):
    m = re.search(r"(\d+) I\.A\. and (\d+) I\.Sc\.", q)
    if m:
        a, b = int(m[1]), int(m[2])
    else:
        total, b = ints(q)[:2]
        a = total - b
    return ("number", F(patterns(a + b, b, no_two_adjacent) * factorial(a) * factorial(b)))


def solve5(k, q):
    n = ints(q)[0]
    return ("number", F(patterns(n, 2, lambda s: s[1] - s[0] > 1) * 2 * factorial(n - 2)))


def solve6(k, q):
    boys, girls = (int(x) for x in re.search(r"(\d+) boys and (\d+) girls", q).groups())
    g, o = (boys, girls) if re.search(r"all the (?:\w+ )?boys do not", q) else (girls, boys)
    block = lambda s: s[-1] - s[0] == len(s) - 1
    return ("number", F(patterns(g + o, g, lambda s: not block(s)) * factorial(g) * factorial(o)))


def solve7(k, q):
    boys, girls = (int(x) for x in re.search(r"(\d+) boys and (\d+) girls", q).groups())
    alt = lambda s: all(((i in s) != (i + 1 in s)) for i in range(boys + girls - 1))
    return ("number", F(patterns(boys + girls, girls, alt) * factorial(boys) * factorial(girls)))
