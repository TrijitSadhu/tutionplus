"""Simple Interest Rules 34-39 (2026-10-31). Rule 34: 1/n1 of a capital at x1%, 1/n2 at x2%, the rest at x3%, yearly income Rs A - capital =
100A / (x1/n1 + x2/n2 + x3/n3). Rule 35: SI on Rs P is Rs I and the years equal the rate - rate = sqrt(100I/P). Rule 36: interest Rs I at
r% for t years - amount = I(1 + 100/(rt)). Rule 37: Rs P1 for t1 years and Rs P2 for t2 years at one rate give Rs I - rate = 100I/(P1t1 +
P2t2). Rule 38: Rs P1 at r1% gives Rs I1; Rs P2 must give Rs I2 in the same years - rate = (I2/I1)(P1/P2)r1. Rule 39: a sum becomes n
times itself at r% in ((n-1)/r) x 100 years. Writes the six cards, regenerates the old rows 796-800 (keys all right; Rule 36 had no row)
and adds the book's examples / exercises with no copy (sentences in sent_34_39.py, number sets in PICK, searched against the book;
the Rule 39 sets leave out the book's own 'double in 8 / 20 years', 'treble in 25 years', 'treble at 3 1/8%'). Usage: python gen_34_39.py"""
import os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
from common import card  # noqa: E402
from fmt import nf  # noqa: E402
from gen_1_6 import frc, num  # noqa: E402
from sent_34_39 import NVIS, SENT  # noqa: E402

TH = {
    34: (r"If \(\frac{1}{n_1}\) of a capital is invested at \(x_1\%\), \(\frac{1}{n_2}\) at \(x_2\%\) and the remainder \(\frac{1}{n_3}\) at \(x_3\%\), and the yearly "
         r"income is Rs \(A\), the capital is", r"\[ \frac{A\times 100}{\frac{x_1}{n_1}+\frac{x_2}{n_2}+\frac{x_3}{n_3}} \]"),
    35: (r"If the simple interest on Rs \(P\) is Rs \(I\) and the number of years equals the rate per cent, the rate (and the time) is",
         r"\[ \sqrt{\frac{100\times I}{P}} \]"),
    36: (r"If a borrower pays \(r\%\) simple interest for \(t\) years and the interest is Rs \(I\), the amount (principal + interest) is",
         r"\[ A = I\left(1+\frac{100}{rt}\right) \]"),
    37: (r"If Rs \(P_1\) is lent for \(t_1\) years and Rs \(P_2\) for \(t_2\) years at one rate and the total simple interest is Rs \(I\), the rate is",
         r"\[ \frac{100I}{P_1t_1+P_2t_2}\ \% \]"),
    38: (r"If Rs \(P_1\) at \(r_1\%\) gives Rs \(I_1\) as interest in some years, the rate at which Rs \(P_2\) gives Rs \(I_2\) in the same years is",
         r"\[ \frac{I_2}{I_1}\times\frac{P_1}{P_2}\times r_1\ \% \]"),
    39: (r"A sum becomes \(n\) times itself at \(r\%\) per annum simple interest in (and, turned round, in \(t\) years at the rate)",
         r"\[ t = \frac{n-1}{r}\times 100\ \text{years},\qquad r = \frac{n-1}{t}\times 100\ \% \]"),
}
PICK = {
    796: (F(1, 5), 3, F(2, 5), 9, 2, 465, 9300), "r34_e1": (F(1, 2), 11, F(1, 4), 8, 12, 1218, 11600), "r34_e2": (F(1, 4), 4, F(1, 2), 14, 8, 1110, 11100),
    "r34_e3": (F(2, 5), 9, F(3, 8), 8, 14, 1092, 11200), "r34_e4": (F(1, 3), 8, F(1, 4), 2, 3, 636, 14400), "r34_e5": (F(3, 10), 2, F(1, 2), 7, 3, 1410, 30000),
    "r34_e6": (F(1, 5), 11, F(3, 5), 12, 9, 2, 3136, 14000),
    797: (5300, 1325, 5), "r35_e1": (5150, 3296, 8), "r35_e2": (9975, 399, 2), "r35_e3": (5075, 1827, 6), "r35_e4": (2100, 1701, 9), "r35_e5": (10000, 19600, 14),
    "r36_e0": (6, 4, 3264, 16864), "r36_e1": (10, F(17, 2), 6545, 14245), "r36_e2": (2, 5, 1390, 15290), "r36_e3": (8, 5, 6060, 21210),
    "r36_e4": (4, F(13, 2), 1807, 8757),
    798: (1100, F(15, 2), 3500, 4, 445, 2), "r37_e1": (3700, 8, 1200, 6, 5336, F(29, 2)), "r37_e2": (300, 4, 3050, 6, 650, F(10, 3)),
    "r37_e3": (2700, 7, 4450, 10, 9510, 15), "r37_e4": (3750, F(19, 2), 1250, F(7, 2), 2000, 5), "r37_e5": (3350, F(17, 2), 900, F(13, 2), 1373, 4),
    799: (4700, 12, 4512, 3520, 4400, 10), "r38_e1": (4000, 2, 240, 5076, 9400, 18), "r38_e2": (10000, 5, 4000, 4176, 8700, 6),
    "r38_e3": (2900, 8, 1624, 2520, 2400, 15), "r38_e4": (3400, 9, 2142, 3528, 8400, 6), "r38_e5": (9600, 15, 5760, 3132, 8700, 9),
    800: (8, F(25, 2)), "r39_e1": (25, 4), "r39_e2": (32, F(25, 4)), "r39_e3": (20, 10), "r39_e4": (16, F(25, 4)),
}


def n_(r, v, trad, ident, sub, unit=""):
    return num(r, v, trad, ident, sub, unit, TH)


# ---------- Rule 34
def r34(f1, r1, f2, r2, r3, *rest):
    (t, A, want) = (1, *rest) if len(rest) == 2 else rest
    f1, r1, f2, r2, r3, t, A = map(F, (f1, r1, f2, r2, r3, t, A))
    f3 = 1 - f1 - f2
    w = f1 * r1 + f2 * r2 + f3 * r3                  # yearly interest on Rs 100
    yearly = A / t
    v = 100 * yearly / w
    assert v == want
    first = "" if t == 1 else rf"In one year the interest is \({nf(A)} \div {nf(t)} = {nf(yearly)}\). "
    trad = [("Yearly interest on Rs 100.", first + rf"The rest is \(1 - {frc(f1)} - {frc(f2)} = {frc(f3)}\). Rs \(100\) earns "
                                           rf"\({frc(f1)}\times {nf(r1)} + {frc(f2)}\times {nf(r2)} + {frc(f3)}\times {nf(r3)} = {nf(w)}\) a year."),
            ("Scale up.", rf"\[ 100\times\frac{{{nf(yearly)}}}{{{nf(w)}}} = {nf(v)} \]")]
    return n_(34, v, trad, rf"\(\frac{{1}}{{n_1}} = {frc(f1)}, x_1 = {nf(r1)}\); \(\frac{{1}}{{n_2}} = {frc(f2)}, x_2 = {nf(r2)}\); \(\frac{{1}}{{n_3}} = {frc(f3)}, x_3 = {nf(r3)}\); "
                                   rf"\(A = {nf(yearly)}\).",
              rf"\[ \frac{{{nf(yearly)}\times 100}}{{{frc(f1 * r1)} + {frc(f2 * r2)} + {frc(f3 * r3)}}} = \frac{{{nf(100 * yearly)}}}{{{nf(w)}}} = {nf(v)} \]", "Rs")


# ---------- Rule 35
def r35(P, I, want):
    P, I = F(P), F(I)
    sq = 100 * I / P
    v = F(isqrt(sq.numerator), isqrt(sq.denominator))
    assert v * v == sq and v == want
    trad = [("Write the interest.", rf"With rate \(r\%\) for \(r\) years: \(\frac{{{nf(P)}\times r\times r}}{{100}} = {nf(I)}\)."),
            ("Solve.", rf"\(r^{{2}} = \frac{{{nf(I)}\times 100}}{{{nf(P)}}} = {nf(sq)}\), so \(r = {nf(v)}\).")]
    return n_(35, v, trad, rf"\(P = {nf(P)}\), \(I = {nf(I)}\).", rf"\[ \sqrt{{\frac{{100\times {nf(I)}}}{{{nf(P)}}}}} = \sqrt{{{nf(sq)}}} = {nf(v)}\% \]", "%")


# ---------- Rule 36
def r36(r, t, I, want):
    r, t, I = map(F, (r, t, I))
    P = 100 * I / (r * t)
    v = I * (1 + 100 / (r * t))
    assert v == P + I == want
    trad = [("The sum borrowed.", rf"Rs \(100\) earns \({nf(r)}\times {nf(t)} = {nf(r * t)}\) in \({nf(t)}\) years, so the sum is \(\frac{{{nf(I)}\times 100}}{{{nf(r * t)}}} = {nf(P)}\)."),
            ("Amount.", rf"\[ {nf(P)} + {nf(I)} = {nf(v)} \]")]
    return n_(36, v, trad, rf"\(r = {nf(r)}\), \(t = {nf(t)}\), \(I = {nf(I)}\).",
              rf"\[ {nf(I)}\left(1 + \frac{{100}}{{{nf(r)}\times {nf(t)}}}\right) = {nf(I)}\times {nf(1 + 100 / (r * t))} = {nf(v)} \]", "Rs")


# ---------- Rule 37
def r37(P1, t1, P2, t2, I, want):
    P1, t1, P2, t2, I = map(F, (P1, t1, P2, t2, I))
    base = P1 * t1 + P2 * t2
    v = 100 * I / base
    assert v == want
    trad = [("Interest at 1%.", rf"At \(1\%\) the loans would earn \(\frac{{{nf(P1)}\times {nf(t1)}}}{{100}} + \frac{{{nf(P2)}\times {nf(t2)}}}{{100}} = {nf(base / 100)}\)."),
            ("Rate.", rf"\[ {nf(I)} \div {nf(base / 100)} = {nf(v)} \]")]
    return n_(37, v, trad, rf"\(P_1 = {nf(P1)}\), \(t_1 = {nf(t1)}\), \(P_2 = {nf(P2)}\), \(t_2 = {nf(t2)}\), \(I = {nf(I)}\).",
              rf"\[ \frac{{100\times {nf(I)}}}{{{nf(P1)}\times {nf(t1)} + {nf(P2)}\times {nf(t2)}}} = \frac{{{nf(100 * I)}}}{{{nf(base)}}} = {nf(v)}\% \]", "%")


# ---------- Rule 38
def r38(P1, r1, I1, I2, P2, want):
    P1, r1, I1, I2, P2 = map(F, (P1, r1, I1, I2, P2))
    t = 100 * I1 / (P1 * r1)
    v = 100 * I2 / (P2 * t)
    assert v == I2 / I1 * P1 / P2 * r1 == want
    trad = [("Number of years.", rf"\(\frac{{{nf(I1)}\times 100}}{{{nf(P1)}\times {nf(r1)}}} = {nf(t)}\) years."),
            ("New rate.", rf"\[ \frac{{{nf(I2)}\times 100}}{{{nf(P2)}\times {nf(t)}}} = {nf(v)}\% \]")]
    return n_(38, v, trad, rf"\(P_1 = {nf(P1)}\), \(r_1 = {nf(r1)}\), \(I_1 = {nf(I1)}\), \(I_2 = {nf(I2)}\), \(P_2 = {nf(P2)}\).",
              rf"\[ \frac{{{nf(I2)}}}{{{nf(I1)}}}\times\frac{{{nf(P1)}}}{{{nf(P2)}}}\times {nf(r1)} = {nf(v)}\% \]", "%")


# ---------- Rule 39
WORD = {2: "double", 3: "treble"}


def r39_time(n, r, want):
    n, r = F(n), F(r)
    v = (n - 1) * 100 / r
    assert v == want
    trad = [("Take the sum as Rs 100.", rf"To {WORD[int(n)]} itself it must earn \({nf(100 * (n - 1))}\) as interest; it earns \({nf(r)}\) a year."),
            ("Years.", rf"\[ {nf(100 * (n - 1))} \div {nf(r)} = {nf(v)} \]")]
    return n_(39, v, trad, rf"\(n = {nf(n)}\), \(r = {nf(r)}\).", rf"\[ \frac{{{nf(n)}-1}}{{{nf(r)}}}\times 100 = {nf(v)} \]", "years")


def r39_rate(n, t, want):
    n, t = F(n), F(t)
    v = (n - 1) * 100 / t
    assert v == want
    trad = [("Take the sum as Rs 100.", rf"To {WORD[int(n)]} itself it must earn \({nf(100 * (n - 1))}\) in \({nf(t)}\) years."),
            ("Rate.", rf"\[ {nf(100 * (n - 1))} \div {nf(t)} = {nf(v)} \]a year on Rs \(100\), i.e. \({nf(v)}\%\).")]
    return n_(39, v, trad, rf"\(n = {nf(n)}\), \(t = {nf(t)}\).", rf"\[ \frac{{{nf(n)}-1}}{{{nf(t)}}}\times 100 = {nf(v)}\% \]", "%")


C = card
CARDS = {
    34: C(34, "Capital in Three Parts", r"Add the yearly interest that Rs 100 of the capital earns from its three parts.",
          r"\[ \frac{A\times 100}{\frac{x_1}{n_1}+\frac{x_2}{n_2}+\frac{x_3}{n_3}} \]",
          [("Part 1", r"\frac{1}{n_1}\ \text{at}\ x_1\%"), ("Part 2", r"\frac{1}{n_2}\ \text{at}\ x_2\%"), ("Rest", r"\frac{1}{n_3} = 1 - \frac{1}{n_1} - \frac{1}{n_2}\ \text{at}\ x_3\%")],
          r"The bottom line is the yearly interest on Rs 100; divide the income for several years by the years first.",
          "'A man invested 1/n1 of his capital at x1%, 1/n2 at x2% and the rest at x3%; his yearly income is Rs A. Find the capital.'",
          r"\(\frac{1}{2}\) at \(6\%\), \(\frac{1}{4}\) at \(8\%\), rest at \(4\%\), Rs \(270\): \(\frac{27000}{3 + 2 + 1} = 4500\).", r"Forgetting to work out the fraction of the rest."),
    35: C(35, "Years Equal to Rate (Interest Given)", r"With \(t = r\), \(SI = \frac{Pr^{2}}{100}\).", r"\[ \sqrt{\frac{100\times I}{P}} \]",
          [("Condition", r"t = r"), ("Interest", r"\frac{Pr^{2}}{100} = I"), ("Rate", r"\sqrt{\frac{100I}{P}}")],
          r"Rule 4 is the same idea with the interest given as a fraction of the sum.", "'The SI on Rs P is Rs I and the number of years equals the rate per cent; find the rate.'",
          r"Rs \(1200\), interest Rs \(300\): \(\sqrt{25} = 5\%\) (and \(5\) years).", r"Forgetting the square root."),
    36: C(36, "Amount From the Interest", r"From the interest find the sum, then add the interest back.", r"\[ A = I\left(1+\frac{100}{rt}\right) \]",
          [("Sum", r"\frac{100I}{rt}"), ("Interest", r"I"), ("Amount", r"\frac{100I}{rt} + I")],
          r"\(\frac{100}{rt}\) is how many times the interest the sum is.", "'A sum is borrowed at r% for t years; the interest is Rs I. Find the amount to be paid.'",
          r"\(5\%\) for \(4\) years, interest Rs \(300\): \(300\left(1 + 5\right) = 1800\).", r"Giving only the sum, without the interest."),
    37: C(37, "Two Loans, One Rate", r"At \(1\%\) the loans earn \(\frac{P_1t_1 + P_2t_2}{100}\); the actual interest is that many times the rate.",
          r"\[ \frac{100I}{P_1t_1+P_2t_2}\ \% \]",
          [("Loan 1", r"P_1\ \text{for}\ t_1"), ("Loan 2", r"P_2\ \text{for}\ t_2"), ("Rate", r"\frac{100I}{P_1t_1+P_2t_2}")],
          r"Each loan counts as principal times years ('rupee-years').", "'A lends Rs P1 for t1 years and Rs P2 for t2 years and receives Rs I as interest in all; find the rate.'",
          r"Rs \(800\) for \(3\) years and Rs \(500\) for \(2\) years, Rs \(204\): \(\frac{20400}{3400} = 6\%\).", r"Adding the sums and the years separately."),
    38: C(38, "Same Years, New Sum and Interest", r"The first deposit fixes the number of years; the new rate follows.", r"\[ \frac{I_2}{I_1}\times\frac{P_1}{P_2}\times r_1\ \% \]",
          [("Years", r"t = \frac{100I_1}{P_1r_1}"), ("New rate", r"\frac{100I_2}{P_2t}"), ("Together", r"\frac{I_2}{I_1}\cdot\frac{P_1}{P_2}\cdot r_1")],
          r"Interest is in proportion to principal times rate when the time is the same.", "'Rs P1 at r1% gives Rs I1 in some years; what rate gives Rs I2 on Rs P2 in the same years?'",
          r"Rs \(2000\) at \(5\%\) gives Rs \(300\); Rs \(600\) on Rs \(1500\): \(\frac{600}{300}\times\frac{2000}{1500}\times 5 = 13\frac{1}{3}\%\).",
          r"Turning one of the fractions upside down."),
    39: C(39, "n Times at a Given Rate", r"Becoming \(n\) times itself means earning \((n-1)\) times the sum as interest.", r"\[ t = \frac{n-1}{r}\times 100 \]",
          [("Double", r"n = 2:\ t = \frac{100}{r}"), ("Treble", r"n = 3:\ t = \frac{200}{r}"), ("Rate", r"r = \frac{100(n-1)}{t}")],
          r"Rule 9 gives the same result; here the time is the usual thing asked.", "'In what time will a sum double / treble itself at r%?' / 'At what rate will it double in t years?'",
          r"Treble at \(8\%\): \(\frac{2}{8}\times 100 = 25\) years.", r"Using \(n\) instead of \(n - 1\)."),
}


def q(k):
    return SENT[k][1](*PICK[k][:NVIS[SENT[k][0]]])


def fn_for(k):
    pool, p = SENT[k][0], PICK[k]
    return {"34": lambda: r34(*p), "34t": lambda: r34(*p), "35": lambda: r35(*p), "36": lambda: r36(*p), "37": lambda: r37(*p), "38": lambda: r38(*p),
            "39t2": lambda: r39_time(2, *p), "39t3": lambda: r39_time(3, *p), "39r2": lambda: r39_rate(2, *p), "39r3": lambda: r39_rate(3, *p)}[pool]


KIND = {"34": "Rs", "34t": "Rs", "35": "%", "36": "Rs", "37": "%", "38": "%", "39t2": "years", "39t3": "years", "39r2": "%", "39r3": "%"}
OLD_RULE = {796: 34, 797: 35, 798: 37, 799: 38, 800: 39}
OLD = {rid: (rule, q(rid), fn_for(rid), KIND[SENT[rid][0]]) for rid, rule in OLD_RULE.items()}
NEW = {}
for k in SENT:
    if isinstance(k, str):
        rule = int(k[1:k.index("_")])
        NEW.setdefault(rule, []).append((k, q(k), fn_for(k), KIND[SENT[k][0]], None))

if __name__ == "__main__":
    gen_1_6.main(OLD, NEW, CARDS, range(34, 40))
