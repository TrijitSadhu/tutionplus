"""Simple Interest Rules 1-6 (2026-10-30). Rule 1: SI = PRT/100 and its three turn-rounds (principal, rate, time). Rule 2: the time
changes - SI1 - SI2 = Pr(t1 - t2)/100. Rule 3: two deposits at two rates - the rate on the whole is (x1 r1 + x2 r2)/(x1 + x2). Rule 4:
SI = P/n and years = rate - rate = sqrt(100/n) %. Rule 5: the principal changes - (P1 - P2)rt/100. Rule 6: the rate changes -
P(r1 - r2)t/100. Writes the six cards, regenerates the old rows 759-768 (764's key was 0.5% for a question that gives 0.05%) and adds
the book's exercises with no copy. Also holds the shared main() / build_opts() for the later Simple Interest batches.
Usage: python gen_1_6.py"""
import json, os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from fmt import M, UU, answer_json, nf, opts, pair_opts, ratio_opts, terms_opts, triple_opts  # noqa: E402
from helpers import place, result  # noqa: E402

TH = {
    1: (r"The simple interest on a principal \(P\) at \(R\%\) per annum for \(T\) years is \(SI = \frac{PRT}{100}\); turned round,",
        r"\[ P = \frac{100\,SI}{RT},\qquad R = \frac{100\,SI}{PT},\qquad T = \frac{100\,SI}{PR} \]"),
    2: (r"When only the time changes from \(t_2\) to \(t_1\), the change in the simple interest is", r"\[ SI_1 - SI_2 = \frac{P\times r\times (t_1-t_2)}{100} \]"),
    3: (r"If Rs \(x_1\) is put at \(r_1\%\) and Rs \(x_2\) at \(r_2\%\) per annum, the rate of interest on the whole sum is", r"\[ \frac{x_1r_1+x_2r_2}{x_1+x_2}\% \]"),
    4: (r"If the simple interest on a sum is \(\frac{1}{n}\) of the sum and the number of years equals the rate per cent, the rate (and the time) is",
        r"\[ \sqrt{100\times\frac{1}{n}}\ \% \]"),
    5: (r"When only the principal changes from \(P_2\) to \(P_1\), the change in the simple interest is", r"\[ SI_1 - SI_2 = \frac{(P_1-P_2)\times r\times t}{100} \]"),
    6: (r"When only the rate changes from \(r_2\) to \(r_1\), the change in the simple interest is", r"\[ SI_1 - SI_2 = \frac{P\times (r_1-r_2)\times t}{100} \]"),
}


def T_(r, th=TH):
    return th[r][0] + "<br>" + th[r][1]


def done(r, ans, fin, trad, ident, sub, th=TH):
    rs = steps(("Identify the values.", ident), ("Apply the specified rule.", th[r][1]), ("Substitute the values.", sub))
    return result(ans, T_(r, th), steps(*trad), rs, fin, [ident, "Answer " + fin + "."], sub)


def num(r, v, trad, ident, sub, unit="", th=TH):
    return done(r, ("number", F(v)), UU(v, unit) if unit != "%" else M(nf(v) + r"\%"), trad, ident, sub, th)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def yrs(t):
    """years written for a step: 3, 2\\frac{1}{2}."""
    return nf(t)


# ---------- Rule 1
def r1_interest(P, R, T, how=""):
    P, R, T = map(F, (P, R, T))
    one = P * R / 100
    v = one * T
    trad = [("Interest for one year.", (how + " " if how else "") + rf"\(\frac{{{nf(R)}}}{{100}}\times {nf(P)} = {nf(one)}\)."),
            ("Interest for the whole time.", rf"\[ {nf(one)}\times {yrs(T)} = {nf(v)} \]")]
    return num(1, v, trad, rf"\(P = {nf(P)}\), \(R = {nf(R)}\), \(T = {yrs(T)}\).", rf"\[ SI = \frac{{{nf(P)}\times {nf(R)}\times {yrs(T)}}}{{100}} = {nf(v)} \]", "Rs"), (one, v)


def r1_si(P, R, T, how=""):
    return r1_interest(P, R, T, how)[0]


def r1_both(P, R, T):
    g, (one, v) = r1_interest(P, R, T)
    A = F(P) + v
    g2 = done(1, ("pair", (v, A)), f"interest Rs {M(nf(v))}, amount Rs {M(nf(A))}",
              [("Interest for one year.", rf"\(\frac{{{nf(R)}}}{{100}}\times {nf(P)} = {nf(one)}\)."),
               ("Interest and amount.", rf"Interest \(= {nf(one)}\times {yrs(F(T))} = {nf(v)}\); amount \(= {nf(P)} + {nf(v)} = {nf(A)}\).")],
              rf"\(P = {nf(P)}\), \(R = {nf(R)}\), \(T = {yrs(F(T))}\).", rf"\[ SI = \frac{{{nf(P)}\times {nf(R)}\times {yrs(F(T))}}}{{100}} = {nf(v)},\quad A = {nf(A)} \]")
    return g2


def r1_settle(P, R, T, cash, thing):
    P, R, T, cash = map(F, (P, R, T, cash))
    I = P * R * T / 100
    v = P + I - cash
    trad = [("What he owed.", rf"Interest \(= \frac{{{nf(R)}}}{{100}}\times {nf(P)}\times {yrs(T)} = {nf(I)}\); amount \(= {nf(P)} + {nf(I)} = {nf(P + I)}\)."),
            (f"Value of the {thing}.", rf"\[ {nf(P + I)} - {nf(cash)} = {nf(v)} \]")]
    return num(1, v, trad, rf"\(P = {nf(P)}\), \(R = {nf(R)}\), \(T = {yrs(T)}\), cash Rs \({nf(cash)}\).",
               rf"\[ SI = \frac{{{nf(P)}\times {nf(R)}\times {yrs(T)}}}{{100}} = {nf(I)};\quad {nf(P + I)} - {nf(cash)} = {nf(v)} \]", "Rs")


def r1_principal(I, R, T):
    I, R, T = map(F, (I, R, T))
    v = 100 * I / (R * T)
    trad = [("Interest on Rs 100.", rf"Rs \(100\) earns \({nf(R)}\times {yrs(T)} = {nf(R * T)}\) in \({yrs(T)}\) years."),
            ("Scale up.", rf"To earn \({nf(I)}\): \[ 100\times\frac{{{nf(I)}}}{{{nf(R * T)}}} = {nf(v)} \]")]
    return num(1, v, trad, rf"\(SI = {nf(I)}\), \(R = {nf(R)}\), \(T = {yrs(T)}\).", rf"\[ P = \frac{{100\times {nf(I)}}}{{{nf(R)}\times {yrs(T)}}} = {nf(v)} \]", "Rs")


def r1_rate(P, I, T, amount=None):
    P, T = F(P), F(T)
    I = F(amount) - P if amount is not None else F(I)
    v = 100 * I / (P * T)
    first = (rf"Interest \(= {nf(amount)} - {nf(P)} = {nf(I)}\). " if amount is not None else "")
    trad = [("Interest for one year.", first + rf"In one year: \({nf(I)} \div {yrs(T)} = {nf(I / T)}\)."),
            ("As a per cent of the sum.", rf"\[ \frac{{{nf(I / T)}}}{{{nf(P)}}}\times 100 = {nf(v)}\% \]")]
    return num(1, v, trad, rf"\(P = {nf(P)}\), \(SI = {nf(I)}\), \(T = {yrs(T)}\).", rf"\[ R = \frac{{100\times {nf(I)}}}{{{nf(P)}\times {yrs(T)}}} = {nf(v)}\% \]", "%")


def r1_time(P, R, I=None, amount=None):
    P, R = F(P), F(R)
    I = F(amount) - P if amount is not None else F(I)
    one = P * R / 100
    v = I / one
    first = (rf"Interest \(= {nf(amount)} - {nf(P)} = {nf(I)}\). " if amount is not None else "")
    trad = [("Interest for one year.", first + rf"One year gives \(\frac{{{nf(R)}}}{{100}}\times {nf(P)} = {nf(one)}\)."),
            ("Number of years.", rf"\[ {nf(I)} \div {nf(one)} = {nf(v)} \]")]
    return num(1, v, trad, rf"\(P = {nf(P)}\), \(R = {nf(R)}\), \(SI = {nf(I)}\).", rf"\[ T = \frac{{100\times {nf(I)}}}{{{nf(P)}\times {nf(R)}}} = {nf(v)} \]", "years")


def r1_xyz():
    trad = [("Write the interest.", r"\(\frac{P\times x\times x}{100} = x\)."), ("Solve for P.", r"\(Px = 100\), so \(P = \frac{100}{x}\).")]
    return done(1, ("expr", F(100, 7)), M(r"\frac{100}{x}"), trad, r"\(SI = x\), \(R = x\), \(T = x\).", r"\[ P = \frac{100\times x}{x\times x} = \frac{100}{x} \]")


def r1_daily(per_day, R):
    per_day, R = F(per_day), F(R)
    v = per_day * 365 * 100 / R
    trad = [("Interest in a year.", rf"Rs \({nf(per_day)}\) a day is \({nf(per_day)}\times 365 = {nf(per_day * 365)}\) a year."),
            ("The sum.", rf"At \({nf(R)}\%\) that is earned by \(\frac{{{nf(per_day * 365)}\times 100}}{{{nf(R)}}} = {nf(v)}\).")]
    return num(1, v, trad, rf"\(SI = {nf(per_day * 365)}\) for \(T = 1\), \(R = {nf(R)}\).", rf"\[ P = \frac{{100\times {nf(per_day * 365)}}}{{{nf(R)}\times 1}} = {nf(v)} \]", "Rs")


# ---------- Rules 2, 5, 6
def r2(P, dI, dT):
    P, dI, dT = map(F, (P, dI, dT))
    v = 100 * dI / (P * dT)
    trad = [("Extra interest a year.", rf"The extra \({nf(dI)}\) comes from \({nf(dT)}\) more years: \({nf(dI / dT)}\) a year."),
            ("Rate.", rf"\[ \frac{{{nf(dI / dT)}}}{{{nf(P)}}}\times 100 = {nf(v)}\% \]")]
    return num(2, v, trad, rf"\(P = {nf(P)}\), \(SI_1 - SI_2 = {nf(dI)}\), \(t_1 - t_2 = {nf(dT)}\).", rf"\[ {nf(dI)} = \frac{{{nf(P)}\times r\times {nf(dT)}}}{{100}} \Rightarrow r = {nf(v)}\% \]", "%")


def r5(P1, P2, dI, t):
    P1, P2, dI, t = map(F, (P1, P2, dI, t))
    v = 100 * dI / ((P1 - P2) * t)
    trad = [("Where the extra interest comes from.", rf"Only the extra Rs \({nf(P1 - P2)}\) of principal makes the difference: it earns \({nf(dI)}\) in \({nf(t)}\) years."),
            ("Rate.", rf"\[ \frac{{{nf(dI)}\times 100}}{{{nf(P1 - P2)}\times {nf(t)}}} = {nf(v)}\% \]")]
    return num(5, v, trad, rf"\(P_1 - P_2 = {nf(P1 - P2)}\), \(SI_1 - SI_2 = {nf(dI)}\), \(t = {nf(t)}\).", rf"\[ {nf(dI)} = \frac{{{nf(P1 - P2)}\times r\times {nf(t)}}}{{100}} \Rightarrow r = {nf(v)}\% \]", "%")


def r6_time(P, dI, dR):
    P, dI, dR = map(F, (P, dI, dR))
    v = 100 * dI / (P * dR)
    trad = [("Extra interest a year.", rf"The extra \({nf(dR)}\%\) on Rs \({nf(P)}\) gives \({nf(P * dR / 100)}\) a year."),
            ("Years.", rf"\[ {nf(dI)} \div {nf(P * dR / 100)} = {nf(v)} \]")]
    return num(6, v, trad, rf"\(P = {nf(P)}\), \(SI_1 - SI_2 = {nf(dI)}\), \(r_1 - r_2 = {nf(dR)}\).", rf"\[ {nf(dI)} = \frac{{{nf(P)}\times {nf(dR)}\times t}}{{100}} \Rightarrow t = {nf(v)} \]", "years")


def r6_rates(P, t, dI):
    P, t, dI = map(F, (P, t, dI))
    v = 100 * dI / (P * t)
    trad = [("Difference a year.", rf"The two interests differ by \({nf(dI)}\) in \({nf(t)}\) years: \({nf(dI / t)}\) a year."),
            ("Difference of rates.", rf"\[ \frac{{{nf(dI / t)}}}{{{nf(P)}}}\times 100 = {nf(v)}\% \]")]
    return num(6, v, trad, rf"\(P = {nf(P)}\), \(t = {nf(t)}\), \(SI_1 - SI_2 = {nf(dI)}\).", rf"\[ r_1 - r_2 = \frac{{100\times {nf(dI)}}}{{{nf(P)}\times {nf(t)}}} = {nf(v)}\% \]", "%")


# ---------- Rules 3 and 4
def r3_rate(x1, r1, x2, r2):
    x1, r1, x2, r2 = map(F, (x1, r1, x2, r2))
    v = (x1 * r1 + x2 * r2) / (x1 + x2)
    trad = [("Interest for one year.", rf"\(\frac{{{nf(r1)}}}{{100}}\times {nf(x1)} + \frac{{{nf(r2)}}}{{100}}\times {nf(x2)} = {nf(x1 * r1 / 100)} + {nf(x2 * r2 / 100)} = {nf((x1 * r1 + x2 * r2) / 100)}\)."),
            ("As a per cent of the whole.", rf"\[ \frac{{{nf((x1 * r1 + x2 * r2) / 100)}}}{{{nf(x1 + x2)}}}\times 100 = {nf(v)}\% \]")]
    return num(3, v, trad, rf"\(x_1 = {nf(x1)}\), \(r_1 = {nf(r1)}\), \(x_2 = {nf(x2)}\), \(r_2 = {nf(r2)}\).",
               rf"\[ \frac{{{nf(x1)}\times {nf(r1)} + {nf(x2)}\times {nf(r2)}}}{{{nf(x1)}+{nf(x2)}}} = {nf(v)}\% \]", "%")


def r3_total(x1, r1, r2, avg):
    x1, r1, r2, avg = map(F, (x1, r1, r2, avg))
    x2 = x1 * (avg - r1) / (r2 - avg)
    v = x1 + x2
    trad = [("Let the second amount be y.", rf"One year's interest: \(\frac{{{nf(r1)}}}{{100}}\times {nf(x1)} + \frac{{{nf(r2)}}}{{100}}y = \frac{{{nf(avg)}}}{{100}}({nf(x1)} + y)\)."),
            ("Solve.", rf"\({nf(r2 - avg)}y = {nf(x1)}\times {nf(avg - r1)}\), so \(y = {nf(x2)}\); total \(= {nf(v)}\).")]
    return num(3, v, trad, rf"\(x_1 = {nf(x1)}\), \(r_1 = {nf(r1)}\), \(r_2 = {nf(r2)}\), whole rate \({nf(avg)}\%\).",
               rf"\[ {nf(avg)} = \frac{{{nf(x1)}\times {nf(r1)} + {nf(r2)}x_2}}{{{nf(x1)}+x_2}} \Rightarrow x_2 = {nf(x2)} \]Total \(= {nf(v)}\).", "Rs")


def r4(a, b):
    """SI = a/b of the sum; years = rate."""
    f = F(a, b)
    sq = 100 * f
    v = F(isqrt(sq.numerator), isqrt(sq.denominator))
    assert v * v == sq
    trad = [("Write the interest.", rf"With rate \(r\%\) for \(r\) years: \(\frac{{P\times r\times r}}{{100}} = {frc(f)}P\)."),
            ("Solve.", rf"\(r^{{2}} = 100\times {frc(f)} = {frc(sq)}\), so \(r = {frc(v)}\).")]
    return num(4, v, trad, rf"\(\frac{{1}}{{n}} = {frc(f)}\).", rf"\[ \sqrt{{100\times {frc(f)}}} = \sqrt{{{frc(sq)}}} = {frc(v)}\% \]", "%")


C = card
CARDS = {
    1: C(1, "Simple Interest", r"Interest grows by the same amount every year: \(\frac{R}{100}\) of the principal.", r"\[ SI = \frac{P\times R\times T}{100} \]",
         [("One year", r"\frac{PR}{100}"), ("T years", r"\frac{PRT}{100}"), ("Amount", r"P + SI")],
         r"Any one of \(P, R, T, SI\) follows from the other three: \(P = \frac{100SI}{RT}\), \(R = \frac{100SI}{PT}\), \(T = \frac{100SI}{PR}\). Write months and days as years.",
         "'Find the simple interest on Rs P for T years at R%' / 'what sum / rate / time ...'.",
         r"Rs \(500\) at \(8\%\) for \(3\) years: \(\frac{500\times 8\times 3}{100} = 120\).", r"Using the amount where the interest is meant."),
    2: C(2, "Change in Time", r"Only the extra years make the extra interest.", r"\[ SI_1 - SI_2 = \frac{Pr(t_1-t_2)}{100} \]",
         [("Extra years", r"t_1 - t_2"), ("Extra interest", r"SI_1 - SI_2"), ("Rate", r"\frac{100(SI_1-SI_2)}{P(t_1-t_2)}")],
         r"The interest for the years both have in common cancels out.", "'If the simple interest on Rs P increases by Rs d when the time increases by n years, find the rate.'",
         r"Rs \(1000\), Rs \(30\) more for \(2\) more years: \(1.5\%\).", r"Using the whole time instead of the extra time."),
    3: C(3, "Rate on Two Deposits Together", r"Add the interest of one year from both deposits and compare it with the whole sum.", r"\[ \frac{x_1r_1+x_2r_2}{x_1+x_2}\% \]",
         [("Deposit 1", r"x_1\ \text{at}\ r_1"), ("Deposit 2", r"x_2\ \text{at}\ r_2"), ("Whole", r"\frac{x_1r_1+x_2r_2}{x_1+x_2}")],
         r"It is a weighted average of the two rates; it lies between them, nearer the rate of the bigger deposit.",
         "'A man deposits Rs x1 at r1% and Rs x2 at r2%; find the rate on the whole sum' / 'find the total invested'.",
         r"Rs \(1000\) at \(5\%\), Rs \(3000\) at \(9\%\): \(\frac{5000+27000}{4000} = 8\%\).", r"Taking the plain average of the two rates."),
    4: C(4, "Rate Equal to Time", r"When the years equal the rate, \(SI = \frac{Pr^{2}}{100}\).", r"\[ \sqrt{100\times\frac{1}{n}}\% \]",
         [("Condition", r"T = R = r"), ("Interest", r"\frac{Pr^{2}}{100} = \frac{P}{n}"), ("Rate", r"r = \sqrt{\frac{100}{n}}")],
         r"The time in years is the same number as the rate.", "'The simple interest is 1/n of the principal and the number of years equals the rate per cent; find the rate.'",
         r"Interest \(\frac{1}{4}\) of the sum: \(r = \sqrt{25} = 5\%\) (and \(5\) years).", r"Forgetting the square root."),
    5: C(5, "Change in Principal", r"Only the extra principal makes the extra interest.", r"\[ SI_1 - SI_2 = \frac{(P_1-P_2)rt}{100} \]",
         [("Extra principal", r"P_1 - P_2"), ("Extra interest", r"SI_1 - SI_2"), ("Rate", r"\frac{100(SI_1-SI_2)}{(P_1-P_2)t}")],
         r"Same rate and time on both sums, so the difference of interests is the interest on the difference of sums.",
         "'If the simple interest on Rs P1 is more than that on Rs P2 by Rs d in t years, find the rate.'",
         r"Rs \(1500\) and Rs \(1000\), Rs \(50\) more in \(2\) years: \(5\%\).", r"Using one of the two sums instead of their difference."),
    6: C(6, "Change in Rate", r"Only the extra rate makes the extra interest.", r"\[ SI_1 - SI_2 = \frac{P(r_1-r_2)t}{100} \]",
         [("Extra rate", r"r_1 - r_2"), ("Extra interest", r"SI_1 - SI_2"), ("Time", r"\frac{100(SI_1-SI_2)}{P(r_1-r_2)}")],
         r"Two banks giving different rates on the same sum for the same time differ by the interest on the difference of rates.",
         "'If simple interest on Rs P increases by Rs d when the rate increases by x%, find the time.'",
         r"Rs \(2000\), Rs \(40\) more for \(2\%\) more: \(1\) year.", r"Using a whole rate instead of the change in rate."),
}
OLD = {
    759: (1, "A shopkeeper takes a loan of Rs 1475 at 8% per annum. How much simple interest does he pay in 3 years?", lambda: r1_si(1475, 8, 3), "Rs"),
    760: (1, r"A sum lent at \(2\frac{2}{3}\%\) per annum earns Rs 360 as simple interest in \(7\frac{1}{2}\) years. What is the sum?", lambda: r1_principal(360, F(8, 3), F(15, 2)), "Rs"),
    761: (1, "A sum of Rs 937.50 grew to Rs 1000 in 1 year 4 months at simple interest. Find the rate per cent per annum.", lambda: r1_rate(F("937.5"), None, F(4, 3), amount=1000), "%"),
    762: (1, "How many years will it take for Rs 6400 to grow to Rs 9472 at 6% simple interest per year?", lambda: r1_time(6400, 6, amount=9472), "years"),
    763: (1, r"A sum of money earns Rs \(x\) as simple interest in \(x\) years at \(x\%\) per annum. Find the sum.", r1_xyz, "expr"),
    764: (2, "If the simple interest on Rs 1500 rises by Rs 54 when the time is increased by 3 years, find the rate per cent per annum.", lambda: r2(1500, 54, 3), "%"),
    765: (3, "A man puts Rs 2500 in a bank at 6% per annum and Rs 3500 in a post office at 12% per annum. What is the rate of interest on the whole sum?",
          lambda: r3_rate(2500, 6, 3500, 12), "%"),
    766: (4, r"The simple interest on a sum is \(\frac{81}{100}\) of the sum, and the number of years equals the rate per cent per annum. Find the rate.", lambda: r4(81, 100), "%"),
    767: (5, "Two loans of Rs 2600 and Rs 2250 are given at the same rate. In 4 years the first earns Rs 42 more interest than the second. Find the rate per cent per annum.", lambda: r5(2600, 2250, 42, 4), "%"),
    768: (6, "The simple interest on Rs 3500 rises by Rs 105 when the rate goes up by 1.5% per annum. Find the time.", lambda: r6_time(3500, 105, F("1.5")), "years"),
}
NEW = {
    1: [("r1_e1", "A trader borrows Rs 650 for a year at 14% per annum. How much interest does he pay?", lambda: r1_si(650, 14, 1), "Rs", None),
        ("r1_e2", "Rs 2800 is given as a loan at 11% per annum. What is the simple interest after 6 years?", lambda: r1_si(2800, 11, 6), "Rs", None),
        ("r1_e3", r"Kamal borrowed Rs 900 at 8% per annum for \(3\frac{1}{2}\) years. Find the interest and the amount he paid back.", lambda: r1_both(900, 8, F(7, 2)), "pair_rs", None),
        ("r1_e4", r"A potter borrowed Rs 3600 at 15% per annum. At the end of \(1\frac{1}{2}\) years he cleared the debt by paying Rs 2500 and a goat. What was the goat worth?",
         lambda: r1_settle(3600, 15, F(3, 2), 2500, "goat"), "Rs", None),
        ("r1_e5", "How much simple interest does Rs 2190 earn in 73 days at 10% per annum?", lambda: r1_si(2190, 10, F(73, 365), r"\(73\) days \(= \frac{73}{365} = \frac{1}{5}\) year."), "Rs", None),
        ("r1_e6", "A sum earns Rs 210 as simple interest in 3 years at 7% per annum. How big is the sum?", lambda: r1_principal(210, 7, 3), "Rs", None),
        ("r1_e7", "A sum of Rs 640 grew to Rs 1040 in 5 years at simple interest. Find the rate per cent per annum.", lambda: r1_rate(640, None, 5, amount=1040), "%", None),
        ("r1_e8", "How many years will Rs 750 take to grow to Rs 1020 at 6% simple interest per year?", lambda: r1_time(750, 6, amount=1020), "years", None),
        ("r1_e9", "A deposit of Rs 850 becomes Rs 1003 after 2 years of simple interest. At what yearly rate was it kept?", lambda: r1_rate(850, None, 2, amount=1003), "%", None),
        ("r1_e10", "After how many years will Rs 480 at 6% simple interest per year become Rs 624?", lambda: r1_time(480, 6, amount=624), "years", None),
        ("r1_e11", "A farmer borrows Rs 1250 at 7% per annum. What simple interest does he owe after 4 years?", lambda: r1_si(1250, 7, 4), "Rs", None),
        ("r1_e12", "A man puts Rs 900 in a bank at 6% per annum. After how many years will he have earned Rs 216 as interest?", lambda: r1_time(900, 6, I=216), "years", None),
        ("r1_e13", r"The interest on a sum for \(1\frac{2}{3}\) years at \(4\frac{1}{2}\%\) per annum is Rs 135. Find the sum.", lambda: r1_principal(135, F(9, 2), F(5, 3)), "Rs", None),
        ("r1_e14", "P borrowed Rs 6500 from Q at simple interest. After 3 years Q got Rs 1365 more than he had lent. What was the rate of interest?",
         lambda: r1_rate(6500, 1365, 3), "%", None),
        ("r1_e15", "Re 1 grows by Rs 3 of interest in 25 years at simple interest. What is the yearly rate?", lambda: r1_rate(1, 3, 25), "%", None),
        ("r1_e16", "What sum gives Rs 2 as interest every day at 8% per annum simple interest?", lambda: r1_daily(2, 8), "Rs", None)],
    2: [("r2_e1", "If the simple interest on Rs 2400 rises by Rs 36 when the time is increased by 2 years, find the rate per cent per annum.", lambda: r2(2400, 36, 2), "%", None),
        ("r2_e2", "The simple interest on Rs 750 goes up by Rs 45 when the time is made 4 years longer. Find the rate per cent per annum.", lambda: r2(750, 45, 4), "%", None),
        ("r2_e3", "On a deposit of Rs 3200, the simple interest goes up by Rs 96 when the deposit is kept 6 years longer. What is the rate per cent per annum?", lambda: r2(3200, 96, 6), "%", None),
        ("r2_e4", "The simple interest on Rs 260 rises by Rs 39 when the time is increased by 5 years. Find the rate per cent per annum.", lambda: r2(260, 39, 5), "%", None)],
    3: [("r3_e1", "Meena invested Rs 15000 at 8% per annum and another amount at 14% per annum. The interest for one year on the whole was 12% of the total. "
                  "Find the total amount invested.", lambda: r3_total(15000, 8, 14, 12), "Rs", None),
        ("r3_e2", "A trader put Rs 9000 at 6% per annum and some more money at 11% per annum. The interest for one year was 8% of the whole. How much did he invest in all?",
         lambda: r3_total(9000, 6, 11, 8), "Rs", None),
        ("r3_e3", "Rs 4500 is lent at 3.5% per annum and another sum at 6% per annum. The interest for one year on the whole is 4.5% of it. Find the total sum lent.",
         lambda: r3_total(4500, F("3.5"), 6, F("4.5")), "Rs", None),
        ("r3_e4", "A woman puts Rs 1650 in one bank at 7% per annum and Rs 1350 in another at 9% per annum. Find the rate of interest on the whole sum.", lambda: r3_rate(1650, 7, 1350, 9), "%", None),
        ("r3_e5", "Rs 5000 is invested at 12% per annum and Rs 7000 at 13.5% per annum. What is the rate of interest on the whole sum?", lambda: r3_rate(5000, 12, 7000, F("13.5")), "%", None)],
    4: [("r4_e1", r"The simple interest on a sum is \(\frac{4}{25}\) of the sum, and the number of years equals the rate per cent. Find the rate.", lambda: r4(4, 25), "%", None),
        ("r4_e2", r"The interest on a loan is \(\frac{9}{64}\) of the loan, and the rate per cent equals the number of years. What is the rate?", lambda: r4(9, 64), "%", None),
        ("r4_e3", r"The simple interest on a sum is \(\frac{16}{25}\) of the sum, and the years are as many as the rate per cent. Find the rate.", lambda: r4(16, 25), "%", None),
        ("r4_e4", r"A sum earns simple interest equal to \(\frac{49}{100}\) of itself, and the number of years equals the rate per cent. Find the rate.", lambda: r4(49, 100), "%", None),
        ("r4_e5", r"The interest on a sum is \(\frac{1}{36}\) of the sum, and the number of years equals the rate per cent per annum. What is the rate?", lambda: r4(1, 36), "%", None)],
    5: [("r5_e1", "Rs 1950 and Rs 1750 are lent at the same rate for 2 years. The interest on the larger sum is Rs 28 more. Find the rate per cent per annum.", lambda: r5(1950, 1750, 28, 2), "%", None),
        ("r5_e2", "Two deposits of Rs 3480 and Rs 3180 earn simple interest at the same rate. In 4 years the first earns Rs 36 more than the second. What is the rate?", lambda: r5(3480, 3180, 36, 4), "%", None),
        ("r5_e3", "In 3 years the simple interest on Rs 2245 is Rs 45 more than that on Rs 1995. Find the rate per cent per annum.", lambda: r5(2245, 1995, 45, 3), "%", None)],
    6: [("r6_e1", "The simple interest on Rs 640 rises by Rs 48 when the rate goes up by 5% per annum. Find the time.", lambda: r6_time(640, 48, 5), "years", None),
        ("r6_e2", "If the interest on Rs 1600 increases by Rs 96 when the rate is raised by 3% per annum, find the time.", lambda: r6_time(1600, 96, 3), "years", None),
        ("r6_e3", "The simple interest on Rs 450 goes up by Rs 81 when the rate is increased by 6% per annum. For how many years was it lent?", lambda: r6_time(450, 81, 6), "years", None),
        ("r6_e4", "Two banks pay different rates. On Rs 2500 for 3 years, the interests from them differ by Rs 45. What is the difference between their rates?",
         lambda: r6_rates(2500, 3, 45), "%", None)],
}


def pct_opts(v, wrong=None):
    v = F(v)
    f = lambda t: M(nf(t) + r"\%")
    if wrong is None:
        step = F(1) if v >= 2 else F(1, 4) if (v * 4).denominator == 1 else F(1, 10)
        wrong = [v + step, v - step, v + 2 * step] if v - step > 0 else [v + step, v + 2 * step, v + 3 * step]
    return place(f(v), [f(w) for w in wrong])


def build_opts(g, kind, wrong):
    a = g["answer"]
    if kind == "expr":
        return place(M(r"\frac{100}{x}"), [M(r"100x"), M(r"x"), M(r"\frac{100}{x^{2}}")])
    if a[0] == "ratio":
        return ratio_opts(*a[1], wrong)
    if a[0] == "terms":
        return terms_opts(a[1], wrong)
    if a[0] == "pair":
        if kind == "pair_rs":
            x, y = a[1]
            f = lambda p, q: f"interest Rs {M(nf(p))}, amount Rs {M(nf(q))}"
            s = max(1, x // 10)
            return place(f(x, y), [f(x + s, y + s), f(x - s, y - s), f(y, x)])
        return pair_opts(*a[1], "", wrong)
    if a[0] == "triple":
        return triple_opts(*a[1], "", wrong)
    if kind == "%":
        return pct_opts(a[1], wrong)
    return opts(a[1], kind, wrong)


def main(old=OLD, new=NEW, cards=CARDS, rules=range(1, 7), card_ids=None):
    """card_ids: {rule: stored card id} when the rows go onto existing cards (Miscellaneous)."""
    for rule in rules:
        folder = os.path.join(HERE if card_ids is None else os.path.join(HERE, "misc"), f"rule{rule:02d}")
        ids = [rid for rid, v in old.items() if v[0] == rule]
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert (dump["rule_card"] is None) == (card_ids is None)
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(ids), (rule, sorted(rows), ids)
        if ids:
            out = []
            for rid in ids:
                _, q, fn, kind = old[rid]
                g = fn()
                op, _ = build_opts(g, kind, None)
                extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
                extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
                out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}" if card_ids is None else card_ids[rule], extra))
            json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        html = cards[rule] if card_ids is None else dump["rule_card"]["rule_html"]
        cc = {"rule_name": f"Rule {rule}", "rule_html": html}
        if card_ids is None:
            json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, kind, wrong in new.get(rule, []):
            g = fn()
            op, pos = build_opts(g, kind, wrong)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        if qs:
            json.dump({"rules_html": [{"chapter": "simple_interest", **cc}], "questions": qs},
                      open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(ids)} rows regenerated, {len(qs)} new questions")


if __name__ == "__main__":
    main()
