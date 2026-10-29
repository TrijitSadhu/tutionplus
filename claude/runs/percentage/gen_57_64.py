"""Rules 57-64: writes the eight rule cards, regenerates the old worked-example rows 642-649 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their text and
options (642 had no option holding Rs 25; 646's "80.76%" is written exactly as 80 10/13%), and adds the book exercises
(numbers changed, wording rewritten) as one JsonImport payload per rule."""
import json, os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, frac, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import P, result  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402
from gen_17_24 import backward  # noqa: E402
from gen_33_40 import D  # noqa: E402


def L(v):
    return rf"\({D(v)}\) litres"


def KG(v):
    return rf"\({D(v)}\) kg"


def per_kg(v):
    return rf"Rs \({D(v)}\) per kg"


# ---------------------------------------------------------------- Rule 57: manufacturer -> wholesaler -> retailer
T57 = (r"The manufacturer of an article makes a profit of \(x\%\), the wholesale dealer \(y\%\) and the retailer \(z\%\). If the retailer sells it "
       r"for Rs \(A\), the cost of manufacturing is<br>\[ A\left(\frac{100}{100 + x}\right)\left(\frac{100}{100 + y}\right)\left(\frac{100}{100 + z}\right) \]")


def maker(x, y, z, A):
    return backward(A, [x, y, z], "+", T57, Rsx, "the cost of manufacturing")


# ---------------------------------------------------------------- Rules 58-60: changing a mixture's strength
T58 = r"In \(A\) litres of \(x\%\) acidic liquid, the water to be ADDED to make it \(y\%\) acidic (\(x \gt y\)) is<br>\[ \frac{A(x - y)}{y}\text{ litres} \]"
T59 = r"In \(A\) litres of \(x\%\) acidic liquid, the water to be TAKEN OUT to make it \(y\%\) acidic (\(y \gt x\)) is<br>\[ \frac{A(y - x)}{y}\text{ litres} \]"
T60 = (r"When a quantity of B is added to a mixture of A and B to change the percentage of A, the quantity of B to be added is<br>"
       r"\[ \frac{\text{Previous \% of A}}{\text{Changed \% of A}}\times \text{Mixture} - \text{Mixture} \]")


def water(A, x, y):
    """Rule 58 when x > y (add water), Rule 59 when y > x (take water out)."""
    A, x, y = F(A), F(x), F(y)
    acid = A * x / 100
    new = acid * 100 / y
    v = abs(new - A)
    add = x > y
    trad = steps(
        ("The acid does not change.", rf"Acid \(= \frac{{{D(x)}}}{{100}}\times {D(A)} = {D(acid)}\) litres."),
        ("Find the new total.", rf"For the acid to be \({D(y)}\%\) of the liquid, the liquid must be \(\frac{{{D(acid)}\times 100}}{{{D(y)}}} = {D(new)}\) litres."),
        ("Compare.", rf"\[ {'%s - %s' % (D(new), D(A)) if add else '%s - %s' % (D(A), D(new))} = {D(v)}\text{{ litres of water {'added' if add else 'taken out'}}} \]"))
    num = rf"{D(A)}({D(x)} - {D(y)})" if add else rf"{D(A)}({D(y)} - {D(x)})"
    rule = steps(
        ("Identify the values.", rf"\(A = {D(A)}\), \(x = {D(x)}\), \(y = {D(y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{A(x - y)}{y} \]" if add else r"\[ \frac{A(y - x)}{y} \]"),
        ("Substitute the values.", rf"\[ \frac{{{num}}}{{{D(y)}}} = \frac{{{D(A * abs(x - y))}}}{{{D(y)}}} = {D(v)} \]"))
    rb = [rf"\(A = {D(A)}\), \(x = {D(x)}\), \(y = {D(y)}\).", r"Water \(= \frac{A(x - y)}{y}\)." if add else r"Water \(= \frac{A(y - x)}{y}\).",
          rf"\(\frac{{{num}}}{{{D(y)}}} = {D(v)}\) litres."]
    sc = rf"\[ \frac{{{num}}}{{{D(y)}}} = {D(v)}\text{{ litres}} \]"
    return result(("number", v), T58 if add else T59, trad, rule, L(v), rb, sc)


def add_other(M, prev, new, a_name, b_name):
    M, prev, new = F(M), F(prev), F(new)
    a = M * prev / 100
    total = a * 100 / new
    v = total - M
    trad = steps(
        (f"The {a_name} does not change.", rf"{a_name.capitalize()} \(= \frac{{{D(prev)}}}{{100}}\times {D(M)} = {D(a)}\) kg."),
        ("Find the new mixture.", rf"For this to be \({D(new)}\%\), the mixture must weigh \(\frac{{{D(a)}\times 100}}{{{D(new)}}} = {D(total)}\) kg."),
        (f"Find the {b_name} to add.", rf"\[ {D(total)} - {D(M)} = {D(v)}\text{{ kg}} \]"))
    rule = steps(
        ("Identify the values.", rf"Previous % of {a_name} \(= {D(prev)}\), changed % \(= {D(new)}\), mixture \(= {D(M)}\) kg."),
        ("Apply the specified rule.", r"\[ \frac{\text{Previous \%}}{\text{Changed \%}}\times \text{Mixture} - \text{Mixture} \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(prev)}}}{{{D(new)}}}\times {D(M)} - {D(M)} = {D(total)} - {D(M)} = {D(v)} \]"))
    rb = [rf"Previous \({D(prev)}\%\), changed \({D(new)}\%\), mixture \({D(M)}\) kg.", r"Add \(\frac{\text{prev}}{\text{new}}\times M - M\).",
          rf"\(\frac{{{D(prev)}}}{{{D(new)}}}\times {D(M)} - {D(M)} = {D(v)}\) kg."]
    sc = rf"\[ \frac{{{D(prev)}}}{{{D(new)}}}\times {D(M)} - {D(M)} = {D(v)}\text{{ kg}} \]"
    return result(("number", v), T60, trad, rule, KG(v), rb, sc)


# ---------------------------------------------------------------- Rule 61: two schools
T61 = (r"If \(p\%\) of the students who appeared from school A qualified, \(a\%\) more students appeared from school B and \(q\%\) more qualified "
       r"from school B than from A, the percentage qualified in school B is<br>\[ \frac{p(100 + q)}{100 + a}\% \]")


def schools(p, a, q, A="A", B="B"):
    p, a, q = F(p), F(a), F(q)
    v = p * (100 + q) / (100 + a)
    qb = p + p * q / 100
    trad = steps(
        (f"Take 100 students in school {A}.", rf"Qualified in {A} \(= {D(p)}\). Appeared in {B} \(= 100 + {D(a)} = {D(100 + a)}\)."),
        (f"Qualified in school {B}.", rf"\[ {D(p)} + \frac{{{D(q)}}}{{100}}\times {D(p)} = {D(qb)} \]"),
        ("Find the percentage.", rf"\[ \frac{{{D(qb)}}}{{{D(100 + a)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(p = {D(p)}\), \(a = {D(a)}\), \(q = {D(q)}\)."),
        ("Apply the specified rule.", r"\[ \frac{p(100 + q)}{100 + a}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(p)}\times {D(100 + q)}}}{{{D(100 + a)}}} = \frac{{{D(p * (100 + q))}}}{{{D(100 + a)}}} = {tex(v)}\% \]"))
    rb = [rf"\(p = {D(p)}\), \(a = {D(a)}\), \(q = {D(q)}\).", r"School B \(= \frac{p(100 + q)}{100 + a}\%\).",
          rf"\(\frac{{{D(p)}\times {D(100 + q)}}}{{{D(100 + a)}}} = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{D(p)}\times {D(100 + q)}}}{{{D(100 + a)}}} = {tex(v)}\% \]"
    return result(("number", v), T61, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rule 62: old price X, new price Y
T62 = (r"If the original price of a commodity is Rs \(X\) and the new price is Rs \(Y\), then the decrease (or increase) in consumption so as not to "
       r"increase (or decrease) the expenditure is<br>\[ \frac{|Y - X|}{Y}\times 100\% = \frac{\text{Difference in price}}{\text{New price}}\times 100\% \]")


def two_prices(X, Y):
    X, Y = F(X), F(Y)
    v = abs(Y - X) / Y * 100
    word = "reduce" if Y > X else "increase"
    c = X * 100 / Y
    trad = steps(
        ("Keep the expenditure fixed.", rf"Suppose the family used 100 kg at Rs \({D(X)}\): expenditure \(= {D(X * 100)}\)."),
        ("Find the consumption at the new price.", rf"\[ \frac{{{D(X * 100)}}}{{{D(Y)}}} = {tex(c)}\text{{ kg}} \]"),
        ("Compare with 100 kg.", rf"\[ |{tex(c)} - 100| = {tex(v)} \]so the consumption must {word} by \({tex(v)}\%\)."))
    rule = steps(
        ("Identify the values.", rf"\(X = {D(X)}\), \(Y = {D(Y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{\text{Difference in price}}{\text{New price}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(abs(Y - X))}}}{{{D(Y)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"Old price \({D(X)}\), new price \({D(Y)}\).", r"Change \(= \frac{\text{difference}}{\text{new price}}\times 100\).",
          rf"\(\frac{{{D(abs(Y - X))}}}{{{D(Y)}}}\times 100 = {tex(v)}\%\) ({word})."]
    sc = rf"\[ \frac{{{D(abs(Y - X))}}}{{{D(Y)}}}\times 100 = {tex(v)}\% \]"
    return result(("number", v), T62, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rule 63: a cut of Rs d buys q more for Rs E
T63 = (r"If the original price of a commodity is Rs \(O\) and the new price is Rs \(N\), then with the expenditure \(E\) kept the same, the change "
       r"in the quantity bought is<br>\[ \Delta Q = \frac{E(O - N)}{N\times O} \]")


def cut_by_rupees(d, q, E, unit="kg"):
    d, q, E = F(d), F(q), F(E)
    k = E * d / q                                         # O(O - d) = k
    disc = d * d + 4 * k
    r = isqrt(int(disc))
    assert r * r == disc
    O = (d + r) / 2
    other = (d - r) / 2
    trad = steps(
        ("Write the two purchases.", rf"Let the original price be Rs \(O\) per {unit}. For Rs \({D(E)}\) one gets \(\frac{{{D(E)}}}{{O}}\) {unit} before and "
                                     rf"\(\frac{{{D(E)}}}{{O - {D(d)}}}\) {unit} after the cut:<br>\[ \frac{{{D(E)}}}{{O - {D(d)}}} - \frac{{{D(E)}}}{{O}} = {D(q)} \]"),
        ("Clear the fractions.", rf"\[ {D(E)}\times {D(d)} = {D(q)}\,O(O - {D(d)}) \Rightarrow O^2 - {D(d)}O - {D(k)} = 0 \]"),
        ("Solve.", rf"\[ (O - {D(O)})(O + {D(-other)}) = 0 \Rightarrow O = {D(O)}\text{{ (a price cannot be negative)}} \]"))
    rule = steps(
        ("Identify the values.", rf"\(\Delta Q = {D(q)}\), \(O - N = {D(d)}\), \(E = {D(E)}\), so \(N = O - {D(d)}\)."),
        ("Apply the specified rule.", r"\[ \Delta Q = \frac{E(O - N)}{N\times O} \]"),
        ("Substitute and solve.", rf"\[ {D(q)} = \frac{{{D(E)}\times {D(d)}}}{{(O - {D(d)})O}} \Rightarrow O^2 - {D(d)}O - {D(k)} = 0 \Rightarrow O = {D(O)} \]"))
    rb = [rf"\(\Delta Q = {D(q)}\), \(O - N = {D(d)}\), \(E = {D(E)}\).", r"\(\Delta Q = \frac{E(O - N)}{N O}\).",
          rf"\(O^2 - {D(d)}O - {D(k)} = 0\), so \(O = {D(O)}\)."]
    sc = rf"\[ {D(q)} = \frac{{{D(E)}\times {D(d)}}}{{(O - {D(d)})O}} \Rightarrow O = {D(O)} \]"
    return result(("number", O), T63, trad, rule, rf"Rs \({D(O)}\) per {unit}", rb, sc)


# ---------------------------------------------------------------- Rule 64: a cut of p% buys q more for Rs E
T64 = (r"If a reduction of \(p\%\) in the price lets a buyer get \(\Delta Q\) more for the same expenditure \(E\), then the reduced price is "
       r"\[ N = \frac{p\times E}{\Delta Q\times 100} \]and the original price is \(O = \frac{100N}{100 - p}\) (since \(p = \frac{O - N}{O}\times 100\)).")


def cut_by_percent(p, q, E, ask="orig", unit="kg", item="tea"):
    """ask: 'orig' (original price), 'both' (reduced, original), 'count_before' (how many per rupee before the cut)."""
    p, q, E = F(p), F(q), F(E)
    N = p * E / (q * 100)
    O = N * 100 / (100 - p)
    saved = E * p / 100
    trad = steps(
        ("See what the cut saves.", rf"A \({tex(p)}\%\) cut on Rs \({D(E)}\) worth of {item} saves \(\frac{{{tex(p)}}}{{100}}\times {D(E)} = {tex(saved)}\) rupees."),
        ("This saving buys the extra quantity.", rf"The saving buys \({D(q)}\) more {unit} at the new price, so<br>\[ \text{{New price}} = \frac{{{tex(saved)}}}{{{D(q)}}} = {tex(N)} \]"),
        ("Find the original price.", rf"The new price is \({tex(100 - p)}\%\) of the old one:<br>\[ \text{{Old price}} = \frac{{{tex(N)}\times 100}}{{{tex(100 - p)}}} = {tex(O)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(p = {tex(p)}\), \(\Delta Q = {D(q)}\), \(E = {D(E)}\)."),
        ("Apply the specified rule.", r"\[ N = \frac{p\times E}{\Delta Q\times 100},\qquad O = \frac{100N}{100 - p} \]"),
        ("Substitute the values.", rf"\[ N = \frac{{{tex(p)}\times {D(E)}}}{{{D(q)}\times 100}} = {tex(N)},\qquad O = \frac{{100\times {tex(N)}}}{{{tex(100 - p)}}} = {tex(O)} \]"))
    rb = [rf"\(p = {tex(p)}\), \(\Delta Q = {D(q)}\), \(E = {D(E)}\).", r"\(N = \frac{pE}{100\Delta Q}\), \(O = \frac{100N}{100 - p}\).",
          rf"\(N = {tex(N)}\), \(O = {tex(O)}\)."]
    sc = rf"\[ N = \frac{{{tex(p)}\times {D(E)}}}{{{D(q)}\times 100}} = {tex(N)},\qquad O = \frac{{100\times {tex(N)}}}{{{tex(100 - p)}}} = {tex(O)} \]"
    if ask == "both":
        fin = rf"reduced price Re \({frac(N)}\), original price Re \({frac(O)}\)" if O < 1 else rf"reduced price Rs \({tex(N)}\), original price Rs \({tex(O)}\)"
        return result(("pair", (N, O)), T64, trad, rule, fin, rb, sc)
    if ask == "count_before":
        n = 1 / O
        extra = (f"Turn the price into a count.", rf"At Re \({frac(O)}\) each, one rupee bought \({tex(n)}\) {item} before the cut.")
        trad += "<br><br>" + rf"<b>Step 4: {extra[0]}</b><br>{extra[1]}"
        rule += "<br><br>" + rf"<b>Step 4: {extra[0]}</b><br>{extra[1]}"
        rb.append(rf"Before the cut: \({tex(n)}\) for a rupee.")
        return result(("number", n), T64, trad, rule, rf"\({tex(n)}\) {item} for a rupee", rb, sc)
    return result(("number", O), T64, trad, rule, rf"Rs \({tex(O)}\) per {unit}", rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    57: card(57, "Manufacturing Cost through a Chain of Profits",
             r"The manufacturer makes \(x\%\) profit, the wholesale dealer \(y\%\) and the retailer \(z\%\). If the retailer sells for Rs \(A\), the "
             r"manufacturing cost is \(A\left(\frac{100}{100 + x}\right)\left(\frac{100}{100 + y}\right)\left(\frac{100}{100 + z}\right)\).",
             r"\[ \text{Cost of manufacturing} = A\left(\frac{100}{100 + x}\right)\left(\frac{100}{100 + y}\right)\left(\frac{100}{100 + z}\right) \]",
             [("Manufacturer sells at", r"C\times\frac{100 + x}{100}"), ("Wholesaler sells at", r"\times\frac{100 + y}{100}"), ("Retailer sells at", r"\times\frac{100 + z}{100} = A")],
             r"Each seller adds his profit on the price HE paid, so the factors multiply; divide them out to get back to the cost.",
             "A chain of sellers each adds a profit %; the final selling price is given and the original cost is asked.",
             r"\(25\%\), \(20\%\), \(28\%\), Rs 48: \(48\times\frac{100}{128}\times\frac{100}{120}\times\frac{100}{125} =\) Rs 25.",
             r"Adding the profits (\(25 + 20 + 28 = 73\%\)) and dividing by 173."),
    58: card(58, "Water to Add to Dilute an Acid",
             r"In \(A\) litres of \(x\%\) acidic liquid, the water to be added to make it \(y\%\) acidic (\(x \gt y\)) is \(\frac{A(x - y)}{y}\) litres.",
             r"\[ \text{Water added} = \frac{A(x - y)}{y}\text{ litres} \]",
             [("Acid (fixed)", r"\frac{x}{100}A"), ("New total", r"\frac{xA}{y}"), ("Water added", r"\frac{xA}{y} - A = \frac{A(x - y)}{y}")],
             r"Adding water does not change the amount of acid; the new total is whatever makes that acid \(y\%\).",
             "Water is ADDED to weaken a solution from x% to y%; the amount of water is asked.",
             r"9 litres, \(50\%\to 30\%\): \(\frac{9\times 20}{30} = 6\) litres.", r"Dividing by \(x\) instead of \(y\)."),
    59: card(59, "Water to Remove to Strengthen an Acid",
             r"In \(A\) litres of \(x\%\) acidic liquid, the water to be taken out to make it \(y\%\) acidic (\(y \gt x\)) is \(\frac{A(y - x)}{y}\) litres.",
             r"\[ \text{Water taken out} = \frac{A(y - x)}{y}\text{ litres} \]",
             [("Acid (fixed)", r"\frac{x}{100}A"), ("New total", r"\frac{xA}{y}"), ("Water removed", r"A - \frac{xA}{y} = \frac{A(y - x)}{y}")],
             r"Removing (evaporating) water keeps the acid; the remaining liquid is the amount that makes it \(y\%\).",
             "Water is TAKEN OUT (evaporated) to concentrate a solution from x% to y%.",
             r"15 litres, \(40\%\to 60\%\): \(\frac{15\times 20}{60} = 5\) litres.", r"Dividing by \(x\) instead of \(y\)."),
    60: card(60, "Adding One Part of a Mixture to Change Its Percentage",
             r"When B is added to a mixture of A and B to change the percentage of A, the quantity of B to add is "
             r"\(\frac{\text{Previous \% of A}}{\text{Changed \% of A}}\times\) Mixture \(-\) Mixture.",
             r"\[ \text{B to add} = \frac{\text{Previous \% of A}}{\text{Changed \% of A}}\times M - M \]",
             [("A (fixed)", r"\frac{\text{prev}}{100}M"), ("New mixture", r"\frac{\text{prev}}{\text{new}}M"), ("B added", r"\frac{\text{prev}}{\text{new}}M - M")],
             r"Only B is added, so the amount of A is fixed; the new mixture is the size that makes A the new percentage.",
             "Sand added to sand-and-iron, water added to milk, sand added to sand-and-cement: how much must be added to bring A's share down?",
             r"1 kg, iron \(20\%\to 10\%\): \(\frac{20}{10}\times 1 - 1 = 1\) kg of sand.", r"Forgetting to subtract the original mixture."),
    61: card(61, "Pass Percentage in a Second School",
             r"If \(p\%\) of the students from school A qualified, \(a\%\) more students appeared from school B and \(q\%\) more qualified from B than from A, "
             r"the qualifying percentage of B is \(\frac{p(100 + q)}{100 + a}\%\).",
             r"\[ \text{B's pass \%} = \frac{p(100 + q)}{100 + a} \]",
             [("A appeared, qualified", "100,\ p"), ("B appeared", "100 + a"), ("B qualified", r"p\times\frac{100 + q}{100}")],
             r"Taking 100 students in A turns every percentage into a number of students.",
             "Two schools: A's pass %, how many more appeared and qualified in B; B's pass % is asked.",
             r"\(70\%\), \(20\%\) more appeared, \(50\%\) more qualified: \(\frac{70\times 150}{120} = 87.5\%\).",
             r"Taking the 'more qualified' percentage on B's students instead of on A's qualified students."),
    62: card(62, "Consumption Change from Old and New Prices",
             r"If the price changes from Rs \(X\) to Rs \(Y\), the consumption must change by \(\frac{|Y - X|}{Y}\times 100\%\) to keep the expenditure the same: "
             r"reduced if the price rose, increased if it fell.",
             r"\[ \text{Change in consumption} = \frac{\text{Difference in price}}{\text{New price}}\times 100\% \]",
             [("Expenditure kept", "100X"), ("New consumption", r"\frac{100X}{Y}"), ("Change", r"\frac{|Y - X|}{Y}\times 100")],
             r"The same money buys \(\frac{X}{Y}\) times as much at the new price; the change is measured on the NEW price.",
             "Old and new prices per kg are given; by what % must consumption change to keep the spending the same?",
             r"Rs 21 to Rs 25: \(\frac{4}{25}\times 100 = 16\%\) reduction.",
             r"Dividing by the OLD price (the book itself slips here in two exercises)."),
    63: card(63, "Price Cut in Rupees: Find the Original Price",
             r"If the price falls from Rs \(O\) to Rs \(N\) and the same expenditure \(E\) now buys \(\Delta Q\) more, then \(\Delta Q = \frac{E(O - N)}{N\times O}\).",
             r"\[ \Delta Q = \frac{E(O - N)}{N\times O} \]",
             [("Bought before", r"\frac{E}{O}"), ("Bought after", r"\frac{E}{N}"), ("Extra", r"\frac{E}{N} - \frac{E}{O} = \frac{E(O - N)}{NO}")],
             r"With \(N = O - d\) this becomes a quadratic in \(O\); take the positive root.",
             "'A reduction of Rs d per kg lets a man buy q kg more for Rs E. Find the original price.'",
             r"Rs 2 off, 4 kg more for Rs 16: \(4 = \frac{32}{(O - 2)O}\Rightarrow O = 4\).", r"Taking the negative root, or mixing up \(O\) and \(N\)."),
    64: card(64, "Price Cut in Per Cent: Find the Prices",
             r"If a \(p\%\) price cut lets a buyer get \(\Delta Q\) more for the same expenditure \(E\), the reduced price is \(N = \frac{pE}{100\,\Delta Q}\) and "
             r"the original price is \(O = \frac{100N}{100 - p}\).",
             r"\[ N = \frac{p\times E}{\Delta Q\times 100},\qquad O = \frac{100N}{100 - p} \]",
             [("Money saved", r"\frac{p}{100}E"), ("Saving buys", r"\Delta Q\text{ at } N"), ("Reduced price", r"N = \frac{pE}{100\Delta Q}")],
             r"The money saved by the cut is exactly what pays for the extra quantity at the NEW price.",
             "'A p% reduction in price enables a person to buy q kg more for Rs E. Find the reduced / original price.'",
             r"\(25\%\), 5 kg more for Rs 120: \(N = \frac{25\times 120}{500} = 6\), \(O = \frac{600}{75} = 8\).",
             r"Dividing the saving by the OLD price (the extra is bought at the new price)."),
}

OLD = {
    57: {642: (lambda: maker(25, 20, 28, 48), "The manufacturer of an article makes a profit of 25%, the wholesale dealer makes a profit of 20%, and "
                                              "the retailer makes a profit of 28%. Find the manufacturing price of the article if the retailer sold it for Rs 48.",
               {"a": Rsx(22), "b": Rsx(25), "c": Rsx(30), "d": Rsx(32)})},
    58: {643: (lambda: water(9, 50, 30), "What quantity of water should be added to reduce 9 litres of 50% acidic liquid to 30% acidic liquid?",
               {"a": L(36), "b": L(21), "c": L(6), "d": L(16)})},
    59: {644: (lambda: water(15, 40, 60), "What quantity of water should be taken out to concentrate 15 litres of 40% acidic liquid to 60% acidic liquid?",
               {"a": L(5), "b": L(6), "c": L(21), "d": L(13)})},
    60: {645: (lambda: add_other(1, 20, 10, "iron", "sand"), "In a 1 kg mixture of sand and iron, 20% is iron. How much sand should be added so that "
                                                            "the proportion of iron becomes 10%?", {"a": KG(11), "b": KG(1), "c": KG(18), "d": KG(21)})},
    61: {646: (lambda: schools(70, 30, 50, "P", "Q"),
               "In an examination, 70% of the students who appeared from school P qualified. In school Q, the number of students who appeared is 30% "
               "more than from school P, and the number of students who qualified from school Q is 50% more than from school P. What percentage of "
               "the students who appeared from school Q qualified?", {"a": P(F(1050, 13)), "b": P(F(151, 2)), "c": P(F(121, 2)), "d": P(43)})},
    62: {647: (lambda: two_prices(21, 25), "Wheat is now being sold at Rs 25 per kg. Last month its cost was Rs 21 per kg. By how much per cent should "
                                           "a family reduce its consumption so as to keep the expenditure the same?",
               {"a": P(61), "b": P(21), "c": P(33), "d": P(16)})},
    63: {648: (lambda: cut_by_rupees(2, 4, 16), "A reduction of Rs 2 per kg enables a man to purchase 4 kg more sugar for Rs 16. Find the original price of sugar.",
               {"a": per_kg(14), "b": per_kg(4), "c": per_kg(11), "d": per_kg(7)})},
    64: {649: (lambda: cut_by_percent(25, 5, 120), "A reduction of 25% in the price of tea enables a person to buy 5 kg more for Rs 120. Find the "
                                                   "original price of tea per kg.", {"a": per_kg(8), "b": per_kg(13), "c": per_kg(11), "d": per_kg(18)})},
}

MAKER = ("The manufacturer of an article makes a profit of {}%, the wholesale dealer makes a profit of {}%, and the retailer makes a profit of {}%. "
         "Find the manufacturing price of the article if the retailer sold it for Rs {}.")
ADDW = "What quantity of water should be added to reduce {} litres of {}% acidic liquid to {}% acidic liquid?"
OUTW = "What quantity of water should be taken out to concentrate {} litres of {}% acidic liquid to {}% acidic liquid?"
SCH = ("In an examination, {}% of the students who appeared from school A qualified. In school B, the number of students who appeared is {}% more "
       "than from school A, and the number who qualified from school B is {}% more than from school A. What percentage of the students who "
       "appeared from school B qualified?")
NEW = {
    57: [("r57_e%d" % i, MAKER.format(x, y, z, A), (lambda x=x, y=y, z=z, A=A: maker(x, y, z, A)), [Rsx(o) for o in opts], pos)
         for i, (x, y, z, A, opts, pos) in enumerate([(10, 20, 25, 7920, [5280, 4800, 4400, 5000], 2),
                                                      (25, 20, 10, 66, [44, 36, 40, 45], 3),
                                                      (5, 20, 25, 2205, [1500, 1350, 1250, 1400], 4)], 1)],
    58: [("r58_e%d" % i, ADDW.format(A, x, y), (lambda A=A, x=x, y=y: water(A, x, y)), [L(o) for o in opts], pos)
         for i, (A, x, y, opts, pos) in enumerate([(8, 40, 25, [F(24, 5), 4, 5, 6], 1), (12, 20, 8, [12, 18, 15, 20], 2),
                                                   (30, 15, 10, [12, 10, 15, 20], 3), (20, 30, 24, [6, 4, 8, 5], 4), (8, 60, 15, [24, 32, 20, 18], 1)], 1)],
    59: [("r59_e%d" % i, OUTW.format(A, x, y), (lambda A=A, x=x, y=y: water(A, x, y)), [L(o) for o in opts], pos)
         for i, (A, x, y, opts, pos) in enumerate([(16, 30, 48, [4, 6, 8, 5], 2), (28, 20, 35, [10, 14, 12, 16], 3),
                                                   (30, 18, 24, [6, 8, 9, F(15, 2)], 4), (26, 15, 39, [16, 15, 18, 12], 1)], 1)],
    60: [("r60_e1", "In a 4 kg mixture of water and milk, 25% is milk. How much water should be added so that the proportion of milk becomes 20%?",
          lambda: add_other(4, 25, 20, "milk", "water"), [KG(F(1, 2)), KG(1), KG(2), KG(F(3, 2))], 2),
         ("r60_e2", "In a 6 kg mixture of water and milk, 30% is milk. How much water should be added so that the proportion of milk becomes 20%?",
          lambda: add_other(6, 30, 20, "milk", "water"), [KG(2), KG(4), KG(3), KG(6)], 3),
         ("r60_e3", "In a 40 kg mixture of sand and cement, 36% is cement. How much sand should be added so that the proportion of cement becomes 12%?",
          lambda: add_other(40, 36, 12, "cement", "sand"), [KG(120), KG(100), KG(60), KG(80)], 4)],
    61: [("r61_e%d" % i, SCH.format(p, a, q), (lambda p=p, a=a, q=q: schools(p, a, q)), [P(o) for o in opts], pos)
         for i, (p, a, q, opts, pos) in enumerate([(75, 20, 30, [F(325, 4), 80, F(165, 2), F(315, 4)], 1),
                                                   (60, 40, 50, [64, F(450, 7), F(460, 7), F(440, 7)], 2),
                                                   (70, 25, 35, [75, F(153, 2), F(378, 5), F(364, 5)], 3),
                                                   (50, 20, 44, [64, 72, 50, 60], 4)], 1)],
    62: [("r62_e1", "Rice is now being sold at Rs 20 per kg. Last month its cost was Rs 16 per kg. By how much per cent should a family reduce its "
                    "consumption so as to keep the expenditure the same?", lambda: two_prices(16, 20), [P(25), P(20), P(16), P(4)], 2),
         ("r62_e2", "Tea is now being sold at Rs 36 per kg. Last month its cost was Rs 30 per kg. By how much per cent should a family reduce its "
                    "consumption so as to keep the expenditure the same?", lambda: two_prices(30, 36), [P(20), P(18), P(F(50, 3)), P(6)], 3),
         ("r62_e3", "Sugar is now being sold at Rs 24 per kg. Last month its cost was Rs 30 per kg. By how much per cent should a family increase its "
                    "consumption so as to keep the expenditure the same?", lambda: two_prices(30, 24), [P(20), P(24), P(30), P(25)], 4),
         ("r62_e4", "Wheat is now being sold at Rs 30 per kg. Last month its cost was Rs 36 per kg. By how much per cent should a family increase its "
                    "consumption so as to keep the expenditure the same?", lambda: two_prices(36, 30), [P(20), P(F(50, 3)), P(6), P(18)], 1),
         ("r62_e5", "Tea is now being sold at Rs 50 per kg. Last month its cost was Rs 35 per kg. By how much per cent should a family reduce its "
                    "consumption so as to keep the expenditure the same?", lambda: two_prices(35, 50), [P(F(300, 7)), P(30), P(15), P(35)], 2)],
    63: [("r63_e1", "A reduction of Re 1 per dozen in the price of eggs means that one dozen more eggs can be bought for Rs 56. Find the original "
                    "price of eggs per dozen.", lambda: cut_by_rupees(1, 1, 56, "dozen"), [r"Rs \(7\) per dozen", r"Rs \(9\) per dozen", r"Rs \(8\) per dozen", r"Rs \(6\) per dozen"], 3),
         ("r63_e2", "A reduction of Rs 2 per kg enables a man to purchase 5 kg more tea for Rs 60. Find the original price of tea per kg.",
          lambda: cut_by_rupees(2, 5, 60), [per_kg(4), per_kg(8), per_kg(5), per_kg(6)], 4),
         ("r63_e3", "A reduction of Rs 5 per kg enables a man to purchase 4 kg more rice for Rs 120. Find the original price of rice per kg.",
          lambda: cut_by_rupees(5, 4, 120), [per_kg(15), per_kg(10), per_kg(20), per_kg(12)], 1)],
    64: [("r64_e1", "A reduction of 20% in the price of bananas enables a purchaser to obtain 5 more for a rupee. What are the reduced price and the "
                    "original price of one banana?", lambda: cut_by_percent(20, 5, 1, "both", "banana", "bananas"),
          [r"Re \(\frac{1}{20}\), Re \(\frac{1}{25}\)", r"Re \(\frac{1}{25}\), Re \(\frac{1}{20}\)", r"Re \(\frac{1}{25}\), Re \(\frac{1}{16}\)",
           r"Re \(\frac{1}{30}\), Re \(\frac{1}{25}\)"], 2),
         ("r64_e2", "A reduction of 25% in the price of sugar would enable a purchaser to obtain 5 kg more for Rs 200. What are the reduced price and "
                    "the original price per kg?", lambda: cut_by_percent(25, 5, 200, "both", "kg", "sugar"),
          [r"Rs \(13\frac{1}{3}\), Rs \(10\)", r"Rs \(10\), Rs \(12.50\)", r"Rs \(10\), Rs \(13\frac{1}{3}\)", r"Rs \(8\), Rs \(10\)"], 3),
         ("r64_e3", "A reduction of 20 per cent in the price of lemons would enable a purchaser to obtain 6 more for a rupee. How many lemons did a "
                    "rupee buy before the reduction?", lambda: cut_by_percent(20, 6, 1, "count_before", "lemon", "lemons"),
          [r"\(30\) for a rupee", r"\(18\) for a rupee", r"\(20\) for a rupee", r"\(24\) for a rupee"], 4),
         ("r64_e4", "A reduction of 16% in the price of coffee enables a person to buy 4 kg more for Rs 125. Find the original price of coffee per kg.",
          lambda: cut_by_percent(16, 4, 125, item="coffee"), [r"Rs \(5\frac{20}{21}\) per kg", r"Rs \(5\) per kg", r"Rs \(6\) per kg", r"Rs \(5\frac{1}{21}\) per kg"], 1)],
}


def main():
    for n in range(57, 65):
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
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "percentage", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
