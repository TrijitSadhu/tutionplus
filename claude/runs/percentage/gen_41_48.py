"""Rules 41-48: writes the eight rule cards, regenerates the old worked-example rows 629-636 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their options
(631 had a NULL option and none holding the 6.25% fall, 634 none holding the 37.5% rise; the effect-on-a-product rules
42-47 now say Increase / Decrease), and adds the book exercises (numbers changed, wording rewritten) plus the worked
examples of Rules 42 and 48 that had no copy, as one JsonImport payload per rule."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from gen_1_8 import Num, result  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402
from gen_33_40 import D, PD, change, chg  # noqa: E402

# ---------------------------------------------------------------- Rule 41: two equal successive decreases
T41 = r"If a value is decreased successively by \(x\%\) and \(x\%\), the final decrease is<br>\[ \left(2x - \frac{x^2}{100}\right)\% \]"


def twice_down(x):
    x = F(x)
    v = 2 * x - x * x / 100
    a = 100 - x
    b = a - a * x / 100
    trad = steps(
        ("Start from 100.", rf"After the first fall of \({D(x)}\%\): \(100 - {D(x)} = {D(a)}\).<br>"
                            rf"After the second fall of \({D(x)}\%\): \({D(a)} - \frac{{{D(x)}}}{{100}}\times {D(a)} = {D(a)} - {D(a * x / 100)} = {D(b)}\)."),
        ("Compare with 100.", rf"\[ 100 - {D(b)} = {D(v)} \]So the value has fallen by \({D(v)}\%\)."))
    rule = steps(
        ("Identify the value.", rf"\(x = {D(x)}\), applied twice."),
        ("Apply the specified rule.", r"\[ \left(2x - \frac{x^2}{100}\right)\% \]"),
        ("Substitute the value.", rf"\[ 2\times {D(x)} - \frac{{{D(x)}^2}}{{100}} = {D(2 * x)} - {D(x * x / 100)} = {D(v)}\% \]"))
    rb = [rf"\(x = {D(x)}\).", r"Decrease \(= 2x - \frac{x^2}{100}\).", rf"\(2\times {D(x)} - \frac{{{D(x)}^2}}{{100}} = {D(v)}\%\)."]
    sc = rf"\[ 2\times {D(x)} - \frac{{{D(x)}^2}}{{100}} = {D(v)}\% \]"
    return result(("number", v), T41, trad, rule, PD(v), rb, sc)


def bill(single, each, diff):
    """A single discount of `single`% and two successive discounts of `each`% differ by Rs diff on a bill: find the bill."""
    single, each, diff = F(single), F(each), F(diff)
    equiv = 2 * each - each * each / 100
    gap = abs(equiv - single)
    B = diff * 100 / gap
    after2 = (100 - each) * (100 - each) / 100
    trad = steps(
        ("Take the bill as Rs 100.", rf"With one discount of \({D(single)}\%\) the customer pays \({D(100 - single)}\).<br>"
                                     rf"With two discounts of \({D(each)}\%\): \(100\to {D(100 - each)}\to {D(100 - each)} - \frac{{{D(each)}}}{{100}}\times {D(100 - each)} = {D(after2)}\)."),
        ("Find the gap on Rs 100.", rf"\[ |{D(100 - single)} - {D(after2)}| = {D(gap)} \]"),
        ("Scale up to the real gap.", rf"A gap of Rs \({D(gap)}\) goes with a bill of Rs 100, so a gap of Rs \({D(diff)}\) goes with<br>"
                                      rf"\[ \frac{{{D(diff)}\times 100}}{{{D(gap)}}} = {D(B)} \]"))
    rule = steps(
        ("Apply the specified rule to the two discounts.", rf"\[ 2\times {D(each)} - \frac{{{D(each)}^2}}{{100}} = {D(2 * each)} - {D(each * each / 100)} = {D(equiv)}\% \]"),
        ("Compare with the single discount.", rf"\[ |{D(equiv)}\% - {D(single)}\%| = {D(gap)}\%\text{{ of the bill}} = \text{{Rs }} {D(diff)} \]"),
        ("Find the bill.", rf"\[ \text{{Bill}} = \frac{{{D(diff)}\times 100}}{{{D(gap)}}} = {D(B)} \]"))
    rb = [rf"Two discounts of \({D(each)}\%\) \(= 2\times {D(each)} - \frac{{{D(each)}^2}}{{100}} = {D(equiv)}\%\).",
          rf"Gap \(= {D(gap)}\%\) of the bill \(=\) Rs \({D(diff)}\).", rf"Bill \(= \frac{{{D(diff)}\times 100}}{{{D(gap)}}} = {D(B)}\)."]
    sc = rf"\[ \frac{{{D(diff)}\times 100}}{{\left(2\times {D(each)} - \frac{{{D(each)}^2}}{{100}}\right) - {D(single)}}} = {D(B)} \]" if equiv > single else \
        rf"\[ \frac{{{D(diff)}\times 100}}{{{D(single)} - \left(2\times {D(each)} - \frac{{{D(each)}^2}}{{100}}\right)}} = {D(B)} \]"
    return result(("number", B), T41, trad, rule, Rsx(B), rb, sc)


# ---------------------------------------------------------------- Rules 42-47: effect on a product of two factors
T42 = (r"If one factor is decreased by \(x\%\) and the other is increased by \(y\%\) (or one is increased by \(x\%\) and the other decreased "
       r"by \(y\%\)), the effect on the product is<br>\[ \left(\text{Inc}\% - \text{Dec}\% - \frac{\text{Inc}\%\times \text{Dec}\%}{100}\right)\% \]"
       r"an increase if the sign is positive and a decrease if it is negative.")
T43 = (r"If one factor is decreased by \(x\%\) and the other is increased by \(x\%\) (or the other way round), the product always decreases, by<br>"
       r"\[ \frac{x^2}{100}\% \]")
T44 = r"If one factor is decreased by \(x\%\) and the other also decreases by \(y\%\), the product decreases by<br>\[ \left(x + y - \frac{xy}{100}\right)\% \]"
T45 = r"If one factor is decreased by \(x\%\) and the other also decreases by \(x\%\), the product decreases by<br>\[ \left(2x - \frac{x^2}{100}\right)\% \]"
T46 = r"If one factor is increased by \(x\%\) and the other increases by \(y\%\), the product increases by<br>\[ \left(x + y + \frac{xy}{100}\right)\% \]"
T47 = r"If one factor is increased by \(x\%\) and the other also increases by \(x\%\), the product increases by<br>\[ \left(2x + \frac{x^2}{100}\right)\% \]"
CTX = {"tax": ("tax", "consumption", "revenue"), "price": ("price", "sale", "income"), "land": ("landholding", "production", "revenue"),
       "seats": ("number of seats", "ticket price", "revenue collected")}


def product(n, a, b, ctx):
    """a, b = signed % changes of the two factors (+ up, - down); n = rule number (42-47) picks the theorem and the rule steps."""
    a, b = F(a), F(b)
    f1, f2, prod = CTX[ctx]
    net = a + b + a * b / 100
    na, nb = 100 + a, 100 + b
    word = "an increase" if net > 0 else "a decrease"
    sg = lambda v: f"+ {D(v)}" if v > 0 else f"- {D(-v)}"
    trad = steps(
        ("Take both factors as 100.", rf"{f1.capitalize()} \(= 100\), {f2} \(= 100\), so the {prod} \(= 100\times 100 = 10000\)."),
        ("Apply the two changes.", rf"New {f1} \(= 100 {sg(a)} = {D(na)}\), new {f2} \(= 100 {sg(b)} = {D(nb)}\).<br>"
                                   rf"\[ \text{{New {prod}}} = {D(na)}\times {D(nb)} = {D(na * nb)} \]"),
        ("Compare with 10000.", rf"\[ \frac{{{D(na * nb)} - 10000}}{{10000}}\times 100 = {D(net)}\% \]So it is {word} of \({D(abs(net))}\%\)."))
    up, dn = max(a, b), -min(a, b)
    if n == 42:
        rule = steps(
            ("Identify the values.", rf"Increase \(= {D(up)}\%\), decrease \(= {D(dn)}\%\)."),
            ("Apply the specified rule.", r"\[ \text{Inc}\% - \text{Dec}\% - \frac{\text{Inc}\%\times \text{Dec}\%}{100} \]"),
            ("Substitute the values.", rf"\[ {D(up)} - {D(dn)} - \frac{{{D(up)}\times {D(dn)}}}{{100}} = {D(up - dn)} - {D(up * dn / 100)} = {D(net)} \]"
                                       rf"The sign is {'positive' if net > 0 else 'negative'}, so it is {word}."))
        calc = rf"{D(up)} - {D(dn)} - \frac{{{D(up)}\times {D(dn)}}}{{100}} = {D(net)}"
    elif n == 43:
        rule = steps(
            ("Identify the value.", rf"One factor goes up and the other down by the same \(x = {D(up)}\)."),
            ("Apply the specified rule.", r"\[ \text{Decrease} = \frac{x^2}{100}\% \]"),
            ("Substitute the value.", rf"\[ \frac{{{D(up)}^2}}{{100}} = \frac{{{D(up * up)}}}{{100}} = {D(-net)}\% \]"))
        calc = rf"\frac{{{D(up)}^2}}{{100}} = {D(-net)}\text{{ (decrease)}}"
    else:
        x, y = abs(a), abs(b)
        sgn = "-" if n in (44, 45) else "+"
        if n in (45, 47):
            rule = steps(
                ("Identify the value.", rf"Both factors change by \(x = {D(x)}\%\)."),
                ("Apply the specified rule.", rf"\[ \left(2x {sgn} \frac{{x^2}}{{100}}\right)\% \]"),
                ("Substitute the value.", rf"\[ 2\times {D(x)} {sgn} \frac{{{D(x)}^2}}{{100}} = {D(2 * x)} {sgn} {D(x * x / 100)} = {D(abs(net))}\% \]"))
            calc = rf"2\times {D(x)} {sgn} \frac{{{D(x)}^2}}{{100}} = {D(abs(net))}"
        else:
            rule = steps(
                ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\)."),
                ("Apply the specified rule.", rf"\[ \left(x + y {sgn} \frac{{xy}}{{100}}\right)\% \]"),
                ("Substitute the values.", rf"\[ {D(x)} + {D(y)} {sgn} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(x + y)} {sgn} {D(x * y / 100)} = {D(abs(net))}\% \]"))
            calc = rf"{D(x)} + {D(y)} {sgn} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(abs(net))}"
    T = {42: T42, 43: T43, 44: T44, 45: T45, 46: T46, 47: T47}[n]
    fin = rf"{word} of \({D(abs(net))}\%\) in the {prod}"
    rb = [rf"{f1.capitalize()}: \({sg(a)}\%\), {f2}: \({sg(b)}\%\).", "Apply the rule for the effect on the product.", rf"\({calc}\), {word}."]
    sc = rf"\[ {calc}\% \]"
    return result(("signed", net), T, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 48: maximum marks from the pass mark
T48 = r"If the pass mark in an examination is \(x\%\) and a candidate who scores \(y\) marks fails by \(z\) marks, then the maximum marks are<br>\[ \frac{100(y + z)}{x} \]"


def max_marks(x, y, z):
    x, y, z = F(x), F(y), F(z)
    M = 100 * (y + z) / x
    trad = steps(
        ("Find the pass mark.", rf"The candidate gets \({D(y)}\) marks and is \({D(z)}\) short, so the pass mark is \({D(y)} + {D(z)} = {D(y + z)}\)."),
        ("Use the unitary method.", rf"\({D(x)}\%\) of the maximum marks is \({D(y + z)}\), so \(1\%\) is \(\frac{{{D(y + z)}}}{{{D(x)}}}\) and \(100\%\) is<br>"
                                    rf"\[ \frac{{{D(y + z)}\times 100}}{{{D(x)}}} = {D(M)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\)."),
        ("Apply the specified rule.", r"\[ \text{Maximum marks} = \frac{100(y + z)}{x} \]"),
        ("Substitute the values.", rf"\[ \frac{{100({D(y)} + {D(z)})}}{{{D(x)}}} = \frac{{{D(100 * (y + z))}}}{{{D(x)}}} = {D(M)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\).", r"Maximum marks \(= \frac{100(y + z)}{x}\).",
          rf"\(\frac{{100({D(y)} + {D(z)})}}{{{D(x)}}} = {D(M)}\)."]
    sc = rf"\[ \frac{{100({D(y)} + {D(z)})}}{{{D(x)}}} = {D(M)} \]"
    return result(("number", M), T48, trad, rule, rf"\({D(M)}\) marks", rb, sc)


# ---------------------------------------------------------------- rule cards
def product_card(n, title, statement, formula, visual, pattern, example, mistake):
    return card(n, title, statement, formula, visual,
                r"Revenue \(=\) Tax \(\times\) Consumption (Income \(=\) Price \(\times\) Sales, Revenue \(=\) Seats \(\times\) Ticket price): "
                r"the two factors' growth factors multiply, \(\frac{100 + a}{100}\times\frac{100 + b}{100}\).", pattern, example, mistake)


CARDS = {
    41: card(41, "Two Equal Successive Decreases",
             r"If a value is decreased successively by \(x\%\) and \(x\%\), the final decrease is \(\left(2x - \frac{x^2}{100}\right)\%\). "
             r"Two successive discounts of \(x\%\) are therefore worth one discount of \(\left(2x - \frac{x^2}{100}\right)\%\).",
             r"\[ \text{Final decrease} = \left(2x - \frac{x^2}{100}\right)\% \]",
             [("Start", "100"), ("After the first x% fall", "100 - x"), ("After the second x% fall", r"100 - 2x + \frac{x^2}{100}")],
             r"The second fall is taken on the already-reduced value, so it is smaller than the first by \(\frac{x^2}{100}\).",
             "Population (price, value) falls by the same x% two years running; or two equal successive discounts compared with a single discount.",
             r"\(12\%\) twice: \(24 - \frac{144}{100} = 22.56\%\).",
             r"Answering \(2x\) (\(24\%\)) - the total fall is less than that."),
    42: product_card(42, "Effect on a Product: One Factor Up, the Other Down",
                     r"If one factor is decreased by \(x\%\) and the other increased by \(y\%\) (or the other way round), the effect on the product is "
                     r"Inc% \(-\) Dec% \(-\) \(\frac{\text{Inc\%}\times\text{Dec\%}}{100}\): an increase if positive, a decrease if negative.",
                     r"\[ \text{Effect} = \left(\text{Inc}\% - \text{Dec}\% - \frac{\text{Inc}\%\times \text{Dec}\%}{100}\right)\% \]",
                     [("Factors", r"100\times 100 = 10000"), ("After the changes", r"(100 + \text{Inc})(100 - \text{Dec})"),
                      ("Effect", r"\text{Inc} - \text{Dec} - \frac{\text{Inc}\times\text{Dec}}{100}")],
                     "Tax cut but consumption up (revenue?), price up but sales down (income?) - one factor rises, the other falls.",
                     r"Tax \(-20\%\), consumption \(+15\%\): \(15 - 20 - 3 = -8\), a decrease of \(8\%\).",
                     r"Taking only Inc \(-\) Dec, or forgetting that a negative result is a DECREASE."),
    43: product_card(43, "Effect on a Product: Equal Rise and Fall",
                     r"If one factor is decreased by \(x\%\) and the other increased by \(x\%\) (or the other way round), the product always "
                     r"DECREASES, by \(\frac{x^2}{100}\%\).",
                     r"\[ \text{Decrease in the product} = \frac{x^2}{100}\% \]",
                     [("Factors", "100, 100"), ("After the changes", "100 - x,\ 100 + x"), ("Product", r"10000 - x^2")],
                     "Tax and consumption (price and sales) change by the SAME percentage in opposite directions.",
                     r"\(25\%\) each way: \(\frac{625}{100} = 6.25\%\) decrease.",
                     r"Saying 'no change' because the two percentages are equal."),
    44: product_card(44, "Effect on a Product: Both Factors Down",
                     r"If one factor decreases by \(x\%\) and the other also decreases by \(y\%\), the product decreases by \(\left(x + y - \frac{xy}{100}\right)\%\).",
                     r"\[ \text{Decrease in the product} = \left(x + y - \frac{xy}{100}\right)\% \]",
                     [("Factors", "100, 100"), ("After the changes", "100 - x,\ 100 - y"), ("Fall in the product", r"x + y - \frac{xy}{100}")],
                     "Landholding and production both fall (revenue?), seats and ticket price both fall by different percentages.",
                     r"\(10\%\) and \(8\%\): \(18 - 0.8 = 17.2\%\) decrease.",
                     r"Adding \(x + y\) only."),
    45: product_card(45, "Effect on a Product: Both Factors Down by the Same %",
                     r"If one factor decreases by \(x\%\) and the other also decreases by \(x\%\), the product decreases by \(\left(2x - \frac{x^2}{100}\right)\%\).",
                     r"\[ \text{Decrease in the product} = \left(2x - \frac{x^2}{100}\right)\% \]",
                     [("Factors", "100, 100"), ("After the changes", "100 - x,\ 100 - x"), ("Fall in the product", r"2x - \frac{x^2}{100}")],
                     "Both factors (seats and ticket price) fall by the SAME percentage.",
                     r"\(5\%\) and \(5\%\): \(10 - 0.25 = 9.75\%\) decrease.",
                     r"Answering \(2x\)."),
    46: product_card(46, "Effect on a Product: Both Factors Up",
                     r"If one factor increases by \(x\%\) and the other increases by \(y\%\), the product increases by \(\left(x + y + \frac{xy}{100}\right)\%\).",
                     r"\[ \text{Increase in the product} = \left(x + y + \frac{xy}{100}\right)\% \]",
                     [("Factors", "100, 100"), ("After the changes", "100 + x,\ 100 + y"), ("Rise in the product", r"x + y + \frac{xy}{100}")],
                     "Seats and ticket price (land and production) both rise by different percentages.",
                     r"\(25\%\) and \(10\%\): \(35 + 2.5 = 37.5\%\) increase.",
                     r"Adding \(x + y\) only."),
    47: product_card(47, "Effect on a Product: Both Factors Up by the Same %",
                     r"If one factor increases by \(x\%\) and the other also increases by \(x\%\), the product increases by \(\left(2x + \frac{x^2}{100}\right)\%\).",
                     r"\[ \text{Increase in the product} = \left(2x + \frac{x^2}{100}\right)\% \]",
                     [("Factors", "100, 100"), ("After the changes", "100 + x,\ 100 + x"), ("Rise in the product", r"2x + \frac{x^2}{100}")],
                     "Both factors (landholding and production) rise by the SAME percentage.",
                     r"\(10\%\) and \(10\%\): \(20 + 1 = 21\%\) increase.",
                     r"Answering \(2x\)."),
    48: card(48, "Maximum Marks from the Pass Mark",
             r"If the pass mark is \(x\%\) and a candidate who scores \(y\) marks fails by \(z\) marks, the maximum marks are \(\frac{100(y + z)}{x}\).",
             r"\[ \text{Maximum marks} = \frac{100(y + z)}{x} \]",
             [("Pass mark", "y + z"), ("Pass mark as %", r"x\%\text{ of the maximum}"), ("Maximum", r"\frac{100(y + z)}{x}")],
             r"The pass mark is the candidate's score plus the shortfall, and it is \(x\%\) of the maximum - Rule 4 with \(y + z\) in place of \(y\).",
             "'Pass mark x%. A candidate gets y marks and fails by z marks. Find the maximum marks.'",
             r"\(40\%\) to pass, gets \(40\), fails by \(40\): \(\frac{100\times 80}{40} = 200\).",
             r"Using \(y\) alone (or \(y - z\)) instead of \(y + z\)."),
}

OLD = {
    41: {629: (lambda: twice_down(12), "The population of a town was reduced by 12% in the year 1988. In 1989 it was again reduced by 12%. By what "
                                       "percentage had the population decreased at the beginning of 1990?",
               {"a": PD(F(1128, 5)), "b": PD(F(282, 125)), "c": PD(F(564, 25)), "d": PD(F(1311, 50))})},
    42: {630: (lambda: product(42, -20, 15, "tax"), "The tax on a commodity is diminished by 20% and its consumption increases by 15%. Find the effect "
                                                    "on the revenue.",
               dict(zip("abcd", chg([("Decrease", 8), ("Increase", F(9, 5)), ("Increase", 8), ("Decrease", F(4, 5))]))))},
    43: {631: (lambda: product(43, -25, 25, "tax"), "The tax on a commodity is diminished by 25% and its consumption increases by 25%. Find the "
                                                    "effect on the revenue.",
               dict(zip("abcd", chg([("Decrease", 50), ("none", 0), ("Increase", F(25, 4)), ("Decrease", F(25, 4))]))))},
    44: {632: (lambda: product(44, -10, -8, "land"), "The landholding of a person is decreased by 10% due to a late monsoon, and the production "
                                                     "decreases by 8%. What is the effect on the revenue?",
               dict(zip("abcd", chg([("Decrease", F(127, 10)), ("Decrease", F(86, 5)), ("Decrease", 17), ("Decrease", 27)]))))},
    45: {633: (lambda: product(45, -5, -5, "seats"), "The number of seats in a cinema hall is decreased by 5%. The price of a ticket is also "
                                                     "decreased by 5%. What is the effect on the revenue collected?",
               dict(zip("abcd", chg([("Decrease", F(159, 20)), ("Decrease", F(169, 25)), ("Decrease", F(39, 4)), ("Decrease", 11)]))))},
    46: {634: (lambda: product(46, 25, 10, "seats"), "The number of seats in a cinema hall is increased by 25%. The price of a ticket is also "
                                                     "increased by 10%. What is the effect on the revenue collected?",
               dict(zip("abcd", chg([("Increase", F(357, 10)), ("Increase", F(75, 2)), ("Increase", 35), ("Increase", 33)]))))},
    47: {635: (lambda: product(47, 10, 10, "land"), "The landholding of a person is increased by 10%. Due to an early monsoon, the production "
                                                    "increases by 10%. What is the effect on the revenue?",
               dict(zip("abcd", chg([("Increase", 31), ("Increase", 21), ("Increase", 55), ("Increase", 36)]))))},
    48: {636: (lambda: max_marks(40, 40, 40), "A student has to secure 40% marks to get through. If he gets 40 marks and fails by 40 marks, find "
                                              "the maximum marks set for the examination.", None)},
}


def ch(sign, vals):
    return chg([("Increase" if s > 0 else "Decrease", v) if s else ("none", 0) for s, v in vals])


NEW = {
    41: [("r41_e1", "The population of a town was reduced by 6% in one year. In the next year it was again reduced by 6%. By what percentage had "
                    "the population decreased at the end of the two years?", lambda: twice_down(6), [PD(12), PD(F(291, 25)), PD(F(573, 50)), PD(F(309, 25))], 2),
         ("r41_e2", "The population of a town was reduced by 30% in one year and again by 30% the next year. By what percentage had the population "
                    "decreased at the end of the two years?", lambda: twice_down(30), [PD(60), PD(51), PD(49), PD(54)], 2),
         ("r41_e3", "The population of a town was reduced by 14% in one year and again by 14% the next year. By what percentage had the population "
                    "decreased at the end of the two years?", lambda: twice_down(14), [PD(F(651, 25)), PD(28), PD(F(649, 25)), PD(F(601, 25))], 1),
         ("r41_e4", "The population of a town was reduced by 40% in one year and again by 40% the next year. By what percentage had the population "
                    "decreased at the end of the two years?", lambda: twice_down(40), [PD(80), PD(60), PD(56), PD(64)], 4),
         ("r41_e5", "The population of a town was reduced by 25% in one year and again by 25% the next year. By what percentage had the population "
                    "decreased at the end of the two years?", lambda: twice_down(25), [PD(50), PD(45), PD(F(175, 4)), PD(F(173, 4))], 3),
         ("r41_e6", "The difference between a single discount of 50% and two successive discounts of 30% each on a bill is Rs 18. Find the amount "
                    "of the bill.", lambda: bill(50, 30, 18), [Rsx(180), Rsx(1800), Rsx(900), Rsx(3600)], 2)],
    42: [("r42_ex2", "If the price of an article is increased by 20% and its sale is decreased by 10%, what will be the effect on the income?",
          lambda: product(42, 20, -10, "price"), ch(1, [(1, 8), (1, 10), (-1, 8), (1, 12)]), 1),
         ("r42_ex3", "If the price of an article is decreased by 25% and its sale is increased by 20%, what will be the effect on the income?",
          lambda: product(42, -25, 20, "price"), ch(1, [(-1, 5), (-1, 10), (1, 5), (-1, 15)]), 2),
         ("r42_e1", "The tax on a commodity is diminished by 30% and its consumption increases by 20%. Find the effect on the revenue.",
          lambda: product(42, -30, 20, "tax"), ch(1, [(-1, 10), (1, 4), (-1, 16), (-1, 4)]), 3),
         ("r42_e2", "The tax on a commodity is diminished by 10% and its consumption increases by 25%. Find the effect on the revenue.",
          lambda: product(42, -10, 25, "tax"), ch(1, [(1, 15), (1, F(35, 2)), (-1, F(25, 2)), (1, F(25, 2))]), 4),
         ("r42_e3", "If the price of an article is increased by 15% and its sale is decreased by 8%, what will be the effect on the income?",
          lambda: product(42, 15, -8, "price"), ch(1, [(1, F(29, 5)), (1, 7), (-1, F(29, 5)), (1, F(41, 5))]), 1),
         ("r42_e4", "If the price of an article is increased by 18% and its sale is decreased by 16%, what will be the effect on the income?",
          lambda: product(42, 18, -16, "price"), ch(1, [(1, 2), (-1, F(22, 25)), (1, F(22, 25)), (-1, F(72, 25))]), 2),
         ("r42_e5", "If the price of an article is increased by 4% and its sale is decreased by 20%, what will be the effect on the income?",
          lambda: product(42, 4, -20, "price"), ch(1, [(-1, 16), (1, F(84, 5)), (-1, F(84, 5)), (-1, F(76, 5))]), 3)],
    43: [("r43_e%d" % i, f"The tax on a commodity is diminished by {x}% and its consumption increases by {x}%. Find the effect on the revenue.",
          (lambda x=x: product(43, -x, x, "tax")), ch(1, rows), pos)
         for i, (x, rows, pos) in enumerate([
             (13, [(-1, F(169, 100)), (1, F(169, 100)), (0, 0), (-1, F(269, 100))], 1),
             (18, [(1, F(81, 25)), (-1, F(81, 25)), (0, 0), (-1, F(106, 25))], 2),
             (21, [(1, F(441, 100)), (0, 0), (-1, F(441, 100)), (-1, F(541, 100))], 3),
             (26, [(1, F(169, 25)), (-1, F(194, 25)), (0, 0), (-1, F(169, 25))], 4),
             (35, [(-1, F(49, 4)), (1, F(49, 4)), (0, 0), (-1, F(53, 4))], 1)], 1)],
    44: [("r44_e1", "The landholding of a person is decreased by 14% due to a late monsoon, and the production decreases by 5%. What is the "
                    "effect on the revenue?", lambda: product(44, -14, -5, "land"), ch(1, [(-1, 19), (-1, F(183, 10)), (1, F(183, 10)), (-1, F(177, 10))]), 2),
         ("r44_e2", "The landholding of a person is decreased by 20% due to a late monsoon, and the production decreases by 10%. What is the "
                    "effect on the revenue?", lambda: product(44, -20, -10, "land"), ch(1, [(-1, 30), (-1, 32), (-1, 28), (1, 28)]), 3),
         ("r44_e3", "The landholding of a person is decreased by 25% due to a late monsoon, and the production decreases by 12%. What is the "
                    "effect on the revenue?", lambda: product(44, -25, -12, "land"), ch(1, [(-1, 37), (1, 34), (-1, 40), (-1, 34)]), 4)],
    45: [("r45_e1", "The number of seats in a cinema hall is decreased by 6%. The price of a ticket is also decreased by 6%. What is the effect "
                    "on the revenue collected?", lambda: product(45, -6, -6, "seats"), ch(1, [(-1, F(291, 25)), (-1, 12), (1, F(291, 25)), (-1, F(309, 25))]), 1),
         ("r45_e2", "The number of seats in a cinema hall is decreased by 15%. The price of a ticket is also decreased by 15%. What is the effect "
                    "on the revenue collected?", lambda: product(45, -15, -15, "seats"), ch(1, [(-1, 30), (-1, F(111, 4)), (1, F(111, 4)), (-1, F(129, 4))]), 2),
         ("r45_e3", "The number of seats in a cinema hall is decreased by 30%. The price of a ticket is also decreased by 30%. What is the effect "
                    "on the revenue collected?", lambda: product(45, -30, -30, "seats"), ch(1, [(-1, 60), (-1, 49), (-1, 51), (1, 51)]), 3)],
    46: [("r46_e1", "The number of seats in a cinema hall is increased by 20%. The price of a ticket is also increased by 5%. What is the effect "
                    "on the revenue collected?", lambda: product(46, 20, 5, "seats"), ch(1, [(1, 25), (1, 26), (-1, 26), (1, 24)]), 2),
         ("r46_e2", "The number of seats in a cinema hall is increased by 40%. The price of a ticket is also increased by 10%. What is the effect "
                    "on the revenue collected?", lambda: product(46, 40, 10, "seats"), ch(1, [(1, 50), (1, 44), (-1, 54), (1, 54)]), 4),
         ("r46_e3", "The number of seats in a cinema hall is increased by 15%. The price of a ticket is also increased by 12%. What is the effect "
                    "on the revenue collected?", lambda: product(46, 15, 12, "seats"), ch(1, [(1, F(144, 5)), (1, 27), (-1, F(144, 5)), (1, F(132, 5))]), 1)],
    47: [("r47_e1", "The landholding of a person is increased by 11%. Due to an early monsoon, the production increases by 11%. What is the effect "
                    "on the revenue?", lambda: product(47, 11, 11, "land"), ch(1, [(1, 22), (1, F(2121, 100)), (-1, F(2321, 100)), (1, F(2321, 100))]), 4),
         ("r47_e2", "The landholding of a person is increased by 15%. Due to an early monsoon, the production increases by 15%. What is the effect "
                    "on the revenue?", lambda: product(47, 15, 15, "land"), ch(1, [(1, F(129, 4)), (1, 30), (1, F(117, 4)), (-1, F(129, 4))]), 1),
         ("r47_e3", "The landholding of a person is increased by 25%. Due to an early monsoon, the production increases by 25%. What is the effect "
                    "on the revenue?", lambda: product(47, 25, 25, "land"), ch(1, [(1, 50), (1, F(175, 4)), (1, F(225, 4)), (-1, F(225, 4))]), 3)],
    48: [("r48_ex2", "In an examination, a candidate must get 70% marks to pass. If a candidate who gets 240 marks fails by 40 marks, find the "
                     "maximum marks.", lambda: max_marks(70, 240, 40), [Num(380), Num(400), Num(360), Num(350)], 2),
         ("r48_e1", "A student has to secure 25% marks to get through. If he gets 45 marks and fails by 30 marks, find the maximum marks set for "
                    "the examination.", lambda: max_marks(25, 45, 30), [Num(180), Num(240), Num(300), Num(375)], 3),
         ("r48_e2", "A student has to secure 12% marks to get through. If he gets 60 marks and fails by 30 marks, find the maximum marks set for "
                    "the examination.", lambda: max_marks(12, 60, 30), [Num(500), Num(600), Num(900), Num(750)], 4),
         ("r48_e3", "A student has to secure 18% marks to get through. If he gets 99 marks and fails by 45 marks, find the maximum marks set for "
                    "the examination.", lambda: max_marks(18, 99, 45), [Num(800), Num(550), Num(750), Num(900)], 1),
         ("r48_e4", "In an examination, a candidate must get 45% marks to pass. If a candidate who gets 150 marks fails by 30 marks, find the "
                    "maximum marks.", lambda: max_marks(45, 150, 30), [Num(360), Num(400), Num(450), Num(300)], 2),
         ("r48_e5", "In an examination, a candidate must get 64% marks to pass. If a candidate who gets 140 marks fails by 20 marks, find the "
                    "maximum marks.", lambda: max_marks(64, 140, 20), [Num(200), Num(300), Num(250), Num(225)], 3),
         ("r48_e6", "In an examination, a candidate must get 55% marks to pass. If a candidate who gets 580 marks fails by 25 marks, find the "
                    "maximum marks.", lambda: max_marks(55, 580, 25), [Num(1050), Num(1200), Num(1000), Num(1100)], 4)],
}


def main():
    for n in range(41, 49):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, opts) in OLD[n].items():
            extra = {"question": question, **(opts or {})}
            if rows[rid]["e"] is None or rows[rid]["e"].strip():
                extra["e"] = ""
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn, op, pos in NEW[n]:
            g = fn()
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "percentage", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
