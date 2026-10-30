"""Profit and Loss Rules 1-3 (2026-10-30): writes the three rule cards (the chapter had none), regenerates every old row in the
prompt #14 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links it to its card and, as
every old row copies a book example or exercise, gives it a sentence in the book's simple style with the setting changed and
all-new numbers (the owner's rewording rule; checked with gate_check.py). The seven old duplicate pairs (282/917, 283/918,
284/919, 285/920, 286/924, 287/923, 288/925) get different numbers. Adds the book exercises that had no copy as one JsonImport
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


def Rs(v):
    return rf"Rs \({money(F(v))}\)"


def SP_(word, v, rs=False):
    """Signed option: 'Profit of 15%' / 'Loss of Rs 28'."""
    return f"{word} of " + (Rs(v) if rs else P(v))


def m(v):
    return money(F(v))


# ---------------------------------------------------------------- Rule 1: profit or loss in rupees
T1 = (r"When the selling price is more than the cost price there is a profit, and when it is less there is a loss:<br>"
      r"\[ \text{Profit}=\text{SP}-\text{CP},\qquad \text{Loss}=\text{CP}-\text{SP} \]")


def r1(cp, sp, who="he", signed=False):
    cp, sp = F(cp), F(sp)
    v = sp - cp
    word = "profit" if v > 0 else "loss"
    size = abs(v)
    trad = steps(
        ("Compare what was paid with what was received.", rf"Paid Rs \({m(cp)}\) and received Rs \({m(sp)}\), so the money received is "
                                                          + ("more" if v > 0 else "less") + rf" than the money paid: {who} makes a {word}."),
        ("Count the difference.", rf"\[ {m(max(cp, sp))} - {m(min(cp, sp))} = {m(size)} \]"))
    formula = r"\text{Profit}=\text{SP}-\text{CP}" if v > 0 else r"\text{Loss}=\text{CP}-\text{SP}"
    rule = steps(
        ("Identify the values.", rf"\(\text{{CP}} = {m(cp)}\), \(\text{{SP}} = {m(sp)}\); SP is " + ("more" if v > 0 else "less") + " than CP."),
        ("Apply the specified rule.", rf"\[ {formula} \]"),
        ("Substitute the values.", rf"\[ {m(max(cp, sp))} - {m(min(cp, sp))} = {m(size)} \]"))
    fin = rf"a {word} of Rs \({m(size)}\)" if signed else rf"Rs \({m(size)}\)"
    rb = [rf"\(\text{{CP}} = {m(cp)}\), \(\text{{SP}} = {m(sp)}\).", rf"\({formula}\).", rf"\({m(max(cp, sp))} - {m(min(cp, sp))} = {m(size)}\)."]
    sc = rf"\[ {m(max(cp, sp))} - {m(min(cp, sp))} = {m(size)} \]"
    return result(("signed", v) if signed else ("number", size), T1, trad, rule, fin, rb, sc)


T1B = (r"Profit \(=\) SP \(-\) CP. If selling for Rs \(a\) gives twice the profit of selling for Rs \(b\), then<br>"
       r"\[ a-\text{CP}=2(b-\text{CP})\;\Rightarrow\;\text{CP}=2b-a \]")


def r1_double(hi, lo):
    hi, lo = F(hi), F(lo)
    cp = 2 * lo - hi
    trad = steps(
        ("Write the two profits.", rf"Let the cost be Rs \(x\). Selling for Rs \({m(hi)}\) gives a profit of \({m(hi)} - x\); selling for Rs \({m(lo)}\) gives \({m(lo)} - x\)."),
        ("Use 'twice'.", rf"\[ {m(hi)} - x = 2({m(lo)} - x) \;\Rightarrow\; {m(hi)} - x = {m(2 * lo)} - 2x \;\Rightarrow\; x = {m(cp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(a = {m(hi)}\), \(b = {m(lo)}\)."),
        ("Apply the specified rule.", r"\[ \text{CP}=2b-a \]"),
        ("Substitute the values.", rf"\[ 2\times {m(lo)} - {m(hi)} = {m(cp)} \]"))
    rb = [rf"\(a = {m(hi)}\), \(b = {m(lo)}\).", r"\(\text{CP} = 2b - a\).", rf"\(2\times {m(lo)} - {m(hi)} = {m(cp)}\)."]
    return result(("number", cp), T1B, trad, rule, Rs(cp), rb, rf"\[ 2\times {m(lo)} - {m(hi)} = {m(cp)} \]")


# ---------------------------------------------------------------- Rule 2: gain or loss per cent (on the cost)
T2 = (r"Profit and loss per cent are always reckoned on the cost price:<br>"
      r"\[ \text{Gain or Loss per cent}=\frac{\text{Gain or Loss}}{\text{CP}}\times 100 \]")


def pct_core(cp, sp, signed, cost_lines, sale_lines):
    cp, sp = F(cp), F(sp)
    v = sp - cp
    pct = v / cp * 100
    word = "gain" if v > 0 else "loss"
    trad = steps(*(cost_lines + sale_lines + [
        (f"Find the {word}.", rf"\[ {m(max(cp, sp))} - {m(min(cp, sp))} = {m(abs(v))} \]"),
        ("Scale it to Rs 100 of cost.", rf"On Rs \({m(cp)}\) of cost the {word} is Rs \({m(abs(v))}\), so on Rs \(100\) it is "
                                       rf"\[ \frac{{{m(abs(v))}}}{{{m(cp)}}}\times 100 = {tex(abs(pct))} \]")]))
    rule = steps(
        ("Identify the values.", rf"{word.capitalize()} \(= {m(abs(v))}\), \(\text{{CP}} = {m(cp)}\)."),
        ("Apply the specified rule.", rf"\[ \text{{{word.capitalize()} per cent}}=\frac{{\text{{{word.capitalize()}}}}}{{\text{{CP}}}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{m(abs(v))}}}{{{m(cp)}}}\times 100 = {tex(abs(pct))}\% \]"))
    fin = rf"a {word} of \({tex(abs(pct))}\%\)" if signed else rf"\({tex(abs(pct))}\%\)"
    rb = [rf"{word.capitalize()} \(= {m(abs(v))}\), \(\text{{CP}} = {m(cp)}\).", rf"{word.capitalize()} \(\% = \frac{{\text{{{word}}}}}{{\text{{CP}}}}\times 100\).",
          rf"\(\frac{{{m(abs(v))}}}{{{m(cp)}}}\times 100 = {tex(abs(pct))}\%\)."]
    sc = rf"\[ \frac{{{m(abs(v))}}}{{{m(cp)}}}\times 100 = {tex(abs(pct))}\% \]"
    return result(("signed", pct) if signed else ("number", abs(pct)), T2, trad, rule, fin, rb, sc)


def r2(cp, sp, signed=False):
    return pct_core(cp, sp, signed, [], [])


def r2_extra(buy, extra, extra_what, sp, signed=True):
    cp = F(buy) + F(extra)
    return pct_core(cp, sp, signed, [("Add up the whole cost.", rf"Price paid \(+\) {extra_what} \(= {m(buy)} + {m(extra)} = {m(cp)}\).")], [])


def r2_dozens(doz, rate, extra, each, signed=False):
    cp = F(doz) * rate + extra
    n = 12 * doz
    sp = F(n) * F(each)
    cost = rf"\({doz}\) dozen at Rs \({m(rate)}\) a dozen \(= {m(F(doz) * rate)}\)" + (rf", plus Rs \({m(extra)}\) \(= {m(cp)}\)" if extra else "")
    return pct_core(cp, sp, signed, [("Find the total cost.", cost + ".")],
                    [("Find the total selling price.", rf"\({doz}\times 12 = {n}\) pieces at Rs \({m(each)}\) each \(= {m(sp)}\).")])


def r2_each(n, total, each):
    sp = F(n) * F(each)
    return pct_core(total, sp, False, [("Cost of all the articles.", rf"\({n}\) articles cost Rs \({m(total)}\).")],
                    [("Selling price of all the articles.", rf"\({n}\times {m(each)} = {m(sp)}\).")])


def r2_rates(a_n, a_rs, b_n, b_rs):
    """Buys a_n for Rs a_rs, sells b_n for Rs b_rs: compare on the LCM of the counts."""
    from math import lcm
    L = lcm(a_n, b_n)
    cp, sp = F(a_rs) * L / a_n, F(b_rs) * L / b_n
    return pct_core(cp, sp, False, [("Take a convenient number of articles.", rf"Take \({L}\) articles (a multiple of \({a_n}\) and \({b_n}\)). "
                                     rf"They cost \(\frac{{{L}}}{{{a_n}}}\times {m(a_rs)} = {m(cp)}\).")],
                    [("Selling price of the same articles.", rf"They sell for \(\frac{{{L}}}{{{b_n}}}\times {m(b_rs)} = {m(sp)}\).")])


def r2_sp_of(N, k):
    """By selling N articles the gain equals the selling price of k of them."""
    s = F(1)                                     # take the selling price of one article as Rs 1
    sp, gain = N * s, k * s
    cp = sp - gain
    return pct_core(cp, sp, False, [("Take the selling price of one article as Rs 1.", rf"\({N}\) articles sell for Rs \({N}\); the gain is the price of \({k}\) of them, Rs \({k}\), "
                                     rf"so the cost is \({N} - {k} = {N - k}\).")], [])


T2B = (r"Going back from the selling price to the cost price (the per cent is on the cost):<br>"
       r"\[ \text{CP}=\text{SP}\times\frac{100}{100+\text{gain}\%}\qquad\text{or}\qquad \text{CP}=\text{SP}\times\frac{100}{100-\text{loss}\%} \]")


def r2_back(sp, pct, loss=True):
    sp, pct = F(sp), F(pct)
    k = 100 - pct if loss else 100 + pct
    cp = sp * 100 / k
    word = "loss" if loss else "gain"
    trad = steps(
        ("Take the cost price as Rs 100.", rf"With a {word} of \({tex(pct)}\%\) the selling price is Rs \({tex(k)}\)."),
        ("Scale to the real selling price.", rf"Rs \({tex(k)}\) of selling price comes from Rs \(100\) of cost, so Rs \({m(sp)}\) comes from "
                                            rf"\[ \frac{{{m(sp)}}}{{{tex(k)}}}\times 100 = {m(cp)} \]"))
    sign = "-" if loss else "+"
    rule = steps(
        ("Identify the values.", rf"\(\text{{SP}} = {m(sp)}\), {word} \(= {tex(pct)}\%\)."),
        ("Apply the specified rule.", rf"\[ \text{{CP}}=\text{{SP}}\times\frac{{100}}{{100{sign}\text{{{word}}}\%}} \]"),
        ("Substitute the values.", rf"\[ {m(sp)}\times\frac{{100}}{{{tex(k)}}} = {m(cp)} \]"))
    rb = [rf"\(\text{{SP}} = {m(sp)}\), {word} \(= {tex(pct)}\%\).", rf"\(\text{{CP}} = \text{{SP}}\times\frac{{100}}{{100{sign}{tex(pct)}}}\).", rf"\({m(sp)}\times\frac{{100}}{{{tex(k)}}} = {m(cp)}\)."]
    return result(("number", cp), T2B, trad, rule, Rs(cp), rb, rf"\[ {m(sp)}\times\frac{{100}}{{{tex(k)}}} = {m(cp)} \]")


T2C = (r"To gain \(g\%\), the selling price is the whole cost price increased by \(g\%\) (the per cent is on the cost):<br>"
       r"\[ \text{SP}=\text{CP}\times\frac{100+g}{100} \]")


def r2_sell(n, rate, extras, g, unit):
    """n units at Rs rate each plus extra costs [(what, Rs)]; selling price of one unit for a gain of g%."""
    base = F(n) * rate
    cp = base + sum(F(v) for _, v in extras)
    one = cp / n
    sp = one * (100 + F(g)) / 100
    parts = " + ".join([m(base)] + [m(v) for _, v in extras])
    trad = steps(
        ("Add up the whole cost.", rf"\({n}\) {unit}s at Rs \({m(rate)}\) \(= {m(base)}\); with " + " and ".join(w for w, _ in extras)
                                   + rf" the cost is \({parts} = {m(cp)}\)."),
        (f"Cost of one {unit}.", rf"\[ \frac{{{m(cp)}}}{{{n}}} = {m(one)} \]"),
        (f"Add the {tex(F(g))}% gain.", rf"\[ {m(one)} + \frac{{{tex(F(g))}}}{{100}}\times {m(one)} = {m(sp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(\text{{CP}}\) of one {unit} \(= {m(one)}\), \(g = {tex(F(g))}\)."),
        ("Apply the specified rule.", r"\[ \text{SP}=\text{CP}\times\frac{100+g}{100} \]"),
        ("Substitute the values.", rf"\[ {m(one)}\times\frac{{{tex(100 + F(g))}}}{{100}} = {m(sp)} \]"))
    rb = [rf"CP of one {unit} \(= \frac{{{m(cp)}}}{{{n}}} = {m(one)}\).", r"\(\text{SP} = \text{CP}\times\frac{100+g}{100}\).",
          rf"\({m(one)}\times\frac{{{tex(100 + F(g))}}}{{100}} = {m(sp)}\)."]
    return result(("number", sp), T2C, trad, rule, Rs(sp), rb, rf"\[ \frac{{{m(cp)}}}{{{n}}}\times\frac{{{tex(100 + F(g))}}}{{100}} = {m(sp)} \]")


T2D = (r"A discount per cent is reckoned on the marked price:<br>"
       r"\[ \text{Discount per cent}=\frac{\text{MP}-\text{SP}}{\text{MP}}\times 100 \]")


def r2_disc(mp, sp):
    mp, sp = F(mp), F(sp)
    d = (mp - sp) / mp * 100
    trad = steps(
        ("Find the discount in rupees.", rf"\[ {m(mp)} - {m(sp)} = {m(mp - sp)} \]"),
        ("Scale it to Rs 100 of marked price.", rf"\[ \frac{{{m(mp - sp)}}}{{{m(mp)}}}\times 100 = {tex(d)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(\text{{MP}} = {m(mp)}\), \(\text{{SP}} = {m(sp)}\)."),
        ("Apply the specified rule.", r"\[ \text{Discount per cent}=\frac{\text{MP}-\text{SP}}{\text{MP}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{m(mp)} - {m(sp)}}}{{{m(mp)}}}\times 100 = {tex(d)}\% \]"))
    rb = [rf"\(\text{{MP}} = {m(mp)}\), \(\text{{SP}} = {m(sp)}\).", r"Discount \(\% = \frac{\text{MP}-\text{SP}}{\text{MP}}\times 100\).",
          rf"\(\frac{{{m(mp - sp)}}}{{{m(mp)}}}\times 100 = {tex(d)}\%\)."]
    return result(("number", d), T2D, trad, rule, P(d), rb, rf"\[ \frac{{{m(mp - sp)}}}{{{m(mp)}}}\times 100 = {tex(d)}\% \]")


# ---------------------------------------------------------------- Rule 3: equal profit and loss, then sell at z% profit
T3 = (r"If the profit made by selling an article for Rs \(x\) equals the loss made by selling it for Rs \(y\), then to make a profit of "
      r"\(z\%\) the article should be sold for<br>\[ \text{Rs }\frac{(x+y)(100+z)}{200} \]")


def r3(x, y, z):
    x, y, z = F(x), F(y), F(z)
    cp = (x + y) / 2
    sp = cp * (100 + z) / 100
    trad = steps(
        ("Let the cost price be Rs \\(c\\).", rf"Profit at Rs \({m(x)}\) is \({m(x)} - c\); loss at Rs \({m(y)}\) is \(c - {m(y)}\)."),
        ("They are equal.", rf"\[ {m(x)} - c = c - {m(y)} \;\Rightarrow\; 2c = {m(x + y)} \;\Rightarrow\; c = {m(cp)} \]"),
        (f"Add the {tex(z)}% profit.", rf"\[ {m(cp)}\times\frac{{{tex(100 + z)}}}{{100}} = {m(sp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {m(x)}\), \(y = {m(y)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", r"\[ \frac{(x+y)(100+z)}{200} \]"),
        ("Substitute the values.", rf"\[ \frac{{({m(x)} + {m(y)})({tex(100 + z)})}}{{200}} = \frac{{{m(x + y)}\times {tex(100 + z)}}}{{200}} = {m(sp)} \]"))
    rb = [rf"\(x = {m(x)}\), \(y = {m(y)}\), \(z = {tex(z)}\).", r"SP \(= \frac{(x+y)(100+z)}{200}\).", rf"\(\frac{{{m(x + y)}\times {tex(100 + z)}}}{{200}} = {m(sp)}\)."]
    return result(("number", sp), T3, trad, rule, Rs(sp), rb, rf"\[ \frac{{{m(x + y)}\times {tex(100 + z)}}}{{200}} = {m(sp)} \]")


# ---------------------------------------------------------------- rule cards
CARDS = {
    1: card(1, "Profit or Loss from the Cost Price and the Selling Price",
            r"When an article is sold for more than it cost there is a profit, and when it is sold for less there is a loss. The profit or "
            r"loss is the difference of the two prices.",
            r"\[ \text{Profit}=\text{SP}-\text{CP}\ (\text{SP}\gt\text{CP}),\qquad \text{Loss}=\text{CP}-\text{SP}\ (\text{CP}\gt\text{SP}) \]",
            [("Cost price (what was paid)", r"\text{CP}"), ("Selling price (what was received)", r"\text{SP}"),
             ("SP above CP", r"\text{Profit}=\text{SP}-\text{CP}"), ("SP below CP", r"\text{Loss}=\text{CP}-\text{SP}")],
            r"The seller's money changes from CP (paid out) to SP (taken in); the change is his profit or his loss.",
            "The question gives the price paid and the price received (or one of them and the profit or loss) and asks for the other.",
            r"A doll bought for Rs \(45\) and sold for Rs \(54\): profit \(= 54 - 45 = \text{Rs }9\).",
            r"Subtracting the wrong way round and calling a loss a profit - always check which price is larger first."),
    2: card(2, "Profit or Loss Per Cent",
            r"Profit and loss per cent are always worked out on the cost price, unless the question says otherwise.",
            r"\[ \text{Gain or Loss per cent}=\frac{\text{Gain or Loss}}{\text{CP}}\times 100 \]",
            [("Profit or loss in rupees", r"\text{SP}-\text{CP}"), ("Divide by the cost price", r"\frac{\text{Gain}}{\text{CP}}"),
             ("Multiply by 100", r"\frac{\text{Gain}}{\text{CP}}\times 100")],
            r"Per cent means 'on every Rs 100 of cost'. Dividing the gain by the cost gives the gain on Rs 1 of cost; multiplying by 100 "
            r"gives it on Rs 100.",
            "The question asks for the gain or loss per cent, the cost price from a selling price and a per cent, or the selling price for a gain per cent.",
            r"A kite bought for Rs \(40\) is sold for Rs \(46\): gain \(=\frac{6}{40}\times 100=15\%\).",
            r"Dividing by the selling price instead of the cost price, or leaving out extra costs (repairs, transport) from the cost."),
    3: card(3, "Equal Profit and Loss at Two Selling Prices",
            r"If selling an article for Rs \(x\) gives the same profit as the loss made by selling it for Rs \(y\), the cost price is exactly "
            r"half-way between \(x\) and \(y\); from it the price for any profit per cent follows.",
            r"\[ \text{CP}=\frac{x+y}{2},\qquad \text{SP for } z\% \text{ profit}=\frac{(x+y)(100+z)}{200} \]",
            [("Profit at Rs x", r"x-\text{CP}"), ("Loss at Rs y", r"\text{CP}-y"), ("Equal, so", r"\text{CP}=\frac{x+y}{2}"),
             ("Add z% profit", r"\text{CP}\times\frac{100+z}{100}")],
            r"The cost price is the same distance below \(x\) as it is above \(y\), so it is their average.",
            "'The profit earned by selling for Rs x equals the loss incurred by selling for Rs y; at what price should it be sold to gain z%?'",
            r"Profit at Rs \(780\) equals loss at Rs \(620\): CP \(= 700\); for \(15\%\) profit SP \(= 700\times 1.15 = \text{Rs }805\).",
            r"Taking the difference \(x - y\) instead of the average, or adding \(z\%\) of the selling price instead of the cost price."),
}

opts = lambda *v: dict(zip("abcd", v))

OLD = {
    1: {278: (lambda: r1(45, 54, "she"), r"A girl buys a doll for Rs 45 and sells it for Rs 54. How much profit does she make?",
              opts(Rs(8), Rs(9), Rs(11), Rs(99))),
        279: (lambda: r1(160, 148), r"A shopkeeper buys a lamp for Rs 160 and sells it for Rs 148. What is his loss?",
              opts(Rs(12), Rs(14), Rs(8), Rs(22)))},
    2: {280: (lambda: r2(40, 46), r"Ravi pays Rs 40 for a kite and later sells it for Rs 46. What per cent does he gain?", opts(P(12), P(18), P(15), P(6))),
        281: (lambda: r2(80, 70), r"A woman buys a vase for Rs 80 and sells it for Rs 70. Find her loss per cent.",
              opts(P(10), P(F(25, 2)), P(F(100, 7)), P(15))),
        916: (lambda: r2(360, 324), r"A fruit seller buys a crate of grapes for Rs 360 but has to sell it for Rs 324 as the grapes start to "
                                    r"go soft. What is his loss per cent?", opts(P(9), P(12), P(36), P(10))),
        282: (lambda: r2_extra(7500, 500, "the repairs", 9200), r"Sohan buys an old scooter for Rs 7500 and spends Rs 500 on repairs. He sells "
                                                                 r"it for Rs 9200. Find his profit or loss per cent.",
              opts(SP_("Loss", 15), SP_("Profit", 15), SP_("Profit", 12), SP_("Profit", 16))),
        917: (lambda: r2_extra(2600, 400, "the repair", 2850), r"Rita buys a used sewing machine for Rs 2600 and spends Rs 400 on its repair. "
                                                               r"She sells it for Rs 2850. Find her profit or loss per cent.",
              opts(SP_("Profit", 5), SP_("Loss", 6), SP_("Loss", 5), SP_("Profit", 9))),
        283: (lambda: r2_dozens(80, 18, 60, 2, signed=True), r"A shop buys 80 dozen erasers at Rs 18 a dozen and spends Rs 60 on carriage. "
                                                              r"It sells the erasers at Rs 2 each. Find its profit or loss per cent.",
              opts(SP_("Profit", 28), SP_("Loss", 28), SP_("Profit", 33), SP_("Profit", 20))),
        918: (lambda: r2_dozens(60, 24, 60, F(5, 2), signed=True), r"A vendor buys 60 dozen bananas at Rs 24 a dozen and pays Rs 60 for "
                                                                    r"transport. He sells them at Rs 2.50 each. What is his profit or loss per cent?",
              opts(SP_("Loss", 20), SP_("Profit", 25), SP_("Profit", 16), SP_("Profit", 20))),
        284: (lambda: r2_dozens(15, 300, 0, 27), r"A trader buys 15 dozen cups at Rs 300 a dozen and sells each cup for Rs 27. What is his "
                                                 r"profit per cent?", opts(P(8), P(9), P(6), P(12))),
        919: (lambda: r2_dozens(25, 96, 0, 9), r"A shop buys 25 dozen spoons at Rs 96 a dozen and sells each spoon at Rs 9. Find its profit "
                                               r"per cent.", opts(P(10), P(F(25, 2)), P(9), P(15))),
        285: (lambda: r2_sp_of(15, 3), r"By selling 15 pens a shopkeeper gains the selling price of 3 pens. Find his gain per cent.",
              opts(P(20), P(18), P(25), P(F(100, 3)))),
        920: (lambda: r2_sp_of(18, 3), r"A girl sells 18 handkerchiefs and makes a profit equal to the selling price of 3 of them. What is "
                                       r"her profit per cent?", opts(P(F(50, 3)), P(15), P(18), P(20))),
        921: (lambda: r2_back(5460, 9), r"A farmer sells a piece of land for Rs 5460 at a loss of 9%. What did the land cost him?",
              opts(Rs(5951.4), Rs(6000), Rs(6500), Rs(5800))),
        922: (lambda: r2_back(270, 10), r"A watch is sold for Rs 270 at a loss of 10%. Find its cost price.",
              opts(Rs(243), Rs(280), Rs(297), Rs(300))),
        287: (lambda: r2_each(12, 30, 3), r"A man buys 12 pencils for Rs 30 and sells them at Rs 3 each. What is his gain per cent?",
              opts(P(20), P(10), P(25), P(F(50, 3)))),
        923: (lambda: r2_each(20, 16, 1), r"A boy buys 20 marbles for Rs 16 and sells them at Rs 1 each. Find his gain per cent.",
              opts(P(20), P(25), P(16), P(4))),
        286: (lambda: r2_sell(60, 45, [("the carriage", 210), ("the packing", 90)], 20, "box"),
              r"A stationer buys 60 boxes of chalk at Rs 45 a box. He spends Rs 210 on carriage and Rs 90 on packing. At what price must he "
              r"sell each box to gain 20%?", opts(Rs(55), Rs(62.5), Rs(60), Rs(58))),
        924: (lambda: r2_sell(50, 950, [("the transport", 1500), ("the porters' charge", 1000)], 20, "bag"),
              r"A shop buys 50 bags of rice at Rs 950 a bag and pays Rs 1500 for transport and Rs 1000 to the porters. At what price should it "
              r"sell each bag to make a profit of 20%?", opts(Rs(1140), Rs(1000), Rs(1200), Rs(1250))),
        288: (lambda: r2_rates(5, 4, 4, 5), r"A woman buys 5 mangoes for Rs 4 and sells 4 mangoes for Rs 5. What is her profit per cent?",
              opts(P(25), P(F(225, 4)), P(20), P(45))),
        925: (lambda: r2_rates(6, 5, 5, 6), r"A boy buys 6 pens for Rs 5 and sells 5 pens for Rs 6. Find his gain per cent.",
              opts(P(20), P(36), P(44), P(F(100, 6)))),
        926: (lambda: r2_disc(450, 378), r"A shirt marked at Rs 450 is sold for Rs 378. What is the rate of discount?",
              opts(P(16), P(18), P(12), P(72)))},
    3: {289: (lambda: r3(780, 620, 15), r"A clock sold for Rs 780 gives the same profit as the loss when it is sold for Rs 620. At what price "
                                        r"should it be sold to gain 15%?", opts(Rs(805), Rs(897), Rs(713), Rs(784))),
        927: (lambda: r3(9700, 8300, 20), r"The gain on selling a sofa for Rs 9700 equals the loss on selling it for Rs 8300. For how much "
                                          r"should it be sold to make a profit of 20%?", opts(Rs(11640), Rs(10800), Rs(9960), Rs(10200))),
        928: (lambda: r3(1150, 850, 12), r"A trader's profit on selling a radio for Rs 1150 is the same as his loss on selling it for Rs 850. "
                                         r"At what price should he sell it for a 12% profit?", opts(Rs(1288), Rs(1220), Rs(1120), Rs(1150))),
        929: (lambda: r3(640, 560, 35), r"Selling a bat for Rs 640 gives as much profit as the loss on selling it for Rs 560. Find the price "
                                        r"that gives a profit of 35%.", opts(Rs(864), Rs(760), Rs(756), Rs(810))),
        930: (lambda: r3(2300, 1700, 45), r"The profit made by selling a table for Rs 2300 is equal to the loss made by selling it for Rs 1700. "
                                          r"What should it be sold for to gain 45%?", opts(Rs(2900), Rs(3335), Rs(2465), Rs(2800))),
        931: (lambda: r3(5400, 4200, 8), r"A cooler sold for Rs 5400 brings a profit equal to the loss when it is sold for Rs 4200. What price "
                                         r"will give a profit of 8%?", opts(Rs(5832), Rs(5184), Rs(5096), Rs(5300)))},
}

NEW = {
    1: [("r1_e1", r"A trader buys a fan for Rs 840 and sells it for Rs 975. Find his profit or loss.", lambda: r1(840, 975, signed=True),
         [SP_("Loss", 135, True), SP_("Profit", 135, True), SP_("Profit", 125, True), SP_("Profit", 145, True)], 2),
        ("r1_e2", r"A chair that cost Rs 1390 is sold for Rs 1362. Is there a profit or a loss, and how much is it?", lambda: r1(1390, 1362, signed=True),
         [SP_("Loss", 28, True), SP_("Profit", 28, True), SP_("Loss", 32, True), SP_("Loss", 18, True)], 1),
        ("r1_e3", r"If a bag is sold for Rs 130, the profit is twice the profit made when it is sold for Rs 115. What did the bag cost?",
         lambda: r1_double(130, 115), [Rs(90), Rs(110), Rs(105), Rs(100)], 4)],
    2: [("r2_e1", r"A cycle bought for Rs 2400 is sold for Rs 2580. Find the gain or loss per cent.", lambda: r2(2400, 2580, signed=True),
         [SP_("Gain", F(15, 2)), SP_("Loss", F(15, 2)), SP_("Gain", 7), SP_("Gain", 18)], 1),
        ("r2_e2", r"A shopkeeper makes a profit of Rs 9 on a box of sweets that cost him Rs 60. What is his profit per cent?",
         lambda: r2(60, 69), [P(9), P(12), P(15), P(18)], 3)],
    3: [],
}


def main():
    for n in (1, 2, 3):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, op) in OLD[n].items():
            extra = {"question": question, **(op or {})}
            if rows[rid]["e"] is None or rows[rid]["e"].strip():
                extra["e"] = ""                      # the page draws option e; NULL prints "None"
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        if NEW[n]:
            qs, answers = [], []
            for key, text, fn, op, pos in NEW[n]:
                g = fn()
                qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
                a = g["answer"]
                answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
            json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                      open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(NEW[n])} new questions")


if __name__ == "__main__":
    main()
