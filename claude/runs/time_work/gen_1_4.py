"""Rules 1-4: regenerates every row (book worked examples copied in 2018 + reworded exercises) in the prompt #11 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links the 2018 book copies to their
rule card and cleans their text (PDF line breaks, OCR slips, display math inside options). Also writes the Rule 1 and
Rule 4 card fixes and the four missing Rule 4 exercises (book Exercise 5-8, numbers changed) as a JsonImport payload.
Writes ruleNN/2_new_rows.json, ruleNN/3_rule_card.json, rule04/3_json_import_payload.json + 3_answers.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import new_question, rbe, regen_entry, shortcut, solution, steps, tex  # noqa: E402

R = lambda *v: tuple(F(x) for x in v)


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rb, shortcut=sc)


def fr(v):
    """Fraction as a plain \\frac (for one-day work), whole numbers as they are."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def amt(v, unit):
    return rf"\({tex(v)}\) {unit}"


# ---------------------------------------------------------------- Rule 1: M1 D1 W2 = M2 D2 W1
T1 = (r"If \(M_1\) persons can do \(W_1\) works in \(D_1\) days and \(M_2\) persons can do \(W_2\) works in \(D_2\) days, "
      r"then<br>\[ M_1D_1W_2 = M_2D_2W_1 \]")
F1 = r"\[ M_1D_1W_2 = M_2D_2W_1 \]"


def men_for_days(M1, D1, D2):
    M2 = F(M1 * D1, D2)
    trad = steps(
        ("Find the total work in man-days.", rf"\({M1}\) men finish the work in \({D1}\) days, so the work needs<br>"
                                              rf"\[ {M1}\times {D1} = {M1 * D1}\text{{ man-days}} \]"),
        ("Share the same man-days over the new time.", rf"To finish the same work in \({D2}\) days, the men needed are<br>"
                                                        rf"\[ \frac{{{M1 * D1}}}{{{D2}}} = {tex(M2)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(M_1 = {M1}\), \(D_1 = {D1}\), \(D_2 = {D2}\), and the work is the same, so \(W_1 = W_2 = 1\)."),
        ("Apply the specified rule.", F1 + r"\[ M_1D_1 = M_2D_2 \]"),
        ("Substitute the values.", rf"\[ {M1}\times {D1} = M_2\times {D2} \]\[ M_2 = \frac{{{M1}\times {D1}}}{{{D2}}} = {tex(M2)} \]"))
    fin = amt(M2, "men")
    rb = rbe([rf"\(M_1 = {M1}\), \(D_1 = {D1}\), \(D_2 = {D2}\), same work so \(W_1 = W_2\).", r"\(M_1D_1 = M_2D_2\).",
              rf"\(M_2 = \frac{{{M1}\times {D1}}}{{{D2}}} = {tex(M2)}\)."], fin)
    sc = shortcut(rf"\[ M_2 = \frac{{M_1D_1}}{{D_2}} = \frac{{{M1}\times {D1}}}{{{D2}}} = {tex(M2)} \]", fin)
    return result(("number", M2), T1, trad, rule, fin, rb, sc)


def trees(M1, W1, D1, leave, D2):
    M2 = M1 - leave
    W2 = F(M2 * D2 * W1, M1 * D1)
    per = F(W1, M1 * D1)
    trad = steps(
        ("Find the work of one man in one hour.", rf"\({M1}\) men cut \({W1}\) trees in \({D1}\) hours, so in one hour one man cuts<br>"
                                                   rf"\[ \frac{{{W1}}}{{{M1}\times {D1}}} = {fr(per)}\text{{ tree}} \]"),
        ("Find the men left.", rf"\[ {M1} - {leave} = {M2}\text{{ men}} \]"),
        ("Find the trees they cut.", rf"In \({D2}\) hours, \({M2}\) men cut<br>\[ {M2}\times {D2}\times {fr(per)} = {tex(W2)}\text{{ trees}} \]"))
    rule = steps(
        ("Identify the values.", rf"\(M_1 = {M1}\), \(D_1 = {D1}\) hours, \(W_1 = {W1}\) trees; \(M_2 = {M1} - {leave} = {M2}\), \(D_2 = {D2}\) hours "
                                 r"(hours play the part of days here, as both measure time)."),
        ("Apply the specified rule.", F1 + r"\[ W_2 = \frac{M_2D_2W_1}{M_1D_1} \]"),
        ("Substitute the values.", rf"\[ W_2 = \frac{{{M2}\times {D2}\times {W1}}}{{{M1}\times {D1}}} = \frac{{{M2 * D2 * W1}}}{{{M1 * D1}}} = {tex(W2)} \]"))
    fin = amt(W2, "trees")
    rb = rbe([rf"\(M_1 = {M1}\), \(D_1 = {D1}\), \(W_1 = {W1}\); \(M_2 = {M1} - {leave} = {M2}\), \(D_2 = {D2}\).",
              r"\(M_1D_1W_2 = M_2D_2W_1\).", rf"\(W_2 = \frac{{{M2}\times {D2}\times {W1}}}{{{M1}\times {D1}}} = {tex(W2)}\)."], fin)
    sc = shortcut(rf"\[ W_2 = \frac{{{M2}\times {D2}\times {W1}}}{{{M1}\times {D1}}} = {tex(W2)} \]", fin)
    return result(("number", W2), T1, trad, rule, fin, rb, sc)


def k_works(D1, k):
    D2 = D1 * k
    trad = steps(
        ("Find A's one-day work.", rf"A finishes one work in \({D1}\) days, so in one day A does \({fr(F(1, D1))}\) of a work."),
        ("Find the time for all the works.", rf"\({k}\) works of the same type need<br>\[ {k}\div {fr(F(1, D1))} = {k}\times {D1} = {D2}\text{{ days}} \]"))
    rule = steps(
        ("Identify the values.", rf"Only A works, so \(M_1 = M_2 = 1\); \(D_1 = {D1}\), \(W_1 = 1\), \(W_2 = {k}\)."),
        ("Apply the specified rule.", F1 + r"\[ D_1W_2 = D_2W_1 \]"),
        ("Substitute the values.", rf"\[ {D1}\times {k} = D_2\times 1 \]\[ D_2 = {D2} \]"))
    fin = amt(D2, "days")
    rb = rbe([rf"\(M_1 = M_2 = 1\), \(D_1 = {D1}\), \(W_1 = 1\), \(W_2 = {k}\).", r"\(D_1W_2 = D_2W_1\).", rf"\(D_2 = {D1}\times {k} = {D2}\)."], fin)
    sc = shortcut(rf"\[ D_2 = \frac{{D_1W_2}}{{W_1}} = {D1}\times {k} = {D2} \]", fin)
    return result(("number", F(D2)), T1, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 2: M1 D1 T1 W2 = M2 D2 T2 W1
T2 = (r"If \(M_1\) persons can do \(W_1\) works in \(D_1\) days working \(T_1\) hours a day and \(M_2\) persons can do \(W_2\) works "
      r"in \(D_2\) days working \(T_2\) hours a day, then<br>\[ M_1D_1T_1W_2 = M_2D_2T_2W_1 \]")
F2 = r"\[ M_1D_1T_1W_2 = M_2D_2T_2W_1 \]"


def toys(M1, W1, D1, T1, M2, W2, T2_):
    D2 = F(M1 * D1 * T1 * W2, M2 * T2_ * W1)
    mh = M1 * D1 * T1
    per_toy = F(mh, W1)
    trad = steps(
        ("Find the man-hours for one toy.", rf"\({M1}\) men working \({T1}\) hours a day for \({D1}\) days give<br>"
                                             rf"\[ {M1}\times {D1}\times {T1} = {mh}\text{{ man-hours for }} {W1}\text{{ toys}} \]"
                                             rf"\[ \text{{One toy}} = \frac{{{mh}}}{{{W1}}} = {tex(per_toy)}\text{{ man-hours}} \]"),
        ("Find the man-hours for the new order.", rf"\[ {W2}\times {tex(per_toy)} = {tex(per_toy * W2)}\text{{ man-hours}} \]"),
        ("Divide by the man-hours worked each day.", rf"\({M2}\) men working \({T2_}\) hours a day give \({M2 * T2_}\) man-hours a day:<br>"
                                                      rf"\[ \frac{{{tex(per_toy * W2)}}}{{{M2 * T2_}}} = {tex(D2)}\text{{ days}} \]"))
    rule = steps(
        ("Identify the values.", rf"\(M_1 = {M1}\), \(D_1 = {D1}\), \(T_1 = {T1}\), \(W_1 = {W1}\); \(M_2 = {M2}\), \(T_2 = {T2_}\), \(W_2 = {W2}\)."),
        ("Apply the specified rule.", F2 + r"\[ D_2 = \frac{M_1D_1T_1W_2}{M_2T_2W_1} \]"),
        ("Substitute the values.", rf"\[ D_2 = \frac{{{M1}\times {D1}\times {T1}\times {W2}}}{{{M2}\times {T2_}\times {W1}}} = "
                                   rf"\frac{{{M1 * D1 * T1 * W2}}}{{{M2 * T2_ * W1}}} = {tex(D2)} \]"))
    fin = amt(D2, "days")
    rb = rbe([rf"\(M_1 = {M1}, D_1 = {D1}, T_1 = {T1}, W_1 = {W1}\); \(M_2 = {M2}, T_2 = {T2_}, W_2 = {W2}\).", r"\(M_1D_1T_1W_2 = M_2D_2T_2W_1\).",
              rf"\(D_2 = \frac{{{M1}\times {D1}\times {T1}\times {W2}}}{{{M2}\times {T2_}\times {W1}}} = {tex(D2)}\)."], fin)
    sc = shortcut(rf"\[ D_2 = \frac{{{M1}\times {D1}\times {T1}\times {W2}}}{{{M2}\times {T2_}\times {W1}}} = {tex(D2)} \]", fin)
    return result(("number", D2), T2, trad, rule, fin, rb, sc)


def wmb(hw, hm, hb, T1_, M1, D1, k, T2_):
    """Woman in hw hours = man in hm hours = boy in hb hours; M1 men, T1 h/day, D1 days; k men + k women + k boys, T2 h/day."""
    w_eq, b_eq = F(hm, hw), F(hm, hb)
    M2 = k + k * w_eq + k * b_eq
    D2 = M1 * D1 * T1_ / (M2 * T2_)
    parts = F(M1 * T1_ * D1, hm)
    hourly = F(k, hm) + F(k, hw) + F(k, hb)
    trad = steps(
        ("Call the common amount of work one part.", rf"A woman does one part in \({hw}\) hours, a man in \({hm}\) hours and a boy in \({hb}\) hours.<br>"
                                                     rf"In one hour: a man does \({fr(F(1, hm))}\), a woman \({fr(F(1, hw))}\) and a boy \({fr(F(1, hb))}\) of a part."),
        ("Find the whole work in parts.", rf"\({M1}\) men work \({T1_}\) hours a day for \({D1}\) days:<br>"
                                          rf"\[ {M1}\times {T1_}\times {D1}\times {fr(F(1, hm))} = {tex(parts)}\text{{ parts}} \]"),
        ("Find what the new group does in one day.", rf"\[ {k}\left({fr(F(1, hm))} + {fr(F(1, hw))} + {fr(F(1, hb))}\right) = {tex(hourly)}\text{{ parts an hour}} \]"
                                                     rf"\[ {tex(hourly)}\times {T2_} = {tex(hourly * T2_)}\text{{ parts a day}} \]"),
        ("Find the days.", rf"\[ \frac{{{tex(parts)}}}{{{tex(hourly * T2_)}}} = {tex(D2)}\text{{ days}} \]"))
    rule = steps(
        ("Turn everyone into men.", rf"\(1\) woman \(= \frac{{{hm}}}{{{hw}}} = {tex(w_eq)}\) man and \(1\) boy \(= \frac{{{hm}}}{{{hb}}} = {tex(b_eq)}\) man, so<br>"
                                    rf"\[ {k} + {k}\times {tex(w_eq)} + {k}\times {tex(b_eq)} = {tex(M2)}\text{{ men}} \]"),
        ("Apply the specified rule.", F2 + rf"The work is the same, so \(W_1 = W_2\):<br>\[ M_1D_1T_1 = M_2D_2T_2 \]"),
        ("Substitute the values.", rf"\[ {M1}\times {D1}\times {T1_} = {tex(M2)}\times D_2\times {T2_} \]"
                                   rf"\[ D_2 = \frac{{{M1 * D1 * T1_}}}{{{tex(M2 * T2_)}}} = {tex(D2)} \]"))
    fin = amt(D2, "days")
    rb = rbe([rf"\(1\) woman \(= {tex(w_eq)}\) man, \(1\) boy \(= {tex(b_eq)}\) man, so the group \(= {tex(M2)}\) men.",
              rf"\(M_1D_1T_1 = M_2D_2T_2\) with \(M_1 = {M1}, D_1 = {D1}, T_1 = {T1_}, T_2 = {T2_}\).",
              rf"\(D_2 = \frac{{{M1}\times {D1}\times {T1_}}}{{{tex(M2)}\times {T2_}}} = {tex(D2)}\)."], fin)
    sc = shortcut(rf"\[ D_2 = \frac{{{M1}\times {D1}\times {T1_}}}{{{tex(M2)}\times {T2_}}} = {tex(D2)} \]", fin)
    return result(("number", D2), T2, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 3: pair times A+B = x, B+C = y, C+A = z
T3 = (r"If A and B can do a piece of work in \(x\) days, B and C in \(y\) days and C and A in \(z\) days, then (A + B + C) working "
      r"together will do the same work in<br>\[ r = \frac{2xyz}{xy+yz+zx}\text{ days} \]"
      r"and A alone in \(\frac{yr}{y-r}\) days, B alone in \(\frac{zr}{z-r}\) days, C alone in \(\frac{xr}{x-r}\) days.")
F3 = r"\[ r = \frac{2xyz}{xy+yz+zx} \]"


def pair_rates(x, y, z):
    s = 1 / x + 1 / y + 1 / z
    return s, s / 2


def r_steps(x, y, z):
    num, den = 2 * x * y * z, x * y + y * z + z * x
    r = num / den
    body = (rf"\[ r = \frac{{2\times {tex(x)}\times {tex(y)}\times {tex(z)}}}{{{tex(x * y)} + {tex(y * z)} + {tex(z * x)}}} = "
            rf"\frac{{{tex(num)}}}{{{tex(den)}}} = {tex(r)} \]")
    return r, body


def trad_total(x, y, z):
    s, t = pair_rates(x, y, z)
    return s, t, steps(
        ("Write the one-day work of each pair.", rf"\[ \text{{(A + B)}} = {fr(1 / x)},\quad \text{{(B + C)}} = {fr(1 / y)},\quad \text{{(C + A)}} = {fr(1 / z)} \]"),
        ("Add the three pairs.", rf"Each person is counted twice:<br>\[ 2(\text{{A + B + C}}) = {fr(1 / x)} + {fr(1 / y)} + {fr(1 / z)} = {fr(s)} \]"
                                 rf"\[ \text{{A + B + C}} = {fr(t)}\text{{ of the work in one day}} \]"))


def together3(x, y, z):
    x, y, z = R(x, y, z)
    s, t, tr = trad_total(x, y, z)
    trad = tr + "<br><br>" + rf"<b>Step 3: Find the time.</b><br>\[ 1\div {fr(t)} = {tex(1 / t)}\text{{ days}} \]"
    r, body = r_steps(x, y, z)
    assert r == 1 / t
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
                 ("Apply the specified rule.", F3), ("Substitute the values.", body))
    fin = amt(r, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\).", r"\(r = \frac{2xyz}{xy+yz+zx}\).", rf"\(r = {tex(r)}\) days."], fin)
    sc = shortcut(body, fin)
    return result(("number", r), T3, trad, rule, fin, rb, sc)


def separately(x, y, z):
    x, y, z = R(x, y, z)
    s, t, tr = trad_total(x, y, z)
    a, b, c = t - 1 / y, t - 1 / z, t - 1 / x
    trad = tr + "<br><br>" + rf"<b>Step 3: Take away the other pair.</b><br>" + \
        rf"\[ \text{{A}} = {fr(t)} - {fr(1 / y)} = {fr(a)},\quad \text{{B}} = {fr(t)} - {fr(1 / z)} = {fr(b)},\quad \text{{C}} = {fr(t)} - {fr(1 / x)} = {fr(c)} \]" + \
        rf"So A takes \({tex(1 / a)}\) days, B takes \({tex(1 / b)}\) days and C takes \({tex(1 / c)}\) days."
    r, body = r_steps(x, y, z)
    A, B, C = y * r / (y - r), z * r / (z - r), x * r / (x - r)
    assert (A, B, C) == (1 / a, 1 / b, 1 / c)
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) (A + B), \(y = {tex(y)}\) (B + C), \(z = {tex(z)}\) (C + A)."),
                 ("Find r with the specified rule.", F3 + body),
                 ("Find each person's time.", rf"\[ \text{{A}} = \frac{{yr}}{{y-r}} = \frac{{{tex(y)}\times {tex(r)}}}{{{tex(y)} - {tex(r)}}} = {tex(A)} \]"
                                              rf"\[ \text{{B}} = \frac{{zr}}{{z-r}} = \frac{{{tex(z)}\times {tex(r)}}}{{{tex(z)} - {tex(r)}}} = {tex(B)} \]"
                                              rf"\[ \text{{C}} = \frac{{xr}}{{x-r}} = \frac{{{tex(x)}\times {tex(r)}}}{{{tex(x)} - {tex(r)}}} = {tex(C)} \]"))
    fin = rf"A \({tex(A)}\) days, B \({tex(B)}\) days, C \({tex(C)}\) days"
    rb = rbe([rf"\(r = \frac{{2xyz}}{{xy+yz+zx}} = {tex(r)}\).", rf"A \(= \frac{{yr}}{{y-r}} = {tex(A)}\), B \(= \frac{{zr}}{{z-r}} = {tex(B)}\).",
              rf"C \(= \frac{{xr}}{{x-r}} = {tex(C)}\)."], fin)
    sc = shortcut(rf"\[ r = {tex(r)};\quad \text{{A}} = \frac{{yr}}{{y-r}} = {tex(A)},\ \text{{B}} = \frac{{zr}}{{z-r}} = {tex(B)},\ \text{{C}} = \frac{{xr}}{{x-r}} = {tex(C)} \]", fin)
    return result(("triple", (A, B, C)), T3, trad, rule, fin, rb, sc)


def stages3(x, y, z, d_all, d_bc):
    x, y, z = R(x, y, z)
    s, t, tr = trad_total(x, y, z)
    c_rate = t - 1 / x
    done1, done2 = d_all * t, d_bc / y
    left = 1 - done1 - done2
    days = left / c_rate
    trad = tr + "<br><br>" + rf"<b>Step 3: Work done before C is alone.</b><br>" + \
        rf"\[ \text{{All three for }} {d_all}\text{{ days}} = {d_all}\times {fr(t)} = {fr(done1)} \]" + \
        rf"\[ \text{{B and C for }} {d_bc}\text{{ days}} = {d_bc}\times {fr(1 / y)} = {fr(done2)} \]" + \
        rf"\[ \text{{Work left}} = 1 - {fr(done1)} - {fr(done2)} = {fr(left)} \]" + "<br><br>" + \
        rf"<b>Step 4: C finishes it.</b><br>C's one-day work \(= {fr(t)} - {fr(1 / x)} = {fr(c_rate)}\), so<br>" + \
        rf"\[ \frac{{{fr(left)}}}{{{fr(c_rate)}}} = {tex(days)}\text{{ days}} \]"
    r, body = r_steps(x, y, z)
    C = x * r / (x - r)
    assert C == 1 / c_rate
    rule = steps(("Find r with the specified rule.", rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\):" + body),
                 ("Find C's own time.", rf"\[ \text{{C}} = \frac{{xr}}{{x-r}} = \frac{{{tex(x)}\times {tex(r)}}}{{{tex(x)} - {tex(r)}}} = {tex(C)}\text{{ days}} \]"),
                 ("Find the work left and C's time for it.", rf"\[ 1 - \frac{{{d_all}}}{{{tex(r)}}} - \frac{{{d_bc}}}{{{tex(y)}}} = {fr(left)} \]"
                                                              rf"\[ {fr(left)}\times {tex(C)} = {tex(days)}\text{{ days}} \]"))
    fin = amt(days, "days")
    rb = rbe([rf"\(r = \frac{{2xyz}}{{xy+yz+zx}} = {tex(r)}\), C alone \(= \frac{{xr}}{{x-r}} = {tex(C)}\) days.",
              rf"Work left \(= 1 - \frac{{{d_all}}}{{{tex(r)}}} - \frac{{{d_bc}}}{{{tex(y)}}} = {fr(left)}\).", rf"C needs \({fr(left)}\times {tex(C)} = {tex(days)}\) days."], fin)
    sc = shortcut(rf"\[ r = {tex(r)},\ \text{{C}} = {tex(C)};\quad \left(1 - \frac{{{d_all}}}{{{tex(r)}}} - \frac{{{d_bc}}}{{{tex(y)}}}\right)\times {tex(C)} = {tex(days)} \]", fin)
    return result(("number", days), T3, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 4: A + B together in xy/(x+y)
T4 = (r"If A can do a piece of work in \(x\) days and B can do it in \(y\) days, then A and B working together will do the same work in"
      r"<br>\[ \frac{xy}{x+y}\text{ days} \]")
F4 = r"\[ T = \frac{xy}{x+y} \]"


def xy_body(x, y, unit="days", num=tex):
    """T = xy/(x+y) worked out; num=fr shows awkward values as improper fractions (150/7 rather than 21 3/7)."""
    T = x * y / (x + y)
    return T, rf"\[ T = \frac{{{num(x)}\times {num(y)}}}{{{num(x)} + {num(y)}}} = \frac{{{num(x * y)}}}{{{num(x + y)}}} = {tex(T)}\text{{ {unit}}} \]"


def two(x, y, a="A", b="B", unit="days", lead=""):
    x, y = R(x, y)
    s = 1 / x + 1 / y
    trad = steps(
        ("Find the one-day work.", lead + rf"\[ \text{{{a}}} = {fr(1 / x)},\qquad \text{{{b}}} = {fr(1 / y)} \]"),
        ("Add the one-day work.", rf"\[ {fr(1 / x)} + {fr(1 / y)} = {fr(s)} \]"),
        ("Find the time for the whole work.", rf"\[ 1\div {fr(s)} = {tex(1 / s)}\text{{ {unit}}} \]"))
    T, body = xy_body(x, y, unit)
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) ({a}), \(y = {tex(y)}\) ({b})."),
                 ("Apply the specified rule.", F4), ("Substitute the values.", body))
    fin = amt(T, unit)
    rb = rbe([rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", r"\(T = \frac{xy}{x+y}\).", rf"\(T = \frac{{{tex(x * y)}}}{{{tex(x + y)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(T)} \]", fin)
    return result(("number", T), T4, trad, rule, fin, rb, sc)


def c_as_ab(x, y):
    """C takes as long as A and B together; time for B and C together."""
    x, y = R(x, y)
    c = 1 / x + 1 / y
    bc = 1 / y + c
    trad = steps(
        ("Find C's one-day work.", rf"C's time equals (A + B)'s time, so C does as much in a day as A and B together:<br>"
                                   rf"\[ \text{{C}} = {fr(1 / x)} + {fr(1 / y)} = {fr(c)} \]"),
        ("Add B's one-day work.", rf"\[ \text{{B + C}} = {fr(1 / y)} + {fr(c)} = {fr(bc)} \]"),
        ("Find the time.", rf"\[ 1\div {fr(bc)} = {tex(1 / bc)}\text{{ days}} \]"))
    C, b1 = xy_body(x, y)
    T, b2 = xy_body(y, C)
    rule = steps(("Find C's time with the specified rule.", rf"C takes as long as A (\(x = {tex(x)}\)) and B (\(y = {tex(y)}\)) together:" + F4 + b1),
                 ("Apply the rule again to B and C.", rf"Now \(x = {tex(y)}\) (B) and \(y = {tex(C)}\) (C):"),
                 ("Substitute the values.", b2))
    fin = amt(T, "days")
    rb = rbe([rf"C \(= \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(C)}\) days.", r"B and C together: \(\frac{xy}{x+y}\) with B and C's times.",
              rf"\(\frac{{{tex(y)}\times {tex(C)}}}{{{tex(y)} + {tex(C)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \text{{C}} = \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(C)};\quad \text{{B + C}} = \frac{{{tex(y)}\times {tex(C)}}}{{{tex(y)} + {tex(C)}}} = {tex(T)} \]", fin)
    return result(("number", T), T4, trad, rule, fin, rb, sc)


def frac_then_help(p, d, e):
    """A does p of the work in d days, the rest with B's help in e days; A and B together?"""
    p, d, e = R(p, d, e)
    rest = 1 - p
    trad = steps(
        ("Find the work left.", rf"\[ 1 - {fr(p)} = {fr(rest)} \]"),
        ("Find what A and B do together in one day.", rf"A and B do \({fr(rest)}\) of the work in \({tex(e)}\) days:<br>\[ {fr(rest)}\div {tex(e)} = {fr(rest / e)} \]"),
        ("Find the time for the whole work.", rf"\[ 1\div {fr(rest / e)} = {tex(e / rest)}\text{{ days}} \]"))
    x = d / p
    b_done = rest - e / x
    y = e / b_done
    T, body = xy_body(x, y, num=fr)
    assert T == e / rest
    rule = steps(
        ("Find A's time.", rf"A does \({fr(p)}\) in \({tex(d)}\) days, so \(x = {tex(d)}\div {fr(p)} = {fr(x)}\) days."),
        ("Find B's time.", rf"In the last \({tex(e)}\) days A does \({tex(e)}\div {fr(x)} = {fr(e / x)}\), so B does \({fr(rest)} - {fr(e / x)} = {fr(b_done)}\) "
                           rf"in \({tex(e)}\) days:<br>\[ y = {tex(e)}\div {fr(b_done)} = {fr(y)}\text{{ days}} \]"),
        ("Apply the specified rule.", F4 + body))
    fin = amt(T, "days")
    rb = rbe([rf"A alone: \(x = {tex(d)}\div {fr(p)} = {fr(x)}\) days.", rf"B does \({fr(b_done)}\) in \({tex(e)}\) days, so \(y = {fr(y)}\) days.",
              rf"\(T = \frac{{xy}}{{x+y}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ x = {fr(x)},\ y = {fr(y)};\quad \frac{{xy}}{{x+y}} = {tex(T)} \]", fin)
    return result(("number", T), T4, trad, rule, fin, rb, sc)


def then_c(x, y, k, m):
    """A (x days) and B (y days) work k days together, C finishes the rest in m days; C alone?"""
    x, y, k, m = R(x, y, k, m)
    s = 1 / x + 1 / y
    left = 1 - k * s
    C = m / left
    trad = steps(
        ("Find (A + B)'s one-day work.", rf"\[ {fr(1 / x)} + {fr(1 / y)} = {fr(s)} \]"),
        ("Find the work left after the joint days.", rf"\[ 1 - {tex(k)}\times {fr(s)} = 1 - {fr(k * s)} = {fr(left)} \]"),
        ("Find C's time for the whole work.", rf"C does \({fr(left)}\) in \({tex(m)}\) days, so C alone needs<br>\[ {tex(m)}\div {fr(left)} = {tex(C)}\text{{ days}} \]"))
    T, body = xy_body(x, y)
    rule = steps(("Find (A + B)'s time with the specified rule.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\):" + F4 + body),
                 ("Find the work left.", rf"In \({tex(k)}\) days they do \(\frac{{{tex(k)}}}{{{tex(T)}}} = {fr(k / T)}\), so \(1 - {fr(k / T)} = {fr(left)}\) is left."),
                 ("Find C's time.", rf"\[ {tex(m)}\div {fr(left)} = {tex(C)}\text{{ days}} \]"))
    fin = amt(C, "days")
    rb = rbe([rf"A + B together: \(\frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(T)}\) days.",
              rf"Work left after \({tex(k)}\) days \(= 1 - \frac{{{tex(k)}}}{{{tex(T)}}} = {fr(left)}\).", rf"C alone \(= {tex(m)}\div {fr(left)} = {tex(C)}\) days."], fin)
    sc = shortcut(rf"\[ T = {tex(T)};\quad \text{{C}} = \frac{{{tex(m)}}}{{1 - \frac{{{tex(k)}}}{{{tex(T)}}}}} = {tex(C)} \]", fin)
    return result(("number", C), T4, trad, rule, fin, rb, sc)


def b_from_pairs(ta, tbc, tac, unit="hours"):
    """A alone ta, B + C tbc, A + C tac: B alone?"""
    ta, tbc, tac = R(ta, tbc, tac)
    c = 1 / tac - 1 / ta
    b = 1 / tbc - c
    trad = steps(
        ("Find C's one-hour work.", rf"\[ \text{{C}} = (\text{{A + C}}) - \text{{A}} = {fr(1 / tac)} - {fr(1 / ta)} = {fr(c)} \]"),
        ("Find B's one-hour work.", rf"\[ \text{{B}} = (\text{{B + C}}) - \text{{C}} = {fr(1 / tbc)} - {fr(c)} = {fr(b)} \]"),
        ("Find B's time.", rf"\[ 1\div {fr(b)} = {tex(1 / b)}\text{{ {unit}}} \]"))
    C = tac * ta / (ta - tac)
    B = tbc * C / (C - tbc)
    rule = steps(("Turn the specified rule round.", F4 + r"If two together take \(T\) and one of them alone takes \(x\), the other alone takes"
                                                     r"\[ y = \frac{Tx}{x-T} \]"),
                 ("Find C from A and (A + C).", rf"\[ \text{{C}} = \frac{{{tex(tac)}\times {tex(ta)}}}{{{tex(ta)} - {tex(tac)}}} = {tex(C)}\text{{ {unit}}} \]"),
                 ("Find B from C and (B + C).", rf"\[ \text{{B}} = \frac{{{tex(tbc)}\times {tex(C)}}}{{{tex(C)} - {tex(tbc)}}} = {tex(B)}\text{{ {unit}}} \]"))
    fin = amt(B, unit)
    rb = rbe([r"From \(T = \frac{xy}{x+y}\): the other worker takes \(y = \frac{Tx}{x-T}\).",
              rf"C \(= \frac{{{tex(tac)}\times {tex(ta)}}}{{{tex(ta)} - {tex(tac)}}} = {tex(C)}\).", rf"B \(= \frac{{{tex(tbc)}\times {tex(C)}}}{{{tex(C)} - {tex(tbc)}}} = {tex(B)}\)."], fin)
    sc = shortcut(rf"\[ \text{{C}} = \frac{{{tex(tac)}\times {tex(ta)}}}{{{tex(ta)} - {tex(tac)}}} = {tex(C)};\quad \text{{B}} = \frac{{{tex(tbc)}\times {tex(C)}}}{{{tex(C)} - {tex(tbc)}}} = {tex(B)} \]", fin)
    return result(("number", B), T4, trad, rule, fin, rb, sc)


def from_fractions(p, d, q, e):
    """A does p of the work in d days, B does q of it in e days; together?"""
    p, d, q, e = R(p, d, q, e)
    a, b = p / d, q / e
    trad = steps(
        ("Find the one-day work.", rf"\[ \text{{A}} = \frac{{{fr(p)}}}{{{tex(d)}}} = {fr(a)},\qquad \text{{B}} = \frac{{{fr(q)}}}{{{tex(e)}}} = {fr(b)} \]"),
        ("Add the one-day work.", rf"\[ {fr(a)} + {fr(b)} = {fr(a + b)} \]"),
        ("Find the time for the whole work.", rf"\[ 1\div {fr(a + b)} = {tex(1 / (a + b))}\text{{ days}} \]"))
    x, y = d / p, e / q
    T, body = xy_body(x, y)
    rule = steps(("Find each person's time for the whole work.", rf"\[ x = {tex(d)}\div {fr(p)} = {tex(x)},\qquad y = {tex(e)}\div {fr(q)} = {tex(y)} \]"),
                 ("Apply the specified rule.", F4), ("Substitute the values.", body))
    fin = amt(T, "days")
    rb = rbe([rf"A alone \(x = {tex(x)}\) days, B alone \(y = {tex(y)}\) days.", r"\(T = \frac{xy}{x+y}\).", rf"\(T = \frac{{{tex(x * y)}}}{{{tex(x + y)}}} = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(T)} \]", fin)
    return result(("number", T), T4, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- plans
def opts(unit, *vals):
    return {k: rf"\({v}\) {unit}" for k, v in zip("abcd", vals)}


def clean(q):
    return " ".join(q.replace("\r\n", "\n").split())


BOOK_Q = {   # 2018 book copies: PDF line breaks joined, OCR slips and inline math fixed
    185: lambda q: clean(q).replace("a work-in 6 days", "a work in 6 days").replace("then in/how many", "then in how many"),
    190: lambda q: clean(q).replace(r"A does \[ \frac{7}{10} \] of", r"A does \(\frac{7}{10}\) of"),
    193: lambda q: clean(q).replace("A can do (1/3) of", r"A can do \(\frac{1}{3}\) of").replace("B can do (2/5) of", r"B can do \(\frac{2}{5}\) of"),
}
BOOK_OPTS = {
    181: opts("men", 2, 4, 5, 3),
    182: opts("trees", 66, 78, 72, 88),
    183: opts("days", 15, 18, 16, 14),
    184: opts("days", 2, 4, 3, 5),
    185: opts("days", r"1\frac{1}{3}", r"1\frac{1}{2}", r"1\frac{1}{4}", r"1\frac{1}{5}"),
    186: {"a": r"A \(30\) days, B \(20\) days, C \(60\) days", "b": r"A \(32\) days, B \(24\) days, C \(68\) days",
          "c": r"A \(26\) days, B \(28\) days, C \(66\) days", "d": r"A \(24\) days, B \(30\) days, C \(60\) days"},
    187: opts("days", 20, 25, 10, 15),
    188: opts("days", r"2\frac{8}{11}", r"1\frac{10}{11}", r"2\frac{6}{11}", r"1\frac{7}{11}"),
    189: opts("days", r"2\frac{1}{5}", r"2\frac{2}{5}", 6, r"4\frac{2}{5}"),
    190: opts("days", r"13\frac{1}{3}", 12, r"12\frac{2}{3}", 14),
    191: opts("days", 40, 80, 90, 120),
    192: opts("hours", 14, 12, 10, 16),
    193: opts("days", r"7\frac{3}{4}", r"9\frac{3}{8}", r"8\frac{4}{5}", 10),
}

PLAN = {
    1: (43, {181: lambda: men_for_days(16, 10, 40), 182: lambda: trees(40, 60, 8, 8, 12), 183: lambda: k_works(5, 3),
             1229: lambda: men_for_days(20, 12, 30), 1230: lambda: trees(30, 48, 6, 6, 10), 1231: lambda: k_works(7, 4),
             1232: lambda: men_for_days(12, 6, 18), 1233: lambda: men_for_days(24, 8, 4), 1234: lambda: trees(30, 45, 6, 6, 10),
             1235: lambda: trees(16, 24, 4, 4, 6), 1236: lambda: k_works(8, 3)}),
    2: (44, {184: lambda: toys(5, 10, 6, 6, 12, 16, 8), 185: lambda: wmb(8, 6, 12, 6, 9, 6, 12, 8), 1237: lambda: wmb(10, 5, 15, 6, 11, 8, 12, 8),
             1238: lambda: toys(15, 20, 4, 9, 18, 24, 6), 1239: lambda: toys(24, 50, 15, 10, 30, 60, 8)}),
    3: (49, {186: lambda: separately(12, 15, 20), 187: lambda: stages3(10, 15, 20, 6, 4), 1240: lambda: together3(24, 36, 48),
             1241: lambda: stages3(12, 15, 20, 6, 4), 1242: lambda: separately(6, 8, 12), 1243: lambda: together3("9/2", 5, 6)}),
    4: (50, {188: lambda: two(5, 6), 189: lambda: c_as_ab(6, 8), 190: lambda: frac_then_help("7/10", 15, 4), 191: lambda: then_c(16, 10, 6, 3),
             192: lambda: b_from_pairs(4, 3, 2), 193: lambda: from_fractions("1/3", 5, "2/5", 10), 1246: lambda: two(9, 15),
             1247: lambda: two(20, 15, "the 15 men", "the 20 women",
                               lead=r"The 15 men finish the work in \(20\) days and the 20 women in \(15\) days. In one day:<br>"),
             1248: lambda: two(16, 24), 1249: lambda: c_as_ab(6, 10), 1250: lambda: frac_then_help("3/5", 12, 6)}),
}

# ---------------------------------------------------------------- card fixes
CARD_FIX = {
    1: [(r"<p>\[ 20 \text{ men can build } 30 \text{ metres of road in } 6 \text{ days. If } 25 \text{ men work for } 8 \text{ days, how many metres will be built?} \]</p>",
         r"<p>20 men can build 30 metres of road in 6 days. How many metres will 25 men build in 8 days?</p>")],
    4: [(r"<li>Simplify and convert to days → <span>\( ... \)</span></li>",
         r"<li>Example → <span>\( x = 8,\ y = 12:\ T = \frac{8\times 12}{8+12} = 4\frac{4}{5} \) days</span></li>")],
}

# ---------------------------------------------------------------- new Rule 4 questions (book Exercise 5-8, numbers changed)
NEW4 = [
    ("ex5", "A can finish a job in 18 days and B can finish it in 12 days. They work on it together for 6 days, and then C completes "
            "the rest of the job in 4 days. How many days would C alone take to finish the whole job?",
     lambda: then_c(18, 12, 6, 4), opts("days", 20, 24, 30, 36), 2),
    ("ex6", "A can complete a task in 10 hours. B and C working together can complete it in 6 hours, while A and C together take 5 hours. "
            "How long would B take to complete the task alone?",
     lambda: b_from_pairs(10, 6, 5), opts("hours", 12, 10, 18, 15), 4),
    ("ex7", "A can finish a piece of work in 28 days, while B can finish it in 36 days. If they work together, in how many days will "
            "they finish it?",
     lambda: two(28, 36), opts("days", r"15\frac{3}{4}", 32, r"16\frac{1}{4}", r"17\frac{1}{2}"), 1),
    ("ex8", r"A completes \(\frac{1}{4}\) of a job in 3 days, and B completes \(\frac{3}{5}\) of the same job in 12 days. Working together, "
            "in how many days can A and B complete the whole job?",
     lambda: from_fractions("1/4", 3, "3/5", 12), opts("days", 8, r"6\frac{2}{3}", r"7\frac{1}{2}", r"9\frac{1}{4}"), 3),
]


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
            if rid in BOOK_Q:
                extra["question"] = BOOK_Q[rid](rows[rid]["question"])
            elif rows[rid]["rule_id"] is None:
                extra["question"] = clean(rows[rid]["question"])
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

    folder = os.path.join(HERE, "rule04")
    card = json.load(open(os.path.join(folder, "3_rule_card.json"), encoding="utf-8"))
    qs, answers = [], []
    for key, text, fn, op, pos in NEW4:
        g = fn()
        qs.append(new_question(4, text, [op[k] for k in "abcd"], pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "time_n_work", **card}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 4: {len(qs)} new questions")


if __name__ == "__main__":
    main()
