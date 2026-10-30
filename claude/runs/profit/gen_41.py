"""Profit and Loss Rule 41 (2026-10-30): two items bought for Rs P together, one sold at x% loss and the other at y% gain, both for
the same price - find both cost prices. Writes the card, regenerates old row 335 (the book's example) with a simple-style
sentence, a new setting and all-new numbers, and adds the 5 book exercises. Same layout as gen_36.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402

T41 = (r"If two items bought for Rs \(P\) together are sold, one at a loss of \(x\%\) and the other at a gain of \(y\%\), for the same "
       r"price, then<br>\[ \text{CP (loss item)}=\frac{P(100+y)}{(100-x)+(100+y)} \]<br>"
       r"\[ \text{CP (gain item)}=\frac{P(100-x)}{(100-x)+(100+y)} \]")  # two lines: on one line it was wider than the solution box


def r41(P, x, y):
    P, x, y = map(F, (P, x, y))
    s = (100 - x) + (100 + y)
    a = P * (100 + y) / s
    b = P * (100 - x) / s
    trad = steps(
        ("Let the item sold at a loss cost Rs \\(c\\).", rf"Then the other costs Rs \(({m(P)} - c)\)."),
        ("Both are sold for the same price.", rf"\[ \frac{{{tex(100 - x)}}}{{100}}c = \frac{{{tex(100 + y)}}}{{100}}({m(P)} - c) \]"),
        ("Solve.", rf"\[ {tex(s)}c = {m(P * (100 + y))} \;\Rightarrow\; c = {m(a)},\quad {m(P)} - c = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(P = {m(P)}\), \(x = {tex(x)}\), \(y = {tex(y)}\); \((100 - x) + (100 + y) = {tex(s)}\)."),
        ("Apply the specified rule.", T41.split("<br>", 1)[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)},\qquad \frac{{{m(P)}\times {tex(100 - x)}}}{{{tex(s)}}} = {m(b)} \]"))
    fin = rf"sold at a loss Rs \({m(a)}\), sold at a gain Rs \({m(b)}\)"
    rb = [rf"\((100 - {tex(x)}) + (100 + {tex(y)}) = {tex(s)}\).", rf"Loss item \(= \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)}\).",
          rf"Gain item \(= {m(P)} - {m(a)} = {m(b)}\)."]
    sc = rf"\[ \frac{{{m(P)}\times {tex(100 + y)}}}{{{tex(s)}}} = {m(a)},\quad \frac{{{m(P)}\times {tex(100 - x)}}}{{{tex(s)}}} = {m(b)} \]"
    return result(("pair", (a, b)), T41, trad, rule, fin, rb, sc)


def opts(g):
    a, b = (F(t) for t in g["answer"][1])
    P = lambda t: rf"Rs \({m(t[0])}\) and Rs \({m(t[1])}\)"
    return place(P((a, b)), [P((b, a)), P((a + 20, b - 20)), P((a - 20, b + 20))])


CARD = card(41, "Two Items Sold for the Same Price, One at a Loss and One at a Gain",
            r"Two items cost Rs \(P\) together. One is sold at a loss of \(x\%\), the other at a gain of \(y\%\), and both fetch the same price, "
            r"so \((100-x)\%\) of one cost equals \((100+y)\%\) of the other.",
            T41.split("<br>", 1)[1],
            [("Same price", r"(100-x)c_1=(100+y)c_2"), ("Costs in ratio", r"c_1:c_2=(100+y):(100-x)"), ("Share Rs P", r"c_1=\frac{P(100+y)}{(100-x)+(100+y)}")],
            r"The item sold at a loss is the dearer one - it needs a bigger cost to fetch the same price.",
            "'A person bought two items for Rs P. He sold one at x% loss and the other at y% gain, and each was sold at the same price. Find the cost prices.'",
            r"Rs \(500\), loss \(10\%\), gain \(35\%\): \(90+135=225\); loss item \(=\frac{500\times 135}{225}=\text{Rs }300\), gain item Rs \(200\).",
            r"Putting \(100-x\) on top for the loss item - the loss item's share goes with \(100+y\).")

TPL = ("A man buys two {item} for Rs {P}. He sells one at a loss of {x}% and the other at a gain of {y}%, and both are sold at the same "
       "price. Find the cost price of the {one} sold at a loss and of the {one} sold at a gain.")
QS = {335: ("cycles", "cycle", (900, 25, 50))}
NEW = [("r41_e1", "cows", "cow", (840, 30, 40)), ("r41_e2", "sheep", "sheep", (1045, 5, 14)),
       ("r41_e3", "lamps", "lamp", (990, 12, 10)), ("r41_e4", "stools", "stool", (567, 16, 5)),
       ("r41_e5", "mirrors", "mirror", (621, 8, 15))]


def q_of(item, one, c):
    P, x, y = c
    return TPL.format(item=item, one=one, P=P, x=x, y=y)


def main():
    folder = os.path.join(HERE, "rule41")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(QS)
    out = []
    for rid, (item, one, c) in QS.items():
        g = r41(*c)
        op, _ = opts(g)
        extra = {"question": q_of(item, one, c), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_41", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": "Rule 41", "rule_html": CARD}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, one, c in NEW:
        g = r41(*c)
        op, pos = opts(g)
        qs.append(new_question(41, q_of(item, one, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, ["pair", [str(v) for v in g["answer"][1]]]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 41: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
