"""Percentage Miscellaneous set (2026-10-30): the 31 Miscellaneous problems at the end of the chapter (book pdf pages 38-42).
18 are in the DB as the old rule-less rows 662-679; each is linked to the card of the rule it uses, rewritten in the simple style
with a new setting and all-new numbers (the gate is on), given Theorem + Traditional Method + Specified Rule, with option e = ''
and no display math in its question or options. The other 13 (M1, M2, M9-M13, M22, M26, M27, M28, M30, M31) are added as new
questions on the same cards (numbers changed; the M9-M13 passage written into each of its five questions). M8 (667), whose
book answer is "Data inadequate", is rewritten into a question with a number for its answer, and M10's numbers are new so its
answer is one of the four options. One folder per linked rule: reword/misc/ruleNN/. Usage: python gen_misc.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, PC)
from common import money as m, new_question, regen_entry  # noqa: E402
from gen_common import place, steps, tex  # noqa: E402
from gen_1_8 import T1, T3, T4, T5, T6, P, Num, Rs, result  # noqa: E402
from gen_17_24 import T17  # noqa: E402
from gen_33_40 import T34, T35, T36, T37  # noqa: E402
from gen_49_56 import T53  # noqa: E402
from gen_73_77 import T74, T75  # noqa: E402

TH = {1: T1, 3: T3, 4: T4, 5: T5, 6: T6, 17: T17, 34: T34, 35: T35, 36: T36, 37: T37, 53: T53, 74: T74, 75: T75}


def R(rule, kind, v, trad, rule_steps, fin, rb, sc):
    return result((kind, v), TH[rule], steps(*trad), steps(*rule_steps), fin, rb, sc)


def apply(rule):
    return ("Apply the specified rule.", TH[rule].split("<br>")[1])


# ---------------------------------------------------------------- builders
def b_spend(x, y, keep, yearly):                         # M3 -> Rule 75
    x, y, keep, yearly = map(F, (x, y, keep, yearly))
    S = yearly / 12
    left = (100 - x) * (100 - y) / 100                    # per cent of income left after the two spends
    inc = S * 100 / (left * keep)
    trad = [("Monthly saving.", rf"\[ {m(yearly)} \div 12 = {m(S)} \]"),
            ("What is left of an income of 100.", rf"After \({tex(x)}\%\): \({tex(100 - x)}\); after \({tex(y)}\%\) of that: \({tex(left)}\); she saves \({tex(keep)}\) of it, i.e. \({tex(left * keep)}\)."),
            ("Income.", rf"\[ {m(S)}\times\frac{{100}}{{{tex(left * keep)}}} = {m(inc)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\); the money left after the two spends is \(\frac{{S}}{{{tex(keep)}}} = {m(S / keep)}\) a month."),
            apply(75), ("Substitute the values.", rf"\[ \frac{{{m(S / keep)}\times 100^2}}{{{tex(100 - x)}\times {tex(100 - y)}}} = {m(inc)} \]")]
    return R(75, "number", inc, trad, rule, Rs(inc), [rf"Saving \(= {m(S)}\) a month.", rf"Left after spending \(= {m(S / keep)}\).", rf"Income \(= {m(inc)}\)."],
             rf"\[ \frac{{{m(S / keep)}\times 100^2}}{{{tex(100 - x)}\times {tex(100 - y)}}} = {m(inc)} \]")


def b_shares(x, k, spent, left):                         # M4 -> Rule 17
    x, k, spent, left = map(F, (x, k, spent, left))
    got = spent + left
    A = got * k * 100 / x
    trad = [("What the last person got.", rf"\({m(spent)} + {m(left)} = {m(got)}\)."),
            ("Go back one step.", rf"That is \(\frac{{1}}{{{tex(k)}}}\) of the second person's share: \({m(got)}\times {tex(k)} = {m(got * k)}\)."),
            ("Go back again.", rf"That is \({tex(x)}\%\) of the first amount: \[ {m(got * k)}\times\frac{{100}}{{{tex(x)}}} = {m(A)} \]")]
    rule = [("Identify the values.", rf"The shares taken are \({tex(x)}\%\) and then \(\frac{{1}}{{{tex(k)}}}\); \(A = {m(got)}\) is what the last share was."),
            apply(17), ("Substitute the values.", rf"\[ {m(got)}\times {tex(k)}\times\frac{{100}}{{{tex(x)}}} = {m(A)} \]")]
    return R(17, "number", A, trad, rule, Rs(A), [rf"Last share \(= {m(got)}\).", rf"Second share \(= {m(got * k)}\).", rf"First amount \(= {m(A)}\)."],
             rf"\[ {m(got)}\times {tex(k)}\times\frac{{100}}{{{tex(x)}}} = {m(A)} \]")


def b_test(p, first, right, a, b):                       # M5 -> Rule 4
    p, first, right, a, b = map(F, (p, first, right, a, b))
    kq = (p / 100 * first - right) / (F(a) / b - p / 100) / b   # number of blocks of b
    rest = kq * b
    N = first + rest
    trad = [("Let the rest be \\(r\\) questions.", rf"Right answers \(= {tex(right)} + \frac{{{tex(a)}}}{{{tex(b)}}}r\); total \(= {tex(first)} + r\)."),
            (f"They are {tex(p)}% of the total.", rf"\[ {tex(right)} + \frac{{{tex(a)}}}{{{tex(b)}}}r = \frac{{{tex(p)}}}{{100}}({tex(first)} + r) \;\Rightarrow\; r = {tex(rest)} \]"),
            ("Total.", rf"\[ {tex(first)} + {tex(rest)} = {tex(N)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(p)}\), \(y = {tex(right + F(a) / b * rest)}\) right answers."), apply(4),
            ("Substitute the values.", rf"\[ N = \frac{{{tex(right + F(a) / b * rest)}}}{{{tex(p)}}}\times 100 = {tex(N)} \]")]
    return R(4, "number", N, trad, rule, Num(N), [rf"Rest \(= {tex(rest)}\).", rf"Right \(= {tex(right + F(a) / b * rest)}\).", rf"Total \(= {tex(N)}\)."],
             rf"\[ \frac{{{tex(right + F(a) / b * rest)}}}{{{tex(p)}}}\times 100 = {tex(N)} \]")


def b_two_langs(n, only_a, both):                        # M6 -> Rule 3
    n, only_a, both = map(F, (n, only_a, both))
    oa, bo = n * only_a / 100, n * both / 100
    v = n - oa
    trad = [("Count each group.", rf"Only the first language: \({tex(only_a)}\%\) of \({tex(n)} = {tex(oa)}\); both: \({tex(both)}\%\) of \({tex(n)} = {tex(bo)}\); only the second: \({tex(n - oa - bo)}\)."),
            ("Speakers of the second language.", rf"\[ {tex(n - oa - bo)} + {tex(bo)} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"Those who do not speak the second language are the \({tex(only_a)}\%\) who speak only the first."), apply(3),
            ("Substitute the values.", rf"\[ {tex(n)} - \frac{{{tex(only_a)}}}{{100}}\times {tex(n)} = {tex(v)} \]")]
    return R(3, "number", v, trad, rule, Num(v), [rf"Only the first \(= {tex(oa)}\).", rf"Everyone else speaks the second.", rf"\({tex(n)} - {tex(oa)} = {tex(v)}\)."],
             rf"\[ {tex(n)} - {tex(oa)} = {tex(v)} \]")


def b_town(a, b, cm, cf, adult_f):                       # M7 -> Rule 4
    a, b, cm, cf, adult_f = map(F, (a, b, cm, cf, adult_f))
    fem = adult_f * 100 / (100 - cf)
    male = fem * a / b
    v = fem + male
    trad = [("Females.", rf"Adults are \({tex(100 - cf)}\%\) of the females: \({tex(adult_f)}\times\frac{{100}}{{{tex(100 - cf)}}} = {tex(fem)}\)."),
            ("Males.", rf"\[ {tex(fem)}\times\frac{{{tex(a)}}}{{{tex(b)}}} = {tex(male)} \]"), ("Population.", rf"\[ {tex(fem)} + {tex(male)} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"\({tex(100 - cf)}\%\) of the females is \({tex(adult_f)}\)."), apply(4),
            ("Substitute the values.", rf"\[ N = \frac{{{tex(adult_f)}}}{{{tex(100 - cf)}}}\times 100 = {tex(fem)},\qquad {tex(fem)}\times\frac{{{tex(a + b)}}}{{{tex(b)}}} = {tex(v)} \]")]
    return R(4, "number", v, trad, rule, Num(v), [rf"Females \(= {tex(fem)}\).", rf"Males \(= {tex(male)}\).", rf"Total \(= {tex(v)}\)."],
             rf"\[ \frac{{{tex(adult_f)}\times 100}}{{{tex(100 - cf)}}}\times\frac{{{tex(a + b)}}}{{{tex(b)}}} = {tex(v)} \]")


def b_towns(r, up, total):                               # M8 -> Rule 74
    r, up = [F(t) for t in r], [F(t) for t in up]
    total = F(total)
    w = sum(ri * (100 + ui) / 100 for ri, ui in zip(r, up))
    k = total / w
    v = r[0] * k
    parts = " + ".join(rf"{tex(ri)}k\times\frac{{{tex(100 + ui)}}}{{100}}" for ri, ui in zip(r, up))
    trad = [("Let the first-year numbers be " + ", ".join(tex(ri) + "k" for ri in r) + ".", rf"Next year: \({parts} = {tex(w)}k\)."),
            ("Solve.", rf"\[ {tex(w)}k = {tex(total)} \;\Rightarrow\; k = {tex(k)} \]"), ("First town in the first year.", rf"\[ {tex(r[0])}k = {tex(v)} \]")]
    rule = [("Identify the values.", rf"Ratio {' : '.join(tex(ri) for ri in r)}; rises " + ", ".join(rf"\({tex(ui)}\%\)" for ui in up) + "."),
            ("Apply the specified rule.", r"Each part grows by its own per cent; the parts of the ratio, grown, add up to the new total (as in the rule's "
                                          r"\(\frac{100+x}{100}\) factors)."),
            ("Substitute the values.", rf"\[ k = \frac{{{tex(total)}}}{{{tex(w)}}} = {tex(k)},\qquad {tex(r[0])}k = {tex(v)} \]")]
    return R(74, "number", v, trad, rule, Num(v), [rf"Grown ratio total \(= {tex(w)}k\).", rf"\(k = {tex(k)}\).", rf"First town \(= {tex(v)}\)."],
             rf"\[ {tex(r[0])}\times\frac{{{tex(total)}}}{{{tex(w)}}} = {tex(v)} \]")


def b_chain(p1, p2, total):                              # M14 -> Rule 6
    p1, p2, total = map(F, (p1, p2, total))
    c = F(100); b = c * p2 / 100; a = b * p1 / 100
    k = total / (a + b + c)
    v = a * k
    trad = [("Take the third person's pay as 100.", rf"Second \(= {tex(p2)}\%\) of 100 \(= {tex(b)}\); first \(= {tex(p1)}\%\) of {tex(b)} \(= {tex(a)}\)."),
            ("Share the total.", rf"\[ {m(total)}\times\frac{{{tex(a)}}}{{{tex(a + b + c)}}} = {m(v)} \]")]
    rule = [("Identify the values.", rf"The three pays are in the ratio \({tex(a)} : {tex(b)} : 100\)."), apply(6),
            ("Substitute the values.", rf"\[ \frac{{N}}{{100}} = \frac{{{m(total)}}}{{{tex(a + b + c)}}},\qquad \text{{first}} = {tex(a)}\times\frac{{{m(total)}}}{{{tex(a + b + c)}}} = {m(v)} \]")]
    return R(6, "number", v, trad, rule, Rs(v), [rf"Ratio \({tex(a)} : {tex(b)} : 100\).", rf"Share of the first \(= \frac{{{tex(a)}}}{{{tex(a + b + c)}}}\).", rf"\(= {m(v)}\)."],
             rf"\[ {m(total)}\times\frac{{{tex(a)}}}{{{tex(a + b + c)}}} = {m(v)} \]")


def b_what_pct(Rv, N):                                   # M15, M18 -> Rule 5
    Rv, N = F(Rv), F(N)
    v = Rv / N * 100
    trad = [("Part over whole, times 100.", rf"\[ \frac{{{tex(Rv)}}}{{{tex(N)}}}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"\(R = {tex(Rv)}\), \(N = {tex(N)}\)."), apply(5), ("Substitute the values.", rf"\[ x = \frac{{{tex(Rv)}}}{{{tex(N)}}}\times 100 = {tex(v)} \]")]
    return R(5, "number", v, trad, rule, P(v), [rf"\(\frac{{{tex(Rv)}}}{{{tex(N)}}}\).", r"Times 100.", rf"\(= {tex(v)}\%\)."], rf"\[ \frac{{{tex(Rv)}}}{{{tex(N)}}}\times 100 = {tex(v)}\% \]")


def b_pct_then(x, V, op, k):                             # M16 (x% of V = k * ?), M19 (x% of V / ? = k) -> Rule 3
    x, V, k = map(F, (x, V, k))
    part = x * V / 100
    v = part / k
    rel = rf"{tex(k)}\times N = {tex(part)}" if op == "times" else rf"\frac{{{tex(part)}}}{{N}} = {tex(k)}"
    trad = [(f"{tex(x)}% of {tex(V)}.", rf"\[ \frac{{{tex(x)}}}{{100}}\times {tex(V)} = {tex(part)} \]"), ("Find the number.", rf"\[ {rel} \;\Rightarrow\; N = {tex(v)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\), value \(= {tex(V)}\)."), apply(3), ("Substitute the values.", rf"\[ {tex(part)} \div {tex(k)} = {tex(v)} \]")]
    return R(3, "number", v, trad, rule, Num(v), [rf"\({tex(x)}\%\) of \({tex(V)} = {tex(part)}\).", rf"\({tex(part)} \div {tex(k)}\).", rf"\(= {tex(v)}\)."],
             rf"\[ \frac{{{tex(x)}\times {tex(V)}}}{{100}} \div {tex(k)} = {tex(v)} \]")


def Dec(v):
    return rf"\({float(F(v)):g}\)"


def b_pct_of_pct(x, y):                                  # M17 -> Rule 3
    x, y = F(x), F(y)
    v = x / 100 * y / 100
    trad = [("Write both as fractions.", rf"\[ \frac{{{tex(x)}}}{{100}}\times\frac{{{tex(y)}}}{{100}} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"\({tex(x)}\%\) of the item \({tex(y)}\%\) \(= {tex(y / 100)}\)."), apply(3),
            ("Substitute the values.", rf"\[ \frac{{{tex(x)}}}{{100}}\times {tex(y / 100)} = {tex(v)} \]")]
    dec = f"{float(v):g}"
    return R(3, "number", v, trad, rule, Dec(v), [rf"\({tex(y)}\%\) \(= {tex(y / 100)}\).", rf"\(\times\frac{{{tex(x)}}}{{100}}\).", rf"\(= {dec}\)."],
             rf"\[ {tex(x / 100)}\times {tex(y / 100)} = {tex(v)} = {dec} \]")


def b_add_back(x, c):                                    # M20 -> Rule 4
    x, c = F(x), F(c)
    N = c * 100 / (100 - x)
    trad = [("The number is the part plus the rest.", rf"\(N = \frac{{{tex(x)}}}{{100}}N + {tex(c)}\), so \(\frac{{{tex(100 - x)}}}{{100}}N = {tex(c)}\)."), ("Solve.", rf"\[ N = {tex(N)} \]")]
    rule = [("Identify the values.", rf"\({tex(100 - x)}\%\) of the number is \({tex(c)}\)."), apply(4), ("Substitute the values.", rf"\[ N = \frac{{{tex(c)}}}{{{tex(100 - x)}}}\times 100 = {tex(N)} \]")]
    return R(4, "number", N, trad, rule, Num(N), [rf"\({tex(100 - x)}\%\) of \(N = {tex(c)}\).", rf"\(N = \frac{{{tex(c)}}}{{{tex(100 - x)}}}\times 100\).", rf"\(= {tex(N)}\)."],
             rf"\[ \frac{{{tex(c)}\times 100}}{{{tex(100 - x)}}} = {tex(N)} \]")


def b_to_pct(d, fr_):                                    # M21 -> Rule 1
    d, fr_ = F(d), F(fr_)
    v = d * fr_ * 100
    trad = [("Multiply.", rf"\[ {tex(d)}\times\frac{{{fr_.numerator}}}{{{fr_.denominator}}} = {tex(d * fr_)} \]"), ("As a per cent.", rf"\[ {tex(d * fr_)}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"The fraction is \({tex(d * fr_)}\)."), apply(1), ("Substitute the values.", rf"\[ {tex(d * fr_)}\times 100 = {tex(v)}\% \]")]
    return R(1, "number", v, trad, rule, P(v), [rf"Product \(= {tex(d * fr_)}\).", r"Times 100.", rf"\(= {tex(v)}\%\)."], rf"\[ {tex(d * fr_)}\times 100 = {tex(v)}\% \]")


def b_up_down(x):                                        # M23 -> Rule 36 (signed)
    x = F(x)
    v = -(x * x / 100)
    trad = [("Take the cost as 100.", rf"Marked \(= {tex(100 + x)}\); after \({tex(x)}\%\) off: \({tex((100 + x) * (100 - x) / 100)}\)."),
            ("Gain or loss.", rf"\[ {tex((100 + x) * (100 - x) / 100)} - 100 = {tex(v)}\% \]" + " It is negative, so a loss.")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\)."), apply(36), ("Substitute the values.", rf"\[ \frac{{{tex(x)}^2}}{{100}} = {tex(-v)}\% \]")]
    return R(36, "signed", v, trad, rule, rf"a loss of \({tex(-v)}\%\)", [rf"\(x = {tex(x)}\).", rf"\(\frac{{x^2}}{{100}} = {tex(-v)}\).", rf"A loss of \({tex(-v)}\%\)."],
             rf"\[ \frac{{{tex(x * x)}}}{{100}} = {tex(-v)}\% \]")


def b_back(x, final):                                    # M27 -> Rule 36
    x, final = F(x), F(final)
    orig = final / (1 - x * x / 10000)
    trad = [("Take the original price as 100.", rf"Up \({tex(x)}\%\): \({tex(100 + x)}\); down \({tex(x)}\%\): \({tex((100 + x) * (100 - x) / 100)}\)."),
            ("Work back.", rf"\[ {m(final)}\times\frac{{100}}{{{tex((100 + x) * (100 - x) / 100)}}} = {m(orig)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\), final price \({m(final)}\)."), apply(36),
            ("Substitute the values.", rf"The net fall is \(\frac{{{tex(x)}^2}}{{100}} = {tex(x * x / 100)}\%\), so \[ {m(final)}\times\frac{{100}}{{{tex(100 - x * x / 100)}}} = {m(orig)} \]")]
    return R(36, "number", orig, trad, rule, Rs(orig), [rf"Net fall \(= {tex(x * x / 100)}\%\).", rf"Final \(= {tex(100 - x * x / 100)}\%\) of the original.", rf"Original \(= {m(orig)}\)."],
             rf"\[ {m(final)}\times\frac{{100}}{{{tex(100 - x * x / 100)}}} = {m(orig)} \]")


def b_other_side(x):                                     # M24 -> Rule 35
    x = F(x)
    v = 100 * 100 / x
    trad = [("Take b as 100.", rf"Then a \(= {tex(x)}\)."), ("b as a per cent of a.", rf"\[ \frac{{100}}{{{tex(x)}}}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"a is \({tex(100 - x)}\%\) less than b."), apply(35),
            ("Substitute the values.", rf"b is \(\frac{{{tex(100 - x)}}}{{{tex(x)}}}\times 100 = {tex(v - 100)}\%\) more than a, i.e. \({tex(v)}\%\) of a.")]
    return R(35, "number", v, trad, rule, P(v), [rf"\(r = {tex(100 - x)}\).", rf"\(\frac{{r}}{{100 - r}}\times 100 = {tex(v - 100)}\).", rf"b \(= {tex(v)}\%\) of a."],
             rf"\[ 100 + {tex(v - 100)} = {tex(v)}\% \]")


def b_less_than(x, V):                                   # M25 -> Rule 3
    x, V = F(x), F(V)
    v = V * (100 - x) / 100
    trad = [(f"{tex(x)}% of {tex(V)}.", rf"\[ \frac{{{tex(x)}}}{{100}}\times {tex(V)} = {tex(V * x / 100)} \]"), ("Take it away.", rf"\[ {tex(V)} - {tex(V * x / 100)} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(100 - x)}\) per cent of \({tex(V)}\) is left."), apply(3), ("Substitute the values.", rf"\[ \frac{{{tex(100 - x)}}}{{100}}\times {tex(V)} = {tex(v)} \]")]
    return R(3, "number", v, trad, rule, Num(v), [rf"\({tex(100 - x)}\%\) is left.", rf"\(\times {tex(V)}\).", rf"\(= {tex(v)}\)."], rf"\[ \frac{{{tex(100 - x)}}}{{100}}\times {tex(V)} = {tex(v)} \]")


def b_sold_back(W, up, down):                            # M29 -> Rule 37
    W, up, down = map(F, (W, up, down))
    got = W * (100 + up) / 100
    paid = got * (100 - down) / 100
    v = got - paid
    trad = [("First sale.", rf"\[ {m(W)}\times\frac{{{tex(100 + up)}}}{{100}} = {m(got)} \]"), ("Bought back.", rf"\[ {m(got)}\times\frac{{{tex(100 - down)}}}{{100}} = {m(paid)} \]"),
            ("Gain (he has the shop again).", rf"\[ {m(got)} - {m(paid)} = {m(v)} \]")]
    rule = [("Identify the values.", rf"Up \({tex(up)}\%\), then down \({tex(down)}\%\) on the new price."), apply(37),
            ("Substitute the values.", rf"The buy-back price is \({tex(up)} - {tex(down)} - \frac{{{tex(up)}\times {tex(down)}}}{{100}} = {tex(up - down - up * down / 100)}\%\) above the worth: "
                                       rf"\({m(paid)}\); gain \(= {m(got)} - {m(paid)} = {m(v)}\).")]
    return R(37, "number", v, trad, rule, Rs(v), [rf"Sold for \({m(got)}\).", rf"Bought back for \({m(paid)}\).", rf"Gain \(= {m(v)}\)."], rf"\[ {m(got)} - {m(paid)} = {m(v)} \]")


def b_only_other(n, only_a, both):                       # M1 -> Rule 53
    n, only_a, both = map(F, (n, only_a, both))
    oa = n * only_a / 100
    v = n - oa - both
    trad = [("Only the first language.", rf"\({tex(only_a)}\%\) of \({tex(n)} = {tex(oa)}\)."), ("Only the second.", rf"\[ {tex(n)} - {tex(oa)} - {tex(both)} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"Only the first \(= {tex(only_a)}\%\), both \(= {tex(both / n * 100)}\%\)."), apply(53),
            ("Substitute the values.", rf"Like 'passed in both': the rest \(= 100 - {tex(only_a)} - {tex(both / n * 100)} = {tex(100 - only_a - both / n * 100)}\%\) of \({tex(n)} = {tex(v)}\).")]
    return R(53, "number", v, trad, rule, Num(v), [rf"Only the first \(= {tex(oa)}\).", rf"Both \(= {tex(both)}\).", rf"Only the second \(= {tex(v)}\)."], rf"\[ {tex(n)} - {tex(oa)} - {tex(both)} = {tex(v)} \]")


def b_games(n, gp, only_b, only_b_boys, girls_both):     # M2 -> Rule 53
    n, gp, only_b, only_b_boys, girls_both = map(F, (n, gp, only_b, only_b_boys, girls_both))
    boys = n * 100 / (100 + gp)
    girls = n - boys
    v = girls - (only_b - only_b_boys) - girls_both
    trad = [("Boys and girls.", rf"Boys \(+ {tex(gp)}\%\) of boys \(= {tex(n)}\): boys \(= {tex(boys)}\), girls \(= {tex(girls)}\)."),
            ("Girls by game.", rf"Girls playing only the second game \(= {tex(only_b)} - {tex(only_b_boys)} = {tex(only_b - only_b_boys)}\); girls playing both \(= {tex(girls_both)}\)."),
            ("Girls playing only the first game.", rf"\[ {tex(girls)} - {tex(only_b - only_b_boys)} - {tex(girls_both)} = {tex(v)} \]")]
    rule = [("Identify the values.", rf"The girls are \({tex(girls)}\); take away the girls in the other two groups."), apply(53),
            ("Substitute the values.", rf"\[ {tex(girls)} - ({tex(only_b - only_b_boys)} + {tex(girls_both)}) = {tex(v)} \]")]
    return R(53, "number", v, trad, rule, Num(v), [rf"Girls \(= {tex(girls)}\).", rf"Other girls \(= {tex(only_b - only_b_boys + girls_both)}\).", rf"Only the first game \(= {tex(v)}\)."],
             rf"\[ {tex(girls)} - {tex(only_b - only_b_boys + girls_both)} = {tex(v)} \]")


def b_passed_both(e, m_, both_fail, passed):             # M31 -> Rule 53
    e, m_, both_fail, passed = map(F, (e, m_, both_fail, passed))
    pb = 100 - ((100 - e) + (100 - m_) - both_fail)
    N = passed * 100 / pb
    trad = [("Failures.", rf"Failed the first \(= {tex(100 - e)}\%\), the second \(= {tex(100 - m_)}\%\), both \(= {tex(both_fail)}\%\); failed at least one \(= {tex((100 - e) + (100 - m_) - both_fail)}\%\)."),
            ("Passed both and the total.", rf"Passed both \(= {tex(pb)}\%\): \[ {tex(passed)}\times\frac{{100}}{{{tex(pb)}}} = {tex(N)} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(100 - e)}\), \(y = {tex(100 - m_)}\), \(z = {tex(both_fail)}\)."), apply(53),
            ("Substitute the values.", rf"\[ 100 - ({tex(100 - e)} + {tex(100 - m_)} - {tex(both_fail)}) = {tex(pb)}\%,\qquad \frac{{{tex(passed)}}}{{{tex(pb)}}}\times 100 = {tex(N)} \]")]
    return R(53, "number", N, trad, rule, Num(N), [rf"Passed both \(= {tex(pb)}\%\).", rf"\({tex(passed)}\) is \({tex(pb)}\%\).", rf"Total \(= {tex(N)}\)."],
             rf"\[ \frac{{{tex(passed)}\times 100}}{{{tex(pb)}}} = {tex(N)} \]")


def b_equal_pcts(x, y, ask):                             # M22 (k with Q = k% of P), M28 (a : b) -> Rule 6
    x, y = F(x), F(y)
    rb_ = x / y                                          # b = (x/y) a   from x% of a = y% of b
    if ask == "pct":
        v = rb_ * 100
        trad = [("Write the equality.", rf"\(\frac{{{tex(x)}}}{{100}}P = \frac{{{tex(y)}}}{{100}}Q\), so \(Q = \frac{{{tex(x)}}}{{{tex(y)}}}P = {tex(rb_)}P\)."), ("As a per cent of P.", rf"\[ {tex(rb_)}\times 100 = {tex(v)} \]")]
        rule = [("Identify the values.", rf"\(x = {tex(x)}\) of P and \(y = {tex(y)}\) of Q are the same amount."), apply(6),
                ("Substitute the values.", rf"\[ \frac{{Q}}{{P}} = \frac{{{tex(x)}}}{{{tex(y)}}} = {tex(rb_)},\quad k = {tex(v)} \]")]
        return R(6, "number", v, trad, rule, Num(v), [rf"\(Q = \frac{{{tex(x)}}}{{{tex(y)}}}P\).", rf"\(= {tex(rb_)}P\).", rf"\(k = {tex(v)}\)."], rf"\[ \frac{{{tex(x)}}}{{{tex(y)}}}\times 100 = {tex(v)} \]")
    r = y / x                                            # a / b
    a, b = r.numerator, r.denominator
    trad = [("Write the equality.", rf"\(\frac{{{tex(x)}}}{{100}}a = \frac{{{tex(y)}}}{{100}}b\), so \(\frac{{a}}{{b}} = \frac{{{tex(y)}}}{{{tex(x)}}}\)."), ("Ratio.", rf"\[ a : b = {a} : {b} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\) of a and \(y = {tex(y)}\) of b are the same amount."), apply(6),
            ("Substitute the values.", rf"\[ \frac{{a}}{{b}} = \frac{{{tex(y)}}}{{{tex(x)}}} = \frac{{{a}}}{{{b}}} \]")]
    return R(6, "ratio", (a, b), trad, rule, rf"\({a} : {b}\)", [rf"\(\frac{{a}}{{b}} = \frac{{{tex(y)}}}{{{tex(x)}}}\).", rf"\(= \frac{{{a}}}{{{b}}}\).", rf"\(a : b = {a} : {b}\)."],
             rf"\[ \frac{{{tex(y)}}}{{{tex(x)}}} = \frac{{{a}}}{{{b}}} \]")


def b_less_by(kind, a):                                  # M26 (length up a%), M30 (x = a times y) -> Rule 34
    a = F(a)
    r = a if kind == "up" else (a - 1) * 100            # first is r% more than the second
    v = r / (100 + r) * 100
    if kind == "up":
        trad = [("Take the length and breadth as 100 each.", rf"New length \(= {tex(100 + a)}\); the area stays 10000, so the breadth \(= \frac{{10000}}{{{tex(100 + a)}}} = {tex(10000 / (100 + a))}\)."),
                ("Cut in the breadth.", rf"\[ 100 - {tex(10000 / (100 + a))} = {tex(v)}\% \]")]
    else:
        trad = [("Take y as 100.", rf"Then x \(= {tex(100 * a)}\)."), ("How far y is below x.", rf"\[ \frac{{{tex(100 * a)} - 100}}{{{tex(100 * a)}}}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"The first is \(r = {tex(r)}\%\) more than the second."), apply(34), ("Substitute the values.", rf"\[ \frac{{{tex(r)}}}{{100 + {tex(r)}}}\times 100 = {tex(v)}\% \]")]
    return R(34, "number", v, trad, rule, P(v), [rf"\(r = {tex(r)}\).", rf"\(\frac{{r}}{{100 + r}}\times 100\).", rf"\(= {tex(v)}\%\)."], rf"\[ \frac{{{tex(r)}}}{{{tex(100 + r)}}}\times 100 = {tex(v)}\% \]")


PASSAGE = ("In a class of 96 students, girls and boys are in the ratio 3 : 5. Each student speaks only Tamil, only English, or both. The "
           "number of boys who speak only Tamil equals the number of girls who speak only Tamil, and each is 50% of the number of girls. "
           "25% of the girls speak both languages, and 40% of the boys speak only English. ")
G, B = F(36), F(60)
GT, BT, GB, BE = G * 50 / 100, G * 50 / 100, G * 25 / 100, B * 40 / 100
GE, BB = G - GT - GB, B - BT - BE


def b_passage(ask):                                      # M9-M13 -> Rule 3
    lines = [rf"Girls \(= \frac{{3}}{{8}}\times 96 = {tex(G)}\), boys \(= {tex(B)}\).",
             rf"Only Tamil: girls \(50\%\) of \({tex(G)} = {tex(GT)}\), boys \(= {tex(BT)}\). Both: girls \(25\%\) of \({tex(G)} = {tex(GB)}\). Only English: boys \(40\%\) of \({tex(B)} = {tex(BE)}\).",
             rf"So girls only English \(= {tex(G)} - {tex(GT)} - {tex(GB)} = {tex(GE)}\); boys both \(= {tex(B)} - {tex(BT)} - {tex(BE)} = {tex(BB)}\)."]
    val, what, fmt = {"girls_eng": (GE, "girls who speak only English", Num), "boys_tamil": (BT + BB, "boys who speak Tamil", Num),
                      "pct_tamil": ((GT + BT) / 96 * 100, "per cent of all students who speak only Tamil", P),
                      "both": (GB + BB, "students who speak both", Num), "boys_one": (BT + BE, "boys who speak only one language", Num)}[ask]
    kind = "number"
    trad = [("Fill in the table.", "<br>".join(lines)), (f"Count the {what}.", rf"\[ {tex(val)} \]")]
    rule = [("Identify the values.", r"Each group is a per cent of the girls or of the boys."), apply(3),
            ("Substitute the values.", rf"For example \(\frac{{50}}{{100}}\times {tex(G)} = {tex(GT)}\); then the {what} \(= {tex(val)}\).")]
    return R(3, kind, val, trad, rule, fmt(val), [rf"Girls {tex(G)}, boys {tex(B)}.", r"Fill in each group from its per cent.", rf"Answer \(= {tex(val)}\)."], rf"\[ {tex(val)} \]")


# ---------------------------------------------------------------- the rows and the new questions
OLD = {   # row: (rule, question, builder, option kind, answer position)
    662: (75, "Kiran spends 25% of her monthly income on rent and 20% of the rest on food. She saves half of what is left. If she saves Rs 25200 a year, what is her monthly income?", lambda: b_spend(25, 20, F(1, 2), 25200), "rs", 3),
    663: (17, "Ravi gave 25% of his money to Sunil. Sunil gave one-fifth of it to Amar. Amar spent Rs 150 on a book and had Rs 350 left. How much money did Ravi have at first?", lambda: b_shares(25, 5, 150, 350), "rs", 1),
    664: (4, "Neha answered 85% of the questions in a test correctly. Of the first 20 questions she got 19 right, and of the rest she got 3 out of every 4 right. How many questions were there in the test?", lambda: b_test(85, 20, 19, 3, 4), "num", 4),
    665: (3, "In a club of 80 members, 35% speak only Tamil, 15% speak both Tamil and Telugu, and the rest speak only Telugu. How many members speak Telugu?", lambda: b_two_langs(80, 35, 15), "num", 2),
    666: (4, "Men and women in a town are in the ratio 5 : 4. Children are 15% of the males and 30% of the females. If there are 28000 adult females, what is the total population of the town?", lambda: b_town(5, 4, 15, 30, 28000), "num", 1),
    667: (74, "Students taking an exam in towns P, Q and R were in the ratio 2 : 3 : 7. Next year their numbers rose by 25%, 30% and 15%, and 2890 students took it in all. How many took it in town P in the first year?", lambda: b_towns((2, 3, 7), (25, 30, 15), 2890), "num", 3),
    668: (6, "Asha's pay is 20% of Bina's, and Bina's pay is 50% of Chitra's. Together they earn Rs 16000 a month. How much does Asha earn?", lambda: b_chain(20, 50, 16000), "rs", 2),
    669: (5, "What per cent of 240 is 16.8?", lambda: b_what_pct(F("16.8"), 240), "pct", 4),
    670: (3, "If 35% of 120 equals 6 times a number, find the number.", lambda: b_pct_then(35, 120, "times", 6), "num", 1),
    671: (3, "What is 40% of 15% written as a decimal?", lambda: b_pct_of_pct(40, 15), "dec", 3),
    672: (5, "7 out of 1750 parts of a soil sample are iron. What per cent of the sample is iron?", lambda: b_what_pct(7, 1750), "pct", 2),
    673: (3, "When 45% of 60 is divided by a number, the result is 9. Find the number.", lambda: b_pct_then(45, 60, "div", 9), "num", 4),
    674: (4, "When 60% of a number is added to 84, the result is the number itself. Find the number.", lambda: b_add_back(60, 84), "num", 2),
    675: (1, r"Write \(0.84\times\frac{5}{8}\) as a per cent.", lambda: b_to_pct(F("0.84"), F(5, 8)), "pct", 1),
    676: (36, "A shop marks a fan 15% above its cost and then gives 15% off the marked price. What is its gain or loss per cent?", lambda: b_up_down(15), "signed", 3),
    677: (35, "If a is 80% of b, what per cent of a is b?", lambda: b_other_side(80), "pct", 1),
    678: (37, "Ravi owns a shop worth Rs 20000. He sells it to Sohan at a profit of 15%, and Sohan sells it back to Ravi at a loss of 12%. How much does Ravi gain in the two deals?", lambda: b_sold_back(20000, 15, 12), "rs", 4),
    679: (3, "What is left when 35% is taken off 140?", lambda: b_less_than(35, 140), "num", 2),
}
NEW = {   # key: (rule, question, builder, option kind, answer position)
    "m01": (53, "In a school, 120 students study only Tamil, only Hindi, or both. 35% of them study only Tamil and 40 study both. How many study only Hindi?", lambda: b_only_other(120, 35, 40), "num", 3),
    "m02": (53, "Of 90 children who play chess or carrom or both, the girls number 80% of the boys. 30 children play only carrom, and 18 of them are boys. 8 girls play both games. How many girls play only chess?", lambda: b_games(90, 80, 30, 18, 8), "num", 1),
    "m09": (3, PASSAGE + "How many girls speak only English?", lambda: b_passage("girls_eng"), "num", 2),
    "m10": (3, PASSAGE + "In all, how many boys speak Tamil?", lambda: b_passage("boys_tamil"), "num", 4),
    "m11": (3, PASSAGE + "What per cent of all the students speak only Tamil?", lambda: b_passage("pct_tamil"), "pct", 1),
    "m12": (3, PASSAGE + "In all, how many students speak both languages?", lambda: b_passage("both"), "num", 3),
    "m13": (3, PASSAGE + "How many boys speak only one of the two languages?", lambda: b_passage("boys_one"), "num", 2),
    "m22": (6, "If 60% of P equals 24% of Q, and Q is k% of P, find k.", lambda: b_equal_pcts(60, 24, "pct"), "num", 4),
    "m26": (34, "The length of a rectangle is increased by 25% but its area stays the same. By what per cent must its breadth be reduced?", lambda: b_less_by("up", 25), "pct", 1),
    "m27": (36, "The price of a toy is raised by 20% and the new price is then cut by 20%. If the toy now costs Rs 192, what was its original price?", lambda: b_back(20, 192), "rs", 3),
    "m28": (6, "If 15% of a equals 25% of b, find a : b.", lambda: b_equal_pcts(15, 25, "ratio"), "ratio", 2),
    "m30": (34, "x is 4 times y. By what per cent is y less than x?", lambda: b_less_by("times", 4), "pct", 4),
    "m31": (53, "In a test, 80% of the students passed in Science and 75% in English, while 15% failed in both. If 350 students passed in both, how many students took the test?", lambda: b_passed_both(80, 75, 15, 350), "num", 1),
}


def options(kind, v, pos):
    if kind == "ratio":
        a, b = v
        return place(rf"\({a} : {b}\)", [rf"\({b} : {a}\)", rf"\({a + 1} : {b}\)", rf"\({a} : {b + 2}\)"], pos)
    if kind == "signed":
        s = abs(F(v))
        w, o = ("Profit", "Loss") if v > 0 else ("Loss", "Profit")
        return place(rf"{w} of \({tex(s)}\%\)", [rf"{o} of \({tex(s)}\%\)", rf"{w} of \({tex(s + 1)}\%\)", rf"{w} of \({tex(s + 2)}\%\)"], pos)
    v = F(v)
    fmt = {"rs": Rs, "num": Num, "pct": P, "dec": Dec}[kind]
    if kind == "dec":
        wrong = [v * 10, v / 10, v * 2]
    elif kind == "pct":
        wrong = [v + 5, v - 3 if v > 3 else v + 8, v * 2 if v * 2 != v + 5 else v + 10]
    else:
        wrong = [v * F(11, 10), v * F(9, 10), v * F(6, 5)] if v >= 50 else [v + 2, v - 1 if v > 1 else v + 3, v + 5]
    return place(fmt(v), [fmt(w) for w in wrong], pos)


def main():
    folders = {}
    for rid, (rule, *_rest) in OLD.items():
        folders.setdefault(rule, {"old": [], "new": []})["old"].append(rid)
    for key, (rule, *_rest) in NEW.items():
        folders.setdefault(rule, {"old": [], "new": []})["new"].append(key)
    for rule, items in sorted(folders.items()):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        card = dump["rule_card"]
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(items["old"]), (rule, sorted(rows), items["old"])
        out = []
        for rid in items["old"]:
            _, q, fn, kind, pos = OLD[rid]
            g = fn()
            op = options(kind, g["answer"][1], pos)
            extra = {"question": q, **dict(zip("abcd", op)), "e": "", "ans": pos}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, card["id"], extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        for p in ("3_json_import_payload.json", "3_answers.json"):
            if os.path.exists(os.path.join(folder, p)):
                os.remove(os.path.join(folder, p))
        if items["new"]:
            qs, answers = [], []
            for key in items["new"]:
                _, q, fn, kind, pos = NEW[key]
                g = fn()
                op = options(kind, g["answer"][1], pos)
                qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
                k_, v = g["answer"]
                answers.append([key, [k_, [str(t) for t in v] if k_ == "ratio" else str(v)]])
            json.dump({"rules_html": [{"chapter": "percentage", "rule_name": f"Rule {rule}", "rule_html": card["rule_html"]}], "questions": qs},
                      open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"misc rule {rule}: rows {items['old']} | new {items['new']}")


if __name__ == "__main__":
    main()
