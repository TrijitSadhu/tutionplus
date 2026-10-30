"""Profit and Loss Rule 37 (2026-10-30): the cost price of x articles equals the selling price of y articles. Writes the card,
regenerates old rows 330 (the book's example) and 331 (a book exercise, "SP of 4/5 of the books = CP of all") with a simple-style
sentence, a new setting and all-new numbers, and adds the 5 book exercises. Same layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402

T37 = r"If the cost price of \(x\) articles equals the selling price of \(y\) articles, the profit is<br>\[ \frac{x-y}{y}\times 100\% \]"


def r37(x, y, note=""):
    x, y = F(x), F(y)
    v = (x - y) / y * 100
    trad = steps(
        ("Take the cost of one article as Re 1.", (note + " " if note else "") + rf"Then \({tex(x)}\) articles cost Rs \({tex(x)}\), and this is what \({tex(y)}\) articles sell for."),
        ("Selling price of one article.", rf"\[ \frac{{{tex(x)}}}{{{tex(y)}}} = {tex(x / y)} \]"),
        ("Profit on Re 1, then on Rs 100.", rf"\[ \left({tex(x / y)} - 1\right)\times 100 = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{x-y}{y}\times 100\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(x)} - {tex(y)}}}{{{tex(y)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", r"Profit \(= \frac{x-y}{y}\times 100\%\).", rf"\(\frac{{{tex(x - y)}}}{{{tex(y)}}}\times 100 = {tex(v)}\%\)."]
    return result(("number", v), T37, trad, rule, P(v), rb, rf"\[ \frac{{{tex(x - y)}}}{{{tex(y)}}}\times 100 = {tex(v)}\% \]")


CARD = card(37, "Cost of x Articles = Selling Price of y Articles",
            r"When the money paid for \(x\) articles is what \(y\) of them fetch, every \(y\) articles sold bring in the cost of \(x\).",
            r"\[ \text{Profit}=\frac{x-y}{y}\times 100\%\quad(\text{a loss of }\frac{y-x}{y}\times 100\%\text{ if }y\gt x) \]",
            [("Cost of one", r"1"), ("SP of one", r"\frac{x}{y}"), ("Profit", r"\left(\frac{x}{y}-1\right)\times 100=\frac{x-y}{y}\times 100")],
            r"Per cent profit is on the cost of the articles actually sold, which is the cost of \(y\) articles.",
            "'The cost price of x articles is equal to the selling price of y articles; find the profit per cent' (also 'I sell y for the money I paid for x').",
            r"Cost of \(15\) = SP of \(12\): \(\frac{15-12}{12}\times 100=25\%\).",
            r"Dividing by \(x\) instead of by \(y\) (\(\frac{3}{15}=20\%\) is wrong).")

OLD = {330: (lambda: r37(15, 12), r"The cost price of 15 pencils is the same as the selling price of 12 pencils. Find the profit per cent."),
       331: (lambda: r37(10, 9, r"Selling \(\frac{9}{10}\) of the books brings in the cost of all of them, so take \(10\) books: the price of \(9\) of them equals the cost of \(10\)."),
             r"A shopkeeper finds that selling \(\frac{9}{10}\) of his books brings in what all the books cost. What is his profit per cent?")}
NEW = [("r37_e1", r"The cost price of 35 cups equals the selling price of 28 cups. Find the gain per cent.", lambda: r37(35, 28)),
       ("r37_e2", r"I sell 21 bangles for the money I paid for 28 bangles. What is my gain per cent?", lambda: r37(28, 21)),
       ("r37_e4", r"By selling 45 metres of ribbon, a shop gains the cost of 9 metres. Find its gain per cent.",
        lambda: r37(54, 45, r"Selling \(45\) m brings in the cost of those \(45\) m plus the cost of \(9\) m more, i.e. the cost of \(54\) m.")),
       ("r37_e5", r"If the cost price of 18 plates is equal to the selling price of 12 plates, find the profit per cent.", lambda: r37(18, 12)),
       ("r37_e6", r"A fruit seller sells 150 apples at the cost price of 180 apples. What is his gain per cent?", lambda: r37(180, 150))]


def main():
    folder = os.path.join(HERE, "rule37")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD)
    out = []
    for rid, (fn, q) in OLD.items():
        g = fn()
        op, _ = popts(g["answer"][1])
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_37", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    c = {"rule_name": "Rule 37", "rule_html": CARD}
    json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, q, fn in NEW:
        g = fn()
        op, pos = popts(g["answer"][1])
        qs.append(new_question(37, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 37: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
