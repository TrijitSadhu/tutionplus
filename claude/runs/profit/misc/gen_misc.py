"""Profit and Loss Miscellaneous set (2026-10-30): the 23 Miscellaneous problems at the end of the chapter. All 23 are in the DB as the old
rule-less rows 382-404 (M1 = 382 ... M23 = 404, in order). Each row is linked to the rule card it uses (no new card), rewritten in the
simple style with a new setting and all-new numbers, and given Theorem + Traditional Method + Specified Rule. Old keys that were wrong:
388 (M7, key on an empty option), 391 (M10, key on option e, no option held the answer), 400 (M19, key on option e, no option held
the answer), 401 (M20, key on 45:46 - the answer is 45:56). One folder per linked rule: misc/ruleNN/ (old rows only, no payload).
Usage: python gen_misc.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import place, popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_57_60 import gopts, r5859  # noqa: E402
from gen_69_72 import rsopts  # noqa: E402

CARD = {1: 253, 2: 254, 3: 255, 4: 256, 7: 259, 18: 270, 20: 272, 21: 273, 53: 304, 58: 309, 59: 310, 72: 323, 79: 330, 84: 335, 85: 336}


def res(kind, v, T, trad, rule, fin, rb, sc):
    return result((kind, v), T, steps(*trad), steps(*rule), fin, rb, sc)


# ---------------------------------------------------------------- builders (one per problem type)
def m_per_article(A, x, N, total):                       # M1, M4 -> Rule 58
    return r5859(58, F(A), F(x), "other", B=F(total) / N,
                 note=rf"The {N} articles are sold for Rs \({m(total)}\), i.e. Rs \({m(F(total) / N)}\) each.")


def m_successive(xs, paid=None, cost=None):              # M2, M16, M18 -> Rule 21 (successive reductions)
    T = (r"Two successive reductions of \(x\%\) and \(y\%\) are one reduction of<br>\[ \left(x+y-\frac{xy}{100}\right)\% \]"
         r"(apply it again for a third reduction).")
    xs = [F(t) for t in xs]
    left, comb = F(1), F(0)
    for t in xs:
        left *= (100 - t) / 100
    for t in xs:
        comb = comb + t - comb * t / 100
    chain = r"\times".join(rf"\frac{{{tex(100 - t)}}}{{100}}" for t in xs)
    rule = [("Identify the values.", ", ".join(rf"\({tex(t)}\%\)" for t in xs) + "."), ("Apply the specified rule.", T.split("<br>")[1])]
    comb_steps, c = [], xs[0]
    for t in xs[1:]:
        comb_steps.append(rf"\({tex(c)} + {tex(t)} - \frac{{{tex(c)}\times {tex(t)}}}{{100}} = {tex(c + t - c * t / 100)}\)")
        c = c + t - c * t / 100
    rule.append(("Combine the reductions.", "; ".join(comb_steps) + rf". Single reduction \(= {tex(comb)}\%\)."))
    if paid is not None:                                 # original price from the price paid
        P = F(paid)
        orig = P / left
        trad = [("Each reduction leaves a share of the price.", rf"Price paid \(= \text{{original}}\times {chain} = {tex(left)}\times\text{{original}}\)."),
                ("Original price.", rf"\[ {m(P)} \div {tex(left)} = {m(orig)} \]")]
        rule.append(("Original price.", rf"\[ {m(P)}\times\frac{{100}}{{{tex(100 - comb)}}} = {m(orig)} \]"))
        return res("number", orig, T, trad, rule, rf"Rs \({m(orig)}\)", [rf"Single reduction \(= {tex(comb)}\%\).", rf"Paid \(= {tex(100 - comb)}\%\) of the original.", rf"Original \(= {m(orig)}\)."],
                   rf"\[ {m(P)}\times\frac{{100}}{{{tex(100 - comb)}}} = {m(orig)} \]")
    if cost is not None:                                 # selling price after the reductions
        C = F(cost)
        sp = C * left
        trad = [("Apply the reductions one by one.", rf"\[ {m(C)}\times {chain} = {m(sp)} \]")]
        rule.append(("New selling price.", rf"\[ {m(C)}\times\frac{{{tex(100 - comb)}}}{{100}} = {m(sp)} \]"))
        return res("number", sp, T, trad, rule, rf"Rs \({m(sp)}\)", [rf"Single reduction \(= {tex(comb)}\%\).", rf"\({m(C)}\times {tex(100 - comb)}\%\).", rf"\(= {m(sp)}\)."],
                   rf"\[ {m(C)}\times\frac{{{tex(100 - comb)}}}{{100}} = {m(sp)} \]")
    trad = [("Take the price as 100.", rf"After the discounts: \(100\times {chain} = {tex(100 * left)}\)."),
            ("Single discount.", rf"\[ 100 - {tex(100 * left)} = {tex(100 - 100 * left)}\% \]")]
    return res("number", comb, T, trad, rule, PCT(comb), [rf"Combine two at a time.", rf"Result \(= {tex(comb)}\%\).", rf"Single discount \(= {tex(comb)}\%\)."],
               rf"\[ 100\left(1 - {chain}\right) = {tex(comb)}\% \]")


def m_overhead(n, rate, extra, mp, disc):                # M3 -> Rule 2
    T = r"Profit per cent is the profit on every 100 of the whole cost:<br>\[ \frac{\text{SP}-\text{CP}}{\text{CP}}\times 100\% \]"
    n, rate, extra, mp, disc = map(F, (n, rate, extra, mp, disc))
    cost = n * rate + extra
    sp = n * mp * (100 - disc) / 100
    v = (sp - cost) / cost * 100
    trad = [("Whole cost.", rf"\[ {tex(n)}\times {m(rate)} + {m(extra)} = {m(cost)} \]"),
            ("Takings after the discount.", rf"\[ {tex(n)}\times {m(mp)}\times\frac{{{tex(100 - disc)}}}{{100}} = {m(sp)} \]"),
            ("Profit per cent.", rf"\[ \frac{{{m(sp)} - {m(cost)}}}{{{m(cost)}}}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"CP \(= {m(cost)}\) (with the extra costs), SP \(= {m(sp)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{m(sp - cost)}}}{{{m(cost)}}}\times 100 = {tex(v)}\% \]")]
    return res("number", v, T, trad, rule, PCT(v), [rf"CP \(= {m(cost)}\).", rf"SP \(= {m(sp)}\).", rf"Profit \(= {tex(v)}\%\)."],
               rf"\[ \frac{{{m(sp - cost)}}}{{{m(cost)}}}\times 100 = {tex(v)}\% \]")


def m_two_items(a1, b1, S1, a2, b2, S2, A, B):            # M5 -> Rule 53 (two kinds of items, two equations)
    T = r"Two lots of two kinds of items with known totals give two equations; subtracting them leaves the difference asked for.<br>\[ a_1x+b_1y=S_1,\quad a_2x+b_2y=S_2 \]"
    a1, b1, S1, a2, b2, S2 = map(F, (a1, b1, S1, a2, b2, S2))
    det = a1 * b2 - a2 * b1
    x, y = (S1 * b2 - S2 * b1) / det, (a1 * S2 - a2 * S1) / det
    v = x - y
    trad = [("Write the two equations.", rf"\[ {tex(a1)}x + {tex(b1)}y = {m(S1)},\qquad {tex(a2)}x + {tex(b2)}y = {m(S2)} \]"),
            ("Solve.", rf"\[ x = {m(x)},\quad y = {m(y)} \]"),
            ("Difference.", rf"\[ {m(x)} - {m(y)} = {m(v)} \]")]
    rule = [("Identify the values.", rf"{A}: \(x\), {B}: \(y\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Subtract the equations.", rf"\[ ({tex(a1 - a2)})x + ({tex(b1 - b2)})y = {m(S1 - S2)} \;\Rightarrow\; x - y = {m(v)} \]")]
    return res("number", v, T, trad, rule, rf"Rs \({m(v)}\)", [rf"\(x = {m(x)}\), \(y = {m(y)}\).", rf"Subtract the equations.", rf"\(x - y = {m(v)}\)."],
               rf"\[ \frac{{{m(S1 - S2)}}}{{{tex(a1 - a2)}}} = {m(v)} \]")


def m_on_sp(x, k):                                       # M6 -> Rule 79
    T = r"If the profit is \(x\%\) of the selling price, the cost is \((100-x)\%\) of the selling price.<br>\[ \text{CP}=\frac{100-x}{100}\times\text{SP} \]"
    x, k = F(x), F(k)
    cp = 100 - x
    v = k * cp / 100
    trad = [("Take the selling price as 100.", rf"Profit \(= {tex(x)}\), cost \(= {tex(cp)}\)."), (f"{tex(k)}% of the cost.", rf"\[ \frac{{{tex(k)}}}{{100}}\times {tex(cp)} = {tex(v)} \]"),
            ("As a per cent of the selling price.", rf"It is \({tex(v)}\) out of \(100\), i.e. \({tex(v)}\%\).")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{tex(k)}}}{{100}}\times\frac{{{tex(cp)}}}{{100}}\times 100 = {tex(v)}\% \]")]
    return res("number", v, T, trad, rule, PCT(v), [rf"CP \(= {tex(cp)}\%\) of SP.", rf"\({tex(k)}\%\) of it.", rf"\(= {tex(v)}\%\) of SP."],
               rf"\[ \frac{{{tex(k)}\times {tex(cp)}}}{{100}} = {tex(v)}\% \]")


def m_resale(A, x, y):                                   # M7 -> Rule 59
    T = (r"If an article sold for Rs \(A\) gives a loss of \(x\%\), the price that would give a profit of \(y\%\) is"
         r"<br>\[ \frac{100+y}{100-x}\times A \]")
    A, x, y = map(F, (A, x, y))
    cp = A * 100 / (100 - x)
    price = cp * (100 + y) / 100
    g = price - A
    trad = [("First owner's cost.", rf"Rs \({m(A)}\) is \({tex(100 - x)}\%\) of it: \[ {m(A)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(cp)} \]"),
            ("Second sale price.", rf"\[ {m(cp)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(price)} \]"),
            ("Second owner's gain.", rf"He paid \({m(A)}\): gain \(= {m(price)} - {m(A)} = {m(g)}\).")]
    rule = [("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{tex(100 + y)}}}{{{tex(100 - x)}}}\times {m(A)} = {m(price)},\qquad {m(price)} - {m(A)} = {m(g)} \]")]
    return res("number", g, T, trad, rule, rf"Rs \({m(g)}\)", [rf"Cost \(= {m(cp)}\).", rf"Second price \(= {m(price)}\).", rf"Gain \(= {m(g)}\)."],
               rf"\[ \frac{{{tex(100 + y)}}}{{{tex(100 - x)}}}\times {m(A)} - {m(A)} = {m(g)} \]")


def m_equal_pl(hi, lo):                                  # M8 -> Rule 3
    T = r"If the profit at Rs \(S_1\) equals the loss at Rs \(S_2\), the cost is halfway between:<br>\[ \text{CP}=\frac{S_1+S_2}{2} \]"
    hi, lo = F(hi), F(lo)
    cp = (hi + lo) / 2
    trad = [("Let the cost be Rs \\(c\\).", rf"\[ {m(hi)} - c = c - {m(lo)} \;\Rightarrow\; 2c = {m(hi + lo)} \;\Rightarrow\; c = {m(cp)} \]")]
    rule = [("Identify the values.", rf"\(S_1 = {m(hi)}\), \(S_2 = {m(lo)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{m(hi)} + {m(lo)}}}{{2}} = {m(cp)} \]")]
    return res("number", cp, T, trad, rule, rf"Rs \({m(cp)}\)", [rf"\(S_1 + S_2 = {m(hi + lo)}\).", r"Half of it.", rf"CP \(= {m(cp)}\)."], rf"\[ \frac{{{m(hi + lo)}}}{{2}} = {m(cp)} \]")


def m_loss_eq_profit(S, p):                              # M15 -> Rule 3 (a loss at Rs S equals a p% profit)
    T = r"If the loss at Rs \(S\) equals the profit at \(p\%\), then the loss is also \(p\%\) of the cost:<br>\[ \text{CP}=\frac{100S}{100-p} \]"
    S, p = F(S), F(p)
    cp = S * 100 / (100 - p)
    trad = [("Let the cost be Rs \\(c\\).", rf"\[ c - {m(S)} = \frac{{{tex(p)}}}{{100}}c \;\Rightarrow\; \frac{{{tex(100 - p)}}}{{100}}c = {m(S)} \;\Rightarrow\; c = {m(cp)} \]")]
    rule = [("Identify the values.", rf"\(S = {m(S)}\), \(p = {tex(p)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{100\times {m(S)}}}{{{tex(100 - p)}}} = {m(cp)} \]")]
    return res("number", cp, T, trad, rule, rf"Rs \({m(cp)}\)", [rf"Loss \(= {tex(p)}\%\) of CP.", rf"Rs \({m(S)}\) is \({tex(100 - p)}\%\) of CP.", rf"CP \(= {m(cp)}\)."],
               rf"\[ \frac{{100\times {m(S)}}}{{{tex(100 - p)}}} = {m(cp)} \]")


def m_gain_minus_loss(g, D):                             # M9 -> Rule 20
    T = r"Going from a loss of \(x\%\) to a gain of \(y\%\) raises the price by \((x+y)\%\) of the cost:<br>\[ \text{CP}=\frac{100D}{x+y} \]"
    g, D = F(g), F(D)
    cp = D * 100 / (2 * g)
    trad = [("Let the cost be Rs \\(c\\).", rf"\[ \frac{{{tex(100 + g)}}}{{100}}c - \frac{{{tex(100 - g)}}}{{100}}c = {m(D)} \;\Rightarrow\; \frac{{{tex(2 * g)}}}{{100}}c = {m(D)} \;\Rightarrow\; c = {m(cp)} \]")]
    rule = [("Identify the values.", rf"\(x = y = {tex(g)}\), \(D = {m(D)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{100\times {m(D)}}}{{{tex(g)} + {tex(g)}}} = {m(cp)} \]")]
    return res("number", cp, T, trad, rule, rf"Rs \({m(cp)}\)", [rf"\(x + y = {tex(2 * g)}\).", rf"Rs \({m(D)}\) is \({tex(2 * g)}\%\) of CP.", rf"CP \(= {m(cp)}\)."],
               rf"\[ \frac{{100\times {m(D)}}}{{{tex(2 * g)}}} = {m(cp)} \]")


def m_mixture_pl(q1, r1, q2, r2, s):                     # M10 -> Rule 1 (signed rupees)
    T = r"Profit or loss in rupees is the selling price less the cost price:<br>\[ \text{Profit}=\text{SP}-\text{CP}\quad(\text{a loss if negative}) \]"
    q1, r1, q2, r2, s = map(F, (q1, r1, q2, r2, s))
    cost, sp = q1 * r1 + q2 * r2, (q1 + q2) * s
    v = sp - cost
    trad = [("Cost of the two lots.", rf"\[ {tex(q1)}\times {m(r1)} + {tex(q2)}\times {m(r2)} = {m(cost)} \]"), ("Takings.", rf"\[ {tex(q1 + q2)}\times {m(s)} = {m(sp)} \]"),
            ("Compare.", rf"\[ {m(sp)} - {m(cost)} = {m(v)} \]" + (" It is negative, so a loss." if v < 0 else ""))]
    rule = [("Identify the values.", rf"CP \(= {m(cost)}\), SP \(= {m(sp)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ {m(sp)} - {m(cost)} = {m(v)} \]")]
    fin = rf"a {'gain' if v > 0 else 'loss'} of Rs \({m(abs(v))}\)"
    return res("signed", v, T, trad, rule, fin, [rf"CP \(= {m(cost)}\).", rf"SP \(= {m(sp)}\).", rf"Result \(= {m(v)}\)."], rf"\[ {m(sp)} - {m(cost)} = {m(v)} \]")


def m_price_sales(up, down):                             # M11 -> Rule 18
    T = r"A rise of \(x\%\) followed by a fall of \(y\%\) is a change of<br>\[ \left(x-y-\frac{xy}{100}\right)\% \]an increase if positive, a decrease if negative."
    up, down = F(up), F(down)
    v = up - down - up * down / 100
    trad = [("Take the price as Re 1 and the sales as 100.", rf"Money taken \(= 100\)."),
            ("After the change.", rf"Price \(= {tex(1 + up / 100)}\), sales \(= {tex(100 - down)}\): money \(= {tex((1 + up / 100) * (100 - down))}\)."),
            ("Change.", rf"\[ {tex((1 + up / 100) * (100 - down))} - 100 = {tex(v)}\% \]" + (" It is negative, so a decrease." if v < 0 else ""))]
    rule = [("Identify the values.", rf"\(x = {tex(up)}\), \(y = {tex(down)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ {tex(up)} - {tex(down)} - \frac{{{tex(up)}\times {tex(down)}}}{{100}} = {tex(v)}\% \]")]
    fin = rf"a {'decrease' if v < 0 else 'increase'} of \({tex(abs(v))}\%\)"
    return res("signed", v, T, trad, rule, fin, [rf"\(\frac{{xy}}{{100}} = {tex(up * down / 100)}\).", rf"\({tex(up)} - {tex(down)} - {tex(up * down / 100)} = {tex(v)}\).", rf"Change \(= {tex(v)}\%\)."],
               rf"\[ {tex(up)} - {tex(down)} - {tex(up * down / 100)} = {tex(v)}\% \]")


def idopts(v):
    v = F(v)
    s = abs(v)
    w, o = ("Increase", "Decrease") if v > 0 else ("Decrease", "Increase")
    return place(rf"{w} of \({tex(s)}\%\)", [rf"{o} of \({tex(s)}\%\)", rf"{w} of \({tex(s + 2)}\%\)", r"No change"])


def m_sell_count(k, rs, each, profit):                   # M12 -> Rule 7
    T = r"Buying \(a\) for Rs \(b\) and selling \(c\) for Rs \(d\), the profit on one article is<br>\[ \frac{d}{c}-\frac{b}{a} \]"
    k, rs, each, profit = map(F, (k, rs, each, profit))
    per = each - rs / k
    n = profit / per
    trad = [("Profit on one.", rf"Cost of one \(= \frac{{{m(rs)}}}{{{tex(k)}}} = {m(rs / k)}\); it sells for \({m(each)}\): profit \(= {m(per)}\)."),
            ("Number for the profit.", rf"\[ {m(profit)} \div {m(per)} = {tex(n)} \]")]
    rule = [("Identify the values.", rf"\(a = {tex(k)}\), \(b = {m(rs)}\), \(c = 1\), \(d = {m(each)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ {m(each)} - \frac{{{m(rs)}}}{{{tex(k)}}} = {m(per)},\qquad \frac{{{m(profit)}}}{{{m(per)}}} = {tex(n)} \]")]
    return res("number", n, T, trad, rule, rf"\({tex(n)}\)", [rf"Profit on one \(= {m(per)}\).", rf"\({m(profit)} \div {m(per)}\).", rf"\(= {tex(n)}\)."],
               rf"\[ \frac{{{m(profit)}}}{{{m(per)}}} = {tex(n)} \]")


def m_frac_cost(f, up):                                  # M13 -> Rule 2
    T = r"Profit per cent is the profit on every 100 of cost:<br>\[ \frac{\text{SP}-\text{CP}}{\text{CP}}\times 100\% \]"
    f, up = F(f), F(up)
    cp, sp = 100 * f, 100 + up
    v = (sp - cp) / cp * 100
    trad = [("Take the usual selling price as 100.", rf"He pays \({tex(f)}\times 100 = {tex(cp)}\) and sells for \({tex(sp)}\)."),
            ("Gain per cent.", rf"\[ \frac{{{tex(sp)} - {tex(cp)}}}{{{tex(cp)}}}\times 100 = {tex(v)}\% \]")]
    rule = [("Identify the values.", rf"CP \(= {tex(cp)}\), SP \(= {tex(sp)}\) (on a usual price of 100)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{tex(sp - cp)}}}{{{tex(cp)}}}\times 100 = {tex(v)}\% \]")]
    return res("number", v, T, trad, rule, PCT(v), [rf"CP \(= {tex(cp)}\).", rf"SP \(= {tex(sp)}\).", rf"Gain \(= {tex(v)}\%\)."], rf"\[ \frac{{{tex(sp - cp)}}}{{{tex(cp)}}}\times 100 = {tex(v)}\% \]")


def m_mixture_price(q1, r1, q2, r2, g):                  # M14 -> Rule 2
    T = r"For a profit of \(g\%\) the selling price is \((100+g)\%\) of the cost:<br>\[ \text{SP}=\frac{100+g}{100}\times\text{CP} \]"
    q1, r1, q2, r2, g = map(F, (q1, r1, q2, r2, g))
    cost = q1 * r1 + q2 * r2
    per = cost / (q1 + q2)
    sp = per * (100 + g) / 100
    trad = [("Cost of the mixture.", rf"\[ {tex(q1)}\times {m(r1)} + {tex(q2)}\times {m(r2)} = {m(cost)} \text{{ for }} {tex(q1 + q2)} \text{{ kg}} \]"),
            ("Cost of 1 kg.", rf"\[ {m(cost)} \div {tex(q1 + q2)} = {m(per)} \]"), ("Price for the gain.", rf"\[ {m(per)}\times\frac{{{tex(100 + g)}}}{{100}} = {m(sp)} \]")]
    rule = [("Identify the values.", rf"CP \(= {m(per)}\) a kg, \(g = {tex(g)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{tex(100 + g)}}}{{100}}\times {m(per)} = {m(sp)} \]")]
    return res("number", sp, T, trad, rule, rf"Rs \({m(sp)}\) a kg", [rf"CP \(= {m(per)}\) a kg.", rf"\(\times\frac{{{tex(100 + g)}}}{{100}}\).", rf"\(= {m(sp)}\) a kg."],
               rf"\[ \frac{{{tex(100 + g)}}}{{100}}\times {m(per)} = {m(sp)} \]")


def m_disc_amount(x, S, y):                              # M17 -> Rule 85
    T = r"If an article is bought at \(x\%\) below its marked price, the price paid is \((100-x)\%\) of the marked price:<br>\[ \text{MP}=\frac{100\times\text{paid}}{100-x} \]"
    x, S, y = map(F, (x, S, y))
    cp = S * 100 / (100 + y)
    mp = cp * 100 / (100 - x)
    d = mp - cp
    trad = [("Cost to the dealer.", rf"He sells for \({m(S)}\) at \({tex(y)}\%\) profit: cost \(= {m(S)}\times\frac{{100}}{{{tex(100 + y)}}} = {m(cp)}\)."),
            ("Marked price.", rf"\[ {m(cp)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(mp)} \]"), ("Discount he got.", rf"\[ {m(mp)} - {m(cp)} = {m(d)} \]")]
    rule = [("Identify the values.", rf"paid \(= {m(cp)}\), \(x = {tex(x)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{100\times {m(cp)}}}{{{tex(100 - x)}}} = {m(mp)},\qquad \frac{{{tex(x)}}}{{100}}\times {m(mp)} = {m(d)} \]")]
    return res("number", d, T, trad, rule, rf"Rs \({m(d)}\)", [rf"Paid \(= {m(cp)}\).", rf"MP \(= {m(mp)}\).", rf"Discount \(= {m(d)}\)."], rf"\[ {m(mp)} - {m(cp)} = {m(d)} \]")


def m_two_discounts(d1, d2, D):                          # M19 -> Rule 72
    T = r"A change from a discount of \(x_1\%\) to \(x_2\%\) changes the selling price, and so the profit, by \((x_2-x_1)\%\) of the marked price.<br>\[ \text{MP}=\frac{100D}{x_2-x_1} \]"
    d1, d2, D = map(F, (d1, d2, D))
    mp = D * 100 / (d2 - d1)
    trad = [("Let the marked price be Rs \\(M\\).", rf"Prices: \(\frac{{{tex(100 - d1)}}}{{100}}M\) and \(\frac{{{tex(100 - d2)}}}{{100}}M\); the cost is the same, so the profits differ by the gap."),
            ("Solve.", rf"\[ \frac{{{tex(d2 - d1)}}}{{100}}M = {m(D)} \;\Rightarrow\; M = {m(mp)} \]")]
    rule = [("Identify the values.", rf"\(x_1 = {tex(d1)}\), \(x_2 = {tex(d2)}\), \(D = {m(D)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{100\times {m(D)}}}{{{tex(d2 - d1)}}} = {m(mp)} \]")]
    return res("number", mp, T, trad, rule, rf"Rs \({m(mp)}\)", [rf"\(x_2 - x_1 = {tex(d2 - d1)}\).", rf"Rs \({m(D)}\) is \({tex(d2 - d1)}\%\) of MP.", rf"MP \(= {m(mp)}\)."],
               rf"\[ \frac{{100\times {m(D)}}}{{{tex(d2 - d1)}}} = {m(mp)} \]")


def m_ratio_cp_mp(y, x):                                 # M20 -> Rule 84 (ratio answer)
    T = r"Marked price \(A\), discount \(x\%\), gain \(y\%\) on the cost \(B\):<br>\[ A(100-x)=B(100+y) \]"
    y, x = F(y), F(x)
    r = (100 - x) / (100 + y)                            # B / A
    a, b = r.numerator, r.denominator
    trad = [("Take the printed price as 100.", rf"After \({tex(x)}\%\) off it sells for \({tex(100 - x)}\), which is \({tex(100 + y)}\%\) of the cost."),
            ("Cost.", rf"\[ {tex(100 - x)}\times\frac{{100}}{{{tex(100 + y)}}} = {tex(100 * r)} \]"), ("Ratio.", rf"\[ {tex(100 * r)} : 100 = {a} : {b} \]")]
    rule = [("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{B}}{{A}} = \frac{{100 - x}}{{100 + y}} = \frac{{{tex(100 - x)}}}{{{tex(100 + y)}}} = \frac{{{a}}}{{{b}}} \]")]
    return res("ratio", (a, b), T, trad, rule, rf"\({a} : {b}\)", [rf"\(\frac{{B}}{{A}} = \frac{{{tex(100 - x)}}}{{{tex(100 + y)}}}\).", rf"\(= \frac{{{a}}}{{{b}}}\).", rf"CP : printed price \(= {a} : {b}\)."],
               rf"\[ \frac{{{tex(100 - x)}}}{{{tex(100 + y)}}} = \frac{{{a}}}{{{b}}} \]")


def ratio_opts(g):
    a, b = g["answer"][1]
    Q = lambda p, q: rf"\({p} : {q}\)"
    return place(Q(a, b), [Q(b, a), Q(a + 1, b), Q(a, b + 2)])


def m_saved_more(d1, d2, D):                             # M21 -> Rule 84
    T = r"Marked price \(A\), discount \(x\%\): the price paid is<br>\[ \frac{A(100-x)}{100} \]"
    d1, d2, D = map(F, (d1, d2, D))
    lp = D * 100 / (d2 - d1)
    paid = lp * (100 - d1) / 100
    trad = [("The extra saving.", rf"The two discounts differ by \({tex(d2 - d1)}\%\) of the labelled price, which is Rs \({m(D)}\): labelled price \(= {m(lp)}\)."),
            ("Price paid.", rf"\[ {m(lp)}\times\frac{{{tex(100 - d1)}}}{{100}} = {m(paid)} \]")]
    rule = [("Identify the values.", rf"\(A = {m(lp)}\), \(x = {tex(d1)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{m(lp)}\times {tex(100 - d1)}}}{{100}} = {m(paid)} \]")]
    return res("number", paid, T, trad, rule, rf"Rs \({m(paid)}\)", [rf"Labelled price \(= {m(lp)}\).", rf"\(\times\frac{{{tex(100 - d1)}}}{{100}}\).", rf"Paid \(= {m(paid)}\)."],
               rf"\[ \frac{{100\times {m(D)}}}{{{tex(d2 - d1)}}}\times\frac{{{tex(100 - d1)}}}{{100}} = {m(paid)} \]")


def m_price_cut(c, more, R, k):                          # M22 -> Rule 4
    T = r"If a cut of \(c\%\) in the price lets Rs \(R\) buy \(n\) more, the new price of one is<br>\[ \frac{cR}{100n} \]"
    c, more, R, k = map(F, (c, more, R, k))
    new = c * R / (100 * more)
    old = new * 100 / (100 - c)
    v = old * k
    trad = [("The saving buys the extra items.", rf"The cut saves \({tex(c)}\%\) of Rs \({m(R)}\) = Rs \({m(c * R / 100)}\), which buys \({tex(more)}\) more: new price \(= {m(new)}\) each."),
            ("Old price.", rf"\[ {m(new)}\times\frac{{100}}{{{tex(100 - c)}}} = {m(old)} \]"), (f"Price of {tex(k)} before the cut.", rf"\[ {tex(k)}\times {m(old)} = {m(v)} \]")]
    rule = [("Identify the values.", rf"\(c = {tex(c)}\), \(R = {m(R)}\), \(n = {tex(more)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
            ("Substitute the values.", rf"\[ \frac{{{tex(c)}\times {m(R)}}}{{100\times {tex(more)}}} = {m(new)},\qquad {tex(k)}\times\frac{{{m(new)}\times 100}}{{{tex(100 - c)}}} = {m(v)} \]")]
    return res("number", v, T, trad, rule, rf"Rs \({m(v)}\)", [rf"New price \(= {m(new)}\).", rf"Old price \(= {m(old)}\).", rf"{tex(k)} items \(= {m(v)}\)."],
               rf"\[ {tex(k)}\times\frac{{{m(new)}\times 100}}{{{tex(100 - c)}}} = {m(v)} \]")


# ---------------------------------------------------------------- the 23 rows: rule, question, builder, options
ROWS = {
    382: (58, "A shop sells a lamp for Rs 450 at a profit of 20%. What is its gain or loss per cent if it sells 8 such lamps for Rs 3240 in all?",
          lambda: m_per_article(450, 20, 8, 3240), "gain"),
    383: (21, "A store gives 25% off the price of a jacket and then a further 10% off the reduced price. If Meena paid Rs 1350, what was the original price?",
          lambda: m_successive([25, 10], paid=1350), "rs"),
    384: (2, "A trader buys 120 fans at Rs 900 each and spends Rs 12000 on carriage. He marks each fan at Rs 1250 and gives a discount of 4%. What is his profit per cent?",
          lambda: m_overhead(120, 900, 12000, 1250, 4), "pct"),
    385: (58, "A dealer sells a table for Rs 1320 at a profit of 10%. What is his gain or loss per cent if he sells 7 such tables at Rs 1164 each?",
          lambda: m_per_article(1320, 10, 7, 7 * 1164), "gain"),
    386: (53, "5 cups and 2 plates cost Rs 450, and 2 cups and 5 plates cost Rs 390. How much more does a cup cost than a plate?",
          lambda: m_two_items(5, 2, 450, 2, 5, 390, "cup", "plate"), "rs"),
    387: (79, "A shop's profit is 20% of the selling price. What per cent of the selling price is 45% of the cost price?",
          lambda: m_on_sp(20, 45), "pct"),
    388: (59, "P sells a scooter to Q for Rs 13600 at a loss of 15%. Q then sells it to R at a price that would have given P a profit of 12%. Find Q's gain.",
          lambda: m_resale(13600, 15, 12), "rs"),
    389: (3, "The profit on selling a fan for Rs 1180 equals the loss on selling it for Rs 940. Find its cost price.",
          lambda: m_equal_pl(1180, 940), "rs"),
    390: (20, "Selling a book at a gain of 15% brings in Rs 9 more than selling it at a loss of 15%. Find the cost price of the book.",
          lambda: m_gain_minus_loss(15, 9), "rs"),
    391: (1, "Ravi buys 40 kg of dal at Rs 52 a kg and 60 kg at Rs 58 a kg, mixes them and sells the mixture at Rs 54 a kg. What is his gain or loss?",
          lambda: m_mixture_pl(40, 52, 60, 58, 54), "rsgain"),
    392: (18, "The price of a heater is raised by 20% and its sales fall by 20%. What is the effect on the money taken from its sales?",
          lambda: m_price_sales(20, 20), "incdec"),
    393: (7, "A girl buys pencils at 6 for Rs 3 and sells them at Rs 1 each. How many must she sell to make a profit of Rs 13?",
          lambda: m_sell_count(6, 3, 1, 13), "count"),
    394: (2, r"Mohan buys a camera for \(\frac{2}{3}\) of its selling price and sells it at 12% more than that selling price. What is his gain per cent?",
          lambda: m_frac_cost(F(2, 3), 12), "pct"),
    395: (2, "At what price per kg must a shop sell a mixture of 60 kg of tea at Rs 150 a kg and 40 kg at Rs 175 a kg to gain 12%?",
          lambda: m_mixture_price(60, 150, 40, 175, 12), "rs"),
    396: (3, "The loss on selling a radio for Rs 570 is the same as the profit it makes when it is sold at a profit of 25%. Find its cost price.",
          lambda: m_loss_eq_profit(570, 25), "rs"),
    397: (21, "A bag costing Rs 800 is sold at a loss of 15%. If the price is cut by a further 6%, what is the new selling price?",
          lambda: m_successive([15, 6], cost=800), "rs"),
    398: (85, "A dealer buys a printer at 12% off its marked price and sells it for Rs 5544, making a profit of 26%. How much discount did he get?",
          lambda: m_disc_amount(12, 5544, 26), "rs"),
    399: (21, "Successive discounts of 12%, 15% and 34% are equal to what single discount?",
          lambda: m_successive([12, 15, 34]), "pct"),
    400: (72, "A shop gives a discount of 8% on a clock. If it gave 12% instead, its profit would be Rs 36 less. Find the marked price of the clock.",
          lambda: m_two_discounts(8, 12, 36), "rs"),
    401: (84, "A shop makes a profit of 25% after giving a discount of 20% on the printed price of a book. Find the ratio of the cost price to the printed price.",
          lambda: m_ratio_cp_mp(25, 20), "ratio"),
    402: (84, "Anu bought a fridge at 10% off its labelled price. With a 15% discount she would have saved Rs 900 more. How much did she pay for it?",
          lambda: m_saved_more(10, 15, 900), "rs"),
    403: (4, "A 40% cut in the price of eggs lets a woman buy 9 more eggs for Rs 27. What was the price of 8 eggs before the cut?",
          lambda: m_price_cut(40, 9, 27, 8), "rs"),
    404: (59, "A grocer would lose 4% by selling sugar at Rs 43.20 a kg. At what price per kg should she sell it to gain 25%?",
          lambda: r5859(59, F("43.20"), F(4), "newsp", y=F(25), per="a kg"), "rs"),
}


def count_opts(g):
    v = F(g["answer"][1])
    return place(rf"\({tex(v)}\)", [rf"\({tex(w)}\)" for w in (v + 10, v - 10, 2 * v)])


OPTS = {"gain": lambda g: gopts(g["answer"][1]), "rs": lambda g: ropts(g["answer"][1]), "pct": lambda g: popts(g["answer"][1]),
        "rsgain": lambda g: rsopts(g["answer"][1]), "incdec": lambda g: idopts(g["answer"][1]), "count": count_opts, "ratio": ratio_opts}


def main():
    by_rule = {}
    for rid, (rule, q, fn, ok) in ROWS.items():
        by_rule.setdefault(rule, []).append(rid)
    for rule, ids in sorted(by_rule.items()):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"]["id"] == CARD[rule], (rule, dump["rule_card"]["id"])
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(ids), (rule, sorted(rows), ids)
        out = []
        for rid in ids:
            _, q, fn, ok = ROWS[rid]
            g = fn()
            op, _ = OPTS[ok](g)
            extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, CARD[rule], extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"misc rule {rule}: rows {ids}")


if __name__ == "__main__":
    main()
