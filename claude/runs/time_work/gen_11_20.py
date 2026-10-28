"""Rules 11-20: regenerates every row (book worked examples and exercises copied in 2018 + reworded exercises) in the
prompt #11 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links the 2018 book
copies to their rule card and cleans their text. The answer keys are not set here: validate.py re-solves every question
and stores the key of the one option holding the answer (all four reworded Rule 18 rows had a wrong key).
Also writes the Rule 19 card fix. Writes ruleNN/2_new_rows.json and rule19/3_rule_card.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_1_4 import R, clean, fr, opts, result  # noqa: E402
from gen_5_10 import fin_of, plain, recip, show, times9  # noqa: E402

WORD = {2: "twice", 3: "thrice"}


# ---------------------------------------------------------------- Rule 11: Dn/(n^2 - 1)
T11 = (r"If A is \(n\) times as fast as B and is therefore able to finish a work in \(D\) days less than B, then A and B working "
       r"together finish it in<br>\[ \frac{Dn}{n^2-1}\text{ days} \]")


def faster11(n, D):
    n, D = R(n, D)
    a = D / (n - 1)
    b = n * a
    s = 1 / a + 1 / b
    T = D * n / (n * n - 1)
    trad = steps(
        ("Find each person's time.", rf"A is \({tex(n)}\) times as fast, so if A takes \(t\) days, B takes \({tex(n)}t\) days. The difference is \({tex(D)}\) days:<br>"
                                     rf"\[ {tex(n)}t - t = {tex(D)} \;\Rightarrow\; t = {tex(a)} \]So A takes \({tex(a)}\) days and B takes \({tex(b)}\) days."),
        ("Add the one-day work.", rf"\[ {fr(1 / a)} + {fr(1 / b)} = {fr(s)} \]"),
        ("Find the time together.", recip(s, "days")))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(D = {tex(D)}\)."),
                 ("Apply the specified rule.", r"\[ T = \frac{Dn}{n^2-1} \]"),
                 ("Substitute the values.", rf"\[ T = \frac{{{tex(D)}\times {tex(n)}}}{{{tex(n)}^2 - 1}} = \frac{{{tex(D * n)}}}{{{tex(n * n - 1)}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(n = {tex(n)}, D = {tex(D)}\).", r"\(T = \frac{Dn}{n^2-1}\).", rf"\(T = \frac{{{tex(D * n)}}}{{{tex(n * n - 1)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(D)}\times {tex(n)}}}{{{tex(n)}^2 - 1}} = {tex(T)} \]", fin)
    return result(("number", T), T11, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 12: different hours a day
T12 = (r"If a person can finish a work in \(d_1\) days at \(h_1\) hours a day and another person can finish the same work in \(d_2\) days at "
       r"\(h_2\) hours a day, then working together \(h\) hours a day they finish it in<br>\[ \frac{(h_1d_1)(h_2d_2)}{(h_1d_1)+(h_2d_2)}\times\frac{1}{h}\text{ days} \]")


def hours12(d1, h1, d2, h2, h, improper=False):
    d1, h1, d2, h2, h = R(d1, h1, d2, h2, h)
    p, q = h1 * d1, h2 * d2
    s = 1 / p + 1 / q
    T = p * q / (p + q) / h
    trad = steps(
        ("Count each person's working hours.", rf"I need \({tex(d1)}\times {tex(h1)} = {tex(p)}\) hours and you need \({tex(d2)}\times {tex(h2)} = {tex(q)}\) hours for the work."),
        ("Find the work done in one hour together.", rf"\[ {fr(1 / p)} + {fr(1 / q)} = {fr(s)} \]Working \({tex(h)}\) hours a day we do \({tex(h)}\times {fr(s)} = {fr(s * h)}\) of the work a day."),
        ("Find the days.", recip(s * h, "days", improper)))
    rule = steps(("Identify the values.", rf"\(h_1d_1 = {tex(p)}\), \(h_2d_2 = {tex(q)}\), \(h = {tex(h)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Days} = \frac{(h_1d_1)(h_2d_2)}{(h_1d_1)+(h_2d_2)}\times\frac{1}{h} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(p)}\times {tex(q)}}}{{{tex(p)} + {tex(q)}}}\times\frac{{1}}{{{tex(h)}}} = \frac{{{tex(p * q / (p + q))}}}{{{tex(h)}}} = {show(T, improper)}\text{{ days}} \]"))
    fin = fin_of(T, "days", improper)
    rb = rbe([rf"\(h_1d_1 = {tex(p)}\), \(h_2d_2 = {tex(q)}\), \(h = {tex(h)}\).", r"Days \(= \frac{(h_1d_1)(h_2d_2)}{(h_1d_1)+(h_2d_2)}\times\frac{1}{h}\).",
              rf"\(\frac{{{tex(p * q / (p + q))}}}{{{tex(h)}}} = {show(T, improper)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(p)}\times {tex(q)}}}{{{tex(p)} + {tex(q)}}}\times\frac{{1}}{{{tex(h)}}} = {show(T, improper)} \]", fin)
    return result(("number", T), T12, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 13: C as long as A and B together
T13 = (r"If A can do a work in \(x\) days, B takes \(y\) days and C takes as long as A and B would take working together, then"
       r"<br>\[ \text{B + C} = \frac{xy}{2x+y},\qquad \text{A + C} = \frac{xy}{x+2y},\qquad \text{A + B + C} = \frac{xy}{2(x+y)}\text{ days} \]")
F13 = {"bc": (r"\frac{xy}{2x+y}", lambda x, y: (2 * x + y, rf"2\times {tex(x)} + {tex(y)}")),
       "ac": (r"\frac{xy}{x+2y}", lambda x, y: (x + 2 * y, rf"{tex(x)} + 2\times {tex(y)}")),
       "abc": (r"\frac{xy}{2(x+y)}", lambda x, y: (2 * (x + y), rf"2({tex(x)} + {tex(y)})"))}
NAME13 = {"bc": "B and C", "ac": "A and C", "abc": "A, B and C"}


def c_ab13(x, y, which):
    x, y = R(x, y)
    a, b = 1 / x, 1 / y
    c = a + b
    s = {"bc": b + c, "ac": a + c, "abc": a + b + c}[which]
    parts = {"bc": rf"{fr(b)} + {fr(c)}", "ac": rf"{fr(a)} + {fr(c)}", "abc": rf"{fr(a)} + {fr(b)} + {fr(c)}"}[which]
    trad = steps(
        ("Find C's one-day work.", rf"C takes as long as A and B together, so C does as much in a day as A and B:<br>\[ \text{{C}} = {fr(a)} + {fr(b)} = {fr(c)} \]"),
        (f"Add the work of {NAME13[which]}.", rf"\[ {parts} = {fr(s)} \]"),
        ("Find the time.", recip(s, "days")))
    form, den = F13[which]
    d, dtxt = den(x, y)
    T = x * y / d
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
                 ("Apply the specified rule.", rf"\[ \text{{{NAME13[which]}}} = {form} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{dtxt}}} = \frac{{{tex(x * y)}}}{{{tex(d)}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"{NAME13[which]} together \(= {form}\).", rf"\(\frac{{{tex(x * y)}}}{{{tex(d)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{dtxt}}} = {tex(T)} \]", fin)
    return result(("number", T), T13, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 14: A n times as good as B
T14 = (r"If A is \(n\) times as good a workman as B and together they finish the work in \(x\) days, then A and B separately can do the "
       r"same work in<br>\[ \text{A} = \frac{(n+1)x}{n}\text{ days},\qquad \text{B} = (n+1)x\text{ days} \]")


def good14(n, x, both=False):
    n, x = R(n, x)
    b = 1 / (x * (n + 1))
    A, B = (n + 1) * x / n, (n + 1) * x
    trad = steps(
        ("Write the one-day work.", rf"Let B do \(b\) of the work in a day; A does \({tex(n)}b\). Together they finish in \({tex(x)}\) days:<br>"
                                    rf"\[ ({tex(n)}b + b)\times {tex(x)} = 1 \;\Rightarrow\; b = {fr(b)} \]"),
        ("Find B's time.", rf"\[ 1\div {fr(b)} = {tex(1 / b)}\text{{ days}} \]"),
        ("Find A's time.", rf"A does \({tex(n)}\times {fr(b)} = {fr(n * b)}\) a day:<br>" + recip(n * b, "days")))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {tex(x)}\)."),
                 ("Apply the specified rule.", r"\[ \text{A} = \frac{(n+1)x}{n},\qquad \text{B} = (n+1)x \]"),
                 ("Substitute the values.", rf"\[ \text{{A}} = \frac{{({tex(n)} + 1)\times {tex(x)}}}{{{tex(n)}}} = {tex(A)},\qquad \text{{B}} = ({tex(n)} + 1)\times {tex(x)} = {tex(B)} \]"))
    if both:
        fin, ans = rf"A \({tex(A)}\) days, B \({tex(B)}\) days", ("pair", (A, B))
    else:
        fin, ans = fin_of(A, "days"), ("number", A)
    rb = rbe([rf"\(n = {tex(n)}, x = {tex(x)}\).", r"A \(= \frac{(n+1)x}{n}\), B \(= (n+1)x\).", rf"A \(= {tex(A)}\), B \(= {tex(B)}\)."], fin)
    sc = shortcut(rf"\[ \text{{A}} = \frac{{{tex((n + 1) * x)}}}{{{tex(n)}}} = {tex(A)}" + (rf",\quad \text{{B}} = {tex(B)}" if both else "") + r" \]", fin)
    return result(ans, T14, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 15: man : boy from "n times as much work"
T15 = (r"If \(a_1\) men and \(b_1\) boys working together can do \(n\) times as much work per hour as \(a_2\) men and \(b_2\) boys together, then"
       r"<br>\[ \frac{\text{Man}}{\text{Boy}} = \frac{nb_2 - b_1}{a_1 - na_2} \]")


def times15(a1, b1, n, a2=1, b2=1):
    g = times9(a1, b1, n, a2, b2)
    k = F(n * b2 - b1, a1 - n * a2)
    p, q = k.numerator, k.denominator
    rule = steps(("Identify the values.", rf"\(a_1 = {a1}, b_1 = {b1}, n = {n}, a_2 = {a2}, b_2 = {b2}\)."),
                 ("Apply the specified rule.", r"\[ \frac{\text{Man}}{\text{Boy}} = \frac{nb_2 - b_1}{a_1 - na_2} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{n}\times {b2} - {b1}}}{{{a1} - {n}\times {a2}}} = \frac{{{n * b2 - b1}}}{{{a1 - n * a2}}}"
                                            + ("" if (p, q) == (n * b2 - b1, a1 - n * a2) else rf" = \frac{{{p}}}{{{q}}}") + rf" \]So man : boy \(= {p} : {q}\)."))
    s = g["solution"]
    head = "<b>Theorem :</b> "
    s = s.replace(s[s.index(head) + len(head):s.index("<hr>")], T15, 1)
    i = s.index("<b>Using the Specified Rule :</b><br><br>") + len("<b>Using the Specified Rule :</b><br><br>")
    j = s.index("<br><br><b>Verification:</b>")
    g["solution"] = s[:i] + rule + s[j:]
    g["rbe"] = rbe([rf"\(a_1 = {a1}, b_1 = {b1}, n = {n}, a_2 = {a2}, b_2 = {b2}\).", r"\(\frac{\text{Man}}{\text{Boy}} = \frac{nb_2 - b_1}{a_1 - na_2}\).",
                    rf"\(\frac{{{n * b2 - b1}}}{{{a1 - n * a2}}}\), so man : boy \(= {p} : {q}\)."], rf"\({p} : {q}\)")
    return g


# ---------------------------------------------------------------- Rule 16: A leaves, B finishes in z days
T16 = (r"If A and B can do a work in \(x\) and \(y\) days respectively, they begin together, A leaves after some time and B finishes the "
       r"remaining work in \(z\) days, then A left after<br>\[ \left(\frac{xy}{x+y}\right)\left(\frac{y-z}{y}\right)\text{ days} \]")
F16 = r"\[ t = \left(\frac{xy}{x+y}\right)\left(\frac{y-z}{y}\right) \]"


def left16(x, y, z):
    x, y, z = R(x, y, z)
    done_b = z / y
    s = 1 / x + 1 / y
    t = (1 - done_b) / s
    trad = steps(
        ("Find B's share at the end.", rf"B works alone \({tex(z)}\) days: \({tex(z)}\times {fr(1 / y)} = {fr(done_b)}\) of the work."),
        ("Find the share done together.", rf"\[ 1 - {fr(done_b)} = {fr(1 - done_b)} \]Together they do \({fr(1 / x)} + {fr(1 / y)} = {fr(s)}\) a day."),
        ("Find the days together.", rf"\[ {fr(1 - done_b)}\div {fr(s)} = {tex(t)}\text{{ days}} \]So A left after \({tex(t)}\) days."))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."), ("Apply the specified rule.", F16),
                 ("Substitute the values.", rf"\[ t = \left(\frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}}\right)\left(\frac{{{tex(y)} - {tex(z)}}}{{{tex(y)}}}\right) "
                                            rf"= {tex(x * y / (x + y))}\times {fr((y - z) / y)} = {tex(t)}\text{{ days}} \]"))
    fin = fin_of(t, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\).", r"\(t = \frac{xy}{x+y}\cdot\frac{y-z}{y}\).", rf"\(t = {tex(x * y / (x + y))}\times {fr((y - z) / y)} = {tex(t)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}}\times\frac{{{tex(y)} - {tex(z)}}}{{{tex(y)}}} = {tex(t)} \]", fin)
    return result(("number", t), T16, trad, rule, fin, rb, sc)


def a_alone16(T, k, m):
    """A and B together take T days; they work k days, B leaves, A finishes in m days: A alone?"""
    T, k, m = R(T, k, m)
    left = 1 - k / T
    A = m / left
    trad = steps(
        ("Find the work done together.", rf"\[ {tex(k)}\times {fr(1 / T)} = {fr(k / T)} \]"),
        ("Find the work A did alone.", rf"\[ 1 - {fr(k / T)} = {fr(left)} \]"),
        ("Find A's time for the whole work.", rf"A does \({fr(left)}\) in \({tex(m)}\) days, so<br>\[ {tex(m)}\div {fr(left)} = {tex(A)}\text{{ days}} \]"))
    rule = steps(("Match the rule's letters.", rf"Here B leaves and A finishes, so A plays the finisher: \(\frac{{xy}}{{x+y}} = {tex(T)}\) (together), "
                                               rf"\(t = {tex(k)}\) (days together), \(z = {tex(m)}\) (days A works alone), \(y\) = A's own time."),
                 ("Apply the specified rule.", F16 + rf"\[ {tex(k)} = {tex(T)}\times\frac{{y - {tex(m)}}}{{y}} \]"),
                 ("Solve for \\(y\\).", rf"\[ {tex(k)}y = {tex(T)}y - {tex(T * m)} \;\Rightarrow\; {tex(T - k)}y = {tex(T * m)} \;\Rightarrow\; y = {tex(A)}\text{{ days}} \]"))
    fin = fin_of(A, "days")
    rb = rbe([rf"Together \(= {tex(T)}\), \(t = {tex(k)}\), \(z = {tex(m)}\).", rf"\({tex(k)} = {tex(T)}\cdot\frac{{y - {tex(m)}}}{{y}}\).", rf"\(y = \frac{{{tex(T * m)}}}{{{tex(T - k)}}} = {tex(A)}\)."], fin)
    sc = shortcut(rf"\[ y = \frac{{{tex(T)}\times {tex(m)}}}{{{tex(T)} - {tex(k)}}} = {tex(A)} \]", fin)
    return result(("number", A), T16, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 17: x1 men or x2 women or x3 boys
T17 = (r"If \(x_1\) men or \(x_2\) women or \(x_3\) boys can do a work in \(D\) days, then 1 man, 1 woman and 1 boy together do it in"
       r"<br>\[ \frac{D\,x_1x_2x_3}{x_1x_2 + x_2x_3 + x_1x_3}\text{ days} \]")


def mwb17(x1, x2, x3, D):
    m, w, b = F(1, x1 * D), F(1, x2 * D), F(1, x3 * D)
    s = m + w + b
    T = F(D * x1 * x2 * x3, x1 * x2 + x2 * x3 + x1 * x3)
    trad = steps(
        ("Find one person's one-day work.", rf"\({x1}\) men take \({D}\) days, so 1 man takes \({x1 * D}\) days and does \({fr(m)}\) a day. "
                                            rf"Likewise 1 woman does \({fr(w)}\) and 1 boy \({fr(b)}\) a day."),
        ("Add them.", rf"\[ {fr(m)} + {fr(w)} + {fr(b)} = {fr(s)} \]"),
        ("Find the time.", recip(s, "days")))
    rule = steps(("Identify the values.", rf"\(x_1 = {x1}, x_2 = {x2}, x_3 = {x3}, D = {D}\)."),
                 ("Apply the specified rule.", r"\[ \text{Days} = \frac{D\,x_1x_2x_3}{x_1x_2 + x_2x_3 + x_1x_3} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{D}\times {x1}\times {x2}\times {x3}}}{{{x1}\times {x2} + {x2}\times {x3} + {x1}\times {x3}}} = "
                                            rf"\frac{{{D * x1 * x2 * x3}}}{{{x1 * x2 + x2 * x3 + x1 * x3}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(x_1 = {x1}, x_2 = {x2}, x_3 = {x3}, D = {D}\).", r"Days \(= \frac{Dx_1x_2x_3}{x_1x_2 + x_2x_3 + x_1x_3}\).",
              rf"\(\frac{{{D * x1 * x2 * x3}}}{{{x1 * x2 + x2 * x3 + x1 * x3}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{D * x1 * x2 * x3}}}{{{x1 * x2 + x2 * x3 + x1 * x3}}} = {tex(T)} \]", fin)
    return result(("number", T), T17, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 18: n absent
T18 = (r"A group of men decided to do a work in \(x\) days, but \(n\) of them became absent. If the rest of the group did the work in "
       r"\(y\) days, then the original number of men is<br>\[ \frac{ny}{y-x} \]")


def absent18(x, n, y):
    M = F(n * y, y - x)
    trad = steps(("Let the group have \\(M\\) men.", rf"The man-days of work are the same:<br>\[ M\times {x} = (M - {n})\times {y} \]"),
                 ("Open the bracket.", rf"\[ {x}M = {y}M - {n * y} \]"),
                 ("Solve for \\(M\\).", rf"\[ {y - x}M = {n * y} \;\Rightarrow\; M = {tex(M)} \]"))
    rule = steps(("Identify the values.", rf"\(x = {x}\), \(n = {n}\), \(y = {y}\)."), ("Apply the specified rule.", r"\[ \text{Men} = \frac{ny}{y-x} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{n}\times {y}}}{{{y} - {x}}} = \frac{{{n * y}}}{{{y - x}}} = {tex(M)} \]"))
    fin = fin_of(M, "men")
    rb = rbe([rf"\(x = {x}, n = {n}, y = {y}\).", r"Men \(= \frac{ny}{y-x}\).", rf"\(\frac{{{n * y}}}{{{y - x}}} = {tex(M)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{n}\times {y}}}{{{y} - {x}}} = {tex(M)} \]", fin)
    return result(("number", M), T18, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 19: x more, d days less
T19 = (r"A certain number of men can do a work in \(D\) days. If there were \(x\) men more it could be finished in \(d\) days less, then "
       r"the number of men originally is<br>\[ \frac{x(D-d)}{d} \]")


def extra19(D, x, d):
    M = F(x * (D - d), d)
    trad = steps(("Let the number of men be \\(M\\).", rf"The man-days of work are the same:<br>\[ M\times {D} = (M + {x})\times {D - d} \]"),
                 ("Open the bracket.", rf"\[ {D}M = {D - d}M + {x * (D - d)} \]"),
                 ("Solve for \\(M\\).", rf"\[ {d}M = {x * (D - d)} \;\Rightarrow\; M = {tex(M)} \]"))
    rule = steps(("Identify the values.", rf"\(D = {D}\), \(x = {x}\), \(d = {d}\)."), ("Apply the specified rule.", r"\[ \text{Men} = \frac{x(D-d)}{d} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{x}({D} - {d})}}{{{d}}} = \frac{{{x}\times {D - d}}}{{{d}}} = {tex(M)} \]"))
    fin = fin_of(M, "men")
    rb = rbe([rf"\(D = {D}, x = {x}, d = {d}\).", r"Men \(= \frac{x(D-d)}{d}\).", rf"\(\frac{{{x}\times {D - d}}}{{{d}}} = {tex(M)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{x}({D} - {d})}}{{{d}}} = {tex(M)} \]", fin)
    return result(("number", M), T19, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 20: builder
T20 = (r"A builder decided to build a farmhouse in \(D\) days. He employed \(x\) men in the beginning and \(y\) more men after \(d\) days and "
       r"finished on time. Without the additional men, the first men would have finished it in<br>\[ \frac{D(x+y) - yd}{x}\text{ days} \]"
       r"and it would have been \(\frac{y(D-d)}{x}\) days behind schedule.")


def builder20(D, x, y, d, delay=True):
    work = x * d + (x + y) * (D - d)
    total = F(work, x)
    late = total - D
    trad = steps(
        ("Count the work in man-days.", rf"\({x}\) men for \({d}\) days and \({x + y}\) men for the last \({D} - {d} = {D - d}\) days:<br>"
                                        rf"\[ {x}\times {d} + {x + y}\times {D - d} = {work}\text{{ man-days}} \]"),
        ("Give all of it to the first men.", rf"\[ \frac{{{work}}}{{{x}}} = {tex(total)}\text{{ days}} \]"),
        ("Compare with the schedule.", rf"\[ {tex(total)} - {D} = {tex(late)}\text{{ days late}} \]" if delay else rf"The first men alone would take \({tex(total)}\) days."))
    if delay:
        form, line, v = (r"\[ \text{Delay} = \frac{y(D-d)}{x} \]",
                         rf"\[ \frac{{{y}({D} - {d})}}{{{x}}} = \frac{{{y * (D - d)}}}{{{x}}} = {tex(late)}\text{{ days}} \]", late)
    else:
        form, line, v = (r"\[ \text{Days} = \frac{D(x+y) - yd}{x} \]",
                         rf"\[ \frac{{{D}({x} + {y}) - {y}\times {d}}}{{{x}}} = \frac{{{D * (x + y) - y * d}}}{{{x}}} = {tex(total)}\text{{ days}} \]", total)
    rule = steps(("Identify the values.", rf"\(D = {D}\), \(x = {x}\), \(y = {y}\), \(d = {d}\)."), ("Apply the specified rule.", form), ("Substitute the values.", line))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(D = {D}, x = {x}, y = {y}, d = {d}\).", r"Delay \(= \frac{y(D-d)}{x}\)." if delay else r"Days \(= \frac{D(x+y) - yd}{x}\).",
              rf"\(= {tex(v)}\) days."], fin)
    sc = shortcut(line, fin)
    return result(("number", v), T20, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- old-row text fixes, card fix, plan
BOOK_Q = {
    220: lambda q: q.replace(r"6\[ \frac{2}{3} \] days", r"\(6\frac{2}{3}\) days"),
    221: lambda q: q.replace("How long will it take B and C, A and C, and A, B and C to complete the work together?",
                             "How long will A, B and C take to complete the work together?"),
    225: lambda q: q + ":",
}
BOOK_OPTS = {
    219: opts("days", 20, 18, 22, r"22\frac{1}{2}"),
    220: opts("days", 3, 4, 5, r"3\frac{1}{2}"),
    221: opts("days", r"1\frac{5}{7}", r"1\frac{4}{7}", r"1\frac{2}{7}", 2),
    222: {k: rf"A \({a}\) days, B \({b}\) days" for k, (a, b) in zip("abcd", ((21, 42), (20, 40), (22, 44), (23, 46)))},
    223: plain("1 : 2", "2 : 1", "4 : 1", "1 : 3"),
    224: opts("days", 8, 10, 9, 7),
    225: opts("days", 54, 60, 48, 50),
    226: opts("days", 23, 22, 26, 24),
    227: opts("men", 30, 32, 28, 31),
    228: opts("men", 38, 42, 40, 44),
    229: opts("days", 7, 5, 6, 8),
}
CARD_FIX = {19: [
    ("<li>Identify extra men available later → <span>\\(x\\)</span></li>",
     "<li>Identify the extra men (working from the start) → <span>\\(x\\)</span></li>"),
    ("The extra \\(x\\) men complete the same amount of work in the reduced schedule that the original men would have taken \\(d\\) more days to finish. "
     "Equating the work portions gives the original number of men.",
     "The total work in man-days is fixed: \\(MD = (M+x)(D-d)\\). Expanding, \\(MD = MD - Md + x(D-d)\\), so \\(Md = x(D-d)\\) and "
     "\\(M = \\frac{x(D-d)}{d}\\)."),
]}

PLAN = {
    11: (57, {219: lambda: faster11(3, 60), 1290: lambda: faster11(3, 48), 1291: lambda: faster11(2, 36), 1292: lambda: faster11(4, 60),
              1293: lambda: faster11(3, 56), 1294: lambda: faster11(3, 72)}),
    12: (58, {220: lambda: hours12(15, 8, "20/3", 9, 10), 1295: lambda: hours12(10, 8, 16, 5, 8), 1296: lambda: hours12(12, 5, 10, 4, 6),
              1297: lambda: hours12(15, 8, 20, 4, 4), 1298: lambda: hours12(20, 6, 5, 8, 8, improper=True)}),
    13: (59, {221: lambda: c_ab13(6, 8, "abc"), 1299: lambda: c_ab13(5, 10, "bc"), 1300: lambda: c_ab13(6, 9, "bc"), 1301: lambda: c_ab13(8, 12, "ac"),
              1302: lambda: c_ab13(9, 12, "ac"), 1303: lambda: c_ab13(12, 18, "abc"), 1304: lambda: c_ab13(18, 6, "abc")}),
    14: (60, {222: lambda: good14(2, 14, both=True), 1305: lambda: good14(2, 21), 1306: lambda: good14(2, 9), 1307: lambda: good14(3, 12),
              1308: lambda: good14(4, 15), 1309: lambda: good14(2, 10), 1310: lambda: good14(3, 6)}),
    15: (61, {223: lambda: times15(5, 2, 4), 1311: lambda: times15(7, 4, 6), 1312: lambda: times15(8, 4, 7)}),
    16: (62, {224: lambda: left16(45, 40, 23), 225: lambda: a_alone16(30, 20, 20), 1313: lambda: left16(60, 40, 20), 1314: lambda: left16(56, 42, 14),
              1315: lambda: left16(60, 36, 24), 1316: lambda: left16(30, 45, 20), 1317: lambda: a_alone16(36, 24, 16)}),
    17: (63, {226: lambda: mwb17(1, 2, 3, 44), 1318: lambda: mwb17(2, 4, 6, 55), 1319: lambda: mwb17(3, 5, 6, 49), 1320: lambda: mwb17(1, 4, 6, 51),
              1321: lambda: mwb17(1, 3, 6, 45)}),
    18: (64, {227: lambda: absent18(10, 5, 12), 1322: lambda: absent18(20, 10, 25), 1323: lambda: absent18(15, 6, 20), 1324: lambda: absent18(18, 9, 24),
              1325: lambda: absent18(10, 3, 15)}),
    19: (65, {228: lambda: extra19(60, 8, 10), 1326: lambda: extra19(80, 8, 16), 1327: lambda: extra19(60, 5, 10), 1328: lambda: extra19(84, 6, 21),
              1329: lambda: extra19(55, 5, 11)}),
    20: (66, {229: lambda: builder20(40, 100, 100, 35), 1330: lambda: builder20(48, 160, 120, 36), 1331: lambda: builder20(50, 180, 120, 35),
              1332: lambda: builder20(45, 60, 30, 35, delay=False), 1333: lambda: builder20(75, 240, 180, 55), 1334: lambda: builder20(30, 80, 40, 20, delay=False)}),
}


def main():
    for n, (card_id, plan) in PLAN.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"]["id"] == card_id
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(plan), (n, sorted(set(rows) ^ set(plan)))
        out = []
        for rid, fn in plan.items():
            extra = {}
            if rows[rid]["rule_id"] is None:
                q = clean(rows[rid]["question"])
                extra["question"] = BOOK_Q[rid](q) if rid in BOOK_Q else q
                assert "\\[" not in extra["question"], rid
            if rid in BOOK_OPTS:
                extra.update(BOOK_OPTS[rid])
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), card_id, extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated")
        if n in CARD_FIX:
            h = dump["rule_card"]["rule_html"]
            for a, b in CARD_FIX[n]:
                assert h.count(a) == 1, (n, a[:60])
                h = h.replace(a, b)
            json.dump({"rule_name": f"Rule {n}", "rule_html": h}, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            print(f"Rule {n}: card fixed")


if __name__ == "__main__":
    main()
