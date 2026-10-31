"""Number search used for Simple Interest Rules 34-39 (kept as the pattern for later batches - the other batches' search scripts were
scratch files and are gone; their results are the PICK dicts in gen_X_Y.py). For each sentence in sent_34_39.ITEMS it draws random
candidate number sets from that pool's generator (cNN: visible numbers first, then the hidden answer), keeps each visible set once and
takes the first set that passes originality.check_question(simple=True) against the book and the old question. Writes
picks_34_39.json next to this file: {key: [visible numbers..., hidden answer...]}; copy the picks into gen_X_Y.PICK.
Gate blind spot: a sentence with one or two numbers can repeat a book exercise exactly - leave the book's own values out by hand.
Usage: ../../../env/Scripts/python.exe -X utf8 number_search_34_39.py"""
import json, random, sys
from fractions import Fraction as F
from math import gcd, lcm
sys.path.insert(0, r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools")
sys.path.insert(0, r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\simple_interest")
from originality import Book, check_question
from sent_34_39 import ITEMS, NVIS

D = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\simple_interest"
book = Book(D + r"\pdf_text.txt")
OLD = {}
for n in range(34, 40):
    for r in json.load(open(D + rf"\rule{n:02d}\0_current_rows.json", encoding="utf-8"))["rows"]:
        OLD[r["id"]] = r["question"]
RNG = random.Random(3439)


def sample(make, n=3000):
    seen, tries = set(), 0
    while len(seen) < n and tries < 400000:
        tries += 1
        c = make(RNG)
        if c:
            seen.add(c)
    out = list(seen)
    RNG.shuffle(out)
    return out


HALF = [F(k, 2) for k in range(4, 31)]
FR = [F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(1, 6), F(1, 8), F(1, 10), F(2, 3), F(2, 5), F(3, 8), F(3, 10), F(2, 7), F(1, 7), F(3, 5)]


def c34(g, years=False):
    f1, f2 = g.sample(FR, 2)
    if f1 + f2 >= 1:
        return None
    r1, r2, r3 = g.sample(range(2, 16), 3)
    C = g.randrange(1200, 30001, 100)
    t = g.randint(2, 5) if years else 1
    A = C * (f1 * r1 + f2 * r2 + (1 - f1 - f2) * r3) / 100 * t
    if (f1 * C).denominator != 1 or (f2 * C).denominator != 1 or A.denominator != 1:
        return None
    return (f1, r1, f2, r2, r3, t, int(A), C) if years else (f1, r1, f2, r2, r3, int(A), C)


def c35(g):
    r = F(g.randint(4, 48), g.choice([1, 2, 3, 4]))
    if r > 15 or r < 1:
        return None
    P = g.randrange(300, 10001, 25)
    I = P * r * r / 100
    return (P, int(I), r) if I.denominator == 1 else None


def c36(g):
    r, t, P = g.randint(2, 15), g.choice(HALF[:17]), g.randrange(500, 20001, 50)
    I = F(P) * r * t / 100
    return (r, t, int(I), P + int(I)) if I.denominator == 1 else None


def c37(g):
    P1, P2, t1, t2, R = g.randrange(200, 5001, 50), g.randrange(200, 5001, 50), g.choice(HALF[:17]), g.choice(HALF[:17]), F(g.randint(4, 30), g.choice([1, 2, 3]))
    if P1 == P2 or t1 == t2 or R > 15:
        return None
    I = (P1 * t1 + P2 * t2) * R / 100
    return (P1, t1, P2, t2, int(I), R) if I.denominator == 1 else None


def c38(g):
    P1, r1, t, P2, R = g.randrange(1000, 10001, 100), g.randint(2, 15), g.choice(HALF[:13]), g.randrange(1000, 10001, 100), g.randint(2, 18)
    I1, I2 = F(P1) * r1 * t / 100, F(P2) * R * t / 100
    if R == r1 or P1 == P2 or I1.denominator != 1 or I2.denominator != 1:
        return None
    return (P1, r1, int(I1), int(I2), P2, R)


def c39t(g, n):
    T = g.randint(4, 80)
    r = F(100 * (n - 1), T)
    if (n, T) in ((2, 20), (3, 64)):                 # the book's own exercises
        return None
    return (r, T) if r <= 25 and (r * 8).denominator == 1 else None


def c39r(g, n):
    t = g.randint(4, 60)
    R = F(100 * (n - 1), t)
    if (n, t) in ((2, 20), (2, 8), (3, 25)):
        return None
    return (t, R) if R <= 25 and (R * 4).denominator == 1 else None


GEN = {"34": c34, "34t": lambda g: c34(g, True), "35": c35, "36": c36, "37": c37, "38": c38, "39t2": lambda g: c39t(g, 2), "39t3": lambda g: c39t(g, 3),
       "39r2": lambda g: c39r(g, 2), "39r3": lambda g: c39r(g, 3)}
pools, used, out = {}, set(), {}
for key, gen, tmpl, old_id in ITEMS:
    if gen not in pools:
        pools[gen] = sample(GEN[gen])
    n = NVIS[gen]
    for p in pools[gen]:
        vis = tuple(p[:n])
        if (gen[:2], vis) in used:
            continue
        q = tmpl(*vis)
        if not check_question(q, book, OLD.get(old_id), simple=True):
            used.add((gen[:2], vis))
            out[str(key)] = [str(x) for x in p]
            print(key, [str(x) for x in p], "|", q[:80], flush=True)
            break
    else:
        print(key, "NONE", flush=True)
json.dump(out, open(D + r"\picks_34_39.json", "w"), indent=1)
