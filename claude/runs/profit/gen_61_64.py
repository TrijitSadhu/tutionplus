"""Profit and Loss Rules 61-64 (2026-10-30). Rule 61: bought x% below the list price, sold y% above the price paid - profit per cent on
the list price. Rule 62: A sells an article to B at x% loss and B sells it back to A at y% gain - A's loss and B's gain. Rule 63:
marked x% above cost, y% discount, sold for Rs S - the cost price. Rule 64: two selling rates, a loss of Rs L at one and a gain of
Rs G at the other - the quantity bought. Rows 369 (R61) and 371 (R63) are those rules' book examples; they were first filed under
Rules 60 and 55 and are moved here with their reworded sentences (gated against the original copies in 0_original_rows.json).
Rows 370 (R62) and 372 (R64) get simple-style sentences with new settings and all-new numbers; the book exercises are added.
Usage: python gen_61_64.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import place, popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
import gen_53_56  # noqa: E402
import gen_57_60  # noqa: E402

T61 = (r"If an article is bought at \(x\%\) below its list price and sold at \(y\%\) above the price paid, the profit on the list "
       r"price is<br>\[ \left(y-x-\frac{xy}{100}\right)\% \]")
T62 = (r"If A sells an article worth Rs \(W\) to B at a loss of \(x\%\) and B sells it back to A at a gain of \(y\%\), A loses "
       r"<br>\[ \frac{y(100-x)}{100}\%\ \text{of }W \]and B gains \(y\%\) on what he paid.")
T63 = (r"If goods marked \(x\%\) above the cost price are sold at a discount of \(y\%\) for Rs \(S\), then"
       r"<br>\[ \text{CP}=S\times\frac{100}{100+x}\times\frac{100}{100-y} \]")
T64 = (r"If selling at Rs \(p_1\) a unit gives a loss of Rs \(L\) and selling at Rs \(p_2\) a unit gives a gain of Rs \(G\), the quantity is"
       r"<br>\[ \frac{G+L}{p_2-p_1} \]")


def r61(x, y):
    x, y = F(x), F(y)
    paid = 100 - x
    sp = paid * (100 + y) / 100
    v = sp - 100
    trad = steps(
        ("Take the list price as 100.", rf"He pays \(100 - {tex(x)} = {tex(paid)}\)."),
        ("He sells at " + tex(y) + "% above what he paid.", rf"\[ {tex(paid)}\times\frac{{{tex(100 + y)}}}{{100}} = {tex(sp)} \]"),
        ("Profit measured on the list price.", rf"\[ {tex(sp)} - 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T61.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {tex(y)} - {tex(x)} - \frac{{{tex(x)}\times {tex(y)}}}{{100}} = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\(\frac{{xy}}{{100}} = {tex(x * y / 100)}\).", rf"\({tex(y)} - {tex(x)} - {tex(x * y / 100)} = {tex(v)}\%\)."]
    return result(("number", v), T61, trad, rule, PCT(v), rb, rf"\[ {tex(y)} - {tex(x)} - {tex(x * y / 100)} = {tex(v)}\% \]")


def r62(W, x, y, ask):
    W, x, y = map(F, (W, x, y))
    got = W * (100 - x) / 100
    paid = got * (100 + y) / 100
    lossA = paid - got
    pA = lossA / W * 100
    trad = steps(
        ("A sells to B.", rf"\[ {m(W)}\times\frac{{{tex(100 - x)}}}{{100}} = {m(got)} \]"),
        ("B sells it back to A.", rf"\[ {m(got)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(paid)} \]"),
        ("A has the article again but has paid out the difference.", rf"A loses \({m(paid)} - {m(got)} = {m(lossA)}\), i.e. "
                                                                    rf"\(\frac{{{m(lossA)}}}{{{m(W)}}}\times 100 = {tex(pA)}\%\); B gains \({m(lossA)}\) on \({m(got)}\), i.e. \({tex(y)}\%\)."))
    rule = steps(
        ("Identify the values.", rf"\(W = {m(W)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T62.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{tex(y)}\times {tex(100 - x)}}}{{100}} = {tex(pA)}\%,\qquad {tex(pA)}\%\text{{ of }}{m(W)} = {m(lossA)} \]"))
    rb = [rf"A's loss \(= \frac{{{tex(y)}\times {tex(100 - x)}}}{{100}} = {tex(pA)}\%\).", rf"Amount \(= {m(lossA)}\).", rf"B gains \({tex(y)}\%\)."]
    sc = rf"\[ \frac{{{tex(y)}\times {tex(100 - x)}}}{{100}} = {tex(pA)}\%,\quad {tex(pA)}\%\times {m(W)} = {m(lossA)} \]"
    if ask == "pct":
        return result(("pair", (pA, y)), T62, trad, rule, rf"A loses \({tex(pA)}\%\), B gains \({tex(y)}\%\)", rb, sc)
    return result(("number", lossA), T62, trad, rule, rf"Rs \({m(lossA)}\)", rb, sc)


def opts62(g):
    a, b = (F(t) for t in g["answer"][1])
    Q = lambda t: rf"A loses \({tex(t[0])}\%\), B gains \({tex(t[1])}\%\)"
    return place(Q((a, b)), [Q((b, b)), Q((a, a)), Q((b, a))])


def r63(x, y, S):
    x, y, S = map(F, (x, y, S))
    mp = S * 100 / (100 - y)
    cp = mp * 100 / (100 + x)
    trad = steps(
        ("Undo the discount.", rf"Rs \({m(S)}\) is \({tex(100 - y)}\%\) of the marked price: \[ \text{{MP}} = {m(S)}\times\frac{{100}}{{{tex(100 - y)}}} = {m(mp)} \]"),
        ("Undo the mark-up.", rf"The marked price is \({tex(100 + x)}\%\) of the cost: \[ \text{{CP}} = {m(mp)}\times\frac{{100}}{{{tex(100 + x)}}} = {m(cp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(S = {m(S)}\)."),
        ("Apply the specified rule.", T63.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {m(S)}\times\frac{{100}}{{{tex(100 + x)}}}\times\frac{{100}}{{{tex(100 - y)}}} = {m(cp)} \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(S = {m(S)}\).", rf"\({m(S)}\times\frac{{100}}{{{tex(100 + x)}}}\times\frac{{100}}{{{tex(100 - y)}}}\).", rf"CP \(= {m(cp)}\)."]
    return result(("number", cp), T63, trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ {m(S)}\times\frac{{100}}{{{tex(100 + x)}}}\times\frac{{100}}{{{tex(100 - y)}}} = {m(cp)} \]")


def plural(unit):
    return unit if unit == "kg" else unit + "s"


def r64(p1, L, p2, G, unit):
    p1, L, p2, G = map(F, (p1, L, p2, G))
    qn = (G + L) / (p2 - p1)
    cost = p1 * qn + L
    trad = steps(
        ("Compare the two sales.", rf"Raising the price by Rs \({m(p2 - p1)}\) a {unit} turns a loss of Rs \({m(L)}\) into a gain of Rs \({m(G)}\), "
                                   rf"so the takings go up by Rs \({m(L + G)}\)."),
        ("Quantity.", rf"\[ \frac{{{m(L + G)}}}{{{m(p2 - p1)}}} = {tex(qn)}\ \text{{{plural(unit)}}} \]"),
        ("Check.", rf"Cost \(= {m(p1)}\times {tex(qn)} + {m(L)} = {m(cost)}\) and also \({m(p2)}\times {tex(qn)} - {m(G)} = {m(cost)}\)."))
    rule = steps(
        ("Identify the values.", rf"\(p_1 = {m(p1)}\), \(L = {m(L)}\), \(p_2 = {m(p2)}\), \(G = {m(G)}\)."),
        ("Apply the specified rule.", T64.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(G)} + {m(L)}}}{{{m(p2)} - {m(p1)}}} = {tex(qn)} \]"))
    rb = [rf"\(G + L = {m(G + L)}\).", rf"\(p_2 - p_1 = {m(p2 - p1)}\).", rf"Quantity \(= {tex(qn)}\) {plural(unit)}."]
    return result(("number", qn), T64, trad, rule, rf"\({tex(qn)}\) {plural(unit)}", rb, rf"\[ \frac{{{m(G + L)}}}{{{m(p2 - p1)}}} = {tex(qn)} \]")


def opts64(g, unit):
    v = F(g["answer"][1])
    Q = lambda t: rf"\({tex(t)}\) {plural(unit)}"
    return place(Q(v), [Q(v + 20), Q(v - 20), Q(2 * v)])


CARDS = {
    61: card(61, "Bought Below the List Price, Sold Above the Price Paid",
             r"Buying at \(x\%\) below the list price and selling at \(y\%\) above the price paid is a cut of \(x\%\) followed by a rise of \(y\%\); "
             r"the result is measured on the list price.",
             r"\[ \text{Profit on the list price}=\left(y-x-\frac{xy}{100}\right)\% \]",
             [("Paid (list = 100)", r"100-x"), ("Sold", r"(100-x)\frac{100+y}{100}"), ("On the list price", r"y-x-\frac{xy}{100}")],
             r"Compare Rule 60, where the sale is \(y\%\) above the list price.",
             "'A trader bought a car at x% discount on its original price and sold it at y% increase on the price he bought it. What profit per cent did he make on the original price?'",
             r"\(10\%\) below, \(30\%\) above the price paid: \(30-10-3=17\%\).",
             r"Answering \(y-x\) - the rise is on the smaller price paid."),
    62: card(62, "Sold at a Loss and Bought Back at a Gain",
             r"A sells to B at a loss of \(x\%\) and buys the same article back from B at a gain of \(y\%\) to B. A ends with the article but has paid "
             r"out B's profit, and B's profit is \(y\%\) of the lower price.",
             r"\[ \text{A's loss}=\frac{y(100-x)}{100}\%\ \text{of the value} \]",
             [("A gets", r"W\frac{100-x}{100}"), ("A pays back", r"W\frac{100-x}{100}\cdot\frac{100+y}{100}"), ("A's loss", r"W\frac{(100-x)y}{100^2}")],
             r"Whatever A loses, B gains; only the per cents differ, because they are on different amounts.",
             "'A horse worth Rs W is sold by A to B at x% loss; B sells it back to A at y% gain. Who gains and who loses, and how much?'",
             r"Rs \(2000\), \(10\%\) loss, \(10\%\) gain: A gets \(1800\), pays \(1980\); A loses Rs \(180\) (\(9\%\)), B gains \(10\%\).",
             r"Thinking the two \(10\%\)s cancel."),
    63: card(63, "Marked Up and Discounted: the Cost from the Selling Price",
             r"The selling price is \((100-y)\%\) of the marked price, which is \((100+x)\%\) of the cost. Undo the two steps in turn.",
             r"\[ \text{CP}=S\times\frac{100}{100+x}\times\frac{100}{100-y} \]",
             [("Marked price", r"S\times\frac{100}{100-y}"), ("Cost", r"\text{MP}\times\frac{100}{100+x}")],
             r"Undo the discount first (it was taken off the marked price), then the mark-up.",
             "'A man marks his goods x% above the cost price and allows y% discount. If he sells an article for Rs S, find its cost price.'",
             r"\(20\%\) up, \(10\%\) off, Rs \(540\): \(540\times\frac{100}{90}\times\frac{100}{120}=\text{Rs }500\).",
             r"Taking \(x-y\) per cent off \(S\) in one step."),
    64: card(64, "A Loss at One Price, a Gain at Another: the Quantity",
             r"Raising the selling price by \(p_2-p_1\) a unit changes a loss of Rs \(L\) into a gain of Rs \(G\), so the takings rise by \(G+L\) "
             r"in all - that is \(p_2-p_1\) on each unit.",
             r"\[ \text{Quantity}=\frac{G+L}{p_2-p_1} \]",
             [("Rise in takings", r"G+L"), ("Rise per unit", r"p_2-p_1"), ("Quantity", r"\frac{G+L}{p_2-p_1}")],
             r"The cost is then \(p_1\times\text{quantity}+L\).",
             "'A milkman sells milk at Rs p1 a litre and loses Rs L; at Rs p2 a litre he gains Rs G. How much milk did he buy?'",
             r"Rs \(4\) a kg: loss Rs \(30\); Rs \(7\) a kg: gain Rs \(60\): \(\frac{90}{3}=30\) kg.",
             r"Using \(G-L\) - the loss and the gain are on opposite sides of the cost."),
}
Q62 = {"pct": "A owns a {item} worth Rs {W}. He sells it to B at a loss of {x}%, and B sells it back to A at a gain of {y}%. Find A's loss per cent and B's gain per cent.",
       "amt": "A owns a {item} worth Rs {W}. He sells it to B at a loss of {x}%, and B sells it back to A at a gain of {y}%. How much money does A lose in all?"}
Q64 = "A {who} buys some {what}. Selling it at Rs {p1} a {unit} gives a loss of Rs {L}, while selling it at Rs {p2} a {unit} gives a gain of Rs {G}. How many {units} did {pron} buy?"
OLD = {61: {369: ("car", (15, 25))}, 62: {370: ("pct", "cow", (8400, 14, 25))}, 63: {371: (30, 10, 1053)},
       64: {372: ("dairy", "milk", "litre", "it", (28, 360, 32, 240))}}
NEW = {61: [("r61_e1", ("van", (12, 30))), ("r61_e2", ("laptop", (25, 44))), ("r61_e3", ("tractor", (8, 15)))],
       62: [("r62_e1", ("amt", "mare", (15000, 4, 4))), ("r62_e2", ("amt", "boat", (11000, 10, 10))), ("r62_e3", ("amt", "camel", (6400, 25, 25))),
            ("r62_e4", ("amt", "bull", (4800, 30, 30)))],
       63: [("r63_e1", (25, 20, 1360)), ("r63_e2", (20, 10, 1620)), ("r63_e3", (40, 25, 2100)), ("r63_e4", (35, 20, 2916))],
       64: [("r64_e1", ("grocer", "oil", "litre", "he", (40, 420, 45, 380))), ("r64_e2", ("trader", "rice", "kg", "he", (15, 270, 21, 150))),
            ("r64_e3", ("vendor", "sugar", "kg", "she", (24, 137, 26, 213)))]}


def build(rule, spec):
    if rule == 61:
        item, (x, y) = spec
        g = r61(x, y)
        return g, gen_57_60.Q60["list"].format(item=item, x=x, y=y), popts(g["answer"][1])
    if rule == 62:
        ask, item, (W, x, y) = spec
        g = r62(W, x, y, ask)
        return g, Q62[ask].format(item=item, W=W, x=x, y=y), (opts62(g) if ask == "pct" else ropts(g["answer"][1]))
    if rule == 63:
        x, y, S = spec
        g = r63(x, y, S)
        return g, gen_53_56.Q55["cp"].format(x=x, y=y, S=S), ropts(g["answer"][1])
    who, what, unit, pron, (p1, L, p2, G) = spec
    g = r64(p1, L, p2, G, unit)
    return g, Q64.format(who=who, what=what, unit=unit, units=plural(unit), pron=pron, p1=p1, L=L, p2=p2, G=G), opts64(g, unit)


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, spec)
        if rule in (61, 63):
            assert q == rows[rid]["question"], rid          # moved rows keep the sentence they already have
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
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
    for r in (61, 62, 63, 64):
        main(r)
