"""Profit and Loss Rule 42 (2026-10-30): a stock bought at one price, m units sold at x% profit and the other n units at y% profit
- find the profit per cent on the whole. Writes the card, regenerates old rows 336 (the book's example) and 337 (Exercise 1, a
fraction of the stock) with a simple-style sentence, a new setting and all-new numbers, and adds Exercises 2-4. Same layout as
gen_37.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402

T42 = r"If \(m\) units of a stock are sold at \(x\%\) profit and the other \(n\) units at \(y\%\) profit, the profit on the whole is<br>\[ \frac{mx+ny}{m+n}\% \]"


def r42(N, price, k, x, y, unit="unit"):
    N, price, k, x, y = map(F, (N, price, k, x, y))
    n = N - k
    cost = N * price
    s1, s2 = k * price * (100 + x) / 100, n * price * (100 + y) / 100
    v = (s1 + s2 - cost) / cost * 100
    trad = steps(
        ("Cost of the whole stock.", rf"\[ {tex(N)}\times {m(price)} = {m(cost)} \]"),
        ("Selling price of the two parts.", rf"\[ {tex(k)}\times {m(price)}\times\frac{{{tex(100 + x)}}}{{100}} = {m(s1)},\qquad "
                                            rf"{tex(n)}\times {m(price)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(s2)} \]"),
        ("Profit per cent.", rf"\[ \frac{{{m(s1 + s2)} - {m(cost)}}}{{{m(cost)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(m = {tex(k)}\), \(x = {tex(x)}\), \(n = {tex(n)}\), \(y = {tex(y)}\) (the price per {unit} is not needed)."),
        ("Apply the specified rule.", r"\[ \frac{mx+ny}{m+n}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(k)}\times {tex(x)} + {tex(n)}\times {tex(y)}}}{{{tex(N)}}} = \frac{{{tex(k * x + n * y)}}}{{{tex(N)}}} = {tex(v)}\% \]"))
    rb = [rf"\(m = {tex(k)}\), \(n = {tex(n)}\).", rf"\(mx + ny = {tex(k * x + n * y)}\).", rf"Profit \(= \frac{{{tex(k * x + n * y)}}}{{{tex(N)}}} = {tex(v)}\%\)."]
    return result(("number", v), T42, trad, rule, P(v), rb, rf"\[ \frac{{{tex(k * x + n * y)}}}{{{tex(N)}}} = {tex(v)}\% \]")


CARD = card(42, "Part of a Stock at x% Profit, the Rest at y% Profit",
            r"When all units cost the same, the profit on the whole is the average of the two rates weighted by the number of units "
            r"sold at each rate.",
            r"\[ \text{Profit}=\frac{mx+ny}{m+n}\% \]",
            [("Profit on part 1", r"\frac{mx}{100}\ \text{units' cost}"), ("Profit on part 2", r"\frac{ny}{100}\ \text{units' cost}"),
             ("On the whole", r"\frac{mx+ny}{m+n}\%")],
            r"The price per unit drops out, so it is not needed; if a fraction of the stock is given, turn it into a number of units first.",
            "'A person buys a stock; he sells m units at x% profit and the remaining n units at y% profit. What is his profit per cent?'",
            r"\(10\) at \(5\%\), \(30\) at \(25\%\): \(\frac{50+750}{40}=20\%\).",
            r"Taking the plain average \(\frac{x+y}{2}\) when the two parts are not equal.")

OLD = {336: (lambda: r42(40, 250, 24, 15, 25, "bag"),
             r"A shopkeeper buys 40 bags of flour at Rs 250 per bag. He sells 24 bags at a profit of 15% and the other 16 bags at a profit of 25%. "
             r"Find his profit per cent on the whole."),
       337: (lambda: r42(60, 4, 15, 6, 14, "orange"),
             r"A girl buys 60 oranges at Rs 4 each. She sells \(\frac{1}{4}\) of them at a profit of 6% and the rest at a profit of 14%. "
             r"Find her profit per cent on the whole.")}
NEW = [("r42_e2", r"A trader buys 35 dozen shirts at Rs 900 per dozen. He sells 14 dozen at a profit of 11% and the other 21 dozen at a profit of 16%. "
                  r"Find his profit per cent on the whole.", lambda: r42(35, 900, 14, 11, 16, "dozen")),
       ("r42_e3", r"A shop buys 18 dozen candles at Rs 45 per dozen. It sells 11 dozen at a profit of 9% and the other 7 dozen at a profit of 9%. "
                  r"Find its profit per cent on the whole.", lambda: r42(18, 45, 11, 9, 9, "dozen")),
       ("r42_e4", r"A boy buys 45 lemons at Rs 6 each. He sells 27 lemons at a profit of 10% and the rest at a profit of 35%. "
                  r"Find his profit per cent on the whole.", lambda: r42(45, 6, 27, 10, 35, "lemon"))]


def main():
    folder = os.path.join(HERE, "rule42")
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
        out.append(regen_entry(rows[rid], g, "NEW_RULE_42", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    c = {"rule_name": "Rule 42", "rule_html": CARD}
    json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, q, fn in NEW:
        g = fn()
        op, pos = popts(g["answer"][1])
        qs.append(new_question(42, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 42: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
