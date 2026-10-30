"""Profit and Loss Rules 47 and 48 (2026-10-30): part n of a stock sold at x% loss (Rule 47) or x% profit (Rule 48) - at what profit
(Rule 47) or loss (Rule 48) per cent must the rest be sold for no profit and no loss on the whole? Writes both cards, regenerates
old rows 342 (Rule 47's example) and 343 (Rule 48's example) with a simple-style sentence, a new setting and all-new numbers, and
adds the 5 book exercises of each rule. Same layout as gen_45.py. Usage: python gen_47_48.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_39 import fr, frac_txt  # noqa: E402

WORDS = {47: ("loss", "profit"), 48: ("profit", "loss")}
TH = {n: rf"If part \(n\) of a stock is sold at a {a} of \(x\%\), then for no profit and no loss on the whole the rest must be sold at a {b} of"
         r"<br>\[ \frac{xn}{1-n}\% \]" for n, (a, b) in WORDS.items()}


def r4748(rule, A, n, x):
    A, n, x = map(F, (A, n, x))
    first, then = WORDS[rule]
    v = x * n / (1 - n)
    sgn = -1 if first == "loss" else 1
    first_cost, rest_cost = A * n, A * (1 - n)
    first_sp = first_cost * (100 + sgn * x) / 100
    rest_sp = A - first_sp
    trad = steps(
        ("Cost of the part sold first and its selling price.", rf"\[ {fr(n)}\times {m(A)} = {m(first_cost)},\qquad {m(first_cost)}\times\frac{{{tex(100 + sgn * x)}}}{{100}} = {m(first_sp)} \]"),
        ("For no profit and no loss the takings must equal the cost.", rf"The rest costs \({m(rest_cost)}\) and must sell for \({m(A)} - {m(first_sp)} = {m(rest_sp)}\)."),
        (f"{then.capitalize()} per cent on the rest.", rf"\[ \frac{{|{m(rest_sp)} - {m(rest_cost)}|}}{{{m(rest_cost)}}}\times 100 = {tex(v)}\% \]"))
    rule_s = steps(
        ("Identify the values.", rf"\(n = {fr(n)}\), \(x = {tex(x)}\) (the cost Rs \({tex(A)}\) is not needed)."),
        ("Apply the specified rule.", r"\[ \frac{xn}{1-n}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(x)}\times {fr(n)}}}{{1 - {fr(n)}}} = \frac{{{tex(x * n)}}}{{{tex(1 - n)}}} = {tex(v)}\% \]"))
    rb = [rf"\(n = {fr(n)}\), \(x = {tex(x)}\).", rf"\(xn = {tex(x * n)}\), \(1 - n = {fr(1 - n)}\).", rf"{then.capitalize()} on the rest \(= {tex(v)}\%\)."]
    return result(("number", v), TH[rule], trad, rule_s, P(v) if then == "profit" else rf"\({tex(v)}\%\) loss", rb,
                  rf"\[ \frac{{{tex(x * n)}}}{{{fr(1 - n)}}} = {tex(v)}\% \]")


CARDS = {
    47: card(47, "Part Sold at a Loss: Profit on the Rest for No Profit, No Loss",
             r"After selling part \(n\) of a stock at a loss of \(x\%\), the rest must earn back exactly that loss, which is \(xn\) per cent of "
             r"the whole cost, on its own cost \((1-n)\).",
             TH[47].split("<br>")[1],
             [("Balance", r"n(-x)+(1-n)r=0"), ("Rest", r"r=\frac{xn}{1-n}")],
             r"It is Rule 45 with the overall profit \(y=0\).",
             "'A person buys goods for Rs A and sells part n at a loss of x%. At what gain per cent should he sell the rest to make no profit and no loss?'",
             r"\(\frac{1}{2}\) at \(10\%\) loss: \(\frac{5}{\frac{1}{2}}=10\%\) profit on the rest.",
             r"Answering \(x\%\) - the rest is a different share of the cost."),
    48: card(48, "Part Sold at a Profit: Loss on the Rest for No Profit, No Loss",
             r"After selling part \(n\) of a stock at a profit of \(x\%\), the rest can be sold at a loss equal to that profit, which is \(xn\) "
             r"per cent of the whole cost, spread over its own cost \((1-n)\).",
             TH[48].split("<br>")[1],
             [("Balance", r"nx-(1-n)l=0"), ("Rest", r"l=\frac{xn}{1-n}")],
             r"The answer is a loss per cent on the rest.",
             "'A man buys goods for Rs A and sells part n at a profit of x%. At what per cent loss should he sell the rest to make no profit and no loss?'",
             r"\(\frac{1}{4}\) at \(12\%\) profit: \(\frac{3}{\frac{3}{4}}=4\%\) loss on the rest.",
             r"Dividing by \(n\) instead of by \(1-n\)."),
}
TPL = {47: "A shop buys {item} for Rs {A}. It sells {n} of them at a loss of {x}%. At what per cent profit must it sell the rest to make no profit and no loss on the whole?",
       48: "A grocer buys {item} for Rs {A}. She sells {n} of it at a profit of {x}%. At what per cent loss must she sell the rest to make no profit and no loss on the whole?"}
OLD = {47: {342: ("lamps", (3600, F(2, 5), 12))}, 48: {343: ("sugar", (5200, F(3, 8), 10))}}
NEW = {47: [("r47_e1", "bulbs", (2700, F(1, 3), 24)), ("r47_e2", "cups", (840, F(3, 7), 28)), ("r47_e3", "plates", (1350, F(1, 5), 36)),
            ("r47_e4", "bowls", (990, F(5, 8), 9)), ("r47_e5", "spoons", (4500, F(1, 6), 35))],
       48: [("r48_e1", "flour", (3900, F(1, 4), 27)), ("r48_e2", "salt", (2100, F(2, 7), 35)), ("r48_e3", "honey", (1800, F(3, 5), 8)),
            ("r48_e4", "ghee", (7200, F(1, 9), 56)), ("r48_e5", "butter", (2500, F(5, 6), 3))]}


def q_of(rule, item, c):
    A, n, x = c
    return TPL[rule].format(item=item, A=A, n=frac_txt(n), x=x)


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, (item, c) in OLD[rule].items():
        g = r4748(rule, *c)
        op, _ = popts(g["answer"][1])
        extra = {"question": q_of(rule, item, c), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW[rule]:
        g = r4748(rule, *c)
        op, pos = popts(g["answer"][1])
        qs.append(new_question(rule, q_of(rule, item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (47, 48):
        main(r)
