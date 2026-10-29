"""Independent solvers for Permutation and Combination Rules 8-13. They COUNT, never use the rule formulas of gen_8_13.py:
- words / balls: a memoised count that builds the arrangement letter by letter (distinct letters only, so alike letters are
  never double counted) and rejects any partial word that breaks the condition (vowels together, ending letter, places);
- people in groups: the same count over group labels (each label must stay in one block), times the orders of the people;
- circles: count the seat patterns that alternate all the way round (or keep the group in one arc), times the orders of the
  people, divided by the number of rotations; necklaces: list the circular orders with bead 0 fixed and keep one of each
  mirror pair."""
import re
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
from math import factorial

from solve_1_7 import WORDS, ints, solve7

VOW = set("AEIOU")


def count_seq(counts, step, init, final=lambda st: True):
    """Number of different sequences using each label exactly counts[label] times; step(state, label, pos) -> new state or None."""
    labels = sorted(counts)
    n = sum(counts.values())

    @lru_cache(None)
    def go(rem, st):
        left = sum(rem)
        if left == 0:
            return 1 if final(st) else 0
        pos = n - left
        tot = 0
        for i, k in enumerate(rem):
            if k:
                ns = step(st, labels[i], pos)
                if ns is not None:
                    tot += go(rem[:i] + (k - 1,) + rem[i + 1:], ns)
        return tot
    return go(tuple(counts[l] for l in labels), init)


def letters(word):
    c = {}
    for ch in word:
        c[ch] = c.get(ch, 0) + 1
    return c


def together(st, ch, pos):                         # 0: no vowel yet, 1: inside the vowel run, 2: run finished
    if ch in VOW:
        return None if st == 2 else 1
    return 2 if st == 1 else st


def blocks(groups):
    """Step function: every label in `groups` must appear in one unbroken block."""
    def step(st, ch, pos):
        cur, closed = st
        if ch in groups and ch == cur:
            return st
        if ch in closed:
            return None
        closed2 = closed | {cur} if cur is not None else closed
        return (ch, closed2) if ch in groups else (None, closed2)
    return step


def word_of(q):
    return re.search(r"word '?([A-Z]{3,})'?", q)[1]


def total(word):
    return count_seq(letters(word), lambda st, ch, pos: 0, 0)


# ---------------------------------------------------------------- Rules 8-11
def solve8(k, q):
    return solve7(k, q)


def solve9(k, q):
    a, b = ints(q)[:2]
    n = a + b
    alt = lambda s: all(((i in s) != ((i + 1) % n in s)) for i in range(n))      # alternate all the way round
    linear = sum(1 for s in combinations(range(n), b) if alt(s)) * factorial(a) * factorial(b)
    return ("number", F(linear, n))                                              # n rotations give the same circle


def solve10(k, q):
    if "circular order" in q:
        n = ints(q)[0]
        return ("number", F(sum(1 for _ in permutations(range(n))), n))
    n = ints(q)[0]
    m = WORDS[re.search(r"(\w+) particular delegates", q)[1]]
    arc = lambda s: any(all((st + j) % n in s for j in range(m)) for st in range(n))   # the m seats form one arc
    linear = sum(1 for s in combinations(range(n), m) if arc(s)) * factorial(m) * factorial(n - m)
    return ("number", F(linear, n))


def solve11(k, q):
    n = ints(q)[0]
    return ("number", F(sum(1 for p in permutations(range(1, n)) if p[0] < p[-1])))   # bead 0 fixed; keep one of each mirror pair


# ---------------------------------------------------------------- Rule 12
def solve12(k, q):
    if "periods" in q:
        periods, subjects = ints(q)[:2]
        return ("number", F(sum(1 for s in product(range(subjects), repeat=periods) if len(set(s)) == subjects)))
    m = re.search(r"(\d+) yellow, (\d+) green and (\d+) black balls", q)
    if m:
        return ("number", F(count_seq({"Y": int(m[1]), "G": int(m[2]), "B": int(m[3])}, lambda st, ch, pos: 0, 0)))
    m = re.search(r"seven different letters, of which (\w+) are vowels and (\w+) are consonants", q)
    if m:
        v, c = WORDS[m[1]], WORDS[m[2]]
        pats = sum(1 for s in combinations(range(v + c), v) if all(b - a > 1 for a, b in zip(s, s[1:])))
        return ("number", F(pats * factorial(v) * factorial(c)))
    word = word_of(q)
    n = len(word)
    cnt = letters(word)
    if "come together" in q:
        return ("number", F(count_seq(cnt, together, 0)))
    if "not all together" in q:
        return ("number", F(total(word) - count_seq(cnt, together, 0)))
    m = re.search(r"end in ([A-Z])", q)
    if m:
        last = m[1]
        ends = count_seq(cnt, lambda st, ch, pos: None if pos == n - 1 and ch != last else 0, 0)
        return ("pair", (F(total(word) - 1), F(ends)))
    if "rearranged" in q:
        return ("number", F(total(word) - 1))
    if "relative order" in q:
        return ("number", F(count_seq(cnt, lambda st, ch, pos: 0 if (ch in VOW) == (word[pos] in VOW) else None, 0)))
    m = re.search(r"(even|odd) (?:places|positions)", q)
    if m:
        want = 0 if m[1] == "even" else 1                                         # 1-based place number parity
        return ("number", F(count_seq(cnt, lambda st, ch, pos: None if ch in VOW and (pos + 1) % 2 != want else 0, 0)))
    return ("number", F(total(word)))


# ---------------------------------------------------------------- Rule 13
def solve13(k, q):
    if "letters of the word" in q:
        return ("number", F(count_seq(letters(word_of(q)), together, 0)))
    m = re.search(r"(\d+) Indians, (\d+) Americans and (\d+) Englishmen", q)
    if m:
        sizes = dict(zip("IAE", map(int, m.groups())))
        pats = count_seq(sizes, blocks(set(sizes)), (None, frozenset()))
        return ("number", F(pats * factorial(sizes["I"]) * factorial(sizes["A"]) * factorial(sizes["E"])))
    m = re.search(r"(\d+) are single volumes and the others are books of (\d+), (\d+) and (\d+) volumes", q)
    if m:
        singles, *vols = map(int, m.groups())
        counts = {f"s{i}": 1 for i in range(singles)} | {f"b{i}": v for i, v in enumerate(vols)}
        pats = count_seq(counts, blocks({f"b{i}" for i in range(len(vols))}), (None, frozenset()))
        mult = 1
        for v in vols:
            mult *= factorial(v)                                                  # the volumes of one book are different
        return ("number", F(pats * mult))
    m = re.search(r"(\w+) books with (\w+) copies each and (\w+) other books with (\w+) copies each", q)
    if m:
        n1, c1, n2, c2 = (WORDS.get(x) or int(x) for x in m.groups())
        counts = {f"a{i}": c1 for i in range(n1)} | {f"b{i}": c2 for i in range(n2)}
        return ("number", F(count_seq(counts, blocks(set(counts)), (None, frozenset()))))   # copies alike: no extra factor
    boys, girls = (int(x) for x in re.search(r"(\d+) boys and (\d+) girls", q).groups())
    pats = count_seq({"B": boys, "G": girls}, blocks({"G"}), (None, frozenset()))
    return ("number", F(pats * factorial(boys) * factorial(girls)))
