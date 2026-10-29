"""Rewording the Time & Work Miscellaneous rows (2026-10-29): 261-277 (the book's Miscellaneous problems) and 1682 (M4, added
with changed numbers but in the book's words) get all-new numbers and a sentence in the book's simple style with the job/object
changed, new options, and an explanation regenerated for the new numbers. The generators of ../../gen_misc.py had the book's
numbers written in; the ones below take the numbers as parameters and keep the same explanation layout (Theorem, Traditional
Method, Specified Rule, Final Answer). Rule links stay (Rules 1, 4, 6, 8, 9, 14, 28, 31). Numbers keep the order the
../../solve_misc.py solvers read them in (misc/solve_misc_rw.py adds 274 with any fractions and maps 1682 to "m4").
Writes reword/misc/ruleNN/2_new_rows.json; check: `python reword_check.py misc` (simple gate - SIMPLE_STYLE marker)."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/misc
sys.path.insert(0, os.path.dirname(HERE))
import rw_common  # noqa: E402
from common import rbe, shortcut, steps, tex  # noqa: E402
from gen_1_4 import F1, T1, T4, fr, result  # noqa: E402
from gen_5_10 import F6, F8, T6, T8, T9  # noqa: E402
from gen_11_20 import T14  # noqa: E402
from gen_21_30 import T28  # noqa: E402
from gen_31_35 import F31, T31  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (job changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-29)")
F14 = r"\[ E_1D_1 = E_2D_2 \quad\text{(efficiency }\times\text{ days is the same for the same work)} \]"
t = tex
plain = lambda *v: dict(zip("abcd", v))


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return result(answer, theorem, trad, rule, fin, rbe(rb_steps, fin), shortcut(sc_body, fin))


def days(v, unit="days"):
    return rf"\({t(v)}\) {unit}"


# ---------------------------------------------------------------- Rule 1 (man-days)
def m266(M, D, leave, after):
    rest = M - leave
    W2 = F(rest * after, M * D)
    T = D * (1 - W2)
    trad = steps(("Count the work in man-days.", rf"\[ {M}\times {D} = {M * D}\text{{ man-days}} \]"),
                 ("Work done after the men leave.", rf"The other \({M} - {leave} = {rest}\) men work \({t(after)}\) days:<br>\[ {rest}\times {t(after)} = {t(rest * after)}\text{{ man-days}} \]"),
                 ("Find when they leave.", rf"The first part needs \({M * D} - {t(rest * after)} = {t(M * D - rest * after)}\) man-days, done by all {M} men:<br>\[ {t(M * D - rest * after)}\div {M} = {t(T)}\text{{ days}} \]"))
    rule = steps(("Find the share done by the remaining men.", F1 + rf"\[ W_2 = \frac{{M_2D_2W_1}}{{M_1D_1}} = \frac{{{rest}\times {t(after)}\times 1}}{{{M}\times {D}}} = {fr(W2)} \]"),
                 ("Find the share left for all the men.", rf"\[ 1 - {fr(W2)} = {fr(1 - W2)} \]"),
                 ("Apply the rule again.", rf"\[ D = \frac{{M_1D_1W}}{{M_2W_1}} = \frac{{{M}\times {D}\times {fr(1 - W2)}}}{{{M}\times 1}} = {t(T)}\text{{ days}} \]"))
    return done(("number", T), T1, trad, rule, days(T),
                [rf"{rest} men in \({t(after)}\) days do \(W_2 = \frac{{{rest}\times {t(after)}}}{{{M}\times {D}}} = {fr(W2)}\).", rf"\({fr(1 - W2)}\) is left for {M} men.",
                 rf"\(D = {D}\times {fr(1 - W2)} = {t(T)}\) days."], rf"\[ {D}\times\left(1 - \frac{{{rest}\times {t(after)}}}{{{M}\times {D}}}\right) = {t(T)} \]")


def m268(M, D, every):
    need, block = M * D, M * every                        # every block adds M more men, so the blocks are block, 2 block, ...
    rows, men, total, d, k = [], M, 0, 0, 0
    while total < need:
        d += every
        k += 1
        total += men * every
        rows.append(rf"<tr><td>\({d - every + 1}\)–\({d}\)</td><td>\({men}\)</td><td>\({men * every}\)</td><td>\({total}\)</td></tr>")
        men += M
    assert total == need
    table = ('<table border="1" cellpadding="4"><tr><th>Days</th><th>Men</th><th>Man-days</th><th>Total</th></tr>' + "".join(rows) + "</table>")
    trad = steps(("Count the work in man-days.", rf"\[ {M}\times {D} = {need}\text{{ man-days}} \]"), (f"Add {every} days at a time.", table),
                 ("Read the answer.", rf"The total reaches {need} at the end of day \({d}\)."))
    rule = steps(("Apply the specified rule.", F1 + r"The same work needs the same man-days: \(M_1D_1 = \) sum of men \(\times\) days in each block."),
                 ("Write the blocks.", rf"\[ {block} + {2 * block} + {3 * block} + \dots = {block}(1 + 2 + \dots + k) = {need} \]"),
                 ("Solve.", rf"\[ 1 + 2 + \dots + k = {need // block} = \frac{{k(k+1)}}{{2}} \;\Rightarrow\; k = {k} \]So the work takes \({k}\times {every} = {d}\) days."))
    return done(("number", F(d)), T1, trad, rule, days(d),
                [rf"Work \(= {M}\times {D} = {need}\) man-days.", rf"Blocks: \({block}(1 + 2 + \dots + k) = {need}\), so \(k = {k}\).", rf"\({k}\times {every} = {d}\) days."],
                rf"\[ {block}\cdot\frac{{k(k+1)}}{{2}} = {need} \Rightarrow k = {k} \Rightarrow {d} \]")


def m269(D, half, extra):
    rest = D - half
    M = F(extra * rest, half - rest)
    trad = steps(("Let the men at first be \\(M\\).", rf"They did half the work in {half} days, so half the work \(= {half}M\) man-days."),
                 ("The second half.", rf"\(M + {extra}\) men did the other half in \({D} - {half} = {rest}\) days: \({rest}(M + {extra})\) man-days."),
                 ("Equate the halves.", rf"\[ {half}M = {rest}(M + {extra}) \;\Rightarrow\; {half - rest}M = {extra * rest} \;\Rightarrow\; M = {t(M)} \]"))
    rule = steps(("Identify the values.", rf"\(M_1 = M,\ D_1 = {half},\ W_1 = \frac{{1}}{{2}}\); \(M_2 = M + {extra},\ D_2 = {rest},\ W_2 = \frac{{1}}{{2}}\)."),
                 ("Apply the specified rule.", F1), ("Substitute the values.", rf"\[ M\times {half}\times\frac{{1}}{{2}} = (M + {extra})\times {rest}\times\frac{{1}}{{2}} \;\Rightarrow\; M = {t(M)} \]"))
    return done(("number", M), T1, trad, rule, days(M, "men"),
                [rf"Halves: \(M\) men {half} days, \(M + {extra}\) men {rest} days.", rf"\({half}M = {rest}(M + {extra})\).", rf"\(M = {t(M)}\)."],
                rf"\[ {half}M = {rest}(M + {extra}) \Rightarrow M = {t(M)} \]")


def m272(m, D, after, join, replace):
    men2 = m - replace + join
    left = m * D - m * after
    T = F(left, men2)
    W2 = 1 - F(after, D)
    trad = steps(("Count the work in man-days.", rf"\[ {m}\times {D} = {m * D}\text{{ man-days}} \]"),
                 (f"Work left after {after} days.", rf"\[ {m * D} - {m}\times {after} = {left}\text{{ man-days}} \]Now \({m} - {replace} + {join} = {men2}\) men work."),
                 ("Find the days.", rf"\[ {left}\div {men2} = {t(T)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(M_1 = {m},\ D_1 = {D},\ W_1 = 1\); \(M_2 = {men2}\), \(W_2 = 1 - \frac{{{after}}}{{{D}}} = {fr(W2)}\)."),
                 ("Apply the specified rule.", F1), ("Substitute the values.", rf"\[ {m}\times {D}\times {fr(W2)} = {men2}\times D_2\times 1 \;\Rightarrow\; D_2 = \frac{{{left}}}{{{men2}}} = {t(T)} \]"))
    return done(("number", T), T1, trad, rule, days(T),
                [rf"\(W_2 = {fr(W2)}\), \(M_2 = {men2}\).", r"\(M_1D_1W_2 = M_2D_2W_1\).", rf"\(D_2 = \frac{{{m}\times {D}\times {fr(W2)}}}{{{men2}}} = {t(T)}\)."],
                rf"\[ \frac{{{m}\times {D}\times {fr(W2)}}}{{{men2}}} = {t(T)} \]")


# ---------------------------------------------------------------- Rule 4 (one-hour work adds)
def m277(k, T):
    trad = steps(("Find each machine's output in one hour.", rf"A: \(x\) toys; B: \(y\) toys in {k} hours, so \(\frac{{y}}{{{k}}}\) toys an hour."),
                 ("Add them.", rf"\[ x + \frac{{y}}{{{k}}} = \frac{{{k}x + y}}{{{k}}}\text{{ toys an hour}} \]"),
                 (f"Multiply by {T} hours.", rf"\[ {T}\times\frac{{{k}x + y}}{{{k}}} = {T // k}({k}x + y) \]"))
    rule = steps(("Use the idea of the specified rule.", r"The rule adds one-hour (one-day) work of two workers: \(\frac{1}{x} + \frac{1}{y}\). Here the outputs per hour add the same way."),
                 ("Add the hourly outputs.", rf"\[ x + \frac{{y}}{{{k}}} \]"), ("Multiply by the time.", rf"\[ {T}\left(x + \frac{{y}}{{{k}}}\right) = {T}x + {T // k}y = {T // k}({k}x + y) \]"))
    fin = rf"\({T // k}({k}x+y)\)"
    return done(("expr", T * F(7) + F(T, k) * 3), T4, trad, rule, fin,
                [rf"Per hour: \(x + \frac{{y}}{{{k}}}\).", rf"In {T} hours: \({T}\left(x + \frac{{y}}{{{k}}}\right)\).", rf"\(= {T // k}({k}x+y)\)."],
                rf"\[ {T}\left(x + \frac{{y}}{{{k}}}\right) = {T // k}({k}x+y) \]")


def m4(x, y, p, d):
    p = F(p)
    ab = F(1, x) + F(1, y)
    T_ab = 1 / ab
    c = p * T_ab
    ans = (1 - d * ab) * c
    trad = steps(("Find (A + B)'s one-day work.", rf"\[ {fr(F(1, x))} + {fr(F(1, y))} = {fr(ab)} \]so together they take {t(T_ab)} days, and C takes \({fr(p)}\times {t(T_ab)} = {t(c)}\) days."),
                 (f"Work left after {d} days.", rf"\[ 1 - {d}\times {fr(ab)} = {fr(1 - d * ab)} \]"),
                 ("C's days.", rf"\[ {fr(1 - d * ab)}\times {t(c)} = {t(ans)}\text{{ days}} \]"))
    rule = steps(("Apply the specified rule.", rf"\[ T = \frac{{xy}}{{x+y}} = \frac{{{x}\times {y}}}{{{x} + {y}}} = {t(T_ab)}\text{{ days (A + B)}} \]"),
                 ("Find C's time.", rf"\[ {fr(p)}\times {t(T_ab)} = {t(c)}\text{{ days}} \]"),
                 ("Find C's days for the rest.", rf"In {d} days A and B do \(\frac{{{d}}}{{{t(T_ab)}}} = {fr(d * ab)}\); C does \({fr(1 - d * ab)}\):<br>\[ {fr(1 - d * ab)}\times {t(c)} = {t(ans)}\text{{ days}} \]"))
    return done(("number", ans), T4, trad, rule, days(ans),
                [rf"A + B \(= \frac{{{x}\times {y}}}{{{x + y}}} = {t(T_ab)}\) days, C \(= {fr(p)}\times {t(T_ab)} = {t(c)}\) days.", rf"Left after {d} days: \({fr(1 - d * ab)}\).",
                 rf"\({fr(1 - d * ab)}\times {t(c)} = {t(ans)}\)."], rf"\[ {fr(1 - d * ab)}\times {fr(p)}\times {t(T_ab)} = {t(ans)} \]")


# ---------------------------------------------------------------- Rule 6 (other worker from the pair)
def m262(m, w, D, k, d):
    first = F(k, D)
    men_rate = (1 - first) / d
    women_rate = F(1, D) - men_rate
    W, Mt = 1 / women_rate, 1 / men_rate
    trad = steps(("Work of the whole group.", rf"{m} men and {w} women do \({fr(F(1, D))}\) a day; in {k} days \({fr(first)}\)."),
                 (f"Work of the {m} men.", rf"They do the last \({fr(1 - first)}\) in {d} days, so \({fr(men_rate)}\) a day."),
                 (f"Work of the {w} women.", rf"\[ {fr(F(1, D))} - {fr(men_rate)} = {fr(women_rate)} \;\Rightarrow\; {t(W)}\text{{ days}} \]"))
    rule = steps((f"Find the {m} men's time.", rf"\[ {d}\div {fr(1 - first)} = {t(Mt)}\text{{ days}} \]"),
                 ("Apply the specified rule.", rf"Treat the {m} men as A and the {w} women as B: together \(x = {D}\), A alone \(y = {t(Mt)}\)." + F6),
                 ("Substitute the values.", rf"\[ \frac{{{D}\times {t(Mt)}}}{{{t(Mt)} - {D}}} = {t(W)}\text{{ days}} \]"))
    return done(("number", W), T6, trad, rule, days(W),
                [rf"{m} men alone: \({d}\div {fr(1 - first)} = {t(Mt)}\) days.", rf"Women \(= \frac{{xy}}{{y-x}}\) with \(x = {D}, y = {t(Mt)}\).", rf"\(= {t(W)}\)."],
                rf"\[ \frac{{{D}\times {t(Mt)}}}{{{t(Mt)} - {D}}} = {t(W)} \]")


def m263(m, w, D, dm):
    men = F(m, dm)
    women = F(1, D) - men
    one = women / w
    Tm = F(dm, m)
    Tw = 1 / women
    trad = steps(("One man's work.", rf"\({fr(F(1, dm))}\) a day, so {m} men do \({fr(men)}\) a day."),
                 (f"{w} women's work.", rf"\[ {fr(F(1, D))} - {fr(men)} = {fr(women)}\text{{ a day}} \]"),
                 ("One woman's time.", rf"One woman does \({fr(women)}\div {w} = {fr(one)}\) a day, so {t(1 / one)} days."))
    rule = steps((f"Find the {m} men's time.", rf"\[ {dm}\div {m} = {t(Tm)}\text{{ days}} \]"),
                 ("Apply the specified rule.", rf"Together \(x = {D}\), {m} men alone \(y = {t(Tm)}\)." + F6 + rf"\[ \frac{{{D}\times {t(Tm)}}}{{{t(Tm)} - {D}}} = {t(Tw)}\text{{ days for {w} women}} \]"),
                 ("One woman.", rf"\[ {t(Tw)}\times {w} = {t(1 / one)}\text{{ days}} \]"))
    return done(("number", 1 / one), T6, trad, rule, days(1 / one),
                [rf"{m} men alone \(= {t(Tm)}\) days.", rf"{w} women \(= \frac{{{D}\times {t(Tm)}}}{{{t(Tm)} - {D}}} = {t(Tw)}\) days.", rf"One woman \(= {t(Tw)}\times {w} = {t(1 / one)}\) days."],
                rf"\[ \frac{{{D}\times {t(Tm)}}}{{{t(Tm - D)}}}\times {w} = {t(1 / one)} \]")


def m267(pa, ha, pab, hab, pb):
    sa, sab = F(pa, ha), F(pab, hab)
    sb = sab - sa
    T = pb / sb
    y, x = F(ha, pa), F(hab, pab)
    bpage = x * y / (y - x)
    trad = steps(("Pages per hour.", rf"A: \({pa}\div {ha} = {t(sa)}\) pages an hour; A and B: \({pab}\div {hab} = {t(sab)}\) pages an hour."),
                 ("B's speed.", rf"\({t(sab)} - {t(sa)} = {t(sb)}\) pages an hour."), (f"Time for {pb} pages.", rf"\[ {pb}\div {t(sb)} = {t(T)}\text{{ hours}} \]"))
    rule = steps(("Time for one page.", rf"A alone \(y = \frac{{{ha}}}{{{pa}}} = {fr(y)}\) hour a page; together \(x = \frac{{{hab}}}{{{pab}}} = {fr(x)}\) hour a page."),
                 ("Apply the specified rule.", F6 + rf"\[ \text{{B}} = \frac{{{fr(x)}\times {fr(y)}}}{{{fr(y)} - {fr(x)}}} = {fr(bpage)}\text{{ hour a page}} \]"),
                 (f"{pb} pages.", rf"\[ {pb}\times {fr(bpage)} = {t(T)}\text{{ hours}} \]"))
    return done(("number", T), T6, trad, rule, days(T, "hours"),
                [rf"Per page: A \({fr(y)}\) hour, together \({fr(x)}\) hour.", rf"B \(= \frac{{xy}}{{y-x}} = {fr(bpage)}\) hour a page.", rf"\({pb}\times {fr(bpage)} = {t(T)}\) hours."],
                rf"\[ \frac{{{fr(x)}\times {fr(y)}}}{{{fr(y)} - {fr(x)}}}\times {pb} = {t(T)} \]")


# ---------------------------------------------------------------- Rule 8, Rule 9
def m264(m, D, w, D2, part, m2, w2):
    part = F(part)
    man = F(1, m * D)
    wd = w * D2 / part                                    # woman-days for the whole job
    woman = 1 / wd
    y1 = wd / D                                           # women who finish it in D days
    assert y1.denominator == 1
    total = m2 * man + w2 * woman
    T = 1 / total
    trad = steps(("One man's and one woman's work.", rf"A man does \(\frac{{1}}{{{m}\times {D}}} = {fr(man)}\) a day. {w} women do \({fr(part)}\) in {D2} days, so the whole job in \({t(D2 / part)}\) days: a woman does \({fr(woman)}\) a day."),
                 ("The group's work.", rf"\[ \frac{{{m2}}}{{{m * D}}} + \frac{{{w2}}}{{{t(wd)}}} = {fr(total)} \]"),
                 ("Find the days.", rf"\[ 1\div {fr(total)} = {t(T)}\text{{ days}} \]"))
    rule = steps(("Make an OR-statement.", rf"The job is \({t(wd)}\) woman-days, so {t(y1)} women take {D} days: {m} men or {t(y1)} women do the job in {D} days."),
                 ("Apply the specified rule.", F8), ("Substitute the values.", rf"\[ \frac{{{D}\times {m}\times {t(y1)}}}{{{m2}\times {t(y1)} + {m}\times {w2}}} = {t(T)}\text{{ days}} \]"))
    return done(("number", T), T8, trad, rule, days(T),
                [rf"{m} men or {t(y1)} women in {D} days.", r"Days \(= \frac{Dx_1y_1}{x_2y_1 + x_1y_2}\).", rf"\(= {t(T)}\)."],
                rf"\[ \frac{{{D}\times {m}\times {t(y1)}}}{{{m2}\times {t(y1)} + {m}\times {w2}}} = {t(T)} \]")


def m265(a1, b1, h1, d1, a2, b2, h2, d2, a3, h3, d3):
    x, y = F(d1, h1), F(d2, h2)                           # days per acre for each group
    n = (y * b2 - x * b1) / (x * a1 - y * a2)            # one man = n boys
    per_acre = (a1 * n + b1) * x                          # boy-days for one acre
    boys = h3 * per_acre / d3 - a3 * n
    man_a, boy_a = n / per_acre, 1 / per_acre            # acres a day
    trad = steps(("Write the daily work in acres.", rf"Let a man plough \(M\) and a boy \(B\) acres a day:<br>\[ {d1}({a1}M + {b1}B) = {h1},\qquad {d2}({a2}M + {b2}B) = {h2} \]"),
                 ("Solve.", rf"\[ M = {fr(man_a)},\quad B = {fr(boy_a)} \]"),
                 ("Find the boys.", rf"{h3} acres in {d3} days is \({t(F(h3, d3))}\) a day; {a3} men plough \({t(a3 * man_a)}\), so the boys plough \({t(F(h3, d3) - a3 * man_a)}\): \({t(F(h3, d3) - a3 * man_a)}\div {fr(boy_a)} = {t(boys)}\) boys."))
    rule = steps(("Time per acre.", rf"Group 1 ({a1} men, {b1} boys) needs \(x = {fr(x)}\) day an acre; group 2 ({a2} men, {b2} boys) needs \(y = {fr(y)}\)."),
                 ("Apply the specified rule.", rf"\[ 1\text{{ man}} = \frac{{yb_2 - xb_1}}{{xa_1 - ya_2}} = \frac{{{fr(y)}\times {b2} - {fr(x)}\times {b1}}}{{{fr(x)}\times {a1} - {fr(y)}\times {a2}}} = {t(n)}\text{{ boys}} \]"),
                 ("Count in boys.", rf"1 acre needs \(({a1}\times {t(n)} + {b1})\times {fr(x)} = {t(per_acre)}\) boy-days, so {h3} acres need {t(h3 * per_acre)} boy-days, i.e. {t(h3 * per_acre / d3)} boys for {d3} days. {a3} men \(= {t(a3 * n)}\) boys, so \({t(h3 * per_acre / d3)} - {t(a3 * n)} = {t(boys)}\) boys."))
    return done(("number", boys), T9, trad, rule, days(boys, "boys"),
                [rf"Per acre: \(x = {fr(x)}\), \(y = {fr(y)}\) day.", rf"1 man \(= {t(n)}\) boys; 1 acre \(= {t(per_acre)}\) boy-days.", rf"\(\frac{{{t(h3 * per_acre)}}}{{{d3}}} - {t(a3 * n)} = {t(boys)}\) boys."],
                rf"\[ \frac{{{h3}\times {t(per_acre)}}}{{{d3}}} - {a3}\times {t(n)} = {t(boys)} \]")


# ---------------------------------------------------------------- Rule 14 (efficiency)
def m271(a, pct):
    b_rate = F(1, a) * F(100 + pct, 100)
    T = 1 / b_rate
    trad = steps(("A's one-day work.", rf"\({fr(F(1, a))}\)."), ("B's one-day work.", rf"\[ {fr(F(1, a))}\times\frac{{{100 + pct}}}{{100}} = {fr(b_rate)} \]"),
                 ("B's time.", rf"\[ 1\div {fr(b_rate)} = {t(T)}\text{{ days}} \]"))
    rule = steps(("Efficiencies.", rf"A \(= 100\), B \(= {100 + pct}\)."), ("Apply the specified rule.", F14),
                 ("Substitute the values.", rf"\[ 100\times {a} = {100 + pct}\times D_2 \;\Rightarrow\; D_2 = {t(T)}\text{{ days}} \]"))
    return done(("number", T), T14, trad, rule, days(T),
                [rf"Efficiencies 100 and {100 + pct}.", r"\(E_1D_1 = E_2D_2\).", rf"\(D_2 = \frac{{{100 * a}}}{{{100 + pct}}} = {t(T)}\)."], rf"\[ \frac{{{a}\times 100}}{{{100 + pct}}} = {t(T)} \]")


def m274(p, q, T):
    p, q = F(p), F(q)
    k = p / q                                             # A's daily work as a part of B's
    b = 1 / (T * (1 + k))
    n = 1 / k                                             # B is n times as good as A
    trad = steps(("Compare the daily work.", rf"A does \({fr(p)}\) of B's work in \({fr(q)}\) of the time, so A's daily work is \(\frac{{{fr(p)}}}{{{fr(q)}}} = {fr(k)}\) of B's."),
                 ("Use the time together.", rf"Let B do \(b\) a day: \[ \left(b + {fr(k)}b\right)\times {T} = 1 \;\Rightarrow\; b = {fr(b)} \]"),
                 ("B's time.", rf"{t(1 / b)} days."))
    rule = steps(("Identify \\(n\\).", rf"B does \({fr(n)}\) times as much as A, so B is \(n = {fr(n)}\) times as good; together \(x = {T}\)."),
                 ("Apply the specified rule.", r"The better workman takes \(\frac{(n+1)x}{n}\) days."),
                 ("Substitute the values.", rf"\[ \frac{{\left({fr(n)} + 1\right)\times {T}}}{{{fr(n)}}} = {t(1 / b)}\text{{ days}} \]"))
    return done(("number", 1 / b), T14, trad, rule, days(1 / b),
                [rf"B is \(n = {fr(n)}\) times as good as A; \(x = {T}\).", r"B \(= \frac{(n+1)x}{n}\).", rf"\(= {t(1 / b)}\)."],
                rf"\[ \frac{{\left({fr(n)} + 1\right)\times {T}}}{{{fr(n)}}} = {t(1 / b)} \]")


# ---------------------------------------------------------------- Rule 28 (part of the work)
def m270(alone, worked, with_d, names=("Sohan", "Mohan")):
    a, b = names
    first = F(worked, alone)
    rest = 1 - first
    T = with_d / rest
    trad = steps((f"{a}'s share.", rf"In {worked} days he does \(\frac{{{worked}}}{{{alone}}} = {fr(first)}\)."),
                 ("Work done together.", rf"The other \({fr(rest)}\) is done together in {with_d} days, so they do \({fr(rest / with_d)}\) a day."),
                 ("Time together.", rf"\[ 1\div {fr(rest / with_d)} = {t(T)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"Together they do \(\frac{{a}}{{b}} = {fr(rest)}\) in \(x = {with_d}\) days; the whole job is \(\frac{{c}}{{d}} = 1\)."),
                 ("Apply the specified rule.", r"\[ \frac{x}{a/b} = \frac{y}{c/d} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{with_d}}}{{{fr(rest)}}} = \frac{{y}}{{1}} \;\Rightarrow\; y = {t(T)}\text{{ days}} \]"))
    return done(("number", T), T28, trad, rule, days(T),
                [rf"\({fr(rest)}\) of the job in {with_d} days.", rf"\(\frac{{{with_d}}}{{{fr(rest)}}} = \frac{{y}}{{1}}\).", rf"\(y = {t(T)}\)."], rf"\[ {with_d}\div {fr(rest)} = {t(T)} \]")


def m276(h, name="Rohit", job="paint", thing="fence", left="unpainted"):
    trad = steps(("Work in one hour.", rf"{name} can {job} \(\frac{{1}}{{x}}\) of the {thing} in an hour."), (f"Work in {h} hours.", rf"\(\frac{{{h}}}{{x}}\)."),
                 ("Part left.", rf"\[ 1 - \frac{{{h}}}{{x}} = \frac{{x-{h}}}{{x}} \]"))
    rule = steps(("Identify the values.", rf"The whole {thing} (\(\frac{{a}}{{b}} = 1\)) takes \(x\) hours; find the part \(\frac{{c}}{{d}}\) done in {h} hours."),
                 ("Apply the specified rule.", rf"\[ \frac{{x}}{{1}} = \frac{{{h}}}{{c/d}} \;\Rightarrow\; \frac{{c}}{{d}} = \frac{{{h}}}{{x}} \]"),
                 ("Part left.", rf"\[ 1 - \frac{{{h}}}{{x}} = \frac{{x-{h}}}{{x}} \]"))
    return done(("expr", 1 - F(h, 7)), T28, trad, rule, rf"\(\frac{{x-{h}}}{{x}}\)",
                [rf"Whole {thing} in \(x\) hours.", rf"In {h} hours: \(\frac{{{h}}}{{x}}\).", rf"Left: \(\frac{{x-{h}}}{{x}}\)."], rf"\[ 1 - \frac{{{h}}}{{x}} = \frac{{x-{h}}}{{x}} \]")


# ---------------------------------------------------------------- Rule 31 (days worked / alone time)
def m261(m1, d1, w1, d2, m, w, t1, last):
    man_t, woman_t = m1 * d1, w1 * d2
    rate = F(m, man_t) + F(w, woman_t)
    first = t1 * rate
    left = 1 - first - last * rate
    extra = left / F(last, man_t)
    tot = t1 + last
    trad = steps(("One person's time.", rf"1 man takes \({m1}\times {d1} = {man_t}\) days and 1 woman \({w1}\times {d2} = {woman_t}\) days."),
                 (f"Work in the first {t1} days.", rf"\[ {t1}\left(\frac{{{m}}}{{{man_t}}} + \frac{{{w}}}{{{woman_t}}}\right) = {t1}\times {fr(rate)} = {fr(first)} \]"),
                 (f"The last {last} days.", rf"The {m} men and {w} women do \({last}\times {fr(rate)} = {fr(last * rate)}\), leaving \({fr(1 - first)} - {fr(last * rate)} = {fr(left)}\) for the extra men. "
                                            rf"One man does \(\frac{{{last}}}{{{man_t}}} = {fr(F(last, man_t))}\) in {last} days, so \({fr(left)}\div {fr(F(last, man_t))} = {t(extra)}\) men."))
    rule = steps(("Count each group's days.", rf"{m} men and {w} women work \({t1} + {last} = {tot}\) days; \(m\) extra men work {last} days. Alone times: man {man_t}, woman {woman_t} days."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{m}\times {tot}}}{{{man_t}}} + \frac{{{w}\times {tot}}}{{{woman_t}}} + \frac{{m\times {last}}}{{{man_t}}} = 1 \]"),
                 ("Solve.", rf"\[ {fr(F(m * tot, man_t))} + {fr(F(w * tot, woman_t))} + \frac{{{last}m}}{{{man_t}}} = 1 \;\Rightarrow\; m = {t(extra)} \]"))
    return done(("number", extra), T31, trad, rule, days(extra, "men"),
                [rf"Alone: man {man_t}, woman {woman_t} days.", rf"\(\frac{{{m}\times {tot}}}{{{man_t}}} + \frac{{{w}\times {tot}}}{{{woman_t}}} + \frac{{{last}m}}{{{man_t}}} = 1\).", rf"\(m = {t(extra)}\)."],
                rf"\[ {fr(F(m * tot, man_t))} + {fr(F(w * tot, woman_t))} + \frac{{{last}m}}{{{man_t}}} = 1 \Rightarrow m = {t(extra)} \]")


def m273(a, b, c, hours=1):
    first = F(hours, a) + F(hours, b) + F(hours, c)
    ab = F(1, a) + F(1, b)
    T = (1 - first) / ab
    trad = steps(("Work in the first hour.", rf"\[ {fr(F(1, a))} + {fr(F(1, b))} + {fr(F(1, c))} = {fr(first)} \]"),
                 ("Work left.", rf"\(1 - {fr(first)} = {fr(1 - first)}\); A and B do \({fr(F(1, a))} + {fr(F(1, b))} = {fr(ab)}\) an hour."),
                 ("Time for A and B.", rf"\[ {fr(1 - first)}\div {fr(ab)} = {t(T)}\text{{ hours}} \]"))
    rule = steps(("Count each person's hours.", r"C works 1 hour; A and B work \(1 + t\) hours."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{1 + t}}{{{a}}} + \frac{{1 + t}}{{{b}}} + \frac{{1}}{{{c}}} = 1 \]"),
                 ("Solve.", rf"\[ {fr(ab)}(1 + t) = {fr(1 - F(1, c))} \;\Rightarrow\; 1 + t = {t(1 + T)} \;\Rightarrow\; t = {t(T)}\text{{ hours}} \]"))
    return done(("number", T), T31, trad, rule, days(T, "hours"),
                [r"C works 1 hour, A and B \(1 + t\) hours.", rf"\(\frac{{1 + t}}{{{a}}} + \frac{{1 + t}}{{{b}}} + \frac{{1}}{{{c}}} = 1\).", rf"\(t = {t(T)}\) hours."],
                rf"\[ \frac{{{fr(1 - first)}}}{{{fr(ab)}}} = {t(T)} \]")


def m275(T1, kb, T2, ka=2):
    kb = F(kb)
    # a + b = 1/T1, ka a + kb b = 1/T2
    a = (F(1, T2) - kb * F(1, T1)) / (ka - kb)
    b = F(1, T1) - a
    X, Y = 1 / a, 1 / b
    trad = steps(("Write the one-day work.", rf"Let A do \(a\) and B do \(b\) a day: \({T1}(a + b) = 1\) and \({T2}\left({ka}a + {fr(kb)}b\right) = 1\)."),
                 ("Simplify.", rf"\[ a + b = {fr(F(1, T1))},\qquad {ka}a + {fr(kb)}b = {fr(F(1, T2))} \]"),
                 ("Solve.", rf"\(b = {fr(F(1, T1))} - a\), so \({ka}a + {fr(kb)}\left({fr(F(1, T1))} - a\right) = {fr(F(1, T2))}\), \(a = {fr(a)}\): A takes \({t(X)}\) days."))
    rule = steps(("Count the effective days.", rf"Let A and B take \(x\) and \(y\) days alone. In the second case A's {T2} days count as {t(ka * T2)} and B's {T2} days count as {t(kb * T2)}."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{T1}}}{{x}} + \frac{{{T1}}}{{y}} = 1,\qquad \frac{{{t(ka * T2)}}}{{x}} + \frac{{{t(kb * T2)}}}{{y}} = 1 \]"),
                 ("Solve.", rf"Eliminating \(\frac{{1}}{{y}}\) gives \(\frac{{1}}{{x}} = {fr(a)}\), so \(x = {t(X)}\) days."))
    return done(("number", X), T31, trad, rule, days(X),
                [rf"\(\frac{{{T1}}}{{x}} + \frac{{{T1}}}{{y}} = 1\), \(\frac{{{t(ka * T2)}}}{{x}} + \frac{{{t(kb * T2)}}}{{y}} = 1\).", rf"Eliminate \(\frac{{1}}{{y}}\): \(\frac{{1}}{{x}} = {fr(a)}\).", rf"\(x = {t(X)}\)."],
                rf"\[ \frac{{1}}{{x}} = {fr(a)} \Rightarrow x = {t(X)} \]")


PLAN = {
    1: [(266, "28 men can paint a stadium in 18 days. When should 21 men leave the work, if the rest of the painting is to be "
              "done in 48 days after they leave?", lambda: m266(28, 18, 21, 48), "days"),
        (268, "12 men would build a dam in 140 days. But at the end of every 5 days, 12 more men are employed. In how many days "
              "will the dam be built?", lambda: m268(12, 140, 5), "days"),
        (269, "A road was to be built in 50 days. Some men did half of the work in 30 days. Then 12 more men were put on, and "
              "the road was finished on time. How many men were employed at first?", lambda: m269(50, 30, 12), "men"),
        (272, "18 men can paint a hall in 20 days. 4 days after they started, 11 men joined them to replace 5 men. How many days "
              "will they take to finish the rest of the painting?", lambda: m272(18, 20, 4, 11, 5), "days")],
    4: [(277, "If machine A makes x toys an hour and machine B makes y toys every 3 hours, the number of toys both machines "
              "make in 12 hours is:", lambda: m277(3, 12),
         plain(r"\(12(x+y)\)", r"\(4(3x+y)\)", r"\(12x + \frac{y}{3}\)", r"\(4(x+3y)\)")),
        (1682, r"A can paint a house in 9 days and B in 18 days. C can paint it in \(\frac{2}{3}\) of the time A and B take "
               r"together. A and B paint together for 3 days and then C alone finishes the house. For how many days did C work?",
         lambda: m4(9, 18, "2/3", 3), "days")],
    6: [(262, "20 men and 14 women can build a house in 18 days. They all start together, and after 9 days the women stop "
              "working. The 20 men finish the rest in 27 days. How many days would 14 women alone take to build the whole "
              "house?", lambda: m262(20, 14, 18, 9, 27), "days"),
        (263, "9 men and 20 women can paint a school in 5 days. One man alone can paint it in 105 days. In how many days will "
              "one woman paint it alone?", lambda: m263(9, 20, 5, 105), "days"),
        (267, "A can type 60 pages in 15 hours, and A and B together can type 98 pages in 14 hours. In what time can B type 54 "
              "pages?", lambda: m267(60, 15, 98, 14, 54), "hours")],
    8: [(264, r"16 men take 15 days to paint a building, whereas 20 women in 9 days can paint \(\frac{3}{5}\) of it. How many "
              r"days will 20 men and 25 women together take to paint the building?", lambda: m264(16, 15, 20, 9, "3/5", 20, 25),
         "days")],
    9: [(265, "If 9 men and 12 boys can plough 26 acres in 2 days, and 8 men and 9 boys can plough 33 acres in 3 days, how "
              "many boys must help 10 men to plough 39 acres in 3 days?", lambda: m265(9, 12, 26, 2, 8, 9, 33, 3, 10, 39, 3), "boys")],
    14: [(271, "A can build a wall in 18 days. B is 50% more efficient than A. How many days will B take to build the same "
               "wall?", lambda: m271(18, 50), "days"),
         (274, r"A does \(\frac{2}{5}\) as much work as B in \(\frac{3}{5}\) of the time. If together they take 36 days to dig "
               r"a pond, how many days would B take to dig it alone?", lambda: m274("2/5", "3/5", 36), "days")],
    28: [(270, "Sohan can paint a house in 24 days. He worked for 16 days alone and finished the rest with Mohan in 3 days. "
               "How many days would Sohan and Mohan together take to paint the whole house?", lambda: m270(24, 16, 3), "days"),
         (276, "Rohit can paint his fence in x hours. After 3 hours it begins to rain. The unpainted part of the fence is:",
          lambda: m276(3), plain(r"\(\frac{3}{x}\)", r"\(\frac{3-x}{3}\)", r"\(\frac{x}{3}\)", r"\(\frac{x-3}{x}\)"))],
    31: [(261, "20 men can build a wall in 15 days. 30 women can build the same wall in 20 days. 10 men and 10 women started "
               "working and worked for 14 days. How many more men must be added to finish the rest of the wall in 3 days?",
          lambda: m261(20, 15, 30, 20, 10, 10, 14, 3), "men"),
         (273, "A can clean a hall in 7 hours, B in 33 hours and C in 21 hours. If C works with them for 1 hour only, how long "
               "will A and B together take to finish the cleaning?", lambda: m273(7, 33, 21), "hours"),
         (275, r"A and B working together finished painting a house in 6 days. If A had worked twice as efficiently as he did "
               r"and B \(\frac{1}{2}\) as efficiently as he did, the painting would have finished in 4 days. Find the time A "
               r"alone would take to paint the house.", lambda: m275(6, "1/2", 4), "days")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
