"""Rules 1-8: writes the eight rule cards (the chapter had none), regenerates every old row in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links it to its card, cleans its text
(OCR "o f", display math in the question and options, empty fifth option) and fixes options that did not hold the
answer (56, 596). Adds the book exercises that had no copy (numbers changed, wording rewritten) as one JsonImport
payload per rule. Writes ruleNN/2_new_rows.json, ruleNN/3_rule_card.json, ruleNN/3_json_import_payload.json + 3_answers.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, frac, money, new_question, rbe, regen_entry, shortcut, solution, steps, tex  # noqa: E402


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb, fin), shortcut=shortcut(sc, fin))


def P(v):
    return rf"\({tex(F(v))}\%\)"


def Fr(v):
    return rf"\({frac(F(v))}\)"


def Rs(v):
    return rf"Rs \({money(F(v))}\)"


def Num(v):
    return rf"\({tex(F(v))}\)"


def pnum(v):
    """A percentage inside math: 12\\frac{1}{2}."""
    return tex(F(v))


# ---------------------------------------------------------------- Rule 1: fraction -> per cent
T1 = r"To express a fraction \(\frac{x}{y}\) as a rate per cent, multiply it by 100:<br>\[ \frac{x}{y}\times 100\% \]"


def r1(x, y):
    v = F(100 * x, y)
    trad = steps(
        ("Per cent means 'out of 100'.", rf"Take the whole as \(100\) equal parts. One \({y}\)th of the whole is \(\frac{{100}}{{{y}}}\) of these parts."),
        ("Take the given share.", rf"\(\frac{{{x}}}{{{y}}}\) of the whole is \({x}\) such shares:<br>"
                                  rf"\[ {x}\times \frac{{100}}{{{y}}} = \frac{{{100 * x}}}{{{y}}} = {tex(v)}\text{{ parts out of 100}} \]"),
        ("Write it as a percentage.", rf"\({tex(v)}\) parts out of \(100\) is \({tex(v)}\%\)."))
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\), \(y = {y}\)."),
        ("Apply the specified rule.", r"\[ \text{Rate per cent} = \frac{x}{y}\times 100\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{x}}}{{{y}}}\times 100\% = \frac{{{100 * x}}}{{{y}}}\% = {tex(v)}\% \]"))
    rb = [rf"\(x = {x}\), \(y = {y}\).", r"Rate per cent \(= \frac{x}{y}\times 100\%\).", rf"\(\frac{{{x}}}{{{y}}}\times 100\% = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{x}}}{{{y}}}\times 100\% = {tex(v)}\% \]"
    return result(("number", v), T1, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rule 2: per cent -> fraction
T2 = r"To express a rate per cent \(x\%\) as a fraction, divide \(x\) by 100:<br>\[ x\% = \frac{x}{100} \]"


def over100(p):
    """\\frac{25}{2}\\% -> \\frac{\\frac{25}{2}}{100} = \\frac{25}{200} chain, ending in lowest terms."""
    p = F(p)
    v = p / 100
    if p.denominator == 1:
        chain = [rf"\frac{{{p}}}{{100}}"]
    else:
        chain = [rf"\frac{{{frac(p)}}}{{100}}", rf"\frac{{{p.numerator}}}{{{p.denominator * 100}}}"]
    if frac(v) != chain[-1]:
        chain.append(frac(v))
    return " = ".join(chain)


def r2(p):
    p = F(p)
    v = p / 100
    trad = steps(
        ("100% is the whole.", r"\(100\%\) of a quantity is the whole quantity, that is \(1\). So \(1\%\) is one hundredth of it:<br>"
                               r"\[ 1\% = \frac{1}{100} \]"),
        ("Take the given number of hundredths.", rf"\[ {pnum(p)}\% = {frac(p)}\times \frac{{1}}{{100}} = \frac{{{p.numerator}}}{{{p.denominator * 100}}} \]"),
        ("Reduce to lowest terms.", rf"\[ \frac{{{p.numerator}}}{{{p.denominator * 100}}} = {frac(v)} \]"))
    rule = steps(
        ("Identify the value.", rf"\(x = {pnum(p)}\)."),
        ("Apply the specified rule.", r"\[ x\% = \frac{x}{100} \]"),
        ("Substitute the value.", rf"\[ {pnum(p)}\% = {over100(p)} \]"))
    rb = [rf"\(x = {pnum(p)}\).", r"\(x\% = \frac{x}{100}\).", rf"\({pnum(p)}\% = {over100(p)}\)."]
    sc = rf"\[ {pnum(p)}\% = {over100(p)} \]"
    return result(("number", v), T2, trad, rule, Fr(v), rb, sc)


# ---------------------------------------------------------------- Rule 3: x% of an item
T3 = r"To find \(x\%\) of an item:<br>\[ x\%\text{ of the item} = \frac{x}{100}\times \text{Value of the item} \]"


def r3(x, V, fmt, what="the value"):
    x, V = F(x), F(V)
    v = x * V / 100
    trad = steps(
        ("Use the unitary method.", rf"\(100\%\) of {what} is \({money(V)}\), so \(1\%\) of it is<br>\[ \frac{{{money(V)}}}{{100}} = {money(V / 100)} \]"),
        ("Take the given per cent.", rf"\[ {pnum(x)}\%\text{{ of it}} = {pnum(x)}\times {money(V / 100)} = {money(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {pnum(x)}\), value of the item \(= {money(V)}\)."),
        ("Apply the specified rule.", r"\[ x\%\text{ of the item} = \frac{x}{100}\times \text{Value of the item} \]"),
        ("Substitute the values.", rf"\[ \frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(v)} \]"))
    rb = [rf"\(x = {pnum(x)}\), value \(= {money(V)}\).", r"\(x\%\) of the item \(= \frac{x}{100}\times\) value.",
          rf"\(\frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(v)}\)."]
    sc = rf"\[ \frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(v)} \]"
    return result(("number", v), T3, trad, rule, fmt(v), rb, sc)


def r3_units(x, total, big, small, factor, show):
    """x% of a quantity given in two units (kg and g, quintals and kg); `total` in the small unit, `show` = how the question writes it."""
    x = F(x)
    v = x * total / 100
    assert v.denominator == 1
    q, r = divmod(int(v), factor)
    bigs = big + ("s" if q != 1 and big == "quintal" else "")
    ans_txt = rf"\({q}\) {bigs} \({r}\) {small}"
    conv = rf"\[ {show} = {total}\text{{ {small}}} \qquad (1\text{{ {big}}} = {factor}\text{{ {small}}}) \]"
    back = rf"\[ {int(v)}\text{{ {small}}} = {q}\text{{ {bigs} }}{r}\text{{ {small}}} \]"
    trad = steps(
        ("Change to the smaller unit.", conv),
        ("Use the unitary method.", rf"\(1\%\) of \({total}\) {small} is \(\frac{{{total}}}{{100}} = {money(F(total, 100))}\) {small}, so<br>"
                                    rf"\[ {pnum(x)}\%\text{{ of it}} = {pnum(x)}\times {money(F(total, 100))} ={int(v)}\text{{ {small}}} \]"),
        ("Change back.", back))
    rule = steps(
        ("Identify the values.", rf"\(x = {pnum(x)}\), value of the item \(= {total}\) {small}." + conv),
        ("Apply the specified rule.", r"\[ x\%\text{ of the item} = \frac{x}{100}\times \text{Value of the item} \]"),
        ("Substitute the values.", rf"\[ \frac{{{frac(x)}}}{{100}}\times {total} = {int(v)}\text{{ {small}}} \]" + back))
    rb = [rf"Value \(= {total}\) {small}, \(x = {pnum(x)}\).", r"\(x\%\) of the item \(= \frac{x}{100}\times\) value.",
          rf"\(\frac{{{frac(x)}}}{{100}}\times {total} = {int(v)}\) {small} \(= {q}\) {bigs} \({r}\) {small}."]
    sc = rf"\[ \frac{{{frac(x)}}}{{100}}\times {total} = {int(v)}\text{{ {small}}} = {q}\text{{ {bigs} }}{r}\text{{ {small}}} \]"
    return result(("pair", (F(q), F(r))), T3, trad, rule, ans_txt, rb, sc)


def r3_left(x, V, unit):
    x, V = F(x), F(V)
    lost = x * V / 100
    left = V - lost
    trad = steps(
        ("Find the part that is left.", rf"\({pnum(x)}\%\) is lost, so \(100 - {pnum(x)} = {pnum(100 - x)}\%\) is left."),
        ("Use the unitary method.", rf"\(1\%\) of \({money(V)}\) {unit} is \({money(V / 100)}\) {unit}, so<br>"
                                    rf"\[ {pnum(100 - x)}\times {money(V / 100)} = {money(left)}\text{{ {unit}}} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {pnum(x)}\), value of the item \(= {money(V)}\) {unit}."),
        ("Apply the specified rule to the loss.", rf"\[ \text{{Loss}} = \frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(lost)}\text{{ {unit}}} \]"),
        ("Subtract the loss.", rf"\[ {money(V)} - {money(lost)} = {money(left)}\text{{ {unit}}} \]"))
    fin = rf"\({money(left)}\) {unit}"
    rb = [rf"\(x = {pnum(x)}\), value \(= {money(V)}\) {unit}.", rf"Loss \(= \frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(lost)}\).",
          rf"Left \(= {money(V)} - {money(lost)} = {money(left)}\) {unit}."]
    sc = rf"\[ {money(V)} - \frac{{{frac(x)}}}{{100}}\times {money(V)} = {money(V)} - {money(lost)} = {money(left)} \]"
    return result(("number", left), T3, trad, rule, fin, rb, sc)


def r3_election(winner_pct, M):
    """Two candidates; the winner gets winner_pct% of the votes and wins by M votes."""
    w = F(winner_pct)
    lo = 100 - w
    d = w - lo
    T = M * 100 / d
    trad = steps(
        ("Find each candidate's share.", rf"The winner gets \({pnum(w)}\%\) of the votes, so the other candidate gets \(100 - {pnum(w)} = {pnum(lo)}\%\)."),
        ("Turn the gap into a per cent.", rf"The gap between them is \({pnum(w)} - {pnum(lo)} = {pnum(d)}\%\) of all the votes, and this gap is \({M}\) votes."),
        ("Use the unitary method.", rf"\[ {pnum(d)}\% \to {M}\text{{ votes}},\qquad 1\% \to \frac{{{M}}}{{{pnum(d)}}},\qquad 100\% \to \frac{{{M}\times 100}}{{{pnum(d)}}} = {tex(T)} \]"))
    rule = steps(
        ("Let the total number of votes be \\(T\\).", rf"By the rule, the winner gets \(\frac{{{pnum(w)}}}{{100}}\times T\) votes and the other gets \(\frac{{{pnum(lo)}}}{{100}}\times T\) votes."),
        ("Use the majority.", rf"\[ \frac{{{pnum(w)}}}{{100}}T - \frac{{{pnum(lo)}}}{{100}}T = {M} \]\[ \frac{{{pnum(d)}}}{{100}}T = {M} \]"),
        ("Solve.", rf"\[ T = \frac{{{M}\times 100}}{{{pnum(d)}}} = {tex(T)} \]"))
    fin = rf"\({tex(T)}\) votes"
    rb = [rf"Shares: \({pnum(w)}\%\) and \({pnum(lo)}\%\) of \(T\).", rf"\(\frac{{{pnum(w)}}}{{100}}T - \frac{{{pnum(lo)}}}{{100}}T = {M}\).",
          rf"\(T = \frac{{{M}\times 100}}{{{pnum(d)}}} = {tex(T)}\)."]
    sc = rf"\[ T = \frac{{{M}\times 100}}{{{pnum(w)} - {pnum(lo)}}} = {tex(T)} \]"
    return result(("number", T), T3, trad, rule, fin, rb, sc)


def r3_shobha():
    parts = [(10, 70, "arithmetic"), (30, 40, "algebra"), (35, 60, "geometry")]
    got = [F(n * p, 100) for n, p, _ in parts]
    need = F(60 * 75, 100)
    more = need - sum(got)
    trad = steps(
        ("Count the right answers one section at a time.", "<br>".join(
            rf"{name}: \({p}\%\) of \({n}\) is \({p}\) out of every \(100\), i.e. \(\frac{{{p}}}{{100}}\) of \({n}\) \(= {tex(g)}\)"
            for (n, p, name), g in zip(parts, got)) + rf"<br>Total right \(= {' + '.join(tex(g) for g in got)} = {tex(sum(got))}\)"),
        ("Count the right answers needed.", rf"\(60\%\) of \(75\): \(1\%\) of \(75\) is \(0.75\), so \(60\times 0.75 = {tex(need)}\)."),
        ("Find the shortfall.", rf"\[ {tex(need)} - {tex(sum(got))} = {tex(more)} \]"))
    rule = steps(
        ("Apply the specified rule to each section.", rf"\[ \frac{{70}}{{100}}\times 10 + \frac{{40}}{{100}}\times 30 + \frac{{60}}{{100}}\times 35 = 7 + 12 + 21 = {tex(sum(got))} \]"),
        ("Apply it to the pass mark.", rf"\[ \frac{{60}}{{100}}\times 75 = {tex(need)} \]"),
        ("Subtract.", rf"\[ {tex(need)} - {tex(sum(got))} = {tex(more)} \]"))
    fin = rf"\({tex(more)}\) more questions"
    rb = [r"Right answers \(= \frac{70}{100}\times 10 + \frac{40}{100}\times 30 + \frac{60}{100}\times 35 = 40\).",
          r"Needed \(= \frac{60}{100}\times 75 = 45\).", rf"\(45 - 40 = {tex(more)}\)."]
    sc = rf"\[ \frac{{60}}{{100}}\times 75 - \left(7 + 12 + 21\right) = 45 - 40 = {tex(more)} \]"
    return result(("number", more), T3, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 4: x% of N is y -> N
T4 = r"If \(x\%\) of a number \(N\) is \(y\), then<br>\[ N = \frac{y}{x}\times 100 \]"


def r4(x, y, fmt, what="the number"):
    x, y = F(x), F(y)
    N = y * 100 / x
    trad = steps(
        ("Write the per cent as a fraction.", rf"\[ {pnum(x)}\% = \frac{{{pnum(x)}}}{{100}} = {frac(x / 100)} \]"),
        ("Form the equation.", rf"Let {what} be \(N\). Then<br>\[ {frac(x / 100)}\times N = {money(y)} \]"),
        ("Solve for N.", rf"\[ N = {money(y)}\div {frac(x / 100)} = {money(y)}\times {frac(100 / x)} = {money(N)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {pnum(x)}\), \(y = {money(y)}\)."),
        ("Apply the specified rule.", r"\[ N = \frac{y}{x}\times 100 \]"),
        ("Substitute the values.", rf"\[ N = \frac{{{money(y)}\times 100}}{{{pnum(x)}}} = \frac{{{money(y * 100)}}}{{{frac(x)}}} = {money(N)} \]"))
    rb = [rf"\(x = {pnum(x)}\), \(y = {money(y)}\).", r"\(N = \frac{y}{x}\times 100\).", rf"\(N = \frac{{{money(y)}\times 100}}{{{pnum(x)}}} = {money(N)}\)."]
    sc = rf"\[ N = \frac{{{money(y)}\times 100}}{{{pnum(x)}}} = {money(N)} \]"
    return result(("number", N), T4, trad, rule, fmt(N), rb, sc)


def r4_left(x, R):
    x, R = F(x), F(R)
    left = 100 - x
    N = R * 100 / left
    trad = steps(
        ("Find what is left as a per cent.", rf"She spends \({pnum(x)}\%\), so \(100 - {pnum(x)} = {pnum(left)}\%\) of her money is left."),
        ("Form the equation.", rf"Let her money at first be Rs \(M\). Then<br>\[ M - \frac{{{pnum(x)}}}{{100}}M = {money(R)} \]\[ \frac{{{pnum(left)}}}{{100}}M = {money(R)} \]"),
        ("Solve.", rf"\[ M = \frac{{{money(R)}\times 100}}{{{pnum(left)}}} = {money(N)} \]"))
    rule = steps(
        ("Identify the values.", rf"The money left, Rs \({money(R)}\), is \(x = {pnum(left)}\%\) of the money at first, so \(y = {money(R)}\)."),
        ("Apply the specified rule.", r"\[ N = \frac{y}{x}\times 100 \]"),
        ("Substitute the values.", rf"\[ N = \frac{{{money(R)}}}{{{pnum(left)}}}\times 100 = {money(N)} \]"))
    rb = [rf"Rs \({money(R)}\) is \({pnum(left)}\%\) of the money at first.", r"\(N = \frac{y}{x}\times 100\).",
          rf"\(N = \frac{{{money(R)}}}{{{pnum(left)}}}\times 100 = {money(N)}\)."]
    sc = rf"\[ N = \frac{{{money(R)}\times 100}}{{100 - {pnum(x)}}} = {money(N)} \]"
    return result(("number", N), T4, trad, rule, Rs(N), rb, sc)


# ---------------------------------------------------------------- Rule 5: what per cent is R of N
T5 = r"If \(x\%\) of a number \(N\) (the Original Number) is the Result \(R\), then<br>\[ x = \frac{R}{N}\times 100 \]"


def r5(R, N, Rtxt, Ntxt, conv=""):
    """R and N as Fractions in one unit; Rtxt / Ntxt = how they are written in the working; conv = a unit-conversion note."""
    R, N = F(R), F(N)
    x = R / N * 100
    pre = (conv + "<br>") if conv else ""
    trad = steps(
        ("Form the equation.", pre + rf"Let \({Rtxt}\) be \(p\%\) of \({Ntxt}\). Then<br>\[ \frac{{p}}{{100}}\times {Ntxt} = {Rtxt} \]"),
        ("Solve for p.", rf"\[ p = \frac{{{Rtxt}\times 100}}{{{Ntxt}}} = {tex(x)} \]"))
    rule = steps(
        ("Identify the values.", pre + rf"The value after 'of' is the Original Number: \(N = {Ntxt}\); the Result is \(R = {Rtxt}\)."),
        ("Apply the specified rule.", r"\[ x = \frac{R}{N}\times 100 \]"),
        ("Substitute the values.", rf"\[ x = \frac{{{Rtxt}}}{{{Ntxt}}}\times 100 = {tex(x)} \]"))
    rb = [rf"\(N = {Ntxt}\), \(R = {Rtxt}\).", r"\(x = \frac{R}{N}\times 100\).", rf"\(x = \frac{{{Rtxt}}}{{{Ntxt}}}\times 100 = {tex(x)}\%\)."]
    sc = rf"\[ \frac{{{Rtxt}}}{{{Ntxt}}}\times 100 = {tex(x)}\% \]"
    return result(("number", x), T5, trad, rule, P(x), rb, sc)


# ---------------------------------------------------------------- Rule 6: x1/x = y1/y = N/100
T6 = r"If \(x\%\) and \(y\%\) of a number \(N\) are \(x_1\) and \(y_1\) respectively, then<br>\[ \frac{x_1}{x} = \frac{y_1}{y} = \frac{N}{100} \]"


def r6(x, x1, y=None, y1=None, both=False):
    """Give y to find y1 (and N when both=True), or y1 to find y."""
    x, x1 = F(x), F(x1)
    N = x1 * 100 / x
    find_n = steps(("Find the number.", rf"Let the number be \(N\). \({pnum(x)}\%\) of \(N\) is \({tex(x1)}\):<br>"
                                        rf"\[ \frac{{{pnum(x)}}}{{100}}\times N = {tex(x1)} \Rightarrow N = \frac{{{tex(x1)}\times 100}}{{{pnum(x)}}} = {tex(N)} \]"))
    if y is not None:
        y = F(y)
        y1 = x1 * y / x
        trad = find_n + "<br><br>" + rf"<b>Step 2: Take the second per cent.</b><br>\[ {pnum(y)}\%\text{{ of }} {tex(N)} = \frac{{{pnum(y)}}}{{100}}\times {tex(N)} = {tex(y1)} \]"
        rule = steps(
            ("Identify the values.", rf"\(x = {pnum(x)}\), \(x_1 = {tex(x1)}\), \(y = {pnum(y)}\)."),
            ("Apply the specified rule.", r"\[ \frac{x_1}{x} = \frac{y_1}{y} \Rightarrow y_1 = \frac{x_1\times y}{x} \]"),
            ("Substitute the values.", rf"\[ y_1 = \frac{{{tex(x1)}\times {pnum(y)}}}{{{pnum(x)}}} = {tex(y1)} \]"
                                       + (rf"\[ \frac{{N}}{{100}} = \frac{{x_1}}{{x}} \Rightarrow N = \frac{{{tex(x1)}\times 100}}{{{pnum(x)}}} = {tex(N)} \]" if both else "")))
        if both:
            fin = rf"\({tex(y1)}\) and \({tex(N)}\)"
            ans = ("pair", (y1, N))
            rb = [rf"\(x = {pnum(x)}\), \(x_1 = {tex(x1)}\), \(y = {pnum(y)}\).", rf"\(y_1 = \frac{{x_1 y}}{{x}} = {tex(y1)}\).",
                  rf"\(N = \frac{{100 x_1}}{{x}} = {tex(N)}\)."]
            sc = rf"\[ y_1 = \frac{{{tex(x1)}\times {pnum(y)}}}{{{pnum(x)}}} = {tex(y1)},\qquad N = \frac{{{tex(x1)}\times 100}}{{{pnum(x)}}} = {tex(N)} \]"
        else:
            fin = Num(y1)
            ans = ("number", y1)
            rb = [rf"\(x = {pnum(x)}\), \(x_1 = {tex(x1)}\), \(y = {pnum(y)}\).", r"\(\frac{x_1}{x} = \frac{y_1}{y}\).",
                  rf"\(y_1 = \frac{{{tex(x1)}\times {pnum(y)}}}{{{pnum(x)}}} = {tex(y1)}\)."]
            sc = rf"\[ y_1 = \frac{{{tex(x1)}\times {pnum(y)}}}{{{pnum(x)}}} = {tex(y1)} \]"
        return result(ans, T6, trad, rule, fin, rb, sc)
    y1 = F(y1)
    y = y1 * x / x1
    trad = find_n + "<br><br>" + rf"<b>Step 2: Compare.</b><br>\[ \frac{{{tex(y1)}}}{{{tex(N)}}}\times 100 = {tex(y)}\% \]"
    rule = steps(
        ("Identify the values.", rf"\(x = {pnum(x)}\), \(x_1 = {tex(x1)}\), \(y_1 = {tex(y1)}\)."),
        ("Apply the specified rule.", r"\[ \frac{x_1}{x} = \frac{y_1}{y} \Rightarrow y = \frac{y_1\times x}{x_1} \]"),
        ("Substitute the values.", rf"\[ y = \frac{{{tex(y1)}\times {pnum(x)}}}{{{tex(x1)}}} = {tex(y)} \]"))
    rb = [rf"\(x = {pnum(x)}\), \(x_1 = {tex(x1)}\), \(y_1 = {tex(y1)}\).", r"\(\frac{x_1}{x} = \frac{y_1}{y}\).",
          rf"\(y = \frac{{{tex(y1)}\times {pnum(x)}}}{{{tex(x1)}}} = {tex(y)}\%\)."]
    sc = rf"\[ y = \frac{{{tex(y1)}\times {pnum(x)}}}{{{tex(x1)}}} = {tex(y)}\% \]"
    return result(("number", y), T6, trad, rule, P(y), rb, sc)


# ---------------------------------------------------------------- Rule 7: total = difference / difference % x 100
T7 = (r"If the absolute difference of two items A and B and their difference in per cent are given, then<br>"
      r"\[ \text{Total value} = \frac{\text{Value of absolute difference}}{\text{Difference in per cent}}\times 100 \]")


def r7(d, p, ask, item="price", unit="Rs"):
    """ask: 'orig', 'new_up', 'new_down', 'both_up' (prices) or 'full' (full marks)."""
    d, p = F(d), F(p)
    base = d * 100 / p
    money_ = unit == "Rs"
    val = (lambda v: rf"Rs \({money(v)}\)") if money_ else (lambda v: rf"\({tex(v)}\) marks")
    if ask == "full":
        trad = steps(
            ("Form the equation.", rf"Let the full marks be \(M\). The difference of \({tex(d)}\) marks is \({pnum(p)}\%\) of \(M\):<br>"
                                   rf"\[ \frac{{{pnum(p)}}}{{100}}\times M = {tex(d)} \]"),
            ("Solve.", rf"\[ M = \frac{{{tex(d)}\times 100}}{{{pnum(p)}}} = {tex(base)} \]"))
        rule = steps(
            ("Identify the values.", rf"Absolute difference \(= {tex(d)}\) marks, difference in per cent \(= {pnum(p)}\)."),
            ("Apply the specified rule.", r"\[ \text{Full marks} = \frac{\text{Difference of marks}}{\text{Percentage difference}}\times 100 \]"),
            ("Substitute the values.", rf"\[ \frac{{{tex(d)}}}{{{pnum(p)}}}\times 100 = {tex(base)} \]"))
        fin = rf"\({tex(base)}\) marks"
        rb = [rf"Difference \(= {tex(d)}\), difference in per cent \(= {pnum(p)}\).", r"Full marks \(= \frac{\text{difference}}{\text{per cent difference}}\times 100\).",
              rf"\(\frac{{{tex(d)}}}{{{pnum(p)}}}\times 100 = {tex(base)}\)."]
        sc = rf"\[ \frac{{{tex(d)}}}{{{pnum(p)}}}\times 100 = {tex(base)} \]"
        return result(("number", base), T7, trad, rule, fin, rb, sc)
    up = ask in ("new_up", "both_up", "orig")
    new = base + d if up else base - d
    word = "increase" if up else "decrease"
    trad_steps = [
        ("Form the equation.", rf"Let the original {item} be Rs \(P\). A {word} of \({pnum(p)}\%\) of \(P\) is Rs \({money(d)}\):<br>"
                               rf"\[ \frac{{{pnum(p)}}}{{100}}\times P = {money(d)} \]"),
        ("Solve.", rf"\[ P = \frac{{{money(d)}\times 100}}{{{pnum(p)}}} = {money(base)} \]")]
    rule_steps = [
        ("Identify the values.", rf"Treat the original and the new {item} as two items: their absolute difference is Rs \({money(d)}\) "
                                 rf"and their difference in per cent is \({pnum(p)}\)."),
        ("Apply the specified rule.", rf"\[ \text{{Original {item}}} = \frac{{\text{{Difference in {item}}}}}{{\text{{Difference in per cent}}}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{money(d)}}}{{{pnum(p)}}}\times 100 = {money(base)} \]")]
    rb = [rf"Difference \(= {money(d)}\), difference in per cent \(= {pnum(p)}\).",
          rf"Original {item} \(= \frac{{{money(d)}}}{{{pnum(p)}}}\times 100 = {money(base)}\)."]
    sc = rf"\[ \frac{{{money(d)}}}{{{pnum(p)}}}\times 100 = {money(base)} \]"
    sign = "+" if up else "-"
    if ask == "orig":
        fin, ans = val(base), ("number", base)
    else:
        step = ("Find the new " + item + ".", rf"\[ {money(base)} {sign} {money(d)} = {money(new)} \]")
        trad_steps.append(step)
        rule_steps.append(step)
        rb.append(rf"New {item} \(= {money(base)} {sign} {money(d)} = {money(new)}\).")
        sc = rf"\[ \frac{{{money(d)}}}{{{pnum(p)}}}\times 100 = {money(base)},\qquad {money(base)} {sign} {money(d)} = {money(new)} \]"
        if ask == "both_up":
            fin, ans = rf"original {item} Rs \({money(base)}\), new {item} Rs \({money(new)}\)", ("pair", (base, new))
        else:
            fin, ans = val(new), ("number", new)
    return result(ans, T7, steps(*trad_steps), steps(*rule_steps), fin, rb, sc)


# ---------------------------------------------------------------- Rule 8: milk in a mixture of two liquids
T8 = (r"If one type of liquid contains \(X\%\) of milk and the other contains \(Y\%\) of milk, and a can is filled with \(x\) parts of the "
      r"first liquid and \(y\) parts of the second, then the percentage of milk in the new mixture is<br>\[ \frac{xX + yY}{x + y}\% \]")


def r8(X, Y, x, y):
    v = F(x * X + y * Y, x + y)
    trad = steps(
        ("Take each part as 100 litres.", rf"First liquid: \({x}\) parts \(= {100 * x}\) litres holding \(\frac{{{X}}}{{100}}\times {100 * x} = {x * X}\) litres of milk.<br>"
                                          rf"Second liquid: \({y}\) parts \(= {100 * y}\) litres holding \(\frac{{{Y}}}{{100}}\times {100 * y} = {y * Y}\) litres of milk."),
        ("Add up.", rf"Milk \(= {x * X} + {y * Y} = {x * X + y * Y}\) litres in \({100 * x} + {100 * y} = {100 * (x + y)}\) litres of mixture."),
        ("Find the percentage.", rf"\[ \frac{{{x * X + y * Y}}}{{{100 * (x + y)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(X = {X}\), \(Y = {Y}\), \(x = {x}\), \(y = {y}\)."),
        ("Apply the specified rule.", r"\[ \frac{xX + yY}{x + y}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{x}\times {X} + {y}\times {Y}}}{{{x} + {y}}} = \frac{{{x * X + y * Y}}}{{{x + y}}} = {tex(v)}\% \]"))
    rb = [rf"\(X = {X}\), \(Y = {Y}\), \(x = {x}\), \(y = {y}\).", r"Milk \(= \frac{xX + yY}{x + y}\%\).",
          rf"\(\frac{{{x}\times {X} + {y}\times {Y}}}{{{x + y}}} = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{x}\times {X} + {y}\times {Y}}}{{{x} + {y}}} = {tex(v)}\% \]"
    return result(("number", v), T8, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    1: card(1, "Fraction to Per Cent",
            r"To express any fraction \(\frac{x}{y}\) as a rate per cent, multiply it by 100.",
            r"\[ \frac{x}{y} = \frac{x}{y}\times 100\% \]",
            [("Fraction", r"\frac{x}{y}"), ("Multiply by 100", r"\frac{x}{y}\times 100"), ("Write the % sign", r"\frac{100x}{y}\%")],
            r"Per cent means 'out of 100'. Multiplying by 100 tells how many of every 100 parts the fraction stands for.",
            "The question gives a fraction (or a decimal) and asks 'what percentage is equivalent to it?'.",
            r"\(\frac{3}{8}\times 100\% = \frac{300}{8}\% = 37\frac{1}{2}\%\).",
            r"Forgetting to multiply by 100 (writing \(\frac{3}{8} = 0.375\%\)), or rounding a repeating value such as \(84\frac{8}{13}\%\)."),
    2: card(2, "Per Cent to Fraction",
            r"To express a rate per cent \(x\%\) as a fraction, divide \(x\) by 100 and reduce to lowest terms.",
            r"\[ x\% = \frac{x}{100} \]",
            [("Rate per cent", r"x\%"), ("Divide by 100", r"\frac{x}{100}"), ("Mixed rate first made improper", r"12\frac{1}{2}\% = \frac{25}{2}\times\frac{1}{100}")],
            r"\(100\%\) is the whole, so \(1\%\) is \(\frac{1}{100}\) of it and \(x\%\) is \(x\) hundredths.",
            "The question asks 'what fraction is x per cent?' or 'express x% as a fraction'.",
            r"\(12\frac{1}{2}\% = \frac{25/2}{100} = \frac{25}{200} = \frac{1}{8}\).",
            r"Dividing only the whole-number part of a mixed rate by 100, or not reducing the fraction to lowest terms."),
    3: card(3, "x% of an Item",
            r"To find \(x\%\) of an item, multiply the value of the item by \(\frac{x}{100}\).",
            r"\[ x\%\text{ of the item} = \frac{x}{100}\times \text{Value of the item} \]",
            [("Value of the item", r"V"), ("1% of it", r"\frac{V}{100}"), ("x% of it", r"\frac{x}{100}\times V")],
            r"\(x\%\) means \(x\) out of every 100, so each 100 of the value gives \(x\).",
            "Commission, duty, tax, leakage, votes, marks: 'find x% of ...'. For a quantity in two units, change it to the smaller unit first.",
            r"\(8\%\) of Rs \(625 = \frac{8}{100}\times 625 =\) Rs \(50\).",
            r"Mixing units (kg with g, quintals with kg) before multiplying, or forgetting to subtract when the question asks what is LEFT."),
    4: card(4, "Find the Number from x% of It",
            r"If \(x\%\) of a number \(N\) is \(y\), then the number is \(\frac{y}{x}\times 100\).",
            r"\[ N = \frac{y}{x}\times 100 \]",
            [("Given", r"x\%\text{ of } N = y"), ("1% of N", r"\frac{y}{x}"), ("Whole number (100%)", r"\frac{y}{x}\times 100")],
            r"If \(x\) parts out of 100 make \(y\), one part is \(\frac{y}{x}\), and all 100 parts make \(\frac{100y}{x}\).",
            "'x% of what number is y?', or 'after spending x%, y is left' (then y is (100 - x)% of the number).",
            r"\(25\%\) of a number is \(36\): \(N = \frac{36}{25}\times 100 = 144\).",
            r"Using the spent per cent instead of the per cent LEFT when the question gives the amount left."),
    5: card(5, "What Per Cent Is R of N",
            r"If \(x\%\) of a number \(N\) (the Original Number) is the Result \(R\), then the percentage is \(\frac{R}{N}\times 100\). "
            r"The value after the word 'of' is the Original Number.",
            r"\[ x = \frac{R}{N}\times 100 \]",
            [("Original Number (after 'of')", r"N"), ("Result", r"R"), ("Percentage", r"\frac{R}{N}\times 100")],
            r"The percentage tells how many of every 100 parts of \(N\) make up \(R\).",
            "'R is what per cent of N?', 'express R as a percentage of N'. Put both in the same unit first (paise and rupees, kg and tonnes).",
            r"\(\frac{1}{3}\) as a percentage of \(\frac{5}{9}\): \(\frac{1/3}{5/9}\times 100 = 60\%\).",
            r"Putting the numbers the wrong way round (the value after 'of' goes in the denominator) or leaving the units different."),
    6: card(6, "Two Percentages of the Same Number",
            r"If \(x\%\) and \(y\%\) of a number \(N\) are \(x_1\) and \(y_1\) respectively, then the three ratios are equal.",
            r"\[ \frac{x_1}{x} = \frac{y_1}{y} = \frac{N}{100} \]",
            [("x% of N", r"x_1"), ("y% of N", r"y_1"), ("One per cent of N", r"\frac{x_1}{x} = \frac{y_1}{y} = \frac{N}{100}")],
            r"Each of the three ratios is the value of \(1\%\) of the same number.",
            "One percentage of a number and its value are given; another percentage, its value or the number itself is asked.",
            r"\(25\%\) of a number is \(20\): \(40\%\) of it is \(\frac{20}{25}\times 40 = 32\) and the number is \(\frac{20}{25}\times 100 = 80\).",
            r"Writing \(\frac{x}{x_1} = \frac{y_1}{y}\) (one ratio upside down)."),
    7: card(7, "Total from a Difference and Its Per Cent",
            r"If the absolute difference of two items A and B and their difference in per cent are given, the total (original) value is the "
            r"difference divided by the per cent difference, times 100.",
            r"\[ \text{Total value} = \frac{\text{Value of absolute difference}}{\text{Difference in per cent}}\times 100 \]",
            [("Absolute difference", r"d"), ("Difference in per cent", r"p\%"), ("Total (original) value", r"\frac{d}{p}\times 100")],
            r"The difference is \(p\%\) of the total, so this is Rule 4 with \(x = p\) and \(y = d\).",
            "A price rises or falls by p% and the change in rupees is given; two candidates' marks differ by d marks, which is p% of the full marks.",
            r"Price up by \(12\frac{1}{2}\%\), increase Rs 5: original \(= \frac{5}{12\frac{1}{2}}\times 100 =\) Rs 40, new price Rs 45.",
            r"Giving the original value when the NEW value is asked (add or subtract the difference at the end)."),
    8: card(8, "Milk Percentage in a Mixture of Two Liquids",
            r"If one type of liquid contains \(X\%\) of milk and the other contains \(Y\%\) of milk, and a can is filled with \(x\) parts of the "
            r"first liquid and \(y\) parts of the second, the percentage of milk in the new mixture is the weighted average.",
            r"\[ \text{Milk in the mixture} = \frac{xX + yY}{x + y}\% \]",
            [("First liquid", r"x\text{ parts at } X\%"), ("Second liquid", r"y\text{ parts at } Y\%"), ("Mixture", r"\frac{xX + yY}{x + y}\%")],
            r"Total milk divided by total liquid: each part brings its own share of milk, so the percentages are weighted by the parts.",
            "Two liquids with given milk (or acid, alcohol) percentages are mixed in given parts; the percentage in the mixture is asked.",
            r"\(6\) parts at \(25\%\) and \(4\) parts at \(30\%\): \(\frac{6\times 25 + 4\times 30}{10} = 27\%\).",
            r"Taking the simple average \(\frac{X + Y}{2}\) when the parts are not equal."),
}

# ---------------------------------------------------------------- old rows: builder, cleaned question, cleaned options
OLD = {
    1: {583: (lambda: r1(3, 8), r"What percentage is equivalent to \(\frac{3}{8}\)?",
              {"a": P(35), "b": P(F(75, 2)), "c": P(F(85, 2)), "d": P(F(125, 2))})},
    2: {584: (lambda: r2(F(25, 2)), r"What fraction is \(12\frac{1}{2}\%\)?",
              {"a": Fr(F(1, 2)), "b": Fr(F(3, 4)), "c": Fr(F(6, 7)), "d": Fr(F(1, 8))})},
    3: {56: (r3_shobha, "Shobha's mathematics test had 75 problems: 10 arithmetic, 30 algebra and 35 geometry problems. She answered 70% of "
                        "the arithmetic, 40% of the algebra and 60% of the geometry problems correctly, but she did not pass because she got "
                        "less than 60% of the problems right. How many more questions would she have had to answer correctly to earn the "
                        "60% passing grade?",
             {"a": Num(3), "b": Num(5), "c": Num(7), "d": Num(10)}),
        585: (lambda: r3(8, 625, Rs, "the amount"), "Find 8% of Rs 625.", None),
        586: (lambda: r3_left(8, 425, "litres"), "A cask containing 425 litres lost 8% by leakage. How many litres were left in the cask?", None),
        587: (lambda: r3_election(62, 144), "At an election where there are only two candidates, the candidate who gets 62 per cent of the votes "
                                            "is elected by a majority of 144 votes. Find the total number of votes recorded.", None)},
    4: {588: (lambda: r4(25, 36, Num), "25% of what number is 36?", None),
        589: (lambda: r4_left(69, 93), "After spending 69% of her money, a lady has Rs 93 left. How much had she at first?", None)},
    5: {47: (lambda: r5(F(1, 2), F(1, 3), r"\frac{1}{2}", r"\frac{1}{3}"), r"\(\frac{1}{2}\) is what per cent of \(\frac{1}{3}\)?",
             {"a": P(157), "b": P(151), "c": P(150), "d": P(154)}),
        590: (lambda: r5(F(5, 8), F(35, 28), "0.625", r"1\frac{7}{28}"), r"0.625 is equal to what per cent of \(1\frac{7}{28}\)?",
              {"a": P(60), "b": P(80), "c": P(30), "d": P(50)}),
        591: (lambda: r5(125, 1000, "125", "1000", r"1 metric tonne \(= 1000\) kg and 1 quintal 25 kg \(= 100 + 25 = 125\) kg."),
              "What rate per cent is 1 quintal 25 kg of 1 metric tonne?",
              {"a": P(F(25, 2)), "b": P(25), "c": P(F(45, 2)), "d": P(45)}),
        592: (lambda: r5(6, 100, "6", "100", r"Re 1 \(= 100\) paise, and the Result is \(6\) paise."), "What rate per cent is 6 P (paise) of the Re (one rupee)?",
              {"a": P(5), "b": P(6), "c": P(12), "d": P(18)}),
        593: (lambda: r5(F(1, 3), F(5, 9), r"\frac{1}{3}", r"\frac{5}{9}"), r"Express \(\frac{1}{3}\) as a percentage of \(\frac{5}{9}\).",
              {"a": P(60), "b": P(F(500, 3)), "c": P(30), "d": P(90)})},
    6: {594: (lambda: r6(25, 20, y=40, both=True), "25% of a number is 20. What is 40% of that number? Also find the number.",
              {"a": r"\(12\) and \(16\)", "b": r"\(65\) and \(42\)", "c": r"\(23\) and \(40\)", "d": r"\(32\) and \(80\)"})},
    7: {595: (lambda: r7(5, F(25, 2), "both_up", "price"),
              r"If the price of one kg of wheat is increased by \(12\frac{1}{2}\%\), the increase is Rs 5. Find the original and the new price of wheat per kg.",
              {"a": "Original price = Rs 20, New price = Rs 15", "b": "Original price = Rs 40, New price = Rs 45",
               "c": "Original price = Rs 34, New price = Rs 52", "d": "Original price = Rs 45, New price = Rs 40"})},
    8: {596: (lambda: r8(25, 30, 6, 4), "One type of liquid contains 25% of milk and the other contains 30% of milk. A can is filled with 6 parts "
                                        "of the first liquid and 4 parts of the second liquid. Find the percentage of milk in the new mixture.",
              {"a": P(32), "b": P(27), "c": P(F(55, 2)), "d": P(26)})},
}

# ---------------------------------------------------------------- new questions (book exercises with no copy; numbers changed)
NEW = {
    1: [("r1_e1", r"Convert \(\frac{2}{5}\) into a percentage.", lambda: r1(2, 5), [P(25), P(40), P(45), P(60)], 2),
        ("r1_e2", r"What percentage is equal to \(\frac{7}{8}\)?", lambda: r1(7, 8), [P(F(175, 2)), P(F(157, 2)), P(F(165, 2)), P(70)], 1),
        ("r1_e3", r"Express \(\frac{19}{20}\) as a rate per cent.", lambda: r1(19, 20), [P(19), P(90), P(85), P(95)], 4),
        ("r1_e4", r"Which percentage is equivalent to \(\frac{13}{14}\)?", lambda: r1(13, 14),
         [P(F(645, 7)), P(F(649, 7)), P(F(650, 7)), P(F(643, 7))], 3),
        ("r1_e5", r"Write the fraction \(\frac{9}{11}\) as a percentage.", lambda: r1(9, 11),
         [P(F(900, 11)), P(F(892, 11)), P(F(800, 11)), P(F(1000, 11))], 1)],
    2: [("r2_e1", r"\(6\frac{1}{4}\%\) written as a fraction in its lowest terms is", lambda: r2(F(25, 4)), [Fr(F(1, 25)), Fr(F(1, 4)), Fr(F(1, 16)), Fr(F(5, 16))], 3),
        ("r2_e2", r"What fraction is \(17\frac{1}{2}\%\)?", lambda: r2(F(35, 2)), [Fr(F(7, 20)), Fr(F(7, 40)), Fr(F(17, 40)), Fr(F(1, 4))], 2),
        ("r2_e3", "Which fraction is equal to 35 per cent?", lambda: r2(35), [Fr(F(7, 10)), Fr(F(3, 5)), Fr(F(7, 50)), Fr(F(7, 20))], 4),
        ("r2_e4", r"Express \(28\frac{4}{5}\%\) as a fraction.", lambda: r2(F(144, 5)), [Fr(F(36, 125)), Fr(F(26, 125)), Fr(F(36, 145)), Fr(F(44, 125))], 1),
        ("r2_e5", "Express 20% as a fraction in its lowest terms.", lambda: r2(20), [Fr(F(1, 20)), Fr(F(1, 5)), Fr(F(2, 5)), Fr(F(1, 50))], 2),
        ("r2_e6", r"What fraction is \(16\frac{2}{3}\%\)?", lambda: r2(F(50, 3)), [Fr(F(1, 16)), Fr(F(2, 3)), Fr(F(1, 6)), Fr(F(3, 16))], 3),
        ("r2_e7", "Express 200% as a fraction (or whole number).", lambda: r2(200), [Fr(F(1, 2)), Fr(F(1, 20)), Num(20), Num(2)], 4)],
    3: [("r3_e1", "Find 6% of Rs 4250.", lambda: r3(6, 4250, Rs, "the amount"), [Rs(215), Rs(255), Rs(265), Rs(425)], 2),
        ("r3_e2", "What is 35% of Rs 840?", lambda: r3(35, 840, Rs, "the amount"), [Rs(294), Rs(249), Rs(284), Rs(336)], 1),
        ("r3_e3", r"Find \(37\frac{1}{2}\%\) of Rs 1600.", lambda: r3(F(75, 2), 1600, Rs, "the amount"), [Rs(480), Rs(640), Rs(600), Rs(375)], 3),
        ("r3_e4", "Find the value of 9 per cent of Rs 2300.", lambda: r3(9, 2300, Rs, "the amount"), [Rs(270), Rs(217), Rs(197), Rs(207)], 4),
        ("r3_e5", "Find the value of 3 per cent of Rs 8350.", lambda: r3(3, 8350, Rs, "the amount"),
         [Rs(F(511, 2)), Rs(F(501, 2)), Rs(F(411, 2)), Rs(F(491, 2))], 2),
        ("r3_e6", "Find 8% of 42 kg 500 g.", lambda: r3_units(8, 42500, "kg", "g", 1000, r"42\text{ kg }500\text{ g}"),
         [r"\(3\) kg \(400\) g", r"\(3\) kg \(40\) g", r"\(4\) kg \(300\) g", r"\(3\) kg \(450\) g"], 1),
        ("r3_e7", "Find 35 per cent of 6 quintals.", lambda: r3_units(35, 600, "quintal", "kg", 100, r"6\text{ quintals}"),
         [r"\(2\) quintals \(1\) kg", r"\(1\) quintal \(10\) kg", r"\(2\) quintals \(10\) kg", r"\(2\) quintals \(40\) kg"], 3),
        ("r3_e8", r"Find \(33\frac{1}{3}\) per cent of 5 kg 418 g.", lambda: r3_units(F(100, 3), 5418, "kg", "g", 1000, r"5\text{ kg }418\text{ g}"),
         [r"\(1\) kg \(860\) g", r"\(1\) kg \(606\) g", r"\(2\) kg \(806\) g", r"\(1\) kg \(806\) g"], 4),
        ("r3_e9", r"A broker sells goods worth Rs 3256 and charges a commission of \(12\frac{1}{2}\%\). How much commission does he get?",
         lambda: r3(F(25, 2), 3256, Rs, "the sale value"), [Rs(417), Rs(407), Rs(397), Rs(F(1628, 5))], 2),
        ("r3_e10", r"Customs duty is charged at \(3\frac{1}{2}\%\). What is the duty on goods worth Rs 7400?",
         lambda: r3(F(7, 2), 7400, Rs, "the value of the goods"), [Rs(259), Rs(295), Rs(249), Rs(222)], 1),
        ("r3_e11", r"A tax collector is paid \(2\frac{1}{2}\%\) of the money he collects. How much does he get for collecting Rs 8400?",
         lambda: r3(F(5, 2), 8400, Rs, "the money collected"), [Rs(201), Rs(168), Rs(210), Rs(252)], 3),
        ("r3_e12", "An auctioneer charges 8% of the sale price for selling a car. The car is sold for Rs 4365. What is the auctioneer's commission?",
         lambda: r3(8, 4365, Rs, "the sale price"), [Rs(F(1971, 5)), Rs(F(873, 2)), Rs(F(1716, 5)), Rs(F(1746, 5))], 4),
        ("r3_e13", "In an election between only two candidates, the losing candidate gets 46% of the votes and loses by 344 votes. "
                   "Find the total number of votes cast.", lambda: r3_election(54, 344), [Num(3440), Num(4300), Num(4000), Num(3700)], 2)],
    4: [("r4_e1", "45% of what number is 81?", lambda: r4(45, 81, Num), [Num(160), Num(200), Num(180), Num(225)], 3),
        ("r4_e2", r"\(14\frac{2}{7}\%\) of what number is 65?", lambda: r4(F(100, 7), 65, Num), [Num(455), Num(445), Num(465), Num(910)], 1),
        ("r4_e3", r"\(11\frac{1}{9}\%\) of what number is 83?", lambda: r4(F(100, 9), 83, Num), [Num(774), Num(747), Num(830), Num(664)], 2),
        ("r4_e4", r"A sum of money is such that \(4\frac{1}{2}\%\) of it is Rs 72. Find the sum.", lambda: r4(F(9, 2), 72, Rs, "the sum"),
         [Rs(1440), Rs(1800), Rs(1500), Rs(1600)], 4),
        ("r4_e5", "If 23% of the oranges in a godown number 1863, how many oranges are there in the godown?", lambda: r4(23, 1863, Num, "the number of oranges"),
         [Num(8600), Num(7900), Num(8100), Num(9100)], 3),
        ("r4_e6", r"\(6\frac{1}{4}\%\) of a certain number is 39. Find the number.", lambda: r4(F(25, 4), 39, Num),
         [Num(642), Num(624), Num(584), Num(664)], 2)],
    5: [("r5_e1", r"Rs \(8\frac{1}{3}\) is what per cent of Rs \(13\frac{8}{9}\)?", lambda: r5(F(25, 3), F(125, 9), r"8\frac{1}{3}", r"13\frac{8}{9}"),
         [P(65), P(54), P(60), P(F(200, 3))], 3)],
    6: [("r6_e1", r"If \(37\frac{1}{2}\%\) of a number is 120, what is 45% of the number?", lambda: r6(F(75, 2), 120, y=45),
         [Num(144), Num(154), Num(136), Num(180)], 1),
        ("r6_e2", r"\(8\frac{1}{3}\%\) of a number is 35. What is \(41\frac{2}{3}\%\) of the same number?", lambda: r6(F(25, 3), 35, y=F(125, 3)),
         [Num(157), Num(175), Num(210), Num(140)], 2),
        ("r6_e3", "52% of a number is 377. What is 72% of that number?", lambda: r6(52, 377, y=72), [Num(552), Num(502), Num(540), Num(522)], 4),
        ("r6_e4", r"\(17\frac{1}{2}\%\) of a number is 56. 120 is what per cent of that number?", lambda: r6(F(35, 2), 56, y1=120),
         [P(35), P(40), P(F(75, 2)), P(F(65, 2))], 3),
        ("r6_e5", "45% of a number is 135. What per cent of the number is 200?", lambda: r6(45, 135, y1=200),
         [P(F(200, 3)), P(60), P(75), P(F(125, 2))], 1)],
    7: [("r7_e1", "Ravi and Sohan wrote the same test. Ravi scored 45 marks more than Sohan, and this difference was 18% of the full marks. "
                  "Find the full marks of the test.", lambda: r7(45, 18, "full", unit="marks"), [Num(225), Num(250), Num(270), Num(300)], 2),
        ("r7_e2", "The price of 1 kg of dal is raised by 20%, which makes it Rs 14 dearer. What is the new price of dal per kg?",
         lambda: r7(14, 20, "new_up", "price"), [Rs(70), Rs(56), Rs(98), Rs(84)], 4),
        ("r7_e3", r"The price of a bag goes up by \(12\frac{1}{2}\%\), an increase of Rs 45. Find the original price of the bag.",
         lambda: r7(45, F(25, 2), "orig", "price"), [Rs(360), Rs(405), Rs(315), Rs(400)], 1),
        ("r7_e4", r"The price of a notebook is cut by \(14\frac{2}{7}\%\), which brings it down by Rs 4. What is the new price of the notebook?",
         lambda: r7(4, F(100, 7), "new_down", "price"), [Rs(28), Rs(32), Rs(24), Rs(20)], 3),
        ("r7_e5", "The marks of P and Q in an examination differ by 36, and this difference is 24% of the full marks. Find the full marks.",
         lambda: r7(36, 24, "full", unit="marks"), [Num(144), Num(150), Num(180), Num(120)], 2),
        ("r7_e6", "X and Y took the same examination. Their marks differ by 27, which is 9% of the maximum marks. What are the maximum marks?",
         lambda: r7(27, 9, "full", unit="marks"), [Num(243), Num(270), Num(330), Num(300)], 4)],
    8: [("r8_e1", "Liquid P has 18% milk and liquid Q has 28% milk. A vessel is filled with 3 parts of P and 3 parts of Q. "
                  "What percentage of the mixture is milk?", lambda: r8(18, 28, 3, 3), [P(23), P(46), P(22), P(25)], 1),
        ("r8_e2", "One liquid is 12% milk and another is 6% milk. A jar holds 5 parts of the first and 4 parts of the second. "
                  "Find the percentage of milk in the jar.", lambda: r8(12, 6, 5, 4), [P(F(29, 3)), P(9), P(F(28, 3)), P(F(39, 4))], 3),
        ("r8_e3", "Two liquids contain 20% and 2% milk. 2 parts of the first are mixed with 7 parts of the second. "
                  "What is the percentage of milk in the mixture?", lambda: r8(20, 2, 2, 7), [P(11), P(6), P(5), P(8)], 2),
        ("r8_e4", "A can is filled with 7 parts of a liquid that is 35% milk and 13 parts of a liquid that is 15% milk. "
                  "What is the percentage of milk in the can?", lambda: r8(35, 15, 7, 13), [P(25), P(20), P(24), P(22)], 4),
        ("r8_e5", "Liquid A contains 18% milk and liquid B contains 30% milk. A container is filled with 4 parts of A and 5 parts of B. "
                  "Find the percentage of milk in the container.", lambda: r8(18, 30, 4, 5), [P(F(74, 3)), P(24), P(F(76, 3)), P(F(68, 3))], 1)],
}


def main():
    for n in range(1, 9):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, opts) in OLD[n].items():
            extra = {"question": question, **(opts or {})}
            if rows[rid]["e"] is None or rows[rid]["e"].strip():
                extra["e"] = ""                      # the page draws option e; NULL prints "None", an old 5th option is not checked
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn, op, pos in NEW[n]:
            g = fn()
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "percentage", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
