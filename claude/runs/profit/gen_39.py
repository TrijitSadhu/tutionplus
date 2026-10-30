"""Profit and Loss Rule 39 (2026-10-30): parts x, y, z of a stock sold at m%, n%, p% profit (or loss) give a total of Rs P - find the
value of the stock. Writes the card, regenerates old rows 333 (the book's example) and 338 (the same example with losses) with a
simple-style sentence, a new setting and all-new numbers, and adds the 5 book exercises. Same layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_13_17 import _k  # noqa: E402

T39 = (r"If parts \(x\), \(y\) and \(z\) of a stock (\(x+y+z=1\)) are sold at \(m\%\), \(n\%\) and \(p\%\) profit and the total profit is "
       r"Rs \(P\), then<br>\[ \text{Value of the stock}=\frac{P\times 100}{mx+ny+pz} \]")


def fr(v):
    return rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def r39(x, y, rates, P, word="profit", theorem=T39):
    x, y, P = F(x), F(y), F(P)
    z = 1 - x - y
    a, b, c = map(F, rates)
    w = a * x + b * y + c * z
    v = P * 100 / w
    parts = [(x, a), (y, b), (z, c)]
    each = r" + ".join(rf"\frac{{{tex(r)}}}{{100}}\times {fr(f)}V" for f, r in parts)
    trad = steps(
        ("Let the value of the stock be Rs \\(V\\).", rf"The rest is \(1 - {fr(x)} - {fr(y)} = {fr(z)}\) of it."),
        (f"Add the {word} on the three parts.", rf"\[ {each} = {m(P)} \]"),
        ("Solve.", rf"\[ \frac{{{tex(w)}}}{{100}}V = {m(P)} \;\Rightarrow\; V = {m(v)} \]"))
    terms = r" + ".join(rf"{tex(r)}\times {fr(f)}" for f, r in parts)
    vals = r" + ".join(tex(r * f) for f, r in parts)
    rule = steps(
        ("Identify the values.", rf"\(x = {fr(x)}\), \(y = {fr(y)}\), \(z = {fr(z)}\); rates \({tex(a)}\%\), \({tex(b)}\%\), \({tex(c)}\%\); "
                                 rf"total {word} \(P = {m(P)}\)."),
        ("Apply the specified rule.", theorem.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(P)}\times 100}}{{{terms}}} = \frac{{{m(P * 100)}}}{{{vals}}} = {m(v)} \]"))
    rb = [rf"Rest \(z = {fr(z)}\).", rf"\(mx + ny + pz = {vals} = {tex(w)}\).", rf"Value \(= \frac{{{m(P)}\times 100}}{{{tex(w)}}} = {m(v)}\)."]
    return result(("number", v), theorem, trad, rule, rf"Rs \({m(v)}\)", rb, rf"\[ \frac{{{m(P)}\times 100}}{{{tex(w)}}} = {m(v)} \]")


CARD = card(39, "Three Parts of a Stock at Three Rates: Find the Value",
            r"When parts \(x\), \(y\) and \(z\) of a stock earn \(m\%\), \(n\%\) and \(p\%\), the whole stock earns the weighted rate "
            r"\(mx+ny+pz\) per cent, and the total profit Rs \(P\) is that rate of the value.",
            T39.split("<br>")[1],
            [("Rest", r"z=1-x-y"), ("Overall rate", r"mx+ny+pz\ \text{per cent}"), ("Value", r"\frac{P\times 100}{mx+ny+pz}")],
            r"The same formula works when every part is sold at a loss and \(P\) is the total loss.",
            "'x of a commodity is sold at m% profit, y at n% profit and the rest at p% profit; the total profit is Rs P. Find the value of the commodity.'",
            r"\(\frac{1}{2}\) at \(10\%\), \(\frac{1}{4}\) at \(20\%\), rest at \(40\%\), profit Rs \(90\): \(5+5+10=20\), value \(=\frac{9000}{20}=\text{Rs }450\).",
            r"Forgetting to work out the rest \(z=1-x-y\) before using it.")

F_ = r"\(\frac{{{0}}}{{{1}}}\)"


def frac_txt(f):
    return F_.format(f.numerator, f.denominator)


TPL = ("A trader sells {x} of his {item} at a {w} of {a}%, {y} of it at a {w} of {b}% and the rest at a {w} of {c}%. "
       "If his total {w} is Rs {P}, find the value of the {item}.")
QS = {333: ("stock of rice", (F(1, 5), F(1, 2), (10, 16, 30), 171), "profit")}
NEW = [("r39_e1", "stock of sugar", (F(1, 4), F(1, 2), (8, 14, 32), 85)),
       ("r39_e2", "stock of tea", (F(2, 5), F(1, 3), (10, 18, 45), 154)),
       ("r39_e3", "stock of wheat", (F(1, 6), F(1, 3), (30, 27, 16), 330)),
       ("r39_e4", "stock of pulses", (F(3, 8), F(1, 4), (16, 28, 40), 196)),
       ("r39_e5", "stock of paint", (F(2, 7), F(3, 7), (12, 12, 12), 54))]


def q_of(item, c, w="profit"):
    x, y, (a, b, cc), P = c
    return TPL.format(x=frac_txt(x), y=frac_txt(y), item=item, w=w, a=a, b=b, c=cc, P=P)


def main():
    folder = os.path.join(HERE, "rule39")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert set(QS) <= set(rows)  # row 338 (the loss version) moved to its own rule on 2026-10-30
    out = []
    for rid, (item, c, w) in QS.items():
        g = r39(*c, word=w)
        op, _ = ropts(g["answer"][1])
        extra = {"question": q_of(item, c, w), **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, "NEW_RULE_39", extra))
    _k[0] += 1  # row 338 used one answer position here before it moved; keeps the applied payload reproducible
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": "Rule 39", "rule_html": CARD}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW:
        g = r39(*c)
        op, pos = ropts(g["answer"][1])
        qs.append(new_question(39, q_of(item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 39: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
