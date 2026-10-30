"""Profit and Loss Rules 53-56 (2026-10-30). Rule 53: n items of A and m of B bought for Rs P, sold at x% and y% profit (or loss) for a
whole gain (or loss) of Rs X - the price of one of each. Rule 54: equal numbers bought at x and y a rupee, sold mixed at z a rupee
for a loss (or gain) of Rs L - how many in all. Rule 55: marked x% above cost, y% discount - profit per cent (and the reverse: the
mark-up needed; the cost from the selling price). Rule 56: two items for Rs P, one at x% loss and one at y% gain, no gain and no
loss on the whole - both costs. Writes the four cards, regenerates old rows 350-352 (R53), 353 (R54), 354, 358, 371 (R55), 359 (R56)
with simple-style sentences, new settings and all-new numbers, and adds the book's other examples and exercises.
Usage: python gen_53_56.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import _k, place, popts  # noqa: E402
from gen_18_21 import ropts, sopts  # noqa: E402
from gen_51_52 import pct_txt  # noqa: E402

# ---------------------------------------------------------------- Rule 53
T53 = (r"If \(n\) items of A and \(m\) items of B cost Rs \(P\), and A is sold at \(x\%\) and B at \(y\%\) profit for a whole gain of "
       r"Rs \(X\) (a loss counts as a negative per cent or gain), then<br>\[ \text{one A}=\frac{100X-Py}{n(x-y)} \]<br>"
       r"\[ \text{one B}=\frac{Px-100X}{m(x-y)} \]")


def sg(w):
    return -1 if w == "loss" else 1


def r53(n, A, mm, B, P, x, wx, y, wy, X, wX, ask):
    n, mm, P, X = map(F, (n, mm, P, X))
    xs, ys, Xs = sg(wx) * F(x), sg(wy) * F(y), sg(wX) * X
    a = (100 * Xs - P * ys) / (n * (xs - ys))
    b = (P * xs - 100 * Xs) / (mm * (xs - ys))
    trad = steps(
        (f"Let one {A} cost Rs \\(a\\) and one {B} Rs \\(b\\).", rf"Cost: \({tex(n)}a + {tex(mm)}b = {m(P)}\)."),
        (f"Write the whole {wX}.", rf"\[ \frac{{{tex(xs)}}}{{100}}\times {tex(n)}a + \frac{{{tex(ys)}}}{{100}}\times {tex(mm)}b = {tex(Xs)} \]"
                                   r"(a loss is written with a minus sign)"),
        ("Solve the two equations.", rf"Multiply the first by \(\frac{{{tex(ys)}}}{{100}}\) and subtract: "
                                     rf"\[ \frac{{{tex(xs - ys)}}}{{100}}\times {tex(n)}a = {tex(Xs - P * ys / 100)} \;\Rightarrow\; a = {m(a)},\quad b = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(n = {tex(n)}\), \(m = {tex(mm)}\), \(P = {m(P)}\), \(x = {tex(xs)}\), \(y = {tex(ys)}\), \(X = {tex(Xs)}\)."),
        ("Apply the specified rule.", T53.split("<br>", 1)[1]),
        ("Substitute the values.", rf"\[ \text{{one {A}}} = \frac{{100\times {tex(Xs)} - {m(P)}\times {tex(ys)}}}{{{tex(n)}\times {tex(xs - ys)}}} = {m(a)} \]<br>"
                                   rf"\[ \text{{one {B}}} = \frac{{{m(P)}\times {tex(xs)} - 100\times {tex(Xs)}}}{{{tex(mm)}\times {tex(xs - ys)}}} = {m(b)} \]"))
    if ask == "totals":
        ans, fin = ("pair", (n * a, mm * b)), rf"all the {A}s Rs \({m(n * a)}\), all the {B}s Rs \({m(mm * b)}\)"
        rule += rf"<br>All the {A}s: \({tex(n)}\times {m(a)} = {m(n * a)}\); all the {B}s: \({tex(mm)}\times {m(b)} = {m(mm * b)}\)."
    elif ask == "oneA":
        ans, fin = ("number", a), rf"Rs \({m(a)}\)"
    else:
        ans, fin = ("pair", (a, b)), rf"one {A} Rs \({m(a)}\), one {B} Rs \({m(b)}\)"
    rb = [rf"\(x = {tex(xs)}\), \(y = {tex(ys)}\), \(X = {tex(Xs)}\).", rf"One {A} \(= \frac{{{tex(100 * Xs - P * ys)}}}{{{tex(n * (xs - ys))}}} = {m(a)}\).",
          rf"One {B} \(= \frac{{{tex(P * xs - 100 * Xs)}}}{{{tex(mm * (xs - ys))}}} = {m(b)}\)."]
    sc = rf"\[ \frac{{{tex(100 * Xs - P * ys)}}}{{{tex(n * (xs - ys))}}} = {m(a)},\quad \frac{{{tex(P * xs - 100 * Xs)}}}{{{tex(mm * (xs - ys))}}} = {m(b)} \]"
    return result(ans, T53, trad, rule, fin, rb, sc)


def opts_pair(g, la, lb):
    a, b = (F(t) for t in g["answer"][1])
    Q = lambda t: rf"{la} Rs \({m(t[0])}\), {lb} Rs \({m(t[1])}\)"
    step = 10 if min(a, b) > 40 else 2
    return place(Q((a, b)), [Q((b, a)), Q((a + step, b)), Q((a, b + step))])


# ---------------------------------------------------------------- Rule 54
T54 = (r"If equal numbers of articles are bought at \(x\) and \(y\) a rupee and all are sold at \(z\) a rupee for a loss of Rs \(L\), "
       r"the number bought in all is<br>\[ \frac{2xyz\,L}{z(x+y)-2xy} \]")


def r54(x, y, z, L, gain=False):
    x, y, z, L = map(F, (x, y, z, L))
    per = 1 / x + 1 / y - 2 / z                     # loss on one article of each kind
    N = (-L if gain else L) / per
    total = 2 * N
    den = z * (x + y) - 2 * x * y
    word = "gain" if gain else "loss"
    trad = steps(
        ("Let him buy \\(N\\) of each kind.", rf"Cost \(= \frac{{N}}{{{tex(x)}}} + \frac{{N}}{{{tex(y)}}}\); takings \(= \frac{{2N}}{{{tex(z)}}}\)."),
        (f"The {word} on one of each kind.", rf"\[ \left|\frac{{1}}{{{tex(x)}}} + \frac{{1}}{{{tex(y)}}} - \frac{{2}}{{{tex(z)}}}\right| = {tex(abs(per))} \]"),
        ("Number of each kind, then in all.", rf"\[ N = {m(L)} \div {tex(abs(per))} = {tex(N)},\qquad 2N = {tex(total)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\), \(L = {m(L)}\) ({word})."),
        ("Apply the specified rule.", T54.split("<br>")[1] + ("" if not gain else r"(for a gain the denominator is negative; use its size)")),
        ("Substitute the values.", rf"\[ \frac{{2\times {tex(x)}\times {tex(y)}\times {tex(z)}\times {m(L)}}}{{|{tex(z)}\times {tex(x + y)} - {tex(2 * x * y)}|}} = "
                                   rf"\frac{{{tex(2 * x * y * z * L)}}}{{{tex(abs(den))}}} = {tex(total)} \]"))
    rb = [rf"\(z(x+y) - 2xy = {tex(den)}\).", rf"\(2xyzL = {tex(2 * x * y * z * L)}\).", rf"Number in all \(= {tex(total)}\)."]
    return result(("number", total), T54, trad, rule, rf"\({tex(total)}\)", rb, rf"\[ \frac{{{tex(2 * x * y * z * L)}}}{{{tex(abs(den))}}} = {tex(total)} \]")


def nopts(v):
    v = F(v)
    return place(rf"\({tex(v)}\)", [rf"\({tex(w)}\)" for w in (v + 60, v - 60, 2 * v)])


# ---------------------------------------------------------------- Rule 55
T55 = (r"If goods are marked \(x\%\) above the cost price and a discount of \(y\%\) is allowed, the profit (loss if negative) is"
       r"<br>\[ \left(x-y-\frac{xy}{100}\right)\% \]")


def r55(x, y, ask="profit", S=None, note=""):
    x, y = F(x), F(y)
    z = x - y - x * y / 100
    mp, sp = 100 + x, (100 + x) * (100 - y) / 100
    trad = [("Take the cost price as 100.", (note + " " if note else "") + rf"Marked price \(= {tex(mp)}\); discount \({tex(y)}\%\) of it \(= {tex(mp * y / 100)}\); selling price \(= {tex(sp)}\).")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T55.split("<br>")[1]),
            ("Substitute the values.", rf"\[ {tex(x)} - {tex(y)} - \frac{{{tex(x)}\times {tex(y)}}}{{100}} = {tex(z)}\% \]")]
    if ask == "cp":
        S = F(S)
        cp = S * 100 / sp
        trad.append(("Selling price is " + tex(sp) + "% of the cost.", rf"\[ \text{{CP}} = {m(S)}\times\frac{{100}}{{{tex(sp)}}} = {m(cp)} \]"))
        rule.append(("Cost from the selling price.", rf"SP \(= (100 + {tex(z)})\%\) of CP, so CP \(= \frac{{{m(S)}\times 100}}{{{tex(100 + z)}}} = {m(cp)}\)."))
        rb = [rf"Profit \(= {tex(z)}\%\).", rf"SP \(= {tex(100 + z)}\%\) of CP.", rf"CP \(= {m(cp)}\)."]
        return result(("number", cp), T55, steps(*trad), steps(*rule), rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{{m(S)}\times 100}}{{{tex(100 + z)}}} = {m(cp)} \]")
    trad.append(("Profit or loss per cent.", rf"\[ {tex(sp)} - 100 = {tex(z)}\% \]" + ("It is negative, so a loss." if z < 0 else "")))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\(\frac{{xy}}{{100}} = {tex(x * y / 100)}\).", rf"\({tex(x)} - {tex(y)} - {tex(x * y / 100)} = {tex(z)}\%\)."]
    if ask == "signed":
        fin = rf"a {'loss' if z < 0 else 'profit'} of \({tex(abs(z))}\%\)"
        return result(("signed", z), T55, steps(*trad), steps(*rule), fin, rb, rf"\[ {tex(x)} - {tex(y)} - {tex(x * y / 100)} = {tex(z)}\% \]")
    return result(("number", z), T55, steps(*trad), steps(*rule), PCT(z), rb, rf"\[ {tex(x)} - {tex(y)} - {tex(x * y / 100)} = {tex(z)}\% \]")


def r55_markup(y, z):
    y, z = F(y), F(z)
    x = 100 * (z + y) / (100 - y)
    trad = steps(
        ("Take the cost price as 100.", rf"For a profit of \({tex(z)}\%\) the selling price must be \({tex(100 + z)}\)."),
        ("The selling price is " + tex(100 - y) + "% of the marked price.", rf"\[ \text{{MP}} = {tex(100 + z)}\times\frac{{100}}{{{tex(100 - y)}}} = {tex(100 + x)} \]"),
        ("Mark-up on the cost.", rf"\[ {tex(100 + x)} - 100 = {tex(x)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(y = {tex(y)}\), profit \(z = {tex(z)}\); the mark-up \(x\) is unknown."),
        ("Apply the specified rule.", T55.split("<br>")[1] + rf"with \(x - y - \frac{{xy}}{{100}} = z\)"),
        ("Solve for x.", rf"\[ x\left(1 - \frac{{{tex(y)}}}{{100}}\right) = {tex(z)} + {tex(y)} \;\Rightarrow\; x = \frac{{100\times {tex(z + y)}}}{{{tex(100 - y)}}} = {tex(x)}\% \]"))
    rb = [rf"\(y = {tex(y)}\), \(z = {tex(z)}\).", rf"\(x = \frac{{100(z + y)}}{{100 - y}}\).", rf"\(= {tex(x)}\%\)."]
    return result(("number", x), T55, trad, rule, PCT(x), rb, rf"\[ \frac{{100\times {tex(z + y)}}}{{{tex(100 - y)}}} = {tex(x)}\% \]")


# ---------------------------------------------------------------- Rule 56
T56 = (r"If two items bought for Rs \(P\) together are sold, A at a loss of \(x\%\) and B at a gain of \(y\%\), with no gain and no loss "
       r"on the whole, then<br>\[ \text{CP of A}=\frac{Py}{x+y},\qquad \text{CP of B}=\frac{Px}{x+y} \]")


def r56(P, x, y, A, B):
    P, x, y = map(F, (P, x, y))
    a, b = P * y / (x + y), P * x / (x + y)
    trad = steps(
        ("The loss on one equals the gain on the other.", rf"\[ \frac{{{tex(x)}}}{{100}}\times\text{{CP of {A}}} = \frac{{{tex(y)}}}{{100}}\times\text{{CP of {B}}} \]"),
        ("So the costs are in the ratio", rf"\[ {A} : {B} = {tex(y)} : {tex(x)} \]"),
        (f"Share Rs {m(P)} in that ratio.", rf"\[ {A} = {m(P)}\times\frac{{{tex(y)}}}{{{tex(x + y)}}} = {m(a)},\qquad {B} = {m(P)} - {m(a)} = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(P = {m(P)}\), \(x = {tex(x)}\) ({A}, loss), \(y = {tex(y)}\) ({B}, gain)."),
        ("Apply the specified rule.", T56.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(P)}\times {tex(y)}}}{{{tex(x + y)}}} = {m(a)},\qquad \frac{{{m(P)}\times {tex(x)}}}{{{tex(x + y)}}} = {m(b)} \]"))
    rb = [rf"\(x + y = {tex(x + y)}\).", rf"{A.capitalize()} \(= \frac{{{m(P)}\times {tex(y)}}}{{{tex(x + y)}}} = {m(a)}\).", rf"{B.capitalize()} \(= {m(b)}\)."]
    return result(("pair", (a, b)), T56, trad, rule, rf"{A} Rs \({m(a)}\), {B} Rs \({m(b)}\)", rb,
                  rf"\[ \frac{{{m(P)}\times {tex(y)}}}{{{tex(x + y)}}} = {m(a)},\quad \frac{{{m(P)}\times {tex(x)}}}{{{tex(x + y)}}} = {m(b)} \]")


CARDS = {
    53: card(53, "Two Kinds of Items, Two Rates, the Whole Gain Known",
             r"\(n\) items of A and \(m\) of B cost Rs \(P\); A gains \(x\%\), B gains \(y\%\) and the whole gain is Rs \(X\). The cost and the gain "
             r"give two equations for the two prices.",
             r"\[ \text{one A}=\frac{100X-Py}{n(x-y)},\qquad \text{one B}=\frac{Px-100X}{m(x-y)} \]",
             [("Cost", r"na+mb=P"), ("Gain", r"\frac{x}{100}na+\frac{y}{100}mb=X"), ("Solve", r"a=\frac{100X-Py}{n(x-y)}")],
             r"A loss is a negative per cent and a whole loss a negative \(X\) - the same formula covers all four cases.",
             "'A man buys n horses and m oxen for Rs P, sells the horses at x% profit and the oxen at y% profit, and gains Rs X. Find the price of each.'",
             r"\(2\) A and \(4\) B for Rs \(400\), \(10\%\) and \(20\%\), gain Rs \(60\): one A \(=\frac{6000-8000}{2\times(-10)}=\text{Rs }100\), one B Rs \(50\).",
             r"Forgetting the minus sign of a loss."),
    54: card(54, "Equal Numbers at Two Rates, Sold Mixed, the Loss Known",
             r"Each pair (one of each kind) costs \(\frac{1}{x}+\frac{1}{y}\) and sells for \(\frac{2}{z}\); the loss Rs \(L\) divided by the loss on "
             r"one pair gives the number of pairs.",
             r"\[ \text{Number in all}=\frac{2xyz\,L}{z(x+y)-2xy} \]",
             [("Loss on a pair", r"\frac{1}{x}+\frac{1}{y}-\frac{2}{z}"), ("Pairs", r"L\div\left(\frac{1}{x}+\frac{1}{y}-\frac{2}{z}\right)"), ("In all", r"2\times\text{pairs}")],
             r"If \(z(x+y)\lt 2xy\) the sale gives a gain, not a loss: a 'loss' question with such numbers has no answer.",
             "'A person bought some oranges at x a rupee and the same number at y a rupee, sold them mixed at z a rupee and lost Rs L. How many did he buy?'",
             r"\(10\) and \(15\) a rupee, sold at \(15\) a rupee, loss Rs \(1\): loss on a pair \(=\frac{1}{10}+\frac{1}{15}-\frac{2}{15}=\frac{1}{30}\), "
             r"so \(30\) pairs, \(60\) in all.",
             r"Giving the number of each kind instead of the number in all."),
    55: card(55, "Marked Up x%, Discount y%",
             r"Marking up by \(x\%\) and then taking \(y\%\) off the marked price leaves a profit of \(x-y-\frac{xy}{100}\) per cent of the cost.",
             r"\[ \text{Profit}=\left(x-y-\frac{xy}{100}\right)\%\quad(\text{a loss if negative}) \]",
             [("Marked price (CP = 100)", r"100+x"), ("After the discount", r"(100+x)\frac{100-y}{100}"), ("Profit", r"x-y-\frac{xy}{100}")],
             r"With \(x=y\) there is always a loss of \(\frac{x^2}{100}\%\); for a profit \(z\) with discount \(y\), mark up \(\frac{100(z+y)}{100-y}\%\).",
             "'A tradesman marks his goods x% above the cost price and allows a discount of y%. What profit per cent does he make?'",
             r"\(20\%\) up, \(5\%\) off: \(20-5-1=14\%\) profit.",
             r"Taking \(x-y\) as the profit - the discount is on the larger marked price."),
    56: card(56, "One at a Loss, One at a Gain, No Gain and No Loss",
             r"Two items cost Rs \(P\) together; the loss on one equals the gain on the other, so \(x\%\) of A's cost equals \(y\%\) of B's cost.",
             r"\[ \text{CP of A}=\frac{Py}{x+y},\qquad \text{CP of B}=\frac{Px}{x+y} \]",
             [("Loss = gain", r"\frac{x}{100}a=\frac{y}{100}b"), ("Ratio", r"a:b=y:x"), ("Share Rs P", r"a=\frac{Py}{x+y}")],
             r"The item sold at the smaller per cent is the dearer one.",
             "'A man buys two horses for Rs P; he sells one at x% loss and the other at y% gain and neither gains nor loses. What does each cost?'",
             r"Rs \(900\), \(10\%\) loss and \(20\%\) gain: \(\frac{900\times 20}{30}=\text{Rs }600\) and Rs \(300\).",
             r"Sharing in the ratio \(x:y\) instead of \(y:x\)."),
}

# ---------------------------------------------------------------- questions
Q53 = ("A dealer buys {n} {As} and {m} {Bs} for Rs {P}. He sells the {As} at a {wx} of {x}% and the {Bs} at a {wy} of {y}%, and his "
       "overall {wX} is Rs {X}. {ask}")
Q53S = ("{n} {As} and {m} {Bs} cost a farmer Rs {P}. He sells them for Rs {S}, making a profit of {x}% on the {As} and a profit of {y}% "
        "on the {Bs}. Find the cost of one {A} and of one {B}.")
ASK53 = {"each": "Find the cost of one {A} and of one {B}.", "totals": "How much did he pay for all the {As} and for all the {Bs}?",
         "oneA": "Find the cost of one {A}."}


def q53(names, c, ask):
    A, As, B, Bs = names
    n, mm, P, x, wx, y, wy, X, wX = c
    return Q53.format(n=n, As=As, m=mm, Bs=Bs, P=P, wx=wx, x=x, wy=wy, y=y, wX=wX, X=X, ask=ASK53[ask].format(A=A, As=As, B=B, Bs=Bs))


Q54 = ("A vendor buys some {item} at {x} a rupee and the same number at {y} a rupee. She mixes them and sells them at {sale}. "
       "In all she makes a {w} of Rs {L}. How many {item} did she buy in all?")


def z_of(sale):
    a, rest = sale.split(" ", 1)
    return F(int(a), int(rest.split()[1])) if rest.startswith("for") else F(int(a))


Q55 = {"profit": "A shopkeeper marks his goods {x}% above the cost price and allows a discount of {y}% on the marked price. Find his profit per cent.",
       "signed": "A shop marks its goods {x}% above the cost price and then gives a discount of {y}% on the marked price. Find its gain or loss per cent.",
       "cp": "A seller marks an article {x}% above its cost price and allows a discount of {y}%. If he sells it for Rs {S}, find its cost price.",
       "markup": "A shop takes {y}% off the marked price of every article. By what per cent should it raise the cost price when marking the goods, so that it still earns a profit of {z}%?",
       "bill": "A shopkeeper marks his goods {x}% above the cost price. On a bill of Rs {B} he allows Rs {D} off. Find his profit per cent.",
       "paise": "A trader marks his goods {x}% above the cost price and allows a discount of {p} paise in a rupee on the marked price. Find his profit per cent."}
Q56 = ("A man buys a {A} and a {B} for Rs {P} in all. He sells the {A} at a loss of {x}% and the {B} at a gain of {y}%, and on the whole "
       "he neither gains nor loses. Find the cost of each.")


def build(rule, spec):
    """spec -> (gen result, question, options, answer position)"""
    if rule == 53:
        kind, names, c = spec
        A, As, B, Bs = names
        if kind == "sp":
            n, mm, P, x, y, S = c
            g = r53(n, A, mm, B, P, x, "profit", y, "profit", S - P, "gain", "each")
            q = Q53S.format(n=n, As=As, m=mm, Bs=Bs, P=P, S=S, x=x, y=y, A=A, B=B)
        else:
            g = r53(*c[:1], A, c[1], B, *c[2:], kind)
            q = q53(names, c, kind)
        if g["answer"][0] == "number":
            op = ropts(g["answer"][1])
        elif kind == "totals":
            op = opts_pair(g, f"all {As}", f"all {Bs}")
        else:
            op = opts_pair(g, A.capitalize(), B)
        return g, q, op
    if rule == 54:
        item, x, y, sale, w, L = spec
        g = r54(x, y, z_of(sale), L, gain=(w == "gain"))
        return g, Q54.format(item=item, x=x, y=y, sale=sale, w=w, L=L), nopts(g["answer"][1])
    if rule == 55:
        kind, c = spec
        if kind == "markup":
            y, z = c
            g = r55_markup(y, z)
            return g, Q55[kind].format(y=pct_txt(y), z=pct_txt(z)), popts(g["answer"][1])
        if kind == "bill":
            x, B, D = c
            g = r55(x, F(D) * 100 / B, note=rf"The discount is Rs \({m(D)}\) on Rs \({m(B)}\), i.e. \({tex(F(D) * 100 / B)}\%\).")
            return g, Q55[kind].format(x=x, B=B, D=D), popts(g["answer"][1])
        if kind == "paise":
            x, p = c
            g = r55(x, p, note=rf"A discount of \({tex(p)}\) paise in a rupee is \({tex(p)}\%\).")
            return g, Q55[kind].format(x=x, p=p), popts(g["answer"][1])
        if kind == "cp":
            x, y, S = c
            g = r55(x, y, "cp", S)
            return g, Q55[kind].format(x=pct_txt(x), y=pct_txt(y), S=S), ropts(g["answer"][1])
        x, y = c
        g = r55(x, y, kind)
        return g, Q55[kind].format(x=pct_txt(x), y=pct_txt(y)), (sopts if kind == "signed" else popts)(g["answer"][1])
    A, B, (P, x, y) = spec
    g = r56(P, x, y, A, B)
    return g, Q56.format(A=A, B=B, P=P, x=x, y=y), opts_pair(g, A.capitalize(), B)


OLD = {53: {350: ("each", ("desk", "desks", "chair", "chairs"), (6, 9, 9000, 15, "profit", 20, "profit", 1530, "gain")),
            351: ("each", ("bag", "bags", "belt", "belts"), (8, 12, 2720, 12, "profit", 20, "loss", 96, "gain")),
            352: ("totals", ("sofa", "sofas", "stool", "stools"), (4, 6, 7500, 8, "profit", 30, "profit", 930, "gain"))},
       54: {353: ("lemons", 7, 14, "20 for 2 rupees", "loss", 2)},
       55: {354: ("profit", (40, 15)), 358: ("signed", (20, 20))},
       56: {359: ("cooler", "fan", (1540, 8, 14))}}
NEW = {53: [("r53_n2", ("each", ("heater", "heaters", "geyser", "geysers"), (7, 5, 12900, 5, "loss", 8, "loss", 780, "loss"))),
            ("r53_n3", ("each", ("pen", "pens", "ink bottle", "ink bottles"), (9, 6, 510, 15, "loss", 12, "profit", 36, "loss"))),
            ("r53_e1", ("oneA", ("cap", "caps", "scarf", "scarves"), (15, 24, 1980, 30, "profit", 25, "profit", 540, "gain"))),
            ("r53_e2", ("sp", ("cow", "cows", "goat", "goats"), (4, 10, 90000, 20, 10, 105000))),
            ("r53_e3", ("oneA", ("pony", "ponies", "calf", "calves"), (3, 8, 38000, 12, "profit", 18, "profit", 5760, "gain"))),
            ("r53_e5", ("each", ("file", "files", "marker", "markers"), (8, 25, 660, 20, "profit", 24, "profit", 144, "gain")))],
       54: [("r54_e1", ("plums", 6, 9, "15 for 2 rupees", "loss", 7)), ("r54_e2", ("guavas", 4, 12, "7 a rupee", "loss", 6)),
            ("r54_e3", ("limes", 10, 15, "22 for 2 rupees", "gain", 5)), ("r54_e4", ("figs", 14, 21, "35 for 2 rupees", "loss", 2))],
       55: [("r55_ex2", ("markup", (4, 20))), ("r55_e1", ("bill", (25, 450, 36))), ("r55_e2", ("markup", (5, 14))),
            ("r55_e3", ("profit", (36, F(25, 4)))), ("r55_e4", ("profit", (50, 20))), ("r55_e5", ("paise", (40, 5))),
            ("r55_e6", ("markup", (15, 19)))],
       56: [("r56_e1", ("chair", "stool", (2100, 9, 12))), ("r56_e2", ("table", "bench", (2600, 12, 14))), ("r56_e3", ("bullock", "goat", (990, 6, 27))),
            ("r56_e4", ("lamp", "clock", (760, 15, 23))), ("r56_e5", ("cycle", "pram", (2040, 21, 30)))]}


MOVED = {55: 1}


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert set(OLD[rule]) <= set(rows)  # row 371 moved to Rule 63 on 2026-10-30 (it is that rule's book example)
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, spec)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    _k[0] += MOVED.get(rule, 0)  # row 371 used an answer position here before it moved; keeps the applied files reproducible
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        kind, v = g["answer"]
        answers.append([key, [kind, [str(t) for t in v] if kind == "pair" else str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (53, 54, 55, 56):
        main(r)
