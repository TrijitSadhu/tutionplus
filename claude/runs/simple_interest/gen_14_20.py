"""Simple Interest Rules 14-20 (2026-10-30). Rule 14: x% lower rate for t years gives Rs A less - P = 100A/(tx). Rule 15: Rs X in two
parts at r1% and r2% with yearly interest A - first part (100A - r2X)/(r1 - r2). Rules 16 / 17: Rs X amounts to A in t1 years; the rate
falls / rises by r% - the interest for t2 years is [(A-X)/t1 -/+ rX/100]t2. Rule 18: interest x in t years, then the principal n times
for t more years - total (n+1)x. Rule 19: the same with t2 more years - x[1 + (t2/t1)n]. Rule 20: parts with equal interests are in the
ratio 1/(r1t1) : 1/(r2t2) : .... Writes the seven cards, regenerates the old rows 776-782 (782's key was on the empty option e and no
option held the two parts) and adds the book's exercises with no copy (sentences in sent_14_20.py, number sets in PICK, searched
against the book). Usage: python gen_14_20.py"""
import os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
import gen_7_13  # noqa: E402,F401  (its build_opts wrapper - kind "pair_pr" - stays in place underneath this one)
from common import card  # noqa: E402
from fmt import M, nf, pair_opts  # noqa: E402
from gen_1_6 import done, num  # noqa: E402
from sent_14_20 import NVIS, SENT  # noqa: E402

TH = {
    14: (r"If a sum put at simple interest for \(t\) years would fetch Rs \(A\) less at a rate \(x\%\) lower, the sum is",
         r"\[ P = \frac{A\times 100}{t\times x} \]"),
    15: (r"If Rs \(X\) is divided into two parts, one put at \(r_1\%\) and the other at \(r_2\%\), and the yearly interest from both is Rs \(A\), the part at \(r_1\%\) is",
         r"\[ \frac{100A - r_2X}{r_1 - r_2} \]"),
    16: (r"If Rs \(X\) amounts to Rs \(A\) in \(t_1\) years at simple interest and the rate is lowered by \(r\%\), the interest for \(t_2\) years is",
         r"\[ \left[\frac{A-X}{t_1} - \frac{rX}{100}\right]t_2 \]"),
    17: (r"If Rs \(X\) amounts to Rs \(A\) in \(t_1\) years at simple interest and the rate is raised by \(r\%\), the interest for \(t_2\) years is",
         r"\[ \left[\frac{A-X}{t_1} + \frac{rX}{100}\right]t_2 \]"),
    18: (r"If the simple interest on a sum is Rs \(x\) after \(t\) years and the principal becomes \(n\) times for the next \(t\) years, the total interest "
         r"at the end of \(2t\) years is", r"\[ (n+1)x \]"),
    19: (r"If the simple interest on a sum is Rs \(x\) after \(t_1\) years and the principal becomes \(n\) times for the next \(t_2\) years, the total interest "
         r"at the end of \(t_1+t_2\) years is", r"\[ x\left[1 + \frac{t_2}{t_1}\,n\right] \]"),
    20: (r"If a sum is lent in parts so that the interest on the first at \(r_1\%\) for \(t_1\) years, on the second at \(r_2\%\) for \(t_2\) years, ... are all "
         r"equal, the parts are in the ratio", r"\[ \frac{1}{r_1t_1} : \frac{1}{r_2t_2} : \frac{1}{r_3t_3} : \dots \]"),
}
PICK = {
    776: (4, 2, 656, 8200), "r14_e1": (7, 5, 1785, 5100), "r14_e2": (4, 7, 364, 1300), "r14_e3": (8, 7, 1176, 2100), "r14_e4": (7, 5, 2625, 7500),
    "r14_e5": (4, 2, 488, 6100),
    777: (16000, 18, 16, 2851, 14550, 1450), "r15_e1": (21500, 10, 13, 6, 23430, 13500, 35000), "r15_e2": (6600, 3, 17, 828, 2100, 4500),
    "r15_e3": (7800, 14, 11, 1071, 7100, 700), "r15_e4": (24000, 14, 2, 3162, 22350, 1650), "r15_e5": (16600, 13, 9, 1538, 1100, 15500),
    "r15_e6": (24600, 11, 5, 4, 8184, 13600, 11000),
    778: (5700, 9120, 5, 11, 2, 5814, 12), "r16_e1": (5900, 10325, 5, 13, 7, 6726, 15), "r16_e2": (3800, 4598, 3, 4, 3, 4142, 7),
    "r16_e3": (3750, 4950, 4, 1, 2, 4275, 8), "r16_e4": (4200, 5292, 2, 9, 4, 4872, 13), "r16_e5": (1250, 1775, 3, 6, 3, 1550, 14),
    779: (3000, 3480, 2, 1, 2, 3540, 8), "r17_e1": (2950, 4366, 6, 1, 4, 4012, 8), "r17_e2": (2250, 4140, 6, 3, 8, 5310, 14),
    "r17_e3": (1250, 1575, 2, 2, 4, 2000, 13), "r17_e4": (5950, 10710, 8, 6, 7, 12614, 10), "r17_e5": (400, 560, 8, 6, 5, 620, 5),
    "r17_e6": (5150, 7725, 5, 2, 9, 10712, 10), "r17_e7": (5000, 6200, 6, 6, 5, 7500, 4),
    780: (905, 3, 8, 8145), "r18_e1": (615, 7, 5, 3690), "r18_e2": (490, 3, 8, 4410), "r18_e3": (1850, 3, 4, 9250), "r18_e4": (1755, 7, 3, 7020),
    781: (1950, 2, 9, 8, 72150), "r19_e1": (1860, 2, 4, 6, 24180), "r19_e2": (535, 2, 8, 8, 17655), "r19_e3": (1935, 3, 8, 4, 22575),
    "r19_e4": (660, 2, 12, 3, 12540), "r19_e5": (620, 5, 4, 6, 3596),
    782: (5280, 12, 7, 2, 2, 240, 5040), "r20_e1": (4715, 2, 9, 3, 2, 8, 2, 920, 2760, 1035), "r20_e2": (7370, 4, 6, 10, 2, 3350, 4020),
    "r20_e3": (2025, 12, 10, 7, 6, 525, 1500), "r20_e4": (9680, 8, 2, 3, 2, 2640, 7040), "r20_e5": (2030, 8, 6, 8, 8, 1160, 870),
}


def n_(r, v, trad, ident, sub, unit=""):
    return num(r, v, trad, ident, sub, unit, TH)


def money_pair(r, a, b, trad, ident, sub):
    return done(r, ("pair", (F(a), F(b))), f"Rs {M(nf(a))} and Rs {M(nf(b))}", trad, ident, sub, TH)


# ---------- Rule 14
def r14(t, x, A, want):
    t, x, A = map(F, (t, x, A))
    v = 100 * A / (t * x)
    assert v == want
    trad = [("Interest lost on Rs 100.", rf"\({nf(x)}\%\) less for \({nf(t)}\) years costs Rs \(100\) an interest of \({nf(x)}\times {nf(t)} = {nf(x * t)}\)."),
            ("Scale up.", rf"The loss is Rs \({nf(A)}\): \[ 100\times\frac{{{nf(A)}}}{{{nf(x * t)}}} = {nf(v)} \]")]
    return n_(14, v, trad, rf"\(t = {nf(t)}\), \(x = {nf(x)}\), \(A = {nf(A)}\).", rf"\[ P = \frac{{{nf(A)}\times 100}}{{{nf(t)}\times {nf(x)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 15
def r15_core(X, r1, r2, I, t=1):
    """Traditional steps and the rule step for the part at r1 (yearly interest I / t)."""
    X, r1, r2, I, t = map(F, (X, r1, r2, I, t))
    A = I / t
    p1 = (100 * A - r2 * X) / (r1 - r2)
    first = "" if t == 1 else rf"In one year the interest is \({nf(I)} \div {nf(t)} = {nf(A)}\). "
    trad = [("Let the part at the first rate be y.", first + rf"\(\frac{{{nf(r1)}}}{{100}}y + \frac{{{nf(r2)}}}{{100}}({nf(X)} - y) = {nf(A)}\)."),
            ("Solve.", rf"\[ {nf(r1)}y + {nf(r2 * X)} - {nf(r2)}y = {nf(100 * A)} \Rightarrow {nf(r1 - r2)}y = {nf(100 * A - r2 * X)} \Rightarrow y = {nf(p1)} \]"
                       rf"The other part is \({nf(X)} - {nf(p1)} = {nf(X - p1)}\).")]
    ident = rf"\(X = {nf(X)}\), \(r_1 = {nf(r1)}\), \(r_2 = {nf(r2)}\), \(A = {nf(A)}\)."
    sub = rf"\[ \frac{{100\times {nf(A)} - {nf(r2)}\times {nf(X)}}}{{{nf(r1)} - {nf(r2)}}} = \frac{{{nf(100 * A - r2 * X)}}}{{{nf(r1 - r2)}}} = {nf(p1)} \]" \
          rf"The other part \(= {nf(X)} - {nf(p1)} = {nf(X - p1)}\)."
    return p1, X - p1, trad, ident, sub


def r15_pair(X, r1, r2, I, p1, p2, t=1):
    a, b, trad, ident, sub = r15_core(X, r1, r2, I, t)
    assert (a, b) == (p1, p2)
    return money_pair(15, a, b, trad, ident, sub)


def r15_one(X, r1, r2, I, p1, p2, ask):
    a, b, trad, ident, sub = r15_core(X, r1, r2, I)
    assert (a, b) == (p1, p2)
    return n_(15, a if ask == 1 else b, trad, ident, sub, "Rs")


def r15_more(X1, r1, r2, t, I, X2, total):
    X1, r1, r2, t, I = map(F, (X1, r1, r2, t, I))
    A = I / t
    I1 = X1 * r1 * t / 100
    x2 = (I - I1) * 100 / (r2 * t)
    assert x2 == X2 and X1 + x2 == total
    trad = [("Interest on the first loan.", rf"\(\frac{{{nf(r1)}}}{{100}}\times {nf(X1)}\times {nf(t)} = {nf(I1)}\); the second loan paid \({nf(I)} - {nf(I1)} = {nf(I - I1)}\)."),
            ("Second loan and the total.", rf"\[ \frac{{{nf(I - I1)}\times 100}}{{{nf(r2)}\times {nf(t)}}} = {nf(x2)};\quad {nf(X1)} + {nf(x2)} = {nf(X1 + x2)} \]")]
    ident = rf"Part at \(r_1 = {nf(r1)}\%\) is \({nf(X1)}\), \(r_2 = {nf(r2)}\), yearly interest \(A = {nf(I)} \div {nf(t)} = {nf(A)}\), whole sum \(X = {nf(X1)} + x\)."
    sub = rf"\[ \frac{{100\times {nf(A)} - {nf(r2)}({nf(X1)} + x)}}{{{nf(r1)} - {nf(r2)}}} = {nf(X1)} \Rightarrow {nf(r2)}x = {nf(100 * A - r2 * X1 - (r1 - r2) * X1)} \Rightarrow x = {nf(x2)} \]" \
          rf"Total \(= {nf(X1)} + {nf(x2)} = {nf(X1 + x2)}\)."
    return n_(15, X1 + x2, trad, ident, sub, "Rs")


# ---------- Rules 16 and 17
def r16_17(rule, X, A, t1, r, t2, want, R0):
    X, A, t1, r, t2 = map(F, (X, A, t1, r, t2))
    s = -1 if rule == 16 else 1
    old = 100 * (A - X) / (X * t1)
    new = old + s * r
    I2 = X * new * t2 / 100
    assert old == R0 and X + I2 == want
    word, op = ("lower", "-") if rule == 16 else ("higher", "+")
    trad = [("Old rate.", rf"Interest \(= {nf(A)} - {nf(X)} = {nf(A - X)}\) in \({nf(t1)}\) years: \(\frac{{{nf(A - X)}\times 100}}{{{nf(X)}\times {nf(t1)}}} = {nf(old)}\%\)."),
            ("New interest and amount.", rf"New rate \(= {nf(old)} {op} {nf(r)} = {nf(new)}\%\): \[ \frac{{{nf(X)}\times {nf(new)}\times {nf(t2)}}}{{100}} = {nf(I2)};\quad {nf(X)} + {nf(I2)} = {nf(X + I2)} \]")]
    ident = rf"\(X = {nf(X)}\), \(A = {nf(A)}\), \(t_1 = {nf(t1)}\), \(r = {nf(r)}\) ({word}), \(t_2 = {nf(t2)}\)."
    sub = rf"\[ \left[\frac{{{nf(A)} - {nf(X)}}}{{{nf(t1)}}} {op} \frac{{{nf(r)}\times {nf(X)}}}{{100}}\right]\times {nf(t2)} = \left[{nf((A - X) / t1)} {op} {nf(r * X / 100)}\right]\times {nf(t2)} = {nf(I2)} \]" \
          rf"Amount \(= {nf(X)} + {nf(I2)} = {nf(X + I2)}\)."
    return n_(rule, X + I2, trad, ident, sub, "Rs")


# ---------- Rules 18 and 19
def r18(x, t, n, want):
    x, t, n = map(F, (x, t, n))
    v = (n + 1) * x
    assert v == want
    trad = [("Interest of the second period.", rf"The first \({nf(t)}\) years give Rs \({nf(x)}\). With \({nf(n)}\) times the principal, the next \({nf(t)}\) years give "
                                               rf"\({nf(n)}\times {nf(x)} = {nf(n * x)}\)."),
            ("Total.", rf"\[ {nf(x)} + {nf(n * x)} = {nf(v)} \]")]
    return n_(18, v, trad, rf"\(x = {nf(x)}\), \(n = {nf(n)}\).", rf"\[ ({nf(n)} + 1)\times {nf(x)} = {nf(v)} \]", "Rs")


def r19(x, t1, t2, n, want):
    x, t1, t2, n = map(F, (x, t1, t2, n))
    v = x * (1 + t2 * n / t1)
    assert v == want
    trad = [("Interest a year.", rf"On the first principal: \({nf(x)} \div {nf(t1)} = {nf(x / t1)}\) a year; on \({nf(n)}\) times the principal: "
                                 rf"\({nf(n)}\times {nf(x / t1)} = {nf(n * x / t1)}\) a year."),
            ("Total.", rf"\[ {nf(x)} + {nf(n * x / t1)}\times {nf(t2)} = {nf(x)} + {nf(n * x * t2 / t1)} = {nf(v)} \]")]
    return n_(19, v, trad, rf"\(x = {nf(x)}\), \(t_1 = {nf(t1)}\), \(t_2 = {nf(t2)}\), \(n = {nf(n)}\).",
              rf"\[ {nf(x)}\left[1 + \frac{{{nf(t2)}}}{{{nf(t1)}}}\times {nf(n)}\right] = {nf(v)} \]", "Rs")


# ---------- Rule 20
def r20_core(X, rts):
    X = F(X)
    prods = [F(r) * t for r, t in rts]
    w = [1 / p for p in prods]
    parts = [X * x / sum(w) for x in w]
    lcm_ = 1
    for p in prods:
        lcm_ = lcm_ * int(p) // gcd(lcm_, int(p))
    ints = [int(lcm_ / p) for p in prods]
    h = 0
    for v in ints:
        h = gcd(h, v)
    ints = [v // h for v in ints]
    names = ["first", "second", "third"]
    eq = " = ".join(rf"\frac{{P_{i + 1}\times {nf(r)}\times {nf(t)}}}{{100}}" for i, (r, t) in enumerate(rts))
    trad = [("Equal interests.", rf"\[ {eq} \]So each part times its \(r\times t\) is the same: \({' = '.join(rf'{nf(p)}P_{i + 1}' for i, p in enumerate(prods))}\)."),
            ("Share the sum.", r"The parts are in the ratio " + M(" : ".join(str(v) for v in ints)) + rf" (\({' + '.join(str(v) for v in ints)} = {sum(ints)}\) shares): "
                               + ", ".join(rf"{names[i]} \(= \frac{{{v}}}{{{sum(ints)}}}\times {nf(X)} = {nf(parts[i])}\)" for i, v in enumerate(ints)) + ".")]
    ident = r"\(" + r",\ ".join(rf"r_{i + 1}t_{i + 1} = {nf(r)}\times {nf(t)} = {nf(p)}" for i, ((r, t), p) in enumerate(zip(rts, prods))) + rf"\), \(X = {nf(X)}\)."
    sub = r"\[ " + " : ".join(rf"\frac{{1}}{{{nf(p)}}}" for p in prods) + " = " + " : ".join(str(v) for v in ints) + r" \]" + \
          ", ".join(rf"\(\frac{{{v}}}{{{sum(ints)}}}\times {nf(X)} = {nf(parts[i])}\)" for i, v in enumerate(ints)) + "."
    return parts, trad, ident, sub


def r20_pair(X, r1, t1, r2, t2, p1, p2):
    parts, trad, ident, sub = r20_core(X, [(r1, t1), (r2, t2)])
    assert parts == [p1, p2]
    return money_pair(20, parts[0], parts[1], trad, ident, sub)


def r20_diff(X, r1, t1, r2, t2, p1, p2, *rest):
    rts = [(r1, t1), (r2, t2)] if not rest else [(r1, t1), (r2, t2), (p1, p2)]
    parts, trad, ident, sub = r20_core(X, rts)
    assert parts == ([p1, p2] if not rest else list(rest))
    d = max(parts) - min(parts)
    big, small = nf(max(parts)), nf(min(parts))
    trad = trad + [("Difference.", rf"\[ {big} - {small} = {nf(d)} \]")]
    return n_(20, d, trad, ident, sub + rf" Difference \(= {big} - {small} = {nf(d)}\).", "Rs")


_below = gen_1_6.build_opts


def build_opts(g, kind, wrong):
    if kind == "pair_money":
        return pair_opts(*g["answer"][1], "Rs", wrong)
    return _below(g, kind, wrong)


gen_1_6.build_opts = build_opts

C = card
CARDS = {
    14: C(14, "Lower Rate, Less Interest", r"Only the drop in the rate makes the drop in the interest.", r"\[ P = \frac{A\times 100}{t\times x} \]",
          [("Drop in rate", r"x\%"), ("Time", r"t\ \text{years}"), ("Less interest", r"A = \frac{P\times x\times t}{100}")],
          r"The interest at the lower rate is part of both interests and cancels out.", "'Had the sum been put at x% lower rate for t years, it would have fetched Rs A less; find the sum.'",
          r"\(3\) years, \(2\%\) lower, Rs \(90\) less: \(\frac{9000}{6} = 1500\).", r"Dividing by the lower rate instead of the drop in rate."),
    15: C(15, "One Sum, Two Rates", r"The yearly interest of the two parts adds up to the given interest.", r"\[ \text{part at } r_1 = \frac{100A - r_2X}{r_1 - r_2} \]",
          [("Part 1", r"y\ \text{at}\ r_1\%"), ("Part 2", r"X - y\ \text{at}\ r_2\%"), ("Yearly interest", r"\frac{r_1y + r_2(X-y)}{100} = A")],
          r"If all of it were at \(r_2\%\) the interest would be \(\frac{r_2X}{100}\); every rupee moved to \(r_1\%\) changes it by \(\frac{r_1 - r_2}{100}\).",
          "'Rs X is divided into two parts, one at r1% and the other at r2%; the yearly interest is Rs A. Find each part.'",
          r"Rs \(5000\) at \(4\%\) and \(6\%\), Rs \(260\) a year: \(\frac{26000 - 30000}{4 - 6} = 2000\) and \(3000\).",
          r"Using the interest of several years as \(A\) - divide it by the years first."),
    16: C(16, "Rate Lowered", r"Find the old yearly interest, then take off the interest lost by the lower rate.", r"\[ \left[\frac{A-X}{t_1} - \frac{rX}{100}\right]t_2 \]",
          [("Old yearly interest", r"\frac{A - X}{t_1}"), ("Lost each year", r"\frac{rX}{100}"), ("New amount", r"X + \left[\frac{A-X}{t_1} - \frac{rX}{100}\right]t_2")],
          r"Lowering the rate by \(r\%\) takes \(\frac{rX}{100}\) off every year's interest.", "'Rs X amounted to Rs A in t1 years; if the rate is decreased by r%, what will the amount be after t2 years?'",
          r"Rs \(1000\) to Rs \(1300\) in \(5\) years, \(2\%\) lower, \(3\) years: \((60 - 20)\times 3 = 120\), amount Rs \(1120\).",
          r"Taking \(r\%\) off the interest instead of off the rate."),
    17: C(17, "Rate Raised", r"Find the old yearly interest, then add the interest gained by the higher rate.", r"\[ \left[\frac{A-X}{t_1} + \frac{rX}{100}\right]t_2 \]",
          [("Old yearly interest", r"\frac{A - X}{t_1}"), ("Gained each year", r"\frac{rX}{100}"), ("New amount", r"X + \left[\frac{A-X}{t_1} + \frac{rX}{100}\right]t_2")],
          r"Raising the rate by \(r\%\) adds \(\frac{rX}{100}\) to every year's interest.", "'Rs X amounted to Rs A in t1 years; if the rate is increased by r%, what will the amount be after t2 years?'",
          r"Rs \(1000\) to Rs \(1300\) in \(5\) years, \(2\%\) higher, \(3\) years: \((60 + 20)\times 3 = 240\), amount Rs \(1240\).",
          r"Giving the interest when the amount is asked."),
    18: C(18, "Principal Grows, Same Time Again", r"With \(n\) times the principal for the same number of years, the interest is \(n\) times as much.", r"\[ (n+1)x \]",
          [("First t years", r"x"), ("Next t years", r"nx"), ("Total", r"(n+1)x")],
          r"Interest is in proportion to the principal when the rate and the time are the same.", "'The SI is Rs x after t years; in the next t years the principal becomes n times. Find the total interest after 2t years.'",
          r"Rs \(200\) in \(4\) years, then \(3\) times the principal for \(4\) years: \(4\times 200 = 800\).", r"Giving \(nx\) - the first period's interest is left out."),
    19: C(19, "Principal Grows, Different Time", r"Work out one year's interest, multiply by \(n\) for the bigger principal and by the new number of years.",
          r"\[ x\left[1 + \frac{t_2}{t_1}\,n\right] \]",
          [("First t1 years", r"x"), ("Yearly, new principal", r"\frac{nx}{t_1}"), ("Next t2 years", r"\frac{nx\,t_2}{t_1}")],
          r"Rule 18 is the case \(t_1 = t_2\).", "'The SI is Rs x after t1 years; in the next t2 years the principal becomes n times. Find the total interest.'",
          r"Rs \(240\) in \(3\) years, then \(2\) times for \(5\) years: \(240\left[1 + \frac{10}{3}\right] = 1040\).", r"Using \(t_1\) for the second period too."),
    20: C(20, "Parts With Equal Interest", r"Equal interest means each part times its rate times its years is the same.", r"\[ \frac{1}{r_1t_1} : \frac{1}{r_2t_2} : \frac{1}{r_3t_3} : \dots \]",
          [("Part 1", r"P_1 r_1 t_1"), ("Part 2", r"P_2 r_2 t_2"), ("Equal", r"P_1r_1t_1 = P_2r_2t_2 = \dots")],
          r"A part that earns faster (bigger \(r\times t\)) must be smaller.", "'A sum is lent in parts so that the interest on each part (at its rate, for its years) is the same; find the parts.'",
          r"Rs \(1700\), \(5\%\) for \(4\) years and \(6\%\) for \(5\) years: \(\frac{1}{20} : \frac{1}{30} = 3 : 2\), Rs \(1020\) and Rs \(680\).",
          r"Making the parts proportional to \(r\times t\) instead of \(\frac{1}{r\times t}\)."),
}


def q(k):
    return SENT[k][1](*PICK[k][:NVIS[SENT[k][0]]])


def fn_for(k):
    pool, p = SENT[k][0], PICK[k]
    return {"14": lambda: r14(*p), "15": lambda: r15_pair(*p), "15b1": lambda: r15_one(*p, 1), "15m1": lambda: r15_one(*p, 1),
            "15b2": lambda: r15_one(*p, 2), "15m2": lambda: r15_one(*p, 2), "15u": lambda: r15_more(*p),
            "15t": lambda: r15_pair(p[0], p[1], p[2], p[4], p[5], p[6], p[3]), "16": lambda: r16_17(16, *p), "17": lambda: r16_17(17, *p),
            "18": lambda: r18(*p), "19": lambda: r19(*p), "20": lambda: r20_pair(*p), "20d": lambda: r20_diff(*p),
            "20t": lambda: r20_diff(p[0], p[1], p[2], p[3], p[4], p[5], p[6], *p[7:])}[pool]


def kind_for(k):
    return "pair_money" if SENT[k][0] in ("15", "15t", "20") else "Rs"


OLD_RULE = {776: 14, 777: 15, 778: 16, 779: 17, 780: 18, 781: 19, 782: 20}
OLD = {rid: (rule, q(rid), fn_for(rid), kind_for(rid)) for rid, rule in OLD_RULE.items()}
NEW = {}
for k in SENT:
    if isinstance(k, str):
        rule = int(k[1:k.index("_")])
        NEW.setdefault(rule, []).append((k, q(k), fn_for(k), kind_for(k), None))

if __name__ == "__main__":
    gen_1_6.main(OLD, NEW, CARDS, range(14, 21))
