"""Simple Interest Rules 7-13 (2026-10-30). Rule 7: the equal yearly payment that clears a debt due in t years - 100A / (100t + rt(t-1)/2).
Rule 8: rates that change over periods - P = 100 I / (r1t1 + r2t2 + r3t3). Rule 9: a sum becomes x times itself - R = 100(x-1)/t and
t = 100(x-1)/r. Rule 10: one sum amounts to A1 at r1% and A2 at r2% in the same time - t = 100(A1-A2)/(A2r1 - A1r2). Rule 11: the same
setting, the sum (A2r1 - A1r2)/(r1 - r2). Rule 12: x% higher rate for t years gives Rs A more - P = 100A/(tx). Rule 13: amounts A1 in t1
years and A2 in t2 years - P = (A2t1 - A1t2)/(t1 - t2). Writes the seven cards, regenerates the old rows 769-775 (775 asked "the sum and
the rate" with rate-only options - it now has sum-and-rate options) and adds the book's exercises with no copy (sentences in sent_7_13.py,
number sets in PICK, searched against the book). Usage: python gen_7_13.py"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
from common import card  # noqa: E402
from fmt import M, nf  # noqa: E402
from gen_1_6 import done, num  # noqa: E402
from helpers import place  # noqa: E402
from sent_7_13 import SENT  # noqa: E402

TH = {
    7: (r"The equal yearly payment that clears a debt of Rs \(A\) due in \(t\) years, at \(r\%\) per annum simple interest, is",
        r"\[ x = \frac{100A}{100t+\frac{rt(t-1)}{2}} \]"),
    8: (r"If the rate is \(r_1\%\) for the first \(t_1\) years, \(r_2\%\) for the next \(t_2\) years and \(r_3\%\) for the next \(t_3\) years, and the "
        r"total simple interest is Rs \(I\), the sum is", r"\[ P = \frac{I\times 100}{r_1t_1+r_2t_2+r_3t_3} \]"),
    9: (r"If a sum becomes \(x\) times itself in \(t\) years at simple interest, the rate is \(R\); at \(r\%\) per annum it takes \(t\) years, where",
        r"\[ R = \frac{100(x-1)}{t}\%,\qquad t = \frac{100(x-1)}{r} \]"),
    10: (r"If a sum amounts to Rs \(A_1\) at \(r_1\%\) per annum and to Rs \(A_2\) at \(r_2\%\) per annum in the same time, the time is",
         r"\[ t = \frac{100(A_1-A_2)}{A_2r_1-A_1r_2}\ \text{years} \]"),
    11: (r"If a sum amounts to Rs \(A_1\) at \(r_1\%\) per annum and to Rs \(A_2\) at \(r_2\%\) per annum in the same time, the sum is",
         r"\[ P = \frac{A_2r_1-A_1r_2}{r_1-r_2} \]"),
    12: (r"If a sum put at simple interest for \(t\) years would fetch Rs \(A\) more at a rate \(x\%\) higher, the sum is",
         r"\[ P = \frac{A\times 100}{t\times x} \]"),
    13: (r"If a sum amounts to Rs \(A_1\) in \(t_1\) years and to Rs \(A_2\) in \(t_2\) years at simple interest, the sum is",
         r"\[ P = \frac{A_2t_1-A_1t_2}{t_1-t_2} \]"),
}
PICK = {
    769: (15960, 3, 12, 4750), "r7_e1": (27300, 5, 10, 4550), "r7_e2": (12150, 6, 5, 1800), "r7_e3": (66456, 8, 12, 5850),
    "r7_e4": (22500, 5, 10, 3750), "r7_e5": (57240, 8, 10, 5300), "r7_e6": (6630, 8, 3, 750),
    770: (9, 4, 13, 3, 7, 11, 4560, 14, 3000), "r8_e1": (9, 3, 11, 2, 5, 8, 8775, 7, 13500), "r8_e2": (14, 2, 8, 5, 7, 12, 19140, 11, 16500),
    "r8_e3": (14, 2, 6, 5, 7, 4, 5600, 10, 8000), "r8_e4": (3, 2, 10, 6, 8, 4, 700, 9, 1000), "r8_e5": (3, 4, 7, 2, 6, 8, 5800, 10, 10000),
    771: (40, F(5, 2)), "r9_x2": (20, 10), "r9_x3": (7, 10, 60), "r9_e1": (6, 40, F(25, 2)), "r9_e2": (5, 25, 16), "r9_e3": (4, 10, 30),
    "r9_e4": (5, 16, 25), "r9_e5": (4, 5, 60), "r9_e6": (2, 50), "r9_e7": (8, 25),
    772: (6, 2059, 4, 1856, 7, 1450), "r10_e1": (10, 2800, 3, 2065, 6, 1750), "r10_e2": (6, 5313, 4, 4692, 9, 3450),
    "r10_e3": (11, 2928, 7, 2736, 2, 2400), "r10_e4": (9, 2808, 5, 2160, 12, 1350), "r10_e5": (14, 390, 7, 320, 4, 250),
    773: (13, 9085, 11, 8295, 10, 3950), "r11_e1": (15, 3750, 14, 3600, 10, 1500), "r11_e2": (15, 3230, 11, 2822, 6, 1700),
    "r11_e3": (14, 2938, 7, 2119, 9, 1300), "r11_e4": (10, 5760, 3, 3968, 8, 3200),
    774: (4, 8, 1056, 3300), "r12_e1": (4, 4, 1296, 8100), "r12_e2": (6, 4, 1080, 4500), "r12_e3": (5, 6, 2310, 7700), "r12_e4": (6, 5, 2940, 9800),
    "r12_e5": (3, 6, 1350, 7500),
    775: (5364, 7, 5616, 8, 3600, 7), "r13_e1": (3420, 2, 4470, 7, 3000, 7), "r13_e2": (5940, 5, 7110, F(15, 2), 3600, 13),
    "r13_e3": (4123, F(11, 2), 4402, 7, 3100, 6), "r13_e4": (5985, 9, 6300, 10, 3150, 10), "r13_e5": (5394, 2, 7254, 7, 4650, 8),
    "r13_e6": (2170, 5, 2632, 8, 1400, 11), "r13_e7": (3588, F(19, 2), 3640, 10, 2600, 4),
}


def n_(r, v, trad, ident, sub, unit=""):
    return num(r, v, trad, ident, sub, unit, TH)


# ---------- Rule 7
def r7(A, t, r, want):
    A, t, r = map(F, (A, t, r))
    S = t * (t - 1) / 2
    v = A / (t + r * S / 100)
    assert v == want
    trad = [("Interest earned by each payment.", rf"Let each payment be Rs \(x\). The payment made at the end of year 1 earns interest for \({nf(t - 1)}\) years, the next for "
                                                 rf"\({nf(t - 2)}\), ..., the last for \(0\) years: \({' + '.join(str(k) for k in range(int(t) - 1, -1, -1))} = {nf(S)}\) years in all."),
            ("Payments and their interest clear the debt.", rf"\[ {nf(t)}x + \frac{{x\times {nf(r)}\times {nf(S)}}}{{100}} = {nf(A)} \]"
                                                            rf"\[ x\left({nf(t)} + {nf(r * S / 100)}\right) = {nf(A)} \Rightarrow x = \frac{{{nf(A)}}}{{{nf(t + r * S / 100)}}} = {nf(v)} \]")]
    return n_(7, v, trad, rf"\(A = {nf(A)}\), \(t = {nf(t)}\), \(r = {nf(r)}\).",
              rf"\[ x = \frac{{100\times {nf(A)}}}{{100\times {nf(t)} + \frac{{{nf(r)}\times {nf(t)}\times {nf(t - 1)}}}{{2}}}} = \frac{{{nf(100 * A)}}}{{{nf(100 * t + r * S)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 8
def r8(r1, t1, r2, t2, t12, r3, I, T, want):
    r1, t1, r2, t2, r3, I, T = map(F, (r1, t1, r2, t2, r3, I, T))
    t3 = T - t1 - t2
    S = r1 * t1 + r2 * t2 + r3 * t3
    v = 100 * I / S
    assert v == want and t12 == t1 + t2
    trad = [("Interest on Rs 100.", rf"The last part lasts \({nf(T)} - {nf(t1 + t2)} = {nf(t3)}\) years. Rs \(100\) earns "
                                    rf"\({nf(r1)}\times {nf(t1)} + {nf(r2)}\times {nf(t2)} + {nf(r3)}\times {nf(t3)} = {nf(r1 * t1)} + {nf(r2 * t2)} + {nf(r3 * t3)} = {nf(S)}\)."),
            ("Scale up.", rf"To earn Rs \({nf(I)}\): \[ 100\times\frac{{{nf(I)}}}{{{nf(S)}}} = {nf(v)} \]")]
    return n_(8, v, trad, rf"\(r_1 = {nf(r1)}, t_1 = {nf(t1)}\); \(r_2 = {nf(r2)}, t_2 = {nf(t2)}\); \(r_3 = {nf(r3)}, t_3 = {nf(t3)}\); \(I = {nf(I)}\).",
              rf"\[ P = \frac{{{nf(I)}\times 100}}{{{nf(r1)}\times {nf(t1)} + {nf(r2)}\times {nf(t2)} + {nf(r3)}\times {nf(t3)}}} = \frac{{{nf(100 * I)}}}{{{nf(S)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 9
def r9_rate(x, t, want):
    x, t = F(x), F(t)
    v = 100 * (x - 1) / t
    assert v == want
    trad = [("Take the sum as Rs 100.", rf"It becomes \({nf(100 * x)}\), so the interest is \({nf(100 * x)} - 100 = {nf(100 * (x - 1))}\) in \({nf(t)}\) years."),
            ("Interest in one year on Rs 100.", rf"\[ {nf(100 * (x - 1))} \div {nf(t)} = {nf(v)} \]That is the rate: \({nf(v)}\%\).")]
    return n_(9, v, trad, rf"\(x = {nf(x)}\), \(t = {nf(t)}\).", rf"\[ R = \frac{{100({nf(x)}-1)}}{{{nf(t)}}} = {nf(v)}\% \]", "%")


def r9_time(x, r, want):
    x, r = F(x), F(r)
    v = 100 * (x - 1) / r
    assert v == want
    trad = [("Take the sum as Rs 100.", rf"It must become \({nf(100 * x)}\), so the interest needed is \({nf(100 * (x - 1))}\)."),
            ("Years.", rf"Rs \(100\) earns \({nf(r)}\) a year: \[ {nf(100 * (x - 1))} \div {nf(r)} = {nf(v)} \]")]
    return n_(9, v, trad, rf"\(x = {nf(x)}\), \(r = {nf(r)}\).", rf"\[ t = \frac{{100({nf(x)}-1)}}{{{nf(r)}}} = {nf(v)} \]", "years")


# ---------- Rules 10 and 11
def r10(r1, A1, r2, A2, t, P):
    r1, A1, r2, A2 = map(F, (r1, A1, r2, A2))
    v = 100 * (A1 - A2) / (A2 * r1 - A1 * r2)
    assert v == t
    trad = [("Write both amounts.", rf"For the sum \(P\) and time \(t\): \({nf(A1)} = P\left(1 + \frac{{{nf(r1)}t}}{{100}}\right)\) and \({nf(A2)} = P\left(1 + \frac{{{nf(r2)}t}}{{100}}\right)\)."),
            ("Divide one by the other.", rf"\[ \frac{{{nf(A1)}}}{{{nf(A2)}}} = \frac{{100 + {nf(r1)}t}}{{100 + {nf(r2)}t}} \Rightarrow {nf(100 * A1)} + {nf(A1 * r2)}t = {nf(100 * A2)} + {nf(A2 * r1)}t \]"
                                         rf"\[ {nf(A2 * r1 - A1 * r2)}t = {nf(100 * (A1 - A2))} \Rightarrow t = {nf(v)} \]")]
    return n_(10, v, trad, rf"\(A_1 = {nf(A1)}\), \(r_1 = {nf(r1)}\), \(A_2 = {nf(A2)}\), \(r_2 = {nf(r2)}\).",
              rf"\[ t = \frac{{100({nf(A1)}-{nf(A2)})}}{{{nf(A2)}\times {nf(r1)} - {nf(A1)}\times {nf(r2)}}} = \frac{{{nf(100 * (A1 - A2))}}}{{{nf(A2 * r1 - A1 * r2)}}} = {nf(v)} \]", "years")


def r11(r1, A1, r2, A2, t, P):
    r1, A1, r2, A2 = map(F, (r1, A1, r2, A2))
    v = (A2 * r1 - A1 * r2) / (r1 - r2)
    assert v == P
    trad = [("Compare the two interests.", rf"In the same time the interests are in the ratio of the rates: \(\frac{{{nf(A1)} - P}}{{{nf(A2)} - P}} = \frac{{{nf(r1)}}}{{{nf(r2)}}}\)."),
            ("Solve for P.", rf"\[ {nf(r2)}({nf(A1)} - P) = {nf(r1)}({nf(A2)} - P) \Rightarrow {nf(r1 - r2)}P = {nf(r1 * A2)} - {nf(r2 * A1)} = {nf(r1 * A2 - r2 * A1)} \]"
                             rf"\[ P = {nf(v)} \]")]
    return n_(11, v, trad, rf"\(A_1 = {nf(A1)}\), \(r_1 = {nf(r1)}\), \(A_2 = {nf(A2)}\), \(r_2 = {nf(r2)}\).",
              rf"\[ P = \frac{{{nf(A2)}\times {nf(r1)} - {nf(A1)}\times {nf(r2)}}}{{{nf(r1)} - {nf(r2)}}} = \frac{{{nf(A2 * r1 - A1 * r2)}}}{{{nf(r1 - r2)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 12
def r12(t, x, A, want):
    t, x, A = map(F, (t, x, A))
    v = 100 * A / (t * x)
    assert v == want
    trad = [("Extra interest on Rs 100.", rf"The extra \({nf(x)}\%\) for \({nf(t)}\) years gives Rs \(100\) an extra \({nf(x)}\times {nf(t)} = {nf(x * t)}\)."),
            ("Scale up.", rf"The extra is Rs \({nf(A)}\): \[ 100\times\frac{{{nf(A)}}}{{{nf(x * t)}}} = {nf(v)} \]")]
    return n_(12, v, trad, rf"\(t = {nf(t)}\), \(x = {nf(x)}\), \(A = {nf(A)}\).", rf"\[ P = \frac{{{nf(A)}\times 100}}{{{nf(t)}\times {nf(x)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 13
def r13_parts(A1, t1, A2, t2):
    A1, t1, A2, t2 = map(F, (A1, t1, A2, t2))
    one = (A2 - A1) / (t2 - t1)
    P = A1 - one * t1
    trad = [("Interest of one year.", rf"From \({nf(t1)}\) to \({nf(t2)}\) years the amount grows by \({nf(A2)} - {nf(A1)} = {nf(A2 - A1)}\) in \({nf(t2 - t1)}\) years: "
                                      rf"\({nf(one)}\) a year."),
            ("Take out the interest.", rf"Interest for \({nf(t1)}\) years \(= {nf(one)}\times {nf(t1)} = {nf(one * t1)}\); sum \(= {nf(A1)} - {nf(one * t1)} = {nf(P)}\).")]
    ident = rf"\(A_1 = {nf(A1)}\), \(t_1 = {nf(t1)}\), \(A_2 = {nf(A2)}\), \(t_2 = {nf(t2)}\)."
    sub = rf"\[ P = \frac{{{nf(A2)}\times {nf(t1)} - {nf(A1)}\times {nf(t2)}}}{{{nf(t1)} - {nf(t2)}}} = \frac{{{nf(A2 * t1 - A1 * t2)}}}{{{nf(t1 - t2)}}} = {nf(P)} \]"
    return P, one, trad, ident, sub


def r13(A1, t1, A2, t2, P, r):
    v, one, trad, ident, sub = r13_parts(A1, t1, A2, t2)
    assert v == P
    return n_(13, v, trad, ident, sub, "Rs")


def r13_rate(A1, t1, A2, t2, P, r):
    v, one, trad, ident, sub = r13_parts(A1, t1, A2, t2)
    R = 100 * one / v
    assert v == P and R == r
    trad = trad + [("Rate.", rf"\[ \frac{{{nf(one)}}}{{{nf(v)}}}\times 100 = {nf(R)}\% \]")]
    sub = sub + rf"Rate \(= \frac{{100\times ({nf(F(A1) - v)})}}{{{nf(v)}\times {nf(t1)}}} = {nf(R)}\%\)."
    return done(13, ("pair", (v, R)), f"sum Rs {M(nf(v))}, rate {M(nf(R) + chr(92) + '%')}", trad, ident, sub, TH)


def pr_opts(g, wrong):
    P, R = g["answer"][1]
    f = lambda p, q: f"Rs {M(nf(p))}, {M(nf(q) + chr(92) + '%')}"
    s = max(1, P // 10)
    return place(f(P, R), [f(p, q) for p, q in (wrong or [(P + s, R), (P, R + 1), (P - s, R + 1)])])


_base_opts = gen_1_6.build_opts


def build_opts(g, kind, wrong):
    return pr_opts(g, wrong) if kind == "pair_pr" else _base_opts(g, kind, wrong)


gen_1_6.build_opts = build_opts

C = card
CARDS = {
    7: C(7, "Equal Yearly Payments", r"Each payment earns interest from the day it is paid until the debt is due; the last payment earns none.",
         r"\[ x = \frac{100A}{100t+\frac{rt(t-1)}{2}} \]",
         [("Payments", r"t\ \text{of Rs}\ x"), ("Years of interest", r"(t-1) + (t-2) + \dots + 0 = \frac{t(t-1)}{2}"), ("Debt", r"tx + \frac{xr}{100}\cdot\frac{t(t-1)}{2} = A")],
         r"The payments together with the interest they earn up to the due date must equal the debt.",
         "'What annual payment will discharge a debt of Rs A due in t years at r% simple interest?'",
         r"Rs \(1030\) due in \(2\) years at \(6\%\): \(\frac{103000}{200 + 6} = 500\).", r"Giving every payment interest for the full \(t\) years."),
    8: C(8, "Rates Over Periods", r"Add the interest that Rs 100 earns in each period at its own rate.", r"\[ P = \frac{I\times 100}{r_1t_1+r_2t_2+r_3t_3} \]",
         [("Period 1", r"r_1\%\ \text{for}\ t_1"), ("Period 2", r"r_2\%\ \text{for}\ t_2"), ("Period 3", r"r_3\%\ \text{for}\ t_3 = T - t_1 - t_2")],
         r"Rs 100 earns \(r_1t_1+r_2t_2+r_3t_3\) in all; the sum is that many hundreds as the interest needs.",
         "'Interest is r1% for the first t1 years, r2% for the next t2 years and r3% beyond; the total interest is Rs I in T years. Find the sum.'",
         r"\(4\%\) for \(2\) years, \(6\%\) for \(3\), \(9\%\) for \(2\) more; Rs \(880\): \(\frac{88000}{8+18+18} = 2000\).", r"Using the whole time for the last rate instead of \(T - t_1 - t_2\)."),
    9: C(9, "Sum Becomes x Times", r"Becoming \(x\) times itself means the interest is \((x-1)\) times the sum.", r"\[ R = \frac{100(x-1)}{t}\%,\qquad t = \frac{100(x-1)}{r} \]",
         [("Doubles", r"x = 2,\ SI = P"), ("Trebles", r"x = 3,\ SI = 2P"), ("x times", r"SI = (x-1)P")],
         r"Take the sum as 100: the interest needed is \(100(x-1)\), and it comes at the rate per cent every year.",
         "'A sum becomes x times itself in t years at SI; find the rate' / 'in what time will a sum become x times itself at r%?'",
         r"\(5\) times in \(32\) years: \(\frac{100\times 4}{32} = 12.5\%\).", r"Using \(x\) instead of \(x - 1\)."),
    10: C(10, "Two Amounts at Two Rates: Time", r"The same sum for the same time gives two amounts at two rates.", r"\[ t = \frac{100(A_1-A_2)}{A_2r_1-A_1r_2} \]",
          [("At r1", r"A_1 = P\left(1+\frac{r_1t}{100}\right)"), ("At r2", r"A_2 = P\left(1+\frac{r_2t}{100}\right)"), ("Time", r"\frac{100(A_1-A_2)}{A_2r_1-A_1r_2}")],
          r"Dividing the two amounts removes the sum and leaves an equation in the time only.",
          "'A sum amounts to Rs A1 at r1% and to Rs A2 at r2% in the same time; find the time.'",
          r"Rs \(660\) at \(8\%\), Rs \(600\) at \(5\%\): \(\frac{100\times 60}{4800 - 3300} = 4\) years.", r"Pairing \(A_1\) with \(r_2\) in the bottom line the wrong way round."),
    11: C(11, "Two Amounts at Two Rates: Sum", r"In the same time the two interests are in the ratio of the rates.", r"\[ P = \frac{A_2r_1-A_1r_2}{r_1-r_2} \]",
          [("Interest at r1", r"A_1 - P"), ("Interest at r2", r"A_2 - P"), ("Ratio", r"\frac{A_1-P}{A_2-P} = \frac{r_1}{r_2}")],
          r"Cross-multiplying the ratio of the interests gives the sum straight away.",
          "'A sum amounts to Rs A1 at r1% and to Rs A2 at r2% in the same time; find the sum.'",
          r"Rs \(660\) at \(8\%\), Rs \(600\) at \(5\%\): \(\frac{4800 - 3300}{3} = 500\).", r"Taking the difference of the amounts as the sum."),
    12: C(12, "Higher Rate, More Interest", r"Only the extra rate makes the extra interest.", r"\[ P = \frac{A\times 100}{t\times x} \]",
          [("Extra rate", r"x\%"), ("Time", r"t\ \text{years}"), ("Extra interest", r"A = \frac{P\times x\times t}{100}")],
          r"The interest at the old rate is the same in both cases and cancels.", "'Had the sum been put at x% higher rate for t years, it would have fetched Rs A more; find the sum.'",
          r"\(4\) years, \(2\%\) higher, Rs \(56\) more: \(\frac{5600}{8} = 700\).", r"Dividing by a whole rate instead of the extra rate."),
    13: C(13, "Amounts After Two Times", r"The growth of the amount between the two times is the interest for the years between.", r"\[ P = \frac{A_2t_1-A_1t_2}{t_1-t_2} \]",
          [("Interest a year", r"\frac{A_2-A_1}{t_2-t_1}"), ("Sum", r"A_1 - t_1\times\frac{A_2-A_1}{t_2-t_1}"), ("Rate", r"\frac{100\times\text{interest a year}}{P}")],
          r"Simple interest is the same every year, so the extra amount per extra year is one year's interest.",
          "'A sum amounts to Rs A1 in t1 years and to Rs A2 in t2 years; find the sum (and the rate).'",
          r"Rs \(1120\) in \(2\) years, Rs \(1240\) in \(4\): \(60\) a year, sum \(1000\), rate \(6\%\).", r"Taking \(A_1\) as the sum."),
}


def q(k):
    return SENT[k][1](*PICK[k][:{"7": 3, "8": 8, "9r2": 1, "9r3": 1, "9t": 2, "9r": 2, "9t2": 1, "9t3": 1, "10": 4, "12": 3, "13": 4}[SENT[k][0]]])


def fn_for(k):
    pool, p = SENT[k][0], PICK[k]
    return {"7": lambda: r7(*p), "8": lambda: r8(*p), "9r2": lambda: r9_rate(2, *p), "9r3": lambda: r9_rate(3, *p), "9r": lambda: r9_rate(*p),
            "9t": lambda: r9_time(*p), "9t2": lambda: r9_time(2, *p), "9t3": lambda: r9_time(3, *p)}.get(pool) or {
        "10": lambda: (r10 if (k == 772 or str(k).startswith("r10")) else r11)(*p), "12": lambda: r12(*p),
        "13": lambda: (r13_rate if (k == 775 or k in ("r13_e5", "r13_e6", "r13_e7")) else r13)(*p)}[pool]


KIND = {7: "Rs", 8: "Rs", 10: "years", 11: "Rs", 12: "Rs", 13: "Rs"}


def kind_for(rule, k):
    if rule == 9:
        return "years" if SENT[k][0].startswith("9t") else "%"
    if rule == 13 and (k == 775 or k in ("r13_e5", "r13_e6", "r13_e7")):
        return "pair_pr"
    return KIND[rule]


OLD_RULE = {769: 7, 770: 8, 771: 9, 772: 10, 773: 11, 774: 12, 775: 13}
OLD = {rid: (rule, q(rid), fn_for(rid), kind_for(rule, rid)) for rid, rule in OLD_RULE.items()}
NEW = {}
for k in SENT:
    if isinstance(k, str):
        rule = int(k[1:k.index("_")])
        NEW.setdefault(rule, []).append((k, q(k), fn_for(k), kind_for(rule, k), None))

if __name__ == "__main__":
    gen_1_6.main(OLD, NEW, CARDS, range(7, 14))
