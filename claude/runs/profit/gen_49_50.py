"""Profit and Loss Rules 49 and 50 (2026-10-30): articles bought at two rates "so many a rupee", mixed and sold at a third rate -
gain or loss per cent. Rule 49: m articles at x a rupee and n at y a rupee; Rule 50: the same number at each rate. Writes both cards,
regenerates old rows 344 (Rule 49's example) and 345-347 (Rule 50's three worked examples) with simple-style sentences, new settings
and all-new numbers, and adds the book exercises (5 for Rule 49, 9 for Rule 50). Answers are signed (a profit / a loss).
Usage: python gen_49_50.py"""
import json, os, sys
from fractions import Fraction as F
from math import lcm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import result  # noqa: E402
from gen_18_21 import sopts  # noqa: E402

T49 = (r"If \(m\) articles are bought at \(x\) a rupee and \(n\) at \(y\) a rupee, and all are sold at \(z\) a rupee, the gain or loss is"
       r"<br>\[ \left(\frac{(m+n)xy}{(my+nx)z}-1\right)\times 100\% \]a gain if positive, a loss if negative.")
T50 = (r"If the same number of articles is bought at \(x\) a rupee and at \(y\) a rupee, and all are sold at \(z\) a rupee, the gain or "
       r"loss is<br>\[ \left(\frac{2xy}{z(x+y)}-1\right)\times 100\% \]a gain if positive, a loss if negative.")


def word(v):
    return "profit" if v > 0 else "loss"


def fin(v):
    return rf"a {word(v)} of \({tex(abs(v))}\%\)"


def r49(mm, x, nn, y, z):
    mm, x, nn, y, z = map(F, (mm, x, nn, y, z))
    cost, sale = mm / x + nn / y, (mm + nn) / z
    v = (sale - cost) / cost * 100
    ratio = (mm + nn) * x * y / ((mm * y + nn * x) * z)
    trad = steps(
        ("Cost of the two lots.", rf"\[ \frac{{{tex(mm)}}}{{{tex(x)}}} + \frac{{{tex(nn)}}}{{{tex(y)}}} = {tex(mm / x)} + {tex(nn / y)} = \text{{Rs }}{tex(cost)} \]"),
        ("Money from selling all of them.", rf"\[ \frac{{{tex(mm + nn)}}}{{{tex(z)}}} = \text{{Rs }}{tex(sale)} \]"),
        ("Gain or loss per cent.", rf"\[ \frac{{{tex(sale)} - {tex(cost)}}}{{{tex(cost)}}}\times 100 = {tex(v)}\% \]"
                                   + f"<br>It is {'positive, so a profit' if v > 0 else 'negative, so a loss'}."))
    rule = steps(
        ("Identify the values.", rf"\(m = {tex(mm)}\), \(x = {tex(x)}\), \(n = {tex(nn)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", T49.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \left(\frac{{{tex(mm + nn)}\times {tex(x)}\times {tex(y)}}}{{({tex(mm)}\times {tex(y)} + {tex(nn)}\times {tex(x)})\times {tex(z)}}} - 1\right)\times 100 "
                                   rf"= \left({tex(ratio)} - 1\right)\times 100 = {tex(v)}\% \]"))
    rb = [rf"\((m+n)xy = {tex((mm + nn) * x * y)}\), \((my+nx)z = {tex((mm * y + nn * x) * z)}\).", rf"Ratio \(= {tex(ratio)}\).",
          rf"\(({tex(ratio)} - 1)\times 100 = {tex(v)}\%\): {fin(v)}."]
    return result(("signed", v), T49, trad, rule, fin(v), rb, rf"\[ \left({tex(ratio)} - 1\right)\times 100 = {tex(v)}\% \]")


def r50(x, y, z):
    x, y, z = map(F, (x, y, z))
    N = F(lcm(int(x), int(y)))
    cost, sale = N / x + N / y, 2 * N / z
    v = (sale - cost) / cost * 100
    ratio = 2 * x * y / (z * (x + y))
    trad = steps(
        ("Take " + tex(N) + " articles of each kind.", rf"Cost \(= \frac{{{tex(N)}}}{{{tex(x)}}} + \frac{{{tex(N)}}}{{{tex(y)}}} = {tex(N / x)} + {tex(N / y)} = \text{{Rs }}{tex(cost)}\)."),
        ("Money from selling all " + tex(2 * N) + ".", rf"\[ \frac{{{tex(2 * N)}}}{{{tex(z)}}} = \text{{Rs }}{tex(sale)} \]"),
        ("Gain or loss per cent.", rf"\[ \frac{{{tex(sale)} - {tex(cost)}}}{{{tex(cost)}}}\times 100 = {tex(v)}\% \]"
                                   + f"<br>It is {'positive, so a profit' if v > 0 else 'negative, so a loss'}."))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", T50.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \left(\frac{{2\times {tex(x)}\times {tex(y)}}}{{{tex(z)}\times ({tex(x)} + {tex(y)})}} - 1\right)\times 100 "
                                   rf"= \left({tex(ratio)} - 1\right)\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(2xy = {tex(2 * x * y)}\), \(z(x+y) = {tex(z * (x + y))}\).", rf"Ratio \(= {tex(ratio)}\).", rf"\(({tex(ratio)} - 1)\times 100 = {tex(v)}\%\): {fin(v)}."]
    return result(("signed", v), T50, trad, rule, fin(v), rb, rf"\[ \left({tex(ratio)} - 1\right)\times 100 = {tex(v)}\% \]")


CARDS = {
    49: card(49, "Two Lots Bought at 'So Many a Rupee', Sold Mixed",
             r"Buying \(m\) articles at \(x\) a rupee costs \(\frac{m}{x}\) rupees; selling all \(m+n\) at \(z\) a rupee brings \(\frac{m+n}{z}\) rupees.",
             r"\[ \left(\frac{(m+n)xy}{(my+nx)z}-1\right)\times 100\% \]",
             [("Cost", r"\frac{m}{x}+\frac{n}{y}=\frac{my+nx}{xy}"), ("Sale", r"\frac{m+n}{z}"), ("Sale ÷ cost", r"\frac{(m+n)xy}{(my+nx)z}")],
             r"A positive answer is a gain and a negative one a loss; more articles a rupee means a lower price.",
             "'A man buys m oranges at x a rupee and n at y a rupee, mixes them and sells them at z a rupee. Find his gain or loss per cent.'",
             r"\(60\) at \(6\), \(40\) at \(4\), sold at \(5\): cost Rs \(20\), sale Rs \(20\) - no gain, no loss.",
             r"Averaging the rates \(x\) and \(y\) - the rates are 'per rupee', so the money has to be added."),
    50: card(50, "Equal Numbers Bought at Two Rates, Sold Mixed",
             r"With the same number bought at \(x\) a rupee and at \(y\) a rupee, the cost of two articles is \(\frac{1}{x}+\frac{1}{y}\) rupees, "
             r"and they sell for \(\frac{2}{z}\) rupees.",
             r"\[ \left(\frac{2xy}{z(x+y)}-1\right)\times 100\% \]",
             [("Cost of one pair", r"\frac{1}{x}+\frac{1}{y}=\frac{x+y}{xy}"), ("Sale of one pair", r"\frac{2}{z}"), ("Sale ÷ cost", r"\frac{2xy}{z(x+y)}")],
             r"Selling at the plain average \(z=\frac{x+y}{2}\) always gives a loss (unless \(x=y\)).",
             "'A man buys some mangoes at x a rupee and the same number at y a rupee, mixes them and sells them at z a rupee. Find his gain or loss per cent.'",
             r"\(4\) and \(6\) a rupee, sold at \(5\): \(\frac{48}{50}-1=-\frac{1}{25}\), a loss of \(4\%\).",
             r"Thinking that selling at the average rate gives no loss."),
}
# Rule 49: (m, x, n, y, z); Rule 50: (x, y, z, sale text)
T49Q = ("A vendor buys {m} {item} at {x} a rupee and {n} more at {y} a rupee. She mixes them and sells them all at {z} a rupee. "
        "Find her gain or loss per cent.")
T50Q = ("A shop buys some {item} at {x} a rupee and the same number at {y} a rupee. It mixes them and sells them at {sale}. "
        "Find its gain or loss per cent.")
OLD = {49: {344: ("lemons", (360, 6, 240, 8, 5))},
       50: {345: ("plums", (5, 7, "5 a rupee")), 346: ("sweets", (15, 10, "50 for 4 rupees")), 347: ("eggs", (16, 8, "12 a rupee"))}}
NEW = {49: [("r49_e1", "guavas", (120, 6, 280, 7, 8)), ("r49_e2", "limes", (90, 9, 210, 6, 6)), ("r49_e3", "pencils", (160, 8, 140, 7, 6)),
            ("r49_e4", "chocolates", (210, 15, 90, 9, 12)), ("r49_e5", "erasers", (260, 13, 140, 7, 11))],
       50: [("r50_e1", "buttons", (21, 28, "22 a rupee")), ("r50_e2", "candles", (6, 9, "6 a rupee")), ("r50_e3", "marbles", (24, 40, "64 for 2 rupees")),
            ("r50_e4", "balloons", (12, 18, "16 a rupee")), ("r50_e5", "stickers", (7, 21, "8 a rupee")), ("r50_e6", "beads", (11, 33, "45 for 2 rupees")),
            ("r50_e7", "pins", (9, 18, "11 a rupee")), ("r50_e8", "clips", (16, 24, "15 a rupee")), ("r50_e9", "badges", (14, 35, "28 a rupee"))]}


def z_of(sale):
    a, rest = sale.split(" ", 1)
    return F(int(a), int(rest.split()[1])) if rest.startswith("for") else F(int(a))


def build(rule, item, c):
    if rule == 49:
        mm, x, nn, y, z = c
        return r49(*c), T49Q.format(m=mm, item=item, x=x, n=nn, y=y, z=z)
    x, y, sale = c
    return r50(x, y, z_of(sale)), T50Q.format(item=item, x=x, y=y, sale=sale)


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, (item, c) in OLD[rule].items():
        g, q = build(rule, item, c)
        op, _ = sopts(g["answer"][1])
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW[rule]:
        g, q = build(rule, item, c)
        op, pos = sopts(g["answer"][1])
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (49, 50):
        main(r)
