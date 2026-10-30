"""Profit and Loss Rules 77-80 (2026-10-30). Rule 77: the selling price raised to n times, the profit was x% - the new profit. Rule 78:
parts of a stock at different gains / losses - the result on the whole (and the book's "had he sold all of it at r% he would have made
Rs D more" exercises - the cost per kg). Rule 79: profit counted as x% of the selling price - the profit on the cost (and the selling
price from the cost). Rule 80: loss counted as x% of the selling price - the loss on the cost. None of the four has an old row; this
writes the four cards and the book's examples and exercises as new questions with new settings and all-new numbers.
Usage: python gen_77_80.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_39 import fr, frac_txt  # noqa: E402
from gen_57_60 import gopts  # noqa: E402

T77 = r"If the selling price is raised to \(n\) times and the profit was \(x\%\), the new profit is<br>\[ [(100+x)n-100]\% \]"
T78 = (r"If parts \(n_1, n_2, n_3, \dots\) of a stock (adding up to 1) are sold at \(x_1\%, x_2\%, x_3\%, \dots\) (a loss counts as negative), "
       r"the result on the whole is<br>\[ (n_1x_1+n_2x_2+n_3x_3+\cdots)\% \]a gain if positive, a loss if negative.")
T79 = r"If the profit is \(x\%\) of the selling price, the profit on the cost price is<br>\[ \frac{x}{100-x}\times 100\% \]"
T80 = r"If the loss is \(x\%\) of the selling price, the loss on the cost price is<br>\[ \frac{x}{100+x}\times 100\% \]"


def r77(n, x):
    n, x = F(n), F(x)
    v = (100 + x) * n - 100
    trad = steps(
        ("Take the cost price as 100.", rf"The old selling price is \({tex(100 + x)}\)."),
        ("The new selling price.", rf"\[ {tex(n)}\times {tex(100 + x)} = {tex((100 + x) * n)} \]"),
        ("New profit per cent.", rf"\[ {tex((100 + x) * n)} - 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {tex(x)}\)."), ("Apply the specified rule.", T77.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ {tex(100 + x)}\times {tex(n)} - 100 = {tex(v)}\% \]"))
    rb = [rf"\(100 + x = {tex(100 + x)}\).", rf"\(\times {tex(n)} = {tex((100 + x) * n)}\).", rf"New profit \(= {tex(v)}\%\)."]
    return result(("number", v), T77, trad, rule, PCT(v), rb, rf"\[ {tex(100 + x)}\times {tex(n)} - 100 = {tex(v)}\% \]")


def word(r):
    return "gain" if r > 0 else "loss"


def r78(parts):
    """parts: [(fraction, signed rate)], the last fraction is the rest."""
    parts = [(F(f), F(r)) for f, r in parts]
    assert sum(f for f, _ in parts) == 1
    v = sum(f * r for f, r in parts)
    D = 1
    for f, _ in parts:
        D = D * f.denominator // __import__("math").gcd(D, f.denominator)
    whole = 100 * D
    lines = [rf"\({fr(f)}\) of it costs \({tex(f * whole)}\) and is sold at a {word(r)} of \({tex(abs(r))}\%\): {word(r)} \({tex(abs(f * whole * r / 100))}\)." for f, r in parts]
    total = sum(f * whole * r / 100 for f, r in parts)
    trad = steps(
        (f"Take the whole stock to cost {tex(whole)}.", "<br>".join(lines)),
        ("Result on the whole.", rf"Net \(= {tex(total)}\) on \({tex(whole)}\), i.e. \(\frac{{{tex(total)}}}{{{tex(whole)}}}\times 100 = {tex(v)}\%\)." + (" It is negative, so a loss." if v < 0 else "")))
    terms = " + ".join(rf"{fr(f)}\times ({tex(r)})" for f, r in parts)
    rule = steps(("Identify the values.", r"Parts and per cents (loss negative): " + ", ".join(rf"\({fr(f)}\) at \({tex(r)}\)" for f, r in parts) + "."),
                 ("Apply the specified rule.", T78.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ {terms} = {tex(v)}\% \]"))
    rb = [r"Weight each per cent by its part.", rf"\({' + '.join(tex(f * r) for f, r in parts)} = {tex(v)}\).", rf"Result \(= {tex(v)}\%\)."]
    fin = rf"a {word(v)} of \({tex(abs(v))}\%\)"
    return result(("signed", v), T78, trad, rule, fin, rb, rf"\[ {' + '.join(tex(f * r) for f, r in parts)} = {tex(v)}\% \]")


def r78_kg(W, parts, r, Dm):
    W, r, Dm = F(W), F(r), F(Dm)
    parts = [(F(f), F(x)) for f, x in parts]
    w = sum(f * x for f, x in parts)
    cost = Dm * 100 / (r - w)
    per = cost / W
    terms = " + ".join(rf"{fr(f)}\times {tex(x)}" for f, x in parts)
    trad = steps(
        ("Let the cost be Rs \\(c\\) a kg.", rf"The whole costs \({tex(W)}c\). The parts gain " + ", ".join(rf"\({tex(x)}\%\) on \({tex(f * W)}c\)" for f, x in parts) + "."),
        ("Gain on the parts and at the single rate.", rf"\[ \left({' + '.join(tex(f * x * W / 100) for f, x in parts)}\right)c = {tex(w * W / 100)}c,\qquad {tex(r)}\%\text{{ of }}{tex(W)}c = {tex(r * W / 100)}c \]"),
        ("The difference is given.", rf"\[ {tex((r - w) * W / 100)}c = {m(Dm)} \;\Rightarrow\; c = {m(per)} \]"))
    rule = steps(("Identify the values.", rf"Parts and per cents: \({terms}\); single rate \({tex(r)}\%\); difference Rs \({m(Dm)}\)."),
                 ("Apply the specified rule.", T78.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ {terms} = {tex(w)}\% \]<br>"                           # three lines: one was wider than the box
                                            rf"\[ ({tex(r)} - {tex(w)})\%\text{{ of the cost}} = {m(Dm)} \;\Rightarrow\; \text{{cost}} = {m(cost)} \]<br>"
                                            rf"\[ \text{{per kg}} = \frac{{{m(cost)}}}{{{tex(W)}}} = {m(per)} \]"))
    rb = [rf"Mixed rate \(= {tex(w)}\%\).", rf"\({tex(r - w)}\%\) of the cost \(= {m(Dm)}\), cost \(= {m(cost)}\).", rf"Per kg \(= {m(per)}\)."]
    return result(("number", per), T78, trad, rule, rf"Rs \({m(per)}\) a kg", rb, rf"\[ \frac{{{m(Dm)}\times 100}}{{{tex(r - w)}}}\div {tex(W)} = {m(per)} \]")


def r79(x):
    x = F(x)
    v = x / (100 - x) * 100
    trad = steps(("Take the selling price as 100.", rf"Profit \(= {tex(x)}\), so the cost \(= 100 - {tex(x)} = {tex(100 - x)}\)."),
                 ("Profit on the cost.", rf"\[ \frac{{{tex(x)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\)."), ("Apply the specified rule.", T79.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)}}}{{100 - {tex(x)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\).", rf"\(\frac{{{tex(x)}}}{{{tex(100 - x)}}}\times 100\).", rf"\(= {tex(v)}\%\)."]
    return result(("number", v), T79, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(x)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]")


def r79_sp(C, x):
    C, x = F(C), F(x)
    sp = C * 100 / (100 - x)
    trad = steps(("Take the selling price as 100.", rf"Profit \(= {tex(x)}\), so the cost is \({tex(100 - x)}\%\) of the selling price."),
                 ("Selling price.", rf"\[ {m(C)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(sp)} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), cost Rs \({m(C)}\)."), ("Apply the specified rule.", T79.split("<br>")[1]),
                 ("Substitute the values.", rf"Profit on the cost \(= \frac{{{tex(x)}}}{{{tex(100 - x)}}}\times 100 = {tex(x / (100 - x) * 100)}\%\), so "
                                            rf"\[ \text{{SP}} = {m(C)}\times\left(1 + \frac{{{tex(x)}}}{{{tex(100 - x)}}}\right) = {m(sp)} \]"))
    rb = [rf"Profit on cost \(= {tex(x / (100 - x) * 100)}\%\).", rf"SP \(= {m(C)}\times\frac{{100}}{{{tex(100 - x)}}}\).", rf"\(= {m(sp)}\)."]
    return result(("number", sp), T79, trad, rule, rf"Rs \({m(sp)}\)", rb, rf"\[ {m(C)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(sp)} \]")


def r80(x):
    x = F(x)
    v = x / (100 + x) * 100
    trad = steps(("Take the selling price as 100.", rf"Loss \(= {tex(x)}\), so the cost \(= 100 + {tex(x)} = {tex(100 + x)}\)."),
                 ("Loss on the cost.", rf"\[ \frac{{{tex(x)}}}{{{tex(100 + x)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\)."), ("Apply the specified rule.", T80.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)}}}{{100 + {tex(x)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\).", rf"\(\frac{{{tex(x)}}}{{{tex(100 + x)}}}\times 100\).", rf"\(= {tex(v)}\%\)."]
    return result(("number", v), T80, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(x)}}}{{{tex(100 + x)}}}\times 100 = {tex(v)}\% \]")


CARDS = {
    77: card(77, "Selling Price Raised to n Times",
             r"On a cost of 100 the old price is \(100+x\); \(n\) times it is \(n(100+x)\).",
             r"\[ \text{New profit}=[(100+x)n-100]\% \]",
             [("Old price", r"100+x"), ("New price", r"n(100+x)"), ("Profit", r"n(100+x)-100")],
             r"The profit per cent does not just become \(n\) times.",
             "'A shopkeeper increases the selling price n times; the first gain was x%. Find the new gain per cent.'",
             r"Price doubled, first gain \(30\%\): \(2\times 130-100=160\%\).",
             r"Answering \(nx\)."),
    78: card(78, "Parts of a Stock at Different Gains and Losses",
             r"The result on the whole is the average of the per cents, each weighted by its share of the stock; losses count as negative.",
             r"\[ (n_1x_1+n_2x_2+n_3x_3+\cdots)\% \]",
             [("Weights", r"n_1+n_2+n_3+\cdots=1"), ("Losses", r"x_i\lt 0"), ("Whole", r"\sum n_ix_i")],
             r"To compare with a single rate \(r\%\), the gap \((r-\sum n_ix_i)\%\) of the whole cost is the money lost or gained by not using it.",
             "'A person sells n1 of his property at x1% gain, n2 at x2% gain and the rest at x3% loss. What is his overall gain or loss per cent?'",
             r"\(\frac{1}{2}\) at \(10\%\) gain, \(\frac{1}{2}\) at \(6\%\) loss: \(5-3=2\%\) gain.",
             r"Forgetting the minus sign of a loss."),
    79: card(79, "Profit Counted on the Selling Price",
             r"If the profit is \(x\%\) of the selling price, then on a selling price of 100 the cost is \(100-x\), and the true profit per cent is on that cost.",
             r"\[ \text{Profit on cost}=\frac{x}{100-x}\times 100\% \]",
             [("SP", r"100"), ("Profit", r"x"), ("Cost", r"100-x")],
             r"The profit on the cost is always more than the same profit on the selling price.",
             "'If a merchant estimates his profit as x% of the selling price, what is his real profit per cent?'",
             r"\(30\%\) of SP: \(\frac{30}{70}\times 100=42\frac{6}{7}\%\).",
             r"Answering \(x\%\)."),
    80: card(80, "Loss Counted on the Selling Price",
             r"If the loss is \(x\%\) of the selling price, then on a selling price of 100 the cost is \(100+x\), and the true loss per cent is on that cost.",
             r"\[ \text{Loss on cost}=\frac{x}{100+x}\times 100\% \]",
             [("SP", r"100"), ("Loss", r"x"), ("Cost", r"100+x")],
             r"The loss on the cost is always less than the same loss on the selling price.",
             "'If a merchant estimates his loss as x% of the selling price, what is his real loss per cent?'",
             r"\(40\%\) of SP: \(\frac{40}{140}\times 100=28\frac{4}{7}\%\).",
             r"Dividing by \(100-x\)."),
}
Q77 = "A shop sells a {item} at a profit of {x}%. If it raises the selling price to {n} times the old price, what is its new profit per cent?"
Q79 = "A trader counts his profit as {x}% of the selling price. What is his profit as a per cent of the cost price?"
Q79S = "A man buys a {item} for Rs {C} and sells it at a profit of {x}% of the selling price. Find the selling price."
Q80 = "A trader counts his loss as {x}% of the selling price. What is his loss as a per cent of the cost price?"


def pt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):g}"


def q78(parts):
    bits = []
    for i, (f, r) in enumerate(parts):
        lead = "the rest" if i == len(parts) - 1 else frac_txt(F(f)) + (" of her stock of cloth" if i == 0 else " of it")
        bits.append(f"{lead} at a {word(r)} of {pt(abs(r))}%")
    body = ", ".join(bits[:-1]) + " and " + bits[-1]
    return f"A woman sells {body}. What is her gain or loss per cent on all of it?"


def q78_kg(W, item, parts, r, Dm):
    bits = []
    for i, (f, x) in enumerate(parts):
        lead = "the rest" if i == len(parts) - 1 else frac_txt(F(f)) + (" of it" if i == 0 else "")
        bits.append(f"{lead} at a gain of {pt(x)}%")
    body = ", ".join(bits[:-1]) + " and " + bits[-1]
    return (f"A merchant buys {W} kg of {item}. He sells {body}. Had he sold all of it at a gain of {pt(r)}%, he would have made "
            f"Rs {m(Dm)} more. Find the cost price per kg.")


NEW = {77: [("r77_ex", ("lamp", (3, 8))), ("r77_e1", ("mug", (2, 12))), ("r77_e2", ("vase", (2, 35))), ("r77_e3", ("clock", (3, F(25, 2)))),
            ("r77_e4", ("frame", (4, 10)))],
       78: [("r78_ex", ("pct", [(F(1, 6), 30), (F(1, 2), 14), (F(1, 3), -9)])),
            ("r78_e1", ("kg", (1500, "rice", [(F(1, 3), 6), (F(1, 2), 9), (F(1, 6), 15)], 12, 180))),
            ("r78_e2", ("kg", (2000, "wheat", [(F(1, 4), 4), (F(1, 5), 10), (F(1, 2), 14), (F(1, 20), 20)], 13, 120))),
            ("r78_e3", ("pct", [(F(3, 5), 15), (F(1, 10), 30), (F(3, 10), -25)])),
            ("r78_e4", ("pct", [(F(3, 8), 24), (F(1, 8), 16), (F(1, 2), -26)]))],
       79: [("r79_ex", ("pct", 40)), ("r79_e1", ("pct", 36)), ("r79_e2", ("pct", 28)), ("r79_e3", ("pct", 4)), ("r79_e4", ("pct", 35)),
            ("r79_e5", ("pct", 44)), ("r79_e6", ("sp", ("camera", 450, 25)))],
       80: [("r80_ex", 12), ("r80_e1", 4), ("r80_e2", 8), ("r80_e3", 60), ("r80_e4", 50), ("r80_e5", 35)]}


def build(rule, spec):
    if rule == 77:
        item, (n, x) = spec
        g = r77(n, x)
        return g, Q77.format(item=item, n=n, x=pt(x)), popts(g["answer"][1])
    if rule == 78:
        kind, c = spec
        if kind == "pct":
            g = r78(c)
            return g, q78(c), gopts(g["answer"][1])
        W, item, parts, r, Dm = c
        g = r78_kg(W, parts, r, Dm)
        return g, q78_kg(W, item, parts, r, Dm), ropts(g["answer"][1])
    if rule == 79:
        kind, c = spec
        if kind == "sp":
            item, C, x = c
            g = r79_sp(C, x)
            return g, Q79S.format(item=item, C=C, x=x), ropts(g["answer"][1])
        g = r79(c)
        return g, Q79.format(x=c), popts(g["answer"][1])
    g = r80(spec)
    return g, Q80.format(x=spec), popts(g["answer"][1])


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
        kind, v = g["answer"]
        answers.append([key, [kind, str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (77, 78, 79, 80):
        main(r)
