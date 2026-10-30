"""Profit and Loss Rule 46 (2026-10-30): part n of a stock sold at x% profit - at what profit per cent must the rest be sold for an
overall profit of y%? (The book's rule allows a loss when y < xn; its example and all its exercises ask for a gain, and so do these.)
Writes the card, regenerates old row 341 (the book's example) with a simple-style sentence, a new setting and all-new numbers, and
adds the 5 book exercises. Same layout as gen_45.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_39 import fr, frac_txt  # noqa: E402

T46 = (r"If part \(n\) of a stock is sold at a profit of \(x\%\), then for an overall profit of \(y\%\) the rest must be sold at"
       r"<br>\[ \frac{y-xn}{1-n}\% \]a profit if positive, a loss if negative.")


def r46(A, n, x, y):
    A, n, x, y = map(F, (A, n, x, y))
    v = (y - x * n) / (1 - n)
    assert v > 0
    first_cost, rest_cost = A * n, A * (1 - n)
    first_sp, need = first_cost * (100 + x) / 100, A * (100 + y) / 100
    trad = steps(
        ("Cost of the part sold first and its selling price.", rf"\[ {fr(n)}\times {m(A)} = {m(first_cost)},\qquad {m(first_cost)}\times\frac{{{tex(100 + x)}}}{{100}} = {m(first_sp)} \]"),
        ("Takings needed for the overall profit.", rf"\[ {m(A)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(need)} \]"),
        ("The rest must bring in the difference.", rf"Rest costs \({m(rest_cost)}\) and must sell for \({m(need)} - {m(first_sp)} = {m(need - first_sp)}\):"
                                                   rf"\[ \frac{{{m(need - first_sp)} - {m(rest_cost)}}}{{{m(rest_cost)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(n = {fr(n)}\), \(x = {tex(x)}\), \(y = {tex(y)}\) (the cost Rs \({tex(A)}\) is not needed)."),
        ("Apply the specified rule.", r"\[ \frac{y-xn}{1-n}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(y)} - {tex(x)}\times {fr(n)}}}{{1 - {fr(n)}}} = \frac{{{tex(y - x * n)}}}{{{tex(1 - n)}}} = {tex(v)}\% \]"
                                   r"<br>It is positive, so it is a profit."))
    rb = [rf"\(n = {fr(n)}\), \(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\(y - xn = {tex(y - x * n)}\), \(1 - n = {fr(1 - n)}\).",
          rf"Profit on the rest \(= {tex(v)}\%\)."]
    return result(("number", v), T46, trad, rule, P(v), rb, rf"\[ \frac{{{tex(y - x * n)}}}{{{fr(1 - n)}}} = {tex(v)}\% \]")


CARD = card(46, "Part Sold at a Profit: Rate Needed on the Rest",
            r"After selling part \(n\) of a stock at a profit of \(x\%\), the rest must bring the profit on the whole cost to \(y\%\). "
            r"The first part has already earned \(xn\) per cent of the whole cost.",
            r"\[ r=\frac{y-xn}{1-n}\%\quad(\text{a profit if positive, a loss if negative}) \]",
            [("Overall", r"nx+(1-n)r=y"), ("Rest", r"r=\frac{y-xn}{1-n}")],
            r"When \(y\gt xn\) the rest needs a profit; when \(y\lt xn\) it can even be sold at a loss.",
            "'A man buys goods for Rs A and sells part n at a profit of x%. At what gain per cent should he sell the remainder to gain y% on the whole?'",
            r"\(\frac{1}{2}\) at \(10\%\) profit, overall \(15\%\): \(\frac{15-5}{\frac{1}{2}}=20\%\) profit on the rest.",
            r"Taking \(y-x\) without weighting the first part by \(n\).")

TPL = ("A grocer buys {item} for Rs {A}. She sells {n} of it at a profit of {x}%. At what per cent profit must she sell the rest to make "
       "a profit of {y}% on the whole?")
QS = {341: ("rice", (6300, F(2, 7), 4, 14))}
NEW = [("r46_e1", "oats", (2800, F(1, 4), 8, 14)), ("r46_e2", "millet", (3600, F(3, 5), 15, 21)),
       ("r46_e3", "maize", (4500, F(1, 3), 30, 22)), ("r46_e4", "barley", (6400, F(5, 8), 16, 13)),
       ("r46_e5", "lentils", (2700, F(4, 9), 27, 32))]


def q_of(item, c):
    A, n, x, y = c
    return TPL.format(item=item, A=A, n=frac_txt(n), x=x, y=y)


def main():
    folder = os.path.join(HERE, "rule46")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(QS)
    out = []
    for rid, (item, c) in QS.items():
        g = r46(*c)
        op, _ = popts(g["answer"][1])
        extra = {"question": q_of(item, c), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_46", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": "Rule 46", "rule_html": CARD}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW:
        g = r46(*c)
        op, pos = popts(g["answer"][1])
        qs.append(new_question(46, q_of(item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 46: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
