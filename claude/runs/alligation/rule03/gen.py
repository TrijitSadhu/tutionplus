"""Rule 3 (milk mixed with l litres of water is worth x per litre, pure milk y per litre: milk = l*x/(y-x)).
Regenerates the 5 existing rows in the prompt #10 layout and builds the missing Rule 3 card."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import S, card, money, ratio, rbe, regen_entry, rtex, shortcut, solution, steps, tex  # noqa: E402

THEOREM = (r"If a mixture of milk with \(l\) litres of water is worth \(x\) per litre and pure milk is worth \(y\) per litre, "
           r"then the quantity of milk in the mixture is<br>\[ \text{Milk} = l\times\frac{x}{y-x}\ \text{litres} \]")
RULE = r"\[ \text{Milk} = l\times\frac{x}{y-x} \]"


def price(v, cur):
    return rf"\({money(v)}\) paise" if cur == "paise" else rf"Rs \({money(v)}\)"


def milk(row, l, x, y, cur):
    l, x, y = F(l), F(x), F(y)
    M = l * x / (y - x)
    r = ratio(x, y - x)
    trad = steps(
        ("Let the unknown be the milk.", rf"Let the mixture contain \(M\) litres of milk and \({tex(l)}\) litres of water (water costs nothing)."),
        ("Write the value of the mixture in two ways.",
         rf"The \((M + {tex(l)})\) litres are worth {price(x, cur)} per litre, and they hold only the milk's value:<br>"
         rf"\[ (M + {tex(l)})\times{money(x)} = M\times{money(y)} + {tex(l)}\times 0 \]"),
        ("Expand and collect the \\(M\\) terms.",
         rf"\[ {money(x)}M + {tex(l * x)} = {money(y)}M \]\[ {money(y)}M - {money(x)}M = {tex(l * x)} \]\[ {tex(y - x)}M = {tex(l * x)} \]"),
        ("Solve for \\(M\\).", rf"\[ M = \frac{{{tex(l * x)}}}{{{tex(y - x)}}} = {tex(M)} \]So the mixture contains \({tex(M)}\) litres of milk.")
    )
    rule = steps(
        ("Identify the values.", rf"Water \(l = {tex(l)}\) litres, mixture price \(x = {money(x)}\), milk price \(y = {money(y)}\)."),
        ("Apply the specified rule.", RULE),
        ("Substitute the values.", rf"\[ \text{{Milk}} = {tex(l)}\times\frac{{{money(x)}}}{{{money(y)} - {money(x)}}} = {tex(l)}\times\frac{{{money(x)}}}{{{tex(y - x)}}} = {tex(M)}\text{{ litres}} \]"
         rf"(Equivalently, by alligation milk : water \(= ({money(x)} - 0) : ({money(y)} - {money(x)}) = {rtex(r)}\).)")
    )
    fin = rf"\({tex(M)}\) litres"
    rb = rbe([rf"\(l = {tex(l)}\), \(x = {money(x)}\), \(y = {money(y)}\).",
              rf"\(y - x = {tex(y - x)}\).",
              rf"Milk \(= {tex(l)}\times\frac{{{money(x)}}}{{{tex(y - x)}}} = {tex(M)}\) litres."], fin)
    sc = shortcut(rf"\[ {tex(l)}\times\frac{{{money(x)}}}{{{money(y)} - {money(x)}}} = {tex(M)} \]", fin)
    return dict(answer=("number", M), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


PLAN = {
    837: (16, 90, 108, "paise"),
    1079: (20, 80, 120, "paise"),
    1080: (24, 3, 15, "Rs"),
    1081: (25, 4, 14, "Rs"),
    1082: (36, "2.50", "7.50", "Rs"),
}

CARD = card(
    3, "Milk in a Milk–Water Mixture",
    r"Water costs nothing, so when milk is diluted the whole value of the mixture comes from the milk alone. "
    r"If a mixture containing \(l\) litres of water is worth \(x\) per litre while pure milk is worth \(y\) per litre, the amount of milk can be found directly.",
    r"\[ \text{Milk} = l\times\frac{x}{y-x}\ \text{litres} \]",
    [("Water in the mixture", r"l"), ("Price gap between milk and mixture", r"y - x"),
     ("Milk : water by alligation", r"x : (y - x)"), ("Milk", r"l\times\frac{x}{y-x}")],
    r"Value of the mixture \(= (\text{Milk} + l)\,x\) must equal the value of the milk \(= \text{Milk}\times y\). "
    r"Rearranging gives \(\text{Milk}\,(y-x) = l\,x\).",
    r"A diluted liquid (milk, juice, spirit) with a known amount of water, a price per litre for the mixture, a price per litre for the pure liquid, and the question asks for the pure liquid.",
    r"\(30\) litres of water are in a milk–water mixture worth Rs \(6\) per litre; pure milk costs Rs \(8\) per litre."
    r"\[ \text{Milk} = 30\times\frac{6}{8-6} = 30\times 3 = 90\text{ litres} \]",
    r"Using \(\frac{x}{y}\) or \(\frac{y-x}{x}\) instead of \(\frac{x}{y-x}\). Check: the milk must be worth more than the mixture, so \(y \gt x\), and the answer is the milk, not the total mixture.",
)

if __name__ == "__main__":
    cur = json.load(open(os.path.join(HERE, "0_current_rows.json"), encoding="utf-8"))
    out = [regen_entry(row, milk(row, *PLAN[row["id"]]), "NEW_RULE_3") for row in cur["rows"]]
    json.dump(out, open(os.path.join(HERE, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump({"rule_name": "Rule 3", "rule_html": CARD}, open(os.path.join(HERE, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("generated", len(out), "rows + Rule 3 card")
