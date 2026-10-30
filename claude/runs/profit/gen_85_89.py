"""Profit and Loss Rules 85-89 (2026-10-30). Rule 85: bought x% below the labelled price, sold y% above it - profit on the price paid.
Rule 86: sold at Rs A after x% discount; without it the profit would be y% - the cost. Rule 87: x% wholesale discount, Rs A paid,
y% profit on the company's original price - the total selling price. Rule 88: sold at Rs A after x% discount with y% profit - the
profit without the discount. Rule 89: bought X a rupee - how many a rupee for a gain of x%. (85 and 88 share one formula, as do 52 and
89; the book gives each its own rule.) None of the five has an old row; this writes the five cards and the book's examples and
exercises as new questions with new settings and all-new numbers. Usage: python gen_85_89.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_57_60 import copts  # noqa: E402

T85 = (r"If an article is bought at \(x\%\) below the labelled price and sold at \(y\%\) above the labelled price, the profit on the "
       r"price paid is<br>\[ \frac{x+y}{100-x}\times 100\% \]")
T86 = (r"If articles sold at Rs \(A\) each after an \(x\%\) discount would have given \(y\%\) profit without the discount, each cost"
       r"<br>\[ \text{Rs }\frac{100^2\,A}{(100-x)(100+y)} \]")
T87 = (r"If Rs \(A\) is paid after an \(x\%\) discount on the company's price and the goods are sold at \(y\%\) profit on that "
       r"original price, the total selling price is<br>\[ \text{Rs }\frac{100+y}{100-x}\times A \]")
T88 = (r"If an article sold after an \(x\%\) discount gives a profit of \(y\%\), then without the discount the profit would be"
       r"<br>\[ \frac{x+y}{100-x}\times 100\% \]")
T89 = r"If articles are bought at \(X\) a rupee, then to gain \(x\%\) the number to sell for a rupee is<br>\[ X\times\frac{100}{100+x} \]"


def r85(x, y):
    x, y = F(x), F(y)
    v = (x + y) / (100 - x) * 100
    trad = steps(("Take the labelled price as 100.", rf"Paid \(= 100 - {tex(x)} = {tex(100 - x)}\); sold for \(100 + {tex(y)} = {tex(100 + y)}\)."),
                 ("Profit on the price paid.", rf"\[ \frac{{{tex(100 + y)} - {tex(100 - x)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T85.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)} + {tex(y)}}}{{100 - {tex(x)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x + y = {tex(x + y)}\).", rf"\(100 - x = {tex(100 - x)}\).", rf"Profit \(= {tex(v)}\%\)."]
    return result(("number", v), T85, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(x + y)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]")


def r86(A, x, y):
    A, x, y = map(F, (A, x, y))
    lp = A * 100 / (100 - x)
    cp = lp * 100 / (100 + y)
    trad = steps(("Labelled price.", rf"Rs \({m(A)}\) is \({tex(100 - x)}\%\) of it: \[ {m(A)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(lp)} \]"),
                 ("Without the discount the profit is " + tex(y) + "%.", rf"So the labelled price is \({tex(100 + y)}\%\) of the cost: \[ {m(lp)}\times\frac{{100}}{{{tex(100 + y)}}} = {m(cp)} \]"))
    rule = steps(("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T86.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{10000\times {m(A)}}}{{{tex(100 - x)}\times {tex(100 + y)}}} = {m(cp)} \]"))
    rb = [rf"Labelled price \(= {m(lp)}\).", rf"Cost \(= {m(lp)}\times\frac{{100}}{{{tex(100 + y)}}}\).", rf"\(= {m(cp)}\)."]
    return result(("number", cp), T86, trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{10000\times {m(A)}}}{{{tex(100 - x)}\times {tex(100 + y)}}} = {m(cp)} \]")


def r87(A, x, y):
    A, x, y = map(F, (A, x, y))
    orig = A * 100 / (100 - x)
    sp = orig * (100 + y) / 100
    trad = steps(("The company's original price.", rf"Rs \({m(A)}\) is \({tex(100 - x)}\%\) of it: \[ {m(A)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(orig)} \]"),
                 ("Selling price with " + tex(y) + "% on that price.", rf"\[ {m(orig)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(sp)} \]"))
    rule = steps(("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T87.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(100 + y)}}}{{{tex(100 - x)}}}\times {m(A)} = {m(sp)} \]"))
    rb = [rf"Original price \(= {m(orig)}\).", rf"\(\times\frac{{{tex(100 + y)}}}{{100}}\).", rf"Total selling price \(= {m(sp)}\)."]
    return result(("number", sp), T87, trad, rule, rf"Rs \({m(sp)}\)", rb, rf"\[ \frac{{{tex(100 + y)}}}{{{tex(100 - x)}}}\times {m(A)} = {m(sp)} \]")


def r88(A, x, y):
    A, x, y = map(F, (A, x, y))
    cp, lp = A * 100 / (100 + y), A * 100 / (100 - x)
    v = (lp - cp) / cp * 100
    trad = steps(("Cost and labelled price from Rs " + tex(A) + ".", rf"Cost \(= {m(A)}\times\frac{{100}}{{{tex(100 + y)}}} = {m(cp)}\); labelled price \(= {m(A)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(lp)}\)."),
                 ("Profit at the labelled price.", rf"\[ \frac{{{m(lp)} - {m(cp)}}}{{{m(cp)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\) (Rs \({m(A)}\) is not needed)."), ("Apply the specified rule.", T88.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)} + {tex(y)}}}{{100 - {tex(x)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x + y = {tex(x + y)}\).", rf"\(100 - x = {tex(100 - x)}\).", rf"Profit without the discount \(= {tex(v)}\%\)."]
    return result(("number", v), T88, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(x + y)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]")


def r89(X, x, item):
    X, x = F(X), F(x)
    v = X * 100 / (100 + x)
    trad = steps(("Cost of one.", rf"\({tex(X)}\) cost Re \(1\), so one costs Re \(\frac{{1}}{{{tex(X)}}}\); for the gain it must sell for \(\frac{{1}}{{{tex(X)}}}\times\frac{{{tex(100 + x)}}}{{100}} = {tex((100 + x) / (100 * X))}\)."),
                 ("Number sold for Re 1.", rf"\[ 1 \div {tex((100 + x) / (100 * X))} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"\(X = {tex(X)}\), \(x = {tex(x)}\)."), ("Apply the specified rule.", T89.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ {tex(X)}\times\frac{{100}}{{{tex(100 + x)}}} = {tex(v)} \]"))
    rb = [rf"\(X = {tex(X)}\), \(x = {tex(x)}\).", rf"\({tex(X)}\times\frac{{100}}{{{tex(100 + x)}}}\).", rf"\(= {tex(v)}\) a rupee."]
    return result(("number", v), T89, trad, rule, rf"\({tex(v)}\) {item} a rupee", rb, rf"\[ {tex(X)}\times\frac{{100}}{{{tex(100 + x)}}} = {tex(v)} \]")


CARDS = {
    85: card(85, "Bought Below the Labelled Price, Sold Above It",
             r"On a labelled price of 100 the buyer pays \(100-x\) and sells for \(100+y\); the profit \(x+y\) is measured on what was paid.",
             r"\[ \text{Profit}=\frac{x+y}{100-x}\times 100\% \]",
             [("Paid", r"100-x"), ("Sold", r"100+y"), ("Profit %", r"\frac{x+y}{100-x}\times 100")],
             r"It is the same working as Rule 60.",
             "'A bought an article at x% discount on the labelled price and sold it at y% profit on the labelled price. What was his profit on the price he paid?'",
             r"\(10\%\) below, \(17\%\) above: \(\frac{27}{90}\times 100=30\%\).",
             r"Answering \(x+y\) - that is the profit on the labelled price."),
    86: card(86, "Cost from the Discounted Price and the Profit Without Discount",
             r"Undo the discount to get the labelled price, then undo the profit that the labelled price would have given.",
             r"\[ \text{CP}=\frac{100^2\,A}{(100-x)(100+y)} \]",
             [("Labelled price", r"\frac{100A}{100-x}"), ("Cost", r"\frac{\text{LP}\times 100}{100+y}")],
             r"The profit per cent is the one the labelled price would give, not the one actually made.",
             "'A shopkeeper sold articles at Rs A each after x% discount; without the discount he would have earned y% profit. Find the cost of each.'",
             r"Rs \(540\) after \(10\%\) off, \(20\%\) profit without it: \(\frac{10000\times 540}{90\times 120}=\text{Rs }500\).",
             r"Taking off \(x\%\) and \(y\%\) from Rs \(A\) in one step."),
    87: card(87, "Wholesale Discount, Profit on the Company's Price",
             r"The amount paid is \((100-x)\%\) of the company's price; the trader's selling price is \((100+y)\%\) of that company price.",
             r"\[ \text{Total SP}=\frac{100+y}{100-x}\times A \]",
             [("Company price", r"\frac{100A}{100-x}"), ("Selling price", r"\frac{100+y}{100}\times\text{company price}")],
             r"The profit here is on the original company price, not on what the trader paid.",
             "'A company gives x% discount to wholesale buyers; a trader pays Rs A and sells at y% profit on the original company price. Find the total selling price.'",
             r"\(20\%\) off, Rs \(400\) paid, \(10\%\) on the company price: \(\frac{110}{80}\times 400=\text{Rs }550\).",
             r"Adding \(y\%\) to the price paid."),
    88: card(88, "Profit If No Discount Had Been Given",
             r"The labelled price is the discounted price divided by \(\frac{100-x}{100}\); compare it with the cost found from the profit made.",
             r"\[ \text{Profit without discount}=\frac{x+y}{100-x}\times 100\% \]",
             [("Cost", r"\frac{100A}{100+y}"), ("Labelled price", r"\frac{100A}{100-x}"), ("Profit %", r"\frac{x+y}{100-x}\times 100")],
             r"The selling price Rs \(A\) is not needed for the per cent.",
             "'A shopkeeper sold an article for Rs A after x% discount and made y% profit. What would the profit per cent have been without the discount?'",
             r"\(20\%\) off, \(8\%\) profit: \(\frac{28}{80}\times 100=35\%\).",
             r"Adding \(x+y\)."),
    89: card(89, "Bought X a Rupee: How Many a Rupee for a Gain",
             r"Each article must sell for \((100+x)\%\) of its cost, so fewer must be sold for a rupee.",
             r"\[ \text{Number a rupee}=X\times\frac{100}{100+x} \]",
             [("Cost of one", r"\frac{1}{X}"), ("Price of one", r"\frac{1}{X}\cdot\frac{100+x}{100}"), ("Number a rupee", r"\frac{100X}{100+x}")],
             r"It is the same working as Rule 52.",
             "'If oranges are bought at X for a rupee, how many must be sold for a rupee to gain x%?'",
             r"\(40\) a rupee, gain \(25\%\): \(40\times\frac{100}{125}=32\).",
             r"Multiplying by \(\frac{100+x}{100}\)."),
}
Q85 = "{who} buys an article at {x}% off its labelled price and sells it at {y}% above the labelled price. What is the profit per cent on the price paid?"
Q86 = ("A shop sells {items} at Rs {A} each after a discount of {x}% on the labelled price. Without the discount it would have made a profit "
       "of {y}% on the cost. Find the cost of each {item}.")
Q87 = ("A wholesaler gives a discount of {x}% to bulk buyers. A trader pays Rs {A} after the discount and fixes his selling price so that he "
       "makes a profit of {y}% on the company's original price. Find his total selling price.")
Q88 = ("A shop sells a {item} for Rs {A} after a discount of {x}% on the labelled price and makes a profit of {y}%. What would its profit "
       "per cent have been without the discount?")
Q89 = "A vendor buys {item} at {X} a rupee. How many should she sell for a rupee to make a gain of {x}%?"


def pt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):g}"


NEW = {85: [("r85_ex", ("Kavya", 25, 35)), ("r85_e1", ("Ritu", 36, 12)), ("r85_e2", ("Sameer", F(25, 2), F(45, 2))), ("r85_e3", ("Imran", 10, 17)),
            ("r85_e4", ("Neha", 40, 20)), ("r85_e5", ("Tarun", 16, 26))],
       86: [("r86_ex", ("lamps", "lamp", 648, 20, 35)), ("r86_e1", ("shirts", "shirt", 720, 4, 25)), ("r86_e2", ("desks", "desk", 2070, 10, 15)),
            ("r86_e3", ("kettles", "kettle", 420, 16, 25)), ("r86_e4", ("stools", "stool", 342, 24, 50)), ("r86_e5", ("beds", "bed", 1120, 30, 60))],
       87: [("r87_ex", (6000, 20, 12)), ("r87_e1", (9000, 25, 6)), ("r87_e2", (4500, 10, 8)), ("r87_e3", (2100, 16, 5)), ("r87_e4", (3500, 30, 9))],
       88: [("r88_ex", ("heater", 630, 10, 26)), ("r88_e1", ("fan", 528, 12, 10)), ("r88_e2", ("cooler", 960, 20, 28)), ("r88_e3", ("sofa", 1170, 10, 17)),
            ("r88_e4", ("mixer", 459, 15, 2)), ("r88_e5", ("printer", 819, 9, 17)), ("r88_e6", ("television", 13800, 8, 15))],
       89: [("r89_ex", ("lemons", 36, 20)), ("r89_e1", ("guavas", 28, 12)), ("r89_e2", ("plums", 45, 25)), ("r89_e3", ("limes", 63, 26)),
            ("r89_e4", ("pears", 26, 30)), ("r89_e5", ("figs", 69, 15))]}


def build(rule, spec):
    if rule == 85:
        who, x, y = spec
        g = r85(x, y)
        return g, Q85.format(who=who, x=pt(x), y=pt(y)), popts(g["answer"][1])
    if rule == 86:
        items, item, A, x, y = spec
        g = r86(A, x, y)
        return g, Q86.format(items=items, item=item, A=A, x=x, y=y), ropts(g["answer"][1])
    if rule == 87:
        A, x, y = spec
        g = r87(A, x, y)
        return g, Q87.format(A=A, x=x, y=y), ropts(g["answer"][1])
    if rule == 88:
        item, A, x, y = spec
        g = r88(A, x, y)
        return g, Q88.format(item=item, A=A, x=x, y=y), popts(g["answer"][1])
    item, X, x = spec
    g = r89(X, x, item)
    return g, Q89.format(item=item, X=X, x=x), copts(g, item)


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None and dump["rows"] == []
    json.dump([], open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"))
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (85, 86, 87, 88, 89):
        main(r)
