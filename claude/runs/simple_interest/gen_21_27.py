"""Simple Interest Rules 21-27 (2026-10-31). Rule 21: n times at r% -> m times in the same time at ((m-1)/(n-1))r %. Rule 22: a sum
amounts to A1 at r1% in the time Rs P amounts to A2 at r2% - sum = A1 / [(1 - r1/r2) + A2r1/(Pr2)]. Rule 23: A1 in t years at r% ->
time to reach A2 = (A2/A1)(t + 100/r) - 100/r. Rule 24: parts whose amounts are equal after different times are in the ratio
1/(100 + r1t1) : 1/(100 + r2t2) : .... Rule 25: sum = 100A/(100 + rt). Rule 26: interest Rs A less than the sum - sum = 100A/(100 - rt).
Rule 27: n times in t years -> m times in ((m-1)/(n-1))t years. Writes the seven cards, regenerates the old rows 783-789 (keys all
right) and adds the book's exercises with no copy (sentences in sent_21_27.py, number sets in PICK, searched against the book).
Usage: python gen_21_27.py"""
import os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
import gen_14_20  # noqa: E402,F401  (its build_opts wrapper - kinds "pair_pr" / "pair_money" - stays underneath this one)
from common import card  # noqa: E402
from fmt import M, nf  # noqa: E402
from gen_1_6 import done, num  # noqa: E402
from helpers import place  # noqa: E402
from sent_21_27 import NVIS, SENT  # noqa: E402

TH = {
    21: (r"If a sum becomes \(n\) times itself at \(r\%\) per annum simple interest, it becomes \(m\) times itself in the same time at",
         r"\[ \left(\frac{m-1}{n-1}\right)\times r\ \% \]"),
    22: (r"If a sum amounts to Rs \(A_1\) at \(r_1\%\) in the time in which Rs \(P\) amounts to Rs \(A_2\) at \(r_2\%\) (simple interest), the sum is",
         r"\[ \frac{A_1}{\left(1-\frac{r_1}{r_2}\right)+\frac{A_2r_1}{Pr_2}} \]"),
    23: (r"If a sum amounts to Rs \(A_1\) in \(t\) years at \(r\%\) simple interest, the time in which it amounts to Rs \(A_2\) at the same rate is",
         r"\[ \frac{A_2}{A_1}\left(t+\frac{100}{r}\right)-\frac{100}{r}\ \text{years} \]"),
    24: (r"If parts of a sum, put at simple interest at \(r_1\%\) for \(t_1\) years, \(r_2\%\) for \(t_2\) years, ..., all amount to the same sum, the parts "
         r"are in the ratio", r"\[ \frac{1}{100+r_1t_1} : \frac{1}{100+r_2t_2} : \frac{1}{100+r_3t_3} : \dots \]"),
    25: (r"The sum that amounts to Rs \(A\) in \(t\) years at \(r\%\) per annum simple interest is", r"\[ P = \frac{100\times A}{100+rt} \]"),
    26: (r"If the simple interest on a sum at \(r\%\) for \(t\) years is Rs \(A\) less than the sum, the sum is", r"\[ P = \frac{100A}{100-rt} \]"),
    27: (r"If a sum becomes \(n\) times itself in \(t\) years at simple interest, it becomes \(m\) times itself in",
         r"\[ \left(\frac{m-1}{n-1}\right)\times t\ \text{years} \]"),
}
PICK = {
    783: (7, 3, 11, 5), "r21_e1": (2, 4, 7, 24), "r21_e2": (5, 5, 11, F(25, 2)), "r21_e3": (5, 4, 4, 3), "r21_e4": (6, 15, 3, 6), "r21_e5": (7, 9, 9, 12),
    784: (2565, 10, 1500, 1905, 3, 1350, 9), "r22_e1": (4130, 6, 2150, 2408, 4, 3500, 3), "r22_e2": (3720, 5, 1100, 1496, 9, 3100, 4),
    "r22_e3": (4961, 3, 200, 256, 4, 4100, 7), "r22_e4": (1652, 6, 2650, 3604, 12, 1400, 3), "r22_e5": (8213, 13, 4400, 7788, 11, 4300, 7),
    785: (9880, F(15, 2), 12, 11440, 10, 5200), "r23_e1": (6099, F(7, 2), 2, 6555, F(15, 2), 5700), "r23_e2": (11039, F(11, 2), 12, 17423, F(27, 2), 6650),
    "r23_e3": (5270, 2, 12, 9605, F(21, 2), 4250), "r23_e4": (9320, F(11, 2), 3, 9920, 8, 8000), "r23_e5": (1435, 7, 15, 1750, 10, 700),
    786: (11865, 3, 7, 9, 10, 4845, 3705, 3315), "r24_e1": (1998, 2, 5, 10, 6, 780, 672, 546), "r24_e2": (18197, 2, 6, 10, 2, 6510, 6045, 5642),
    "r24_e3": (26848, 3, 4, 4, 7, 8, 8, 10496, 9184, 7168), "r24_e4": (1776, 2, 5, 8, 10, 720, 576, 480), "r24_e5": (2150, 7, 16, 23, 10, 850, 1300),
    787: (1992, F(11, 2), 12, 1200), "r25_e1": (693, 5, F(23, 2), 440), "r25_e2": (11088, F(13, 2), 4, 8800), "r25_e3": (8442, 8, 10, 4690),
    "r25_e4": (10063, 6, F(15, 2), 6940), "r25_e5": (7443, 8, 10, 4135),
    788: (3, 3, 9373, 10300), "r26_e1": (3, F(21, 2), 6987, 10200), "r26_e2": (2, 12, 13262, 17450), "r26_e3": (F(17, 2), 7, 3564, 8800),
    "r26_e4": (2, F(11, 2), 6675, 7500), "r26_e5": (4, F(9, 2), 533, 650),
    789: (25, 5, 100), "r27_e1": (3, 20, 12, 110), "r27_e2": (4, 12, 12, 44), "r27_e3": (3, 10, 12, 55), "r27_e4": (3, 10, 11, 50), "r27_e5": (8, 7, 48),
    "r27_e6": (10, 8, 70),
}


def n_(r, v, trad, ident, sub, unit=""):
    return num(r, v, trad, ident, sub, unit, TH)


# ---------- Rule 21
def r21(n, r, m, want):
    n, r, m = map(F, (n, r, m))
    T = 100 * (n - 1) / r
    v = 100 * (m - 1) / T
    assert v == want
    trad = [("Time taken.", rf"Take the sum as Rs \(100\). It becomes \({nf(100 * n)}\), so the interest is \({nf(100 * (n - 1))}\); at \({nf(r)}\%\) that takes "
                            rf"\({nf(100 * (n - 1))} \div {nf(r)} = {nf(T)}\) years."),
            ("Rate for the new amount.", rf"To become \({nf(100 * m)}\) the interest must be \({nf(100 * (m - 1))}\) in \({nf(T)}\) years: "
                                         rf"\[ {nf(100 * (m - 1))} \div {nf(T)} = {nf(v)} \]per Rs \(100\) a year, i.e. \({nf(v)}\%\).")]
    return n_(21, v, trad, rf"\(n = {nf(n)}\), \(r = {nf(r)}\), \(m = {nf(m)}\).", rf"\[ \left(\frac{{{nf(m)}-1}}{{{nf(n)}-1}}\right)\times {nf(r)} = {nf(v)}\% \]", "%")


# ---------- Rule 22
def r22(A1, r1, P, A2, r2, want, t):
    A1, r1, P, A2, r2 = map(F, (A1, r1, P, A2, r2))
    T = (A2 - P) * 100 / (P * r2)
    v = 100 * A1 / (100 + r1 * T)
    assert T == t and v == want
    a, b = 1 - r1 / r2, A2 * r1 / (P * r2)
    trad = [("The common time.", rf"Rs \({nf(P)}\) earns \({nf(A2)} - {nf(P)} = {nf(A2 - P)}\) at \({nf(r2)}\%\): \(\frac{{{nf(A2 - P)}\times 100}}{{{nf(P)}\times {nf(r2)}}} = {nf(T)}\) years."),
            ("The sum.", rf"In \({nf(T)}\) years at \({nf(r1)}\%\), Rs \(100\) becomes \({nf(100 + r1 * T)}\): \[ \frac{{100\times {nf(A1)}}}{{{nf(100 + r1 * T)}}} = {nf(v)} \]")]
    return n_(22, v, trad, rf"\(A_1 = {nf(A1)}\), \(r_1 = {nf(r1)}\), \(P = {nf(P)}\), \(A_2 = {nf(A2)}\), \(r_2 = {nf(r2)}\).",
              rf"\[ \left(1-\frac{{{nf(r1)}}}{{{nf(r2)}}}\right)+\frac{{{nf(A2)}\times {nf(r1)}}}{{{nf(P)}\times {nf(r2)}}} = {nf(a)} + {nf(b)} = {nf(a + b)} \]"
              rf"\[ \frac{{{nf(A1)}}}{{{nf(a + b)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 23
def r23(A1, t, r, A2, want, P):
    A1, t, r, A2 = map(F, (A1, t, r, A2))
    p = 100 * A1 / (100 + r * t)
    v = (A2 - p) * 100 / (p * r)
    assert p == P and v == want
    trad = [("The sum.", rf"Rs \(100\) becomes \(100 + {nf(r)}\times {nf(t)} = {nf(100 + r * t)}\): sum \(= \frac{{100\times {nf(A1)}}}{{{nf(100 + r * t)}}} = {nf(p)}\)."),
            ("Time for the new amount.", rf"Interest needed \(= {nf(A2)} - {nf(p)} = {nf(A2 - p)}\); one year gives \(\frac{{{nf(r)}}}{{100}}\times {nf(p)} = {nf(p * r / 100)}\): "
                                         rf"\[ {nf(A2 - p)} \div {nf(p * r / 100)} = {nf(v)} \]")]
    return n_(23, v, trad, rf"\(A_1 = {nf(A1)}\), \(t = {nf(t)}\), \(r = {nf(r)}\), \(A_2 = {nf(A2)}\).",
              rf"\[ \frac{{{nf(A2)}}}{{{nf(A1)}}}\left({nf(t)}+\frac{{100}}{{{nf(r)}}}\right)-\frac{{100}}{{{nf(r)}}} = \frac{{{nf(A2)}}}{{{nf(A1)}}}\times {nf(t + 100 / r)} - {nf(100 / r)} = {nf(v)} \]",
              "years")


# ---------- Rule 24
def r24_core(X, rts, names):
    X = F(X)
    dens = [100 + F(r) * t for r, t in rts]
    L = 1
    for d in dens:
        L = L * int(d) // gcd(L, int(d))
    ints = [L // int(d) for d in dens]
    h = 0
    for x in ints:
        h = gcd(h, x)
    ints = [x // h for x in ints]
    parts = [X * x / sum(ints) for x in ints]
    A = parts[0] * dens[0] / 100
    terms = " + ".join(rf"\frac{{100A}}{{{nf(d)}}}" for d in dens)
    trad = [("Let every amount be A.", "A part that grows for \\(t\\) years at \\(r\\%\\) becomes \\(\\frac{100 + rt}{100}\\) of itself, so the parts are "
                                       + ", ".join(rf"\(\frac{{100A}}{{{nf(d)}}}\)" for d in dens) + "."),
            ("Add them up.", rf"\[ {terms} = {nf(X)} \Rightarrow A = {nf(A)} \]"
                             + ", ".join(rf"{names[i]} \(= \frac{{100\times {nf(A)}}}{{{nf(d)}}} = {nf(p)}\)" for i, (d, p) in enumerate(zip(dens, parts))) + ".")]
    ident = r"\(" + r",\ ".join(rf"100 + {nf(r)}\times {nf(t)} = {nf(d)}" for (r, t), d in zip(rts, dens)) + rf"\), \(X = {nf(X)}\)."
    sub = r"\[ " + " : ".join(rf"\frac{{1}}{{{nf(d)}}}" for d in dens) + " = " + " : ".join(str(x) for x in ints) + r" \]"
    share = ", ".join(rf"\(\frac{{{x}}}{{{sum(ints)}}}\times {nf(X)} = {nf(p)}\)" for x, p in zip(ints, parts)) + "."
    return parts, ints, trad, ident, sub, share


NAMES3, NAMES2 = ["first", "second", "third"], ["the younger son", "the elder son"]


def r24_ratio(X, t1, t2, t3, r, *parts):
    got, ints, trad, ident, sub, share = r24_core(X, [(r, t1), (r, t2), (r, t3)], NAMES3)
    assert got == list(parts)
    recips = " : ".join(rf"\frac{{1}}{{{nf(100 + F(r) * t)}}}" for t in (t1, t2, t3))
    trad = [trad[0], ("Compare the parts.", r"Dividing every part by \(100A\) leaves \(" + recips + " = " + " : ".join(str(x) for x in ints)
                      + r"\) (multiply through by the common multiple).")]
    return done(24, ("terms", tuple(ints)), M(" : ".join(str(x) for x in ints)), trad, ident, sub, TH)


def r24_diff(X, t1, t2, t3, r, *parts):
    got, ints, trad, ident, sub, share = r24_core(X, [(r, t1), (r, t2), (r, t3)], NAMES3)
    assert got == list(parts)
    d = max(got) - min(got)
    trad = trad + [("Difference.", rf"\[ {nf(max(got))} - {nf(min(got))} = {nf(d)} \]")]
    return n_(24, d, trad, ident, sub + share + rf" Difference \(= {nf(max(got))} - {nf(min(got))} = {nf(d)}\).", "Rs")


def r24_parts(X, rts, parts):
    got, ints, trad, ident, sub, share = r24_core(X, rts, NAMES3)
    assert got == list(parts)
    return done(24, ("triple", tuple(got)), ", ".join(f"Rs {M(nf(p))}" for p in got[:2]) + f" and Rs {M(nf(got[2]))}", trad, ident, sub + share, TH)


def r24_sons(X, a1, a2, Mt, r, p1, p2):
    got, ints, trad, ident, sub, share = r24_core(X, [(r, Mt - a1), (r, Mt - a2)], NAMES2)
    assert got == [p1, p2]
    first = rf"The sons have \({nf(Mt)} - {nf(a1)} = {nf(Mt - a1)}\) and \({nf(Mt)} - {nf(a2)} = {nf(Mt - a2)}\) years to go. "
    trad = [(trad[0][0], first + trad[0][1]), trad[1]]
    return done(24, ("pair", tuple(got)), f"Rs {M(nf(got[0]))} and Rs {M(nf(got[1]))}", trad, ident, sub + share, TH)


# ---------- Rules 25 and 26
def r25(A, t, r, want):
    A, t, r = map(F, (A, t, r))
    v = 100 * A / (100 + r * t)
    assert v == want
    trad = [("Amount of Rs 100.", rf"Rs \(100\) earns \({nf(r)}\times {nf(t)} = {nf(r * t)}\) in \({nf(t)}\) years and becomes \({nf(100 + r * t)}\)."),
            ("Scale down.", rf"\[ 100\times\frac{{{nf(A)}}}{{{nf(100 + r * t)}}} = {nf(v)} \]")]
    return n_(25, v, trad, rf"\(A = {nf(A)}\), \(t = {nf(t)}\), \(r = {nf(r)}\).", rf"\[ P = \frac{{100\times {nf(A)}}}{{100 + {nf(r)}\times {nf(t)}}} = \frac{{{nf(100 * A)}}}{{{nf(100 + r * t)}}} = {nf(v)} \]", "Rs")


def r26(r, t, A, want):
    r, t, A = map(F, (r, t, A))
    v = 100 * A / (100 - r * t)
    assert v == want
    trad = [("Interest as a part of the sum.", rf"In \({nf(t)}\) years at \({nf(r)}\%\) the interest is \(\frac{{{nf(r * t)}}}{{100}}\) of the sum, so the sum minus the interest is "
                                               rf"\(\frac{{{nf(100 - r * t)}}}{{100}}\) of the sum."),
            ("Solve.", rf"\[ \frac{{{nf(100 - r * t)}}}{{100}}P = {nf(A)} \Rightarrow P = {nf(v)} \]")]
    return n_(26, v, trad, rf"\(r = {nf(r)}\), \(t = {nf(t)}\), \(A = {nf(A)}\).", rf"\[ P = \frac{{100\times {nf(A)}}}{{100 - {nf(r)}\times {nf(t)}}} = \frac{{{nf(100 * A)}}}{{{nf(100 - r * t)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 27
def r27(n, t, m, want):
    n, t, m = map(F, (n, t, m))
    R = 100 * (n - 1) / t
    v = 100 * (m - 1) / R
    assert v == want
    trad = [("Rate.", rf"Take the sum as Rs \(100\): the interest is \({nf(100 * (n - 1))}\) in \({nf(t)}\) years, so the rate is \({nf(100 * (n - 1))} \div {nf(t)} = {nf(R)}\%\)."),
            ("Time for the new amount.", rf"It must earn \({nf(100 * (m - 1))}\): \[ {nf(100 * (m - 1))} \div {nf(R)} = {nf(v)} \]")]
    return n_(27, v, trad, rf"\(n = {nf(n)}\), \(t = {nf(t)}\), \(m = {nf(m)}\).", rf"\[ \left(\frac{{{nf(m)}-1}}{{{nf(n)}-1}}\right)\times {nf(t)} = {nf(v)} \]", "years")


_below = gen_1_6.build_opts


def triple_money(g, wrong):
    x, y, z = g["answer"][1]
    f = lambda a, b, c: f"Rs {M(nf(a))}, Rs {M(nf(b))} and Rs {M(nf(c))}"
    s = max(1, x // 20)
    return place(f(x, y, z), [f(*w) for w in (wrong or [(z, y, x), (y, x, z), (x + s, y - s, z)])])


def build_opts(g, kind, wrong):
    return triple_money(g, wrong) if kind == "triple_money" else _below(g, kind, wrong)


gen_1_6.build_opts = build_opts

C = card
CARDS = {
    21: C(21, "From n Times to m Times", r"In the same time the interest grows with the rate, and the interest needed is \((n-1)\) and \((m-1)\) times the sum.",
          r"\[ \left(\frac{m-1}{n-1}\right)\times r\ \% \]",
          [("n times", r"SI = (n-1)P\ \text{at}\ r\%"), ("m times", r"SI = (m-1)P"), ("New rate", r"\frac{m-1}{n-1}\times r")],
          r"Same sum, same time: the interest is in proportion to the rate.", "'A sum becomes n times itself at r%; at what rate will it become m times itself (in the same time)?'",
          r"\(3\) times at \(6\%\) \(\to\) \(5\) times: \(\frac{4}{2}\times 6 = 12\%\).", r"Using \(\frac{m}{n}\) instead of \(\frac{m-1}{n-1}\)."),
    22: C(22, "Same Time, Two Sums", r"The second sum fixes the time; the first sum follows from that time.", r"\[ \frac{A_1}{\left(1-\frac{r_1}{r_2}\right)+\frac{A_2r_1}{Pr_2}} \]",
          [("Time", r"t = \frac{100(A_2-P)}{Pr_2}"), ("Sum", r"\frac{100A_1}{100+r_1t}"), ("Equal rates", r"\frac{A_1}{A_2}\times P")],
          r"When \(r_1 = r_2\) the formula becomes \(\frac{A_1}{A_2}\times P\).", "'A sum amounted to Rs A1 at r1% in the time in which Rs P amounted to Rs A2 at r2%; find the sum.'",
          r"Rs \(520\) at \(6\%\) in the time Rs \(600\) became Rs \(750\) at \(5\%\): \(\frac{520}{-0.2 + 1.5} = 400\).", r"Swapping \(r_1\) and \(r_2\)."),
    23: C(23, "Time to Reach a New Amount", r"Find the sum from the first amount, then the years its interest needs for the new amount.",
          r"\[ \frac{A_2}{A_1}\left(t+\frac{100}{r}\right)-\frac{100}{r} \]",
          [("Sum", r"\frac{100A_1}{100+rt}"), ("Interest needed", r"A_2 - P"), ("Time", r"\frac{100(A_2-P)}{Pr}")],
          r"\(t + \frac{100}{r}\) is the amount per year of interest; scaling it by \(\frac{A_2}{A_1}\) gives the new one.",
          "'A sum amounts to Rs A1 in t years at r%; in how many years will it amount to Rs A2?'",
          r"Rs \(1200\) in \(4\) years at \(5\%\), Rs \(1500\): \(\frac{1500}{1200}\times 24 - 20 = 10\) years.", r"Taking \(A_1\) as the principal."),
    24: C(24, "Parts With Equal Amounts", r"Each part times \((100 + rt)\) is the same, so the parts go as the reciprocals.",
          r"\[ \frac{1}{100+r_1t_1} : \frac{1}{100+r_2t_2} : \dots \]",
          [("Part 1", r"P_1\left(1+\frac{r_1t_1}{100}\right)"), ("Part 2", r"P_2\left(1+\frac{r_2t_2}{100}\right)"), ("Equal", r"P_1(100+r_1t_1) = P_2(100+r_2t_2)")],
          r"Compare Rule 20: there the interests are equal, here the amounts.", "'A sum is divided so that the amounts after t1, t2, t3 years (at r%) are equal; find the parts / their ratio.'",
          r"Two parts, \(2\) and \(5\) years at \(10\%\): \(\frac{1}{120} : \frac{1}{150} = 5 : 4\).", r"Making the parts proportional to \(100 + rt\) instead of its reciprocal."),
    25: C(25, "Sum From the Amount", r"Rs 100 grows to \(100 + rt\); scale that to the amount.", r"\[ P = \frac{100A}{100+rt} \]",
          [("Rs 100 becomes", r"100 + rt"), ("Amount", r"A"), ("Sum", r"\frac{100A}{100+rt}")],
          r"The amount is principal plus interest, and the interest is worked on the principal.", "'What sum will amount to Rs A in t years at r% simple interest?'",
          r"Rs \(1300\) in \(6\) years at \(5\%\): \(\frac{130000}{130} = 1000\).", r"Taking \(rt\%\) off the amount."),
    26: C(26, "Interest Short of the Sum", r"Sum minus interest is \(\frac{100 - rt}{100}\) of the sum.", r"\[ P = \frac{100A}{100-rt} \]",
          [("Interest", r"\frac{rt}{100}P"), ("Sum - interest", r"\frac{100-rt}{100}P = A"), ("Sum", r"\frac{100A}{100-rt}")],
          r"Works only while \(rt \lt 100\) (the interest is still less than the sum).", "'A sum lent at r%; in t years the interest is Rs A less than the sum. Find the sum.'",
          r"\(5\%\) for \(6\) years, Rs \(280\) less: \(\frac{28000}{70} = 400\).", r"Using \(100 + rt\) in the bottom line."),
    27: C(27, "Times Itself, Different Multiple", r"The interest needed is \((n-1)\) and \((m-1)\) times the sum at the same rate, so the times go the same way.",
          r"\[ \left(\frac{m-1}{n-1}\right)\times t \]",
          [("n times", r"(n-1)P\ \text{in}\ t\ \text{years}"), ("m times", r"(m-1)P"), ("Time", r"\frac{m-1}{n-1}\times t")],
          r"Same sum, same rate: the interest is in proportion to the time.", "'A sum becomes n times itself in t years; in how many years will it become m times itself?'",
          r"\(3\) times in \(8\) years \(\to\) \(5\) times: \(\frac{4}{2}\times 8 = 16\) years.", r"Using \(\frac{m}{n}\times t\)."),
}


def q(k):
    return SENT[k][1](*PICK[k][:NVIS[SENT[k][0]]])


def fn_for(k):
    pool, p = SENT[k][0], PICK[k]
    return {"21": lambda: r21(*p), "22": lambda: r22(*p), "23": lambda: r23(*p), "24r": lambda: r24_ratio(*p), "24d": lambda: r24_diff(*p),
            "24p": lambda: r24_parts(p[0], [(p[4], p[1]), (p[4], p[2]), (p[4], p[3])], p[5:]),
            "24v": lambda: r24_parts(p[0], [(p[1], p[2]), (p[3], p[4]), (p[5], p[6])], p[7:]), "24s": lambda: r24_sons(*p),
            "25": lambda: r25(*p), "26": lambda: r26(*p), "27": lambda: r27(*p), "27d": lambda: r27(2, *p)}[pool]


KIND = {"21": "%", "22": "Rs", "23": "years", "24r": "terms", "24d": "Rs", "24p": "triple_money", "24v": "triple_money", "24s": "pair_money",
        "25": "Rs", "26": "Rs", "27": "years", "27d": "years"}
OLD_RULE = {783: 21, 784: 22, 785: 23, 786: 24, 787: 25, 788: 26, 789: 27}
OLD = {rid: (rule, q(rid), fn_for(rid), KIND[SENT[rid][0]]) for rid, rule in OLD_RULE.items()}
NEW = {}
for k in SENT:
    if isinstance(k, str):
        rule = int(k[1:k.index("_")])
        NEW.setdefault(rule, []).append((k, q(k), fn_for(k), KIND[SENT[k][0]], None))

if __name__ == "__main__":
    gen_1_6.main(OLD, NEW, CARDS, range(21, 28))
