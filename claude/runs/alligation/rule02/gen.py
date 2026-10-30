"""Rule 2 (m kg at x mixed with n kg at y, sold at z for p% gain: m = n[100z - y(100+p)] / [x(100+p) - 100z]).
Regenerates the book example row 836, rebuilds the Rule 2 card (the old one named x/y the wrong way round), and
writes the 9 book exercises that are missing as a JsonImport payload with new numbers."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import (S, card, frac, money, new_question, pct, ratio, ratio_steps, rbe, regen_entry, rtex,  # noqa: E402
                    shortcut, solution, steps, tex)

THEOREM = (r"If \(m\) kg of an item costing \(x\) per kg is mixed with \(n\) kg of it costing \(y\) per kg, and the mixture is sold "
           r"at \(z\) per kg to gain \(p\%\) on the outlay, then<br>"
           r"\[ \frac{m}{n} = \frac{100z - y(100+p)}{x(100+p) - 100z} \]")
RULE = r"\[ \frac{m}{n} = \frac{100z - y(100+p)}{x(100+p) - 100z} \]"


def price(v, cur):
    return rf"\({money(v)}\) paise" if cur == "paise" else rf"Rs \({money(v)}\)"


def cp_of(z, p):
    return F(z) * 100 / (100 + F(p))


def cp_step(z, p, cur, unit="kg"):
    z, p = F(z), F(p)
    if p == 0:
        return rf"There is neither gain nor loss, so the cost price of the mixture equals its selling price: {price(z, cur)} per {unit}."
    return (rf"Selling price {price(z, cur)} per {unit} with a gain of \({pct(p)}\%\):<br>"
            rf"\[ \text{{CP}} = {money(z)}\times\frac{{100}}{{100 + {pct(p)}}} = {money(cp_of(z, p))} \]")


def pos_eq(a_coef, a_var, b_coef, b_var):
    """'a*A = b*B' with both coefficients made positive."""
    if a_coef < 0:
        a_coef, b_coef = -a_coef, -b_coef
    return rf"{tex(a_coef)}{a_var} = {tex(b_coef)}{b_var}"


def num_den(x, y, z, p):
    x, y, z, p = map(F, (x, y, z, p))
    return 100 * z - y * (100 + p), x * (100 + p) - 100 * z


def subst(x, y, z, p):
    num, den = num_den(x, y, z, p)
    return (rf"\[ \frac{{100\times{money(z)} - {money(y)}\times(100 + {pct(p)})}}{{{money(x)}\times(100 + {pct(p)}) - 100\times{money(z)}}}"
            rf" = \frac{{{tex(100 * F(z))} - {tex(F(y) * (100 + F(p)))}}}{{{tex(F(x) * (100 + F(p)))} - {tex(100 * F(z))}}} = \frac{{{tex(num)}}}{{{tex(den)}}} \]")


def quantity(x, n, y, z, p, cur, item, unit_name="kg"):
    """How many kg at x must be mixed with n kg at y (sold at z, gain p%)."""
    x, n, y, z, p = map(F, (x, n, y, z, p))
    cp = cp_of(z, p)
    m = n * (cp - y) / (x - cp)
    num, den = num_den(x, y, z, p)
    assert m == n * num / den
    trad = steps(
        ("Find the cost price of the mixture.", cp_step(z, p, cur)),
        ("Let the unknown quantity be \\(m\\) kg.", rf"\(m\) kg of {item} at {price(x, cur)} and \({tex(n)}\) kg at {price(y, cur)} make \((m + {tex(n)})\) kg costing {price(cp, cur)} per kg:<br>"
         rf"\[ {money(x)}m + {money(y)}\times{tex(n)} = {money(cp)}(m + {tex(n)}) \]"),
        ("Collect the \\(m\\) terms.", rf"\[ {money(x)}m - {money(cp)}m = {money(cp)}\times{tex(n)} - {money(y)}\times{tex(n)} \]"
         rf"\[ {pos_eq(x - cp, 'm', (cp - y) * n, '')} \]"),
        ("Solve for \\(m\\).", rf"\[ m = {tex(m)} \]So \({tex(m)}\) kg of the {item} at {price(x, cur)} is needed.")
    )
    rule = steps(
        ("Identify the values.", rf"\(x = {money(x)}\), \(n = {tex(n)}\), \(y = {money(y)}\), \(z = {money(z)}\), \(p = {pct(p)}\)."),
        ("Apply the specified rule.", RULE),
        ("Substitute the values.", subst(x, y, z, p) + rf"\[ m = {tex(n)}\times\frac{{{tex(num)}}}{{{tex(den)}}} = {tex(m)}\text{{ kg}} \]")
    )
    fin = rf"\({tex(m)}\) kg"
    rb = rbe([rf"\(x = {money(x)}\), \(n = {tex(n)}\), \(y = {money(y)}\), \(z = {money(z)}\), \(p = {pct(p)}\).",
              rf"Numerator \(= {tex(num)}\), denominator \(= {tex(den)}\).",
              rf"\(m = {tex(n)}\times\frac{{{tex(num)}}}{{{tex(den)}}} = {tex(m)}\) kg."], fin)
    sc = shortcut(rf"\[ m = {tex(n)}\times\frac{{{tex(num)}}}{{{tex(den)}}} = {tex(m)} \]", fin)
    return dict(answer=("number", m), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def selling_price(m, x, n, y, p, item):
    """m kg at x and n kg at y; price per kg for p% gain."""
    m, x, n, y, p = map(F, (m, x, n, y, p))
    total = m * x + n * y
    cp = total / (m + n)
    z = cp * (100 + p) / 100
    trad = steps(
        ("Find the total cost.", rf"\[ {tex(m)}\times{money(x)} + {tex(n)}\times{money(y)} = {money(m * x)} + {money(n * y)} = {money(total)} \]"),
        ("Find the cost price per kg.", rf"\[ \text{{CP}} = \frac{{{money(total)}}}{{{tex(m)} + {tex(n)}}} = \frac{{{money(total)}}}{{{tex(m + n)}}} = {money(cp)} \]"),
        ("Add the profit.", rf"\[ \text{{SP}} = {money(cp)}\times\frac{{100 + {pct(p)}}}{{100}} = {money(z)} \]So the {item} must be sold at Rs \({money(z)}\) per kg.")
    )
    rule = steps(
        ("Identify the values.", rf"\(m = {tex(m)}\), \(x = {money(x)}\), \(n = {tex(n)}\), \(y = {money(y)}\), \(p = {pct(p)}\); \(z\) is unknown."),
        ("Apply the specified rule.", RULE + rf"\[ \frac{{{tex(m)}}}{{{tex(n)}}} = \frac{{100z - {money(y)}\times(100 + {pct(p)})}}{{{money(x)}\times(100 + {pct(p)}) - 100z}} \]"),
        ("Cross-multiply and solve for \\(z\\).",
         rf"\[ {tex(m)}\,({tex(x * (100 + p))} - 100z) = {tex(n)}\,(100z - {tex(y * (100 + p))}) \]"
         rf"\[ {tex(m * x * (100 + p))} + {tex(n * y * (100 + p))} = {tex(100 * (m + n))}z \]"
         rf"\[ z = \frac{{{tex((m * x + n * y) * (100 + p))}}}{{{tex(100 * (m + n))}}} = {money(z)} \]")
    )
    fin = rf"Rs \({money(z)}\) per kg"
    rb = rbe([rf"\(m = {tex(m)}\), \(x = {money(x)}\), \(n = {tex(n)}\), \(y = {money(y)}\), \(p = {pct(p)}\).",
              rf"From the rule: \(100z\,(m + n) = (100 + p)(mx + ny)\).",
              rf"\(z = \frac{{(100 + {pct(p)})\times{money(total)}}}{{100\times{tex(m + n)}}} = {money(z)}\)."], fin)
    sc = shortcut(rf"\[ z = \frac{{(100 + {pct(p)})({tex(m)}\times{money(x)} + {tex(n)}\times{money(y)})}}{{100\,({tex(m)} + {tex(n)})}} = {money(z)} \]", fin)
    return dict(answer=("number", z), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def unknown_price(m, x, n, z, p, item):
    """m kg at x and n kg at an unknown y, all sold at z for p% gain: find y."""
    m, x, n, z, p = map(F, (m, x, n, z, p))
    cp = cp_of(z, p)
    y = (cp * (m + n) - m * x) / n
    trad = steps(
        ("Find the cost price of the mixture.", cp_step(z, p, "Rs")),
        ("Set up the total cost.", rf"Let the second lot cost Rs \(y\) per kg:<br>\[ {tex(m)}\times{money(x)} + {tex(n)}y = {money(cp)}\times{tex(m + n)} \]"),
        ("Solve for \\(y\\).", rf"\[ {money(m * x)} + {tex(n)}y = {money(cp * (m + n))} \]\[ {tex(n)}y = {money(cp * (m + n) - m * x)} \;\Rightarrow\; y = {money(y)} \]")
    )
    rule = steps(
        ("Identify the values.", rf"\(m = {tex(m)}\) kg at \(x = {money(x)}\), \(n = {tex(n)}\) kg at \(y\) (unknown), \(z = {money(z)}\), \(p = {pct(p)}\)."),
        ("Apply the specified rule.", RULE + rf"\[ \frac{{{tex(m)}}}{{{tex(n)}}} = \frac{{100\times{money(z)} - y\times{tex(100 + p)}}}{{{money(x)}\times{tex(100 + p)} - 100\times{money(z)}}} = \frac{{{tex(100 * z)} - {tex(100 + p)}y}}{{{tex(x * (100 + p) - 100 * z)}}} \]"),
        ("Solve for \\(y\\).", rf"\[ {tex(m / n)}\times{tex(x * (100 + p) - 100 * z)} = {tex(100 * z)} - {tex(100 + p)}y \]"
         rf"\[ {tex(100 + p)}y = {tex(100 * z - m / n * (x * (100 + p) - 100 * z))} \;\Rightarrow\; y = {money(y)} \]")
    )
    fin = rf"Rs \({money(y)}\) per kg"
    rb = rbe([rf"\(m = {tex(m)}\), \(x = {money(x)}\), \(n = {tex(n)}\), \(z = {money(z)}\), \(p = {pct(p)}\).",
              rf"\(\frac{{{tex(m)}}}{{{tex(n)}}} = \frac{{{tex(100 * z)} - {tex(100 + p)}y}}{{{tex(x * (100 + p) - 100 * z)}}}\).",
              rf"\({tex(100 + p)}y = {tex(100 * z - m / n * (x * (100 + p) - 100 * z))}\), so \(y = {money(y)}\)."], fin)
    sc = shortcut(rf"\[ {tex(100 + p)}y = {tex(100 * z)} - {tex(m / n)}\times{tex(x * (100 + p) - 100 * z)} \Rightarrow y = {money(y)} \]", fin)
    return dict(answer=("number", y), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def mix_ratio(x, y, z, p, first, second):
    """Ratio first (price x) : second (price y) when sold at z for p% gain."""
    x, y, z, p = map(F, (x, y, z, p))
    cp = cp_of(z, p)
    r = ratio(cp - y, x - cp)
    num, den = num_den(x, y, z, p)
    assert ratio(num, den) == r
    trad = steps(
        ("Find the cost price of the mixture.", cp_step(z, p, "Rs")),
        ("Let the quantities be unknowns.", rf"Let \(a\) kg of the {first} (Rs \({money(x)}\)) be mixed with \(b\) kg of the {second} (Rs \({money(y)}\)):<br>"
         rf"\[ {money(x)}a + {money(y)}b = {money(cp)}(a + b) \]"),
        ("Collect the terms.", rf"\[ {money(x)}a - {money(cp)}a = {money(cp)}b - {money(y)}b \]\[ {pos_eq(x - cp, 'a', cp - y, 'b')} \]"),
        ("Find the ratio.", rf"\[ \frac{{a}}{{b}} = {ratio_steps(cp - y, x - cp)} \]So the {first} and the {second} are mixed in the ratio \({rtex(r)}\).")
    )
    rule = steps(
        ("Identify the values.", rf"\(x = {money(x)}\) ({first}), \(y = {money(y)}\) ({second}), \(z = {money(z)}\), \(p = {pct(p)}\)."),
        ("Apply the specified rule.", RULE),
        ("Substitute the values.", subst(x, y, z, p) + rf"\[ \frac{{m}}{{n}} = {ratio_steps(num, den)} \]")
    )
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"\(x = {money(x)}\), \(y = {money(y)}\), \(z = {money(z)}\), \(p = {pct(p)}\).",
              rf"Numerator \(= {tex(num)}\), denominator \(= {tex(den)}\).",
              rf"\(\frac{{m}}{{n}} = \frac{{{tex(num)}}}{{{tex(den)}}} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{m}}{{n}} = \frac{{{tex(num)}}}{{{tex(den)}}} = {rtex(r)} \]", fin)
    return dict(answer=("ratio", r), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


CARD = card(
    2, "Mixing to Sell at a Profit",
    r"Two lots of the same item are mixed: \(m\) kg costing \(x\) per kg and \(n\) kg costing \(y\) per kg. "
    r"The mixture is sold at \(z\) per kg and earns \(p\%\) on the money spent. The rule links all of these, so any one unknown "
    r"(the quantity \(m\), the ratio \(m : n\), the selling price \(z\) or one of the cost prices) can be found.",
    r"\[ \frac{m}{n} = \frac{100z - y(100+p)}{x(100+p) - 100z} \]",
    [("Cost price of the mixture", r"\text{CP} = \frac{100z}{100+p}"), ("Mixing ratio by alligation", r"\frac{m}{n} = \frac{\text{CP} - y}{x - \text{CP}}"),
     ("Multiply top and bottom by 100+p", r"\frac{100z - y(100+p)}{x(100+p) - 100z}"), ("Known lot", r"m = n\times\frac{m}{n}")],
    r"Alligation works on cost prices. Turning the selling price into the cost price, \(\frac{100z}{100+p}\), and then applying "
    r"\(\frac{m}{n} = \frac{\text{CP} - y}{x - \text{CP}}\) gives exactly this formula after clearing the fraction.",
    r"Two prices of the same item, a selling price for the mixture and a profit (or no gain, \(p = 0\)); the question asks for a quantity, a ratio, the selling price or a missing cost price.",
    r"How much salt at \(30\) P per kg must be mixed with \(20\) kg at \(45\) P per kg so that selling at \(50\) P per kg gives \(25\%\) profit?"
    r"\[ m = 20\times\frac{100\times50 - 45\times125}{30\times125 - 100\times50} = 20\times\frac{-625}{-1250} = 10\text{ kg} \]",
    r"Using the selling price \(z\) as the mean price in alligation. The mean price must be the cost price \(\frac{100z}{100+p}\); the formula already includes this step.",
)

FIX_836 = ("selling the mixture at 40 per kg, gain 25% on the outlay?", "selling the mixture at 40 P per kg, gain 25% on the outlay?")

NEW = [
    ("E1", "Ravi buys \\(20\\) kg of rice at Rs \\(18\\) per kg and \\(30\\) kg of rice at Rs \\(23\\) per kg. He mixes the two lots and sells the mixture. At what price per kg must he sell it to make a profit of \\(25\\%\\)?",
     ["Rs 25.50", "Rs 26.25", "Rs 27.00", "Rs 28.75"], 2, selling_price, (20, 18, 30, 23, 25, "rice"), "BSRB Mumbai PO 1998"),
    ("E2", "A trader buys \\(30\\) kg of wheat at Rs \\(12.50\\) per kg and \\(20\\) kg of wheat at Rs \\(15\\) per kg and mixes them. At what price per kg should the mixture be sold to earn a profit of \\(30\\%\\)?",
     ["Rs 16.80", "Rs 17.25", "Rs 17.55", "Rs 18.20"], 3, selling_price, (30, "12.50", 20, 15, 30, "wheat"), "BSRB Calcutta PO 1999"),
    ("E3", "Meena bought \\(40\\) kg of rice at Rs \\(18\\) per kg and another \\(40\\) kg of rice at a rate she does not remember. She mixed both lots and sold all of it at Rs \\(19.20\\) per kg, making an overall profit of \\(20\\%\\). What price per kg did she pay for the second lot?",
     ["Rs 12.50", "Rs 13.00", "Rs 15.50", "Rs 14.00"], 4, unknown_price, (40, 18, 40, "19.20", 20, "rice"), "BSRB Chennai PO 2000"),
    ("E4", "A shopkeeper buys \\(30\\) kg of rice at Rs \\(16\\) per kg and \\(30\\) kg of rice at Rs \\(14\\) per kg. At what price per kg should he sell the mixture to earn a profit of \\(33\\frac{1}{3}\\%\\) on his cost?",
     ["Rs 20.00", "Rs 18.50", "Rs 19.20", "Rs 21.00"], 1, selling_price, (30, 16, 30, 14, F(100, 3), "rice"), "BSRB Delhi PO 2000"),
    ("E5", "A grocer has two varieties of barley costing Rs \\(1.80\\) and Rs \\(1.20\\) per kg. In what ratio must he mix the two so that selling the mixture at Rs \\(1.92\\) per kg earns him a gain of \\(20\\%\\)?",
     ["1 : 2", "2 : 3", "3 : 2", "2 : 1"], 4, mix_ratio, ("1.80", "1.20", "1.92", 20, "Rs 1.80 barley", "Rs 1.20 barley"), ""),
    ("E6", "Wheat costing Rs \\(5.50\\) per kg is to be mixed with wheat costing Rs \\(4.50\\) per kg. In what ratio should they be mixed so that the mixture, sold at Rs \\(6.30\\) per kg, gives a profit of \\(20\\%\\)?",
     ["2 : 1", "3 : 1", "1 : 3", "3 : 2"], 2, mix_ratio, ("5.50", "4.50", "6.30", 20, "Rs 5.50 wheat", "Rs 4.50 wheat"), ""),
    ("E7", "How many kg of salt costing \\(30\\) P per kg must be mixed with \\(20\\) kg of salt costing \\(45\\) P per kg so that selling the mixture at \\(50\\) P per kg gives a profit of \\(25\\%\\)?",
     ["8 kg", "12 kg", "10 kg", "15 kg"], 3, quantity, (30, 20, 45, 50, 25, "paise", "salt"), ""),
    ("E8", "What weight of wheat costing Rs \\(5\\) per kg must be mixed with \\(45\\) kg of wheat costing Rs \\(3\\) per kg so that selling the mixture at Rs \\(3.80\\) per kg gives neither gain nor loss?",
     ["25 kg", "30 kg", "35 kg", "40 kg"], 2, quantity, (5, 45, 3, "3.80", 0, "Rs", "wheat"), ""),
    ("E9", "Kamal mixes \\(60\\) kg of sugar costing Rs \\(7.25\\) per kg with \\(140\\) kg of sugar costing Rs \\(8.50\\) per kg. At what rate per kg should he sell the mixture to gain \\(20\\%\\)?",
     ["Rs 9.25", "Rs 9.50", "Rs 9.75", "Rs 10.20"], 3, selling_price, (60, "7.25", 140, "8.50", 20, "sugar"), "SBI PO Exam 1987"),
]


def as_json_answer(ans):
    return [ans[0], [str(v) for v in ans[1]] if isinstance(ans[1], tuple) else str(ans[1])]


if __name__ == "__main__":
    cur = json.load(open(os.path.join(HERE, "0_current_rows.json"), encoding="utf-8"))
    card_id = cur["rule_card"]["id"]
    row = cur["rows"][0]
    assert row["id"] == 836 and FIX_836[0] in row["question"]
    out = [regen_entry(row, quantity(42, 25, 24, 40, 25, "paise", "salt"), card_id, {"question": row["question"].replace(*FIX_836)})]
    json.dump(out, open(os.path.join(HERE, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump({"rule_name": "Rule 2", "rule_html": CARD}, open(os.path.join(HERE, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    questions, answers = [], []
    for key, text, opts, pos, fn, args, exam in NEW:
        g = fn(*args)
        questions.append(new_question(2, text, opts, pos, g["solution"], g["rbe"], g["shortcut"], exam))
        answers.append([key, as_json_answer(g["answer"])])
    payload = {"rules_html": [{"chapter": "alligation_n_mixture", "rule_name": "Rule 2", "rule_html": CARD}], "questions": questions}
    json.dump(payload, open(os.path.join(HERE, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(HERE, "3_answers.json"), "w", encoding="utf-8"), indent=2)
    print("generated row 836 + Rule 2 card +", len(questions), "new questions")
