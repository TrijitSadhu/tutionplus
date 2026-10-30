"""Profit and Loss Rules 73-76 (2026-10-30). Rule 73: two articles sold together for Rs S1 at x% and y% profit, and for Rs S2 with the
per cents swapped - both costs. Rule 74: selling at 1/n of the usual price would lose x% - the profit at the usual price. Rule 75: d%
more is gained by selling at Rs S2 than at Rs S1 - the cost. Rule 76: false weights, x% gained when buying and y% when selling - the
whole gain. Writes the four cards, regenerates old rows 409 (R74) and 410 (R75; its key pointed at a wrong option) with simple-style
sentences, new settings and all-new numbers (Rules 73 and 76 have no old row), and adds the book's examples and exercises.
Usage: python gen_73_76.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_39 import fr, frac_txt  # noqa: E402
from gen_53_56 import opts_pair  # noqa: E402

# ---------------------------------------------------------------- Rule 73
T73 = (r"If A and B are sold together for Rs \(S_1\) at \(x\%\) profit on A and \(y\%\) on B, and for Rs \(S_2\) at \(y\%\) on A and \(x\%\) "
       r"on B, then with \(p=\frac{100+x}{100}\), \(q=\frac{100+y}{100}\)<br>\[ \text{CP of A}=\frac{qS_2-pS_1}{q^2-p^2} \]<br>"
       r"\[ \text{CP of B}=\frac{qS_1-pS_2}{q^2-p^2} \]")


def r73(A_, B_, S1, x, y, S2):
    S1, S2, x, y = map(F, (S1, S2, x, y))
    p, q = (100 + x) / 100, (100 + y) / 100
    a = (q * S2 - p * S1) / (q * q - p * p)
    b = (q * S1 - p * S2) / (q * q - p * p)
    trad = steps(
        (f"Let the {A_} cost Rs \\(a\\) and the {B_} Rs \\(b\\).", rf"\[ {tex(p)}a + {tex(q)}b = {m(S1)},\qquad {tex(q)}a + {tex(p)}b = {m(S2)} \]"),
        ("Add and subtract the two sales.", rf"Adding: \({tex(p + q)}(a + b) = {m(S1 + S2)}\), so \(a + b = {m((S1 + S2) / (p + q))}\). "
                                            rf"Subtracting: \({tex(q - p)}(a - b) = {m(S2 - S1)}\), so \(a - b = {m((S2 - S1) / (q - p))}\)."),
        ("Solve.", rf"\[ a = {m(a)},\qquad b = {m(b)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(S_1 = {m(S1)}\), \(S_2 = {m(S2)}\), \(p = {tex(p)}\), \(q = {tex(q)}\)."),
        ("Apply the specified rule.", T73.split("<br>", 1)[1]),
        ("Substitute the values.", rf"\[ \text{{{A_}}} = \frac{{{tex(q)}\times {m(S2)} - {tex(p)}\times {m(S1)}}}{{{tex(q * q)} - {tex(p * p)}}} = {m(a)} \]<br>"
                                   rf"\[ \text{{{B_}}} = \frac{{{tex(q)}\times {m(S1)} - {tex(p)}\times {m(S2)}}}{{{tex(q * q)} - {tex(p * p)}}} = {m(b)} \]"))
    rb = [rf"\(q^2 - p^2 = {tex(q * q - p * p)}\).", rf"{A_.capitalize()} \(= {m(a)}\).", rf"{B_.capitalize()} \(= {m(b)}\)."]
    return result(("pair", (a, b)), T73, trad, rule, rf"{A_} Rs \({m(a)}\), {B_} Rs \({m(b)}\)", rb,
                  rf"\[ \frac{{{tex(q * S2 - p * S1)}}}{{{tex(q * q - p * p)}}} = {m(a)},\quad \frac{{{tex(q * S1 - p * S2)}}}{{{tex(q * q - p * p)}}} = {m(b)} \]")


# ---------------------------------------------------------------- Rule 74
T74 = (r"If selling an article at \(\frac{1}{n}\) of its price would give a loss of \(x\%\), then at the full price the profit is"
       r"<br>\[ [n(100-x)-100]\% \]")


def r74(k, x):
    k, x = F(k), F(x)                                   # k = the fraction of the price (1/n)
    n = 1 / k
    v = n * (100 - x) - 100
    trad = steps(
        ("Take the cost price as 100.", rf"At \({fr(k)}\) of the price the article sells for \(100 - {tex(x)} = {tex(100 - x)}\)."),
        ("The full price.", rf"\[ {tex(100 - x)} \div {fr(k)} = {tex(n * (100 - x))} \]"),
        ("Profit per cent.", rf"\[ {tex(n * (100 - x))} - 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(n = {tex(n)}\), \(x = {tex(x)}\)."),
        ("Apply the specified rule.", T74.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {tex(n)}\times({tex(100 - x)}) - 100 = {tex(v)}\% \]"))
    rb = [rf"\(n = {tex(n)}\), \(100 - x = {tex(100 - x)}\).", rf"\(n(100 - x) = {tex(n * (100 - x))}\).", rf"Profit \(= {tex(v)}\%\)."]
    return result(("number", v), T74, trad, rule, PCT(v), rb, rf"\[ {tex(n)}\times {tex(100 - x)} - 100 = {tex(v)}\% \]")


# ---------------------------------------------------------------- Rule 75
T75 = r"If \(d\%\) more is gained by selling an article for Rs \(S_2\) than for Rs \(S_1\), then<br>\[ \text{CP}=\frac{100(S_2-S_1)}{d} \]"


def r75(d, S2, S1):
    d, S2, S1 = map(F, (d, S2, S1))
    cp = 100 * (S2 - S1) / d
    trad = steps(
        ("Compare the two gains.", rf"The two gains differ by \({m(S2)} - {m(S1)} = {m(S2 - S1)}\) rupees, and by \({tex(d)}\%\) of the cost."),
        ("So", rf"\[ \frac{{{tex(d)}}}{{100}}\times\text{{CP}} = {m(S2 - S1)} \;\Rightarrow\; \text{{CP}} = {m(cp)} \]"),
        ("Check.", rf"Gains: \(\frac{{{m(S2 - cp)}}}{{{m(cp)}}}\times 100 = {tex((S2 - cp) / cp * 100)}\%\) and \({tex((S1 - cp) / cp * 100)}\%\), "
                   rf"a difference of \({tex(d)}\%\)."))
    rule = steps(
        ("Identify the values.", rf"\(d = {tex(d)}\), \(S_2 = {m(S2)}\), \(S_1 = {m(S1)}\)."),
        ("Apply the specified rule.", T75.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{100\times {m(S2 - S1)}}}{{{tex(d)}}} = {m(cp)} \]"))
    rb = [rf"\(S_2 - S_1 = {m(S2 - S1)}\).", rf"It is \({tex(d)}\%\) of the cost.", rf"CP \(= {m(cp)}\)."]
    return result(("number", cp), T75, trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{100\times {m(S2 - S1)}}}{{{tex(d)}}} = {m(cp)} \]")


# ---------------------------------------------------------------- Rule 76
T76 = (r"If a trader gains \(x\%\) by a false weight when buying and \(y\%\) when selling, his whole gain is"
       r"<br>\[ \left(\frac{(100+x)(100+y)}{100}-100\right)\% \]")


def r76(x, y):
    x, y = F(x), F(y)
    got = 100 + x
    sold = got * (100 + y) / 100
    v = sold - 100
    trad = steps(
        ("Buying.", rf"For Rs \(100\) he takes goods worth Rs \({tex(got)}\)."),
        ("Selling.", rf"He charges for \({tex(100 + y)}\%\) of what he hands over, so those goods bring in \({tex(got)}\times\frac{{{tex(100 + y)}}}{{100}} = {tex(sold)}\)."),
        ("Whole gain.", rf"\[ {tex(sold)} - 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T76.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{tex(100 + x)}\times {tex(100 + y)}}}{{100}} - 100 = {tex(v)}\% \]"))
    rb = [rf"\((100+x)(100+y) = {tex((100 + x) * (100 + y))}\).", rf"Divide by 100: \({tex(sold)}\).", rf"Gain \(= {tex(v)}\%\)."]
    return result(("number", v), T76, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(100 + x)}\times {tex(100 + y)}}}{{100}} - 100 = {tex(v)}\% \]")


CARDS = {
    73: card(73, "Two Sales of the Same Pair with the Per Cents Swapped",
             r"Two articles A and B are sold together twice; the profit per cents on A and B change places in the second sale. Two equations "
             r"give both costs.",
             r"\[ \text{CP of A}=\frac{qS_2-pS_1}{q^2-p^2},\qquad \text{CP of B}=\frac{qS_1-pS_2}{q^2-p^2} \]",
             [("First sale", r"pa+qb=S_1"), ("Second sale", r"qa+pb=S_2"), ("Add / subtract", r"a+b=\frac{S_1+S_2}{p+q},\ a-b=\frac{S_2-S_1}{q-p}")],
             r"Adding and subtracting the two sales is the quickest way by hand.",
             "'A farmer sold a cow and a calf for Rs S1 at x% and y% profit; selling them for Rs S2 he gets y% on the cow and x% on the calf. Find each cost.'",
             r"\(10\%\) and \(20\%\): sold for Rs \(340\) and Rs \(350\) - \(a+b=\frac{690}{2.3}=300\), \(a-b=\frac{10}{0.1}=100\), so \(a=200\), \(b=100\).",
             r"Pairing the wrong per cent with each article in the second sale."),
    74: card(74, "At a Fraction of the Price It Would Be a Loss",
             r"If \(\frac{1}{n}\) of the price is \((100-x)\%\) of the cost, the full price is \(n(100-x)\%\) of the cost.",
             r"\[ \text{Profit}=[n(100-x)-100]\% \]",
             [("Part price", r"100-x"), ("Full price", r"n(100-x)"), ("Profit", r"n(100-x)-100")],
             r"For half the price (\(n=2\)) the profit is \(100-2x\) per cent.",
             "'If there is a loss of x% when the article is sold at 1/n of its selling price, what is the profit per cent at the full price?'",
             r"At a quarter of the price a loss of \(70\%\): \(4\times 30-100=20\%\) profit.",
             r"Multiplying the loss by \(n\) instead of the part price."),
    75: card(75, "d% More Gained at a Higher Price",
             r"The two selling prices differ by Rs \(S_2-S_1\), and the two gains differ by \(d\%\) of the same cost, so that gap is \(d\%\) of the cost.",
             r"\[ \text{CP}=\frac{100(S_2-S_1)}{d} \]",
             [("Gap in rupees", r"S_2-S_1"), ("Gap in per cent", r"d\%\ \text{of CP}"), ("Cost", r"\frac{100(S_2-S_1)}{d}")],
             r"'More is gained at the lower price' cannot happen: the higher price always gives the bigger gain.",
             "'d% more is gained by selling an article for Rs S2 than by selling it for Rs S1. Find the cost price.'",
             r"\(4\%\) more at Rs \(520\) than at Rs \(500\): \(\frac{100\times 20}{4}=\text{Rs }500\).",
             r"Dividing the gap by the selling price."),
    76: card(76, "False Weights When Buying and When Selling",
             r"Cheating by \(x\%\) when buying gives goods worth \((100+x)\%\) of the money paid; cheating by \(y\%\) when selling charges for "
             r"\((100+y)\%\) of the goods handed over. The two act one after the other.",
             r"\[ \text{Gain}=\left(\frac{(100+x)(100+y)}{100}-100\right)\% \]",
             [("Buying", r"100\to 100+x"), ("Selling", r"(100+x)\frac{100+y}{100}"), ("Gain", r"\frac{(100+x)(100+y)}{100}-100")],
             r"The two per cents multiply; they do not just add.",
             "'A shopkeeper, on purchasing, deceives the seller by x% and on selling deceives the customer by y%. What is his whole gain?'",
             r"\(10\%\) and \(10\%\): \(\frac{110\times 110}{100}-100=21\%\).",
             r"Adding \(x+y\)."),
}

Q73 = ("A farmer sells a {A} and a {B} together for Rs {S1}, making a profit of {x}% on the {A} and {y}% on the {B}. Had he sold them for "
       "Rs {S2}, his profit would have been {y}% on the {A} and {x}% on the {B}. Find the cost price of each.")
Q74 = "If a shop sold a {item} at {k} of its usual price, it would make a loss of {x}%. What is its profit per cent at the usual price?"
Q75 = "A man sells a {item} for Rs {S2}. Had he sold it for Rs {S1}, his gain per cent would have been {d} less. What did the {item} cost him?"
Q76 = ("When buying, a trader takes {x}% more goods than he pays for, and when selling he charges for {y}% more goods than he hands over. "
       "What is his gain per cent on the whole?")


def pt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):g}"


OLD = {73: {}, 74: {409: ("kettle", (F(1, 3), 20))}, 75: {410: ("buffalo", (8, 1530, 1450))}, 76: {}}
NEW = {73: [("r73_ex", ("buffalo", "calf", (732, 8, 20, 750))), ("r73_e1", ("horse", "pony", (1320, 15, 40, F(2715, 2)))),
            ("r73_e2", ("cow", "goat", (1398, 12, 30, 1506)))],
       74: [("r74_e1", ("blender", (F(1, 4), 65))), ("r74_e2", ("toaster", (F(1, 2), 45))), ("r74_e3", ("heater", (F(1, 2), 15))),
            ("r74_e4", ("cooler", (F(2, 5), 48))), ("r74_e5", ("steamer", (F(1, 3), 55)))],
       75: [("r75_e1", ("goat", (6, 642, 615))), ("r75_e2", ("sheep", (14, 497, 427))), ("r75_e3", ("camel", (25, 1880, 1680))),
            ("r75_e4", ("cow", (9, 390, 363))), ("r75_e5", ("horse", (18, 2088, 1872)))],
       76: [("r76_ex", (15, 20)), ("r76_e1", (4, 5)), ("r76_e2", (12, 25)), ("r76_e3", (8, 10)), ("r76_e4", (30, 40)), ("r76_e5", (5, 16))]}


def build(rule, spec):
    if rule == 73:
        A_, B_, (S1, x, y, S2) = spec
        g = r73(A_, B_, S1, x, y, S2)
        return g, Q73.format(A=A_, B=B_, S1=m(S1), x=x, y=y, S2=m(S2)), opts_pair(g, A_.capitalize(), B_)
    if rule == 74:
        item, (k, x) = spec
        g = r74(k, x)
        return g, Q74.format(item=item, k=frac_txt(F(k)), x=x), popts(g["answer"][1])
    if rule == 75:
        item, (d, S2, S1) = spec
        g = r75(d, S2, S1)
        return g, Q75.format(item=item, d=d, S2=S2, S1=S1), ropts(g["answer"][1])
    x, y = spec
    g = r76(x, y)
    return g, Q76.format(x=x, y=y), popts(g["answer"][1])


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, spec)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        kind, v = g["answer"]
        answers.append([key, [kind, [str(t) for t in v] if kind == "pair" else str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (73, 74, 75, 76):
        main(r)
