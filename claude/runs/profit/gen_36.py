"""Profit and Loss Rule 36 (2026-10-30): two items sold one at x% profit and the other at y% loss for an overall gain of Rs X, and
the other way round for no profit and no loss - find both cost prices. Writes the card, regenerates old row 329 (the book's
example) with a simple-style sentence, a new setting and all-new numbers, and adds the 5 book exercises. Same layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402

T36 = (r"If an item A is sold at \(x\%\) profit and an item B at \(y\%\) loss for an overall gain of Rs \(X\), while A at \(y\%\) loss and "
       r"B at \(x\%\) profit give neither gain nor loss, then<br>\[ \text{CP of A}=\frac{Xx}{x^2-y^2}\times 100,\qquad "
       r"\text{CP of B}=\frac{Xy}{x^2-y^2}\times 100 \]")


def r36(x, y, X, A="table", B="chair"):
    x, y, X = map(F, (x, y, X))
    a = 100 * X * x / (x * x - y * y)
    b = 100 * X * y / (x * x - y * y)
    trad = steps(
        ("Write the two statements.", rf"Let the {A} cost \(a\) and the {B} \(b\). First sale: \(\frac{{{tex(x)}}}{{100}}a - \frac{{{tex(y)}}}{{100}}b = {m(X)}\). "
                                      rf"Second sale: \(-\frac{{{tex(y)}}}{{100}}a + \frac{{{tex(x)}}}{{100}}b = 0\)."),
        ("Use the second statement.", rf"\[ {tex(x)}b = {tex(y)}a \;\Rightarrow\; b = \frac{{{tex(y)}}}{{{tex(x)}}}a \]"),
        ("Put it in the first.", rf"\[ \frac{{{tex(x)}}}{{100}}a - \frac{{{tex(y)}}}{{100}}\times\frac{{{tex(y)}}}{{{tex(x)}}}a = {m(X)} \;\Rightarrow\; a = {m(a)},\quad b = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\); \(x^2 - y^2 = {tex(x * x - y * y)}\)."),
        ("Apply the specified rule.", T36.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(X)}\times {tex(x)}}}{{{tex(x * x - y * y)}}}\times 100 = {m(a)},\qquad \frac{{{m(X)}\times {tex(y)}}}{{{tex(x * x - y * y)}}}\times 100 = {m(b)} \]"))
    fin = rf"{A} Rs \({m(a)}\), {B} Rs \({m(b)}\)"
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\).", rf"\(x^2 - y^2 = {tex(x * x - y * y)}\).", rf"{A.capitalize()} \(= {m(a)}\), {B} \(= {m(b)}\)."]
    sc = rf"\[ \frac{{{m(X)}\times {tex(x)}\times 100}}{{{tex(x * x - y * y)}}} = {m(a)},\quad \frac{{{m(X)}\times {tex(y)}\times 100}}{{{tex(x * x - y * y)}}} = {m(b)} \]"
    return result(("pair", (a, b)), T36, trad, rule, fin, rb, sc)


def opts(g, A, B):
    a, b = (F(t) for t in g["answer"][1])
    P = lambda t: rf"{A.capitalize()} Rs \({m(t[0])}\), {B} Rs \({m(t[1])}\)"
    return place(P((a, b)), [P((b, a)), P((a + 20, b)), P((a, b + 20))])


CARD = card(36, "Two Items, a Gain One Way and Nothing the Other Way",
            r"Item A at a profit of \(x\%\) and item B at a loss of \(y\%\) give a gain of Rs \(X\); A at a loss of \(y\%\) and B at a "
            r"profit of \(x\%\) give no gain and no loss. The two statements fix both cost prices.",
            T36.split("<br>")[1],
            [("Second sale balances", r"\frac{y}{100}a=\frac{x}{100}b\Rightarrow b=\frac{y}{x}a"), ("First sale", r"\frac{x}{100}a-\frac{y}{100}b=X"),
             ("Solve", r"a=\frac{100Xx}{x^2-y^2},\ b=\frac{100Xy}{x^2-y^2}")],
            r"The 'no gain, no loss' sale says the loss on A equals the gain on B, which ties the two costs together.",
            "'A person sells his table at x% profit and his chair at y% loss and gains Rs X; selling the table at y% loss and the chair at x% profit he neither gains nor loses.'",
            r"\(35\%\), \(15\%\), Rs \(40\): \(x^2-y^2=1000\); table \(=\frac{40\times 35\times 100}{1000}=\text{Rs }140\), chair \(=\text{Rs }60\).",
            r"Writing \(x-y\) in place of \(x^2-y^2\).")

QS = {329: ("bed", "sofa", r"A man sells his bed at a profit of 35% and his sofa at a loss of 20%, and gains Rs 165 on the whole. Had he sold the bed at a loss of 20% "
                           r"and the sofa at a profit of 35%, he would have neither gained nor lost. Find the cost price of the bed and of the sofa.", (35, 20, 165))}
NEW = [("r36_e1", "desk", "lamp", r"A shop sells a desk at a profit of 15% and a lamp at a loss of 5%, gaining Rs 284 in all. Selling the desk at a loss of 5% and the lamp "
                                  r"at a profit of 15% would give no gain and no loss. Find the cost price of each.", (15, 5, 284)),
       ("r36_e2", "cupboard", "stool", r"A trader makes a profit of 30% on a cupboard and a loss of 15% on a stool, and gains Rs 225 on both. If he sold the cupboard at a loss of "
                                       r"15% and the stool at a profit of 30%, he would break even. Find the cost of each.", (30, 15, 225)),
       ("r36_e3", "fan", "heater", r"A woman sells a fan at a gain of 34% and a heater at a loss of 26%, and gains Rs 120 overall. Selling the fan at a loss of 26% and the "
                                   r"heater at a gain of 34% would leave her with neither profit nor loss. What did each cost?", (34, 26, 120)),
       ("r36_e4", "radio", "clock", r"A man sells a radio at a profit of 36% and a clock at a loss of 24%, and gains Rs 105 altogether. With the radio at a loss of 24% and the "
                                    r"clock at a profit of 36% he would gain nothing and lose nothing. Find the cost price of each.", (36, 24, 105)),
       ("r36_e5", "carpet", "mirror", r"A dealer sells a carpet at a profit of 45% and a mirror at a loss of 30%, gaining Rs 78 on the two. Had the carpet been sold at a loss "
                                      r"of 30% and the mirror at a profit of 45%, there would have been no gain and no loss. Find the cost of each.", (45, 30, 78))]


def main():
    folder = os.path.join(HERE, "rule36")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == [329]
    out = []
    for rid, (A, B, q, c) in QS.items():
        g = r36(*c, A, B)
        op, _ = opts(g, A, B)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_36", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    c = {"rule_name": "Rule 36", "rule_html": CARD}
    json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, A, B, q, cc in NEW:
        g = r36(*cc, A, B)
        op, pos = opts(g, A, B)
        qs.append(new_question(36, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, ["pair", [str(v) for v in g["answer"][1]]]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 36: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
