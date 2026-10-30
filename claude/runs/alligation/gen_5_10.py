"""Rules 5-10: regenerates every row (book worked example + reworded exercises) in the prompt #10 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer) and links the worked examples
to their rule card. Writes ruleNN/2_new_rows.json for each rule."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import frac, money, pct, ratio, ratio_steps, rbe, regen_entry, rtex, shortcut, solution, steps, tex  # noqa: E402

R = lambda *v: tuple(F(x) for x in v)


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rb, shortcut=sc)


# ---------------------------------------------------------------- Rule 5: add a pure component
T5 = (r"If \(n\) units of a mixture contain \(x\%\) of a substance, the amount of that pure substance which must be added "
      r"to raise its share to \(y\%\) is<br>\[ \text{Quantity added} = n\times\frac{y-x}{100-y} \]")
F5 = r"\[ \text{Quantity added} = n\times\frac{y-x}{100-y} \]"


def add_pure(n, x, y, unit, added, other, convert="", scale=1, out_unit=None):
    n, x, y = R(n, x, y)
    a = n * (y - x) / (100 - y)
    keep = n * (100 - x) / 100
    out_unit = out_unit or unit
    tail = rf"\[ {tex(a)}\text{{ {unit}}} = {tex(a * scale)}\text{{ {out_unit}}} \]" if scale != 1 else ""
    trad = steps(
        (f"Find the {other}, which does not change.", (convert + "<br>" if convert else "") +
         rf"The {other} is \(100 - {pct(x)} = {pct(100 - x)}\%\) of the mixture:<br>\[ {tex(n)}\times\frac{{{pct(100 - x)}}}{{100}} = {tex(keep)}\text{{ {unit}}} \]"),
        ("Write the new mixture in terms of it.", rf"After adding \(a\) {unit} of {added}, the {other} must be \({pct(100 - y)}\%\) of \(({tex(n)} + a)\):<br>"
         rf"\[ ({tex(n)} + a)\times\frac{{{pct(100 - y)}}}{{100}} = {tex(keep)} \]"),
        ("Solve for \\(a\\).", rf"\[ {tex(n)} + a = {tex(keep)}\times\frac{{100}}{{{pct(100 - y)}}} = {tex(n + a)} \]\[ a = {tex(n + a)} - {tex(n)} = {tex(a)} \]" + tail)
    )
    rule = steps(
        ("Identify the values.", (convert + "<br>" if convert else "") + rf"\(n = {tex(n)}\), \(x = {pct(x)}\), \(y = {pct(y)}\) (percentages of {added})."),
        ("Apply the specified rule.", F5),
        ("Substitute the values.", rf"\[ {tex(n)}\times\frac{{{pct(y)} - {pct(x)}}}{{100 - {pct(y)}}} = {tex(n)}\times\frac{{{pct(y - x)}}}{{{pct(100 - y)}}} = {tex(a)}\text{{ {unit}}} \]" + tail)
    )
    fin = rf"\({tex(a * scale)}\) {out_unit}"
    rb = rbe([rf"\(n = {tex(n)}\), \(x = {pct(x)}\), \(y = {pct(y)}\).", rf"\(y - x = {pct(y - x)}\), \(100 - y = {pct(100 - y)}\).",
              rf"Quantity added \(= {tex(n)}\times\frac{{{pct(y - x)}}}{{{pct(100 - y)}}} = {tex(a)}\) {unit}" + (rf" \(= {tex(a * scale)}\) {out_unit}." if scale != 1 else ".")], fin)
    sc = shortcut(rf"\[ {tex(n)}\times\frac{{{pct(y)} - {pct(x)}}}{{100 - {pct(y)}}} = {tex(a)} \]", fin)
    return result(("number", a * scale), T5, trad, rule, fin, rb, sc)


def alcohol_after_water(n, alc, w):
    n, alc, w = R(n, alc, w)
    amount = n * alc / 100
    new = amount / (n + w) * 100
    x = 100 - alc
    trad = steps(
        ("Find the alcohol, which does not change.", rf"\[ {tex(n)}\times\frac{{{pct(alc)}}}{{100}} = {tex(amount)}\text{{ litres of alcohol}} \]"),
        ("Find the new total.", rf"\[ {tex(n)} + {tex(w)} = {tex(n + w)}\text{{ litres}} \]"),
        ("Find the new percentage.", rf"\[ \frac{{{tex(amount)}}}{{{tex(n + w)}}}\times 100 = {pct(new)}\% \]")
    )
    rule = steps(
        ("Identify the values.", rf"Water is the substance being added: \(n = {tex(n)}\), water now \(x = 100 - {pct(alc)} = {pct(x)}\%\), water added \(= {tex(w)}\) litres, new water share \(y\%\) unknown."),
        ("Apply the specified rule.", F5 + rf"\[ {tex(w)} = {tex(n)}\times\frac{{y - {pct(x)}}}{{100 - y}} \]"),
        ("Solve for \\(y\\).", rf"\[ {tex(w)}(100 - y) = {tex(n)}(y - {pct(x)}) \]\[ {tex(100 * w + n * x)} = {tex(n + w)}y \;\Rightarrow\; y = {pct(100 - new)} \]"
         rf"So water is \({pct(100 - new)}\%\) and alcohol is \(100 - {pct(100 - new)} = {pct(new)}\%\).")
    )
    fin = rf"\({pct(new)}\%\)"
    rb = rbe([rf"Water now \(x = {pct(x)}\%\), water added \(= {tex(w)}\) litres to \(n = {tex(n)}\) litres.",
              rf"\({tex(w)}(100 - y) = {tex(n)}(y - {pct(x)})\) gives \(y = {pct(100 - new)}\).", rf"Alcohol \(= 100 - {pct(100 - new)} = {pct(new)}\%\)."], fin)
    sc = shortcut(rf"\[ \text{{Alcohol}} = \frac{{{tex(n)}\times{pct(alc)}}}{{{tex(n + w)}}} = {pct(new)}\% \]", fin)
    return result(("number", new), T5, trad, rule, fin, rb, sc)


def water_for_ratio(n, a, b, c, d, unit):
    n = F(n)
    milk = n * a / (a + b)
    water = n - milk
    new_water = milk * d / c
    add = new_water - water
    x, y = F(100 * b, a + b), F(100 * d, c + d)
    assert add == n * (y - x) / (100 - y)
    trad = steps(
        ("Split the mixture.", rf"Milk \(= {tex(n)}\times\frac{{{a}}}{{{a + b}}} = {tex(milk)}\) {unit}, water \(= {tex(n)} - {tex(milk)} = {tex(water)}\) {unit}."),
        ("Keep the milk and find the water needed.", rf"For milk : water \(= {c} : {d}\):<br>\[ \text{{Water}} = {tex(milk)}\times\frac{{{d}}}{{{c}}} = {tex(new_water)}\text{{ {unit}}} \]"),
        ("Find the water to add.", rf"\[ {tex(new_water)} - {tex(water)} = {tex(add)}\text{{ {unit}}} \]")
    )
    rule = steps(
        ("Turn the ratios into percentages of water.", rf"\[ x = \frac{{{b}}}{{{a + b}}}\times 100 = {pct(x)}\%,\qquad y = \frac{{{d}}}{{{c + d}}}\times 100 = {pct(y)}\% \]"),
        ("Apply the specified rule.", F5),
        ("Substitute the values.", rf"\[ {tex(n)}\times\frac{{{pct(y)} - {pct(x)}}}{{100 - {pct(y)}}} = {tex(n)}\times\frac{{{pct(y - x)}}}{{{pct(100 - y)}}} = {tex(add)}\text{{ {unit}}} \]")
    )
    fin = rf"\({tex(add)}\) {unit}"
    rb = rbe([rf"Water now \(x = {pct(x)}\%\), wanted \(y = {pct(y)}\%\), \(n = {tex(n)}\).", rf"\(y - x = {pct(y - x)}\), \(100 - y = {pct(100 - y)}\).",
              rf"Water added \(= {tex(n)}\times\frac{{{pct(y - x)}}}{{{pct(100 - y)}}} = {tex(add)}\) {unit}."], fin)
    sc = shortcut(rf"\[ {tex(n)}\times\frac{{{pct(y)} - {pct(x)}}}{{100 - {pct(y)}}} = {tex(add)} \]", fin)
    return result(("number", add), T5, trad, rule, fin, rb, sc)


LEADED = r"Leaded petrol is the part being added. It is now \(100 - {u1} = {l1}\%\) of the mixture and must become \(100 - {u2} = {l2}\%\)."
BARLEY = r"Barley is the part being added. It is now \(100 - 70 = 30\%\) of the mixture and must become \(100 - 60 = 40\%\)."
PLAN5 = {
    839: lambda: add_pure(300, 40, 50, "gm", "sugar", "rest of the solution"),
    1104: lambda: add_pure(450, 35, 55, "gm", "sugar", "rest of the solution"),
    1105: lambda: add_pure(60, 15, 25, "litres", "water", "milk"),
    1106: lambda: add_pure("1.5", 85, 95, "litres", "leaded petrol", "unleaded petrol", LEADED.format(u1=15, l1=85, u2=5, l2=95), 1000, "ml"),
    1107: lambda: add_pure(240, 30, 40, "gm", "sugar", "rest of the solution"),
    1108: lambda: add_pure(3, 75, 90, "litres", "leaded petrol", "unleaded petrol", LEADED.format(u1=25, l1=75, u2=10, l2=90), 1000, "ml"),
    1109: lambda: add_pure(60, 20, 40, "litres", "water", "milk"),
    1110: lambda: add_pure(600, 30, 40, "quintals", "barley", "wheat", BARLEY),
    1111: lambda: add_pure(80, 75, 90, "gm", "gold", "silver"),
    1112: lambda: alcohol_after_water(20, 25, 5),
    1113: lambda: water_for_ratio(450, 7, 2, 7, 3, "ml"),
    1114: lambda: water_for_ratio(90, 2, 1, 1, 2, "litres"),
    1115: lambda: water_for_ratio(72, 5, 1, 5, 3, "litres"),
}

# ---------------------------------------------------------------- Rule 6: money shared by boys and girls
T6 = (r"If \(N\) students share \(X\) so that each boy gets \(x\) and each girl gets \(y\) (all in the same unit), then<br>"
      r"\[ \text{Boys} = \frac{X - Ny}{x - y},\qquad \text{Girls} = \frac{Nx - X}{x - y} \]")
F6 = r"\[ \text{Boys} = \frac{X - Ny}{x - y},\qquad \text{Girls} = \frac{Nx - X}{x - y} \]"


def students(N, X, x, y, ask, money_text):
    """All money in paise. ask: 'bg' (boys, girls), 'gb' (girls, boys) or 'ratio' (boys : girls)."""
    N, X, x, y = R(N, X, x, y)
    boys = (X - N * y) / (x - y)
    girls = N - boys
    r = ratio(boys, girls)
    trad = steps(
        ("Use paise throughout.", money_text),
        ("Let the unknowns be the boys and girls.", rf"Let there be \(b\) boys and \(g\) girls:<br>\[ b + g = {tex(N)} \]\[ {tex(x)}b + {tex(y)}g = {tex(X)} \]"),
        ("Substitute \\(g = " + tex(N) + " - b\\).", rf"\[ {tex(x)}b + {tex(y)}({tex(N)} - b) = {tex(X)} \]\[ {tex(x - y)}b = {tex(X)} - {tex(N * y)} = {tex(X - N * y)} \]"),
        ("Find both numbers.", rf"\[ b = \frac{{{tex(X - N * y)}}}{{{tex(x - y)}}} = {tex(boys)},\qquad g = {tex(N)} - {tex(boys)} = {tex(girls)} \]")
    )
    rule = steps(
        ("Identify the values.", rf"\(N = {tex(N)}\), \(X = {tex(X)}\) paise, \(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", F6),
        ("Substitute the values.", rf"\[ \text{{Boys}} = \frac{{{tex(X)} - {tex(N)}\times{tex(y)}}}{{{tex(x)} - {tex(y)}}} = \frac{{{tex(X - N * y)}}}{{{tex(x - y)}}} = {tex(boys)} \]"
         rf"\[ \text{{Girls}} = \frac{{{tex(N)}\times{tex(x)} - {tex(X)}}}{{{tex(x)} - {tex(y)}}} = \frac{{{tex(N * x - X)}}}{{{tex(x - y)}}} = {tex(girls)} \]")
    )
    if ask == "ratio":
        rule += rf"<br>Boys : girls \(= {tex(boys)} : {tex(girls)} = {rtex(r)}\)."
        fin, answer = rf"\({rtex(r)}\)", ("ratio", r)
    elif ask == "gb":
        fin, answer = rf"\({tex(girls)}\) girls and \({tex(boys)}\) boys", ("pair", (girls, boys))
    else:
        fin, answer = rf"\({tex(boys)}\) boys and \({tex(girls)}\) girls", ("pair", (boys, girls))
    rb = rbe([rf"\(N = {tex(N)}\), \(X = {tex(X)}\), \(x = {tex(x)}\), \(y = {tex(y)}\) (paise).",
              rf"Boys \(= \frac{{{tex(X - N * y)}}}{{{tex(x - y)}}} = {tex(boys)}\).", rf"Girls \(= \frac{{{tex(N * x - X)}}}{{{tex(x - y)}}} = {tex(girls)}\)."], fin)
    sc = shortcut(rf"\[ \text{{Boys}} = \frac{{{tex(X - N * y)}}}{{{tex(x - y)}}} = {tex(boys)},\quad \text{{Girls}} = {tex(girls)} \]", fin)
    return result(answer, T6, trad, rule, fin, rb, sc)


PLAN6 = {
    840: lambda: students(65, 3900, 80, 30, "bg", r"Rs \(39 = 3900\) paise; each boy gets \(80\) paise and each girl \(30\) paise."),
    1116: lambda: students(85, 5100, 80, 30, "bg", r"Rs \(51 = 5100\) paise; each boy gets \(80\) paise and each girl \(30\) paise."),
    1117: lambda: students(80, 16000, 250, 50, "ratio", r"Rs \(160 = 16000\) paise; each boy gets Rs \(2.50 = 250\) paise and each girl \(50\) paise."),
    1118: lambda: students(100, 6400, 100, 40, "bg", r"Rs \(64 = 6400\) paise; each boy gets Re \(1 = 100\) paise and each girl \(40\) paise."),
    1119: lambda: students(60, 4200, 100, 50, "gb", r"Rs \(42 = 4200\) paise; each boy gets Re \(1 = 100\) paise and each girl \(50\) paise."),
}

# ---------------------------------------------------------------- Rule 7: water in a liquid sold at a profit
T7 = (r"If a liquid costing \(x\) per litre is mixed with water and the mixture is sold at \(y\) per litre to gain \(P\%\), then<br>"
      r"\[ \text{Liquid} : \text{Water} = y : \left[(x-y) + \frac{P}{100}\,x\right] \]")
F7 = r"\[ \text{Liquid} : \text{Water} = y : \left[(x-y) + \frac{P}{100}\,x\right] \]"


def liquid(x, y, P, name, ask, unit_text, cur="Rs"):
    """ask: 'lw' liquid : water, 'wl' water : liquid, 'per_litre' water in each litre of mixture."""
    x, y, P = R(x, y, P)
    z = y * 100 / (100 + P)
    lw = ratio(z, x - z)
    second = x - y + P * x / 100
    assert ratio(y, second) == lw
    c = (lambda v: rf"\({money(v)}\) paise") if cur == "paise" else (lambda v: rf"Rs \({money(v)}\)")
    trad = steps(
        ("Find the cost price of the mixture.", (unit_text + "<br>" if unit_text else "") +
         rf"Selling price {c(y)} per litre with a gain of \({pct(P)}\%\):<br>\[ \text{{CP}} = {money(y)}\times\frac{{100}}{{100 + {pct(P)}}} = {money(z)} \]"),
        ("Set up the cost equation.", rf"Let \(a\) litres of {name} (at {c(x)}) be mixed with \(b\) litres of water (free):<br>\[ {money(x)}a + 0\cdot b = {money(z)}(a + b) \]"),
        ("Find the ratio.", rf"\[ {tex(x - z)}a = {money(z)}b \;\Rightarrow\; \frac{{a}}{{b}} = {ratio_steps(z, x - z)} \]So {name} : water \(= {rtex(lw)}\).")
    )
    rule = steps(
        ("Identify the values.", rf"\(x = {money(x)}\), \(y = {money(y)}\), \(P = {pct(P)}\)."),
        ("Apply the specified rule.", F7),
        ("Substitute the values.", rf"\[ {money(y)} : \left[({money(x)} - {money(y)}) + \frac{{{pct(P)}}}{{100}}\times{money(x)}\right] = {money(y)} : \left[{tex(x - y)} + {tex(P * x / 100)}\right] = {money(y)} : {tex(second)} = {rtex(lw)} \]")
    )
    if ask == "wl":
        r = (lw[1], lw[0])
        rule += rf"<br>So water : {name} \(= {rtex(r)}\)."
        fin, answer, rb_last = rf"\({rtex(r)}\)", ("ratio", r), rf"Water : {name} \(= {rtex(r)}\)."
    elif ask == "per_litre":
        w = F(lw[1], lw[0] + lw[1])
        rule += rf"<br>Water in each litre of mixture \(= \frac{{{lw[1]}}}{{{lw[0]} + {lw[1]}}} = {frac(w)}\) litre."
        fin, answer, rb_last = rf"\({frac(w)}\) litre", ("number", w), rf"Water per litre \(= \frac{{{lw[1]}}}{{{lw[0] + lw[1]}}} = {frac(w)}\) litre."
    else:
        r = lw
        fin, answer, rb_last = rf"\({rtex(r)}\)", ("ratio", r), rf"{name.capitalize()} : water \(= {rtex(r)}\)."
    rb = rbe([rf"\(x = {money(x)}\), \(y = {money(y)}\), \(P = {pct(P)}\).", rf"\((x - y) + \frac{{P}}{{100}}x = {tex(second)}\), so ratio \(= {money(y)} : {tex(second)} = {rtex(lw)}\).", rb_last], fin)
    sc = shortcut(rf"\[ {money(y)} : \left[{tex(x - y)} + {tex(P * x / 100)}\right] = {rtex(lw)} \]", fin)
    return result(answer, T7, trad, rule, fin, rb, sc)


PLAN7 = {
    841: lambda: liquid(25, 20, 25, "chemical", "lw", ""),
    1120: lambda: liquid(6, "7.20", F(100, 3), "milk", "lw", ""),
    1121: lambda: liquid(9, 6, 20, "milk", "per_litre", ""),
    1122: lambda: liquid(60, 70, 40, "milk", "wl", r"Rs \(600\) per kilolitre \(= \frac{60000}{1000} = 60\) paise per litre.", "paise"),
    1123: lambda: liquid(90, 75, 50, "chemical", "lw", ""),
}

# ---------------------------------------------------------------- Rule 8: two-stage journey
T8 = (r"If \(D\) km are covered in \(T\) hours, partly by bus at \(x\) km/hr and the rest by train at \(y\) km/hr, then<br>"
      r"\[ \text{Bus distance} = \frac{yT - D}{y - x}\times x,\qquad \text{Train distance} = \frac{D - xT}{y - x}\times y \]")
F8 = r"\[ \text{Bus distance} = \frac{yT - D}{y - x}\times x,\qquad \text{Train distance} = \frac{D - xT}{y - x}\times y \]"


def journey(D, T, x, y, ask):
    """ask: 'bus', 'train', 'ratio' (bus : train) or 'both' (bus, train)."""
    D, T, x, y = R(D, T, x, y)
    t = (y * T - D) / (y - x)
    bus, train = x * t, D - x * t
    assert train == (D - x * T) / (y - x) * y
    trad = steps(
        ("Let the time by bus be \\(t\\) hours.", rf"Then the time by train is \(({tex(T)} - t)\) hours."),
        ("Use the total distance.", rf"\[ {tex(x)}t + {tex(y)}({tex(T)} - t) = {tex(D)} \]\[ {tex(y * T)} - {tex(y - x)}t = {tex(D)} \;\Rightarrow\; t = \frac{{{tex(y * T - D)}}}{{{tex(y - x)}}} = {tex(t)} \]"),
        ("Find the distances.", rf"\[ \text{{Bus}} = {tex(x)}\times{tex(t)} = {tex(bus)}\text{{ km}},\qquad \text{{Train}} = {tex(D)} - {tex(bus)} = {tex(train)}\text{{ km}} \]")
    )
    bus_line = rf"\[ \text{{Bus}} = \frac{{{tex(y)}\times{tex(T)} - {tex(D)}}}{{{tex(y)} - {tex(x)}}}\times{tex(x)} = \frac{{{tex(y * T - D)}}}{{{tex(y - x)}}}\times{tex(x)} = {tex(bus)}\text{{ km}} \]"
    train_line = rf"\[ \text{{Train}} = \frac{{{tex(D)} - {tex(x)}\times{tex(T)}}}{{{tex(y)} - {tex(x)}}}\times{tex(y)} = \frac{{{tex(D - x * T)}}}{{{tex(y - x)}}}\times{tex(y)} = {tex(train)}\text{{ km}} \]"
    lines = {"bus": bus_line, "train": train_line}.get(ask, bus_line + train_line)
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(T = {tex(T)}\), \(x = {tex(x)}\) (bus), \(y = {tex(y)}\) (train)."),
                 ("Apply the specified rule.", F8), ("Substitute the values.", lines))
    if ask == "bus":
        fin, answer = rf"\({tex(bus)}\) km", ("number", bus)
    elif ask == "train":
        fin, answer = rf"\({tex(train)}\) km", ("number", train)
    elif ask == "ratio":
        r = ratio(bus, train)
        rule += rf"<br>Bus : train \(= {tex(bus)} : {tex(train)} = {rtex(r)}\)."
        fin, answer = rf"\({rtex(r)}\)", ("ratio", r)
    else:
        fin, answer = rf"\({tex(bus)}\) km by bus and \({tex(train)}\) km by train", ("pair", (bus, train))
    rb = rbe([rf"\(D = {tex(D)}\), \(T = {tex(T)}\), \(x = {tex(x)}\), \(y = {tex(y)}\).",
              rf"Bus \(= \frac{{{tex(y * T - D)}}}{{{tex(y - x)}}}\times{tex(x)} = {tex(bus)}\) km.",
              rf"Train \(= \frac{{{tex(D - x * T)}}}{{{tex(y - x)}}}\times{tex(y)} = {tex(train)}\) km."], fin)
    sc = shortcut(rf"\[ \text{{Bus}} = {tex(bus)},\quad \text{{Train}} = {tex(train)} \]", fin)
    return result(answer, T8, trad, rule, fin, rb, sc)


PLAN8 = {842: lambda: journey(285, 6, 40, 55, "train"), 1125: lambda: journey(260, 6, 40, 60, "bus"),
         1126: lambda: journey(270, 7, 30, 50, "train"), 1127: lambda: journey(330, 6, 40, 70, "ratio"),
         1128: lambda: journey(205, 4, 40, 75, "both")}

# ---------------------------------------------------------------- Rule 9: two profit rates
T9 = (r"If \(N\) kg are sold partly at \(x\%\) profit and the rest at \(y\%\) profit, and the overall profit is \(P\%\), then<br>"
      r"\[ \text{Sold at } x\% = \frac{y-P}{y-x}\times N,\qquad \text{Sold at } y\% = \frac{P-x}{y-x}\times N \]")


def two_profits(N, x, y, P, item):
    N, x, y, P = R(N, x, y, P)
    q = (P - x) / (y - x) * N
    trad = steps(
        ("Take a convenient cost.", rf"Let the {item} cost Rs \(1\) per kg, so the whole lot costs Rs \({tex(N)}\)."),
        ("Let the unknown be the part sold at the higher profit.", rf"Let \(q\) kg be sold at \({pct(y)}\%\) and \(({tex(N)} - q)\) kg at \({pct(x)}\%\). The profits must add up:<br>"
         rf"\[ \frac{{{pct(x)}}}{{100}}({tex(N)} - q) + \frac{{{pct(y)}}}{{100}}q = \frac{{{pct(P)}}}{{100}}\times{tex(N)} \]"),
        ("Clear the 100s and solve.", rf"\[ {tex(x * N)} - {pct(x)}q + {pct(y)}q = {tex(P * N)} \]\[ {pct(y - x)}q = {tex(P * N - x * N)} \;\Rightarrow\; q = {tex(q)} \]")
    )
    rule = steps(("Identify the values.", rf"\(N = {tex(N)}\), \(x = {pct(x)}\), \(y = {pct(y)}\), \(P = {pct(P)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Sold at } y\% = \frac{P-x}{y-x}\times N \]"),
                 ("Substitute the values.", rf"\[ \frac{{{pct(P)} - {pct(x)}}}{{{pct(y)} - {pct(x)}}}\times{tex(N)} = \frac{{{pct(P - x)}}}{{{pct(y - x)}}}\times{tex(N)} = {tex(q)}\text{{ kg}} \]"))
    fin = rf"\({tex(q)}\) kg"
    rb = rbe([rf"\(N = {tex(N)}\), \(x = {pct(x)}\), \(y = {pct(y)}\), \(P = {pct(P)}\).", rf"\(P - x = {pct(P - x)}\), \(y - x = {pct(y - x)}\).",
              rf"Sold at \({pct(y)}\%\) \(= \frac{{{pct(P - x)}}}{{{pct(y - x)}}}\times{tex(N)} = {tex(q)}\) kg."], fin)
    sc = shortcut(rf"\[ \frac{{{pct(P)} - {pct(x)}}}{{{pct(y)} - {pct(x)}}}\times{tex(N)} = {tex(q)} \]", fin)
    return result(("number", q), T9, trad, rule, fin, rb, sc)


PLAN9 = {843: lambda: two_profits(50, 8, 18, 14, "pulses"), 1129: lambda: two_profits(60, 10, 22, 16, "pulses"),
         1130: lambda: two_profits(30, 6, 10, 8, "rice"), 1131: lambda: two_profits(90, 14, 34, 26, "wheat"),
         1132: lambda: two_profits(45, 10, 25, 16, "pulses")}

# ---------------------------------------------------------------- Rule 10: profit on one part, loss on the other
T10 = (r"If \(N\) kg are sold partly at \(x\%\) profit and the rest at \(y\%\) loss, and the overall profit is \(P\%\), then<br>"
       r"\[ \text{At } x\%\text{ profit} = \frac{P+y}{x+y}\times N,\qquad \text{At } y\%\text{ loss} = \frac{x-P}{x+y}\times N \]")
F10 = r"\[ \text{At } x\%\text{ profit} = \frac{P+y}{x+y}\times N,\qquad \text{At } y\%\text{ loss} = \frac{x-P}{x+y}\times N \]"


def profit_loss(N, x, y, P, item):
    N, x, y, P = R(N, x, y, P)
    q = (P + y) / (x + y) * N
    rest = N - q
    trad = steps(
        ("Take a convenient cost.", rf"Let the {item} cost Rs \(1\) per kg, so the whole lot costs Rs \({tex(N)}\)."),
        ("Let the unknown be the part sold at a profit.", rf"Let \(q\) kg be sold at \({pct(x)}\%\) profit and \(({tex(N)} - q)\) kg at \({pct(y)}\%\) loss. Profit minus loss equals the overall profit:<br>"
         rf"\[ \frac{{{pct(x)}}}{{100}}q - \frac{{{pct(y)}}}{{100}}({tex(N)} - q) = \frac{{{pct(P)}}}{{100}}\times{tex(N)} \]"),
        ("Clear the 100s and solve.", rf"\[ {pct(x)}q - {tex(y * N)} + {pct(y)}q = {tex(P * N)} \]\[ {pct(x + y)}q = {tex(P * N + y * N)} \;\Rightarrow\; q = {tex(q)} \]"
         rf"So \({tex(q)}\) kg at a profit and \({tex(N)} - {tex(q)} = {tex(rest)}\) kg at a loss.")
    )
    rule = steps(("Identify the values.", rf"\(N = {tex(N)}\), \(x = {pct(x)}\) (profit), \(y = {pct(y)}\) (loss), \(P = {pct(P)}\)."),
                 ("Apply the specified rule.", F10),
                 ("Substitute the values.", rf"\[ \frac{{{pct(P)} + {pct(y)}}}{{{pct(x)} + {pct(y)}}}\times{tex(N)} = \frac{{{pct(P + y)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)}\text{{ kg}} \]"
                  rf"\[ \frac{{{pct(x)} - {pct(P)}}}{{{pct(x)} + {pct(y)}}}\times{tex(N)} = \frac{{{pct(x - P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(rest)}\text{{ kg}} \]"))
    fin = rf"\({tex(q)}\) kg at \({pct(x)}\%\) profit and \({tex(rest)}\) kg at \({pct(y)}\%\) loss"
    rb = rbe([rf"\(N = {tex(N)}\), \(x = {pct(x)}\), \(y = {pct(y)}\), \(P = {pct(P)}\).", rf"Profit part \(= \frac{{{pct(P + y)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)}\) kg.",
              rf"Loss part \(= \frac{{{pct(x - P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(rest)}\) kg."], fin)
    sc = shortcut(rf"\[ \frac{{{pct(P + y)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)},\quad {tex(N)} - {tex(q)} = {tex(rest)} \]", fin)
    return result(("pair", (q, rest)), T10, trad, rule, fin, rb, sc)


PLAN10 = {844: lambda: profit_loss(50, 10, 5, 7, "rice"), 1133: lambda: profit_loss(60, 14, 6, 10, "rice"),
          1134: lambda: profit_loss(80, 24, 12, 15, "pulse"), 1135: lambda: profit_loss(50, 28, 12, 16, "wheat"),
          1136: lambda: profit_loss(60, 18, 10, 11, "tea")}

PLANS = {5: PLAN5, 6: PLAN6, 7: PLAN7, 8: PLAN8, 9: PLAN9, 10: PLAN10}

if __name__ == "__main__":
    for n in map(int, sys.argv[1:] or PLANS):
        folder = os.path.join(HERE, f"rule{n:02d}")
        cur = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        card_id = cur["rule_card"]["id"]
        out = [regen_entry(row, PLANS[n][row["id"]](), card_id) for row in cur["rows"]]
        assert sorted(PLANS[n]) == sorted(r["id"] for r in cur["rows"])
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: generated {len(out)} rows")
