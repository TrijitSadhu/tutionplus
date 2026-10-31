"""Ratio and Proportion Rules 26-33 (2026-10-30). Rules 26 / 27: incomes a : b, expenses c : d, each saves X - incomes
Xa(d-c)/(ad-bc), Xb(d-c)/(ad-bc) and expenses Xc(b-a)/(ad-bc), Xd(b-a)/(ad-bc). Rules 28-31: each of two numbers in the ratio a : b
is increased (28, 29) or decreased (30, 31) by x and the ratio becomes c : d - their sum (28, 30) or difference (29, 31). Rule 32:
quantities in inverse proportion - 1/a : 1/b : 1/c. Rule 33: sum A and difference a - the numbers are in the ratio A + a : A - a.
Writes the eight cards, regenerates the old rows 734-740 and adds the book's examples and exercises with no copy. The number sets
were searched against the book (scratch ratio_search3.py) and the sentences follow the searched templates. Usage: python gen_26_33.py"""
import os, sys
from fractions import Fraction as F
from math import gcd, lcm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from fmt import M, R, UU, low, nf  # noqa: E402
from gen_1_5 import main  # noqa: E402
from helpers import result  # noqa: E402

TH = {
    26: (r"If the incomes of two persons are in the ratio \(a : b\), their expenses in the ratio \(c : d\) and each saves Rs \(X\), their incomes are",
         r"\[ \frac{Xa(d-c)}{ad-bc}\quad\text{and}\quad\frac{Xb(d-c)}{ad-bc} \]"),
    27: (r"If the incomes of two persons are in the ratio \(a : b\), their expenses in the ratio \(c : d\) and each saves Rs \(X\), their expenses are",
         r"\[ \frac{Xc(b-a)}{ad-bc}\quad\text{and}\quad\frac{Xd(b-a)}{ad-bc} \]"),
    28: (r"If two numbers are in the ratio \(a : b\) and adding \(x\) to each makes it \(c : d\), the sum of the numbers is", r"\[ \frac{x(a+b)(c-d)}{ad-bc} \]"),
    29: (r"If two numbers are in the ratio \(a : b\) and adding \(x\) to each makes it \(c : d\), the difference of the numbers is", r"\[ \frac{x(a-b)(c-d)}{ad-bc} \]"),
    30: (r"If two numbers are in the ratio \(a : b\) and taking \(x\) from each makes it \(c : d\), the sum of the numbers is", r"\[ \frac{x(a+b)(d-c)}{ad-bc} \]"),
    31: (r"If two numbers are in the ratio \(a : b\) and taking \(x\) from each makes it \(c : d\), the difference of the numbers is", r"\[ \frac{x(a-b)(d-c)}{ad-bc} \]"),
    32: (r"If some quantities are in the ratio \(a : b : c\), the quantities that are inversely proportional to them are in the ratio", r"\[ \frac{1}{a} : \frac{1}{b} : \frac{1}{c} \]"),
    33: (r"If the sum of two numbers is \(A\) and their difference is \(a\), the numbers are in the ratio", r"\[ A+a : A-a \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rsteps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def done(r, ans, fin, trad, ident, sub):
    return result(ans, T(r), steps(*trad), rsteps(r, ident, sub), fin, [ident, "Answer " + fin + "."], sub)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def money_pair(p, q):
    return f"Rs {M(nf(p))} and Rs {M(nf(q))}"


# ---------- Rules 26 and 27
def r26(a, b, c, d, X, ask):
    den = a * d - b * c
    k = F(X * (d - c), den)                     # incomes ak, bk
    m = F(X * (b - a), den)                     # expenses cm, dm
    i1, i2, e1, e2 = a * k, b * k, c * m, d * m
    assert i1 - e1 == X and i2 - e2 == X
    trad = [("Set up the two savings.", rf"Incomes \({a}k\), \({b}k\); expenses \({c}m\), \({d}m\): \({a}k - {c}m = {X}\) and \({b}k - {d}m = {X}\)."),
            ("Solve.", rf"\(k = {nf(k)}\), \(m = {nf(m)}\): incomes Rs \({nf(i1)}\), Rs \({nf(i2)}\); expenses Rs \({nf(e1)}\), Rs \({nf(e2)}\).")]
    ident = rf"\(a : b = {a} : {b}\), \(c : d = {c} : {d}\), \(X = {X}\)."
    if ask == "inc":
        sub = rf"\[ \frac{{{X}\times {a}({d}-{c})}}{{{a}\times {d}-{b}\times {c}}} = {nf(i1)},\qquad \frac{{{X}\times {b}({d}-{c})}}{{{a}\times {d}-{b}\times {c}}} = {nf(i2)} \]"
        return done(26, ("pair", (i1, i2)), money_pair(i1, i2), trad, ident, sub)
    sub = rf"\[ \frac{{{X}\times {c}({b}-{a})}}{{{a}\times {d}-{b}\times {c}}} = {nf(e1)},\qquad \frac{{{X}\times {d}({b}-{a})}}{{{a}\times {d}-{b}\times {c}}} = {nf(e2)} \]"
    return done(27, ("pair", (e1, e2)), money_pair(e1, e2), trad, ident, sub)


# ---------- Rules 28-31
def r28_31(a, b, x, c, d, rule):
    """rule 28 / 29: x added; 30 / 31: x taken away. Returns the sum (28, 30) or the difference (29, 31)."""
    s = 1 if rule in (28, 29) else -1
    k = F(s * x * (c - d), a * d - b * c)
    p, q = a * k, b * k
    assert F(p + s * x, q + s * x) == F(c, d)
    v = p + q if rule in (28, 30) else abs(p - q)
    sg = "+" if s > 0 else "-"
    trad = [("Write the numbers as parts.", rf"Let them be \({a}k\) and \({b}k\): \(\frac{{{a}k {sg} {x}}}{{{b}k {sg} {x}}} = \frac{{{c}}}{{{d}}}\)."),
            ("Solve.", rf"\({d}({a}k {sg} {x}) = {c}({b}k {sg} {x})\) gives \(k = {nf(k)}\): the numbers are \({nf(p)}\) and \({nf(q)}\)."),
            ("What is asked.", (rf"Sum \(= {nf(p)} + {nf(q)} = {nf(v)}\)." if rule in (28, 30) else rf"Difference \(= {nf(max(p, q))} - {nf(min(p, q))} = {nf(v)}\)."))]
    top = {28: rf"{x}({a}+{b})({c}-{d})", 29: rf"{x}({a}-{b})({c}-{d})", 30: rf"{x}({a}+{b})({d}-{c})", 31: rf"{x}({a}-{b})({d}-{c})"}[rule]
    raw = F({28: x * (a + b) * (c - d), 29: x * (a - b) * (c - d), 30: x * (a + b) * (d - c), 31: x * (a - b) * (d - c)}[rule], a * d - b * c)
    sub = rf"\[ \frac{{{top}}}{{{a}\times {d}-{b}\times {c}}} = {nf(raw)} \]" + (rf"(the size of the difference is \({nf(v)}\))." if raw < 0 else "")
    return done(rule, ("number", v), M(nf(v)), trad, rf"\(a : b = {a} : {b}\), \(x = {x}\), \(c : d = {c} : {d}\).", sub)


# ---------- Rule 32
def terms_of(fracs):
    L = 1
    for f in fracs:
        L = lcm(L, f.denominator)
    ts = [int(f * L) for f in fracs]
    g = 0
    for t in ts:
        g = gcd(g, t)
    return [t // g for t in ts], L


def r32(parts, what):
    fr = [F(1, p) for p in parts]
    ts, L = terms_of(fr)
    trad = [("Inverse quantities.", rf"For the same {what[0]}, {what[1]} is inversely proportional to {what[2]}, so take " + " : ".join(rf"\(\frac{{1}}{{{p}}}\)" for p in parts) + "."),
            ("Clear the fractions.", rf"Multiply every term by \({L}\): \({' : '.join(map(str, ts))}\).")]
    sub = rf"\[ {' : '.join(chr(92) + 'frac{1}{' + str(p) + '}' for p in parts)} = {' : '.join(map(str, ts))} \]"
    return done(32, ("terms", tuple(ts)), M(" : ".join(map(str, ts))), trad, rf"Ratio \({' : '.join(map(str, parts))}\).", sub)


def r32_pens(fracs):
    ts, L = terms_of(fracs)
    v = sum(ts)
    trad = [("Clear the fractions.", rf"Multiply " + " : ".join(rf"\({frc(f)}\)" for f in fracs) + rf" by \({L}\): \({' : '.join(map(str, ts))}\)."),
            ("Least number.", rf"Each friend must get a whole number of pens, so the least total is \({' + '.join(map(str, ts))} = {v}\).")]
    sub = rf"\[ {' : '.join(frc(f) for f in fracs)} = {' : '.join(map(str, ts))} \]Least total \(= {v}\)."
    return done(32, ("number", F(v)), M(str(v)), trad, "Shares in the ratio " + " : ".join(rf"\({frc(f)}\)" for f in fracs) + ".", sub)


# ---------- Rule 33
def r33(A, a):
    big, small = F(A + a, 2), F(A - a, 2)
    x, y = low(A + a, A - a)
    trad = [("Find the numbers.", rf"Larger \(= \frac{{{A}+{a}}}{{2}} = {nf(big)}\), smaller \(= \frac{{{A}-{a}}}{{2}} = {nf(small)}\)."),
            ("Ratio.", rf"\[ {nf(big)} : {nf(small)} = {x} : {y} \]")]
    return done(33, ("ratio", (x, y)), R(x, y), trad, rf"\(A = {A}\), \(a = {a}\).", rf"\[ {A}+{a} : {A}-{a} = {A + a} : {A - a} = {x} : {y} \]")


INC = lambda a, b, c, d, X: f"The incomes of P and Q are in the ratio {a} : {b} and their spending is in the ratio {c} : {d}. If each saves Rs {X}, what are their incomes?"
INC2 = lambda a, b, c, d, X: f"The monthly incomes of two clerks are in the ratio {a} : {b} and their expenses are in the ratio {c} : {d}. Each of them saves Rs {X}. Find their incomes."
EXP = lambda a, b, c, d, X: f"The incomes of P and Q are in the ratio {a} : {b} and their spending is in the ratio {c} : {d}. If each saves Rs {X}, how much does each spend?"
EXP2 = lambda a, b, c, d, X: f"Two workers earn in the ratio {a} : {b} and spend in the ratio {c} : {d}. Each saves Rs {X} a month. Find what each of them spends."
ADD_SUM = lambda a, b, x, c, d: f"Two numbers are in the ratio {a} : {b}. If {x} is added to each of them, the ratio becomes {c} : {d}. What is the sum of the numbers?"
ADD_DIF = lambda a, b, x, c, d: f"Two numbers are in the ratio {a} : {b}. If {x} is added to each of them, the ratio becomes {c} : {d}. What is the difference of the numbers?"
SUB_SUM = lambda a, b, x, c, d: f"Two numbers are in the ratio {a} : {b}. If {x} is taken from each of them, the ratio becomes {c} : {d}. What is the sum of the numbers?"
SUB_DIF = lambda a, b, x, c, d: f"Two numbers are in the ratio {a} : {b}. If {x} is taken from each of them, the ratio becomes {c} : {d}. What is the difference of the numbers?"
SPD = lambda a, b, c: f"Three buses run at speeds in the ratio {a} : {b} : {c}. What is the ratio of the times they take to cover the same distance?"
GRP = lambda a, b, c: f"Three teams of workers are given the same job. The numbers of workers are in the ratio {a} : {b} : {c}. Find the ratio of the days they take."
SD = lambda A, a: f"The sum of two numbers is {A} and their difference is {a}. Find the ratio of the larger number to the smaller."
BUS = ("distance", "the time", "the speed")
TEAM = ("job", "the number of days", "the number of workers")

PICK = {"734": (11, 6, 7, 2, 1800), "r26_e1": (7, 8, 3, 7, 1500), "r26_e2": (13, 11, 4, 3, 3600), "r26_e3": (7, 4, 11, 5, 2400), "r26_e4": (9, 10, 6, 7, 3000),
        "r26_e5": (9, 8, 11, 8, 1200), "735": (12, 7, 9, 4, 1500), "r27_e1": (11, 9, 9, 7, 1500), "r27_e2": (8, 3, 10, 3, 4500), "r27_e3": (7, 9, 3, 5, 3000),
        "r27_e4": (7, 3, 11, 3, 1800), "r27_e5": (12, 11, 7, 6, 6000), "r28_ex": (23, 29, 7, 4, 5), "r28_e1": (11, 21, 15, 27, 47), "r28_e2": (14, 25, 12, 18, 29),
        "r28_e3": (21, 17, 11, 53, 45), "r28_e4": (27, 22, 18, 33, 28), "r28_e5": (10, 27, 15, 13, 30), "736": (18, 11, 22, 29, 22), "r29_e1": (23, 17, 19, 37, 29),
        "r29_e2": (23, 10, 8, 24, 11), "r29_e3": (13, 28, 20, 6, 11), "r29_e4": (19, 17, 8, 21, 19), "r29_e5": (28, 13, 16, 12, 7), "r29_e6": (18, 23, 20, 28, 33),
        "r29_e7": (20, 13, 13, 19, 13), "737": (26, 21, 11, 29, 23), "r30_e1": (23, 28, 15, 31, 41), "r30_e2": (11, 23, 13, 3, 11), "r30_e3": (15, 19, 7, 23, 31),
        "r30_e4": (23, 20, 4, 37, 32), "r30_e5": (19, 28, 22, 8, 17), "r30_e6": (9, 23, 6, 3, 10), "738": (17, 14, 5, 16, 13), "r31_e1": (17, 6, 24, 14, 3),
        "r31_e2": (29, 20, 23, 35, 17), "r31_e3": (9, 17, 18, 9, 25), "r31_e4": (23, 6, 5, 22, 5), "r31_e5": (7, 11, 21, 7, 17), "r31_e6": (17, 5, 9, 19, 4),
        "739": (3, 13, 14), "r32_e1": (2, 11, 12), "r32_e2": (3, 7, 14), "r32_e3": (3, 5, 15), "r32_ex2": (3, 10, 15), "r32_e5": (3, 7, 13), "r32_e6": (3, 10, 13),
        "r32_e7": (2, 3, 7), "740": (89, 15), "r33_e1": (54, 24), "r33_e2": (140, 30), "r33_e3": (54, 4), "r33_e4": (75, 23), "r33_e5": (97, 33), "r33_e6": (175, 5),
        "r33_e7": (128, 20)}


def item(key, rule):
    p = PICK[key]
    if rule == 26:
        t = INC2 if key in ("r26_e2", "r26_e4") else INC
        return t(*p), (lambda p=p: r26(*p, "inc")), "pair_rs"
    if rule == 27:
        t = EXP2 if key in ("r27_e2", "r27_e4") else EXP
        return t(*p), (lambda p=p: r26(*p, "exp")), "pair_rs"
    if rule in (28, 29, 30, 31):
        t = {28: ADD_SUM, 29: ADD_DIF, 30: SUB_SUM, 31: SUB_DIF}[rule]
        return t(*p), (lambda p=p, rule=rule: r28_31(*p, rule)), ""
    if rule == 32:
        team = key in ("r32_ex2", "r32_e5", "r32_e6", "r32_e7")
        return (GRP if team else SPD)(*p), (lambda p=p, team=team: r32(list(p), TEAM if team else BUS)), "terms"
    return SD(*p), (lambda p=p: r33(*p)), "ratio"


C = card
CARDS = {
    26: C(26, "Incomes From Savings", r"Write incomes as \(ak, bk\) and expenses as \(cm, dm\); each income minus its expense is the saving.",
          r"\[ \frac{Xa(d-c)}{ad-bc},\quad \frac{Xb(d-c)}{ad-bc} \]", [("Incomes", r"ak,\ bk"), ("Expenses", r"cm,\ dm"), ("Savings", r"ak-cm = bk-dm = X")],
          r"Two equations in \(k\) and \(m\); solving gives \(k = \frac{X(d-c)}{ad-bc}\).", "'The incomes of A and B are in the ratio a : b and their expenditures c : d; each saves Rs X; find their incomes.'",
          r"Incomes \(3 : 2\), expenses \(5 : 3\), saving Rs \(2000\): incomes Rs \(12000\), Rs \(8000\).", r"Subtracting the ratios term by term."),
    27: C(27, "Expenses From Savings", r"The same two equations, solved for the expenses.", r"\[ \frac{Xc(b-a)}{ad-bc},\quad \frac{Xd(b-a)}{ad-bc} \]",
          [("Incomes", r"ak,\ bk"), ("Expenses", r"cm,\ dm"), ("Solve for m", r"m = \frac{X(b-a)}{ad-bc}")],
          r"Check: income \(-\) expense must give the same saving for both.", "'... each saves Rs X; what are their expenditures?'",
          r"Incomes \(3 : 2\), expenses \(5 : 3\), saving Rs \(2000\): expenses Rs \(10000\), Rs \(6000\).", r"Giving the incomes when the expenses are asked."),
    28: C(28, "Sum After an Increase", r"Find \(k\) from the new ratio, then add the two numbers.", r"\[ \frac{x(a+b)(c-d)}{ad-bc} \]",
          [("Numbers", r"ak,\ bk"), ("Increase", r"ak+x : bk+x = c : d"), ("Sum", r"(a+b)k")], r"The same \(k\) as in Rule 24; the sum is \((a+b)k\).",
          "'The ratio of two numbers is a : b; if each is increased by x the ratio becomes c : d; find the sum.'", r"\(3 : 4\), add \(9\), becomes \(18 : 23\): sum \(105\).", r"Sign slips in \(ad-bc\)."),
    29: C(29, "Difference After an Increase", r"Find \(k\) from the new ratio; the difference is \((a-b)k\) in size.", r"\[ \frac{x(a-b)(c-d)}{ad-bc} \]",
          [("Numbers", r"ak,\ bk"), ("Increase", r"ak+x : bk+x = c : d"), ("Difference", r"|a-b|\,k")], r"Give the difference as a positive number.",
          "'... if each is increased by x the ratio becomes c : d; find the difference of the numbers.'", r"\(3 : 4\), add \(2\), becomes \(7 : 9\): difference \(4\).", r"Answering with a minus sign."),
    30: C(30, "Sum After a Decrease", r"Taking \(x\) from each number: solve for \(k\), then add.", r"\[ \frac{x(a+b)(d-c)}{ad-bc} \]",
          [("Numbers", r"ak,\ bk"), ("Decrease", r"ak-x : bk-x = c : d"), ("Sum", r"(a+b)k")], r"Rule 28 with \(-x\) in place of \(x\).",
          "'The ratio of two numbers is a : b; if each is decreased by x the ratio becomes c : d; find the sum.'", r"\(7 : 9\), take \(2\), becomes \(3 : 4\): sum \(32\).", r"Using \(c-d\) where \(d-c\) is needed."),
    31: C(31, "Difference After a Decrease", r"Taking \(x\) from each number: solve for \(k\); the difference is \(|a-b|k\).", r"\[ \frac{x(a-b)(d-c)}{ad-bc} \]",
          [("Numbers", r"ak,\ bk"), ("Decrease", r"ak-x : bk-x = c : d"), ("Difference", r"|a-b|\,k")], r"Subtracting the same number keeps the difference of the numbers.",
          "'... if each is decreased by x the ratio becomes c : d; find the difference of the numbers.'", r"\(7 : 9\), take \(2\), becomes \(3 : 4\): difference \(4\).", r"Answering with a minus sign."),
    32: C(32, "Inverse Proportion", r"When one quantity goes up as the other goes down (speed and time, workers and days), take the reciprocals.",
          r"\[ \frac{1}{a} : \frac{1}{b} : \frac{1}{c} \]", [("Speeds", r"a : b : c"), ("Times", r"\frac{1}{a} : \frac{1}{b} : \frac{1}{c}"), ("Whole numbers", r"\times\ \text{LCM}(a,b,c)")],
          r"Multiply the reciprocals by the LCM of the denominators to get whole numbers.", "'The speeds of three cars are a : b : c; ratio of the times for the same distance.'",
          r"Speeds \(2 : 3 : 4\): times \(6 : 4 : 3\).", r"Keeping the same order of sizes (the fastest takes the least time)."),
    33: C(33, "Ratio From Sum and Difference", r"Larger \(= \frac{A+a}{2}\), smaller \(= \frac{A-a}{2}\).", r"\[ A+a : A-a \]",
          [("Larger", r"\frac{A+a}{2}"), ("Smaller", r"\frac{A-a}{2}"), ("Ratio", r"A+a : A-a")], r"The halves cancel, so the ratio is simply \(A+a : A-a\) in lowest terms.",
          "'The sum of two numbers is A and their difference is a; what is the ratio of the numbers?'", r"Sum \(40\), difference \(4\): \(44 : 36 = 11 : 9\).", r"Writing \(A : a\)."),
}
RULE_OF = {"734": 26, "735": 27, "736": 29, "737": 30, "738": 31, "739": 32, "740": 33}
OLD = {}
for key, rule in RULE_OF.items():
    q, fn, kind = item(key, rule)
    OLD[int(key)] = (rule, q, fn, kind)
NEW = {r: [] for r in range(26, 34)}
for key in PICK:
    if key in RULE_OF:
        continue
    rule = int(key[1:3])
    q, fn, kind = item(key, rule)
    NEW[rule].append((key, q, fn, kind, None))
NEW[32].insert(4, ("r32_e4", r"A man shares his marbles among four friends in the ratio \(\frac{1}{2} : \frac{1}{3} : \frac{1}{5} : \frac{1}{6}\). "
                             "What is the least number of marbles he must have?", lambda: r32_pens([F(1, 2), F(1, 3), F(1, 5), F(1, 6)]), "", None))

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(26, 34))
