"""Rules 5-10: regenerates every row (book worked examples and exercises copied in 2018 + reworded exercises) in the
prompt #11 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links the 2018 book
copies to their rule card and cleans their text (PDF line breaks, OCR slips, display math inside options, units).
The six rule cards were checked and need no change. Writes ruleNN/2_new_rows.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_1_4 import R, amt, clean, fr, opts, result, xy_body  # noqa: E402


def show(v, improper=False):
    return fr(v) if improper else tex(v)


def fin_of(v, unit, improper=False):
    return rf"\({show(v, improper)}\) {unit}"


def triple_fin(a, b, c, unit="days"):
    return rf"A \({tex(a)}\) {unit}, B \({tex(b)}\) {unit}, C \({tex(c)}\) {unit}"


def recip(rate, unit, improper=False):
    return rf"\[ 1\div {fr(rate)} = {show(1 / rate, improper)}\text{{ {unit}}} \]"


# ---------------------------------------------------------------- Rule 5: A, B, C together in xyz/(xy+yz+zx)
T5 = (r"If A, B and C can do a work in \(x\), \(y\) and \(z\) days respectively, then all of them working together can finish "
      r"the work in<br>\[ \frac{xyz}{xy+yz+zx}\text{ days} \]")
F5 = r"\[ T = \frac{xyz}{xy+yz+zx} \]"


def r5_body(x, y, z, unit, improper=False):
    num, den = x * y * z, x * y + y * z + z * x
    T = num / den
    return T, (rf"\[ T = \frac{{{tex(x)}\times {tex(y)}\times {tex(z)}}}{{{tex(x)}\times {tex(y)} + {tex(y)}\times {tex(z)} + {tex(z)}\times {tex(x)}}} "
               rf"= \frac{{{tex(num)}}}{{{tex(den)}}} = {show(T, improper)}\text{{ {unit}}} \]")


def three5(x, y, z, unit="days", names=("A", "B", "C"), improper=False, lead=""):
    x, y, z = R(x, y, z)
    s = 1 / x + 1 / y + 1 / z
    a, b, c = names
    trad = steps(
        ("Find the one-day work of each.", lead + rf"\[ \text{{{a}}} = {fr(1 / x)},\quad \text{{{b}}} = {fr(1 / y)},\quad \text{{{c}}} = {fr(1 / z)} \]"),
        ("Add them.", rf"\[ {fr(1 / x)} + {fr(1 / y)} + {fr(1 / z)} = {fr(s)} \]"),
        ("Find the time for the whole work.", recip(s, unit, improper)))
    T, body = r5_body(x, y, z, unit, improper)
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
                 ("Apply the specified rule.", F5), ("Substitute the values.", body))
    fin = fin_of(T, unit, improper)
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\).", r"\(T = \frac{xyz}{xy+yz+zx}\).",
              rf"\(T = \frac{{{tex(x * y * z)}}}{{{tex(x * y + y * z + z * x)}}} = {show(T, improper)}\)."], fin)
    sc = shortcut(body, fin)
    return result(("number", T), T5, trad, rule, fin, rb, sc)


def c_missing5(x, y, T):
    x, y, T = R(x, y, T)
    c = 1 / T - 1 / x - 1 / y
    trad = steps(
        ("Write the one-day work.", rf"\[ \text{{A}} = {fr(1 / x)},\quad \text{{B}} = {fr(1 / y)},\quad \text{{A + B + C}} = {fr(1 / T)} \]"),
        ("Take away A and B.", rf"\[ \text{{C}} = {fr(1 / T)} - {fr(1 / x)} - {fr(1 / y)} = {fr(c)} \]"),
        ("Find C's time.", recip(c, "days")))
    z = T * x * y / (x * y - T * (x + y))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) (A), \(y = {tex(y)}\) (B), \(T = {tex(T)}\) (all three)."),
                 ("Turn the specified rule round for C.", F5 + r"Solving \(\frac{1}{T} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}\) for \(z\):"
                                                           r"\[ z = \frac{Txy}{xy - T(x+y)} \]"),
                 ("Substitute the values.", rf"\[ z = \frac{{{tex(T)}\times {tex(x)}\times {tex(y)}}}{{{tex(x)}\times {tex(y)} - {tex(T)}({tex(x)} + {tex(y)})}} "
                                            rf"= \frac{{{tex(T * x * y)}}}{{{tex(x * y - T * (x + y))}}} = {tex(z)}\text{{ days}} \]"))
    fin = fin_of(z, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, T = {tex(T)}\).", r"\(z = \frac{Txy}{xy - T(x+y)}\).",
              rf"\(z = \frac{{{tex(T * x * y)}}}{{{tex(x * y - T * (x + y))}}} = {tex(z)}\)."], fin)
    sc = shortcut(rf"\[ z = \frac{{{tex(T)}\times {tex(x)}\times {tex(y)}}}{{{tex(x)}\times {tex(y)} - {tex(T)}({tex(x)} + {tex(y)})}} = {tex(z)} \]", fin)
    return result(("number", z), T5, trad, rule, fin, rb, sc)


def half5(T):
    """A takes half as long as B; C as long as A and B together; all three take T days."""
    T = F(T)
    A = 3 * T
    trad = steps(
        ("Write everyone's one-day work with A's time.", r"Let A take \(x\) days. Then B takes \(2x\) days, so<br>"
                                                         r"\[ \text{A} = \frac{1}{x},\quad \text{B} = \frac{1}{2x},\quad \text{C} = \text{A + B} = \frac{1}{x} + \frac{1}{2x} = \frac{3}{2x} \]"),
        ("Add the three.", r"\[ \frac{1}{x} + \frac{1}{2x} + \frac{3}{2x} = \frac{2 + 1 + 3}{2x} = \frac{3}{x} \]"),
        ("Use the time of all three.", rf"\[ \frac{{3}}{{x}} = \frac{{1}}{{{tex(T)}}} \;\Rightarrow\; x = {tex(A)} \]"
                                       rf"So A takes \({tex(A)}\) days, B takes \({tex(2 * A)}\) days and C takes \(\frac{{2x}}{{3}} = {tex(2 * A / 3)}\) days."))
    rule = steps(
        ("Write the three times.", r"\(x\) (A), \(2x\) (B) and, since C equals A and B together, \(\frac{x\cdot 2x}{x + 2x} = \frac{2x}{3}\) (C)."),
        ("Apply the specified rule.", F5 + r"\[ T = \frac{x\cdot 2x\cdot \frac{2x}{3}}{2x^2 + \frac{4x^2}{3} + \frac{2x^2}{3}} = \frac{\frac{4x^3}{3}}{4x^2} = \frac{x}{3} \]"),
        ("Substitute the total time.", rf"\[ \frac{{x}}{{3}} = {tex(T)} \;\Rightarrow\; x = {tex(A)} \]"
                                       rf"A \(= {tex(A)}\), B \(= 2\times {tex(A)} = {tex(2 * A)}\), C \(= \frac{{2\times {tex(A)}}}{{3}} = {tex(2 * A / 3)}\)."))
    fin = triple_fin(A, 2 * A, 2 * A / 3)
    rb = rbe([r"Times: A \(= x\), B \(= 2x\), C \(= \frac{2x}{3}\).", r"\(T = \frac{xyz}{xy+yz+zx} = \frac{x}{3}\).",
              rf"\(\frac{{x}}{{3}} = {tex(T)}\) gives \(x = {tex(A)}\); so \({tex(A)}, {tex(2 * A)}, {tex(2 * A / 3)}\) days."], fin)
    sc = shortcut(rf"\[ \frac{{x}}{{3}} = {tex(T)} \Rightarrow x = {tex(A)};\quad \text{{B}} = {tex(2 * A)},\ \text{{C}} = {tex(2 * A / 3)} \]", fin)
    return result(("triple", (A, 2 * A, 2 * A / 3)), T5, trad, rule, fin, rb, sc)


def twice_thrice5(T):
    """A takes twice B's time and thrice C's time; together T days."""
    T = F(T)
    A = 6 * T
    trad = steps(
        ("Write everyone's one-day work with A's time.", r"Let A take \(x\) days; B takes \(\frac{x}{2}\) and C takes \(\frac{x}{3}\) days, so<br>"
                                                         r"\[ \text{A} = \frac{1}{x},\quad \text{B} = \frac{2}{x},\quad \text{C} = \frac{3}{x} \]"),
        ("Add the three.", r"\[ \frac{1}{x} + \frac{2}{x} + \frac{3}{x} = \frac{6}{x} \]"),
        ("Use the time together.", rf"\[ \frac{{6}}{{x}} = \frac{{1}}{{{tex(T)}}} \;\Rightarrow\; x = {tex(A)} \]"
                                   rf"So A takes \({tex(A)}\), B \({tex(A / 2)}\) and C \({tex(A / 3)}\) days."))
    rule = steps(
        ("Write the three times.", r"A \(= x\), B \(= \frac{x}{2}\), C \(= \frac{x}{3}\)."),
        ("Apply the specified rule.", F5 + r"\[ T = \frac{x\cdot\frac{x}{2}\cdot\frac{x}{3}}{\frac{x^2}{2} + \frac{x^2}{6} + \frac{x^2}{3}} = \frac{\frac{x^3}{6}}{x^2} = \frac{x}{6} \]"),
        ("Substitute the total time.", rf"\[ \frac{{x}}{{6}} = {tex(T)} \;\Rightarrow\; x = {tex(A)} \]"
                                       rf"A \(= {tex(A)}\), B \(= {tex(A / 2)}\), C \(= {tex(A / 3)}\)."))
    fin = triple_fin(A, A / 2, A / 3)
    rb = rbe([r"Times: A \(= x\), B \(= \frac{x}{2}\), C \(= \frac{x}{3}\).", r"\(T = \frac{xyz}{xy+yz+zx} = \frac{x}{6}\).",
              rf"\(\frac{{x}}{{6}} = {tex(T)}\) gives \(x = {tex(A)}\); so \({tex(A)}, {tex(A / 2)}, {tex(A / 3)}\) days."], fin)
    sc = shortcut(rf"\[ \frac{{x}}{{6}} = {tex(T)} \Rightarrow x = {tex(A)};\quad \text{{B}} = {tex(A / 2)},\ \text{{C}} = {tex(A / 3)} \]", fin)
    return result(("triple", (A, A / 2, A / 3)), T5, trad, rule, fin, rb, sc)


def groups5(m, tm, w, tw, c, tc, unit="hours", improper=False):
    x, y, z = F(m * tm), F(w * tw), F(c * tc)
    lead = (rf"\({m}\) men take \({tm}\) {unit}, so 1 man takes \({m}\times {tm} = {tex(x)}\) {unit}; likewise 1 woman takes \({w}\times {tw} = {tex(y)}\) "
            rf"and 1 child \({c}\times {tc} = {tex(z)}\) {unit}. In one {unit[:-1]}:<br>")
    g = three5(x, y, z, unit, ("1 man", "1 woman", "1 child"), improper, lead)
    T = x * y * z / (x * y + y * z + z * x)
    rule = steps(("Turn each group into one person's time.", rf"\(x = {m}\times {tm} = {tex(x)}\), \(y = {w}\times {tw} = {tex(y)}\), \(z = {c}\times {tc} = {tex(z)}\) {unit}."),
                 ("Apply the specified rule.", F5), ("Substitute the values.", r5_body(x, y, z, unit, improper)[1]))
    sol = g["solution"]
    i, j = sol.index("<b>Using the Specified Rule :</b><br><br>") + len("<b>Using the Specified Rule :</b><br><br>"), sol.index("<br><br><b>Verification:</b>")
    g["solution"] = sol[:i] + rule + sol[j:]
    g["rbe"] = rbe([rf"One person's time: \(x = {tex(x)}, y = {tex(y)}, z = {tex(z)}\) {unit}.", r"\(T = \frac{xyz}{xy+yz+zx}\).",
                    rf"\(T = \frac{{{tex(x * y * z)}}}{{{tex(x * y + y * z + z * x)}}} = {show(T, improper)}\)."], fin_of(T, unit, improper))
    return g


# ---------------------------------------------------------------- Rule 6: B alone in xy/(y-x)
T6 = (r"If A and B together can do a piece of work in \(x\) days and A alone can do it in \(y\) days, then B alone can do the "
      r"work in<br>\[ \frac{xy}{y-x}\text{ days} \]")
F6 = r"\[ \text{Other alone} = \frac{xy}{y-x} \]"


def r6(x, y, unit="days", improper=False):
    """x = time of the pair, y = time of the known one; returns the other one's time and the worked line."""
    v = x * y / (y - x)
    return v, rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(y)} - {tex(x)}}} = \frac{{{tex(x * y)}}}{{{tex(y - x)}}} = {show(v, improper)}\text{{ {unit}}} \]"


def other_alone(x, y, known="A", other="B", pair="A and B"):
    x, y = R(x, y)
    o = 1 / x - 1 / y
    trad = steps(
        ("Write the one-day work.", rf"\[ \text{{{pair}}} = {fr(1 / x)},\qquad \text{{{known}}} = {fr(1 / y)} \]"),
        (f"Take away {known}'s work.", rf"\[ \text{{{other}}} = {fr(1 / x)} - {fr(1 / y)} = {fr(o)} \]"),
        (f"Find {other}'s time.", recip(o, "days")))
    v, line = r6(x, y)
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) ({pair} together), \(y = {tex(y)}\) ({known} alone)."),
                 ("Apply the specified rule.", F6), ("Substitute the values.", line))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"{other} alone \(= \frac{{xy}}{{y-x}}\).", rf"\(\frac{{{tex(x * y)}}}{{{tex(y - x)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(y)} - {tex(x)}}} = {tex(v)} \]", fin)
    return result(("number", v), T6, trad, rule, fin, rb, sc)


def c_from_groups(ab, abc):
    ab, abc = R(ab, abc)
    c = 1 / abc - 1 / ab
    trad = steps(
        ("Write the one-day work.", rf"\[ \text{{A + B}} = {fr(1 / ab)},\qquad \text{{A + B + C}} = {fr(1 / abc)} \]"),
        ("Take away (A + B).", rf"\[ \text{{C}} = {fr(1 / abc)} - {fr(1 / ab)} = {fr(c)} \]"),
        ("Find C's time.", recip(c, "days")))
    v, line = r6(abc, ab)
    rule = steps(("Treat (A + B) as one worker.", rf"(A + B) and C together take \(x = {tex(abc)}\) days; (A + B) alone takes \(y = {tex(ab)}\) days."),
                 ("Apply the specified rule.", F6), ("Substitute the values.", line))
    fin = fin_of(v, "days")
    rb = rbe([rf"Together \(x = {tex(abc)}\), (A + B) alone \(y = {tex(ab)}\).", r"C alone \(= \frac{xy}{y-x}\).", rf"\(\frac{{{tex(abc * ab)}}}{{{tex(ab - abc)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(abc)}\times {tex(ab)}}}{{{tex(ab)} - {tex(abc)}}} = {tex(v)} \]", fin)
    return result(("number", v), T6, trad, rule, fin, rb, sc)


def ab_from_chain(b, bc, abc, unit="hours"):
    b, bc, abc = R(b, bc, abc)
    c = 1 / bc - 1 / b
    a = 1 / abc - 1 / bc
    trad = steps(
        ("Find C's one-hour work.", rf"\[ \text{{C}} = (\text{{B + C}}) - \text{{B}} = {fr(1 / bc)} - {fr(1 / b)} = {fr(c)} \]"),
        ("Find A's one-hour work.", rf"\[ \text{{A}} = (\text{{A + B + C}}) - (\text{{B + C}}) = {fr(1 / abc)} - {fr(1 / bc)} = {fr(a)} \]"),
        ("Add A and B.", rf"\[ \text{{A + B}} = {fr(a)} + {fr(1 / b)} = {fr(a + 1 / b)} \]" + recip(a + 1 / b, unit)))
    C, l1 = r6(bc, b, unit)
    AB, l2 = r6(abc, C, unit)
    rule = steps(("Find C with the specified rule.", rf"B and C together \(x = {tex(bc)}\), B alone \(y = {tex(b)}\):" + F6 + l1),
                 ("Find (A + B) with the rule again.", rf"All three \(x = {tex(abc)}\), C alone \(y = {tex(C)}\):" + l2),
                 ("Read the answer.", rf"A and B together take \({tex(AB)}\) {unit}."))
    fin = fin_of(AB, unit)
    rb = rbe([rf"C \(= \frac{{{tex(bc)}\times {tex(b)}}}{{{tex(b)} - {tex(bc)}}} = {tex(C)}\).", rf"A + B \(= \frac{{{tex(abc)}\times {tex(C)}}}{{{tex(C)} - {tex(abc)}}}\).",
              rf"A + B \(= {tex(AB)}\) {unit}."], fin)
    sc = shortcut(rf"\[ \text{{C}} = \frac{{{tex(bc)}\times {tex(b)}}}{{{tex(b)} - {tex(bc)}}} = {tex(C)};\quad \text{{A + B}} = \frac{{{tex(abc)}\times {tex(C)}}}{{{tex(C)} - {tex(abc)}}} = {tex(AB)} \]", fin)
    return result(("number", AB), T6, trad, rule, fin, rb, sc)


def ac_and_b(ab, bc, abc):
    ab, bc, abc = R(ab, bc, abc)
    c, a = 1 / abc - 1 / ab, 1 / abc - 1 / bc
    b = 1 / abc - (a + c)
    trad = steps(
        ("Find C's and A's one-day work.", rf"\[ \text{{C}} = {fr(1 / abc)} - {fr(1 / ab)} = {fr(c)},\qquad \text{{A}} = {fr(1 / abc)} - {fr(1 / bc)} = {fr(a)} \]"),
        ("Find (A + C).", rf"\[ \text{{A + C}} = {fr(a)} + {fr(c)} = {fr(a + c)} \]" + recip(a + c, "days")),
        ("Find B.", rf"\[ \text{{B}} = {fr(1 / abc)} - {fr(a + c)} = {fr(b)} \]" + recip(b, "days")))
    C, l1 = r6(abc, ab)
    A, l2 = r6(abc, bc)
    AC, l3 = xy_body(A, C)
    B, l4 = r6(abc, AC)
    rule = steps(("Find C and A with the specified rule.", F6 + rf"C (from A + B \(= {tex(ab)}\)): " + l1 + rf"A (from B + C \(= {tex(bc)}\)): " + l2),
                 ("Combine A and C.", r"Two workers together take \(\frac{xy}{x+y}\):" + l3),
                 ("Find B with the rule.", rf"All three \(x = {tex(abc)}\), (A + C) \(y = {tex(AC)}\):" + l4))
    fin = rf"A and C together \({tex(AC)}\) days, B alone \({tex(B)}\) days"
    rb = rbe([rf"C \(= {tex(C)}\), A \(= {tex(A)}\) days (rule with all three \(= {tex(abc)}\)).", rf"A + C \(= \frac{{{tex(A)}\times {tex(C)}}}{{{tex(A)} + {tex(C)}}} = {tex(AC)}\).",
              rf"B \(= \frac{{{tex(abc)}\times {tex(AC)}}}{{{tex(AC)} - {tex(abc)}}} = {tex(B)}\)."], fin)
    sc = shortcut(rf"\[ \text{{C}} = {tex(C)},\ \text{{A}} = {tex(A)};\ \text{{A + C}} = {tex(AC)};\ \text{{B}} = \frac{{{tex(abc)}\times {tex(AC)}}}{{{tex(AC)} - {tex(abc)}}} = {tex(B)} \]", fin)
    return result(("pair", (AC, B)), T6, trad, rule, fin, rb, sc)


def frac_b6(p, d, e):
    p, d, e = R(p, d, e)
    a, ab = p / d, (1 - p) / e
    trad = steps(
        ("Find A's one-day work.", rf"\[ {fr(p)}\div {tex(d)} = {fr(a)} \]"),
        ("Find (A + B)'s one-day work.", rf"The other \({fr(1 - p)}\) is done together in \({tex(e)}\) days:<br>\[ {fr(1 - p)}\div {tex(e)} = {fr(ab)} \]"),
        ("Find B.", rf"\[ \text{{B}} = {fr(ab)} - {fr(a)} = {fr(ab - a)} \]" + recip(ab - a, "days")))
    A, AB = d / p, e / (1 - p)
    v, line = r6(AB, A)
    rule = steps(("Find A's time and (A + B)'s time.", rf"\[ y = {tex(d)}\div {fr(p)} = {tex(A)},\qquad x = {tex(e)}\div {fr(1 - p)} = {tex(AB)} \]"),
                 ("Apply the specified rule.", F6), ("Substitute the values.", line))
    fin = fin_of(v, "days")
    rb = rbe([rf"A alone \(y = {tex(A)}\), A + B \(x = {tex(AB)}\).", r"B \(= \frac{xy}{y-x}\).", rf"B \(= {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(AB)}\times {tex(A)}}}{{{tex(A)} - {tex(AB)}}} = {tex(v)} \]", fin)
    return result(("number", v), T6, trad, rule, fin, rb, sc)


def a_finishes6(ab, b, k, b_alone_first=False):
    """A + B take ab, B alone b. Either both work k days (B stops) or B alone works k days; then A finishes."""
    ab, b, k = R(ab, b, k)
    a = 1 / ab - 1 / b
    done = k / b if b_alone_first else k / ab
    who = rf"B alone works \({tex(k)}\) days" if b_alone_first else rf"A and B work together \({tex(k)}\) days"
    trad = steps(
        ("Find A's one-day work.", rf"\[ \text{{A}} = {fr(1 / ab)} - {fr(1 / b)} = {fr(a)} \]"),
        ("Find the work left.", rf"{who}:<br>\[ 1 - {tex(k)}\times {fr(1 / b if b_alone_first else 1 / ab)} = {fr(1 - done)} \]"),
        ("Find A's time for it.", rf"\[ {fr(1 - done)}\div {fr(a)} = {tex((1 - done) / a)}\text{{ days}} \]"))
    A, line = r6(ab, b)
    v = (1 - done) * A
    rule = steps(("Find A's time with the specified rule.", rf"A and B together \(x = {tex(ab)}\), B alone \(y = {tex(b)}\):" + F6 + line),
                 ("Find the work left.", rf"\[ 1 - \frac{{{tex(k)}}}{{{tex(b if b_alone_first else ab)}}} = {fr(1 - done)} \]"),
                 ("Find A's time for it.", rf"\[ {fr(1 - done)}\times {tex(A)} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"A alone \(= \frac{{{tex(ab)}\times {tex(b)}}}{{{tex(b)} - {tex(ab)}}} = {tex(A)}\) days.", rf"Work left \(= {fr(1 - done)}\).", rf"\({fr(1 - done)}\times {tex(A)} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \text{{A}} = {tex(A)};\quad {fr(1 - done)}\times {tex(A)} = {tex(v)} \]", fin)
    return result(("number", v), T6, trad, rule, fin, rb, sc)


def called_off6(ab, k, m):
    ab, k, m = R(ab, k, m)
    left = 1 - k / ab
    a = left / m
    b = 1 / ab - a
    trad = steps(
        ("Find the work left when B goes.", rf"\[ 1 - \frac{{{tex(k)}}}{{{tex(ab)}}} = {fr(left)} \]"),
        ("Find A's one-day work.", rf"A does \({fr(left)}\) in \({tex(m)}\) days: \({fr(left)}\div {tex(m)} = {fr(a)}\), so A alone takes \({tex(1 / a)}\) days."),
        ("Find B's one-day work.", rf"\[ \text{{B}} = {fr(1 / ab)} - {fr(a)} = {fr(b)} \]So B alone takes \({tex(1 / b)}\) days."))
    A = m / left
    B, line = r6(ab, A)
    rule = steps(("Find A's time.", rf"\[ {tex(m)}\div {fr(left)} = {tex(A)}\text{{ days}} \]"),
                 ("Apply the specified rule for B.", rf"A and B together \(x = {tex(ab)}\), A alone \(y = {tex(A)}\):" + F6),
                 ("Substitute the values.", line))
    fin = rf"A \({tex(A)}\) days, B \({tex(B)}\) days"
    rb = rbe([rf"Work left \(= 1 - \frac{{{tex(k)}}}{{{tex(ab)}}} = {fr(left)}\), so A alone \(= {tex(A)}\) days.", r"B alone \(= \frac{xy}{y-x}\).",
              rf"B \(= {tex(B)}\) days."], fin)
    sc = shortcut(rf"\[ \text{{A}} = {tex(m)}\div {fr(left)} = {tex(A)};\quad \text{{B}} = \frac{{{tex(ab)}\times {tex(A)}}}{{{tex(A)} - {tex(ab)}}} = {tex(B)} \]", fin)
    return result(("pair", (A, B)), T6, trad, rule, fin, rb, sc)


def ab_from_abc6(abc, b, bc, improper=False):
    abc, b, bc = R(abc, b, bc)
    a = 1 / abc - 1 / bc
    trad = steps(
        ("Find A's one-day work.", rf"\[ \text{{A}} = (\text{{A + B + C}}) - (\text{{B + C}}) = {fr(1 / abc)} - {fr(1 / bc)} = {fr(a)} \]"),
        ("Add B's one-day work.", rf"\[ {fr(a)} + {fr(1 / b)} = {fr(a + 1 / b)} \]"),
        ("Find the time.", recip(a + 1 / b, "days", improper)))
    A, l1 = r6(abc, bc)
    AB, l2 = xy_body(A, b, num=tex)
    rule = steps(("Find A with the specified rule.", rf"All three \(x = {tex(abc)}\), (B + C) \(y = {tex(bc)}\):" + F6 + l1),
                 ("Combine A and B.", r"Two workers together take \(\frac{xy}{x+y}\):"),
                 ("Substitute the values.", l2.replace(rf"= {tex(AB)}\text", rf"= {show(AB, improper)}\text")))
    fin = fin_of(AB, "days", improper)
    rb = rbe([rf"A \(= \frac{{{tex(abc)}\times {tex(bc)}}}{{{tex(bc)} - {tex(abc)}}} = {tex(A)}\) days.", r"A and B together \(= \frac{xy}{x+y}\).",
              rf"\(\frac{{{tex(A)}\times {tex(b)}}}{{{tex(A)} + {tex(b)}}} = {show(AB, improper)}\)."], fin)
    sc = shortcut(rf"\[ \text{{A}} = {tex(A)};\quad \frac{{{tex(A)}\times {tex(b)}}}{{{tex(A)} + {tex(b)}}} = {show(AB, improper)} \]", fin)
    return result(("number", AB), T6, trad, rule, fin, rb, sc)


def three6(x, y, z):
    """A, B, C alone x, y, z: together (book Rule 6 Exercise 1)."""
    x, y, z = R(x, y, z)
    s = 1 / x + 1 / y + 1 / z
    trad = steps(("Find the one-day work of each.", rf"\[ \text{{A}} = {fr(1 / x)},\quad \text{{B}} = {fr(1 / y)},\quad \text{{C}} = {fr(1 / z)} \]"),
                 ("Add them.", rf"\[ {fr(1 / x)} + {fr(1 / y)} + {fr(1 / z)} = {fr(s)} \]"), ("Find the time.", recip(s, "days")))
    AB = x * y / (x + y)
    T = AB * z / (AB + z)
    rule = steps(("Read the specified rule backwards.", F6 + r"If the pair takes \(x\) and one of them \(y\), the other takes \(b = \frac{xy}{y-x}\). "
                                                         r"Solving for \(x\): two workers taking \(y\) and \(b\) days together take \(\frac{yb}{y+b}\) days."),
                 ("Combine A and B.", rf"\[ \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(AB)}\text{{ days}} \]"),
                 ("Combine (A + B) with C.", rf"\[ \frac{{{tex(AB)}\times {tex(z)}}}{{{tex(AB)} + {tex(z)}}} = {tex(T)}\text{{ days}} \]"))
    fin = fin_of(T, "days")
    rb = rbe([rf"A + B \(= \frac{{{tex(x)}\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(AB)}\).", rf"Add C: \(\frac{{{tex(AB)}\times {tex(z)}}}{{{tex(AB)} + {tex(z)}}}\).",
              rf"\(= {tex(T)}\) days."], fin)
    sc = shortcut(rf"\[ {tex(AB)}\ \text{{(A + B)}};\quad \frac{{{tex(AB)}\times {tex(z)}}}{{{tex(AB)} + {tex(z)}}} = {tex(T)} \]", fin)
    return result(("number", T), T6, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 7: B n times A + C, C m times A + B
T7 = (r"If B would take \(n\) times as long as A and C together, C would take \(m\) times as long as A and B together, and the three "
      r"together finish the work in \(x\) days, then<br>\[ \text{B} = x(n+1)\text{ days},\qquad \text{C} = x(m+1)\text{ days} \]"
      r"and A takes \(\frac{x(n+1)(m+1)}{nm-1}\) days.")
F7 = r"\[ \text{B} = x(n+1),\quad \text{C} = x(m+1),\quad \text{A} = \frac{x(n+1)(m+1)}{nm-1} \]"


def r7_trad(n, m, T, phrase_b, phrase_c):
    b, c = 1 / (T * (n + 1)), 1 / (T * (m + 1))
    a = 1 / T - b - c
    return a, b, c, steps(
        ("Find B's one-day work.", rf"{phrase_b} so (A + C)'s one-day work is \({n}\) times B's. Adding B's own work:<br>"
                                   rf"\[ ({n} + 1)\times \text{{B}} = \text{{A + B + C}} = {fr(1 / T)} \;\Rightarrow\; \text{{B}} = {fr(b)} \]"),
        ("Find C's one-day work.", rf"{phrase_c} so (A + B)'s one-day work is \({m}\) times C's:<br>"
                                   rf"\[ ({m} + 1)\times \text{{C}} = {fr(1 / T)} \;\Rightarrow\; \text{{C}} = {fr(c)} \]"),
        ("Find A's one-day work.", rf"\[ \text{{A}} = {fr(1 / T)} - {fr(b)} - {fr(c)} = {fr(a)} \]"))


def each7(n, m, T, phrase_b, phrase_c):
    n, m, T = R(n, m, T)
    a, b, c, trad = r7_trad(n, m, T, phrase_b, phrase_c)
    trad += "<br><br>" + rf"So A takes \({tex(1 / a)}\), B \({tex(1 / b)}\) and C \({tex(1 / c)}\) days."
    B, C, A = T * (n + 1), T * (m + 1), T * (n + 1) * (m + 1) / (n * m - 1)
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(m = {tex(m)}\), \(x = {tex(T)}\)."), ("Apply the specified rule.", F7),
                 ("Substitute the values.", rf"\[ \text{{B}} = {tex(T)}({tex(n)} + 1) = {tex(B)},\quad \text{{C}} = {tex(T)}({tex(m)} + 1) = {tex(C)} \]"
                                            rf"\[ \text{{A}} = \frac{{{tex(T)}\times {tex(n + 1)}\times {tex(m + 1)}}}{{{tex(n)}\times {tex(m)} - 1}} = \frac{{{tex(T * (n + 1) * (m + 1))}}}{{{tex(n * m - 1)}}} = {tex(A)} \]"))
    fin = triple_fin(A, B, C)
    rb = rbe([rf"\(n = {tex(n)}, m = {tex(m)}, x = {tex(T)}\).", rf"B \(= x(n+1) = {tex(B)}\), C \(= x(m+1) = {tex(C)}\).", rf"A \(= \frac{{x(n+1)(m+1)}}{{nm-1}} = {tex(A)}\)."], fin)
    sc = shortcut(rf"\[ \text{{B}} = {tex(B)},\ \text{{C}} = {tex(C)},\ \text{{A}} = \frac{{{tex(T * (n + 1) * (m + 1))}}}{{{tex(n * m - 1)}}} = {tex(A)} \]", fin)
    assert (A, B, C) == (1 / a, 1 / b, 1 / c)
    return result(("triple", (A, B, C)), T7, trad, rule, fin, rb, sc)


def bc7(n, m, T, phrase_b, phrase_c):
    n, m, T = R(n, m, T)
    a, b, c, trad = r7_trad(n, m, T, phrase_b, phrase_c)
    trad = trad.rsplit("<br><br><b>Step 3", 1)[0] + "<br><br>" + rf"<b>Step 3: Add B and C.</b><br>\[ {fr(b)} + {fr(c)} = {fr(b + c)} \]" + recip(b + c, "days")
    B, C = T * (n + 1), T * (m + 1)
    BC = B * C / (B + C)
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(m = {tex(m)}\), \(x = {tex(T)}\)."),
                 ("Apply the specified rule.", F7 + rf"\[ \text{{B}} = {tex(T)}({tex(n)} + 1) = {tex(B)},\quad \text{{C}} = {tex(T)}({tex(m)} + 1) = {tex(C)} \]"),
                 ("Put B and C together.", rf"\[ \frac{{{tex(B)}\times {tex(C)}}}{{{tex(B)} + {tex(C)}}} = \frac{{{tex(B * C)}}}{{{tex(B + C)}}} = {tex(BC)}\text{{ days}} \]"))
    fin = fin_of(BC, "days")
    rb = rbe([rf"B \(= x(n+1) = {tex(B)}\), C \(= x(m+1) = {tex(C)}\).", r"Together: \(\frac{BC}{B+C}\).", rf"\(\frac{{{tex(B * C)}}}{{{tex(B + C)}}} = {tex(BC)}\)."], fin)
    sc = shortcut(rf"\[ \text{{B}} = {tex(B)},\ \text{{C}} = {tex(C)};\quad \frac{{{tex(B)}\times {tex(C)}}}{{{tex(B)} + {tex(C)}}} = {tex(BC)} \]", fin)
    assert BC == 1 / (b + c)
    return result(("number", BC), T7, trad, rule, fin, rb, sc)


PB_LONG = r"B takes \({n}\) times as long as A and C together,"
PC_LONG = r"C takes \({m}\) times as long as A and B together,"
PB_MUCH = r"A and C together do \({n}\) times as much work as B,"
PC_MUCH = r"A and B together do \({m}\) times as much work as C,"


def r7(kind, n, m, T, much=False):
    pb, pc = (PB_MUCH, PC_MUCH) if much else (PB_LONG, PC_LONG)
    return (each7 if kind == "each" else bc7)(n, m, T, pb.format(n=n), pc.format(m=m))


# ---------------------------------------------------------------- Rule 8: x1 men or y1 women in D days
T8 = (r"If \(x_1\) men or \(y_1\) women can reap a field in \(D\) days, then \(x_2\) men and \(y_2\) women take<br>"
      r"\[ \frac{D\,x_1y_1}{x_2y_1 + x_1y_2}\text{ days} \]")
F8 = r"\[ \text{Days} = \frac{D\,x_1y_1}{x_2y_1 + x_1y_2} \]"


def mw8(x1, y1, D, x2, y2, w="women", part=1, task="reap the field"):
    part = F(part)
    m, wo = F(1, x1 * D), F(1, y1 * D)
    rate = x2 * m + y2 * wo
    v = part / rate
    ptxt = "" if part == 1 else rf"Only \({fr(part)}\) of the field is needed:<br>"
    trad = steps(
        ("Find one person's one-day work.", rf"\({x1}\) men take \({D}\) days, so 1 man does \(\frac{{1}}{{{x1}\times {D}}} = {fr(m)}\) a day; "
                                            rf"1 of the {w} does \(\frac{{1}}{{{y1}\times {D}}} = {fr(wo)}\) a day."),
        ("Find the group's one-day work.", rf"\[ {x2}\times {fr(m)} + {y2}\times {fr(wo)} = {fr(rate)} \]"),
        ("Find the time.", ptxt + rf"\[ {fr(part)}\div {fr(rate)} = {tex(v)}\text{{ days}} \]"))
    full = F(D * x1 * y1, x2 * y1 + x1 * y2)
    line = (rf"\[ \frac{{{D}\times {x1}\times {y1}}}{{{x2}\times {y1} + {x1}\times {y2}}} = \frac{{{D * x1 * y1}}}{{{x2 * y1 + x1 * y2}}} = {tex(full)} \]")
    rule = steps(("Identify the values.", rf"\(x_1 = {x1}\), \(y_1 = {y1}\), \(D = {D}\); \(x_2 = {x2}\), \(y_2 = {y2}\)."),
                 ("Apply the specified rule.", F8),
                 ("Substitute the values.", line + ("" if part == 1 else rf"That is for the whole field; for \({fr(part)}\) of it: \({fr(part)}\times {tex(full)} = {tex(v)}\) days.")))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x_1 = {x1}, y_1 = {y1}, D = {D}, x_2 = {x2}, y_2 = {y2}\).", r"Days \(= \frac{Dx_1y_1}{x_2y_1 + x_1y_2}\).",
              rf"\(\frac{{{D * x1 * y1}}}{{{x2 * y1 + x1 * y2}}} = {tex(full)}\)" + ("." if part == 1 else rf", so \({fr(part)}\times {tex(full)} = {tex(v)}\)." )], fin)
    sc = shortcut(rf"\[ \frac{{{D}\times {x1}\times {y1}}}{{{x2}\times {y1} + {x1}\times {y2}}}" + ("" if part == 1 else rf"\times {fr(part)}") + rf" = {tex(v)} \]", fin)
    return result(("number", v), T8, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 9: 1 man = (y b2 - x b1)/(x a1 - y a2) boys
T9 = (r"If \(a_1\) men and \(b_1\) boys can do a piece of work in \(x\) days and \(a_2\) men and \(b_2\) boys can do it in \(y\) days, then"
      r"<br>\[ 1\text{ man} = \frac{yb_2 - xb_1}{xa_1 - ya_2}\text{ boys} \]")
F9 = r"\[ 1\text{ man} = \frac{yb_2 - xb_1}{xa_1 - ya_2}\text{ boys} \]"


def k9(a1, b1, x, a2, b2, y):
    return F(y * b2 - x * b1) / F(x * a1 - y * a2)


def k9_line(a1, b1, x, a2, b2, y):
    k = k9(a1, b1, x, a2, b2, y)
    return k, (rf"\[ 1\text{{ man}} = \frac{{{tex(y)}\times {tex(b2)} - {tex(x)}\times {tex(b1)}}}{{{tex(x)}\times {tex(a1)} - {tex(y)}\times {tex(a2)}}} "
               rf"= \frac{{{tex(y * b2 - x * b1)}}}{{{tex(x * a1 - y * a2)}}} = {tex(k)}\text{{ boys}} \]")


def k9_trad(a1, b1, x, a2, b2, y, first="Equate the total work of the two groups."):
    k = k9(a1, b1, x, a2, b2, y)
    cm, cb = x * a1 - y * a2, y * b2 - x * b1
    if cm < 0:                                      # collect on the other side so both coefficients are positive
        cm, cb = -cm, -cb
    return k, (first, rf"Let a man do \(M\) and a boy \(B\) units a day. Both groups do the same work:<br>"
                      rf"\[ {tex(x)}({tex(a1)}M + {tex(b1)}B) = {tex(y)}({tex(a2)}M + {tex(b2)}B) \]"
                      rf"\[ {tex(x * a1)}M + {tex(x * b1)}B = {tex(y * a2)}M + {tex(y * b2)}B \]"
                      rf"\[ {tex(cm)}M = {tex(cb)}B \;\Rightarrow\; M = {tex(k)}B \]")


def mb_time9(a1, b1, x, a2, b2, y, a3, b3, man="men", boy="boys"):
    k, st = k9_trad(a1, b1, x, a2, b2, y)
    g1, g3 = a1 * k + b1, a3 * k + b3
    v = g1 * x / g3
    trad = steps(st, ("Count everyone in boys.", rf"\({a1}\) men and \({b1}\) boys \(= {tex(a1 * k)} + {b1} = {tex(g1)}\) boys; "
                                                 rf"\({a3}\) men and \({b3}\) boys \(= {tex(a3 * k)} + {b3} = {tex(g3)}\) boys."),
                 ("Use the same work.", rf"\[ {tex(g1)}\times {x} = {tex(g3)}\times D \;\Rightarrow\; D = \frac{{{tex(g1 * x)}}}{{{tex(g3)}}} = {tex(v)}\text{{ days}} \]"))
    k_, line = k9_line(a1, b1, x, a2, b2, y)
    rule = steps(("Identify the values.", rf"\(a_1 = {a1}, b_1 = {b1}, x = {x}\); \(a_2 = {a2}, b_2 = {b2}, y = {y}\)."),
                 ("Apply the specified rule.", F9 + line),
                 ("Convert and finish.", rf"\({a1}\) men + \({b1}\) boys \(= {tex(g1)}\) boys and \({a3}\) men + \({b3}\) boys \(= {tex(g3)}\) boys:<br>"
                                         rf"\[ D = \frac{{{tex(g1)}\times {x}}}{{{tex(g3)}}} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"1 man \(= \frac{{yb_2 - xb_1}}{{xa_1 - ya_2}} = {tex(k)}\) boys.", rf"Groups: \({tex(g1)}\) boys and \({tex(g3)}\) boys.",
              rf"\(D = \frac{{{tex(g1)}\times {x}}}{{{tex(g3)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ 1\text{{ man}} = {tex(k)}\text{{ boys}};\quad D = \frac{{{tex(g1)}\times {x}}}{{{tex(g3)}}} = {tex(v)} \]", fin)
    return result(("number", v), T9, trad, rule, fin, rb, sc)


def ratio_of(k, boy_first):
    """k = boys per man -> (p, q) in lowest whole numbers for man : boy (or boy : man)."""
    r = F(1) / k if boy_first else F(k)
    return r.numerator, r.denominator


def ratio9(a1, b1, x, a2, b2, y, boy_first=False, lead=None):
    k, st = k9_trad(a1, b1, x, a2, b2, y)
    p, q = ratio_of(k, boy_first)
    order = "boy : man" if boy_first else "man : boy"
    trad = steps(st if lead is None else (st[0], lead + st[1].split("<br>", 1)[1]),
                 ("Write the ratio.", rf"A man does \({tex(k)}\) times a boy's work, so {order} \(= {p} : {q}\)."))
    k_, line = k9_line(a1, b1, x, a2, b2, y)
    rule = steps(("Identify the values.", rf"\(a_1 = {tex(a1)}, b_1 = {tex(b1)}, x = {tex(x)}\); \(a_2 = {tex(a2)}, b_2 = {tex(b2)}, y = {tex(y)}\)."),
                 ("Apply the specified rule.", F9 + line),
                 ("Write the ratio.", rf"{order} \(= {p} : {q}\)."))
    fin = rf"\({p} : {q}\)"
    rb = rbe([rf"\(a_1 = {tex(a1)}, b_1 = {tex(b1)}, x = {tex(x)}, a_2 = {tex(a2)}, b_2 = {tex(b2)}, y = {tex(y)}\).",
              rf"1 man \(= \frac{{{tex(y * b2 - x * b1)}}}{{{tex(x * a1 - y * a2)}}} = {tex(k)}\) boys.", rf"{order} \(= {p} : {q}\)."], fin)
    sc = shortcut(rf"\[ 1\text{{ man}} = \frac{{{tex(y * b2 - x * b1)}}}{{{tex(x * a1 - y * a2)}}} = {tex(k)}\text{{ boys}} \;\Rightarrow\; {p} : {q} \]", fin)
    return result(("ratio", (p, q)), T9, trad, rule, fin, rb, sc)


def times9(a1, b1, n, a2=1, b2=1):
    """a1 men + b1 boys do n times as much per hour as a2 men + b2 boys: man : boy (rule with x = 1, y = n)."""
    k = F(n * b2 - b1, a1 - n * a2)
    p, q = ratio_of(k, False)
    c = lambda v: "" if v == 1 else tex(v)           # 1M -> M
    trad = steps(("Write the hourly work.", rf"Let a man do \(M\) and a boy \(B\) units an hour:<br>\[ {c(a1)}M + {c(b1)}B = {n}({c(a2)}M + {c(b2)}B) \]"
                                            rf"\[ {c(a1 - n * a2)}M = {c(n * b2 - b1)}B" + (rf" \;\Rightarrow\; M = {tex(k)}B \]" if a1 - n * a2 != 1 else r" \]")),
                 ("Write the ratio.", rf"man : boy \(= {p} : {q}\)."))
    rule = steps(("Read the question as two groups.", rf"The first group does in 1 hour what the second needs \({n}\) hours for, so \(x = 1\), \(y = {n}\), "
                                                     rf"\(a_1 = {a1}, b_1 = {b1}, a_2 = {a2}, b_2 = {b2}\)."),
                 ("Apply the specified rule.", F9 + rf"\[ 1\text{{ man}} = \frac{{{n}\times {b2} - 1\times {b1}}}{{1\times {a1} - {n}\times {a2}}} = {tex(k)}\text{{ boys}} \]"),
                 ("Write the ratio.", rf"man : boy \(= {p} : {q}\)."))
    fin = rf"\({p} : {q}\)"
    rb = rbe([rf"\(x = 1, y = {n}\); \(a_1 = {a1}, b_1 = {b1}, a_2 = {a2}, b_2 = {b2}\).", rf"1 man \(= \frac{{{n * b2 - b1}}}{{{a1 - n * a2}}} = {tex(k)}\) boys.",
              rf"man : boy \(= {p} : {q}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{n}\times {b2} - {b1}}}{{{a1} - {n}\times {a2}}} = {tex(k)} \;\Rightarrow\; {p} : {q} \]", fin)
    return result(("ratio", (p, q)), T9, trad, rule, fin, rb, sc)


def equiv9(m1, b1, D, m2, b2, em, eb):
    k = F(eb, em)
    g1, g2 = m1 * k + b1, m2 * k + b2
    v = g1 * D / g2
    trad = steps(("Write the daily work in boys' units.", rf"\({em}\) men do as much as \({eb}\) boys, so a man does \({tex(k)}\) times a boy's daily work."),
                 ("Find the whole work.", rf"Let a boy do 1 unit a day: \({m1}\) men and \({b1}\) boys do \({m1}\times {tex(k)} + {b1} = {tex(g1)}\) units a day, "
                                          rf"so the work is \({tex(g1)}\times {D} = {tex(g1 * D)}\) units."),
                 ("Find the new time.", rf"\({m2}\) men and \({b2}\) boys do \({m2}\times {tex(k)} + {b2} = {tex(g2)}\) units a day:<br>"
                                        rf"\[ {tex(g1 * D)}\div {tex(g2)} = {tex(v)}\text{{ days}} \]"))
    rule = steps(("Convert men into boys.", rf"1 man \(= \frac{{{eb}}}{{{em}}} = {tex(k)}\) boys, so \(M_1 = {tex(g1)}\) boys and \(M_2 = {tex(g2)}\) boys."),
                 ("Apply the specified rule's last step.", r"Once everyone is in the same unit, \(M_1D_1 = M_2D_2\)."),
                 ("Substitute the values.", rf"\[ D_2 = \frac{{{tex(g1)}\times {D}}}{{{tex(g2)}}} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"1 man \(= {tex(k)}\) boys.", rf"\(M_1 = {tex(g1)}\), \(M_2 = {tex(g2)}\) boys.", rf"\(D_2 = \frac{{{tex(g1)}\times {D}}}{{{tex(g2)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(g1)}\times {D}}}{{{tex(g2)}}} = {tex(v)} \]", fin)
    return result(("number", v), T9, trad, rule, fin, rb, sc)


def children9(c, m, D, m2, f=2):
    g = F(c, f) + m
    v = g * D / m2
    trad = steps(("Write the one-day work.", rf"A child takes \({f}\) times a man's time, so a child does \(\frac{{1}}{{{f}}}\) of a man's daily work. "
                                             rf"Let a man do 1 unit a day: the group does \({c}\times \frac{{1}}{{{f}}} + {m} = {tex(g)}\) units a day."),
                 ("Find the whole work.", rf"\[ {tex(g)}\times {D} = {tex(g * D)}\text{{ units}} \]"),
                 ("Find the time for the men.", rf"\[ {tex(g * D)}\div {m2} = {tex(v)}\text{{ days}} \]"))
    rule = steps(("Convert children into men.", rf"\({c}\) children \(= \frac{{{c}}}{{{f}}} = {tex(F(c, f))}\) men, so \(M_1 = {tex(F(c, f))} + {m} = {tex(g)}\) men."),
                 ("Apply the specified rule's last step.", r"With everyone in the same unit, \(M_1D_1 = M_2D_2\)."),
                 ("Substitute the values.", rf"\[ D_2 = \frac{{{tex(g)}\times {D}}}{{{m2}}} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"\({c}\) children \(= {tex(F(c, f))}\) men, so \(M_1 = {tex(g)}\).", r"\(M_1D_1 = M_2D_2\).", rf"\(D_2 = \frac{{{tex(g)}\times {D}}}{{{m2}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(g)}\times {D}}}{{{m2}}} = {tex(v)} \]", fin)
    return result(("number", v), T9, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 10: original men = x(D+d)/d
T10 = (r"A certain number of men can do a work in \(D\) days. If there were \(x\) men less it could be finished in \(d\) days more, "
       r"then the number of men originally is<br>\[ \frac{x(D+d)}{d} \]")


def orig10(D, x, d):
    M = F(x * (D + d), d)
    trad = steps(("Let the number of men be \\(M\\).", rf"The work in man-days is the same both times:<br>\[ M\times {D} = (M - {x})\times {D + d} \]"),
                 ("Open the bracket.", rf"\[ {D}M = {D + d}M - {x * (D + d)} \]"),
                 ("Solve for \\(M\\).", rf"\[ {d}M = {x * (D + d)} \;\Rightarrow\; M = {tex(M)} \]"))
    rule = steps(("Identify the values.", rf"\(D = {D}\), \(x = {x}\), \(d = {d}\)."),
                 ("Apply the specified rule.", r"\[ \text{Men} = \frac{x(D+d)}{d} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{x}({D} + {d})}}{{{d}}} = \frac{{{x}\times {D + d}}}{{{d}}} = {tex(M)} \]"))
    fin = fin_of(M, "men")
    rb = rbe([rf"\(D = {D}, x = {x}, d = {d}\).", r"Men \(= \frac{x(D+d)}{d}\).", rf"\(\frac{{{x}\times {D + d}}}{{{d}}} = {tex(M)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{x}({D} + {d})}}{{{d}}} = {tex(M)} \]", fin)
    return result(("number", M), T10, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- old-row text fixes
def trip(unit, *rows):
    return {k: rf"A \({a}\) {unit}, B \({b}\) {unit}, C \({c}\) {unit}" for k, (a, b, c) in zip("abcd", rows)}


def pair_ab(*rows):
    return {k: (rf"A \({a}\) days, B \({b}\) days" if a else "None of these") for k, (a, b) in zip("abcd", rows)}


def plain(*vals):
    return dict(zip("abcd", vals))


DISPLAY = lambda s, a, b: s.replace(a, b)
BOOK_Q = {
    201: lambda q: q.replace(r"2\[ \frac{2}{3} \] hours", r"\(2\frac{2}{3}\) hours"),
    202: lambda q: q.replace(r"4\[ \frac{4}{5} \] days", r"\(4\frac{4}{5}\) days"),
    203: lambda q: q.replace(r"A does \[ \frac{2}{5} \] of", r"A does \(\frac{2}{5}\) of").replace("by himself", "by himself?"),
    207: lambda q: q.replace("can do. A piece", "can do a piece"),
    210: lambda q: q.replace("How long would take B and C to complete", "How long would B and C take to complete"),
    211: lambda q: q.replace("he long will", "how long will"),
    213: lambda q: q.replace("12 men and 16 days can do", "12 men and 16 boys can do"),
    214: lambda q: q.replace("If 13 men and 14 boys", "If 30 men and 14 boys"),
    216: lambda q: q.replace("If 1 must hire", "If I must hire").replace(r"1\[ \frac{1}{2} \] days", r"\(1\frac{1}{2}\) days"),
    217: lambda q: q.replace("twice the time by a man", "twice the time taken by a man"),
    218: lambda q: q.replace("Iff] there were", "If there were").replace("10 day*| more", "10 days more"),
}
BOOK_OPTS = {
    194: opts("days", r"2\frac{4}{9}", r"2\frac{2}{9}", 2, r"2\frac{5}{9}"),
    195: opts("days", 25, 12, 15, 20),
    196: trip("days", (21, 42, 14), (20, 40, r"13\frac{1}{3}"), (15, 45, r"11\frac{1}{4}"), (15, 42, r"11\frac{1}{4}")),
    197: opts("hours", r"\frac{1260}{221}", r"\frac{1270}{231}", r"\frac{1221}{260}", r"\frac{1260}{231}"),
    198: trip("days", (12, 6, 4), (18, 9, 6), (24, 12, 8), (18, 12, 8)),
    199: opts("days", 20, 18, 22, 19),
    200: opts("days", 86, 48, 84, 68),
    201: opts("hours", r"3\frac{3}{7}", r"3\frac{5}{7}", r"3\frac{2}{7}", r"3\frac{4}{7}"),
    202: {k: rf"\({a}\) days, \({b}\) days" for k, (a, b) in zip("abcd", ((8, 12), (4, 8), (6, 12), (8, 16)))},
    203: opts("days", 18, 16, 12, 21),
    204: opts("days", r"7\frac{4}{5}", r"5\frac{4}{5}", r"4\frac{4}{5}", r"4\frac{1}{5}"),
    205: pair_ab((60, 60), (15, 30), (20, 60), (25, 60)),
    206: opts("days", r"\frac{240}{31}", r"\frac{242}{31}", r"\frac{241}{31}", r"\frac{244}{31}"),
    207: opts("days", 18, 24, 16, 20),
    208: trip("days", (24, 40, 30), (40, 24, 30), (28, 40, 30), (24, 30, 40)),
    209: trip("days", (r"28\frac{4}{5}", 42, 48), (r"28\frac{4}{5}", 36, 48), (28, r"36\frac{4}{5}", 48), (r"28\frac{4}{5}", 48, 36)),
    210: opts("days", r"9\frac{1}{11}", r"11\frac{1}{9}", r"26\frac{2}{3}", r"28\frac{3}{5}"),
    211: opts("days", 16, 10, 14, 12),
    212: opts("days", r"8\frac{1}{8}", r"8\frac{1}{3}", 11, r"7\frac{1}{3}"),
    213: plain("1 : 2", "2 : 1", "1 : 3", "3 : 1"),
    214: opts("days", 36, 30, 42, 45),
    215: plain("2 : 1", "3 : 1", "4 : 1", "1 : 2"),
    216: plain("7 : 3", "3 : 7", "2 : 5", "5 : 2"),
    217: opts("days", 8, 9, 12, 15),
    218: opts("men", 56, 58, 60, 52),
    1265: pair_ab((50, 50), (40, 60), (30, 50), (None, None)),
}

PLAN = {
    5: (51, {194: lambda: three5(5, 6, 12), 195: lambda: c_missing5(5, 4, 2), 196: lambda: half5(7), 197: lambda: groups5(5, 2, 7, 3, 9, 4, improper=True),
             198: lambda: twice_thrice5(2), 1251: lambda: three5(6, 8, 12), 1252: lambda: c_missing5(6, 8, 3), 1253: lambda: half5(6),
             1254: lambda: groups5(3, 4, 6, 3, 4, 9), 1255: lambda: twice_thrice5(3), 1256: lambda: three5(3, 4, 6, improper=True),
             1257: lambda: three5(4, 6, 12)}),
    6: (52, {199: lambda: other_alone(6, 9), 200: lambda: c_from_groups(28, 21), 201: lambda: ab_from_chain(6, 4, "8/3"),
             202: lambda: ac_and_b("24/5", 8, 4), 203: lambda: frac_b6("2/5", 9, 6), 204: lambda: a_finishes6(6, 16, 3),
             205: lambda: called_off6(30, 11, 38), 206: lambda: ab_from_abc6(6, 16, 10, improper=True), 207: lambda: a_finishes6(8, 12, 4, True),
             1258: lambda: other_alone(8, 12), 1259: lambda: three6(4, 8, 16), 1260: lambda: c_from_groups(24, 16),
             1261: lambda: ab_from_chain(8, 5, "8/3"), 1262: lambda: ac_and_b(6, 10, 5), 1263: lambda: frac_b6("3/5", 12, 4),
             1264: lambda: a_finishes6(10, 15, 4), 1265: lambda: called_off6(25, 10, 30), 1266: lambda: ab_from_abc6(8, 18, 12),
             1267: lambda: a_finishes6(12, 18, 6, True), 1268: lambda: other_alone(12, 16, "B", "A"), 1269: lambda: c_from_groups(20, 12)}),
    7: (53, {208: lambda: r7("each", 3, 2, 10), 209: lambda: r7("each", 2, 3, 12, much=True), 210: lambda: r7("bc", 4, 3, 5),
             1270: lambda: r7("each", 4, 3, 11), 1271: lambda: r7("each", 2, 3, 15, much=True), 1272: lambda: r7("bc", 5, 4, 6),
             1273: lambda: r7("bc", 3, 4, 12)}),
    8: (54, {211: lambda: mw8(3, 4, 43, 7, 5), 1274: lambda: mw8(4, 5, 23, 3, 2), 1275: lambda: mw8(5, 6, 39, 4, 3),
             1276: lambda: mw8(3, 4, 26, 5, 2, part=F(1, 2)), 1277: lambda: mw8(6, 8, 53, 8, 7), 1278: lambda: mw8(4, 8, 19, 6, 7, w="boys"),
             1279: lambda: mw8(5, 6, 12, 10, 6)}),
    9: (55, {212: lambda: mb_time9(12, 16, 5, 13, 24, 4, 7, 10), 213: lambda: ratio9(12, 16, 5, 13, 24, 4), 214: lambda: equiv9(30, 14, 21, 20, 4, 3, 5),
             215: lambda: times9(5, 2, 4), 216: lambda: ratio9(2, 3, 6, 11, 5, F(3, 2), boy_first=True,
                                                                  lead="Let a man do \\(M\\) and a boy \\(B\\) units a day. Both hirings do the same work:<br>"),
             217: lambda: children9(8, 12, 9, 12), 1280: lambda: mb_time9(9, 7, 6, 10, 10, 5, 5, 8), 1281: lambda: ratio9(5, 3, 4, 6, 6, 3),
             1282: lambda: equiv9(30, 10, 20, 12, 10, 3, 5), 1283: lambda: times9(7, 1, 3, 2, 1), 1284: lambda: ratio9(3, 4, 8, 10, 6, 4, boy_first=True),
             1285: lambda: children9(12, 12, 10, 15)}),
    10: (56, {218: lambda: orig10(60, 8, 10), 1286: lambda: orig10(48, 5, 12), 1287: lambda: orig10(36, 6, 12), 1288: lambda: orig10(24, 6, 18),
              1289: lambda: orig10(30, 7, 15)}),
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


if __name__ == "__main__":
    main()
