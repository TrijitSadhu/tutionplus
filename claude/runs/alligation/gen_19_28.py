"""Rules 19-28: regenerates every row in the prompt #10 layout (Theorem -> Traditional Method -> Specified Rule ->
Verification -> Final Answer) and builds the 6 missing book worked examples (Rules 20, 23, 25, 26 and two for 28)
as JsonImport payloads with new numbers. Writes ruleNN/2_new_rows.json (+ 3_json_import_payload.json / 3_answers.json)."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import frac, money, new_question, pct, ratio, ratio_steps, rbe, regen_entry, rtex, shortcut, solution, steps, tex  # noqa: E402

R = lambda *v: tuple(F(x) for x in v)
TIMES = chr(92) + 'times'


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rb, shortcut=sc)


def ftex(v):
    """Fraction as \\frac{a}{b} (or a whole number) - for shares and proportions."""
    return frac(F(v))


# ---------------------------------------------------------------- Rule 19: vessels of different sizes
T19 = (r"If vessels of sizes \(S_1, S_2, \ldots, S_x\) hold two liquids in the ratios \(a_1 : b_1, \ldots, a_x : b_x\) and are emptied into one vessel, then<br>"
       r"\[ \text{First} : \text{Second} = \left(\frac{a_1S_1}{a_1+b_1} + \cdots + \frac{a_xS_x}{a_x+b_x}\right) : \left(\frac{b_1S_1}{a_1+b_1} + \cdots + \frac{b_xS_x}{a_x+b_x}\right) \]")


def sizes_mix(sizes, pairs, first, second, extra=0, pct_text=""):
    sizes, pairs, extra = [F(s) for s in sizes], [(F(a), F(b)) for a, b in pairs], F(extra)
    A = [s * a / (a + b) for s, (a, b) in zip(sizes, pairs)]
    B = [s * b / (a + b) for s, (a, b) in zip(sizes, pairs)]
    tA, tB = sum(A), sum(B)
    r = ratio(tA, tB + extra)
    rows = "".join(rf"<tr><td>\({tex(s)}\)</td><td>\({tex(a)} : {tex(b)}\)</td><td>\({tex(s)}\times\frac{{{tex(a)}}}{{{tex(a + b)}}} = {tex(x)}\)</td>"
                   rf"<td>\({tex(s)}\times\frac{{{tex(b)}}}{{{tex(a + b)}}} = {tex(y)}\)</td></tr>" for s, (a, b), x, y in zip(sizes, pairs, A, B))
    table = f'<table border="1" cellpadding="4"><tr><th>Size (litres)</th><th>Ratio</th><th>{first.capitalize()}</th><th>{second.capitalize()}</th></tr>{rows}</table>'
    add_line = rf"<br>Then \({tex(extra)}\) litres of water are added: {second} \(= {tex(tB)} + {tex(extra)} = {tex(tB + extra)}\)." if extra else ""
    trad = steps(
        ("Work out each vessel.", (pct_text + "<br>" if pct_text else "") + table),
        ("Add up.", rf"\[ \text{{{first.capitalize()}}} = {' + '.join(tex(x) for x in A)} = {tex(tA)},\qquad \text{{{second.capitalize()}}} = {' + '.join(tex(y) for y in B)} = {tex(tB)} \]" + add_line),
        ("Compare.", rf"\[ {tex(tA)} : {tex(tB + extra)} = {rtex(r)} \]")
    )
    sa = " + ".join(rf"\frac{{{tex(a)}\times{tex(s)}}}{{{tex(a + b)}}}" for s, (a, b) in zip(sizes, pairs))
    sb = " + ".join(rf"\frac{{{tex(b)}\times{tex(s)}}}{{{tex(a + b)}}}" for s, (a, b) in zip(sizes, pairs))
    rule = steps(("Identify the values.", "Sizes " + ", ".join(rf"\({tex(s)}\)" for s in sizes) + "; ratios " + ", ".join(rf"\({tex(a)} : {tex(b)}\)" for a, b in pairs) + "."),
                 ("Apply the specified rule.", rf"\[ \left({sa}\right) : \left({sb}\right) \]"),
                 ("Simplify.", rf"\[ = {tex(tA)} : {tex(tB)} \]" + (rf"Adding \({tex(extra)}\) litres of water: \({tex(tA)} : ({tex(tB)} + {tex(extra)}) = {tex(tA)} : {tex(tB + extra)}\).<br>" if extra else "")
                  + rf"\[ = {rtex(r)} \]"))
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"{first.capitalize()} \(= {' + '.join(tex(x) for x in A)} = {tex(tA)}\).", rf"{second.capitalize()} \(= {' + '.join(tex(y) for y in B)}" + (rf" + {tex(extra)}" if extra else "") + rf" = {tex(tB + extra)}\).",
              rf"Ratio \(= {tex(tA)} : {tex(tB + extra)} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ {tex(tA)} : {tex(tB + extra)} = {rtex(r)} \]", fin)
    return result(("ratio", r), T19, trad, rule, fin, rb, sc)


P = lambda *ps: [(p, 100 - p) for p in ps]
PCT = r"A concentration of \(p\%\) means milk : water \(= p : (100 - p)\)."
PLAN19 = {1168: lambda: sizes_mix([5, 10, 15], [(2, 3), (3, 7), (4, 11)], "spirit", "water"),
          1169: lambda: sizes_mix([60, 70], [(13, 7), (18, 17)], "wine", "water", 25),
          1170: lambda: sizes_mix([4, 7, 10], P(90, 80, 70), "milk", "water", pct_text=PCT),
          1171: lambda: sizes_mix([6, 8, 9, 14], [(2, 1), (5, 3), (6, 3), (9, 5)], "milk", "water"),
          1172: lambda: sizes_mix([5, 8, 10], P(60, 75, 80), "milk", "water", pct_text=PCT)}

# ---------------------------------------------------------------- Rule 20: water to bring two milks to an average value
T20 = (r"If \(M_1\) units of milk at Rs \(x\) and \(M_2\) units at Rs \(y\) are mixed with water so that the mixture is worth Rs \(z\) per unit, the water added is<br>"
       r"\[ \text{Water} = \frac{M_1(x - z) + M_2(y - z)}{z} \]")


def water_avg(M1, x, M2, y, z, unit="kilolitres"):
    M1, x, M2, y, z = R(M1, x, M2, y, z)
    w = (M1 * (x - z) + M2 * (y - z)) / z
    cost = M1 * x + M2 * y
    trad = steps(
        ("Find the total cost.", rf"\[ {tex(M1)}\times{money(x)} + {tex(M2)}\times{money(y)} = {money(M1 * x)} + {money(M2 * y)} = {money(cost)} \]"),
        ("Let the water be \\(w\\) " + unit + ".", rf"Water costs nothing, so the whole \(({tex(M1 + M2)} + w)\) {unit} must be worth Rs \({money(z)}\) each:<br>"
         rf"\[ \frac{{{money(cost)}}}{{{tex(M1 + M2)} + w}} = {money(z)} \]"),
        ("Solve for \\(w\\).", rf"\[ {tex(M1 + M2)} + w = \frac{{{money(cost)}}}{{{money(z)}}} = {tex(cost / z)} \;\Rightarrow\; w = {tex(w)} \]")
    )
    rule = steps(("Identify the values.", rf"\(M_1 = {tex(M1)}\), \(x = {money(x)}\), \(M_2 = {tex(M2)}\), \(y = {money(y)}\), \(z = {money(z)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Water} = \frac{M_1(x - z) + M_2(y - z)}{z} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(M1)}({money(x)} - {money(z)}) + {tex(M2)}({money(y)} - {money(z)})}}{{{money(z)}}} = \frac{{{tex(M1 * (x - z))} + {tex(M2 * (y - z))}}}{{{money(z)}}} = {tex(w)}\text{{ {unit}}} \]"))
    fin = rf"\({tex(w)}\) {unit}"
    rb = rbe([rf"\(M_1 = {tex(M1)}\), \(x = {money(x)}\), \(M_2 = {tex(M2)}\), \(y = {money(y)}\), \(z = {money(z)}\).",
              rf"\(M_1(x - z) + M_2(y - z) = {tex(M1 * (x - z) + M2 * (y - z))}\).", rf"Water \(= \frac{{{tex(M1 * (x - z) + M2 * (y - z))}}}{{{money(z)}}} = {tex(w)}\) {unit}."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(M1 * (x - z))} + {tex(M2 * (y - z))}}}{{{money(z)}}} = {tex(w)} \]", fin)
    return result(("number", w), T20, trad, rule, fin, rb, sc)


PLAN20 = {1173: lambda: water_avg(5, 5800, 6, 6000, 5000), 1174: lambda: water_avg(6, 730, 7, 660, 600), 1175: lambda: water_avg(5, 570, 7, 690, 540)}

# ---------------------------------------------------------------- Rule 21: mixing two alloys (or two strengths)
T21 = (r"If one alloy has a fraction \(x\) of zinc, another has \(y\), and the mix must have \(z\) (\(z\) between \(x\) and \(y\)), they are mixed in the ratio<br>"
       r"\[ \frac{Q_1}{Q_2} = \frac{|y - z|}{|z - x|} \]")


def two_alloys(r1, r2, rt):
    f1, f2, ft = (F(a, a + b) for a, b in (r1, r2, rt))
    r = ratio(abs(f2 - ft), abs(ft - f1))
    trad = steps(
        ("Write the zinc share of each alloy.", rf"First alloy \(= \frac{{{r1[0]}}}{{{r1[0] + r1[1]}}}\), second alloy \(= \frac{{{r2[0]}}}{{{r2[0] + r2[1]}}}\), new alloy \(= \frac{{{rt[0]}}}{{{rt[0] + rt[1]}}}\)."),
        ("Mix \\(p\\) kg of the first with \\(q\\) kg of the second.", rf"Zinc must make up \(\frac{{{rt[0]}}}{{{rt[0] + rt[1]}}}\) of the \((p + q)\) kg:<br>"
         rf"\[ {ftex(f1)}p + {ftex(f2)}q = {ftex(ft)}(p + q) \]"),
        ("Collect the terms.", rf"\[ \left({ftex(f1)} - {ftex(ft)}\right)p = \left({ftex(ft)} - {ftex(f2)}\right)q \;\Rightarrow\; {ftex(f1 - ft)}\,p = {ftex(ft - f2)}\,q \]"),
        ("Find the ratio.", rf"\[ \frac{{p}}{{q}} = \frac{{{ftex(ft - f2)}}}{{{ftex(f1 - ft)}}} = {rtex(r).replace(' : ', ':')} \]So the alloys are mixed in the ratio \({rtex(r)}\).")
    )
    rule = steps(("Identify the values.", rf"\(x = {ftex(f1)}\), \(y = {ftex(f2)}\), \(z = {ftex(ft)}\) (zinc shares)."),
                 ("Apply the specified rule.", r"\[ \frac{Q_1}{Q_2} = \frac{|y - z|}{|z - x|} \]"),
                 ("Substitute the values.", rf"\[ \frac{{\left|{ftex(f2)} - {ftex(ft)}\right|}}{{\left|{ftex(ft)} - {ftex(f1)}\right|}} = \frac{{{ftex(abs(f2 - ft))}}}{{{ftex(abs(ft - f1))}}} = {rtex(r).replace(' : ', ':')} \]"))
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"Zinc shares \(x = {ftex(f1)}\), \(y = {ftex(f2)}\), \(z = {ftex(ft)}\).", rf"\(|y - z| = {ftex(abs(f2 - ft))}\), \(|z - x| = {ftex(abs(ft - f1))}\).",
              rf"Ratio \(= {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{ftex(abs(f2 - ft))}}}{{{ftex(abs(ft - f1))}}} = {rtex(r).replace(' : ', ':')} \]", fin)
    return result(("ratio", r), T21, trad, rule, fin, rb, sc)


def whisky_replaced(p_old, p_new, p_final):
    a, b, c = R(p_old, p_new, p_final)
    f = (a - c) / (a - b)
    keep = ratio(c - b, a - c)
    trad = steps(
        ("Let a fraction \\(f\\) of the whisky be replaced.", rf"The jar keeps \((1 - f)\) of the \({pct(a)}\%\) whisky and gets \(f\) of the \({pct(b)}\%\) whisky."),
        ("Balance the alcohol.", rf"\[ {pct(a)}(1 - f) + {pct(b)}f = {pct(c)} \]\[ {pct(a)} - {pct(a - b)}f = {pct(c)} \;\Rightarrow\; f = \frac{{{pct(a - c)}}}{{{pct(a - b)}}} = {ftex(f)} \]")
    )
    rule = steps(("Identify the values.", rf"Strengths \(x = {pct(a)}\%\) (left in the jar), \(y = {pct(b)}\%\) (poured in), \(z = {pct(c)}\%\) (result)."),
                 ("Apply the specified rule.", r"\[ \frac{Q_1}{Q_2} = \frac{|y - z|}{|z - x|} \]"),
                 ("Substitute the values.", rf"\[ \frac{{\text{{Whisky kept}}}}{{\text{{Whisky replaced}}}} = \frac{{|{pct(b)} - {pct(c)}|}}{{|{pct(c)} - {pct(a)}|}} = \frac{{{pct(c - b)}}}{{{pct(a - c)}}} = {rtex(keep).replace(' : ', ':')} \]"
                  rf"So the part replaced \(= \frac{{{keep[1]}}}{{{keep[0]} + {keep[1]}}} = {ftex(f)}\)."))
    fin = rf"\({ftex(f)}\)"
    rb = rbe([rf"\(x = {pct(a)}\), \(y = {pct(b)}\), \(z = {pct(c)}\).", rf"Kept : replaced \(= {pct(c - b)} : {pct(a - c)} = {rtex(keep)}\).", rf"Replaced \(= {ftex(f)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{pct(a)} - {pct(c)}}}{{{pct(a)} - {pct(b)}}} = {ftex(f)} \]", fin)
    return result(("number", f), T21, trad, rule, fin, rb, sc)


PLAN21 = {1176: lambda: two_alloys((1, 4), (2, 3), (1, 2)), 1177: lambda: two_alloys((1, 4), (3, 5), (3, 7)),
          1178: lambda: two_alloys((2, 5), (4, 7), (1, 2)), 1179: lambda: two_alloys((3, 4), (4, 5), (10, 13)),
          1180: lambda: whisky_replaced(45, 20, 30)}

# ---------------------------------------------------------------- Rule 22: rate for the remaining quantity
T22 = (r"If \(n\) kg are bought at Rs \(P\) per kg and \(m\) kg are sold at \(x\%\) profit, the remaining must be sold at<br>"
       r"\[ \text{Rate} = P\left(1 + \frac{ny - mx}{100(n - m)}\right) \]<br>per kg to make \(y\%\) profit on the whole.")


def remaining_rate(n, Pr, m, x, y, name, item):
    n, Pr, m, x, y = R(n, Pr, m, x, y)
    total_sp = n * Pr * (100 + y) / 100
    first_sp = m * Pr * (100 + x) / 100
    rate = (total_sp - first_sp) / (n - m)
    assert rate == Pr * (1 + (n * y - m * x) / (100 * (n - m)))
    trad = steps(
        ("Selling price needed for the whole lot.", rf"Cost \(= {tex(n)}\times{money(Pr)} = {money(n * Pr)}\); with \({pct(y)}\%\) profit:<br>\[ {money(n * Pr)}\times\frac{{{tex(100 + y)}}}{{100}} = {money(total_sp)} \]"),
        ("Money from the part already sold.", rf"\[ {tex(m)}\times{money(Pr)}\times\frac{{{tex(100 + x)}}}{{100}} = {money(first_sp)} \]"),
        ("Rate for the remaining.", rf"\[ \frac{{{money(total_sp)} - {money(first_sp)}}}{{{tex(n)} - {tex(m)}}} = \frac{{{money(total_sp - first_sp)}}}{{{tex(n - m)}}} = {money(rate)} \]")
    )
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(P = {money(Pr)}\), \(m = {tex(m)}\), \(x = {pct(x)}\), \(y = {pct(y)}\)."),
                 ("Apply the specified rule.", r"\[ P\left(1 + \frac{ny - mx}{100(n - m)}\right) \]"),
                 ("Substitute the values.", rf"\[ {money(Pr)}\left(1 + \frac{{{tex(n)}\times{pct(y)} - {tex(m)}\times{pct(x)}}}{{100\times{tex(n - m)}}}\right) = {money(Pr)}\left(1 + \frac{{{tex(n * y - m * x)}}}{{{tex(100 * (n - m))}}}\right) = {money(rate)} \]"))
    fin = rf"Rs \({money(rate)}\) per kg"
    rb = rbe([rf"\(n = {tex(n)}\), \(P = {money(Pr)}\), \(m = {tex(m)}\), \(x = {pct(x)}\), \(y = {pct(y)}\).", rf"\(\frac{{ny - mx}}{{100(n - m)}} = \frac{{{tex(n * y - m * x)}}}{{{tex(100 * (n - m))}}}\).",
              rf"Rate \(= {money(Pr)}\times{tex(1 + (n * y - m * x) / (100 * (n - m)))} = {money(rate)}\)."], fin)
    sc = shortcut(rf"\[ {money(Pr)}\left(1 + \frac{{{tex(n * y - m * x)}}}{{{tex(100 * (n - m))}}}\right) = {money(rate)} \]", fin)
    return result(("number", rate), T22, trad, rule, fin, rb, sc)


PLAN22 = {1181: lambda: remaining_rate(180, 20, 60, 15, 25, "Kavita", "rice"), 1182: lambda: remaining_rate(100, 12, 40, 10, 20, "Meera", "wheat"),
          1183: lambda: remaining_rate(70, 9, 20, 5, 10, "Rita", "pulses"), 1184: lambda: remaining_rate(120, 30, 40, 10, 20, "the shopkeeper", "sugar")}

# ---------------------------------------------------------------- Rule 23: replace to make half-and-half
T23 = (r"If a container holds \(x\) parts of one liquid and \(y\) parts of another, the part of the mixture to draw off and replace with the second liquid "
       r"so that the container becomes half and half is<br>\[ a = \frac{1}{2}\left(\frac{x - y}{x}\right) \]")


def half_half(x, y, kept, added):
    x, y = R(x, y)
    share = x / (x + y)
    a = (x - y) / (2 * x)
    trad = steps(
        ("Take one unit of mixture.", rf"It holds \({ftex(share)}\) {kept} and \({ftex(1 - share)}\) {added}."),
        ("Draw off a fraction \\(f\\) and refill with " + added + ".", rf"Only the {kept} that remains counts: \({ftex(share)}(1 - f)\). It must be half the container:<br>"
         rf"\[ {ftex(share)}(1 - f) = \frac{{1}}{{2}} \]"),
        ("Solve for \\(f\\).", rf"\[ 1 - f = \frac{{1}}{{2}}\times{ftex(1 / share)} = {ftex(1 / (2 * share))} \;\Rightarrow\; f = {ftex(a)} \]")
    )
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) parts of {kept}, \(y = {tex(y)}\) parts of {added}."),
                 ("Apply the specified rule.", r"\[ a = \frac{1}{2}\left(\frac{x - y}{x}\right) \]"),
                 ("Substitute the values.", rf"\[ \frac{{1}}{{2}}\left(\frac{{{tex(x)} - {tex(y)}}}{{{tex(x)}}}\right) = \frac{{{tex(x - y)}}}{{{tex(2 * x)}}} = {ftex(a)} \]"))
    fin = rf"\({ftex(a)}\) of the mixture"
    rb = rbe([rf"\(x = {tex(x)}\) ({kept}), \(y = {tex(y)}\) ({added}).", rf"\(x - y = {tex(x - y)}\), \(2x = {tex(2 * x)}\).", rf"Part drawn off \(= {ftex(a)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)} - {tex(y)}}}{{2\times{tex(x)}}} = {ftex(a)} \]", fin)
    return result(("number", a), T23, trad, rule, fin, rb, sc)


PLAN23 = {1185: lambda: half_half(7, 4, "syrup", "water"), 1186: lambda: half_half(5, 2, "ale", "porter"),
          1187: lambda: half_half(10, 6, "milk", "water"), 1188: lambda: half_half(7, 5, "milk", "water"), 1189: lambda: half_half(5, 1, "milk", "water")}

# ---------------------------------------------------------------- Rule 24: add a cheaper item to lower the price
T24 = (r"If a cask holds \(L\) litres of milk costing Rs \(x\) per litre, the water to add so that the cost becomes Rs \(y\) per litre is<br>"
       r"\[ \text{Water} = L\left(\frac{x - y}{y}\right) \]")
T24C = T24 + (r"<br>When the item added is not free but costs Rs \(c\), the same reasoning gives "
              r"\(\text{Quantity added} = L\left(\frac{x - y}{y - c}\right)\), which is the rule above with \(c = 0\).")


def lower_price(L, x, y, unit, base, added, c=0, price_note="", count=False):
    L, x, y, c = R(L, x, y, c)
    q = L * (x - y) / (y - c)
    cur = lambda v: rf"Rs \({money(v)}\)"
    trad = steps(
        ("Find the cost of what is there.", (price_note + "<br>" if price_note else "") + rf"\[ {tex(L)}\times{money(x)} = {money(L * x)} \]"),
        ("Add \\(w\\) of the cheaper item.", rf"{added.capitalize()} costs {cur(c)} each; the mixture must cost {cur(y)} each:<br>"
         rf"\[ {money(L * x)} + {money(c)}w = {money(y)}({tex(L)} + w) \]" if c else
         rf"Water costs nothing; the mixture must cost {cur(y)} per {unit}:<br>\[ {money(L * x)} = {money(y)}({tex(L)} + w) \]"),
        ("Solve for \\(w\\).", rf"\[ {tex(y - c)}w = {money(L * x)} - {money(y * L)} = {money(L * x - y * L)} \;\Rightarrow\; w = {tex(q)} \]")
    )
    formula = r"\[ L\left(\frac{x - y}{y - c}\right) \]" if c else r"\[ \text{Water} = L\left(\frac{x - y}{y}\right) \]"
    sub = (rf"\[ {tex(L)}\left(\frac{{{money(x)} - {money(y)}}}{{{money(y)} - {money(c)}}}\right) = {tex(L)}\times\frac{{{tex(x - y)}}}{{{tex(y - c)}}} = {tex(q)} \]" if c else
           rf"\[ {tex(L)}\left(\frac{{{money(x)} - {money(y)}}}{{{money(y)}}}\right) = {tex(L)}\times\frac{{{tex(x - y)}}}{{{money(y)}}} = {tex(q)} \]")
    rule = steps(("Identify the values.", rf"\(L = {tex(L)}\), \(x = {money(x)}\), \(y = {money(y)}\)" + (rf", \(c = {money(c)}\)." if c else ".")),
                 ("Apply the specified rule.", formula), ("Substitute the values.", sub))
    fin = rf"\({tex(q)}\)" + ("" if count else f" {unit}")
    rb = rbe([rf"\(L = {tex(L)}\), \(x = {money(x)}\), \(y = {money(y)}\)" + (rf", \(c = {money(c)}\)." if c else "."),
              rf"\(x - y = {tex(x - y)}\), " + (rf"\(y - c = {tex(y - c)}\)." if c else rf"\(y = {money(y)}\)."), rf"Quantity added \(= {tex(q)}\)."], fin)
    sc = shortcut(rf"\[ {tex(L)}\times\frac{{{tex(x - y)}}}{{{tex(y - c)}}} = {tex(q)} \]", fin)
    return result(("number", q), T24C if c else T24, trad, rule, fin, rb, sc)


PLAN24 = {1190: lambda: lower_price(50, "4.80", "3.20", "litres", "milk", "water"),
          1191: lambda: lower_price(18, "6.40", "4.80", "kilolitres", "milk", "water"),
          1192: lambda: lower_price(80, 8, "6.40", "litres", "milk", "water", price_note=r"\(1\frac{1}{2}\) litres for Rs \(12\) means Rs \(12\div 1\frac{1}{2} = 8\) per litre."),
          1193: lambda: lower_price(36, "16.80", "12.60", "litres", "spirit", "water"),
          1194: lambda: lower_price(24, 80, 50, "kg", "tea", "chicory", 30),
          1195: lambda: lower_price(300, "0.45", "0.40", "bananas", "bananas", "the cheaper bananas", "0.30",
                                   r"Price per banana: \(3.60\div 8 = 0.45\), \(1.50\div 5 = 0.30\), and Rs \(4.80\) a dozen \(= 0.40\).", count=True)}

# ---------------------------------------------------------------- Rule 25: percentage after mixing two liquids
T25 = (r"If one liquid contains \(x\%\) of A and another \(y\%\) of A, and \(n\) parts of the first are mixed with \(m\) parts of the second, then<br>"
       r"\[ \text{A in the mixture} = \frac{nx + my}{n + m}\,\% \]")


def blend_pct(x, y, n, m, what):
    x, y, n, m = R(x, y, n, m)
    p = (n * x + m * y) / (n + m)
    trad = steps(
        ("Take the parts as litres.", rf"\({tex(n)}\) litres of the first and \({tex(m)}\) litres of the second, \({tex(n + m)}\) litres in all."),
        (f"Find the {what} in each.", rf"\[ {tex(n)}\times\frac{{{pct(x)}}}{{100}} = {tex(n * x / 100)},\qquad {tex(m)}\times\frac{{{pct(y)}}}{{100}} = {tex(m * y / 100)} \]"),
        ("Find the percentage.", rf"\[ \frac{{{tex(n * x / 100)} + {tex(m * y / 100)}}}{{{tex(n + m)}}}\times 100 = {tex(p)}\% \]")
    )
    rule = steps(("Identify the values.", rf"\(x = {pct(x)}\), \(y = {pct(y)}\), \(n = {tex(n)}\), \(m = {tex(m)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{nx + my}{n + m} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(n)}\times{pct(x)} + {tex(m)}\times{pct(y)}}}{{{tex(n)} + {tex(m)}}} = \frac{{{tex(n * x + m * y)}}}{{{tex(n + m)}}} = {tex(p)}\% \]"))
    fin = rf"\({tex(p)}\%\)"
    rb = rbe([rf"\(x = {pct(x)}\), \(y = {pct(y)}\), \(n = {tex(n)}\), \(m = {tex(m)}\).", rf"\(nx + my = {tex(n * x + m * y)}\), \(n + m = {tex(n + m)}\).", rf"Percentage \(= {tex(p)}\%\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(n * x + m * y)}}}{{{tex(n + m)}}} = {tex(p)}\% \]", fin)
    return result(("number", p), T25, trad, rule, fin, rb, sc)


def blend_qty(x, n, y, target):
    """n litres at x%; how much of the y% solution makes target%?"""
    x, n, y, t = R(x, n, y, target)
    m = n * (x - t) / (t - y)
    trad = steps(
        ("Let \\(m\\) litres of the second solution be added.", rf"Sugar: \({tex(n)}\times\frac{{{pct(x)}}}{{100}} + m\times\frac{{{pct(y)}}}{{100}}\) in \(({tex(n)} + m)\) litres."),
        ("Set the strength.", rf"\[ {tex(n * x)} + {pct(y)}m = {pct(t)}({tex(n)} + m) \]"),
        ("Solve for \\(m\\).", rf"\[ {tex(n * x - n * t)} = {pct(t - y)}m \;\Rightarrow\; m = {tex(m)} \]")
    )
    rule = steps(("Identify the values.", rf"\(x = {pct(x)}\), \(n = {tex(n)}\), \(y = {pct(y)}\), result \({pct(t)}\%\); \(m\) is unknown."),
                 ("Apply the specified rule.", rf"\[ \frac{{nx + my}}{{n + m}} = {pct(t)} \]"),
                 ("Substitute and solve.", rf"\[ \frac{{{tex(n)}\times{pct(x)} + {pct(y)}m}}{{{tex(n)} + m}} = {pct(t)} \;\Rightarrow\; {tex(n * x)} + {pct(y)}m = {tex(n * t)} + {pct(t)}m \;\Rightarrow\; m = \frac{{{tex(n * x - n * t)}}}{{{pct(t - y)}}} = {tex(m)} \]"))
    fin = rf"\({tex(m)}\) litres"
    rb = rbe([rf"\(x = {pct(x)}\), \(n = {tex(n)}\), \(y = {pct(y)}\), target \({pct(t)}\%\).", rf"\({tex(n * x)} + {pct(y)}m = {pct(t)}({tex(n)} + m)\).", rf"\(m = {tex(m)}\) litres."], fin)
    sc = shortcut(rf"\[ m = {tex(n)}\times\frac{{{pct(x)} - {pct(t)}}}{{{pct(t)} - {pct(y)}}} = {tex(m)} \]", fin)
    return result(("number", m), T25, trad, rule, fin, rb, sc)


PLAN25 = {1196: lambda: blend_qty(20, 30, 8, 12), 1197: lambda: blend_pct(24, 36, 5, 3, "water"), 1198: lambda: blend_pct(12, 18, 5, 7, "milk"),
          1199: lambda: blend_pct(16, 24, 3, 5, "milk"), 1200: lambda: blend_pct(4, 10, 2, 4, "milk")}

# ---------------------------------------------------------------- Rule 26: second friend's weight increase
T26 = (r"If the weights of A and B are in the ratio \(a : b\), A's weight rises by \(x\%\) and the total rises by \(y\%\), then B's weight rises by<br>"
       r"\[ \frac{y(a + b) - ax}{b}\,\% \]")


def weights(a, b, x, total, y, A, B):
    a, b, x, total, y = R(a, b, x, total, y)
    inc = (y * (a + b) - a * x) / b
    old = total * 100 / (100 + y)
    wa, wb = old * a / (a + b), old * b / (a + b)
    na = wa * (100 + x) / 100
    nb = total - na
    assert (nb - wb) / wb * 100 == inc
    trad = steps(
        ("Find the old total.", rf"The total rose by \({pct(y)}\%\) to \({tex(total)}\) kg:<br>\[ \text{{Old total}} = {tex(total)}\times\frac{{100}}{{{tex(100 + y)}}} = {tex(old)} \]"),
        ("Split it in the ratio.", rf"\[ {A} = {tex(old)}\times\frac{{{tex(a)}}}{{{tex(a + b)}}} = {tex(wa)},\qquad {B} = {tex(wb)} \]"),
        (f"Find {B}'s new weight.", rf"\[ {A}\text{{ now}} = {tex(wa)}\times\frac{{{tex(100 + x)}}}{{100}} = {tex(na)},\qquad {B}\text{{ now}} = {tex(total)} - {tex(na)} = {tex(nb)} \]"),
        ("Find the increase.", rf"\[ \frac{{{tex(nb)} - {tex(wb)}}}{{{tex(wb)}}}\times 100 = {pct(inc)}\% \]")
    )
    rule = steps(("Identify the values.", rf"\(a : b = {tex(a)} : {tex(b)}\), \(x = {pct(x)}\), \(y = {pct(y)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{y(a + b) - ax}{b} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{pct(y)}\times{tex(a + b)} - {tex(a)}\times{pct(x)}}}{{{tex(b)}}} = \frac{{{tex(y * (a + b))} - {tex(a * x)}}}{{{tex(b)}}} = {pct(inc)}\% \]"))
    fin = rf"\({pct(inc)}\%\)"
    rb = rbe([rf"\(a : b = {tex(a)} : {tex(b)}\), \(x = {pct(x)}\), \(y = {pct(y)}\).", rf"\(y(a + b) - ax = {tex(y * (a + b) - a * x)}\).", rf"Increase \(= \frac{{{tex(y * (a + b) - a * x)}}}{{{tex(b)}}} = {pct(inc)}\%\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(y * (a + b))} - {tex(a * x)}}}{{{tex(b)}}} = {pct(inc)}\% \]", fin)
    return result(("number", inc), T26, trad, rule, fin, rb, sc)


PLAN26 = {1201: lambda: weights(3, 5, 10, 92, 15, "Naval", "Keval"), 1202: lambda: weights(2, 3, "5.5", 107, 7, "Pran", "Prem"),
          1203: lambda: weights(5, 2, 8, 84, 20, "Sudhir", "Sudhesh")}

# ---------------------------------------------------------------- Rule 27: amount released each time
T27 = (r"If \(R\) units of a mixture of \(M\) units are taken out and replaced by B only, and this is done \(n\) times, then<br>"
       r"\[ \frac{\text{A left}}{\text{A at first}} = \left(1 - \frac{R}{M}\right)^n \]")


def released(M, p0, p1, n=2):
    M, p0, p1 = R(M, p0, p1)
    k = {F(9, 16): F(3, 4), F(1, 4): F(1, 2), F(25, 49): F(5, 7), F(16, 25): F(4, 5)}[p1 / p0]
    Rl = M * (1 - k)
    o0 = M * p0 / 100
    trad = steps(
        ("Oxygen at the start.", rf"\[ {tex(M)}\times\frac{{{pct(p0)}}}{{100}} = {tex(o0)}\text{{ litres}} \]"),
        ("Each release keeps the same share.", rf"Taking out \(R\) litres of the \({tex(M)}\) and refilling with nitrogen keeps a share \(\frac{{{tex(M)} - R}}{{{tex(M)}}}\) of the oxygen. After two rounds:<br>"
         rf"\[ {tex(o0)}\left(\frac{{{tex(M)} - R}}{{{tex(M)}}}\right)^2 = {tex(M)}\times\frac{{{pct(p1)}}}{{100}} = {tex(M * p1 / 100)} \]"),
        ("Solve for \\(R\\).", rf"\[ \left(\frac{{{tex(M)} - R}}{{{tex(M)}}}\right)^2 = \frac{{{tex(M * p1 / 100)}}}{{{tex(o0)}}} = {ftex(k * k)} \;\Rightarrow\; \frac{{{tex(M)} - R}}{{{tex(M)}}} = {ftex(k)} \]"
         rf"\[ R = {tex(M)} - {tex(M * k)} = {tex(Rl)} \]")
    )
    rule = steps(("Identify the values.", rf"\(M = {tex(M)}\), \(n = 2\), oxygen goes from \({pct(p0)}\%\) to \({pct(p1)}\%\)."),
                 ("Apply the specified rule.", r"\[ \frac{\text{A left}}{\text{A at first}} = \left(1 - \frac{R}{M}\right)^n \]"),
                 ("Substitute the values.", rf"\[ \frac{{{pct(p1)}}}{{{pct(p0)}}} = \left(1 - \frac{{R}}{{{tex(M)}}}\right)^2 \;\Rightarrow\; 1 - \frac{{R}}{{{tex(M)}}} = {ftex(k)} \;\Rightarrow\; R = {tex(Rl)} \]"))
    fin = rf"\({tex(Rl)}\) litres"
    rb = rbe([rf"\(M = {tex(M)}\), \(n = 2\), ratio left \(= \frac{{{pct(p1)}}}{{{pct(p0)}}} = {ftex(k * k)}\).", rf"\(1 - \frac{{R}}{{M}} = {ftex(k)}\).", rf"\(R = {tex(Rl)}\) litres."], fin)
    sc = shortcut(rf"\[ \left(1 - \frac{{R}}{{{tex(M)}}}\right)^2 = {ftex(k * k)} \Rightarrow R = {tex(Rl)} \]", fin)
    return result(("number", Rl), T27, trad, rule, fin, rb, sc)


def lotion(a, b):
    a, b = R(a, b)
    s = a / (a + b)
    f = 1 - F(1, 2) / s
    trad = steps(
        ("Take one unit of mixture.", rf"It holds \({ftex(s)}\) lotion and \({ftex(1 - s)}\) water."),
        ("Take out \\(f\\) and add water.", rf"The lotion left is \({ftex(s)}(1 - f)\), and it must equal the water, i.e. half:<br>\[ {ftex(s)}(1 - f) = \frac{{1}}{{2}} \]"),
        ("Solve for \\(f\\).", rf"\[ 1 - f = {ftex(F(1, 2) / s)} \;\Rightarrow\; f = {ftex(f)} \]")
    )
    rule = steps(("Identify the values.", r"One operation, \(n = 1\); take \(M = 1\) unit."),
                 ("Apply the specified rule.", r"\[ \frac{\text{A left}}{\text{A at first}} = \left(1 - \frac{R}{M}\right)^n \]"),
                 ("Substitute the values.", rf"\[ \frac{{1/2}}{{{ftex(s)}}} = 1 - R \;\Rightarrow\; R = 1 - {ftex(F(1, 2) / s)} = {ftex(f)} \]"))
    fin = rf"\({ftex(f)}\) of the mixture"
    rb = rbe([rf"Lotion at first \(= {ftex(s)}\), lotion wanted \(= \frac{{1}}{{2}}\), \(n = 1\).", rf"\(1 - R = {ftex(F(1, 2) / s)}\).", rf"\(R = {ftex(f)}\)."], fin)
    sc = shortcut(rf"\[ 1 - \frac{{1/2}}{{{ftex(s)}}} = {ftex(f)} \]", fin)
    return result(("number", f), T27, trad, rule, fin, rb, sc)


PLAN27 = {1204: lambda: released(20, 16, 9), 1205: lambda: lotion(3, 1), 1206: lambda: released(18, 36, 9),
          1207: lambda: released(35, 49, 25), 1208: lambda: released(75, 25, 16)}

# ---------------------------------------------------------------- Rule 28: liquid left after repeated replacement
T28 = (r"If a container holds \(x\) units of a liquid and \(y\) units are taken out and replaced by water each time, then after \(n\) operations<br>"
       r"\[ \text{Liquid left} = x\left(1 - \frac{y}{x}\right)^n \]")


def left_after(x, y, n, ask, liquid, unit="litres"):
    """x = 1 when only a fraction y is given. ask: 'amount', 'removed', 'left_ratio' (left : original), 'lw' (liquid : water)."""
    x, y = R(x, y)
    k = 1 - y / x
    amounts = [x]
    for _ in range(n):
        amounts.append(amounts[-1] - amounts[-1] * y / x)
    left = amounts[-1]
    assert left == x * k ** n
    whole = x != 1
    rows = "".join(rf"<tr><td>{i}</td><td>\({tex(amounts[i - 1])} - {tex(amounts[i - 1])}\times{ftex(y / x)} = {tex(amounts[i]) if whole else ftex(amounts[i])}\)</td></tr>" for i in range(1, n + 1))
    trad = steps(
        ("Follow the liquid one draw at a time.", rf"Each draw removes \({ftex(y / x)}\) of whatever {liquid} is in the container; water then fills it up again."
         + (rf" Take the container to hold \(1\) unit." if not whole else "")),
        ("Make a table.", f'<table border="1" cellpadding="4"><tr><th>Draw</th><th>{liquid.capitalize()} left</th></tr>{rows}</table>'),
        ("Read off the result.", rf"After {n} draws, {liquid} left \(= {tex(left) if whole else ftex(left)}\)" + (f" {unit}." if whole else " of the original."))
    )
    rule = steps(("Identify the values.", (rf"\(x = {tex(x)}\), \(y = {tex(y)}\), " if whole else rf"Fraction taken out each time \(= {ftex(y)}\), ") + rf"\(n = {n}\)."),
                 ("Apply the specified rule.", T28.split("<br>")[1] if whole else r"\[ \frac{\text{Liquid left}}{\text{Original}} = \left(1 - \frac{y}{x}\right)^n \]"),
                 ("Substitute the values.", rf"\[ {tex(x) if whole else ''}\left(1 - {ftex(y / x)}\right)^{{{n}}} = {tex(x) if whole else ''}{TIMES if whole else ''}\left({ftex(k)}\right)^{{{n}}} = {tex(left) if whole else ftex(left)} \]"))
    if ask == "amount":
        fin, answer = rf"\({tex(left)}\) {unit}", ("number", left)
    elif ask == "removed":
        rm = 1 - left
        rule += rf"<br>Removed \(= 1 - {ftex(left)} = {ftex(rm)}\)."
        fin, answer = rf"\({ftex(rm)}\)", ("number", rm)
    elif ask == "left_ratio":
        r = ratio(left, 1)
        fin, answer = rf"\({rtex(r)}\)", ("ratio", r)
    else:
        r = ratio(left, x - left)
        rule += rf"<br>Water \(= {tex(x) if whole else '1'} - {tex(left) if whole else ftex(left)} = {tex(x - left) if whole else ftex(x - left)}\), so {liquid} : water \(= {rtex(r)}\)."
        fin, answer = rf"\({rtex(r)}\)", ("ratio", r)
    rb = rbe([rf"Fraction kept each time \(= 1 - {ftex(y / x)} = {ftex(k)}\), \(n = {n}\).", rf"Left \(= {tex(x) + TIMES if whole else ''}\left({ftex(k)}\right)^{{{n}}} = {tex(left) if whole else ftex(left)}\).",
              "Answer: " + fin + "."], fin)
    sc = shortcut(rf"\[ {tex(x) + TIMES if whole else ''}\left({ftex(k)}\right)^{{{n}}} = {tex(left) if whole else ftex(left)} \]", fin)
    return result(answer, T28, trad, rule, fin, rb, sc)


PLAN28 = {1209: lambda: left_after(64, 16, 3, "amount", "wine"), 1210: lambda: left_after(1, F(1, 4), 5, "removed", "alcohol"),
          1211: lambda: left_after(1, F(1, 20), 3, "left_ratio", "spirit"), 1212: lambda: left_after(32, 8, 3, "lw", "wine"),
          1213: lambda: left_after(243, 81, 3, "amount", "wine"), 1214: lambda: left_after(125, 25, 3, "lw", "wine"),
          1215: lambda: left_after(36, 6, 2, "lw", "milk")}

PLANS = {19: PLAN19, 20: PLAN20, 21: PLAN21, 22: PLAN22, 23: PLAN23, 24: PLAN24, 25: PLAN25, 26: PLAN26, 27: PLAN27, 28: PLAN28}

# Missing book worked examples, rewritten with new numbers.
NEW = {
    20: [("N1", "A dairy owner mixes \\(4\\) kilolitres of milk costing Rs \\(900\\) per kilolitre with \\(8\\) kilolitres costing Rs \\(750\\) per kilolitre, and adds enough water to bring the average value down to Rs \\(600\\) per kilolitre. How many kilolitres of water does he add?",
          ["3 kilolitres", "4 kilolitres", "5 kilolitres", "6 kilolitres"], 2, lambda: water_avg(4, 900, 8, 750, 600))],
    23: [("N1", "A jug holds \\(9\\) parts milk and \\(3\\) parts water. What part of the mixture must be poured out and replaced with water so that the jug holds equal amounts of milk and water?",
          ["\\(\\frac{1}{4}\\)", "\\(\\frac{1}{3}\\)", "\\(\\frac{1}{6}\\)", "\\(\\frac{2}{5}\\)"], 2, lambda: half_half(9, 3, "milk", "water"))],
    25: [("N1", "One liquid contains \\(20\\%\\) milk and another contains \\(30\\%\\) milk. A can is filled with \\(7\\) parts of the first and \\(3\\) parts of the second. What percentage of the new mixture is milk?",
          ["\\(21\\%\\)", "\\(22\\%\\)", "\\(23\\%\\)", "\\(24\\%\\)"], 3, lambda: blend_pct(20, 30, 7, 3, "milk"))],
    26: [("N1", "The weights of Anil and Sunil are in the ratio \\(2:3\\). Anil's weight goes up by \\(12\\%\\), and their combined weight becomes \\(115\\) kg, a rise of \\(15\\%\\). By what percentage did Sunil's weight go up?",
          ["\\(14\\%\\)", "\\(15\\%\\)", "\\(16\\%\\)", "\\(17\\%\\)"], 4, lambda: weights(2, 3, 12, 115, 15, "Anil", "Sunil"))],
    28: [("N1", "A tank holds \\(50\\) litres of milk. \\(5\\) litres are taken out and replaced with water, and this is done three times in all. How much milk is left in the tank?",
          ["35 litres", "36.45 litres", "37.50 litres", "40.50 litres"], 2, lambda: left_after(50, 5, 3, "amount", "milk")),
         ("N2", "A bottle is full of dettol. One-third of it is poured out and the bottle is topped up with water. This is done three times in all. What is the final ratio of dettol to water in the bottle?",
          ["\\(19:8\\)", "\\(8:27\\)", "\\(8:19\\)", "\\(1:2\\)"], 3, lambda: left_after(1, F(1, 3), 3, "lw", "dettol"))],
}


def as_json_answer(ans):
    return [ans[0], [str(v) for v in ans[1]] if isinstance(ans[1], tuple) else str(ans[1])]


if __name__ == "__main__":
    for n in map(int, sys.argv[1:] or PLANS):
        folder = os.path.join(HERE, f"rule{n:02d}")
        cur = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        card = cur["rule_card"]
        assert sorted(PLANS[n]) == sorted(r["id"] for r in cur["rows"])
        out = [regen_entry(row, PLANS[n][row["id"]](), card["id"]) for row in cur["rows"]]
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        extra = ""
        if n in NEW:
            qs, answers = [], []
            for key, text, opts, pos, fn in NEW[n]:
                g = fn()
                qs.append(new_question(n, text, opts, pos, g["solution"], g["rbe"], g["shortcut"]))
                answers.append([key, as_json_answer(g["answer"])])
            payload = {"rules_html": [{"chapter": "alligation_n_mixture", "rule_name": f"Rule {n}", "rule_html": card["rule_html"]}], "questions": qs}
            json.dump(payload, open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2)
            extra = f" + {len(qs)} new question(s)"
        print(f"Rule {n}: generated {len(out)} rows{extra}")
