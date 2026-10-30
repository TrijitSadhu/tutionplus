"""Profit and Loss Rules 18-21 (2026-10-30): a profit then a loss (18), sold at x% profit - Rs X more would have given y% (19), sold
at x% loss - Rs X more would have given y% gain (20), two successive losses (21). Writes the four cards, regenerates the 6 old
rows (309-313 and 957, copies of the book; 312's key was on option e) with a simple-style sentence, a new setting and all-new
numbers, and adds the 18 book exercises that had no copy. Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, Rs, m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402


def sopts(v):
    v = F(v)
    s = abs(v)
    w, o = ("Profit", "Loss") if v > 0 else ("Loss", "Profit")
    return place(rf"{w} of \({tex(s)}\%\)", [rf"{o} of \({tex(s)}\%\)", rf"{w} of \({tex(s + 2)}\%\)", rf"{w} of \({tex(s + 5)}\%\)"])


def popts(v):
    v = F(v)
    return place(P(v), [P(w) for w in (v + 2, v - 2 if v > 2 else v + 5, v + 5)])


def ropts(v):
    v = F(v)
    return place(Rs(v), [Rs(w) for w in (v * F(11, 10), v * F(9, 10), v * F(6, 5))])


# ---------------------------------------------------------------- Rules 18 and 21
T18 = (r"When there is a profit of \(x\%\) and then a loss of \(y\%\), the resultant profit or loss is<br>"
       r"\[ \left(x-y-\frac{xy}{100}\right)\% \]a profit if positive, a loss if negative.")
T21 = r"When there are two successive losses of \(x\%\) and \(y\%\), the resultant loss is<br>\[ \left(x+y-\frac{xy}{100}\right)\% \]"


def two(n, x, y):
    x, y = F(x), F(y)
    a = 100 + x if n == 18 else 100 - x
    b = a * (100 - y) / 100
    v = (x - y - x * y / 100) if n == 18 else (x + y - x * y / 100)
    trad = steps(
        ("Take the first cost as Rs 100.", rf"After the first sale ({'profit' if n == 18 else 'loss'} of \({tex(x)}\%\)) the price is Rs \({tex(a)}\)."),
        ("The second sale is at a loss on that price.", rf"\[ {tex(a)} - \frac{{{tex(y)}}}{{100}}\times {tex(a)} = {tex(b)} \]"),
        ("Overall.", rf"From Rs \(100\) to Rs \({tex(b)}\) is " + (rf"a {'profit' if b > 100 else 'loss'} of \({tex(abs(b - 100))}\%\)." if n == 18 else rf"a loss of \({tex(100 - b)}\%\).")))
    formula = r"x-y-\frac{xy}{100}" if n == 18 else r"x+y-\frac{xy}{100}"
    sign = "-" if n == 18 else "+"
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", rf"\[ {formula} \]"),
        ("Substitute the values.", rf"\[ {tex(x)} {sign} {tex(y)} - \frac{{{tex(x)}\times {tex(y)}}}{{100}} = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\({formula}\).", rf"\({tex(x)} {sign} {tex(y)} - {tex(x * y / 100)} = {tex(v)}\%\)."]
    sc = rf"\[ {tex(x)} {sign} {tex(y)} - \frac{{{tex(x * y)}}}{{100}} = {tex(v)}\% \]"
    if n == 18:
        fin = rf"a {'profit' if v > 0 else 'loss'} of \({tex(abs(v))}\%\)"
        return result(("signed", v), T18, trad, rule, fin, rb, sc)
    return result(("number", v), T21, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rules 19 and 20
T19 = (r"If an article sold at a profit of \(x\%\) would have given \(y\%\) had it been sold for Rs \(X\) more, then<br>"
       r"\[ \text{CP}=\frac{X}{y-x}\times 100 \]")
T20 = (r"If an article sold at a loss of \(x\%\) would have given a gain of \(y\%\) had it been sold for Rs \(X\) more, then<br>"
       r"\[ \text{CP}=\frac{X}{x+y}\times 100 \]")


def more(n, x, X, y, ask="cp"):
    x, X, y = F(x), F(X), F(y)
    first = 100 + x if n == 19 else 100 - x
    gap = (100 + y) - first
    cp = X * 100 / gap
    sp = cp * first / 100
    trad = steps(
        ("Take the cost price as Rs 100.", rf"The real sale brings Rs \({tex(first)}\); the better sale would bring Rs \({tex(100 + y)}\)."),
        ("The difference matches the extra money.", rf"\({tex(100 + y)} - {tex(first)} = {tex(gap)}\) rupees on every Rs \(100\) of cost is the Rs \({m(X)}\), so"
                                                    rf"\[ \text{{CP}} = \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]"))
    formula = r"\frac{X}{y-x}\times 100" if n == 19 else r"\frac{X}{x+y}\times 100"
    rule_steps = [
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\)."),
        ("Apply the specified rule.", rf"\[ \text{{CP}}={formula} \]"),
        ("Substitute the values.", rf"\[ \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]")]
    if ask == "sp":
        rule_steps.append(("Find the selling price.", rf"It was sold at a loss of \({tex(x)}\%\): \[ {m(cp)}\times\frac{{{tex(first)}}}{{100}} = {m(sp)} \]"))
        trad = steps(
            ("Take the cost price as Rs 100.", rf"The real sale brings Rs \({tex(first)}\); the better sale would bring Rs \({tex(100 + y)}\)."),
            ("The difference matches the extra money.", rf"\({tex(gap)}\) rupees on every Rs \(100\) of cost is the Rs \({m(X)}\), so the cost is "
                                                        rf"\(\frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)}\)."),
            ("Find what it was sold for.", rf"\[ {m(cp)}\times\frac{{{tex(first)}}}{{100}} = {m(sp)} \]"))
    rule = steps(*rule_steps)
    v = sp if ask == "sp" else cp
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\).", rf"\(\text{{CP}} = {formula} = {m(cp)}\)."] + ([rf"SP \(= {m(sp)}\)."] if ask == "sp" else [])
    sc = rf"\[ \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]" + (rf"\[ {m(cp)}\times\frac{{{tex(first)}}}{{100}} = {m(sp)} \]" if ask == "sp" else "")
    return result(("number", v), T19 if n == 19 else T20, trad, rule, Rs(v), rb, sc)


CARDS = {
    18: card(18, "A Profit Followed by a Loss",
             r"If an article is sold at a profit of \(x\%\) and then sold again at a loss of \(y\%\), the overall result is",
             r"\[ \left(x-y-\frac{xy}{100}\right)\%\quad(\text{profit if positive, loss if negative}) \]",
             [("Start", r"100"), ("After x% profit", r"100+x"), ("After y% loss on that", r"(100+x)\frac{100-y}{100}")],
             r"The loss is taken on the already raised price, so it removes a little more than \(y\%\) of the first cost.",
             "'A sells to B at x% profit and B sells to C at y% loss; find the resultant profit or loss.'",
             r"\(25\%\) profit then \(12\%\) loss: \(25-12-3=10\%\) profit.",
             r"Writing \(x-y\) and forgetting the \(\frac{xy}{100}\) term."),
    19: card(19, "Rs X More Would Have Given y% Instead of x%",
             r"If an article sold at \(x\%\) profit would have brought \(y\%\) profit had it been sold for Rs \(X\) more, the extra money is "
             r"\((y-x)\%\) of the cost price.",
             r"\[ \text{CP}=\frac{X}{y-x}\times 100=\frac{\text{More gain}}{\text{Difference in per cent profit}}\times 100 \]",
             [("Actual SP", r"(100+x)\%\text{ of CP}"), ("Wished SP", r"(100+y)\%\text{ of CP}"), ("Difference", r"(y-x)\%\text{ of CP}=X")],
             r"Both selling prices are per cents of the same cost price, so their gap is a per cent of it too.",
             "'I sold it at x% profit; had I sold it for Rs X more, y% would have been gained. Find the cost price.'",
             r"\(8\%\) and \(15\%\), Rs \(35\) more: \(\frac{35}{7}\times 100=\text{Rs }500\).",
             r"Dividing by \(y\) alone, or by \(x+y\) (that is for a loss turned into a gain, Rule 20)."),
    20: card(20, "From a Loss of x% to a Gain of y% with Rs X More",
             r"If an article sold at a loss of \(x\%\) would have given a gain of \(y\%\) for Rs \(X\) more, the extra money covers the loss "
             r"and the gain together.",
             r"\[ \text{CP}=\frac{X}{x+y}\times 100 \]",
             [("Actual SP", r"(100-x)\%\text{ of CP}"), ("Wished SP", r"(100+y)\%\text{ of CP}"), ("Difference", r"(x+y)\%\text{ of CP}=X")],
             r"From \(x\%\) below the cost to \(y\%\) above it is a jump of \((x+y)\%\) of the cost.",
             "'A man sold it at a loss of x%. Had he sold it for Rs X more, he would have gained y%. What was the cost price?'",
             r"Loss \(6\%\), gain \(10\%\), Rs \(96\) more: \(\frac{96}{16}\times 100=\text{Rs }600\).",
             r"Using \(y-x\); or giving the cost price when the question asks for the selling price."),
    21: card(21, "Two Successive Losses",
             r"If an article is sold at a loss of \(x\%\) and the buyer sells it again at a loss of \(y\%\), the total loss is a little less than \(x+y\).",
             r"\[ \left(x+y-\frac{xy}{100}\right)\% \]",
             [("Start", r"100"), ("After x% loss", r"100-x"), ("After y% loss on that", r"(100-x)\frac{100-y}{100}")],
             r"The second loss is taken on the smaller price, so it removes less than \(y\%\) of the first cost.",
             "'A sells to B at a loss of x% and B sells to C at a loss of y%; find the resultant loss per cent.'",
             r"\(10\%\) and \(30\%\): \(10+30-3=37\%\) loss.",
             r"Writing \(x+y\) and forgetting the \(\frac{xy}{100}\) term."),
}

OLD = {
    18: {309: (lambda: two(18, 25, 12), r"A lamp is sold by A to B at a profit of 25%. B then sells it to C at a loss of 12%. Find the profit or loss per cent over both sales.")},
    19: {310: (lambda: more(19, 8, 49, 15), r"A shop sold a clock at a profit of 8%. Had it sold the clock for Rs 49 more, it would have made 15%. Find the cost of the clock.")},
    20: {311: (lambda: more(20, 6, 96, 10), r"A woman sold a sewing machine at a loss of 6%. If she had got Rs 96 more, she would have gained 10%. What did the machine cost her?"),
         957: (lambda: more(20, 4, 135, 11), r"A cow was sold at a loss of 4%. For Rs 135 more it would have been sold at a gain of 11%. Find the cost price of the cow."),
         312: (lambda: more(20, 12, 90, 6, "sp"), r"A bench was sold at a loss of 12%. Had it been sold for Rs 90 more, there would have been a gain of 6%. For how much was the bench sold?")},
    21: {313: (lambda: two(21, 10, 30), r"A sells a sofa to B at a loss of 10%, and B sells it to C at a loss of 30%. What is the total loss per cent?")},
}

NEW = {
    18: [("r18_e1", r"A trader sells a cycle to a shop at a profit of 16%; the shop sells it on at a loss of 5%. Find the overall profit or loss per cent.", lambda: two(18, 16, 5)),
         ("r18_e2", r"Raju sells a cooler to Hari at a profit of 8%. Hari sells it to Mona at a loss of 25%. How much per cent is gained or lost overall?", lambda: two(18, 8, 25)),
         ("r18_e3", r"A fridge changes hands twice: first at a profit of 30%, then at a loss of 25%. What is the overall profit or loss per cent?",
          lambda: two(18, 30, 25)),
         ("r18_e4", r"A watch is sold at a profit of 12%, and the buyer sells it again at a loss of 6%. What is the profit or loss per cent on the whole?",
          lambda: two(18, 12, 6)),
         ("r18_e5", r"A farmer sells a goat at a profit of 40% and the buyer sells it at a loss of 30%. Find the overall profit or loss per cent.",
          lambda: two(18, 40, 30))],
    19: [("r19_e1", r"A car dealer made a profit of 4% on a car. If the price had been Rs 900 higher, his profit would have been 22%. What did the car cost him?",
          lambda: more(19, 4, 900, 22)),
         ("r19_e2", r"I sold a bag at a profit of 10%. If I had sold it for Rs 42 more, I would have gained 17%. What did the bag cost?", lambda: more(19, 10, 42, 17)),
         ("r19_e3", r"A shopkeeper sold a mixer at 9% profit. For Rs 52 more his profit would have been 13%. Find the cost price.", lambda: more(19, 9, 52, 13)),
         ("r19_e4", r"A girl sold a doll house at a gain of 6%. Had she got Rs 63 more, she would have gained 13%. What did it cost her?", lambda: more(19, 6, 63, 13))],
    20: [("r20_e2", r"A man sells a cupboard at 8% below its cost price. Had he got Rs 1260 more, he would have made a profit of 10%. What did the cupboard cost?",
          lambda: more(20, 8, 1260, 10)),
         ("r20_e3", r"A buyer offers 12% less than the value of a carpet. A second buyer offers Rs 380 more, which is 7% above the value. Find the value of the carpet.",
          lambda: more(20, 12, 380, 7)),
         ("r20_e4", r"I sold a jacket at a loss of 9%. Had I sold it for Rs 140 more, I would have gained 5%. Find the cost price.", lambda: more(20, 9, 140, 5)),
         ("r20_e5", r"A trader sold a lamp at a loss of 3%. For Rs 88 more he would have gained 8%. What did the lamp cost him?", lambda: more(20, 3, 88, 8))],
    21: [("r21_e1", r"A sells a bat to B at a loss of 6%, and B sells it to C at a loss of 8%. Find the total loss per cent.", lambda: two(21, 6, 8)),
         ("r21_e2", r"A scooter is sold at a loss of 12% and then sold again at a loss of 20%. What is the total loss per cent?", lambda: two(21, 12, 20)),
         ("r21_e3", r"A tent is sold at a loss of 4%, and its buyer later sells it at a loss of 25%. What is the loss per cent over both sales?", lambda: two(21, 4, 25)),
         ("r21_e4", r"A shop sells a toy at a loss of 14%, and the buyer sells it at a loss of 30%. Find the overall loss per cent.", lambda: two(21, 14, 30)),
         ("r21_e5", r"A radio changes hands twice, each time at a loss: first 25%, then 40%. Find the total loss per cent.", lambda: two(21, 25, 40))],
}
OPTS = {18: sopts, 19: ropts, 20: ropts, 21: popts}


def main():
    for n in (18, 19, 20, 21):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question) in OLD[n].items():
            g = fn()
            op, _ = OPTS[n](g["answer"][1])
            extra = {"question": question, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn in NEW[n]:
            g = fn()
            op, pos = OPTS[n](g["answer"][1])
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
