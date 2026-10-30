"""Profit and Loss Rules 69-72 (2026-10-30). Rule 69: one person takes his profit as x% of the selling price, another as y% of the cost
price; same selling price, profits differ by Rs A - the selling price. Rule 70: two articles sold for Rs A in all, the first's cost =
the second's selling price, x% loss on the first and y% gain on the second - the gain or loss in rupees. Rule 71: one article sold
for Rs A at x% profit, a second at y% loss, no profit and no loss on the whole - the cost of the second. Rule 72: x1% discount gives
P% profit - the profit at x2% discount. Writes the four cards, regenerates old rows 406 (R69), 407 (R71) and 408 (R72) with
simple-style sentences, new settings and all-new numbers (Rule 70 has no old row), and adds the book's examples and exercises.
Usage: python gen_69_72.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import place, popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402

# ---------------------------------------------------------------- Rule 69
T69 = (r"If, at the same selling price, one person's profit is \(x\%\) of the selling price and another's is \(y\%\) of the cost price, "
       r"and the two profits differ by Rs \(A\), then<br>\[ \text{SP}=\frac{A\times 100\times(100+y)}{100^2-(100+y)(100-x)} \]")


def r69(x, y, A, n1, n2):
    x, y, A = map(F, (x, y, A))
    sp = A * 100 * (100 + y) / (100 * 100 - (100 + y) * (100 - x))
    p1, p2 = sp * x / 100, sp - sp * 100 / (100 + y)
    trad = steps(
        ("Let the selling price be Rs \\(S\\).", rf"{n1}'s profit \(= \frac{{{tex(x)}}}{{100}}S\). {n2}'s cost \(= \frac{{100}}{{{tex(100 + y)}}}S\), so his profit \(= S - \frac{{100}}{{{tex(100 + y)}}}S = \frac{{{tex(y)}}}{{{tex(100 + y)}}}S\)."),
        ("The difference is given.", rf"\[ \frac{{{tex(x)}}}{{100}}S - \frac{{{tex(y)}}}{{{tex(100 + y)}}}S = {m(A)} \;\Rightarrow\; {tex(F(x) / 100 - F(y) / (100 + y))}S = {m(A)} \;\Rightarrow\; S = {m(sp)} \]"),
        ("Check.", rf"{n1}'s profit \(= {m(p1)}\), {n2}'s \(= {m(p2)}\); difference \(= {m(p1 - p2)}\)."))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(A = {m(A)}\)."),
        ("Apply the specified rule.", T69.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(A)}\times 100\times {tex(100 + y)}}}{{10000 - {tex(100 + y)}\times {tex(100 - x)}}} = "
                                   rf"\frac{{{m(A * 100 * (100 + y))}}}{{{tex(10000 - (100 + y) * (100 - x))}}} = {m(sp)} \]"))
    rb = [rf"\(100^2 - (100+y)(100-x) = {tex(10000 - (100 + y) * (100 - x))}\).", rf"\(A\times 100\times(100+y) = {m(A * 100 * (100 + y))}\).", rf"SP \(= {m(sp)}\)."]
    return result(("number", sp), T69, trad, rule, rf"Rs \({m(sp)}\)", rb,
                  rf"\[ \frac{{{m(A * 100 * (100 + y))}}}{{{tex(10000 - (100 + y) * (100 - x))}}} = {m(sp)} \]")


# ---------------------------------------------------------------- Rule 70
T70 = (r"If two articles are sold for Rs \(A\) in all, the cost of the first equals the selling price of the second, and the first is "
       r"sold at \(x\%\) loss and the second at \(y\%\) gain, the gain (loss if negative) is<br>"
       r"\[ \frac{(100-x)-\frac{100^2}{100+y}}{100+(100-x)}\times A \]")


def r70(A, x, y):
    A, x, y = map(F, (A, x, y))
    cp2 = F(10000) / (100 + y)
    sp_t, cp_t = 200 - x, 100 + cp2
    v = (sp_t - cp_t) / sp_t * A
    trad = steps(
        ("Take the cost of the first as 100.", rf"First: cost \(100\), sold for \({tex(100 - x)}\). Second: sold for \(100\), cost \(100\times\frac{{100}}{{{tex(100 + y)}}} = {tex(cp2)}\)."),
        ("Totals.", rf"Selling prices \(= {tex(sp_t)}\), costs \(= {tex(cp_t)}\); the gain is \({tex(sp_t - cp_t)}\) on every \({tex(sp_t)}\) of selling price."),
        ("Scale to Rs " + tex(A) + ".", rf"\[ \frac{{{tex(sp_t - cp_t)}}}{{{tex(sp_t)}}}\times {m(A)} = {m(v)} \]" + (" It is negative, so a loss." if v < 0 else "")))
    rule = steps(
        ("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T70.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{tex(100 - x)} - {tex(cp2)}}}{{100 + {tex(100 - x)}}}\times {m(A)} = {m(v)} \]"))
    rb = [rf"\((100-x) - \frac{{100^2}}{{100+y}} = {tex(100 - x - cp2)}\).", rf"\(100 + (100-x) = {tex(sp_t)}\).", rf"Result \(= {m(v)}\)."]
    fin = rf"a {'gain' if v > 0 else 'loss'} of Rs \({m(abs(v))}\)"
    return result(("signed", v), T70, trad, rule, fin, rb, rf"\[ \frac{{{tex(100 - x - cp2)}}}{{{tex(sp_t)}}}\times {m(A)} = {m(v)} \]")


def rsopts(v):
    v = F(v)
    s = abs(v)
    w, o = ("Gain", "Loss") if v > 0 else ("Loss", "Gain")
    step = 10 if s >= 50 else 5
    return place(rf"{w} of Rs \({m(s)}\)", [rf"{o} of Rs \({m(s)}\)", rf"{w} of Rs \({m(s + step)}\)", rf"{o} of Rs \({m(s + step)}\)"])


# ---------------------------------------------------------------- Rule 71
T71 = (r"If one article is sold for Rs \(A\) at \(x\%\) profit and a second at \(y\%\) loss, with no profit and no loss on the whole, the "
       r"second cost<br>\[ \text{Rs }\frac{100\,A\,x}{(100+x)\,y} \]")


def r71(A, x, y, item):
    A, x, y = map(F, (A, x, y))
    cp1 = A * 100 / (100 + x)
    gain = A - cp1
    cp2 = gain * 100 / y
    trad = steps(
        ("Profit on the first.", rf"Cost \(= {m(A)}\times\frac{{100}}{{{tex(100 + x)}}} = {m(cp1)}\); profit \(= {m(A)} - {m(cp1)} = {m(gain)}\)."),
        ("No profit and no loss on the whole.", rf"So the loss on the second is also Rs \({m(gain)}\), and that is \({tex(y)}\%\) of its cost."),
        ("Cost of the second.", rf"\[ {m(gain)}\times\frac{{100}}{{{tex(y)}}} = {m(cp2)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T71.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{100\times {m(A)}\times {tex(x)}}}{{{tex(100 + x)}\times {tex(y)}}} = {m(cp2)} \]"))
    rb = [rf"Profit on the first \(= {m(gain)}\).", rf"It equals \({tex(y)}\%\) of the second's cost.", rf"Second {item} cost \(= {m(cp2)}\)."]
    return result(("number", cp2), T71, trad, rule, rf"Rs \({m(cp2)}\)", rb, rf"\[ \frac{{100\times {m(A)}\times {tex(x)}}}{{{tex(100 + x)}\times {tex(y)}}} = {m(cp2)} \]")


# ---------------------------------------------------------------- Rule 72
T72 = (r"If a discount of \(x_1\%\) gives a profit of \(P\%\), then a discount of \(x_2\%\) gives a profit of"
       r"<br>\[ \left((100+P)\times\frac{100-x_2}{100-x_1}-100\right)\% \]")


def r72(x1, P, x2):
    x1, P, x2 = map(F, (x1, P, x2))
    sp1, sp2 = 100 - x1, 100 - x2
    cp = sp1 * 100 / (100 + P)
    v = (sp2 - cp) / cp * 100
    trad = steps(
        ("Take the marked price as 100.", rf"At \({tex(x1)}\%\) off the price is \({tex(sp1)}\), which is \({tex(100 + P)}\%\) of the cost: cost \(= {tex(sp1)}\times\frac{{100}}{{{tex(100 + P)}}} = {tex(cp)}\)."),
        ("At the new discount.", rf"Price \(= 100 - {tex(x2)} = {tex(sp2)}\)."),
        ("Profit per cent.", rf"\[ \frac{{{tex(sp2)} - {tex(cp)}}}{{{tex(cp)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x_1 = {tex(x1)}\), \(P = {tex(P)}\), \(x_2 = {tex(x2)}\)."),
        ("Apply the specified rule.", T72.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {tex(100 + P)}\times\frac{{{tex(sp2)}}}{{{tex(sp1)}}} - 100 = {tex(v)}\% \]"))
    rb = [rf"\((100+P) = {tex(100 + P)}\).", rf"\(\frac{{100-x_2}}{{100-x_1}} = {tex(sp2 / sp1)}\).", rf"Profit \(= {tex(v)}\%\)."]
    return result(("number", v), T72, trad, rule, PCT(v), rb, rf"\[ {tex(100 + P)}\times\frac{{{tex(sp2)}}}{{{tex(sp1)}}} - 100 = {tex(v)}\% \]")


CARDS = {
    69: card(69, "Profit on the Selling Price Against Profit on the Cost",
             r"At the same selling price \(S\), a profit of \(x\%\) of \(S\) and a profit of \(y\%\) of the cost (which is \(\frac{y}{100+y}S\)) differ "
             r"by a fixed share of \(S\).",
             r"\[ \text{SP}=\frac{A\times 100\times(100+y)}{100^2-(100+y)(100-x)} \]",
             [("Profit on SP", r"\frac{x}{100}S"), ("Profit on CP", r"\frac{y}{100+y}S"), ("Difference", r"\left(\frac{x}{100}-\frac{y}{100+y}\right)S=A")],
             r"With the same per cent \(x\) for both, the formula becomes \(\frac{A\times 100(100+x)}{x^2}\).",
             "'A calculates his profit on the selling price, B on the cost price; with the same selling price, A gets x% and B y%, and their profits differ by Rs A. Find the selling price.'",
             r"\(40\%\) on SP, \(25\%\) on CP, difference Rs \(10\): \(\frac{40}{100}-\frac{25}{125}=\frac{1}{5}\), so \(S=\text{Rs }50\).",
             r"Taking both per cents on the same base."),
    70: card(70, "First's Cost = Second's Selling Price",
             r"Take the first article's cost as 100. Its price is \(100-x\); the second sells for 100 and costs \(\frac{100^2}{100+y}\). Compare the "
             r"totals and scale to Rs \(A\).",
             r"\[ \text{Gain}=\frac{(100-x)-\frac{100^2}{100+y}}{100+(100-x)}\times A \]",
             [("Costs", r"100+\frac{100^2}{100+y}"), ("Prices", r"(100-x)+100"), ("Scale", r"\frac{\text{prices}-\text{costs}}{\text{prices}}\times A")],
             r"A negative answer is a loss; Rs \(A\) is the total of the two selling prices.",
             "'A man sells two horses for Rs A; the cost of the first equals the selling price of the second; the first is sold at x% loss and the second at y% gain. Find his gain or loss.'",
             r"\(4\%\) loss, \(25\%\) gain: prices \(96+100=196\), costs \(100+80=180\); gain \(=\frac{16}{196}\times A\).",
             r"Taking both costs as 100."),
    71: card(71, "A Profit on One Sale Cancelled by a Loss on Another",
             r"The profit on the first article is Rs \(A-\frac{100A}{100+x}=\frac{Ax}{100+x}\). With no profit and no loss overall, that is the loss on "
             r"the second, which is \(y\%\) of its cost.",
             r"\[ \text{CP of the second}=\frac{100\,A\,x}{(100+x)\,y} \]",
             [("Profit on the first", r"\frac{Ax}{100+x}"), ("Loss on the second", r"\frac{y}{100}c"), ("Equal", r"c=\frac{100Ax}{(100+x)y}")],
             r"The profit is found from the selling price, so divide by \(100+x\), not by 100.",
             "'A dealer sells a table for Rs A at x% profit, and another at y% loss, with neither profit nor loss on the whole. What did the second cost?'",
             r"Rs \(330\) at \(10\%\) profit, then \(5\%\) loss: profit Rs \(30\), second \(=\frac{30}{5}\times 100=\text{Rs }600\).",
             r"Taking \(x\%\) of Rs \(A\) as the profit."),
    72: card(72, "Profit at One Discount from the Profit at Another",
             r"With the marked price as 100, the cost is fixed by the first discount and profit; the second discount gives a new price on the same cost.",
             r"\[ \text{New profit}=\left((100+P)\frac{100-x_2}{100-x_1}-100\right)\% \]",
             [("Cost (MP = 100)", r"\frac{100(100-x_1)}{100+P}"), ("New price", r"100-x_2"), ("Profit", r"(100+P)\frac{100-x_2}{100-x_1}-100")],
             r"A larger discount lowers the profit; it can turn into a loss.",
             "'If a discount of x1% gives a profit of P%, what is the profit per cent at a discount of x2%?'",
             r"\(5\%\) off gives \(14\%\) profit; at \(20\%\) off: \(114\times\frac{80}{95}-100=-4\), a loss of \(4\%\).",
             r"Taking off \(x_2-x_1\) from the profit per cent."),
}

Q69 = ("{n1} works out his profit as a per cent of the selling price, while {n2} works it out as a per cent of the cost price. They sell at the "
       "same price; {n1} makes {x}% profit and {n2} makes {y}%, and {n1}'s profit is Rs {A} more than {n2}'s. Find the selling price.")
Q69S = ("{n1} works out his profit as a per cent of the selling price, while {n2} works it out as a per cent of the cost price. They sell at the "
        "same price and each makes {x}% profit, but {n1}'s profit is Rs {A} more than {n2}'s. Find the selling price.")
Q70 = ("A dealer sells two {items} for Rs {A} in all. The cost price of the first is the same as the selling price of the second. The first "
       "is sold at a loss of {x}% and the second at a gain of {y}%. Find his total gain or loss in rupees.")
Q71 = ("A shop sells a {item} for Rs {A} at a profit of {x}%. It sells a second {item} at a loss of {y}%, and on the two sales together it "
       "makes neither profit nor loss. What did the second {item} cost?")
Q72 = "When a shop gives {x1}% off the marked price of a {item}, it makes a profit of {P}%. What is its profit per cent if it gives {x2}% off instead?"


def pt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):g}"


OLD = {69: {406: (("Arjun", "Kiran"), (40, 30, 110))}, 70: {}, 71: {407: ("cupboard", (650, 30, 12))}, 72: {408: ("rug", (15, 36, 25))}}
NEW = {69: [("r69_n", (("Sohan", "Mohit"), (20, 20, 50))), ("r69_e1", (("Raju", "Vikas"), (60, 50, 480))), ("r69_e2", (("Anil", "Deepak"), (12, 8, 62))),
            ("r69_e3", (("Gopal", "Manoj"), (35, 30, 93))), ("r69_e4", (("Hari", "Suresh"), (24, 20, 176))), ("r69_e5", (("Naveen", "Prakash"), (8, 4, 54)))],
       70: [("r70_ex", ("cows", (1440, 20, 60))), ("r70_e1", ("bikes", (1140, 10, 20))), ("r70_e2", ("boats", (1920, 8, 25))),
            ("r70_e3", ("carts", (1200, 40, 50))), ("r70_e4", ("ponies", (2050, 36, 25))), ("r70_e5", ("buffaloes", (1880, 12, 60)))],
       71: [("r71_e1", ("bench", (540, 35, 8))), ("r71_e2", ("desk", (580, 16, 4))), ("r71_e3", ("sofa", (1360, 36, 9))),
            ("r71_e4", ("bed", (490, 40, 14))), ("r71_e5", ("shelf", (756, 8, 16)))],
       72: [("r72_e1", ("lamp", (6, 41, 20))), ("r72_e2", ("watch", (F(25, 2), 40, 20))), ("r72_e3", ("bag", (10, 35, 16))),
            ("r72_e4", ("coat", (20, 50, 28))), ("r72_e5", ("radio", (30, 40, 44)))]}


def build(rule, spec):
    if rule == 69:
        (n1, n2), (x, y, A) = spec
        g = r69(x, y, A, n1, n2)
        q = (Q69S if x == y else Q69).format(n1=n1, n2=n2, x=x, y=y, A=A)
        return g, q, ropts(g["answer"][1])
    if rule == 70:
        items, (A, x, y) = spec
        g = r70(A, x, y)
        return g, Q70.format(items=items, A=A, x=x, y=y), rsopts(g["answer"][1])
    if rule == 71:
        item, (A, x, y) = spec
        g = r71(A, x, y, item)
        return g, Q71.format(item=item, A=A, x=x, y=y), ropts(g["answer"][1])
    item, (x1, P, x2) = spec
    g = r72(x1, P, x2)
    return g, Q72.format(item=item, x1=pt(x1), P=P, x2=x2), popts(g["answer"][1])


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, spec)
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
    for r in (69, 70, 71, 72):
        main(r)
