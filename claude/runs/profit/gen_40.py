"""Profit and Loss Rule 40 (2026-10-30): part x of a stock sold at m% profit and the rest at n% loss gives an overall profit of
Rs P - find the value of the stock. Writes the card, regenerates old rows 334 (the book's example) and 339 (the same example with
loss and profit swapped) with a simple-style sentence, a new setting and all-new numbers, and adds the 5 book exercises."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_13_17 import _k  # noqa: E402
from gen_39 import fr, frac_txt  # noqa: E402

T40 = (r"If part \(x\) of a stock is sold at \(m\%\) profit and the rest \(y = 1 - x\) at \(n\%\) loss, and the overall profit is "
       r"Rs \(P\), then<br>\[ \text{Value of the stock}=\frac{P\times 100}{mx-ny} \]")
OTHER = {"profit": "loss", "loss": "profit"}


def r40(x, a, b, P, word="profit", theorem=T40):
    x, a, b, P = map(F, (x, a, b, P))
    y = 1 - x
    w = a * x - b * y
    v = P * 100 / w
    o = OTHER[word]
    trad = steps(
        ("Let the value of the stock be Rs \\(V\\).", rf"\({fr(x)}V\) is sold at a {word} of \({tex(a)}\%\) and the rest, \({fr(y)}V\), at a {o} of \({tex(b)}\%\)."),
        (f"The overall {word} is the {word} on the first part less the {o} on the rest.",
         rf"\[ \frac{{{tex(a)}}}{{100}}\times {fr(x)}V - \frac{{{tex(b)}}}{{100}}\times {fr(y)}V = {m(P)} \]"),
        ("Solve.", rf"\[ \frac{{{tex(a * x)} - {tex(b * y)}}}{{100}}V = {m(P)} \;\Rightarrow\; V = {m(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {fr(x)}\), \(y = {fr(y)}\), \(m = {tex(a)}\), \(n = {tex(b)}\), \(P = {m(P)}\)"
                                 + ("." if word == "profit" else rf" (here the first part is at a loss and the rest at a profit, so the same rule gives the value from the overall loss).")),
        ("Apply the specified rule.", theorem.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(P)}\times 100}}{{{tex(a)}\times {fr(x)} - {tex(b)}\times {fr(y)}}} = \frac{{{m(P * 100)}}}{{{tex(w)}}} = {m(v)} \]"))
    rb = [rf"\(y = 1 - {fr(x)} = {fr(y)}\).", rf"\(mx - ny = {tex(a * x)} - {tex(b * y)} = {tex(w)}\).", rf"Value \(= \frac{{{m(P)}\times 100}}{{{tex(w)}}} = {m(v)}\)."]
    return result(("number", v), theorem, trad, rule, rf"Rs \({m(v)}\)", rb, rf"\[ \frac{{{m(P)}\times 100}}{{{tex(w)}}} = {m(v)} \]")


CARD = card(40, "Part at a Profit, the Rest at a Loss: Find the Value",
            r"When part \(x\) of a stock earns \(m\%\) and the rest \(y\) loses \(n\%\), the whole stock earns \(mx-ny\) per cent, and the "
            r"overall profit Rs \(P\) is that rate of the value.",
            T40.split("<br>")[1],
            [("Rest", r"y=1-x"), ("Overall rate", r"mx-ny\ \text{per cent}"), ("Value", r"\frac{P\times 100}{mx-ny}")],
            r"If the first part is sold at a loss and the rest at a profit, and there is an overall loss, the same formula gives the value.",
            "'x of a consignment was sold at m% profit and the rest at n% loss; the overall profit was Rs P. Find the value of the consignment.'",
            r"\(\frac{1}{2}\) at \(20\%\) profit, rest at \(10\%\) loss, profit Rs \(50\): \(10-5=5\), value \(=\frac{5000}{5}=\text{Rs }1000\).",
            r"Adding \(ny\) instead of taking it away - the loss on the rest lowers the overall rate.")

TPL = ("A dealer sells {x} of a lot of {item} at a {w} of {a}% and the rest at a {o} of {b}%. "
       "If his overall {w} is Rs {P}, find the value of the lot.")
QS = {334: ("shoes", (F(3, 4), 12, 8, 350), "profit")}
NEW = [("r40_e1", "toys", (F(2, 5), 30, 15, 45)),
       ("r40_e2", "pens", (F(5, 6), 18, 30, 270)),
       ("r40_e3", "umbrellas", (F(7, 10), 20, 30, 115)),
       ("r40_e4", "fans", (F(5, 8), 40, 24, 128)),
       ("r40_e5", "chairs", (F(4, 9), 45, 9, 90))]


def q_of(item, c, w="profit"):
    x, a, b, P = c
    return TPL.format(x=frac_txt(x), item=item, w=w, o=OTHER[w], a=a, b=b, P=P)


def main():
    folder = os.path.join(HERE, "rule40")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert set(QS) <= set(rows)  # row 339 (the loss version) moved to its own rule on 2026-10-30
    out = []
    for rid, (item, c, w) in QS.items():
        g = r40(*c, word=w)
        op, _ = ropts(g["answer"][1])
        extra = {"question": q_of(item, c, w), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_40", extra))
    _k[0] += 1  # row 339 used one answer position here before it moved; keeps the applied payload reproducible
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": "Rule 40", "rule_html": CARD}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW:
        g = r40(*c)
        op, pos = ropts(g["answer"][1])
        qs.append(new_question(40, q_of(item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 40: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
