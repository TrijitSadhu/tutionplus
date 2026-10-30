"""Profit and Loss Rule 38 (2026-10-30): sold at x% profit; the cost price rises by Rs A and the selling price by Rs B, and the profit
becomes y%. Writes the card, regenerates old row 332 (the book's example) with a simple-style sentence, a new setting and all-new
numbers, and adds the 5 book exercises. Same layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_18_21 import ropts  # noqa: E402

T38 = (r"If an article sold at \(x\%\) profit has its cost price raised by Rs \(A\) and its selling price by Rs \(B\), and the profit "
       r"becomes \(y\%\), then<br>\[ \text{CP}=\frac{A-B+\frac{Ay}{100}}{x-y}\times 100 \]")


def r38(x, A, B, y):
    x, A, B, y = map(F, (x, A, B, y))
    cp = (A - B + A * y / 100) / (x - y) * 100
    trad = steps(
        ("Let the cost price be Rs \\(c\\).", rf"Selling price \(= \frac{{{tex(100 + x)}}}{{100}}c\). New cost \(= c + {m(A)}\); new selling price \(= \frac{{{tex(100 + x)}}}{{100}}c + {m(B)}\)."),
        ("The new price is " + tex(100 + y) + "% of the new cost.", rf"\[ \frac{{{tex(100 + x)}}}{{100}}c + {m(B)} = \frac{{{tex(100 + y)}}}{{100}}(c + {m(A)}) \]"),
        ("Solve.", rf"\[ \frac{{{tex(x - y)}}}{{100}}c = {m(A * (100 + y) / 100)} - {m(B)} \;\Rightarrow\; c = {m(cp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(A = {m(A)}\), \(B = {m(B)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T38.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(A)} - {m(B)} + \frac{{{m(A)}\times {tex(y)}}}{{100}}}}{{{tex(x)} - {tex(y)}}}\times 100 = \frac{{{m(A - B + A * y / 100)}}}{{{tex(x - y)}}}\times 100 = {m(cp)} \]"))
    rb = [rf"\(x = {tex(x)}\), \(A = {m(A)}\), \(B = {m(B)}\), \(y = {tex(y)}\).", rf"Numerator \(= {m(A - B + A * y / 100)}\), \(x - y = {tex(x - y)}\).", rf"CP \(= {m(cp)}\)."]
    return result(("number", cp), T38, trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{{m(A - B + A * y / 100)}}}{{{tex(x - y)}}}\times 100 = {m(cp)} \]")


CARD = card(38, "Cost Up by Rs A, Price Up by Rs B: the New Profit Is y%",
            r"If an article is sold at \(x\%\) profit and the cost goes up by Rs \(A\) while the price goes up by only Rs \(B\), the profit falls "
            r"to \(y\%\); one equation then gives the cost price.",
            T38.split("<br>")[1],
            [("Old", r"\text{SP}=\frac{100+x}{100}\text{CP}"), ("New", r"\text{SP}+B=\frac{100+y}{100}(\text{CP}+A)"),
             ("Solve", r"\text{CP}=\frac{A-B+\frac{Ay}{100}}{x-y}\times 100")],
            r"Write the new selling price as \(y\%\) more than the new cost and compare it with the old selling price plus \(B\).",
            "'An article is sold at x% profit. If its cost price is increased by Rs A and its selling price by Rs B, the profit becomes y%. Find the cost price.'",
            r"\(25\%\), Rs \(40\), Rs \(20\), \(20\%\): \(\frac{40-20+8}{5}\times 100=\text{Rs }560\).",
            r"Leaving out the \(\frac{Ay}{100}\) term - the new profit is on the larger cost.")

TPL = r"A {item} is sold at a profit of {x}%. If its cost price goes up by Rs {A} and its selling price by Rs {B}, the profit becomes {y}%. Find the cost price."
QS = {332: ("heater", (28, 45, 27, 22))}
NEW = [("r38_e1", "cooler", (15, 30, 18, 10)), ("r38_e2", "printer", (30, 40, 24, 20)), ("r38_e3", "geyser", (16, 36, 24, 12)),
       ("r38_e4", "blender", (24, 50, 35, 20)), ("r38_e5", "trolley", (40, 60, 48, 25))]


def q_of(item, c):
    x, A, B, y = c
    return TPL.format(item=item, x=x, A=A, B=B, y=y)


def main():
    folder = os.path.join(HERE, "rule38")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == [332]
    out = []
    for rid, (item, c) in QS.items():
        g = r38(*c)
        op, _ = ropts(g["answer"][1])
        extra = {"question": q_of(item, c), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_38", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": "Rule 38", "rule_html": CARD}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW:
        g = r38(*c)
        op, pos = ropts(g["answer"][1])
        qs.append(new_question(38, q_of(item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 38: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
