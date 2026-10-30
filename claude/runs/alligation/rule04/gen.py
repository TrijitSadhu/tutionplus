"""Rule 4 (water mixed with spirit and sold at the spirit's cost price to gain x%: water : spirit = x : 100).
Regenerates the 6 existing rows in the prompt #10 layout, fixes 838's display-math percentage, builds the Rule 4 card."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import S, card, frac, pct, ratio, rbe, regen_entry, rtex, shortcut, solution, steps, tex  # noqa: E402

THEOREM = (r"If water is mixed with spirit and the mixture is sold at the cost price of the spirit to gain \(x\%\), "
           r"then water and spirit are mixed in the ratio<br>\[ \text{Water} : \text{Spirit} = x : 100 \]")
RULE = r"\[ \text{Water} : \text{Spirit} = x : 100 \]"


def spirit(row, g):
    g = F(g)
    r = ratio(g, 100)
    cpm = F(100) / (100 + g)
    trad = steps(
        ("Choose a convenient cost price.", r"Let pure spirit cost Rs \(1\) per litre. Water costs Rs \(0\)."
         r"<br>The mixture is sold at the spirit's cost price, so its selling price is Rs \(1\) per litre."),
        ("Find the cost price of the mixture.", rf"A gain of \({pct(g)}\%\) means<br>"
         rf"\[ \text{{CP}} = 1\times\frac{{100}}{{100 + {pct(g)}}} = {frac(cpm)} \]Each litre of mixture costs Rs \({frac(cpm)}\)."),
        ("Set up the cost equation.", rf"Let \(a\) litres of water be mixed with \(b\) litres of spirit:<br>"
         rf"\[ a\times 0 + b\times 1 = (a + b)\times{frac(cpm)} \]"),
        ("Solve for the ratio.", rf"\[ {(100 + g).numerator if (100 + g).denominator == 1 else frac(100 + g)}\,b = 100\,(a + b) \;\Rightarrow\; {pct(g)}\,b = 100\,a \]"
         rf"\[ \frac{{a}}{{b}} = \frac{{{pct(g)}}}{{100}} = \frac{{{r[0]}}}{{{r[1]}}} \]So water : spirit \(= {rtex(r)}\).")
    )
    rule = steps(
        ("Identify the gain.", rf"\(x = {pct(g)}\%\)."),
        ("Apply the specified rule.", RULE),
        ("Substitute and simplify.", rf"\[ \text{{Water}} : \text{{Spirit}} = {pct(g)} : 100 = {rtex(r)} \]")
    )
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"Gain \(x = {pct(g)}\%\).", r"Water : spirit \(= x : 100\).", rf"\({pct(g)} : 100 = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ {pct(g)} : 100 = {rtex(r)} \]", fin)
    return dict(answer=("ratio", r), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


PLAN = {838: F(50, 3), 1095: F(25, 2), 1096: F(75, 2), 1097: 20, 1098: 12, 1099: 40}
FIX_QUESTION = {838: ("In what proportion must water be mixed with spirit to gain \\[ \\frac{50}{3} \\] %  by selling it at cost price?",
                      "In what proportion must water be mixed with spirit to gain \\(16\\frac{2}{3}\\%\\) by selling it at cost price?")}

CARD = card(
    4, "Gain by Mixing Water with Spirit",
    r"If spirit (or milk, oil, any liquid) is diluted with free water and the whole mixture is sold at the cost price of the pure liquid, "
    r"the water added is pure profit. To make a gain of \(x\%\) the water must be \(x\) parts for every \(100\) parts of the liquid.",
    r"\[ \text{Water} : \text{Spirit} = x : 100 \]",
    [("Gain wanted", r"x\%"), ("Water parts", r"x"), ("Spirit parts", r"100"), ("Simplify", r"x : 100")],
    r"Selling at the spirit's cost price means each litre of water is sold for the price of spirit while costing nothing. "
    r"The profit is the value of the water, so profit \(\div\) cost \(=\) water \(\div\) spirit \(= \frac{x}{100}\).",
    r"Water mixed with a liquid, the mixture sold at the liquid's cost price, and a gain percent is given or asked.",
    r"To gain \(25\%\): \[ \text{Water} : \text{Spirit} = 25 : 100 = 1 : 4 \]",
    r"Writing the ratio as \(100 : x\) or as water : mixture. The gain is on the spirit's cost, so the comparison is water : spirit.",
)

if __name__ == "__main__":
    cur = json.load(open(os.path.join(HERE, "0_current_rows.json"), encoding="utf-8"))
    out = []
    for row in cur["rows"]:
        extra = {}
        if row["id"] in FIX_QUESTION:
            old_q, new_q = FIX_QUESTION[row["id"]]
            assert row["question"] == old_q
            extra["question"] = new_q
        out.append(regen_entry(row, spirit(row, PLAN[row["id"]]), "NEW_RULE_4", extra))
    json.dump(out, open(os.path.join(HERE, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump({"rule_name": "Rule 4", "rule_html": CARD}, open(os.path.join(HERE, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("generated", len(out), "rows + Rule 4 card")
