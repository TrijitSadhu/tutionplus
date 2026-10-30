"""Profit and Loss Rules 8-12 (2026-10-30): the dishonest dealer - false weights at cost price (8), a profit plus a short weight (9),
a stated loss with a short weight in grams (10) or in per cent (11), a profit with a false kilogram (12). Writes the five cards,
regenerates the 8 old rows (copies of book examples / exercises; 298 and 299 had $$-garbage and almost no solution) with a
simple-style sentence, a new setting and all-new numbers, and adds the 23 book exercises that had no copy (numbers and wording
changed; checked with gate_check.py). Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, result  # noqa: E402

_k = [0]
POS = [2, 4, 1, 3, 3, 1, 4, 2, 1, 3, 2, 4]


def word(v):
    return "a profit" if v > 0 else ("a loss" if v < 0 else "no profit, no loss")


def sopts(v, signed=True):
    """Options for a per cent: signed ones say Profit / Loss (or No profit, no loss)."""
    v = F(v)
    s = abs(v)
    if not signed:
        vals = [P(s)] + [P(w) for w in (s + 1, s * 2, s + F(1, 2)) if w != s][:3]
    elif v == 0:
        vals = ["No profit, no loss", rf"Profit of \(5\%\)", rf"Loss of \(5\%\)", rf"Profit of \(10\%\)"]
    else:
        w, o = ("Profit", "Loss") if v > 0 else ("Loss", "Profit")
        vals = [rf"{w} of \({tex(s)}\%\)", rf"{o} of \({tex(s)}\%\)", rf"{w} of \({tex(s + 2)}\%\)", rf"{w} of \({tex(s * 2)}\%\)"]
    pos = POS[_k[0] % len(POS)]
    _k[0] += 1
    right, others = vals[0], vals[1:]
    others.insert(pos - 1, right)
    return others, pos


def fin_signed(v):
    return r"no profit, no loss (\(0\%\))" if v == 0 else rf"{word(v)} of \({tex(abs(v))}\%\)"


# ---------------------------------------------------------------- Rule 8
T8 = (r"A dealer who claims to sell at cost price but gives short measure gains, on what he really gives,<br>"
      r"\[ \%\text{ gain}=\frac{\text{True weight}-\text{False weight}}{\text{False weight}}\times 100 \]")


def r8(true, false, unit_big="kg", unit_small="g"):
    T, Fw = F(true), F(false)
    g = (T - Fw) / Fw * 100
    trad = steps(
        ("Price the goods per small unit.", rf"Let the goods cost Re \(1\) per {unit_small}. For one {unit_big} the buyer pays Rs \({tex(T)}\)."),
        ("What the dealer really gives.", rf"He gives only \({tex(Fw)}\) {unit_small}, which cost him Rs \({tex(Fw)}\)."),
        ("Gain on Rs 100 of cost.", rf"\[ \frac{{{tex(T)} - {tex(Fw)}}}{{{tex(Fw)}}}\times 100 = {tex(g)} \]"))
    rule = steps(
        ("Identify the values.", rf"True weight \(= {tex(T)}\) {unit_small}, false weight \(= {tex(Fw)}\) {unit_small}."),
        ("Apply the specified rule.", r"\[ \%\text{ gain}=\frac{\text{True weight}-\text{False weight}}{\text{False weight}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(T)} - {tex(Fw)}}}{{{tex(Fw)}}}\times 100 = {tex(g)}\% \]"))
    rb = [rf"True \(= {tex(T)}\), false \(= {tex(Fw)}\).", r"Gain \(\% = \frac{\text{True}-\text{False}}{\text{False}}\times 100\).", rf"\(\frac{{{tex(T - Fw)}}}{{{tex(Fw)}}}\times 100 = {tex(g)}\%\)."]
    return result(("number", g), T8, trad, rule, P(g), rb, rf"\[ \frac{{{tex(T - Fw)}}}{{{tex(Fw)}}}\times 100 = {tex(g)}\% \]")


# ---------------------------------------------------------------- Rule 9
T9 = r"If a dealer sells at a profit of \(p\%\) and also uses a weight that is \(w\%\) less, his total gain is<br>\[ \frac{p+w}{100-w}\times 100\% \]"


def r9(p, w):
    p, w = F(p), F(w)
    g = (p + w) / (100 - w) * 100
    trad = steps(
        ("Take the cost of 100 units as Rs 100.", rf"He charges Rs \({tex(100 + p)}\) for what he calls \(100\) units, but gives only \({tex(100 - w)}\) units, which cost him Rs \({tex(100 - w)}\)."),
        ("Gain on Rs 100 of cost.", rf"\[ \frac{{{tex(100 + p)} - {tex(100 - w)}}}{{{tex(100 - w)}}}\times 100 = {tex(g)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(p = {tex(p)}\), \(w = {tex(w)}\)."),
        ("Apply the specified rule.", r"\[ \frac{p+w}{100-w}\times 100\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(p)} + {tex(w)}}}{{100 - {tex(w)}}}\times 100 = {tex(g)}\% \]"))
    rb = [rf"\(p = {tex(p)}\), \(w = {tex(w)}\).", r"Gain \(= \frac{p+w}{100-w}\times 100\%\).", rf"\(\frac{{{tex(p + w)}}}{{{tex(100 - w)}}}\times 100 = {tex(g)}\%\)."]
    return result(("number", g), T9, trad, rule, P(g), rb, rf"\[ \frac{{{tex(p + w)}}}{{{tex(100 - w)}}}\times 100 = {tex(g)}\% \]")


# ---------------------------------------------------------------- Rule 10
T10 = (r"If a shopkeeper sells at \(x\%\) loss on cost price but gives \(y\) units in place of \(z\) units, his profit or loss per cent is<br>"
       r"\[ (100-x)\frac{z}{y}-100 \]a profit if positive, a loss if negative.")


def r10(x, y, z, unit="g"):
    x, y, z = F(x), F(y), F(z)
    v = (100 - x) * z / y - 100
    trad = steps(
        ("Take the cost of the true measure as Rs 100.", rf"\({tex(z)}\) {unit} cost Rs \(100\); with a \({tex(x)}\%\) loss he charges Rs \({tex(100 - x)}\) for them."),
        ("What the dealer really gives.", rf"He gives only \({tex(y)}\) {unit}, which cost him \(\frac{{{tex(y)}}}{{{tex(z)}}}\times 100 = {tex(100 * y / z)}\) rupees."),
        ("Compare.", rf"\[ \frac{{{tex(100 - x)} - {tex(100 * y / z)}}}{{{tex(100 * y / z)}}}\times 100 = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", r"\[ (100-x)\frac{z}{y}-100 \]"),
        ("Substitute the values.", rf"\[ {tex(100 - x)}\times\frac{{{tex(z)}}}{{{tex(y)}}} - 100 = {tex((100 - x) * z / y)} - 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\).", r"\((100-x)\frac{z}{y}-100\).", rf"\({tex((100 - x) * z / y)} - 100 = {tex(v)}\%\)."]
    return result(("signed", v), T10, trad, rule, fin_signed(v), rb, rf"\[ {tex(100 - x)}\times\frac{{{tex(z)}}}{{{tex(y)}}} - 100 = {tex(v)}\% \]")


# ---------------------------------------------------------------- Rule 11
T11 = r"If a dealer sells at \(x\%\) loss on cost price but uses a weight \(y\%\) less, his profit or loss per cent is<br>\[ \frac{y-x}{100-y}\times 100 \]"


def r11(x, y):
    x, y = F(x), F(y)
    v = (y - x) / (100 - y) * 100
    trad = steps(
        ("Take the cost of 100 units as Rs 100.", rf"He charges Rs \({tex(100 - x)}\) for what he calls \(100\) units, but gives \({tex(100 - y)}\) units costing Rs \({tex(100 - y)}\)."),
        ("Compare.", rf"\[ \frac{{{tex(100 - x)} - {tex(100 - y)}}}{{{tex(100 - y)}}}\times 100 = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{y-x}{100-y}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(y)} - {tex(x)}}}{{100 - {tex(y)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", r"\(\frac{y-x}{100-y}\times 100\).", rf"\(\frac{{{tex(y - x)}}}{{{tex(100 - y)}}}\times 100 = {tex(v)}\%\)."]
    return result(("signed", v), T11, trad, rule, fin_signed(v), rb, rf"\[ \frac{{{tex(y - x)}}}{{{tex(100 - y)}}}\times 100 = {tex(v)}\% \]")


# ---------------------------------------------------------------- Rule 12
T12 = (r"If a seller gives \(X\) g in place of one kilogram (1000 g) and sells at a profit of \(x\%\) on cost price, his actual gain or loss is<br>"
       r"\[ (100+x)\frac{1000}{X}-100 \]a gain if positive, a loss if negative.")


def r12(X, x):
    X, x = F(X), F(x)
    v = (100 + x) * 1000 / X - 100
    trad = steps(
        ("Take the cost of 1000 g as Rs 100.", rf"He charges Rs \({tex(100 + x)}\) for what he calls \(1\) kg."),
        ("What he really gives.", rf"He gives \({tex(X)}\) g, which cost him \(\frac{{{tex(X)}}}{{1000}}\times 100 = {tex(X / 10)}\) rupees."),
        ("Compare.", rf"\[ \frac{{{tex(100 + x)} - {tex(X / 10)}}}{{{tex(X / 10)}}}\times 100 = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(X = {tex(X)}\), \(x = {tex(x)}\)."),
        ("Apply the specified rule.", r"\[ (100+x)\frac{1000}{X}-100 \]"),
        ("Substitute the values.", rf"\[ {tex(100 + x)}\times\frac{{1000}}{{{tex(X)}}} - 100 = {tex((100 + x) * 1000 / X)} - 100 = {tex(v)}\% \]"))
    rb = [rf"\(X = {tex(X)}\), \(x = {tex(x)}\).", r"\((100+x)\frac{1000}{X}-100\).", rf"\({tex((100 + x) * 1000 / X)} - 100 = {tex(v)}\%\)."]
    return result(("signed", v), T12, trad, rule, fin_signed(v), rb, rf"\[ {tex(100 + x)}\times\frac{{1000}}{{{tex(X)}}} - 100 = {tex(v)}\% \]")


CARDS = {
    8: card(8, "Dishonest Dealer: Short Weight at Cost Price",
            r"A dealer who says he sells at cost price but gives less than the true measure still gains: he is paid for the true measure "
            r"and gives the false one.",
            r"\[ \%\text{ gain}=\frac{\text{True weight}-\text{False weight}}{\text{False weight}}\times 100=\frac{\text{Error}}{\text{True value}-\text{Error}}\times 100 \]",
            [("He is paid for", r"\text{True weight}"), ("He gives", r"\text{False weight}"), ("Gain on what he gives", r"\frac{\text{True}-\text{False}}{\text{False}}\times 100")],
            r"The gain is the goods he keeps back, measured against the goods he really hands over (his real cost), not against the true weight.",
            "'A dealer professes to sell at cost price but uses a weight of 875 g for a kilogram (or a metre of 96 cm).'",
            r"\(875\) g for \(1\) kg: \(\frac{1000-875}{875}\times 100=14\frac{2}{7}\%\).",
            r"Dividing by the true weight (\(\frac{125}{1000}=12.5\%\)) instead of by the false weight."),
    9: card(9, "Profit Plus a Short Weight",
            r"If a dealer sells at a profit of \(p\%\) and also gives \(w\%\) short weight, the two gains combine on what he really gives.",
            r"\[ \text{Total gain}=\frac{p+w}{100-w}\times 100\% \]",
            [("Charged for 100 units", r"100+p"), ("Units given", r"100-w"), ("Gain", r"\frac{(100+p)-(100-w)}{100-w}\times 100")],
            r"He is paid Rs \(100+p\) for goods that cost him only Rs \(100-w\).",
            "'A grocer sells rice at a profit of p% and uses a weight which is w% less; find his total percentage gain.'",
            r"Profit \(15\%\), weight \(10\%\) less: \(\frac{15+10}{90}\times 100=27\frac{7}{9}\%\).",
            r"Simply adding \(p\) and \(w\) - the short weight also shrinks the base."),
    10: card(10, "Stated Loss with a Short Weight",
             r"A dealer may say he sells at a loss of \(x\%\) and still gain, if he gives \(y\) units in place of \(z\).",
             r"\[ (100-x)\frac{z}{y}-100\quad(\text{profit if positive, loss if negative}) \]",
             [("Charged for z units", r"100-x"), ("Real cost of the y units given", r"100\times\frac{y}{z}"), ("Result", r"(100-x)\frac{z}{y}-100")],
             r"The selling price is fixed by the stated loss; the cost is only that of the smaller quantity really given.",
             "'A merchant professes to lose x% but uses a weight equal to y g instead of 1 kg (or y cm for a metre).'",
             r"Loss \(4\%\), \(12\) g for \(15\) g: \(96\times\frac{15}{12}-100=20\%\) profit.",
             r"Putting \(\frac{y}{z}\) in place of \(\frac{z}{y}\)."),
    11: card(11, "Stated Loss with a Weight y% Less",
             r"If a dealer sells at \(x\%\) loss on cost but uses a weight \(y\%\) less, the result depends on which per cent is larger.",
             r"\[ \frac{y-x}{100-y}\times 100\quad(\text{profit if positive, loss if negative}) \]",
             [("Charged for 100 units", r"100-x"), ("Units given", r"100-y"), ("Result", r"\frac{(100-x)-(100-y)}{100-y}\times 100")],
             r"When the weight is cut by more than the price, the dealer still gains.",
             "'A dishonest dealer sells at x% loss on cost price but uses y% less weight; what is his profit or loss per cent?'",
             r"Loss \(5\%\), weight \(20\%\) less: \(\frac{20-5}{80}\times 100=18\frac{3}{4}\%\) profit.",
             r"Dividing by \(100-x\) instead of by \(100-y\)."),
    12: card(12, "Profit with a False Kilogram",
             r"If a seller gives \(X\) g in place of \(1000\) g and also sells at \(x\%\) profit on cost, his actual result is",
             r"\[ (100+x)\frac{1000}{X}-100\quad(\text{gain if positive, loss if negative}) \]",
             [("Charged for 1 kg", r"100+x"), ("Real cost of X g", r"\frac{X}{10}"), ("Result", r"(100+x)\frac{1000}{X}-100")],
             r"A weight lighter than 1000 g adds to his gain; a weight heavier than 1000 g eats into it and can turn it into a loss.",
             "'A seller uses X gm in place of one kg and sells on x% gain on cost price; find his actual % profit or loss.'",
             r"\(800\) g, \(12\%\): \(112\times\frac{1000}{800}-100=40\%\) gain.",
             r"Forgetting that a weight above \(1000\) g (such as \(1125\) g) lowers the result."),
}

OLD = {
    8: {294: (lambda: r8(1000, 875), r"A shopkeeper claims to sell sugar at cost price, but he uses a weight of 875 g in place of 1 kg. What is his gain per cent?"),
        955: (lambda: r8(1000, 750), r"A spice seller says he sells at cost price, but his kilogram weight is really 750 g. Find his gain per cent.")},
    9: {295: (lambda: r9(15, 8), r"A shop sells dal at a profit of 15% and also uses a weight that is 8% less. Find its total gain per cent.")},
    10: {296: (lambda: r10(2, 28, 35), r"A trader says he sells saffron at a loss of 2% on cost, but he gives 28 g in place of 35 g. Find his real profit or loss per cent.")},
    11: {297: (lambda: r11(5, 20), r"A dealer sells oil at a loss of 5% on cost price but uses a weight 20% less than it should be. What is his profit or loss per cent?"),
         298: (lambda: r11(25, 10), r"A trader sells nuts at a loss of 25% on cost price and gives 10% less weight. Find his profit or loss per cent."),
         299: (lambda: r11(36, 20), r"A vendor sells grain at a loss of 36% on cost price but uses 20% less weight. What is his profit or loss per cent?")},
    12: {300: (lambda: r12(800, 12), r"A seller gives 800 g in place of 1 kg and sells his goods at a gain of 12% on cost price. Find his actual profit or loss per cent.")},
}
SIGNED = {10, 11, 12}

NEW = {
    8: [("r8_e2", r"A tailor says he sells cloth at cost price, but his metre rod is only 96 cm long. Find his gain per cent.", lambda: r8(100, 96, "metre", "cm")),
        ("r8_e3", r"A tea seller claims to sell at cost price but uses a weight of 850 g for the kilogram. What is his gain per cent?", lambda: r8(1000, 850)),
        ("r8_e4", r"A sweet shop sells at cost price but its kilogram weight weighs only 625 g. Find the shop's gain per cent.", lambda: r8(1000, 625)),
        ("r8_e5", r"A ribbon seller charges for a metre at cost price but gives only 90 cm. What is his gain per cent?", lambda: r8(100, 90, "metre", "cm"))],
    9: [("r9_e1", r"A grocer sells sugar at a profit of 12% and uses a weight which is 4% less. Find his total gain per cent.", lambda: r9(12, 4)),
        ("r9_e2", r"A shop sells flour at a profit of 15% and gives 25% less weight. What is its total gain per cent?", lambda: r9(15, 25)),
        ("r9_e3", r"A trader makes a profit of 30% on wheat and also uses a weight 10% short. Find his total gain per cent.", lambda: r9(30, 10)),
        ("r9_e4", r"A dealer sells pulses at a profit of 20% using a weight that is 40% less. What is his total gain per cent?", lambda: r9(20, 40)),
        ("r9_e5", r"A vendor sells rice at a profit of 25% and gives 10% less than he charges for. Find his total gain per cent.", lambda: r9(25, 10))],
    10: [("r10_e1", r"A shop claims to lose 5% on its coffee, but it uses a weight of 760 g in place of 1 kg. Find its real profit or loss per cent.",
          lambda: r10(5, 760, 1000)),
         ("r10_e2", r"A trader says he loses 12% on rice, but his kilogram weight is only 800 g. What is his real profit or loss per cent?",
          lambda: r10(12, 800, 1000)),
         ("r10_e3", r"A grocer claims a loss of 20% on dal but gives 640 g for every kilogram. Find his real gain or loss per cent.", lambda: r10(20, 640, 1000)),
         ("r10_e4", r"A cloth seller says he loses 12% on silk, but his metre is only 88 cm long. Find his gain or loss per cent.", lambda: r10(12, 88, 100, "cm")),
         ("r10_e5", r"A fruit seller says he loses 10% on grapes, but he gives 750 g for a kilogram. What is his real profit or loss per cent?",
          lambda: r10(10, 750, 1000)),
         ("r10_e6", r"A merchant claims to lose 2% on tea, but he uses a weight of 875 g for one kilogram. Find his real gain per cent.",
          lambda: r10(2, 875, 1000))],
    11: [("r11_e1", r"A dealer sells soap at a loss of 15% on cost price but uses 40% less weight. Find his profit or loss per cent.", lambda: r11(15, 40)),
         ("r11_e3", r"A shopkeeper sells oil at a loss of 30% on cost price but gives 40% less weight. What is his profit or loss per cent?", lambda: r11(30, 40)),
         ("r11_e5", r"A trader sells salt at a loss of 8% on cost price but uses a weight 20% less. Find his profit or loss per cent.", lambda: r11(8, 20))],
    12: [("r12_e1", r"A seller gives 960 g in place of 1 kg and sells at 8% gain on cost price. Find his actual profit or loss per cent.", lambda: r12(960, 8)),
         ("r12_e2", r"A shop uses 880 g for a kilogram and sells at a profit of 10% on cost. What is its actual gain or loss per cent?", lambda: r12(880, 10)),
         ("r12_e3", r"A trader gives 950 g as one kilogram and sells at 14% gain on cost price. Find his actual profit or loss per cent.", lambda: r12(950, 14)),
         ("r12_e4", r"A seller uses a weight of 1200 g for one kilogram and sells at a profit of 20% on cost. Find his actual profit or loss per cent.",
          lambda: r12(1200, 20)),
         ("r12_e5", r"A shop gives 1125 g in place of 1 kg and sells at 8% gain on cost price. What is its actual profit or loss per cent?",
          lambda: r12(1125, 8))],
}


def main():
    for n in (8, 9, 10, 11, 12):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question) in OLD[n].items():
            g = fn()
            op, _ = sopts(g["answer"][1], n in SIGNED)
            extra = {"question": question, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn in NEW[n]:
            g = fn()
            op, pos = sopts(g["answer"][1], n in SIGNED)
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], str(a[1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
