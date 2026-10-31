"""Simple Interest Rules 28-33 (2026-10-31). Rule 28: the interest on Rs P1 is Rs A less than on Rs P2 at r% - time = 100A/(r(P2-P1)).
Rule 29: two equal sums at r1% for t1 years and r2% for t2 years differ in interest by Rs Id - sum = 100Id/(r1t1 - r2t2). Rule 30: two
banks' interests on Rs X for t years differ by Rs Id - the rates differ by 100Id/(Xt) %. Rule 31: amounts A1 in t1 years and A2 in t2
years - rate = 100(A2 - A1)/(A1t2 - A2t1) %. Rule 32: Rs X borrowed, Rs x1 repaid after t1 years, Rs x2 settles it at the end of t2
years - rate = (x1 + x2 - X)/(x1t1 + t2(X - x1)) x 100 %. Rule 33: part of Rs P at r1%, the rest at r2%, total interest Rs A in t years -
part at r1% = (100A - Pr2t)/((r1 - r2)t). Writes the six cards, regenerates the old rows 790-795 (keys all right) and adds the book's
exercises with no copy (sentences in sent_28_33.py, number sets in PICK, searched against the book). Usage: python gen_28_33.py"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
from common import card  # noqa: E402
from fmt import nf  # noqa: E402
from gen_1_6 import num  # noqa: E402
from sent_28_33 import NVIS, SENT  # noqa: E402

TH = {
    28: (r"If the simple interest on Rs \(P_1\) is Rs \(A\) less than the interest on Rs \(P_2\) at \(r\%\) for the same time, the time is",
         r"\[ t = \frac{A\times 100}{r(P_2-P_1)}\ \text{years} \]"),
    29: (r"If two equal sums are put at \(r_1\%\) for \(t_1\) years and at \(r_2\%\) for \(t_2\) years and their interests differ by Rs \(I_d\), each sum is",
         r"\[ \frac{I_d\times 100}{r_1t_1-r_2t_2} \]"),
    30: (r"If the interests from two banks on Rs \(X\) for \(t\) years differ by Rs \(I_d\), their rates differ by", r"\[ \frac{I_d\times 100}{X\times t}\ \% \]"),
    31: (r"If a sum amounts to Rs \(A_1\) in \(t_1\) years and to Rs \(A_2\) in \(t_2\) years at simple interest, the rate per annum is",
         r"\[ \frac{100(A_2-A_1)}{A_1t_2-A_2t_1}\ \% \]"),
    32: (r"If Rs \(X\) is borrowed at simple interest, Rs \(x_1\) is paid back after \(t_1\) years and Rs \(x_2\) at the end of \(t_2\) years settles the "
         r"account, the rate is", r"\[ \frac{x_1+x_2-X}{x_1t_1+t_2(X-x_1)}\times 100\ \% \]"),
    33: (r"If part of Rs \(P\) is lent at \(r_1\%\) and the rest at \(r_2\%\), and the total simple interest in \(t\) years is Rs \(A\), the part lent at \(r_1\%\) is",
         r"\[ \frac{100A-Pr_2t}{(r_1-r_2)t} \]"),
}
PICK = {
    790: (4525, 4875, 14, 196, 4), "r28_e1": (3275, 3825, 4, 77, F(7, 2)), "r28_e2": (2525, 4975, 15, 3675, 10), "r28_e3": (9975, 12225, 4, 945, F(21, 2)),
    "r28_e4": (8875, 11675, 5, 350, F(5, 2)), "r28_e5": (1700, 3350, 4, 429, F(13, 2)),
    791: (9, 10, 10, 3, 7260, 12100), "r29_e1": (6, 10, 14, 2, 4224, 13200), "r29_e2": (30, 6, 3, 2, 1044, 7200), "r29_e3": (5, 7, 9, 2898, 16100),
    "r29_e4": (12, 6, 7, 7, 230, 1000), "r29_e5": (6, 8, 9, 2, 4050, 13500), "r29_e6": (7, 10, 5, 2880, 19200),
    792: (7200, 8, 432, F(3, 4)), "r30_e1": (2500, 2, 150, 3), "r30_e2": (1900, 3, 114, 2), "r30_e3": (950, 2, 95, 5), "r30_e4": (4250, 6, 1020, 4),
    "r30_e5": (2400, 4, 24, F(1, 4)),
    793: (7840, 3, 9760, 7, F(15, 2), 6400), "r31_e1": (3245, 2, 3740, 4, 9, 2750), "r31_e2": (4485, 3, 5070, 3, 5, 3900),
    "r31_e3": (6084, 2, 10062, 11, F(17, 2), 5200), "r31_e4": (1736, 8, 1862, 11, 3, 1400), "r31_e5": (7920, 4, 8745, F(13, 2), 5, 6600),
    "r31_e6": (3876, 4, 4590, 10, F(7, 2), 3400), "r31_e7": (4928, F(7, 2), 7546, 12, 8, 3850),
    794: (2800, 3, 2200, 6, 1263, F(13, 2)), "r32_e1": (2400, 3, 1100, 8, 1985, 5), "r32_e2": (11000, 3, 9500, 8, 3120, 4),
    "r32_e3": (5200, 2, 1200, 6, 6772, F(21, 2)), "r32_e4": (11700, 4, 2100, 8, 13860, 5),
    795: (18300, 12, 3, 8, 14724, 14350), "r33_e1": (1000, 14, 4, 6, 570, 550), "r33_e2": (16500, 6, 3, 4, 3924, 16200), "r33_e3": (13700, 13, 9, 6, 8310, 3800),
}


def n_(r, v, trad, ident, sub, unit=""):
    return num(r, v, trad, ident, sub, unit, TH)


# ---------- Rule 28
def r28(P1, P2, r, A, want):
    P1, P2, r, A = map(F, (P1, P2, r, A))
    d = P2 - P1
    one = d * r / 100
    v = A / one
    assert v == want
    trad = [("Where the extra interest comes from.", rf"Only the extra Rs \({nf(P2)} - {nf(P1)} = {nf(d)}\) makes the difference; it earns "
                                                     rf"\(\frac{{{nf(r)}}}{{100}}\times {nf(d)} = {nf(one)}\) a year."),
            ("Years.", rf"\[ {nf(A)} \div {nf(one)} = {nf(v)} \]")]
    return n_(28, v, trad, rf"\(P_1 = {nf(P1)}\), \(P_2 = {nf(P2)}\), \(r = {nf(r)}\), \(A = {nf(A)}\).",
              rf"\[ t = \frac{{{nf(A)}\times 100}}{{{nf(r)}({nf(P2)} - {nf(P1)})}} = \frac{{{nf(100 * A)}}}{{{nf(r * d)}}} = {nf(v)} \]", "years")


# ---------- Rule 29
def r29_core(r1, t1, r2, t2, D, want, note=""):
    r1, t1, r2, t2, D = map(F, (r1, t1, r2, t2, D))
    gap = r1 * t1 - r2 * t2
    v = 100 * D / gap
    assert v == want
    trad = [("Difference on Rs 100.", note + rf"Rs \(100\) earns \({nf(r1)}\times {nf(t1)} = {nf(r1 * t1)}\) in the first case and \({nf(r2)}\times {nf(t2)} = {nf(r2 * t2)}\) "
                                      rf"in the second: a difference of \({nf(gap)}\)."),
            ("Scale up.", rf"The difference is Rs \({nf(D)}\): \[ 100\times\frac{{{nf(D)}}}{{{nf(gap)}}} = {nf(v)} \]")]
    return n_(29, v, trad, rf"\(r_1t_1 = {nf(r1)}\times {nf(t1)}\), \(r_2t_2 = {nf(r2)}\times {nf(t2)}\), \(I_d = {nf(D)}\).",
              rf"\[ \frac{{{nf(D)}\times 100}}{{{nf(r1)}\times {nf(t1)} - {nf(r2)}\times {nf(t2)}}} = \frac{{{nf(100 * D)}}}{{{nf(gap)}}} = {nf(v)} \]", "Rs")


def r29(r1, t1, r2, t2, D, P):
    return r29_core(r1, t1, r2, t2, D, P)


def r29m(m1, r1, m2, r2, D, P):
    t1, t2 = F(m1, 12), F(m2, 12)
    return r29_core(r1, t1, r2, t2, D, P, rf"\({nf(m1)}\) months \(= {nf(t1)}\) years and \({nf(m2)}\) months \(= {nf(t2)}\) years. ")


def r29s(t1, t2, r, D, P):
    return r29_core(r, t2, r, t1, D, P)


# ---------- Rule 30
def r30(X, t, D, want):
    X, t, D = map(F, (X, t, D))
    v = 100 * D / (X * t)
    assert v == want
    trad = [("Difference a year.", rf"The interests differ by \({nf(D)}\) in \({nf(t)}\) years: \({nf(D / t)}\) a year."),
            ("As a per cent of the sum.", rf"\[ \frac{{{nf(D / t)}}}{{{nf(X)}}}\times 100 = {nf(v)}\% \]")]
    return n_(30, v, trad, rf"\(X = {nf(X)}\), \(t = {nf(t)}\), \(I_d = {nf(D)}\).", rf"\[ \frac{{{nf(D)}\times 100}}{{{nf(X)}\times {nf(t)}}} = {nf(v)}\% \]", "%")


# ---------- Rule 31
def r31(A1, t1, A2, t2, want, P, more=False):
    A1, t1, A2 = map(F, (A1, t1, A2))
    t2 = t1 + F(t2) if more else F(t2)
    one = (A2 - A1) / (t2 - t1)
    p = A1 - one * t1
    v = 100 * one / p
    w = 100 * (A2 - A1) / (A1 * t2 - A2 * t1)
    assert v == w == want and p == P
    first = rf"The second time is \({nf(t1)} + {nf(t2 - t1)} = {nf(t2)}\) years. " if more else ""
    trad = [("Interest of one year.", first + rf"In \({nf(t2 - t1)}\) years the amount grows by \({nf(A2)} - {nf(A1)} = {nf(A2 - A1)}\): \({nf(one)}\) a year."),
            ("Sum and rate.", rf"Sum \(= {nf(A1)} - {nf(one)}\times {nf(t1)} = {nf(p)}\); \[ \frac{{{nf(one)}}}{{{nf(p)}}}\times 100 = {nf(v)}\% \]")]
    return n_(31, v, trad, rf"\(A_1 = {nf(A1)}\), \(t_1 = {nf(t1)}\), \(A_2 = {nf(A2)}\), \(t_2 = {nf(t2)}\).",
              rf"\[ \frac{{100({nf(A2)} - {nf(A1)})}}{{{nf(A1)}\times {nf(t2)} - {nf(A2)}\times {nf(t1)}}} = \frac{{{nf(100 * (A2 - A1))}}}{{{nf(A1 * t2 - A2 * t1)}}} = {nf(v)}\% \]", "%")


# ---------- Rule 32
def r32(X, t1, x1, t2, x2, want):
    X, t1, x1, t2, x2 = map(F, (X, t1, x1, t2, x2))
    I = x1 + x2 - X
    base = X * t1 + (X - x1) * (t2 - t1)
    v = 100 * I / base
    assert v == want and base == x1 * t1 + t2 * (X - x1)
    trad = [("Total interest.", rf"He paid \({nf(x1)} + {nf(x2)} = {nf(x1 + x2)}\) for a loan of \({nf(X)}\): interest \(= {nf(I)}\). The first payment comes off the "
                                rf"principal, so Rs \({nf(X)}\) runs for \({nf(t1)}\) years and Rs \({nf(X - x1)}\) for \({nf(t2 - t1)}\) more years."),
            ("Rate.", rf"\[ \frac{{{nf(X)}\times r\times {nf(t1)}}}{{100}} + \frac{{{nf(X - x1)}\times r\times {nf(t2 - t1)}}}{{100}} = {nf(I)} \Rightarrow {nf(base)}r = {nf(100 * I)} "
                      rf"\Rightarrow r = {nf(v)} \]")]
    return n_(32, v, trad, rf"\(X = {nf(X)}\), \(x_1 = {nf(x1)}\), \(t_1 = {nf(t1)}\), \(x_2 = {nf(x2)}\), \(t_2 = {nf(t2)}\).",
              rf"\[ \frac{{{nf(x1)} + {nf(x2)} - {nf(X)}}}{{{nf(x1)}\times {nf(t1)} + {nf(t2)}({nf(X)} - {nf(x1)})}}\times 100 = \frac{{{nf(I)}\times 100}}{{{nf(base)}}} = {nf(v)}\% \]", "%")


# ---------- Rule 33
def r33(P, r1, r2, t, A, want):
    P, r1, r2, t, A = map(F, (P, r1, r2, t, A))
    v = (100 * A - P * r2 * t) / ((r1 - r2) * t)
    assert v == want
    trad = [("Let the part at the first rate be y.", rf"\(\frac{{y\times {nf(r1)}\times {nf(t)}}}{{100}} + \frac{{({nf(P)} - y)\times {nf(r2)}\times {nf(t)}}}{{100}} = {nf(A)}\)."),
            ("Solve.", rf"\[ {nf(r1 * t)}y + {nf(P * r2 * t)} - {nf(r2 * t)}y = {nf(100 * A)} \Rightarrow {nf((r1 - r2) * t)}y = {nf(100 * A - P * r2 * t)} \Rightarrow y = {nf(v)} \]")]
    return n_(33, v, trad, rf"\(P = {nf(P)}\), \(r_1 = {nf(r1)}\), \(r_2 = {nf(r2)}\), \(t = {nf(t)}\), \(A = {nf(A)}\).",
              rf"\[ \frac{{100\times {nf(A)} - {nf(P)}\times {nf(r2)}\times {nf(t)}}}{{({nf(r1)} - {nf(r2)})\times {nf(t)}}} = \frac{{{nf(100 * A - P * r2 * t)}}}{{{nf((r1 - r2) * t)}}} = {nf(v)} \]", "Rs")


C = card
CARDS = {
    28: C(28, "Two Principals, Same Rate: Time", r"Only the difference of the principals makes the difference of the interests.", r"\[ t = \frac{A\times 100}{r(P_2-P_1)} \]",
          [("Extra principal", r"P_2 - P_1"), ("Its interest a year", r"\frac{r(P_2-P_1)}{100}"), ("Time", r"\frac{100A}{r(P_2-P_1)}")],
          r"Same rate and same time on both sums, so the interest common to both cancels.", "'The SI on Rs P1 is Rs A less than the SI on Rs P2 at r%; find the time.'",
          r"Rs \(1200\) and Rs \(1500\) at \(5\%\), Rs \(45\) less: \(\frac{4500}{5\times 300} = 3\) years.", r"Using one of the principals instead of their difference."),
    29: C(29, "Equal Sums, Different Rate and Time", r"Rs 100 earns \(r_1t_1\) in one case and \(r_2t_2\) in the other.", r"\[ \frac{I_d\times 100}{r_1t_1-r_2t_2} \]",
          [("Case 1", r"r_1\%\ \text{for}\ t_1"), ("Case 2", r"r_2\%\ \text{for}\ t_2"), ("Sum", r"\frac{100I_d}{r_1t_1-r_2t_2}")],
          r"Write months as years first (8 months \(= \frac{2}{3}\) year).", "'Two equal sums at r1% for t1 years and r2% for t2 years; the interests differ by Rs Id. Find each sum.'",
          r"\(8\%\) for \(5\) years and \(6\%\) for \(4\) years, Rs \(96\): \(\frac{9600}{40-24} = 600\).", r"Subtracting the rates and the times separately."),
    30: C(30, "Two Banks: Difference of Rates", r"Same sum and same time: the difference of interests comes from the difference of rates.", r"\[ \frac{I_d\times 100}{X\times t}\ \% \]",
          [("Sum", r"X"), ("Time", r"t"), ("Rate gap", r"\frac{100I_d}{Xt}")],
          r"It is Rule 6 turned round: the change in rate from the change in interest.", "'The interests from two banks on Rs X for t years differ by Rs Id; find the difference of their rates.'",
          r"Rs \(1500\) for \(3\) years, Rs \(36\): \(\frac{3600}{4500} = 0.8\%\).", r"Forgetting to divide by the years."),
    31: C(31, "Two Amounts: the Rate", r"The growth between the two times is the interest of the years between; the sum follows, then the rate.",
          r"\[ \frac{100(A_2-A_1)}{A_1t_2-A_2t_1}\ \% \]",
          [("Interest a year", r"\frac{A_2-A_1}{t_2-t_1}"), ("Sum", r"A_1 - t_1\times\frac{A_2-A_1}{t_2-t_1}"), ("Rate", r"\frac{100\times\text{interest a year}}{\text{sum}}")],
          r"Rule 13 gives the sum from the same two amounts.", "'A sum amounts to Rs A1 in t1 years and to Rs A2 in t2 years; find the rate.'",
          r"Rs \(1150\) in \(3\) years, Rs \(1250\) in \(5\): \(\frac{10000}{5750 - 3750} = 5\%\).", r"Working the rate on \(A_1\) instead of on the sum."),
    32: C(32, "Part Repaid, Then Settled", r"A part payment comes off the principal; interest runs on what is still owed.",
          r"\[ \frac{x_1+x_2-X}{x_1t_1+t_2(X-x_1)}\times 100\ \% \]",
          [("Interest paid", r"x_1 + x_2 - X"), ("First t1 years", r"X\ \text{at}\ r\%"), ("Next t2 - t1 years", r"X - x_1\ \text{at}\ r\%")],
          r"\(Xt_1 + (X-x_1)(t_2-t_1)\) is the same as \(x_1t_1 + t_2(X-x_1)\).", "'A man borrows Rs X; after t1 years he pays Rs x1 and at the end of t2 years Rs x2 to settle the account. Find the rate.'",
          r"Rs \(4000\), Rs \(1000\) after \(2\) years, Rs \(3700\) after \(4\): \(\frac{700}{2000 + 12000}\times 100 = 5\%\).", r"Taking the part payment off the interest instead of the principal."),
    33: C(33, "Sum Lent in Two Parts", r"The interest of both parts over the years adds up to the total interest.", r"\[ \frac{100A-Pr_2t}{(r_1-r_2)t} \]",
          [("Part 1", r"y\ \text{at}\ r_1\%"), ("Part 2", r"P - y\ \text{at}\ r_2\%"), ("Total", r"\frac{[r_1y + r_2(P-y)]t}{100} = A")],
          r"Rule 15 is the case \(t = 1\).", "'Some amount out of Rs P was lent at r1% and the rest at r2%; the total interest in t years was Rs A. Find the part at r1%.'",
          r"Rs \(5000\) at \(8\%\) and \(5\%\), \(2\) years, Rs \(620\): \(\frac{62000 - 50000}{3\times 2} = 2000\).", r"Leaving the years out of the bottom line."),
}


def q(k):
    return SENT[k][1](*PICK[k][:NVIS[SENT[k][0]]])


def fn_for(k):
    pool, p = SENT[k][0], PICK[k]
    return {"28": lambda: r28(*p), "28b": lambda: r28(*p), "29": lambda: r29(*p), "29m": lambda: r29m(*p), "29s": lambda: r29s(*p), "30": lambda: r30(*p),
            "31": lambda: r31(*p), "31m": lambda: r31(*p, more=True), "32": lambda: r32(*p), "33": lambda: r33(*p)}[pool]


KIND = {"28": "years", "28b": "years", "29": "Rs", "29m": "Rs", "29s": "Rs", "30": "%", "31": "%", "31m": "%", "32": "%", "33": "Rs"}
OLD_RULE = {790: 28, 791: 29, 792: 30, 793: 31, 794: 32, 795: 33}
OLD = {rid: (rule, q(rid), fn_for(rid), KIND[SENT[rid][0]]) for rid, rule in OLD_RULE.items()}
NEW = {}
for k in SENT:
    if isinstance(k, str):
        rule = int(k[1:k.index("_")])
        NEW.setdefault(rule, []).append((k, q(k), fn_for(k), KIND[SENT[k][0]], None))

if __name__ == "__main__":
    gen_1_6.main(OLD, NEW, CARDS, range(28, 34))
