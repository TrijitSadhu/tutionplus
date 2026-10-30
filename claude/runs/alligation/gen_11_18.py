"""Rules 11-18: regenerates every row in the prompt #10 layout (Theorem -> Traditional Method -> Specified Rule ->
Verification -> Final Answer) and builds the two missing book worked examples (Rules 13 and 14) as JsonImport
payloads with new numbers. Writes ruleNN/2_new_rows.json (+ 3_json_import_payload.json / 3_answers.json)."""
import json, os, sys
from fractions import Fraction as F
from functools import reduce
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import frac, money, new_question, pct, ratio, ratio_steps, rbe, regen_entry, rtex, shortcut, solution, steps, tex  # noqa: E402

R = lambda *v: tuple(F(x) for x in v)


def result(answer, theorem, trad, rule, fin, rb, sc):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rb, shortcut=sc)


# ---------------------------------------------------------------- Rule 11: profit on one part, overall loss
T11 = (r"If \(N\) kg are sold partly at \(x\%\) profit and the rest at \(y\%\) loss, and on the whole there is a loss of \(P\%\), then<br>"
       r"\[ \text{At } x\%\text{ profit} = \frac{y-P}{x+y}\times N,\qquad \text{At } y\%\text{ loss} = \frac{x+P}{x+y}\times N \]")


def overall_loss(N, x, y, P):
    N, x, y, P = R(N, x, y, P)
    q = (y - P) / (x + y) * N
    rest = N - q
    trad = steps(
        ("Take a convenient cost.", rf"Let the rice cost Rs \(1\) per kg, so the whole lot costs Rs \({tex(N)}\)."),
        ("Let the unknown be the part sold at a profit.", rf"Let \(q\) kg be sold at \({pct(x)}\%\) profit and \(({tex(N)} - q)\) kg at \({pct(y)}\%\) loss. "
         rf"The overall result is a loss of \({pct(P)}\%\):<br>\[ \frac{{{pct(x)}}}{{100}}q - \frac{{{pct(y)}}}{{100}}({tex(N)} - q) = -\frac{{{pct(P)}}}{{100}}\times{tex(N)} \]"),
        ("Clear the 100s and solve.", rf"\[ {pct(x)}q - {tex(y * N)} + {pct(y)}q = -{tex(P * N)} \]\[ {pct(x + y)}q = {tex(y * N - P * N)} \;\Rightarrow\; q = {tex(q)} \]"
         rf"So \({tex(q)}\) kg at a profit and \({tex(N)} - {tex(q)} = {tex(rest)}\) kg at a loss.")
    )
    rule = steps(("Identify the values.", rf"\(N = {tex(N)}\), \(x = {pct(x)}\) (profit), \(y = {pct(y)}\) (loss), overall loss \(P = {pct(P)}\)."),
                 ("Apply the specified rule.", r"\[ \text{At } x\%\text{ profit} = \frac{y-P}{x+y}\times N,\qquad \text{At } y\%\text{ loss} = \frac{x+P}{x+y}\times N \]"),
                 ("Substitute the values.", rf"\[ \frac{{{pct(y)} - {pct(P)}}}{{{pct(x)} + {pct(y)}}}\times{tex(N)} = \frac{{{pct(y - P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)}\text{{ kg}} \]"
                  rf"\[ \frac{{{pct(x)} + {pct(P)}}}{{{pct(x)} + {pct(y)}}}\times{tex(N)} = \frac{{{pct(x + P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(rest)}\text{{ kg}} \]"))
    fin = rf"\({tex(q)}\) kg at \({pct(x)}\%\) profit and \({tex(rest)}\) kg at \({pct(y)}\%\) loss"
    rb = rbe([rf"\(N = {tex(N)}\), \(x = {pct(x)}\), \(y = {pct(y)}\), overall loss \(P = {pct(P)}\).",
              rf"Profit part \(= \frac{{{pct(y - P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)}\) kg.", rf"Loss part \(= \frac{{{pct(x + P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(rest)}\) kg."], fin)
    sc = shortcut(rf"\[ \frac{{{pct(y - P)}}}{{{pct(x + y)}}}\times{tex(N)} = {tex(q)},\quad {tex(N)} - {tex(q)} = {tex(rest)} \]", fin)
    return result(("pair", (q, rest)), T11, trad, rule, fin, rb, sc)


PLAN11 = {1137: lambda: overall_loss(70, 18, 10, 6), 1138: lambda: overall_loss(60, 25, 15, 5),
          1139: lambda: overall_loss(60, 22, 8, 4), 1140: lambda: overall_loss(100, 35, 15, 5)}

# ---------------------------------------------------------------- Rule 12: increase in savings
T12 = (r"If expenditure and savings are in the ratio \(a : b\), income rises by \(x\%\) and expenditure rises by \(y\%\), then<br>"
       r"\[ \text{Increase in savings} = \left[\left(\frac{a}{b} + 1\right)x - \frac{a}{b}\,y\right]\% \]")


def savings(a, b, x, y, name):
    a, b, x, y = R(a, b, x, y)
    inc = (a + b) * x / b - a * y / b
    E, S = 100 * a, 100 * b
    newI, newE = (E + S) * (100 + x) / 100, E * (100 + y) / 100
    newS = newI - newE
    assert (newS - S) / S * 100 == inc
    trad = steps(
        ("Take convenient amounts.", rf"Let {name}'s expenditure be Rs \({tex(E)}\) and savings Rs \({tex(S)}\) (ratio \({tex(a)} : {tex(b)}\)). Income \(= {tex(E + S)}\)."),
        ("Apply the increases.", rf"\[ \text{{New income}} = {tex(E + S)}\times\frac{{{tex(100 + x)}}}{{100}} = {tex(newI)} \]\[ \text{{New expenditure}} = {tex(E)}\times\frac{{{tex(100 + y)}}}{{100}} = {tex(newE)} \]"),
        ("Find the new savings and the increase.", rf"\[ \text{{New savings}} = {tex(newI)} - {tex(newE)} = {tex(newS)} \]"
         rf"\[ \text{{Increase}} = \frac{{{tex(newS)} - {tex(S)}}}{{{tex(S)}}}\times 100 = {pct(inc)}\% \]")
    )
    rule = steps(("Identify the values.", rf"\(a : b = {tex(a)} : {tex(b)}\), \(x = {pct(x)}\), \(y = {pct(y)}\)."),
                 ("Apply the specified rule.", r"\[ \left[\left(\frac{a}{b} + 1\right)x - \frac{a}{b}\,y\right]\% \]"),
                 ("Substitute the values.", rf"\[ \left(\frac{{{tex(a)}}}{{{tex(b)}}} + 1\right)\times{pct(x)} - \frac{{{tex(a)}}}{{{tex(b)}}}\times{pct(y)} = {tex((a + b) * x / b)} - {tex(a * y / b)} = {pct(inc)}\% \]"))
    fin = rf"\({pct(inc)}\%\)"
    rb = rbe([rf"\(\frac{{a}}{{b}} = \frac{{{tex(a)}}}{{{tex(b)}}}\), \(x = {pct(x)}\), \(y = {pct(y)}\).",
              rf"\(\left(\frac{{a}}{{b}} + 1\right)x = {tex((a + b) * x / b)}\) and \(\frac{{a}}{{b}}y = {tex(a * y / b)}\).", rf"Increase \(= {pct(inc)}\%\)."], fin)
    sc = shortcut(rf"\[ {tex((a + b) * x / b)} - {tex(a * y / b)} = {pct(inc)}\% \]", fin)
    return result(("number", inc), T12, trad, rule, fin, rb, sc)


PLAN12 = {1141: lambda: savings(4, 3, 15, 18, "Mira"), 1142: lambda: savings(3, 1, 12, 14, "Ritu"),
          1143: lambda: savings(5, 4, 18, 26, "Sita"), 1144: lambda: savings(2, 3, 20, 26, "Ranju")}

# ---------------------------------------------------------------- Rule 13: vessel partly emptied
T13 = (r"If a vessel of \(L\) litres holds liquids A and B, and taking out \(x\%\) of A and \(y\%\) of B empties \(z\%\) of the vessel, then<br>"
       r"\[ \text{A} = \frac{z-y}{x-y}\times L,\qquad \text{B} = \frac{x-z}{x-y}\times L \]")


def vessel(L, x, y, z, ask):
    L, x, y, z = R(L, x, y, z)
    m = (z - y) / (x - y) * L
    w = L - m
    trad = steps(
        ("Let the milk be \\(m\\) litres.", rf"Then the water is \(({tex(L)} - m)\) litres."),
        ("Write what was taken out.", rf"\[ \frac{{{pct(x)}}}{{100}}m + \frac{{{pct(y)}}}{{100}}({tex(L)} - m) = \frac{{{pct(z)}}}{{100}}\times{tex(L)} \]"),
        ("Clear the 100s and solve.", rf"\[ {pct(x)}m + {tex(y * L)} - {pct(y)}m = {tex(z * L)} \]\[ {pct(x - y)}m = {tex(z * L - y * L)} \;\Rightarrow\; m = {tex(m)} \]"
         rf"So milk \(= {tex(m)}\) litres and water \(= {tex(L)} - {tex(m)} = {tex(w)}\) litres.")
    )
    rule = steps(("Identify the values.", rf"\(L = {tex(L)}\), \(x = {pct(x)}\) (milk), \(y = {pct(y)}\) (water), \(z = {pct(z)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Milk} = \frac{z-y}{x-y}\times L,\qquad \text{Water} = \frac{x-z}{x-y}\times L \]"),
                 ("Substitute the values.", rf"\[ \text{{Milk}} = \frac{{{pct(z)} - {pct(y)}}}{{{pct(x)} - {pct(y)}}}\times{tex(L)} = \frac{{{pct(z - y)}}}{{{pct(x - y)}}}\times{tex(L)} = {tex(m)} \]"
                  rf"\[ \text{{Water}} = \frac{{{pct(x)} - {pct(z)}}}{{{pct(x)} - {pct(y)}}}\times{tex(L)} = \frac{{{pct(x - z)}}}{{{pct(x - y)}}}\times{tex(L)} = {tex(w)} \]"))
    if ask == "ratio":
        r = ratio(m, w)
        rule += rf"<br>Milk : water \(= {tex(m)} : {tex(w)} = {rtex(r)}\)."
        fin, answer = rf"\({rtex(r)}\)", ("ratio", r)
    else:
        fin, answer = rf"\({tex(m)}\) litres of milk and \({tex(w)}\) litres of water", ("pair", (m, w))
    rb = rbe([rf"\(L = {tex(L)}\), \(x = {pct(x)}\), \(y = {pct(y)}\), \(z = {pct(z)}\).", rf"Milk \(= \frac{{{pct(z - y)}}}{{{pct(x - y)}}}\times{tex(L)} = {tex(m)}\).",
              rf"Water \(= \frac{{{pct(x - z)}}}{{{pct(x - y)}}}\times{tex(L)} = {tex(w)}\)."], fin)
    sc = shortcut(rf"\[ \text{{Milk}} = \frac{{{pct(z - y)}}}{{{pct(x - y)}}}\times{tex(L)} = {tex(m)},\quad \text{{Water}} = {tex(w)} \]", fin)
    return result(answer, T13, trad, rule, fin, rb, sc)


PLAN13 = {1145: lambda: vessel(140, 82, 34, 62, "ratio"), 1146: lambda: vessel(60, 76, 36, 60, "pair"), 1147: lambda: vessel(90, 80, 35, 60, "pair")}

# ---------------------------------------------------------------- Rule 14: heads and legs
T14 = (r"If a group of 4-legged and 2-legged creatures has \(x\) heads and \(y\) legs, then<br>"
       r"\[ \text{4-legged} = \frac{y - 2x}{2},\qquad \text{2-legged} = \frac{4x - y}{2} \]")


def heads_legs(H, L, four, two, ask):
    H, L = R(H, L)
    f, t = (L - 2 * H) / 2, (4 * H - L) / 2
    trad = steps(
        ("Let the unknowns be the two kinds.", rf"Let there be \(f\) {four} (4 legs) and \(t\) {two} (2 legs)."),
        ("Write the heads and legs.", rf"\[ f + t = {tex(H)} \]\[ 4f + 2t = {tex(L)} \]"),
        ("Eliminate \\(t\\).", rf"Subtract twice the first equation from the second:<br>\[ 2f = {tex(L)} - {tex(2 * H)} = {tex(L - 2 * H)} \;\Rightarrow\; f = {tex(f)} \]\[ t = {tex(H)} - {tex(f)} = {tex(t)} \]")
    )
    rule = steps(("Identify the values.", rf"Heads \(x = {tex(H)}\), legs \(y = {tex(L)}\)."),
                 ("Apply the specified rule.", r"\[ \text{4-legged} = \frac{y - 2x}{2},\qquad \text{2-legged} = \frac{4x - y}{2} \]"),
                 ("Substitute the values.", rf"\[ \text{{{four.capitalize()}}} = \frac{{{tex(L)} - 2\times{tex(H)}}}{{2}} = {tex(f)},\qquad \text{{{two.capitalize()}}} = \frac{{4\times{tex(H)} - {tex(L)}}}{{2}} = {tex(t)} \]"))
    if ask == "four":
        fin, answer = rf"\({tex(f)}\) {four}", ("number", f)
    elif ask == "two":
        fin, answer = rf"\({tex(t)}\) {two}", ("number", t)
    else:
        fin, answer = rf"\({tex(t)}\) {two} and \({tex(f)}\) {four}", ("pair", (t, f))
    rb = rbe([rf"Heads \(x = {tex(H)}\), legs \(y = {tex(L)}\).", rf"4-legged \(= \frac{{{tex(L)} - {tex(2 * H)}}}{{2}} = {tex(f)}\).",
              rf"2-legged \(= \frac{{{tex(4 * H)} - {tex(L)}}}{{2}} = {tex(t)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(L)} - {tex(2 * H)}}}{{2}} = {tex(f)},\quad \frac{{{tex(4 * H)} - {tex(L)}}}{{2}} = {tex(t)} \]", fin)
    return result(answer, T14, trad, rule, fin, rb, sc)


PLAN14 = {1148: lambda: heads_legs(90, 240, "goats", "chickens", "pair"), 1149: lambda: heads_legs(120, 330, "rabbits", "pigeons", "four"),
          1150: lambda: heads_legs(90, 260, "rabbits", "pigeons", "two")}

# ---------------------------------------------------------------- Rule 15: draw off mixture, pour in B
T15 = (r"If a jar holds A and B in the ratio \(a : b\), and after \(L\) litres of the mixture are taken out and \(P\) litres of B are poured in the ratio "
       r"becomes \(x : y\), then the jar first held<br>\[ \text{A} = a\left(\frac{L}{a+b} + \frac{xP}{ay - bx}\right)\text{ litres} \]")


def replace(a, b, L, P, x, y):
    a, b, L, P, x, y = R(a, b, L, P, x, y)
    s = L / (a + b)
    k = s + x * P / (a * y - b * x)
    A = a * k
    trad = steps(
        ("Let the jar hold \\(a k\\) litres of A and \\(b k\\) of B.", rf"Here A \(= {tex(a)}k\) and B \(= {tex(b)}k\)."),
        ("Take out the mixture and pour in B.", rf"The \({tex(L)}\) litres taken out contain A \(= {tex(L)}\times\frac{{{tex(a)}}}{{{tex(a + b)}}} = {tex(a * s)}\) and B \(= {tex(b * s)}\).<br>"
         rf"\[ \text{{A left}} = {tex(a)}k - {tex(a * s)},\qquad \text{{B now}} = {tex(b)}k - {tex(b * s)} + {tex(P)} \]"),
        ("Use the new ratio.", rf"\[ \frac{{{tex(a)}k - {tex(a * s)}}}{{{tex(b)}k - {tex(b * s)} + {tex(P)}}} = \frac{{{tex(x)}}}{{{tex(y)}}} \]"
         rf"\[ {tex(y * a)}k - {tex(y * a * s)} = {tex(x * b)}k - {tex(x * b * s)} + {tex(x * P)} \]"
         rf"\[ {tex(y * a - x * b)}k = {tex(y * a * s - x * b * s + x * P)} \;\Rightarrow\; k = {tex(k)} \]"),
        ("Find A.", rf"\[ \text{{A}} = {tex(a)}\times{tex(k)} = {tex(A)}\text{{ litres}} \]")
    )
    rule = steps(("Identify the values.", rf"\(a : b = {tex(a)} : {tex(b)}\), \(L = {tex(L)}\), \(P = {tex(P)}\), \(x : y = {tex(x)} : {tex(y)}\)."),
                 ("Apply the specified rule.", r"\[ \text{A} = a\left(\frac{L}{a+b} + \frac{xP}{ay - bx}\right) \]"),
                 ("Substitute the values.", rf"\[ {tex(a)}\left(\frac{{{tex(L)}}}{{{tex(a + b)}}} + \frac{{{tex(x)}\times{tex(P)}}}{{{tex(a)}\times{tex(y)} - {tex(b)}\times{tex(x)}}}\right) = {tex(a)}\left({tex(s)} + \frac{{{tex(x * P)}}}{{{tex(a * y - b * x)}}}\right) = {tex(a)}\times{tex(k)} = {tex(A)} \]"))
    fin = rf"\({tex(A)}\) litres"
    rb = rbe([rf"\(a : b = {tex(a)} : {tex(b)}\), \(L = {tex(L)}\), \(P = {tex(P)}\), \(x : y = {tex(x)} : {tex(y)}\).",
              rf"\(\frac{{L}}{{a+b}} = {tex(s)}\) and \(\frac{{xP}}{{ay - bx}} = \frac{{{tex(x * P)}}}{{{tex(a * y - b * x)}}} = {tex(x * P / (a * y - b * x))}\).", rf"A \(= {tex(a)}\times{tex(k)} = {tex(A)}\) litres."], fin)
    sc = shortcut(rf"\[ {tex(a)}\left({tex(s)} + {tex(x * P / (a * y - b * x))}\right) = {tex(A)} \]", fin)
    return result(("number", A), T15, trad, rule, fin, rb, sc)


PLAN15 = {1151: lambda: replace(3, 1, 12, 12, 3, 5), 1152: lambda: replace(5, 2, 14, 16, 1, 2),
          1153: lambda: replace(4, 3, 14, 14, 2, 5), 1154: lambda: replace(5, 3, 16, 16, 5, 7)}

# ---------------------------------------------------------------- Rule 16: add B to change the ratio
T16 = (r"If \(L\) litres of a mixture hold A and B in the ratio \(a : b\), the amount of B to add to make the ratio \(x : y\) is<br>"
       r"\[ \text{B to add} = L\times\frac{ay - bx}{x(a+b)} \]")


def add_b(L, a, b, x, y):
    L, a, b, x, y = R(L, a, b, x, y)
    milk, water = L * a / (a + b), L * b / (a + b)
    need = milk * y / x
    add = need - water
    assert add == L * (a * y - b * x) / (x * (a + b))
    trad = steps(
        ("Split the mixture.", rf"Milk \(= {tex(L)}\times\frac{{{tex(a)}}}{{{tex(a + b)}}} = {tex(milk)}\) litres, water \(= {tex(water)}\) litres."),
        ("Keep the milk and find the water needed.", rf"For milk : water \(= {tex(x)} : {tex(y)}\):<br>\[ \text{{Water}} = {tex(milk)}\times\frac{{{tex(y)}}}{{{tex(x)}}} = {tex(need)} \]"),
        ("Find the water to add.", rf"\[ {tex(need)} - {tex(water)} = {tex(add)}\text{{ litres}} \]")
    )
    rule = steps(("Identify the values.", rf"\(L = {tex(L)}\), \(a : b = {tex(a)} : {tex(b)}\), \(x : y = {tex(x)} : {tex(y)}\)."),
                 ("Apply the specified rule.", r"\[ \text{B to add} = L\times\frac{ay - bx}{x(a+b)} \]"),
                 ("Substitute the values.", rf"\[ {tex(L)}\times\frac{{{tex(a)}\times{tex(y)} - {tex(b)}\times{tex(x)}}}{{{tex(x)}\times{tex(a + b)}}} = {tex(L)}\times\frac{{{tex(a * y - b * x)}}}{{{tex(x * (a + b))}}} = {tex(add)}\text{{ litres}} \]"))
    fin = rf"\({tex(add)}\) litres"
    rb = rbe([rf"\(L = {tex(L)}\), \(a : b = {tex(a)} : {tex(b)}\), \(x : y = {tex(x)} : {tex(y)}\).", rf"\(ay - bx = {tex(a * y - b * x)}\), \(x(a+b) = {tex(x * (a + b))}\).",
              rf"Water to add \(= {tex(L)}\times\frac{{{tex(a * y - b * x)}}}{{{tex(x * (a + b))}}} = {tex(add)}\) litres."], fin)
    sc = shortcut(rf"\[ {tex(L)}\times\frac{{{tex(a * y - b * x)}}}{{{tex(x * (a + b))}}} = {tex(add)} \]", fin)
    return result(("number", add), T16, trad, rule, fin, rb, sc)


PLAN16 = {1155: lambda: add_b(63, 4, 3, 2, 3), 1156: lambda: add_b(45, 3, 2, 3, 5), 1157: lambda: add_b(40, 5, 3, 5, 7), 1158: lambda: add_b(360, 5, 1, 5, 2)}

# ---------------------------------------------------------------- Rule 17: equal glasses emptied together
T17 = (r"If equal glasses hold spirit and water in the ratios \(a_1 : b_1,\ a_2 : b_2,\ \ldots,\ a_x : b_x\) and are emptied into one vessel, then<br>"
       r"\[ \text{Spirit} : \text{Water} = \left(\frac{a_1}{a_1+b_1} + \cdots + \frac{a_x}{a_x+b_x}\right) : \left(\frac{b_1}{a_1+b_1} + \cdots + \frac{b_x}{a_x+b_x}\right) \]")


def equal_glasses(pairs, first, second, given=None):
    """pairs: list of (a, b). given: optional sentence (e.g. '8 litres each')."""
    pairs = [(F(a), F(b)) for a, b in pairs]
    n = reduce(lambda u, v: u * v // gcd(u, v), [int(a + b) for a, b in pairs])
    A = sum(n * a / (a + b) for a, b in pairs)
    B = sum(n * b / (a + b) for a, b in pairs)
    r = ratio(A, B)
    rows = "".join(rf"<tr><td>\({tex(a)} : {tex(b)}\)</td><td>\({n}\times\frac{{{tex(a)}}}{{{tex(a + b)}}} = {tex(n * a / (a + b))}\)</td>"
                   rf"<td>\({n}\times\frac{{{tex(b)}}}{{{tex(a + b)}}} = {tex(n * b / (a + b))}\)</td></tr>" for a, b in pairs)
    table = f'<table border="1" cellpadding="4"><tr><th>Ratio</th><th>{first.capitalize()}</th><th>{second.capitalize()}</th></tr>{rows}</table>'
    trad = steps(
        ("Pick a convenient common size.", (given + " " if given else "") +
         rf"Only the fact that the glasses are equal matters, so let each hold \({n}\) litres (the LCM of {', '.join(f'{tex(a + b)}' for a, b in pairs)})."),
        ("Work out each glass.", table),
        ("Add up and compare.", rf"\[ \text{{{first.capitalize()}}} = {' + '.join(tex(n * a / (a + b)) for a, b in pairs)} = {tex(A)},\qquad "
         rf"\text{{{second.capitalize()}}} = {' + '.join(tex(n * b / (a + b)) for a, b in pairs)} = {tex(B)} \]So {first} : {second} \(= {tex(A)} : {tex(B)} = {rtex(r)}\).")
    )
    sa = " + ".join(rf"\frac{{{tex(a)}}}{{{tex(a + b)}}}" for a, b in pairs)
    sb = " + ".join(rf"\frac{{{tex(b)}}}{{{tex(a + b)}}}" for a, b in pairs)
    rule = steps(("Identify the ratios.", ", ".join(rf"\({tex(a)} : {tex(b)}\)" for a, b in pairs) + "."),
                 ("Apply the specified rule.", rf"\[ \left({sa}\right) : \left({sb}\right) \]"),
                 ("Simplify.", rf"\[ = \frac{{{tex(A)}}}{{{n}}} : \frac{{{tex(B)}}}{{{n}}} = {tex(A)} : {tex(B)} = {rtex(r)} \]"))
    fin = rf"\({rtex(r)}\)"
    rb = rbe([", ".join(rf"\({tex(a)} : {tex(b)}\)" for a, b in pairs) + ".", rf"Sum of {first} fractions \(= \frac{{{tex(A)}}}{{{n}}}\), sum of {second} fractions \(= \frac{{{tex(B)}}}{{{n}}}\).",
              rf"{first.capitalize()} : {second} \(= {tex(A)} : {tex(B)} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \left({sa}\right) : \left({sb}\right) = {rtex(r)} \]", fin)
    return result(("ratio", r), T17, trad, rule, fin, rb, sc)


PLAN17 = {1159: lambda: equal_glasses([(3, 2), (4, 3), (2, 1)], "milk", "water", r"The vessels hold \(8\) litres each."),
          1160: lambda: equal_glasses([(1, 2), (2, 3), (3, 4)], "spirit", "water"),
          1161: lambda: equal_glasses([(2, 1), (3, 1), (4, 1)], "milk", "water"),
          1162: lambda: equal_glasses([(65, 35), (75, 25), (80, 20), (85, 15)], "spirit", "water", r"A concentration of \(65\%\) means spirit : water \(= 65 : 35\), and so on."),
          1163: lambda: equal_glasses([(3, 1), (2, 1)], "alcohol", "water")}

# ---------------------------------------------------------------- Rule 18: two alloys mixed
T18 = (r"If \(M\) kg of a mixture, of which a fraction \(\frac{a}{b}\) is A, is mixed with \(N\) kg of a mixture, of which \(\frac{x}{y}\) is A, then<br>"
       r"\[ \text{A} : \text{B} = \left(M\frac{a}{b} + N\frac{x}{y}\right) : \left[M\left(1 - \frac{a}{b}\right) + N\left(1 - \frac{x}{y}\right)\right] \]")


def alloys(M, f1, N, f2):
    M, f1, N, f2 = R(M, f1, N, f2)
    z = M * f1 + N * f2
    c = M + N - z
    r = ratio(z, c)
    trad = steps(
        ("Zinc in each piece.", rf"\[ {tex(M)}\times{frac(f1)} = {tex(M * f1)}\text{{ kg}},\qquad {tex(N)}\times{frac(f2)} = {tex(N * f2)}\text{{ kg}} \]"),
        ("Totals.", rf"\[ \text{{Zinc}} = {tex(M * f1)} + {tex(N * f2)} = {tex(z)},\qquad \text{{Copper}} = ({tex(M)} + {tex(N)}) - {tex(z)} = {tex(c)} \]"),
        ("Ratio.", rf"\[ {tex(z)} : {tex(c)} = {rtex(r)} \]")
    )
    rule = steps(("Identify the values.", rf"\(M = {tex(M)}\), \(\frac{{a}}{{b}} = {frac(f1)}\), \(N = {tex(N)}\), \(\frac{{x}}{{y}} = {frac(f2)}\)."),
                 ("Apply the specified rule.", r"\[ \left(M\frac{a}{b} + N\frac{x}{y}\right) : \left[M\left(1 - \frac{a}{b}\right) + N\left(1 - \frac{x}{y}\right)\right] \]"),
                 ("Substitute the values.", rf"\[ \left({tex(M)}\times{frac(f1)} + {tex(N)}\times{frac(f2)}\right) : \left[{tex(M)}\times{frac(1 - f1)} + {tex(N)}\times{frac(1 - f2)}\right] = {tex(z)} : {tex(c)} = {rtex(r)} \]"))
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"\(M = {tex(M)}\), \(\frac{{a}}{{b}} = {frac(f1)}\), \(N = {tex(N)}\), \(\frac{{x}}{{y}} = {frac(f2)}\).", rf"Zinc \(= {tex(z)}\), copper \(= {tex(c)}\).",
              rf"Zinc : copper \(= {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ {tex(z)} : {tex(c)} = {rtex(r)} \]", fin)
    return result(("ratio", r), T18, trad, rule, fin, rb, sc)


PLAN18 = {1164: lambda: alloys(4, F(2, 5), 5, F(3, 10)), 1165: lambda: alloys(2, F(1, 3), 4, F(1, 4)),
          1166: lambda: alloys(6, F(1, 3), 5, F(1, 5)), 1167: lambda: alloys(6, F(2, 3), 4, F(3, 4))}

PLANS = {11: PLAN11, 12: PLAN12, 13: PLAN13, 14: PLAN14, 15: PLAN15, 16: PLAN16, 17: PLAN17, 18: PLAN18}

# Missing book worked examples, rewritten with new numbers.
NEW = {
    13: [("N1", "A vessel of \\(100\\) litres is filled with milk and water. When \\(75\\%\\) of the milk and \\(25\\%\\) of the water are taken out, "
                "the vessel is found to be \\(55\\%\\) empty. How much milk and how much water did the vessel hold at first?",
          ["55 litres, 45 litres", "65 litres, 35 litres", "60 litres, 40 litres", "None of these"], 3, lambda: vessel(100, 75, 25, 55, "pair"))],
    14: [("N1", "A zoo has rabbits and pigeons only. Counting heads gives \\(150\\) and counting legs gives \\(440\\). How many pigeons are there?",
          ["70", "80", "75", "85"], 2, lambda: heads_legs(150, 440, "rabbits", "pigeons", "two"))],
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
