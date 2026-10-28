"""Rules 21-30: regenerates every row (book worked examples copied in 2018 + reworded exercises) in the prompt #11 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links the 2018 book copies to their
rule card and cleans their text. Answer keys come from validate.py (232, 234 and all four reworded Rule 30 rows were
wrong). Also writes the Rule 30 card fix and the missing Rule 27 exercise (book Exercise 4, numbers changed) as a
JsonImport payload. Writes ruleNN/2_new_rows.json, rule30/3_rule_card.json, rule27/3_json_import_payload.json + 3_answers.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import new_question, rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_1_4 import R, clean, fr, opts, result  # noqa: E402
from gen_5_10 import fin_of, plain, recip  # noqa: E402


# ---------------------------------------------------------------- Rule 21: B and C leave before the end
T21 = (r"If A, B and C can do a work in \(x\), \(y\) and \(z\) days respectively, they all begin together, A continues till the work is "
       r"finished, B leaves \(d_1\) days and C leaves \(d_2\) days before its completion, then the work is finished in<br>"
       r"\[ \frac{x(yz + d_1z + d_2y)}{xy + xz + yz}\text{ days} \]")


def leave21(x, y, z, dc, db):
    x, y, z, dc, db = R(x, y, z, dc, db)
    s = 1 / x + 1 / y + 1 / z
    rhs = 1 + db / y + dc / z
    T = rhs / s
    trad = steps(
        ("Write each person's working days.", rf"Let the work take \(T\) days. A works \(T\) days, B works \((T - {tex(db)})\) days and C works \((T - {tex(dc)})\) days:<br>"
                                              rf"\[ \frac{{T}}{{{tex(x)}}} + \frac{{T - {tex(db)}}}{{{tex(y)}}} + \frac{{T - {tex(dc)}}}{{{tex(z)}}} = 1 \]"),
        ("Collect the \\(T\\) terms.", rf"\[ T\left({fr(1 / x)} + {fr(1 / y)} + {fr(1 / z)}\right) = 1 + {fr(db / y)} + {fr(dc / z)} \]\[ {fr(s)}\,T = {fr(rhs)} \]"),
        ("Solve for \\(T\\).", rf"\[ T = {fr(rhs)}\div {fr(s)} = {tex(T)}\text{{ days}} \]"))
    num, den = x * (y * z + db * z + dc * y), x * y + x * z + y * z
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\); B leaves \(d_1 = {tex(db)}\) and C leaves \(d_2 = {tex(dc)}\) days before the end."),
                 ("Apply the specified rule.", r"\[ T = \frac{x(yz + d_1z + d_2y)}{xy + xz + yz} \]"),
                 ("Substitute the values.", rf"\[ T = \frac{{{tex(x)}({tex(y)}\times {tex(z)} + {tex(db)}\times {tex(z)} + {tex(dc)}\times {tex(y)})}}{{{tex(x)}\times {tex(y)} + {tex(x)}\times {tex(z)} + {tex(y)}\times {tex(z)}}} "
                                            rf"= \frac{{{tex(num)}}}{{{tex(den)}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}, d_1 = {tex(db)}, d_2 = {tex(dc)}\).", r"\(T = \frac{x(yz + d_1z + d_2y)}{xy + xz + yz}\).",
              rf"\(T = \frac{{{tex(num)}}}{{{tex(den)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(num)}}}{{{tex(den)}}} = {tex(T)} \]", fin)
    return result(("number", T), T21, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 22: food after some men leave
T22 = (r"If there is sufficient food for \(M\) men for \(D\) days and after \(d\) days \(m\) men leave the place, then the rest of the food "
       r"lasts the rest of the men for<br>\[ \frac{D-d}{M-m}\times M\text{ days} \]")


def food22(M, D, d, m):
    left = M * (D - d)
    v = F(left, M - m)
    trad = steps(("Count the food in man-days.", rf"The food feeds \({M}\) men for \({D}\) days. After \({d}\) days, food for \({D} - {d} = {D - d}\) days is left:<br>"
                                                 rf"\[ {M}\times {D - d} = {left}\text{{ man-days}} \]"),
                 ("Find the men left.", rf"\[ {M} - {m} = {M - m}\text{{ men}} \]"),
                 ("Share the food among them.", rf"\[ \frac{{{left}}}{{{M - m}}} = {tex(v)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(M = {M}\), \(D = {D}\), \(d = {d}\), \(m = {m}\)."),
                 ("Apply the specified rule.", r"\[ \text{Days} = \frac{D-d}{M-m}\times M \]"),
                 ("Substitute the values.", rf"\[ \frac{{{D} - {d}}}{{{M} - {m}}}\times {M} = \frac{{{D - d}}}{{{M - m}}}\times {M} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(M = {M}, D = {D}, d = {d}, m = {m}\).", r"Days \(= \frac{D-d}{M-m}\times M\).", rf"\(\frac{{{D - d}}}{{{M - m}}}\times {M} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{D} - {d}}}{{{M} - {m}}}\times {M} = {tex(v)} \]", fin)
    return result(("number", v), T22, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 23: A = B + C
T23 = (r"If A takes as much time as B and C together, A and B together finish the job in \(x\) days and C alone in \(y\) days, then"
       r"<br>\[ \text{B alone} = \frac{2xy}{y-x}\text{ days},\qquad \text{A alone} = \frac{2xy}{y+x}\text{ days} \]")


def abc23(x, y, ask="B"):
    x, y = R(x, y)
    c = 1 / y
    b = (1 / x - c) / 2
    a = b + c
    trad = steps(
        ("Write what is known.", rf"A does as much in a day as B and C together, so \(\text{{A}} = \text{{B}} + \text{{C}}\). Also "
                                 rf"\(\text{{A}} + \text{{B}} = {fr(1 / x)}\) and \(\text{{C}} = {fr(c)}\)."),
        ("Replace A.", rf"\[ (\text{{B}} + {fr(c)}) + \text{{B}} = {fr(1 / x)} \;\Rightarrow\; 2\,\text{{B}} = {fr(1 / x - c)} \;\Rightarrow\; \text{{B}} = {fr(b)} \]"
                       + (rf"\[ \text{{A}} = {fr(b)} + {fr(c)} = {fr(a)} \]" if ask == "A" else "")),
        (f"Find {ask}'s time.", recip(a if ask == "A" else b, "days")))
    if ask == "A":
        v, form, line = 2 * x * y / (y + x), r"\frac{2xy}{y+x}", rf"\frac{{2\times {tex(x)}\times {tex(y)}}}{{{tex(y)} + {tex(x)}}} = \frac{{{tex(2 * x * y)}}}{{{tex(x + y)}}}"
    else:
        v, form, line = 2 * x * y / (y - x), r"\frac{2xy}{y-x}", rf"\frac{{2\times {tex(x)}\times {tex(y)}}}{{{tex(y)} - {tex(x)}}} = \frac{{{tex(2 * x * y)}}}{{{tex(y - x)}}}"
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) (A and B together), \(y = {tex(y)}\) (C alone)."),
                 ("Apply the specified rule.", rf"\[ \text{{{ask} alone}} = {form} \]"),
                 ("Substitute the values.", rf"\[ {line} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}\).", rf"{ask} alone \(= {form}\).", rf"\({line} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ {line} = {tex(v)} \]", fin)
    return result(("number", v), T23, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 24: more men, finished d2 days early
T24 = (r"If a team of \(x\) persons is supposed to do a work in \(D\) days, after \(d_1\) days \(y\) more persons are employed and the work "
       r"is finished \(d_2\) days earlier, then without the extra persons the work would have been delayed by<br>"
       r"\[ \frac{y\{D - (d_1 + d_2)\} - d_2x}{x}\text{ days} \]and finished in \(\frac{(x+y)(D-d_2) - d_1y}{x}\) days.")


def team24(x, D, d1, y, d2, delay=True):
    work = x * d1 + (x + y) * (D - d1 - d2)
    total = F(work, x)
    late = total - D
    trad = steps(
        ("Count the work in man-days.", rf"\({x}\) men for \({d1}\) days, then \({x + y}\) men for \({D} - {d1} - {d2} = {D - d1 - d2}\) days:<br>"
                                        rf"\[ {x}\times {d1} + {x + y}\times {D - d1 - d2} = {work}\text{{ man-days}} \]"),
        ("Give all of it to the first team.", rf"\[ \frac{{{work}}}{{{x}}} = {tex(total)}\text{{ days}} \]"),
        ("Compare with the plan.", rf"\[ {tex(total)} - {D} = {tex(late)}\text{{ days late}} \]" if delay else rf"The first team alone would take \({tex(total)}\) days."))
    if delay:
        form = r"\[ \text{Delay} = \frac{y\{D - (d_1 + d_2)\} - d_2x}{x} \]"
        line = rf"\[ \frac{{{y}\{{{D} - ({d1} + {d2})\}} - {d2}\times {x}}}{{{x}}} = \frac{{{y * (D - d1 - d2)} - {d2 * x}}}{{{x}}} = {tex(late)}\text{{ days}} \]"
        v = late
    else:
        form = r"\[ \text{Days} = \frac{(x+y)(D-d_2) - d_1y}{x} \]"
        line = rf"\[ \frac{{{x + y}\times {D - d2} - {d1}\times {y}}}{{{x}}} = \frac{{{(x + y) * (D - d2) - d1 * y}}}{{{x}}} = {tex(total)}\text{{ days}} \]"
        v = total
    rule = steps(("Identify the values.", rf"\(x = {x}\), \(D = {D}\), \(d_1 = {d1}\), \(y = {y}\), \(d_2 = {d2}\)."), ("Apply the specified rule.", form),
                 ("Substitute the values.", line))
    unit = "day" if v == 1 else "days"
    fin = fin_of(v, unit)
    rb = rbe([rf"\(x = {x}, D = {D}, d_1 = {d1}, y = {y}, d_2 = {d2}\).", form.replace(r"\[ ", r"\(").replace(r" \]", r"\)") + ".", rf"\(= {tex(v)}\) {unit}."], fin)
    sc = shortcut(line, fin)
    return result(("number", v), T24, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 25: A leaves after d1, B d2 before the end
T25 = (r"If A, B and C can do a work in \(x\), \(y\) and \(z\) days respectively, they start together, A leaves after \(d_1\) days and B "
       r"leaves \(d_2\) days before the completion, then the whole work is completed in<br>\[ \frac{z}{x}\left[\frac{y(x - d_1) + d_2x}{y + z}\right]\text{ days} \]")


def leave25(x, y, z, d1, d2):
    x, y, z, d1, d2 = R(x, y, z, d1, d2)
    s = 1 / y + 1 / z
    rhs = 1 - d1 / x + d2 / y
    T = rhs / s
    trad = steps(
        ("Write each person's working days.", rf"Let the work take \(T\) days. A works \({tex(d1)}\) days, B works \((T - {tex(d2)})\) days and C works \(T\) days:<br>"
                                              rf"\[ \frac{{{tex(d1)}}}{{{tex(x)}}} + \frac{{T - {tex(d2)}}}{{{tex(y)}}} + \frac{{T}}{{{tex(z)}}} = 1 \]"),
        ("Collect the \\(T\\) terms.", rf"\[ T\left({fr(1 / y)} + {fr(1 / z)}\right) = 1 - {fr(d1 / x)} + {fr(d2 / y)} \]\[ {fr(s)}\,T = {fr(rhs)} \]"),
        ("Solve for \\(T\\).", rf"\[ T = {fr(rhs)}\div {fr(s)} = {tex(T)}\text{{ days}} \]"))
    inner = y * (x - d1) + d2 * x
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}, d_1 = {tex(d1)}, d_2 = {tex(d2)}\)."),
                 ("Apply the specified rule.", r"\[ T = \frac{z}{x}\left[\frac{y(x - d_1) + d_2x}{y + z}\right] \]"),
                 ("Substitute the values.", rf"\[ T = \frac{{{tex(z)}}}{{{tex(x)}}}\left[\frac{{{tex(y)}({tex(x)} - {tex(d1)}) + {tex(d2)}\times {tex(x)}}}{{{tex(y)} + {tex(z)}}}\right] "
                                            rf"= \frac{{{tex(z)}}}{{{tex(x)}}}\times\frac{{{tex(inner)}}}{{{tex(y + z)}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}, d_1 = {tex(d1)}, d_2 = {tex(d2)}\).", r"\(T = \frac{z}{x}\cdot\frac{y(x - d_1) + d_2x}{y + z}\).",
              rf"\(T = \frac{{{tex(z)}}}{{{tex(x)}}}\times\frac{{{tex(inner)}}}{{{tex(y + z)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(z)}}}{{{tex(x)}}}\times\frac{{{tex(inner)}}}{{{tex(y + z)}}} = {tex(T)} \]", fin)
    return result(("number", T), T25, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 26: two cases A then B
T26 = (r"If A works \(a_1\) days and B then finishes the work in \(b_1\) days, and had A worked \(a_2\) days B would have finished the rest in "
       r"\(b_2\) days, then A and B alone finish the whole work in<br>\[ \text{A} = \frac{b_2a_1 - b_1a_2}{b_2 - b_1},\qquad \text{B} = \frac{a_2b_1 - a_1b_2}{a_2 - a_1}\text{ days} \]")


def twocase26(a1, b1, a2, b2):
    A = F(b2 * a1 - b1 * a2, b2 - b1)
    B = F(a2 * b1 - a1 * b2, a2 - a1)
    trad = steps(
        ("Write the two cases.", r"Let A take \(x\) days and B take \(y\) days alone. Each case finishes the whole work:<br>"
                                 rf"\[ \frac{{{a1}}}{{x}} + \frac{{{b1}}}{{y}} = 1,\qquad \frac{{{a2}}}{{x}} + \frac{{{b2}}}{{y}} = 1 \]"),
        ("Compare the cases.", rf"A's extra \({a2} - {a1} = {a2 - a1}\) days replace B's \({b1} - {b2} = {b1 - b2}\) days, so \(\frac{{{a2 - a1}}}{{x}} = \frac{{{b1 - b2}}}{{y}}\), "
                               rf"that is \(y = \frac{{{b1 - b2}}}{{{a2 - a1}}}x\)."),
        ("Solve.", rf"Putting this into the first case: \(\frac{{{a1}}}{{x}} + \frac{{{b1}\times {a2 - a1}}}{{{b1 - b2}\,x}} = 1\), so "
                   rf"\(x = {tex(A)}\) days and \(y = {tex(B)}\) days."))
    rule = steps(("Identify the values.", rf"\(a_1 = {a1}, b_1 = {b1}, a_2 = {a2}, b_2 = {b2}\)."),
                 ("Apply the specified rule.", r"\[ \text{A} = \frac{b_2a_1 - b_1a_2}{b_2 - b_1},\qquad \text{B} = \frac{a_2b_1 - a_1b_2}{a_2 - a_1} \]"),
                 ("Substitute the values.", rf"\[ \text{{A}} = \frac{{{b2}\times {a1} - {b1}\times {a2}}}{{{b2} - {b1}}} = \frac{{{b2 * a1 - b1 * a2}}}{{{b2 - b1}}} = {tex(A)} \]"
                                            rf"\[ \text{{B}} = \frac{{{a2}\times {b1} - {a1}\times {b2}}}{{{a2} - {a1}}} = \frac{{{a2 * b1 - a1 * b2}}}{{{a2 - a1}}} = {tex(B)} \]"))
    fin = rf"A \({tex(A)}\) days, B \({tex(B)}\) days"
    rb = rbe([rf"\(a_1 = {a1}, b_1 = {b1}, a_2 = {a2}, b_2 = {b2}\).", rf"A \(= \frac{{{b2 * a1 - b1 * a2}}}{{{b2 - b1}}} = {tex(A)}\).",
              rf"B \(= \frac{{{a2 * b1 - a1 * b2}}}{{{a2 - a1}}} = {tex(B)}\)."], fin)
    sc = shortcut(rf"\[ \text{{A}} = \frac{{{b2 * a1 - b1 * a2}}}{{{b2 - b1}}} = {tex(A)},\quad \text{{B}} = \frac{{{a2 * b1 - a1 * b2}}}{{{a2 - a1}}} = {tex(B)} \]", fin)
    return result(("pair", (A, B)), T26, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 27: together d days, A goes away
T27 = (r"If A can do a work in \(x\) days and B in \(y\) days, they work together for \(d\) days and then A goes away, then B finishes the "
       r"work in<br>\[ y - \left(1 + \frac{y}{x}\right)d\text{ days} \]")


def remain27(x, y, d):
    x, y, d = R(x, y, d)
    s = 1 / x + 1 / y
    left = 1 - d * s
    v = y - (1 + y / x) * d
    trad = steps(("Find the work done together.", rf"\[ {tex(d)}\left({fr(1 / x)} + {fr(1 / y)}\right) = {tex(d)}\times {fr(s)} = {fr(d * s)} \]"),
                 ("Find the work left.", rf"\[ 1 - {fr(d * s)} = {fr(left)} \]"),
                 ("Find B's time for it.", rf"\[ {fr(left)}\times {tex(y)} = {tex(left * y)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(d = {tex(d)}\)."),
                 ("Apply the specified rule.", r"\[ \text{B's days} = y - \left(1 + \frac{y}{x}\right)d \]"),
                 ("Substitute the values.", rf"\[ {tex(y)} - \left(1 + \frac{{{tex(y)}}}{{{tex(x)}}}\right)\times {tex(d)} = {tex(y)} - {tex(1 + y / x)}\times {tex(d)} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, d = {tex(d)}\).", r"B's days \(= y - \left(1 + \frac{y}{x}\right)d\).", rf"\({tex(y)} - {tex(1 + y / x)}\times {tex(d)} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ {tex(y)} - \left(1 + \frac{{{tex(y)}}}{{{tex(x)}}}\right){tex(d)} = {tex(v)} \]", fin)
    return result(("number", v), T27, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 28: part of the work
T28 = (r"If A can complete \(\frac{a}{b}\) part of a work in \(x\) days, then \(\frac{c}{d}\) part of the work will be done in \(y\) days, where"
       r"<br>\[ \frac{x}{a/b} = \frac{y}{c/d} \]")


def part28(p, x, r, name="A"):
    p, x, r = R(p, x, r)
    whole = x / p
    y = whole * r
    trad = steps(("Find the time for the whole work.", rf"{name} does \({fr(p)}\) of the work in \({tex(x)}\) days, so the whole work takes<br>\[ {tex(x)}\div {fr(p)} = {tex(whole)}\text{{ days}} \]"),
                 ("Take the part asked.", rf"\[ {fr(r)}\times {tex(whole)} = {tex(y)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(\frac{{a}}{{b}} = {fr(p)}\), \(x = {tex(x)}\), \(\frac{{c}}{{d}} = {fr(r)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{x}{a/b} = \frac{y}{c/d} \;\Rightarrow\; y = x\times\frac{c/d}{a/b} \]"),
                 ("Substitute the values.", rf"\[ y = {tex(x)}\times {fr(r)}\div {fr(p)} = {tex(y)}\text{{ days}} \]"))
    unit = "day" if y == 1 else "days"
    fin = fin_of(y, unit)
    rb = rbe([rf"\(\frac{{a}}{{b}} = {fr(p)}, x = {tex(x)}, \frac{{c}}{{d}} = {fr(r)}\).", r"\(y = x\times\frac{c/d}{a/b}\).", rf"\(y = {tex(y)}\)."], fin)
    sc = shortcut(rf"\[ y = {tex(x)}\times {fr(r)}\div {fr(p)} = {tex(y)} \]", fin)
    return result(("number", y), T28, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 29: efficiency of two groups
T29 = (r"When two groups differ in men, days, hours a day, efficiency and amount of work,<br>\[ M_1D_1T_1E_1W_2 = M_2D_2T_2E_2W_1 \]"
       r"where \(E_1 : E_2\) is found from the given comparison of the two groups.")


def eff29(M1, T1, D1, M2, T2, W2, m1, h1, m2, h2):
    m1, h1, m2, h2 = R(m1, h1, m2, h2)
    e = (m2 * h2) / (m1 * h1)                        # E1 / E2
    E1, E2 = e.numerator, e.denominator
    job = M1 * D1 * T1 * e * W2
    D2 = job / (M2 * T2)
    trad = steps(
        ("Compare the two kinds of men.", rf"\({tex(m1)}\) men of the first group in \({tex(h1)}\) hour(s) do the work of \({tex(m2)}\) men of the second group in "
                                          rf"\({tex(h2)}\) hour(s), so one first-group man-hour \(= \frac{{{tex(m2)}\times {tex(h2)}}}{{{tex(m1)}\times {tex(h1)}}} = {tex(e)}\) second-group man-hours."),
        ("Measure the work in second-group man-hours.", rf"\[ \text{{One work}} = {M1}\times {D1}\times {T1}\times {tex(e)} = {tex(M1 * D1 * T1 * e)} \]"
                                                         rf"\[ {W2}\text{{ works}} = {tex(job)}\text{{ man-hours}} \]"),
        ("Divide by the new group's daily man-hours.", rf"\({M2}\) men working \({T2}\) hours a day give \({M2 * T2}\) man-hours a day:<br>"
                                                        rf"\[ \frac{{{tex(job)}}}{{{M2 * T2}}} = {tex(D2)}\text{{ days}} \]"))
    rule = steps(("Find the efficiency ratio.", rf"\[ {tex(m1)}\times {tex(h1)}\times E_1 = {tex(m2)}\times {tex(h2)}\times E_2 \;\Rightarrow\; E_1 : E_2 = {E1} : {E2} \]"),
                 ("Apply the specified rule.", r"\[ M_1D_1T_1E_1W_2 = M_2D_2T_2E_2W_1 \]"),
                 ("Substitute the values.", rf"\[ D_2 = \frac{{{M1}\times {D1}\times {T1}\times {E1}\times {W2}}}{{{M2}\times {T2}\times {E2}\times 1}} = "
                                            rf"\frac{{{M1 * D1 * T1 * E1 * W2}}}{{{M2 * T2 * E2}}} = {tex(D2)}\text{{ days}} \]"))
    fin = fin_of(D2, "days")
    rb = rbe([rf"\(E_1 : E_2 = {E1} : {E2}\).", r"\(M_1D_1T_1E_1W_2 = M_2D_2T_2E_2W_1\).", rf"\(D_2 = \frac{{{M1 * D1 * T1 * E1 * W2}}}{{{M2 * T2 * E2}}} = {tex(D2)}\)."], fin)
    sc = shortcut(rf"\[ E_1 : E_2 = {E1} : {E2};\quad D_2 = \frac{{{M1}\times {D1}\times {T1}\times {E1}\times {W2}}}{{{M2}\times {T2}\times {E2}}} = {tex(D2)} \]", fin)
    return result(("number", D2), T29, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 30: sqrt(xy)
T30 = (r"If A working alone takes \(x\) days (or hours) more than A and B together, and B working alone takes \(y\) more, then A and B "
       r"working together take<br>\[ \sqrt{xy}\text{ days (or hours)} \]")


def sqrt30(x, y, unit="hours"):
    x, y = R(x, y)
    T2 = x * y
    T = F(round(float(T2) ** 0.5 * 10 ** 6), 10 ** 6)
    assert T * T == T2, (x, y)
    trad = steps(
        ("Write the three times.", rf"Let A and B together take \(T\) {unit}. Then A alone takes \((T + {tex(x)})\) and B alone \((T + {tex(y)})\) {unit}."),
        ("Add the one-hour work.", rf"\[ \frac{{1}}{{T + {tex(x)}}} + \frac{{1}}{{T + {tex(y)}}} = \frac{{1}}{{T}} \]"
                                   rf"\[ T(2T + {tex(x + y)}) = (T + {tex(x)})(T + {tex(y)}) \]"
                                   rf"\[ 2T^2 + {tex(x + y)}T = T^2 + {tex(x + y)}T + {tex(T2)} \]"),
        ("Solve.", rf"\[ T^2 = {tex(T2)} \;\Rightarrow\; T = {tex(T)}\text{{ {unit}}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", r"\[ T = \sqrt{xy} \]"),
                 ("Substitute the values.", rf"\[ T = \sqrt{{{tex(x)}\times {tex(y)}}} = \sqrt{{{tex(T2)}}} = {tex(T)}\text{{ {unit}}} \]"))
    fin = fin_of(T, unit)
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}\).", r"\(T = \sqrt{xy}\).", rf"\(T = \sqrt{{{tex(T2)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \sqrt{{{tex(x)}\times {tex(y)}}} = \sqrt{{{tex(T2)}}} = {tex(T)} \]", fin)
    return result(("number", T), T30, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- text fixes, card fix, plan
BOOK_Q = {
    234: lambda q: q.replace(r"12\[ \frac{4}{5} \] days", r"\(12\frac{4}{5}\) days"),
    236: lambda q: q.replace(r"A can do \[ \frac{3}{4} \] of", r"A can do \(\frac{3}{4}\) of").replace(r"finish \[ \frac{1}{8} \] of the work.", r"finish \(\frac{1}{8}\) of the work?"),
    237: lambda q: q.replace("piece of Work", "piece of work").replace(r"1\[ \frac{1}{2} \] hr.", r"\(1\frac{1}{2}\) hours."),
    238: lambda q: q.replace("the j ob", "the job").replace(r"3\[ \frac{1}{2} \] hours", r"\(3\frac{1}{2}\) hours").replace("What time, would", "What time would"),
}
BOOK_OPTS = {
    230: opts("days", 8, 5, 7, 9),
    231: opts("days", 10, 11, 9, 12),
    232: opts("days", 60, 70, 65, 55),
    233: plain(r"\(3\) days", r"\(1\) day", r"\(2\) days", r"\(4\) days"),
    234: opts("days", 7, 9, 8, 11),
    235: {k: rf"A \({a}\) days, B \({b}\) days" for k, (a, b) in zip("abcd", ((4, 14), (6, 13), (5, 15), (5, 16)))},
    236: plain(r"\(2\) days", r"\(4\) days", r"\(1\) day", r"\(3\frac{1}{2}\) days"),
    237: opts("days", 29, 27, 28, 30),
    238: opts("hours", 9, 10, 7, 8),
    1337: {"b": r"\(6\frac{1}{2}\) days"},
    1350: {"b": r"\(1\frac{1}{2}\) days", "d": r"\(2\frac{1}{2}\) days"},
    1351: {"a": r"\(\frac{1}{2}\) day", "c": r"\(1\frac{1}{2}\) days"},
}
CARD_FIX = {30: [(
    "The extra times \\(x\\) and \\(y\\) arise from the difference between working alone and working together. Their geometric mean gives the "
    "combined time because the individual work rates are reciprocal functions of these extra times.",
    "If A and B together take \\(T\\), then A alone takes \\(T+x\\) and B alone \\(T+y\\). Adding one-day work, "
    "\\(\\frac{1}{T+x}+\\frac{1}{T+y}=\\frac{1}{T}\\), so \\(T(2T+x+y)=(T+x)(T+y)\\). Expanding, \\(2T^2+(x+y)T=T^2+(x+y)T+xy\\), "
    "which leaves \\(T^2=xy\\), that is \\(T=\\sqrt{xy}\\).")]}

PLAN = {
    21: (67, {230: lambda: leave21(8, 16, 24, 2, 1), 1335: lambda: leave21(20, 30, 40, 2, 1), 1336: lambda: leave21(9, 18, 27, 3, 2),
              1337: lambda: leave21(12, 15, 20, 4, 3), 1338: lambda: leave21(6, 8, 12, 2, 1)}),
    22: (68, {231: lambda: food22(400, 31, 28, 280), 1339: lambda: food22(500, 36, 30, 350), 1340: lambda: food22(300, 40, 36, 240),
              1341: lambda: food22(240, 30, 26, 210), 1342: lambda: food22(450, 45, 42, 360), 1343: lambda: food22(300, 18, 12, 240)}),
    23: (69, {232: lambda: abc23(10, 15), 1344: lambda: abc23(12, 18), 1345: lambda: abc23(8, 40), 1346: lambda: abc23(12, 36),
              1347: lambda: abc23(14, 28), 1348: lambda: abc23(15, 30, "A")}),
    24: (70, {233: lambda: team24(30, 38, 25, 5, 1), 1349: lambda: team24(20, 36, 24, 8, 2), 1350: lambda: team24(32, 50, 35, 12, 3),
              1351: lambda: team24(24, 40, 18, 6, 4), 1352: lambda: team24(21, 32, 14, 7, 3, delay=False), 1353: lambda: team24(24, 40, 30, 8, 4, delay=False)}),
    25: (71, {234: lambda: leave25(16, "64/5", 32, 4, 3), 1354: lambda: leave25(16, 24, 20, 4, 4), 1355: lambda: leave25(15, 20, 30, 3, 4),
              1356: lambda: leave25(9, 12, 18, 3, 2), 1357: lambda: leave25(24, 36, 18, 6, 3), 1358: lambda: leave25(20, 30, 40, 5, 2)}),
    26: (72, {235: lambda: twocase26(2, 9, 3, 6), 1359: lambda: twocase26(2, 6, 3, 4), 1360: lambda: twocase26(3, 10, 5, 6), 1361: lambda: twocase26(5, 28, 8, 16)}),
    27: (73, {1362: lambda: remain27(36, 24, 6), 1363: lambda: remain27("15/2", 6, 2), 1364: lambda: remain27(40, 30, 8), 1365: lambda: remain27(32, 24, 8)}),
    28: (74, {236: lambda: part28("3/4", 12, "1/8"), 1366: lambda: part28("3/5", 9, "1/3"), 1367: lambda: part28("3/4", 18, "1/8", "Ram"),
              1368: lambda: part28("2/3", 8, "1/3", "Vinay"), 1369: lambda: part28("1/3", 6, "1/18", "Sudhir")}),
    29: (75, {237: lambda: eff29(38, 6, 12, 57, 8, 2, 2, 1, 3, "3/2"), 1370: lambda: eff29(50, 6, 12, 60, 8, 2, 2, 1, 4, 1),
              1371: lambda: eff29(36, 6, 10, 50, 8, 2, 4, 3, 5, 4), 1372: lambda: eff29(24, 6, 15, 40, 9, 2, 3, 4, 5, 3)}),
    30: (76, {238: lambda: sqrt30(14, "7/2"), 1373: lambda: sqrt30(18, "9/2"), 1374: lambda: sqrt30(12, 3), 1375: lambda: sqrt30(25, 4), 1376: lambda: sqrt30(24, 6)}),
}

NEW27 = [("ex4", r"A can do a piece of work in \(22\frac{1}{2}\) days and B in \(7\frac{1}{2}\) days. They work together for \(4\frac{1}{2}\) days "
                 "and then A leaves B to finish the work alone. How long will B take to finish it?",
          lambda: remain27("45/2", "15/2", "9/2"), opts("days", r"1\frac{1}{5}", r"2\frac{1}{4}", r"1\frac{1}{2}", 3), 3)]


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

    folder = os.path.join(HERE, "rule27")
    card = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))["rule_card"]
    qs, answers = [], []
    for key, text, fn, op, pos in NEW27:
        g = fn()
        qs.append(new_question(27, text, [op[k] for k in "abcd"], pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "time_n_work", "rule_name": "Rule 27", "rule_html": card["rule_html"]}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 27: {len(qs)} new question")


if __name__ == "__main__":
    main()
