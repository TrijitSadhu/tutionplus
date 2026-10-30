"""Profit and Loss Rules 51 and 52 (2026-10-30). Rule 51: two items bought for Rs P together, sold at gains of x% and y% for the same
price - both cost prices (like Rule 41, with two gains). Rule 52: articles bought at A a rupee - how many a rupee to gain x%. Writes
both cards, regenerates old rows 348 (Rule 51's example) and 349 (Rule 52's example) with simple-style sentences, new settings and
all-new numbers, and adds the book exercises (5 for Rule 51, 4 for Rule 52). Usage: python gen_51_52.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402

T51 = (r"If two items A and B bought for Rs \(P\) together are sold at gains of \(x\%\) and \(y\%\) for the same price, then"
       r"<br>\[ \text{CP of A}=\frac{P(100+y)}{(100+x)+(100+y)} \]<br>\[ \text{CP of B}=\frac{P(100+x)}{(100+x)+(100+y)} \]")
T52 = r"If articles are bought at \(A\) a rupee, then to gain \(x\%\) they must be sold at<br>\[ A\times\frac{100}{100+x}\ \text{a rupee} \]"


def r51(P, x, y, A, B):
    P, x, y = map(F, (P, x, y))
    s = (100 + x) + (100 + y)
    a, b = P * (100 + y) / s, P * (100 + x) / s
    trad = steps(
        (f"Let the {A} cost Rs \\(c\\).", rf"Then the {B} costs Rs \(({m(P)} - c)\)."),
        ("Both are sold for the same price.", rf"\[ \frac{{{tex(100 + x)}}}{{100}}c = \frac{{{tex(100 + y)}}}{{100}}({m(P)} - c) \]"),
        ("Solve.", rf"\[ {tex(s)}c = {m(P * (100 + y))} \;\Rightarrow\; c = {m(a)},\quad {m(P)} - c = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(P = {m(P)}\), \(x = {tex(x)}\) ({A}), \(y = {tex(y)}\) ({B}); \((100 + x) + (100 + y) = {tex(s)}\)."),
        ("Apply the specified rule.", T51.split("<br>", 1)[1]),
        ("Substitute the values.", rf"\[ \text{{{A}}} = \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)} \]<br>"
                                   rf"\[ \text{{{B}}} = \frac{{{m(P)}\times {tex(100 + x)}}}{{{tex(s)}}} = {m(b)} \]"))
    fin = rf"{A} Rs \({m(a)}\), {B} Rs \({m(b)}\)"
    rb = [rf"\((100 + {tex(x)}) + (100 + {tex(y)}) = {tex(s)}\).", rf"{A.capitalize()} \(= \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)}\).",
          rf"{B.capitalize()} \(= {m(P)} - {m(a)} = {m(b)}\)."]
    sc = rf"\[ \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)},\quad \frac{{{m(P)}\times {tex(100 + x)}}}{{{tex(s)}}} = {m(b)} \]"
    return result(("pair", (a, b)), T51, trad, rule, fin, rb, sc)


def opts51(g, A, B):
    a, b = (F(t) for t in g["answer"][1])
    Q = lambda t: rf"{A.capitalize()} Rs \({m(t[0])}\), {B} Rs \({m(t[1])}\)"
    return place(Q((a, b)), [Q((b, a)), Q((a + 20, b - 20)), Q((a - 20, b + 20))])


def r52(A, x, item):
    A, x = F(A), F(x)
    v = A * 100 / (100 + x)
    trad = steps(
        ("Cost of one article.", rf"\({tex(A)}\) cost Re \(1\), so one costs Re \(\frac{{1}}{{{tex(A)}}}\)."),
        ("Selling price of one article for the gain.", rf"\[ \frac{{1}}{{{tex(A)}}}\times\frac{{{tex(100 + x)}}}{{100}} = {tex((100 + x) / (100 * A))} \]"),
        ("Number sold for Re 1.", rf"\[ 1 \div {tex((100 + x) / (100 * A))} = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(A = {tex(A)}\), \(x = {tex(x)}\)."),
        ("Apply the specified rule.", T52.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {tex(A)}\times\frac{{100}}{{{tex(100 + x)}}} = {tex(v)} \]"))
    rb = [rf"\(A = {tex(A)}\), \(x = {tex(x)}\).", rf"\({tex(A)}\times\frac{{100}}{{{tex(100 + x)}}}\).", rf"\(= {tex(v)}\) a rupee."]
    return result(("number", v), T52, trad, rule, rf"\({tex(v)}\) {item} a rupee", rb, rf"\[ {tex(A)}\times\frac{{100}}{{{tex(100 + x)}}} = {tex(v)} \]")


def opts52(g, item):
    v = F(g["answer"][1])
    Q = lambda t: rf"\({tex(t)}\) {item} a rupee"
    return place(Q(v), [Q(v + 1), Q(v - 2), Q(v + 3)])


CARDS = {
    51: card(51, "Two Items Sold for the Same Price at Two Gains",
             r"Two items cost Rs \(P\) together and are sold at gains of \(x\%\) and \(y\%\) for the same price, so \((100+x)\%\) of one cost equals "
             r"\((100+y)\%\) of the other.",
             r"\[ \text{CP of A}=\frac{P(100+y)}{(100+x)+(100+y)} \]",
             [("Same price", r"(100+x)c_A=(100+y)c_B"), ("Costs in ratio", r"c_A:c_B=(100+y):(100+x)"), ("Share Rs P", r"c_A=\frac{P(100+y)}{(100+x)+(100+y)}")],
             r"The item sold at the smaller gain is the dearer one.",
             "'A person bought two items for Rs P. He sold one at a gain of x% and the other at a gain of y%, and each was sold at the same price. Find the cost prices.'",
             r"Rs \(1240\), gains \(20\%\) and \(28\%\): A \(=\frac{1240\times 128}{248}=\text{Rs }640\), B Rs \(600\).",
             r"Pairing \(100+x\) with item A - item A's share goes with \(100+y\)."),
    52: card(52, "Bought at A a Rupee: How Many a Rupee for a Gain",
             r"Selling fewer articles for a rupee raises the price of each. For a gain of \(x\%\) each article must fetch \(\frac{100+x}{100}\) of its cost.",
             r"\[ \text{Number a rupee}=A\times\frac{100}{100+x} \]",
             [("Cost of one", r"\frac{1}{A}"), ("Price of one", r"\frac{1}{A}\times\frac{100+x}{100}"), ("Number a rupee", r"\frac{100A}{100+x}")],
             r"For a gain the number sold for a rupee is smaller than the number bought for a rupee.",
             "'If toffees are bought at A a rupee, how many must be sold for a rupee to gain x%?'",
             r"\(30\) a rupee, gain \(20\%\): \(30\times\frac{100}{120}=25\) a rupee.",
             r"Multiplying by \(\frac{100+x}{100}\) - that gives more articles a rupee, i.e. a loss."),
}

T51Q = ("A man buys a {A} and a {B} for Rs {P} in all. He sells the {A} at a gain of {x}% and the {B} at a gain of {y}%, and both fetch the "
        "same price. Find the cost price of each.")
T52Q = "A shop buys {item} at {A} a rupee. How many must it sell for a rupee to make a profit of {x}%?"
OLD = {51: {348: (("fan", "cooler"), (960, 15, 25))}, 52: {349: ("candies", (24, 20))}}
NEW = {51: [("r51_e1", ("desk", "shelf"), (1170, 8, 26)), ("r51_e2", ("lamp", "kettle"), (702, 30, 4)), ("r51_e3", ("rug", "mat"), (1008, 12, 40)),
            ("r51_e4", ("watch", "radio"), (1100, 50, 25)), ("r51_e5", ("bag", "trunk"), (1184, 36, 60))],
       52: [("r52_e1", "lemons", (26, 4)), ("r52_e2", "eggs", (18, F(25, 2))), ("r52_e3", "pencils", (35, 40)), ("r52_e4", "apples", (9, 50))]}


def pct_txt(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{float(x):g}"


def build(rule, item, c):
    if rule == 51:
        A, B = item
        P, x, y = c
        g = r51(P, x, y, A, B)
        return g, T51Q.format(A=A, B=B, P=P, x=x, y=y), opts51(g, A, B)
    A, x = c
    g = r52(A, x, item)
    return g, T52Q.format(item=item, A=A, x=pct_txt(x)), opts52(g, item)


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, (item, c) in OLD[rule].items():
        g, q, (op, _) = build(rule, item, c)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW[rule]:
        g, q, (op, pos) = build(rule, item, c)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        kind, v = g["answer"]
        answers.append([key, [kind, [str(t) for t in v] if kind == "pair" else str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (51, 52):
        main(r)
