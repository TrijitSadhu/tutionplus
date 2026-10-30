"""Profit and Loss Rules 22-24 (2026-10-30): "had he bought it y% cheaper and sold it for Rs X more (or less), he would have gained
z%" - after a profit (22), after a loss (23), and with Rs X less (24). Writes the three cards, regenerates the 7 old rows (314-317
and their copies 958-960; 315 was the book's "can't be determined" exercise and becomes a solvable one with the new numbers, 959
was a garbled copy with Rs 5) with a simple-style sentence, a new setting and all-new numbers, and adds the 15 book exercises that
had no copy. Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import Rs, m, result  # noqa: E402
from gen_18_21 import ropts  # noqa: E402

TH = {
    22: (r"If an article sold at a profit of \(x\%\) would have given \(z\%\) had it been bought \(y\%\) cheaper and sold for Rs \(X\) more, then<br>"
         r"\[ \text{CP}=\frac{X}{z-\left(x+y+\frac{zy}{100}\right)}\times 100 \]"),
    23: (r"If an article sold at a loss of \(x\%\) would have given a profit of \(z\%\) had it been bought \(y\%\) cheaper and sold for Rs \(X\) more, then<br>"
         r"\[ \text{CP}=\frac{X}{z+\left(x-y-\frac{zy}{100}\right)}\times 100 \]"),
    24: (r"If an article sold at a profit of \(x\%\) would still have given \(z\%\) had it been bought \(y\%\) cheaper and sold for Rs \(X\) less, then<br>"
         r"\[ \text{CP}=\frac{X}{x+\left(y-z+\frac{zy}{100}\right)}\times 100 \]"),
}


def cheaper(n, x, y, X, z):
    x, y, X, z = map(F, (x, y, X, z))
    real = 100 + x if n in (22, 24) else 100 - x            # real selling price on a cost of 100
    new_cost = 100 - y
    wished = new_cost * (100 + z) / 100                      # selling price that gives z% on the cheaper cost
    gap = wished - real if n in (22, 23) else real - wished  # on a cost of 100 this is the Rs X
    cp = X * 100 / gap
    word = "more" if n in (22, 23) else "less"
    trad = steps(
        ("Take the cost price as Rs 100.", rf"The real sale brings Rs \({tex(real)}\). Bought \({tex(y)}\%\) cheaper the cost is Rs \({tex(new_cost)}\), and a "
                                           rf"\({tex(z)}\%\) profit on it means selling for \({tex(new_cost)}\times\frac{{{tex(100 + z)}}}{{100}} = {tex(wished)}\)."),
        ("The difference is the Rs " + tex(X) + ".", rf"The second price is \({tex(abs(gap))}\) {word} on every Rs \(100\) of cost, and that is Rs \({m(X)}\), so"
                                                    rf"\[ \text{{CP}} = \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]"))
    if n == 22:
        den = rf"{tex(z)} - \left({tex(x)} + {tex(y)} + \frac{{{tex(z)}\times {tex(y)}}}{{100}}\right)"
    elif n == 23:
        den = rf"{tex(z)} + \left({tex(x)} - {tex(y)} - \frac{{{tex(z)}\times {tex(y)}}}{{100}}\right)"
    else:
        den = rf"{tex(x)} + \left({tex(y)} - {tex(z)} + \frac{{{tex(z)}\times {tex(y)}}}{{100}}\right)"
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", TH[n].split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(X)}}}{{{den}}}\times 100 = \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(X = {m(X)}\), \(z = {tex(z)}\).", rf"Denominator \(= {tex(gap)}\).", rf"\(\frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)}\)."]
    return result(("number", cp), TH[n], trad, rule, Rs(cp), rb, rf"\[ \frac{{{m(X)}}}{{{tex(gap)}}}\times 100 = {m(cp)} \]")


def card_(n, title, intuition, pattern, example, mistake):
    statement = {22: r"Compare the real sale (at \(x\%\) profit) with the wished sale: bought \(y\%\) cheaper and sold for Rs \(X\) more at \(z\%\) profit.",
                 23: r"Compare the real sale (at \(x\%\) loss) with the wished sale: bought \(y\%\) cheaper and sold for Rs \(X\) more at \(z\%\) profit.",
                 24: r"Compare the real sale (at \(x\%\) profit) with the wished sale: bought \(y\%\) cheaper and sold for Rs \(X\) less, still at \(z\%\) profit."}[n]
    visual = [("Real SP (CP = 100)", r"100+x" if n != 23 else r"100-x"), ("Cheaper cost", r"100-y"), ("Wished SP", r"(100-y)\frac{100+z}{100}"),
              ("Their difference is X", r"\text{CP}=\frac{X}{\text{difference}}\times 100")]
    return card(n, title, statement, TH[n].split("<br>")[1], visual, intuition, pattern, example, mistake)


CARDS = {
    22: card_(22, "Bought Cheaper, Sold for Rs X More (after a Profit)",
              r"Both selling prices are written on a cost of Rs 100; their gap on that cost is what the Rs \(X\) stands for.",
              "'A person sells an article at x% profit. If he had bought it at y% less and sold it for Rs X more, he would have gained z%.'",
              r"\(5\%\); \(10\%\) cheaper; Rs \(6\) more; \(20\%\): gap \(=90\times 1.2-105=3\), CP \(=\frac{6}{3}\times 100=\text{Rs }200\).",
              r"Taking the \(z\%\) profit on the old cost instead of on the cheaper one (the \(\frac{zy}{100}\) term)."),
    23: card_(23, "Bought Cheaper, Sold for Rs X More (after a Loss)",
              r"The real sale is below the cost; the wished sale is \(z\%\) above the cheaper cost - the Rs \(X\) covers the whole gap.",
              "'A person bought an article and sold it at a loss of x%. If he had bought it for y% less and sold it for Rs X more, he would have had a profit of z%.'",
              r"Loss \(5\%\); \(20\%\) cheaper; Rs \(45\) more; \(30\%\): gap \(=80\times 1.3-95=9\), CP \(=\frac{45}{9}\times 100=\text{Rs }500\).",
              r"Using \(100+x\) for the real sale (it was a loss)."),
    24: card_(24, "Bought Cheaper, Sold for Rs X Less",
              r"Here the wished sale is lower than the real one; the Rs \(X\) is the amount by which it falls short.",
              "'A man sells an article at x% profit. Had he bought it at y% less and sold it for Rs X less, he would have gained z%.'",
              r"\(16\%\); \(10\%\) cheaper; Rs \(42\) less; \(20\%\): gap \(=116-90\times 1.2=8\), CP \(=\frac{42}{8}\times 100=\text{Rs }525\).",
              r"Subtracting the two selling prices the wrong way round, which gives a negative cost."),
}

OLD = {
    22: {314: (lambda: cheaper(22, 5, 19, 147, 40), r"A man makes a profit of 5% on a fan. If the fan had cost 19% less and been sold for Rs 147 more, the profit would have been 40%. What did the fan cost?"),
         958: (lambda: cheaper(22, 8, 5, 21, 20), r"A shop sells a kettle at a gain of 8%. If it had paid 5% less for the kettle and sold it for Rs 21 more, it would have gained 20%. What did the kettle cost?"),
         315: (lambda: cheaper(22, 11, 10, 159, 40), r"A carpenter makes a profit of 11% on a stool. If the stool had cost 10% less and been sold for Rs 159 more, the profit would have been 40%. What did the stool cost?")},
    23: {316: (lambda: cheaper(23, 16, 4, 96, 50), r"A basket is sold at a loss of 16%. Bought for 4% less and sold for Rs 96 more, it would have brought a profit of 50%. Find what the basket cost."),
         959: (lambda: cheaper(23, 9, 22, 208, 50), r"A mirror is sold at a loss of 9%. Bought for 22% less and sold for Rs 208 more, it would have brought a profit of 50%. Find what the mirror cost.")},
    24: {317: (lambda: cheaper(24, 29, 10, 297, 10), r"A heater brings a profit of 29%. Had its cost been 10% lower and its price Rs 297 lower, the profit would have been 10%. Find the cost price of the heater."),
         960: (lambda: cheaper(24, 12, 5, 93, 10), r"A bag brings a profit of 12%. Had its cost been 5% lower and its price Rs 93 lower, the profit would have been 10%. Find the cost price of the bag.")},
}

NEW = {
    22: [("r22_e1", r"A bookseller makes a profit of 16% on a book. If the book had cost 16% less and been sold for Rs 112 more, the profit would have been 50%. What did the book cost?",
          lambda: cheaper(22, 16, 16, 112, 50)),
         ("r22_e2", r"A man makes a profit of 7% on a chair. If the chair had cost 9% less and been sold for Rs 135 more, the profit would have been 25%. What did the chair cost?",
          lambda: cheaper(22, 7, 9, 135, 25)),
         ("r22_e4", r"A dealer makes a profit of 15% on a table. If the table had cost 10% less and been sold for Rs 237 more, the profit would have been 50%. What did the table cost?",
          lambda: cheaper(22, 15, 10, 237, 50)),
         ("r22_e5", r"A girl makes a profit of 24% on a clock. If the clock had cost 12% less and been sold for Rs 273 more, the profit would have been 60%. What did the clock cost?",
          lambda: cheaper(22, 24, 12, 273, 60)),
         ("r22_e6", r"A shop sells a cupboard at 8% profit. If it had bought it 4% cheaper and sold it for Rs 48 more, it would have gained 15%. Find the cost price.",
          lambda: cheaper(22, 8, 4, 48, 15))],
    23: [("r23_e1", r"A cot is sold at a loss of 6%. Bought for 14% less and sold for Rs 230 more, it would have brought a profit of 20%. Find what the cot cost.",
          lambda: cheaper(23, 6, 14, 230, 20)),
         ("r23_e2", r"A trader sold a fan at a loss of 15%. If he had paid 25% less and sold it for Rs 80 more, he would have made a profit of 40%. What did the fan cost?",
          lambda: cheaper(23, 15, 25, 80, 40)),
         ("r23_e3", r"A girl sold a cycle at a loss of 20%. Had she bought it for 30% less and sold it for Rs 210 more, she would have gained 50%. Find its cost price.",
          lambda: cheaper(23, 20, 30, 210, 50)),
         ("r23_e4", r"A shop sold a lamp at a loss of 12%. If it had bought the lamp for 4% less and sold it for Rs 168 more, it would have gained 25%. What did the lamp cost?",
          lambda: cheaper(23, 12, 4, 168, 25)),
         ("r23_e5", r"A man sold a radio at a loss of 24%. Had he paid 20% less and sold it for Rs 84 more, his profit would have been 30%. Find the cost price.",
          lambda: cheaper(23, 24, 20, 84, 30))],
    24: [("r24_e1", r"A watch brings a profit of 36%. Had its cost been 6% lower and its price Rs 58 lower, the profit would have been 20%. Find the cost price of the watch.",
          lambda: cheaper(24, 36, 6, 58, 20)),
         ("r24_e2", r"A woman sells a vase at a gain of 14%. If she had bought it at 12% less and sold it for Rs 9 less, she would have gained 25%. Find the cost price.",
          lambda: cheaper(24, 14, 12, 9, 25)),
         ("r24_e3", r"A shop sells a mixer at a profit of 18%. Had it paid 10% less and sold it for Rs 66 less, its gain would have been 20%. What did the mixer cost?",
          lambda: cheaper(24, 18, 10, 66, 20)),
         ("r24_e4", r"A man sells a pair of shoes at a profit of 28%. If he had bought them at 15% less and sold them for Rs 52 less, he would have gained 20%. Find the cost price.",
          lambda: cheaper(24, 28, 15, 52, 20)),
         ("r24_e5", r"A sofa brings a profit of 23%. Had its cost been 10% lower and its price Rs 81 lower, the profit would have been 20%. Find the cost price of the sofa.",
          lambda: cheaper(24, 23, 10, 81, 20))],
}


def main():
    for n in (22, 23, 24):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question) in OLD[n].items():
            g = fn()
            op, _ = ropts(g["answer"][1])
            extra = {"question": question, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn in NEW[n]:
            g = fn()
            op, pos = ropts(g["answer"][1])
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
