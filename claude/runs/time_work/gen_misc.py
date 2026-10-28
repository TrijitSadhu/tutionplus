"""The book's Miscellaneous problems (rows 261-277, copied in 2018 and never linked to a rule) are linked to the rule
each one actually uses and regenerated in the prompt #11 layout; the missing M4 is added (numbers changed) under Rule 4.
Fixes: 275's question had lost "1/3" (B worked 1/3 as efficiently - without it no option is right); 262's options did
not contain the answer (36 days); 276's option typo x-22; OCR slips. Keys come from validate.py (261, 262 had ans = 5,
268 was wrong). Works in misc/ruleNN so the finished rule folders are not touched."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
MISC = os.path.join(HERE, "misc")
sys.path.insert(0, HERE)
from common import new_question, rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_1_4 import F1, T1, T4, clean, fr, opts, result  # noqa: E402
from gen_5_10 import F6, F8, T6, T8, T9, fin_of, plain  # noqa: E402
from gen_11_20 import T14  # noqa: E402
from gen_21_30 import T28  # noqa: E402
from gen_31_35 import F31, T31  # noqa: E402

F14 = r"\[ E_1D_1 = E_2D_2 \quad\text{(efficiency }\times\text{ days is the same for the same work)} \]"


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return result(answer, theorem, trad, rule, fin, rbe(rb_steps, fin), shortcut(sc_body, fin))


# ---------------------------------------------------------------- Rule 1 (man-days)
def m266():
    W2 = F(10 * 75, 2) / (25 * 20)
    trad = steps(("Count the work in man-days.", r"\[ 25\times 20 = 500\text{ man-days} \]"),
                 ("Work done after the 15 men leave.", r"The other \(25 - 15 = 10\) men work \(37\frac{1}{2}\) days:<br>\[ 10\times 37\frac{1}{2} = 375\text{ man-days} \]"),
                 ("Find when they leave.", r"The first part needs \(500 - 375 = 125\) man-days, done by all 25 men:<br>\[ 125\div 25 = 5\text{ days} \]"))
    rule = steps(("Find the share done by the 10 men.", F1 + rf"\[ W_2 = \frac{{M_2D_2W_1}}{{M_1D_1}} = \frac{{10\times 37\frac{{1}}{{2}}\times 1}}{{25\times 20}} = {fr(W2)} \]"),
                 ("Find the share left for all 25 men.", rf"\[ 1 - {fr(W2)} = {fr(1 - W2)} \]"),
                 ("Apply the rule again.", rf"\[ D = \frac{{M_1D_1W}}{{M_2W_1}} = \frac{{25\times 20\times {fr(1 - W2)}}}{{25\times 1}} = 5\text{{ days}} \]"))
    return done(("number", F(5)), T1, trad, rule, r"\(5\) days",
                [r"10 men in \(37\frac{1}{2}\) days do \(W_2 = \frac{10\times 37.5}{25\times 20} = \frac{3}{4}\).", r"\(\frac{1}{4}\) is left for 25 men.",
                 r"\(D = 20\times\frac{1}{4} = 5\) days."], r"\[ 20\times\left(1 - \frac{10\times 37\frac{1}{2}}{25\times 20}\right) = 5 \]")


def m268():
    rows, men, total, d = [], 15, 0, 0
    while total < 3150:
        d += 10
        total += men * 10
        rows.append(rf"<tr><td>\({d - 9}\)–\({d}\)</td><td>\({men}\)</td><td>\({men * 10}\)</td><td>\({total}\)</td></tr>")
        men += 15
    table = ('<table border="1" cellpadding="4"><tr><th>Days</th><th>Men</th><th>Man-days</th><th>Total</th></tr>' + "".join(rows) + "</table>")
    trad = steps(("Count the work in man-days.", r"\[ 15\times 210 = 3150\text{ man-days} \]"), ("Add 10 days at a time.", table),
                 ("Read the answer.", rf"The total reaches 3150 at the end of day \({d}\)."))
    rule = steps(("Apply the specified rule.", F1 + r"The same work needs the same man-days: \(M_1D_1 = \) sum of men \(\times\) days in each block."),
                 ("Write the blocks.", r"\[ 150 + 300 + 450 + \dots = 150(1 + 2 + \dots + k) = 3150 \]"),
                 ("Solve.", r"\[ 1 + 2 + \dots + k = 21 = \frac{k(k+1)}{2} \;\Rightarrow\; k = 6 \]So the work takes \(6\times 10 = 60\) days."))
    return done(("number", F(60)), T1, trad, rule, r"\(60\) days",
                [r"Work \(= 15\times 210 = 3150\) man-days.", r"Blocks: \(150(1 + 2 + \dots + k) = 3150\), so \(k = 6\).", r"\(6\times 10 = 60\) days."],
                r"\[ 150\cdot\frac{k(k+1)}{2} = 3150 \Rightarrow k = 6 \Rightarrow 60 \]")


def m269():
    trad = steps(("Let the men at first be \\(M\\).", r"They did half the work in 24 days, so half the work \(= 24M\) man-days."),
                 ("The second half.", r"\(M + 16\) men did the other half in \(40 - 24 = 16\) days: \(16(M + 16)\) man-days."),
                 ("Equate the halves.", r"\[ 24M = 16(M + 16) \;\Rightarrow\; 8M = 256 \;\Rightarrow\; M = 32 \]"))
    rule = steps(("Identify the values.", r"\(M_1 = M,\ D_1 = 24,\ W_1 = \frac{1}{2}\); \(M_2 = M + 16,\ D_2 = 16,\ W_2 = \frac{1}{2}\)."),
                 ("Apply the specified rule.", F1), ("Substitute the values.", r"\[ M\times 24\times\frac{1}{2} = (M + 16)\times 16\times\frac{1}{2} \;\Rightarrow\; M = 32 \]"))
    return done(("number", F(32)), T1, trad, rule, r"\(32\) men",
                [r"Halves: \(M\) men 24 days, \(M + 16\) men 16 days.", r"\(24M = 16(M + 16)\).", r"\(M = 32\)."], r"\[ 24M = 16(M + 16) \Rightarrow M = 32 \]")


def m272():
    trad = steps(("Count the work in man-days.", r"\[ 12\times 9 = 108\text{ man-days} \]"),
                 ("Work left after 3 days.", r"\[ 108 - 12\times 3 = 72\text{ man-days} \]Now \(12 - 2 + 6 = 16\) men work."),
                 ("Find the days.", r"\[ 72\div 16 = 4\frac{1}{2}\text{ days} \]"))
    rule = steps(("Identify the values.", r"\(M_1 = 12,\ D_1 = 9,\ W_1 = 1\); \(M_2 = 16\), \(W_2 = 1 - \frac{3}{9} = \frac{2}{3}\)."),
                 ("Apply the specified rule.", F1), ("Substitute the values.", r"\[ 12\times 9\times\frac{2}{3} = 16\times D_2\times 1 \;\Rightarrow\; D_2 = \frac{72}{16} = 4\frac{1}{2} \]"))
    return done(("number", F(9, 2)), T1, trad, rule, r"\(4\frac{1}{2}\) days",
                [r"\(W_2 = \frac{2}{3}\), \(M_2 = 16\).", r"\(M_1D_1W_2 = M_2D_2W_1\).", r"\(D_2 = \frac{12\times 9\times\frac{2}{3}}{16} = 4\frac{1}{2}\)."],
                r"\[ \frac{12\times 9\times\frac{2}{3}}{16} = 4\frac{1}{2} \]")


# ---------------------------------------------------------------- Rule 4 (one-hour work adds)
def m277():
    trad = steps(("Find each factory's output in one hour.", r"A: \(x\) cars; B: \(y\) cars in 2 hours, so \(\frac{y}{2}\) cars an hour."),
                 ("Add them.", r"\[ x + \frac{y}{2} = \frac{2x + y}{2}\text{ cars an hour} \]"),
                 ("Multiply by 8 hours.", r"\[ 8\times\frac{2x + y}{2} = 4(2x + y) \]"))
    rule = steps(("Use the idea of the specified rule.", r"The rule adds one-hour (one-day) work of two workers: \(\frac{1}{x} + \frac{1}{y}\). Here the outputs per hour add the same way."),
                 ("Add the hourly outputs.", r"\[ x + \frac{y}{2} \]"), ("Multiply by the time.", r"\[ 8\left(x + \frac{y}{2}\right) = 8x + 4y = 4(2x + y) \]"))
    return done(("expr", 4 * (2 * F(7) + 3)), T4, trad, rule, r"\(4(2x+y)\)",
                [r"Per hour: \(x + \frac{y}{2}\).", r"In 8 hours: \(8\left(x + \frac{y}{2}\right)\).", r"\(= 4(2x+y)\)."], r"\[ 8\left(x + \frac{y}{2}\right) = 4(2x+y) \]")


def m4():
    ab = F(1, 10) + F(1, 15)
    c = F(4, 5) / ab
    ans = (1 - 2 * ab) * c
    trad = steps(("Find (A + B)'s one-day work.", rf"\[ {fr(F(1, 10))} + {fr(F(1, 15))} = {fr(ab)} \]so together they take 6 days, and C takes \(\frac{{4}}{{5}}\times 6 = {tex(c)}\) days."),
                 ("Work left after 2 days.", rf"\[ 1 - 2\times {fr(ab)} = {fr(1 - 2 * ab)} \]"),
                 ("C's days.", rf"\[ {fr(1 - 2 * ab)}\times {tex(c)} = {tex(ans)}\text{{ days}} \]"))
    rule = steps(("Apply the specified rule.", r"\[ T = \frac{xy}{x+y} = \frac{10\times 15}{10 + 15} = 6\text{ days (A + B)} \]"),
                 ("Find C's time.", rf"\[ \frac{{4}}{{5}}\times 6 = {tex(c)}\text{{ days}} \]"),
                 ("Find C's days for the rest.", rf"In 2 days A and B do \(\frac{{2}}{{6}} = \frac{{1}}{{3}}\); C does \(\frac{{2}}{{3}}\):<br>\[ \frac{{2}}{{3}}\times {tex(c)} = {tex(ans)}\text{{ days}} \]"))
    return done(("number", ans), T4, trad, rule, rf"\({tex(ans)}\) days",
                [r"A + B \(= \frac{10\times 15}{25} = 6\) days, C \(= \frac{4}{5}\times 6 = 4\frac{4}{5}\) days.", r"Left after 2 days: \(\frac{2}{3}\).",
                 rf"\(\frac{{2}}{{3}}\times 4\frac{{4}}{{5}} = {tex(ans)}\)."], rf"\[ \frac{{2}}{{3}}\times\frac{{4}}{{5}}\times 6 = {tex(ans)} \]")


# ---------------------------------------------------------------- Rule 6 (other worker from the pair)
def m262():
    trad = steps(("Work of the whole group.", r"25 men and 15 women do \(\frac{1}{12}\) a day; in 8 days \(\frac{8}{12} = \frac{2}{3}\)."),
                 ("Work of the 25 men.", r"They do the last \(\frac{1}{3}\) in 6 days, so \(\frac{1}{18}\) a day."),
                 ("Work of the 15 women.", r"\[ \frac{1}{12} - \frac{1}{18} = \frac{1}{36} \;\Rightarrow\; 36\text{ days} \]"))
    rule = steps(("Find the 25 men's time.", r"\[ 6\div\frac{1}{3} = 18\text{ days} \]"),
                 ("Apply the specified rule.", r"Treat the 25 men as A and the 15 women as B: together \(x = 12\), A alone \(y = 18\)." + F6),
                 ("Substitute the values.", r"\[ \frac{12\times 18}{18 - 12} = \frac{216}{6} = 36\text{ days} \]"))
    return done(("number", F(36)), T6, trad, rule, r"\(36\) days",
                [r"25 men alone: \(6\div\frac{1}{3} = 18\) days.", r"Women \(= \frac{xy}{y-x}\) with \(x = 12, y = 18\).", r"\(\frac{216}{6} = 36\)."], r"\[ \frac{12\times 18}{18 - 12} = 36 \]")


def m263():
    trad = steps(("One man's work.", r"\(\frac{1}{100}\) a day, so 10 men do \(\frac{10}{100} = \frac{1}{10}\) a day."),
                 ("15 women's work.", r"\[ \frac{1}{6} - \frac{1}{10} = \frac{1}{15}\text{ a day} \]"),
                 ("One woman's time.", r"One woman does \(\frac{1}{15}\div 15 = \frac{1}{225}\) a day, so 225 days."))
    rule = steps(("Find the 10 men's time.", r"\[ 100\div 10 = 10\text{ days} \]"),
                 ("Apply the specified rule.", r"Together \(x = 6\), 10 men alone \(y = 10\)." + F6 + r"\[ \frac{6\times 10}{10 - 6} = 15\text{ days for 15 women} \]"),
                 ("One woman.", r"\[ 15\times 15 = 225\text{ days} \]"))
    return done(("number", F(225)), T6, trad, rule, r"\(225\) days",
                [r"10 men alone \(= 10\) days.", r"15 women \(= \frac{6\times 10}{10 - 6} = 15\) days.", r"One woman \(= 15\times 15 = 225\) days."], r"\[ \frac{6\times 10}{4}\times 15 = 225 \]")


def m267():
    trad = steps(("Pages per hour.", r"A: \(75\div 25 = 3\) pages an hour; A and B: \(135\div 27 = 5\) pages an hour."),
                 ("B's speed.", r"\(5 - 3 = 2\) pages an hour."), ("Time for 42 pages.", r"\[ 42\div 2 = 21\text{ hours} \]"))
    rule = steps(("Time for one page.", r"A alone \(y = \frac{25}{75} = \frac{1}{3}\) hour a page; together \(x = \frac{27}{135} = \frac{1}{5}\) hour a page."),
                 ("Apply the specified rule.", F6 + r"\[ \text{B} = \frac{\frac{1}{5}\times\frac{1}{3}}{\frac{1}{3} - \frac{1}{5}} = \frac{\frac{1}{15}}{\frac{2}{15}} = \frac{1}{2}\text{ hour a page} \]"),
                 ("42 pages.", r"\[ 42\times\frac{1}{2} = 21\text{ hours} \]"))
    return done(("number", F(21)), T6, trad, rule, r"\(21\) hours",
                [r"Per page: A \(\frac{1}{3}\) hour, together \(\frac{1}{5}\) hour.", r"B \(= \frac{xy}{y-x} = \frac{1}{2}\) hour a page.", r"\(42\times\frac{1}{2} = 21\) hours."],
                r"\[ \frac{\frac{1}{5}\times\frac{1}{3}}{\frac{1}{3} - \frac{1}{5}}\times 42 = 21 \]")


# ---------------------------------------------------------------- Rule 8, Rule 9
def m264():
    trad = steps(("One man's and one woman's work.", r"A man does \(\frac{1}{12\times 18} = \frac{1}{216}\) a day. 12 women do \(\frac{3}{4}\) in 18 days, so the whole job in 24 days: a woman does \(\frac{1}{288}\) a day."),
                 ("The group's work.", r"\[ \frac{10}{216} + \frac{8}{288} = \frac{5}{108} + \frac{3}{108} = \frac{2}{27} \]"),
                 ("Find the days.", r"\[ 1\div\frac{2}{27} = 13\frac{1}{2}\text{ days} \]"))
    rule = steps(("Make an OR-statement.", r"12 women take 24 days, so 16 women take 18 days: 12 men or 16 women do the job in 18 days."),
                 ("Apply the specified rule.", F8), ("Substitute the values.", r"\[ \frac{18\times 12\times 16}{10\times 16 + 12\times 8} = \frac{3456}{256} = 13\frac{1}{2}\text{ days} \]"))
    return done(("number", F(27, 2)), T8, trad, rule, r"\(13\frac{1}{2}\) days",
                [r"12 men or 16 women in 18 days.", r"Days \(= \frac{Dx_1y_1}{x_2y_1 + x_1y_2}\).", r"\(\frac{3456}{256} = 13\frac{1}{2}\)."], r"\[ \frac{18\times 12\times 16}{10\times 16 + 12\times 8} = 13\frac{1}{2} \]")


def m265():
    trad = steps(("Write the daily work in hectares.", r"Let a man reap \(M\) and a boy \(B\) hectares a day:<br>\[ 4(5M + 3B) = 23,\qquad 2(3M + 2B) = 7 \]"),
                 ("Solve.", r"\[ 20M + 12B = 23,\quad 18M + 12B = 21 \;\Rightarrow\; 2M = 2,\ M = 1,\ B = \frac{1}{4} \]"),
                 ("Find the boys.", r"45 hectares in 6 days is \(7\frac{1}{2}\) a day; 7 men reap 7, so the boys reap \(\frac{1}{2}\): \(\frac{1}{2}\div\frac{1}{4} = 2\) boys."))
    rule = steps(("Time per hectare.", r"Group 1 (5 men, 3 boys) needs \(x = \frac{4}{23}\) day a hectare; group 2 (3 men, 2 boys) needs \(y = \frac{2}{7}\)."),
                 ("Apply the specified rule.", r"\[ 1\text{ man} = \frac{yb_2 - xb_1}{xa_1 - ya_2} = \frac{\frac{2}{7}\times 2 - \frac{4}{23}\times 3}{\frac{4}{23}\times 5 - \frac{2}{7}\times 3} = \frac{\frac{8}{161}}{\frac{2}{161}} = 4\text{ boys} \]"),
                 ("Count in boys.", r"1 hectare needs \((5\times 4 + 3)\times\frac{4}{23} = 4\) boy-days, so 45 hectares need 180 boy-days, i.e. 30 boys for 6 days. 7 men \(= 28\) boys, so \(30 - 28 = 2\) boys."))
    return done(("number", F(2)), T9, trad, rule, r"\(2\) boys",
                [r"Per hectare: \(x = \frac{4}{23}\), \(y = \frac{2}{7}\) day.", r"1 man \(= 4\) boys; 1 hectare \(= 4\) boy-days.", r"\(\frac{180}{6} - 28 = 2\) boys."],
                r"\[ \frac{45\times 4}{6} - 7\times 4 = 2 \]")


# ---------------------------------------------------------------- Rule 14 (efficiency)
def m271():
    trad = steps(("A's one-day work.", r"\(\frac{1}{12}\)."), ("B's one-day work.", r"\[ \frac{1}{12}\times\frac{160}{100} = \frac{2}{15} \]"),
                 ("B's time.", r"\[ 1\div\frac{2}{15} = 7\frac{1}{2}\text{ days} \]"))
    rule = steps(("Efficiencies.", r"A \(= 100\), B \(= 160\)."), ("Apply the specified rule.", F14),
                 ("Substitute the values.", r"\[ 100\times 12 = 160\times D_2 \;\Rightarrow\; D_2 = 7\frac{1}{2}\text{ days} \]"))
    return done(("number", F(15, 2)), T14, trad, rule, r"\(7\frac{1}{2}\) days",
                [r"Efficiencies 100 and 160.", r"\(E_1D_1 = E_2D_2\).", r"\(D_2 = \frac{1200}{160} = 7\frac{1}{2}\)."], r"\[ \frac{12\times 100}{160} = 7\frac{1}{2} \]")


def m274():
    trad = steps(("Compare the daily work.", r"A does \(\frac{1}{2}\) of B's work in \(\frac{3}{4}\) of the time, so A's daily work is \(\frac{1/2}{3/4} = \frac{2}{3}\) of B's."),
                 ("Use the time together.", r"Let B do \(b\) a day: \[ \left(b + \frac{2}{3}b\right)\times 18 = 1 \;\Rightarrow\; b = \frac{1}{30} \]"),
                 ("B's time.", r"30 days."))
    rule = steps(("Identify \\(n\\).", r"B does \(\frac{3}{2}\) times as much as A, so B is \(n = \frac{3}{2}\) times as good; together \(x = 18\)."),
                 ("Apply the specified rule.", r"The better workman takes \(\frac{(n+1)x}{n}\) days."),
                 ("Substitute the values.", r"\[ \frac{\left(\frac{3}{2} + 1\right)\times 18}{\frac{3}{2}} = \frac{45}{\frac{3}{2}} = 30\text{ days} \]"))
    return done(("number", F(30)), T14, trad, rule, r"\(30\) days",
                [r"B is \(n = \frac{3}{2}\) times as good as A; \(x = 18\).", r"B \(= \frac{(n+1)x}{n}\).", r"\(\frac{45}{3/2} = 30\)."], r"\[ \frac{(1.5 + 1)\times 18}{1.5} = 30 \]")


# ---------------------------------------------------------------- Rule 28 (part of the work)
def m270():
    trad = steps(("Ramesh's share.", r"In 10 days he does \(\frac{10}{20} = \frac{1}{2}\)."),
                 ("Work done together.", r"The other \(\frac{1}{2}\) is done together in 2 days, so they do \(\frac{1}{4}\) a day."),
                 ("Time together.", r"\[ 1\div\frac{1}{4} = 4\text{ days} \]"))
    rule = steps(("Identify the values.", r"Together they do \(\frac{a}{b} = \frac{1}{2}\) in \(x = 2\) days; the whole job is \(\frac{c}{d} = 1\)."),
                 ("Apply the specified rule.", r"\[ \frac{x}{a/b} = \frac{y}{c/d} \]"),
                 ("Substitute the values.", r"\[ \frac{2}{1/2} = \frac{y}{1} \;\Rightarrow\; y = 4\text{ days} \]"))
    return done(("number", F(4)), T28, trad, rule, r"\(4\) days",
                [r"\(\frac{1}{2}\) of the job in 2 days.", r"\(\frac{2}{1/2} = \frac{y}{1}\).", r"\(y = 4\)."], r"\[ 2\div\frac{1}{2} = 4 \]")


def m276():
    trad = steps(("Work in one hour.", r"Mohan mows \(\frac{1}{x}\) of the lawn in an hour."), ("Work in 2 hours.", r"\(\frac{2}{x}\)."),
                 ("Part left.", r"\[ 1 - \frac{2}{x} = \frac{x-2}{x} \]"))
    rule = steps(("Identify the values.", r"The whole lawn (\(\frac{a}{b} = 1\)) takes \(x\) hours; find the part \(\frac{c}{d}\) done in 2 hours."),
                 ("Apply the specified rule.", r"\[ \frac{x}{1} = \frac{2}{c/d} \;\Rightarrow\; \frac{c}{d} = \frac{2}{x} \]"),
                 ("Part left.", r"\[ 1 - \frac{2}{x} = \frac{x-2}{x} \]"))
    return done(("expr", F(5, 7)), T28, trad, rule, r"\(\frac{x-2}{x}\)",
                [r"Whole lawn in \(x\) hours.", r"In 2 hours: \(\frac{2}{x}\).", r"Left: \(\frac{x-2}{x}\)."], r"\[ 1 - \frac{2}{x} = \frac{x-2}{x} \]")


# ---------------------------------------------------------------- Rule 31 (days worked / alone time)
def m261():
    trad = steps(("One person's time.", r"1 man takes \(24\times 16 = 384\) days and 1 woman \(32\times 24 = 768\) days."),
                 ("Work in the first 12 days.", r"\[ 12\left(\frac{16}{384} + \frac{16}{768}\right) = 12\times\frac{3}{48} = \frac{3}{4} \]"),
                 ("The last 2 days.", r"The 16 men and 16 women do \(2\times\frac{3}{48} = \frac{1}{8}\), leaving \(\frac{1}{4} - \frac{1}{8} = \frac{1}{8}\) for the extra men. "
                                      r"One man does \(\frac{2}{384} = \frac{1}{192}\) in 2 days, so \(\frac{1}{8}\div\frac{1}{192} = 24\) men."))
    rule = steps(("Count each group's days.", r"16 men and 16 women work \(12 + 2 = 14\) days; \(m\) extra men work 2 days. Alone times: man 384, woman 768 days."),
                 ("Apply the specified rule.", F31 + r"\[ \frac{16\times 14}{384} + \frac{16\times 14}{768} + \frac{m\times 2}{384} = 1 \]"),
                 ("Solve.", r"\[ \frac{7}{12} + \frac{7}{24} + \frac{m}{192} = 1 \;\Rightarrow\; \frac{m}{192} = \frac{1}{8} \;\Rightarrow\; m = 24 \]"))
    return done(("number", F(24)), T31, trad, rule, r"\(24\) men",
                [r"Alone: man 384, woman 768 days.", r"\(\frac{16\times 14}{384} + \frac{16\times 14}{768} + \frac{2m}{384} = 1\).", r"\(m = 24\)."],
                r"\[ \frac{7}{12} + \frac{7}{24} + \frac{m}{192} = 1 \Rightarrow m = 24 \]")


def m273():
    trad = steps(("Work in the first hour.", r"\[ \frac{1}{5} + \frac{1}{9} + \frac{1}{15} = \frac{9 + 5 + 3}{45} = \frac{17}{45} \]"),
                 ("Work left.", r"\(1 - \frac{17}{45} = \frac{28}{45}\); A and B do \(\frac{1}{5} + \frac{1}{9} = \frac{14}{45}\) an hour."),
                 ("Time for A and B.", r"\[ \frac{28}{45}\div\frac{14}{45} = 2\text{ hours} \]"))
    rule = steps(("Count each person's hours.", r"C works 1 hour; A and B work \(1 + t\) hours."),
                 ("Apply the specified rule.", F31 + r"\[ \frac{1 + t}{5} + \frac{1 + t}{9} + \frac{1}{15} = 1 \]"),
                 ("Solve.", r"\[ \frac{14(1 + t)}{45} = \frac{14}{15} \;\Rightarrow\; 1 + t = 3 \;\Rightarrow\; t = 2\text{ hours} \]"))
    return done(("number", F(2)), T31, trad, rule, r"\(2\) hours",
                [r"C works 1 hour, A and B \(1 + t\) hours.", r"\(\frac{1 + t}{5} + \frac{1 + t}{9} + \frac{1}{15} = 1\).", r"\(t = 2\) hours."], r"\[ \frac{28/45}{14/45} = 2 \]")


def m275():
    trad = steps(("Write the one-day work.", r"Let A do \(a\) and B do \(b\) a day: \(5(a + b) = 1\) and \(3\left(2a + \frac{b}{3}\right) = 1\)."),
                 ("Simplify.", r"\[ a + b = \frac{1}{5},\qquad 2a + \frac{b}{3} = \frac{1}{3} \]"),
                 ("Solve.", r"\(b = \frac{1}{5} - a\), so \(2a + \frac{1}{15} - \frac{a}{3} = \frac{1}{3}\), \(\frac{5a}{3} = \frac{4}{15}\), \(a = \frac{4}{25}\): A takes \(6\frac{1}{4}\) days."))
    rule = steps(("Count the effective days.", r"Let A and B take \(x\) and \(y\) days alone. In the second case A's 3 days count as 6 and B's 3 days count as 1."),
                 ("Apply the specified rule.", F31 + r"\[ \frac{5}{x} + \frac{5}{y} = 1,\qquad \frac{6}{x} + \frac{1}{y} = 1 \]"),
                 ("Solve.", r"From the second, \(\frac{1}{y} = 1 - \frac{6}{x}\); then \(\frac{5}{x} + 5 - \frac{30}{x} = 1\), so \(\frac{25}{x} = 4\) and \(x = 6\frac{1}{4}\) days."))
    return done(("number", F(25, 4)), T31, trad, rule, r"\(6\frac{1}{4}\) days",
                [r"\(\frac{5}{x} + \frac{5}{y} = 1\), \(\frac{6}{x} + \frac{1}{y} = 1\).", r"Eliminate \(\frac{1}{y}\): \(\frac{25}{x} = 4\).", r"\(x = 6\frac{1}{4}\)."],
                r"\[ \frac{25}{x} = 4 \Rightarrow x = 6\frac{1}{4} \]")


# ---------------------------------------------------------------- text fixes and plan
BOOK_Q = {
    262: lambda q: q + "?",
    264: lambda q: q.replace(r"\[ \frac{3}{4} \] of", r"\(\frac{3}{4}\) of"),
    265: lambda q: q + "?",
    266: lambda q: q.replace(r"37\[ \frac{1}{2} \] days", r"\(37\frac{1}{2}\) days"),
    270: lambda q: q.replace("finish ajob", "finish a job"),
    272: lambda q: q.replace("After 3 days they started the work, 6 men joined", "3 days after they started the work, 6 men joined"),
    275: lambda q: q.replace("B worked as efficiently as he actually did", r"B worked \(\frac{1}{3}\) as efficiently as he actually did"),
    276: lambda q: q.replace("The unmoved part of the lawn in", "The unmowed part of the lawn is:"),
    277: lambda q: q + ":",
}
BOOK_OPTS = {
    261: opts("men", 48, 24, 36, 28), 262: opts("days", 60, 88, 94, 36), 263: opts("days", 125, 150, 90, 225),
    264: opts("days", 6, r"13\frac{1}{2}", 12, 8), 265: opts("boys", 2, 6, 4, 5), 266: opts("days", 6, 4, 5, 3),
    267: plain(r"\(21\) hours", r"\(5\) hours \(36\) seconds", r"\(18\) hours", r"\(24\) hours"),
    268: opts("days", 30, 70, 35, 60), 269: opts("men", 16, 32, 24, 48), 270: opts("days", 4, 5, 10, 12),
    271: opts("days", r"7\frac{1}{2}", r"6\frac{1}{4}", 8, 6), 272: opts("days", 2, 3, 4, r"4\frac{1}{2}"),
    273: opts("hours", 2, 3, r"3\frac{1}{2}", 4), 274: opts("days", 40, 35, 30, 38),
    275: opts("days", r"6\frac{1}{2}", r"6\frac{1}{4}", r"6\frac{3}{4}", r"12\frac{1}{2}"),
    276: plain(r"\(\frac{2}{x}\)", r"\(\frac{2-x}{2}\)", r"\(\frac{x}{2}\)", r"\(\frac{x-2}{x}\)"),
    277: plain(r"\(8(x+y)\)", r"\(8x + \frac{y}{2}\)", r"\(16(x+y)\)", r"\(4(2x+y)\)"),
}
PLAN = {1: (43, {266: m266, 268: m268, 269: m269, 272: m272}), 4: (50, {277: m277}), 6: (52, {262: m262, 263: m263, 267: m267}),
        8: (54, {264: m264}), 9: (55, {265: m265}), 14: (60, {271: m271, 274: m274}), 28: (74, {270: m270, 276: m276}),
        31: (77, {261: m261, 273: m273, 275: m275})}
NEW4 = ("m4", r"A can do a piece of work in 10 days and B in 15 days. C can do the same work in \(\frac{4}{5}\) of the time A and B take "
              "working together. A and B work together for 2 days and then C alone completes the work. For how many days did C work?",
        m4, opts("days", 3, r"3\frac{1}{5}", 4, r"2\frac{2}{5}"), 2)


def main():
    for n, (card_id, plan) in PLAN.items():
        folder = os.path.join(MISC, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"]["id"] == card_id
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(plan)
        out = []
        for rid, fn in plan.items():
            q = clean(rows[rid]["question"])
            extra = {"question": BOOK_Q[rid](q) if rid in BOOK_Q else q, **BOOK_OPTS[rid]}
            assert "\\[" not in extra["question"], rid
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), card_id, extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(os.path.join(folder, "solve.py"), "w").write("from solve_misc import solve  # noqa: F401\n")
        print(f"misc Rule {n}: {len(out)} rows regenerated")
        if n == 4:
            key, text, fn, op, pos = NEW4
            g = fn()
            q = new_question(4, text, [op[k] for k in "abcd"], pos, g["solution"], g["rbe"], g["shortcut"])
            json.dump({"rules_html": [{"chapter": "time_n_work", "rule_name": "Rule 4", "rule_html": dump["rule_card"]["rule_html"]}], "questions": [q]},
                      open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump([[key, [g["answer"][0], str(g["answer"][1])]]], open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2)
            print("misc Rule 4: M4 added")


if __name__ == "__main__":
    main()
