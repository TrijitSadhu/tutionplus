"""Rules 49-56: writes the eight rule cards, regenerates the old rows 637 (Rule 49), 638 (53), 639 (54), 640 (55) and 641 (56)
in the prompt #12 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them and
cleans their text, and adds the book exercises (numbers changed, wording rewritten) plus the worked examples that had no
copy (Rules 49, 50, 51, 52 - the last three had no row at all) as one JsonImport payload per rule. Rule 50's answer
(excess / deficit in an area) is of kind "signed"."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from gen_1_8 import Num, result  # noqa: E402
from gen_17_24 import backward  # noqa: E402
from gen_33_40 import D, PD  # noqa: E402


def kg(v):
    return rf"\({D(v)}\) kg"


# ---------------------------------------------------------------- Rule 49: two candidates, maximum marks
T49 = (r"A candidate scoring \(x\%\) in an examination fails by \(a\) marks, while another candidate who scores \(y\%\) gets \(b\) marks more "
       r"than the minimum pass mark. Then the maximum marks are<br>\[ \frac{100(a + b)}{y - x} \]")


def two_candidates(x, a, y, b, ask="max"):
    x, a, y, b = F(x), F(a), F(y), F(b)
    M = 100 * (a + b) / (y - x)
    pas = x * M / 100 + a
    trad = steps(
        ("Write the pass mark two ways.", rf"Let the maximum marks be \(M\). The first candidate gets \(\frac{{{D(x)}}}{{100}}M\) and is \({D(a)}\) short; "
                                          rf"the second gets \(\frac{{{D(y)}}}{{100}}M\), which is \({D(b)}\) above the pass mark:<br>"
                                          rf"\[ \frac{{{D(x)}}}{{100}}M + {D(a)} = \frac{{{D(y)}}}{{100}}M - {D(b)} \]"),
        ("Solve for M.", rf"\[ \frac{{{D(y - x)}}}{{100}}M = {D(a + b)} \Rightarrow M = {D(M)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(a = {D(a)}\), \(y = {D(y)}\), \(b = {D(b)}\)."),
        ("Apply the specified rule.", r"\[ \text{Maximum marks} = \frac{100(a + b)}{y - x} \]"),
        ("Substitute the values.", rf"\[ \frac{{100({D(a)} + {D(b)})}}{{{D(y)} - {D(x)}}} = \frac{{{D(100 * (a + b))}}}{{{D(y - x)}}} = {D(M)} \]"))
    rb = [rf"\(x = {D(x)}\), \(a = {D(a)}\), \(y = {D(y)}\), \(b = {D(b)}\).", r"Maximum \(= \frac{100(a + b)}{y - x}\).",
          rf"\(\frac{{100\times {D(a + b)}}}{{{D(y - x)}}} = {D(M)}\)."]
    sc = rf"\[ \frac{{100({D(a)} + {D(b)})}}{{{D(y)} - {D(x)}}} = {D(M)} \]"
    if ask == "max":
        return result(("number", M), T49, trad, rule, rf"\({D(M)}\) marks", rb, sc)
    p = pas / M * 100
    last = ("Find the pass percentage.", rf"Pass mark \(= \frac{{{D(x)}}}{{100}}\times {D(M)} + {D(a)} = {D(pas)}\), so<br>"
                                         rf"\[ \frac{{{D(pas)}}}{{{D(M)}}}\times 100 = {D(p)}\% \]")
    trad += "<br><br>" + rf"<b>Step 3: {last[0]}</b><br>{last[1]}"
    rule += "<br><br>" + rf"<b>Step 4: {last[0]}</b><br>{last[1]}"
    rb.append(rf"Pass mark \(= {D(pas)}\), i.e. \({D(p)}\%\).")
    sc = rf"\[ M = {D(M)},\qquad \frac{{{D(pas)}}}{{{D(M)}}}\times 100 = {D(p)}\% \]"
    return result(("number", p), T49, trad, rule, PD(p), rb, sc)


# ---------------------------------------------------------------- Rules 50-52: area of a rectangle
T50 = (r"In measuring the sides of a rectangle, one side is taken \(x\%\) in excess and the other \(y\%\) in deficit. The error per cent in the "
       r"area is<br>\[ \left(x - y - \frac{xy}{100}\right)\% \]in excess or in deficit according as the sign is positive or negative.")
T51 = r"If one side of a rectangle is increased by \(x\%\) and the other by \(y\%\), the area increases by<br>\[ \left(x + y + \frac{xy}{100}\right)\% \]"
T52 = r"If one side of a rectangle is decreased by \(x\%\) and the other by \(y\%\), the area decreases by<br>\[ \left(x + y - \frac{xy}{100}\right)\% \]"


def area(n, x, y):
    """n = 50 (x% excess, y% deficit; signed answer), 51 (both up), 52 (both down)."""
    x, y = F(x), F(y)
    a, b = {50: (100 + x, 100 - y), 51: (100 + x, 100 + y), 52: (100 - x, 100 - y)}[n]
    change = a * b / 100 - 100
    trad = steps(
        ("Take both true sides as 100.", r"The true area is \(100\times 100 = 10000\)."),
        ("Use the measured (or changed) sides.", rf"The sides become \({D(a)}\) and \({D(b)}\), so the area is \({D(a)}\times {D(b)} = {D(a * b)}\)."),
        ("Compare.", rf"\[ \frac{{{D(a * b)} - 10000}}{{10000}}\times 100 = {D(change)}\% \]"))
    if n == 50:
        word = "an excess" if change > 0 else "a deficit"
        rule = steps(
            ("Identify the values.", rf"\(x = {D(x)}\) (excess), \(y = {D(y)}\) (deficit)."),
            ("Apply the specified rule.", r"\[ \left(x - y - \frac{xy}{100}\right)\% \]"),
            ("Substitute the values.", rf"\[ {D(x)} - {D(y)} - \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(x - y)} - {D(x * y / 100)} = {D(change)} \]"
                                       rf"The sign is {'positive' if change > 0 else 'negative'}, so the error is {word[2:] if word.startswith('a ') else word[3:]}."))
        fin = rf"{word} of \({D(abs(change))}\%\)"
        calc = rf"{D(x)} - {D(y)} - \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(change)}"
        rb = [rf"\(x = {D(x)}\) (excess), \(y = {D(y)}\) (deficit).", r"Error \(= x - y - \frac{xy}{100}\).", rf"\({calc}\), {word}."]
        return result(("signed", change), T50, trad, rule, fin, rb, rf"\[ {calc}\% \]")
    s = "+" if n == 51 else "-"
    v = abs(change)
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\)."),
        ("Apply the specified rule.", rf"\[ \left(x + y {s} \frac{{xy}}{{100}}\right)\% \]"),
        ("Substitute the values.", rf"\[ {D(x)} + {D(y)} {s} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(x + y)} {s} {D(x * y / 100)} = {D(v)}\% \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\).", rf"Change \(= x + y {s} \frac{{xy}}{{100}}\).", rf"\({D(x)} + {D(y)} {s} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(v)}\%\)."]
    sc = rf"\[ {D(x)} + {D(y)} {s} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(v)}\% \]"
    return result(("number", v), T51 if n == 51 else T52, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- Rule 53: failed in English, Maths, both
T53 = r"In an examination \(x\%\) failed in English, \(y\%\) failed in Maths and \(z\%\) failed in both. The percentage who passed in both subjects is<br>\[ 100 - (x + y - z) \]"


def passed_both(m, e, b):
    m, e, b = F(m), F(e), F(b)
    v = 100 - (m + e - b)
    trad = steps(
        ("Split the students who failed.", rf"Failed in Maths only \(= {D(m)} - {D(b)} = {D(m - b)}\%\), failed in English only \(= {D(e)} - {D(b)} = {D(e - b)}\%\), "
                                           rf"failed in both \(= {D(b)}\%\)."),
        ("Add the parts that failed.", rf"\[ {D(m - b)} + {D(e - b)} + {D(b)} = {D(m + e - b)}\% \]"),
        ("The rest passed in both.", rf"\[ 100 - {D(m + e - b)} = {D(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"English \(x = {D(e)}\), Maths \(y = {D(m)}\), both \(z = {D(b)}\)."),
        ("Apply the specified rule.", r"\[ 100 - (x + y - z) \]"),
        ("Substitute the values.", rf"\[ 100 - ({D(e)} + {D(m)} - {D(b)}) = 100 - {D(m + e - b)} = {D(v)}\% \]"))
    rb = [rf"\(x = {D(e)}\), \(y = {D(m)}\), \(z = {D(b)}\).", r"Passed in both \(= 100 - (x + y - z)\).", rf"\(100 - {D(m + e - b)} = {D(v)}\%\)."]
    sc = rf"\[ 100 - ({D(e)} + {D(m)} - {D(b)}) = {D(v)}\% \]"
    return result(("number", v), T53, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- Rule 54: savings
T54 = (r"A man spends \(x\%\) of his income. If his income increases by \(y\%\) and his expenditure by \(z\%\), his savings increase by<br>"
       r"\[ \frac{100y - xz}{100 - x}\% \]")


def savings(x, y, z):
    x, y, z = F(x), F(y), F(z)
    v = (100 * y - x * z) / (100 - x)
    ni, ne = 100 + y, x + x * z / 100
    trad = steps(
        ("Take the income as 100.", rf"He spends \({D(x)}\) and saves \(100 - {D(x)} = {D(100 - x)}\)."),
        ("Apply the changes.", rf"New income \(= {D(ni)}\), new expenditure \(= {D(x)} + \frac{{{D(z)}}}{{100}}\times {D(x)} = {D(ne)}\), new savings \(= {D(ni)} - {D(ne)} = {D(ni - ne)}\)."),
        ("Find the increase in savings.", rf"\[ \frac{{{D(ni - ne)} - {D(100 - x)}}}{{{D(100 - x)}}}\times 100 = {D(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\)."),
        ("Apply the specified rule.", r"\[ \frac{100y - xz}{100 - x}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{100\times {D(y)} - {D(x)}\times {D(z)}}}{{100 - {D(x)}}} = \frac{{{D(100 * y - x * z)}}}{{{D(100 - x)}}} = {D(v)}\% \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\).", r"Increase in savings \(= \frac{100y - xz}{100 - x}\%\).",
          rf"\(\frac{{{D(100 * y - x * z)}}}{{{D(100 - x)}}} = {D(v)}\%\)."]
    sc = rf"\[ \frac{{100\times {D(y)} - {D(x)}\times {D(z)}}}{{100 - {D(x)}}} = {D(v)}\% \]"
    return result(("number", v), T54, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- Rule 55: salt solution
T55 = (r"A solution of salt and water contains \(x\%\) salt by weight. If \(A\) kg of water evaporates and the solution then contains \(y\%\) salt, "
       r"the original quantity of solution is<br>\[ A\left(\frac{y}{y - x}\right)\text{ kg} \]")


def salt(x, A, y):
    x, A, y = F(x), F(A), F(y)
    S = A * y / (y - x)
    trad = steps(
        ("The salt does not change.", rf"Let the solution weigh \(S\) kg. Salt \(= \frac{{{D(x)}}}{{100}}S\). After \({D(A)}\) kg of water goes, the solution is "
                                      rf"\(S - {D(A)}\) kg with the same salt, now \({D(y)}\%\):<br>\[ \frac{{{D(x)}}}{{100}}S = \frac{{{D(y)}}}{{100}}(S - {D(A)}) \]"),
        ("Solve.", rf"\[ {D(x)}S = {D(y)}S - {D(y * A)} \Rightarrow {D(y - x)}S = {D(y * A)} \Rightarrow S = {D(S)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(A = {D(A)}\) kg."),
        ("Apply the specified rule.", r"\[ A\left(\frac{y}{y - x}\right) \]"),
        ("Substitute the values.", rf"\[ {D(A)}\times \frac{{{D(y)}}}{{{D(y)} - {D(x)}}} = {D(A)}\times \frac{{{D(y)}}}{{{D(y - x)}}} = {D(S)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(A = {D(A)}\).", r"Original \(= A\left(\frac{y}{y - x}\right)\).", rf"\({D(A)}\times\frac{{{D(y)}}}{{{D(y - x)}}} = {D(S)}\) kg."]
    sc = rf"\[ {D(A)}\times \frac{{{D(y)}}}{{{D(y)} - {D(x)}}} = {D(S)}\text{{ kg}} \]"
    return result(("number", S), T55, trad, rule, kg(S), rb, sc)


# ---------------------------------------------------------------- Rule 56: of the remaining -> total
T56 = (r"If \(x\%\) of a thing is of one type, \(y\%\) of the remaining is of a second type, \(z\%\) of the remaining is of a third type and the "
       r"rest, \(A\), is left, then the total is<br>\[ A\left(\frac{100}{100 - x}\right)\left(\frac{100}{100 - y}\right)\left(\frac{100}{100 - z}\right) \]")


def library(x, y, z, A):
    return backward(A, [x, y, z], "-", T56, Num, "the total number of books")


# ---------------------------------------------------------------- rule cards
CARDS = {
    49: card(49, "Maximum Marks from Two Candidates",
             r"A candidate scoring \(x\%\) fails by \(a\) marks, while another scoring \(y\%\) gets \(b\) marks more than the pass mark. Then the "
             r"maximum marks are \(\frac{100(a + b)}{y - x}\).",
             r"\[ \text{Maximum marks} = \frac{100(a + b)}{y - x} = \frac{100\times\text{Difference of their scores}}{\text{Difference of their \%}} \]",
             [("First candidate", r"x\%\text{ of } M = \text{pass} - a"), ("Second candidate", r"y\%\text{ of } M = \text{pass} + b"),
              ("Difference", r"(y - x)\%\text{ of } M = a + b")],
             r"The two candidates' scores differ by \(a + b\) marks, and that difference is \((y - x)\%\) of the maximum - Rule 4 again.",
             "Two candidates, one below and one above the pass mark; their percentages and marks short / above are given. Also: then find the pass percentage.",
             r"\(25\%\) fails by 30, \(50\%\) is 20 above: \(\frac{100\times 50}{25} = 200\).",
             r"Using \(a - b\) instead of \(a + b\) (one is BELOW and the other ABOVE the pass mark)."),
    50: card(50, "Measurement Error in the Area of a Rectangle",
             r"If one side is measured \(x\%\) in excess and the other \(y\%\) in deficit, the error in the area is \(\left(x - y - \frac{xy}{100}\right)\%\): "
             r"in excess if positive, in deficit if negative.",
             r"\[ \text{Error in area} = \left(x - y - \frac{xy}{100}\right)\% \]",
             [("True sides", "100, 100"), ("Measured sides", "100 + x,\ 100 - y"), ("Measured area", r"10000 + 100(x - y) - xy")],
             r"Area \(=\) Length \(\times\) Breadth, so the two errors combine like an increase and a decrease of a product (Rule 42).",
             "One side measured too long by x%, the other too short by y%: error per cent in the calculated area, in excess or deficit.",
             r"\(5\%\) excess, \(4\%\) deficit: \(5 - 4 - 0.2 = 0.8\%\) excess.",
             r"Answering \(x - y\), or calling a negative result an excess."),
    51: card(51, "Area of a Rectangle: Both Sides Increased",
             r"If one side of a rectangle is increased by \(x\%\) and the other by \(y\%\), the area increases by \(\left(x + y + \frac{xy}{100}\right)\%\).",
             r"\[ \text{Increase in area} = \left(x + y + \frac{xy}{100}\right)\% \]",
             [("Sides", "100, 100"), ("New sides", "100 + x,\ 100 + y"), ("New area", r"10000 + 100(x + y) + xy")],
             r"The extra strip \(\frac{xy}{100}\) is the corner piece where both increases overlap.",
             "Both sides of a rectangle (or both factors of a product) increase; the % change in area is asked.",
             r"\(20\%\) and \(5\%\): \(25 + 1 = 26\%\).", r"Adding \(x + y\) only."),
    52: card(52, "Area of a Rectangle: Both Sides Decreased",
             r"If one side of a rectangle is decreased by \(x\%\) and the other by \(y\%\), the area decreases by \(\left(x + y - \frac{xy}{100}\right)\%\).",
             r"\[ \text{Decrease in area} = \left(x + y - \frac{xy}{100}\right)\% \]",
             [("Sides", "100, 100"), ("New sides", "100 - x,\ 100 - y"), ("New area", r"10000 - 100(x + y) + xy")],
             r"The corner piece \(\frac{xy}{100}\) would be taken off twice, so it is added back.",
             "Both sides of a rectangle are measured short (or both decrease); the % error or decrease in area is asked.",
             r"\(5\%\) and \(4\%\) short: \(9 - 0.2 = 8.8\%\).", r"Adding \(x + y\) only."),
    53: card(53, "Passed in Both Subjects",
             r"If \(x\%\) failed in English, \(y\%\) failed in Maths and \(z\%\) failed in both, the percentage who passed in both is \(100 - (x + y - z)\).",
             r"\[ \text{Passed in both} = 100 - (x + y - z) \]",
             [("Failed in English only", "x - z"), ("Failed in Maths only", "y - z"), ("Failed in both", "z"), ("Passed in both", "100 - (x + y - z)")],
             r"Students failing in both are counted in \(x\) AND in \(y\), so \(z\) is subtracted once to count each failing student once.",
             "Percentages failing in each of two subjects and in both are given; the % passing in both is asked.",
             r"\(40\%\), \(30\%\), both \(10\%\): \(100 - 60 = 40\%\).", r"Answering \(100 - (x + y)\) and forgetting the students counted twice."),
    54: card(54, "Change in Savings",
             r"A man spends \(x\%\) of his income. If his income increases by \(y\%\) and his expenditure by \(z\%\), his savings increase by \(\frac{100y - xz}{100 - x}\%\).",
             r"\[ \text{Increase in savings} = \frac{100y - xz}{100 - x}\% \]",
             [("Income", r"100 \to 100 + y"), ("Expenditure", r"x \to x + \frac{xz}{100}"), ("Savings", r"100 - x \to 100 + y - x - \frac{xz}{100}")],
             r"Savings \(=\) Income \(-\) Expenditure: the increase \(y - \frac{xz}{100}\) is measured on the old savings \(100 - x\).",
             "Income and expenditure both rise by given percentages; the % change in savings is asked.",
             r"Spends \(75\%\), income \(+20\%\), spending \(+10\%\): \(\frac{2000 - 750}{25} = 50\%\).",
             r"Measuring the change in savings on the income (100) instead of on the old savings."),
    55: card(55, "Salt Solution after Evaporation",
             r"A solution contains \(x\%\) salt. After \(A\) kg of water evaporates it contains \(y\%\) salt. The original quantity is \(A\left(\frac{y}{y - x}\right)\) kg.",
             r"\[ \text{Original quantity} = A\left(\frac{y}{y - x}\right)\text{ kg} \]",
             [("Salt (unchanged)", r"\frac{x}{100}S"), ("After evaporation", r"\frac{y}{100}(S - A)"), ("Equal", r"xS = y(S - A)")],
             r"Only water leaves, so the amount of salt is the same before and after; equate it.",
             "A solution loses water by evaporation and its salt (acid, sugar) percentage rises; the original quantity is asked.",
             r"\(15\%\to 20\%\) after 30 kg: \(30\times\frac{20}{5} = 120\) kg.", r"Dividing by \(x\) or \(y\) alone instead of by \(y - x\)."),
    56: card(56, "Total from Shares of the Remaining",
             r"If \(x\%\) of a thing is of one type, \(y\%\) of the remaining of a second type, \(z\%\) of the remaining of a third type, and \(A\) are left, "
             r"the total is \(A\left(\frac{100}{100 - x}\right)\left(\frac{100}{100 - y}\right)\left(\frac{100}{100 - z}\right)\).",
             r"\[ \text{Total} = A\left(\frac{100}{100 - x}\right)\left(\frac{100}{100 - y}\right)\left(\frac{100}{100 - z}\right) \]",
             [("After the first type", r"\frac{100 - x}{100}\text{ left}"), ("After the second", r"\frac{100 - y}{100}\text{ of that}"),
              ("Left at the end", "A")],
             r"Each step keeps a fraction of what was left, so divide the final amount by every one of those fractions (same as Rule 17).",
             "Books (students, money) split step by step 'of the remaining'; the number left is given and the total is asked.",
             r"\(20\%\), \(50\%\), \(30\%\), 6300 left: \(6300\times\frac{100}{80}\times\frac{100}{50}\times\frac{100}{70} = 22500\).",
             r"Taking every percentage of the TOTAL instead of 'of the remaining'."),
}

OLD = {
    49: {637: (lambda: two_candidates(25, 45, 50, 5), "A candidate scores 25% and fails by 45 marks, while another candidate who scores 50% gets 5 marks "
                                                      "more than the minimum required to pass the examination. Find the maximum marks for the examination.", None)},
    53: {638: (lambda: passed_both(40, 30, 10), "In an examination, 40% of the students failed in Mathematics, 30% failed in English and 10% failed in "
                                                "both. Find the percentage of students who passed in both the subjects.", None)},
    54: {639: (lambda: savings(75, 20, 10), "A man spends 75% of his income. His income increases by 20% and his expenditure also increases by 10%. "
                                            "Find the percentage increase in his savings.", None)},
    55: {640: (lambda: salt(15, 30, 20), "A solution of salt and water contains 15% salt by weight. Of it 30 kg of water evaporates and the solution "
                                         "now contains 20% of salt. Find the original quantity of the solution.", None)},
    56: {641: (lambda: library(20, 50, 30, 6300), "In a library, 20% of the books are in Hindi, 50% of the remaining are in English and 30% of the "
                                                  "remaining are in French. The remaining 6300 books are in regional languages. What is the total number "
                                                  "of books in the library?", None)},
}
for n in (50, 51, 52):
    OLD[n] = {}


def sg(pairs):
    return [rf"\({D(v)}\%\) {w}" for w, v in pairs]


TWO = "A candidate scores {}% and fails by {} marks, while another candidate who scores {}% gets {} marks more than the minimum required to pass. "
NEW = {
    49: [("r49_ex", TWO.format(30, 24, 45, 21) + "Find the maximum marks for the examination.", lambda: two_candidates(30, 24, 45, 21),
          [Num(250), Num(300), Num(350), Num(450)], 2),
         ("r49_e1", TWO.format(30, 42, 55, 28) + "Find the maximum marks for the examination.", lambda: two_candidates(30, 42, 55, 28),
          [Num(280), Num(300), Num(250), Num(320)], 1),
         ("r49_e2", TWO.format(40, 36, 64, 24) + "Find the maximum marks for the examination.", lambda: two_candidates(40, 36, 64, 24),
          [Num(200), Num(300), Num(250), Num(240)], 3),
         ("r49_e3", TWO.format(28, 57, 40, 33) + "Find the maximum marks for the examination.", lambda: two_candidates(28, 57, 40, 33),
          [Num(850), Num(700), Num(900), Num(750)], 4),
         ("r49_e4", TWO.format(42, 52, 57, 38) + "Find the maximum marks for the examination.", lambda: two_candidates(42, 52, 57, 38),
          [Num(500), Num(600), Num(650), Num(550)], 2),
         ("r49_e6", TWO.format(20, 36, 40, 24) + "Find the minimum pass percentage.", lambda: two_candidates(20, 36, 40, 24, "pass"),
          [PD(30), PD(36), PD(32), PD(40)], 3)],
    50: [("r50_e%d" % i, f"In measuring the sides of a rectangle, one side is taken {x}% in excess and the other {y}% in deficit. Find the error "
                          "per cent in the area calculated from the measurement.", (lambda x=x, y=y: area(50, x, y)), sg(opts), pos)
         for i, (x, y, opts, pos) in enumerate([
             (6, 5, [("excess", F(7, 10)), ("deficit", F(7, 10)), ("excess", F(13, 10)), ("excess", 1)], 1),
             (4, 6, [("deficit", 2), ("deficit", F(56, 25)), ("excess", F(56, 25)), ("deficit", F(44, 25))], 2),
             (15, 5, [("excess", 10), ("excess", F(43, 4)), ("excess", F(37, 4)), ("deficit", F(37, 4))], 3),
             (8, 2, [("excess", 6), ("excess", F(154, 25)), ("deficit", F(146, 25)), ("excess", F(146, 25))], 4),
             (20, 30, [("deficit", 16), ("deficit", 10), ("excess", 16), ("deficit", 4)], 1)])],
    51: [("r51_e%d" % i, f"If one side of a rectangle is increased by {x}% and the other by {y}%, find the per cent value by which the area changes.",
          (lambda x=x, y=y: area(51, x, y)), [PD(o) for o in opts], pos)
         for i, (x, y, opts, pos) in enumerate([
             (10, 5, [15, F(31, 2), F(33, 2), F(301, 20)], 2),
             (30, 10, [40, 44, 43, 33], 3),
             (20, 15, [35, 38, 40, 37], 2),
             (12, 3, [15, F(381, 25), F(384, 25), F(386, 25)], 3),
             (35, 20, [62, 55, 60, 70], 1),
             (40, 25, [65, 70, 72, 75], 4)])],
    52: [("r52_e%d" % i, f"In measuring the sides of a rectangle, one side is taken {x}% in deficit and the other {y}% in deficit. Find the error "
                          "per cent in the area calculated from the measurement.", (lambda x=x, y=y: area(52, x, y)), [PD(o) for o in opts], pos)
         for i, (x, y, opts, pos) in enumerate([
             (6, 5, [11, F(107, 10), F(113, 10), F(103, 10)], 2),
             (4, 3, [F(172, 25), 7, F(178, 25), F(163, 25)], 1),
             (20, 5, [25, 23, 24, 26], 3),
             (25, 8, [33, 35, F(67, 2), 31], 4),
             (12, 10, [22, F(104, 5), F(116, 5), F(101, 5)], 2)])],
    53: [("r53_e%d" % i, f"In an examination, {m}% of the students failed in Mathematics, {e}% failed in English and {b}% failed in both. Find the "
                          "percentage of students who passed in both the subjects.", (lambda m=m, e=e, b=b: passed_both(m, e, b)), [PD(o) for o in opts], pos)
         for i, (m, e, b, opts, pos) in enumerate([
             (15, 25, 10, [70, 60, 75, 80], 1),
             (35, 20, 15, [45, 60, 55, 70], 2),
             (37, 28, 15, [35, 65, 50, 40], 3),
             (52, 33, 25, [15, 60, 30, 40], 4),
             (38, 27, 12, [47, 35, 53, 41], 1),
             (55, 35, 20, [10, 30, 20, 40], 2)], 1)]
        + [("r53_e7", "In an examination, 48% of the candidates failed in English, 36% failed in Mathematics and 12% failed in both. What percentage "
                      "of the candidates passed in both the subjects?", lambda: passed_both(36, 48, 12), [PD(16), PD(40), PD(28), PD(24)], 3)],
    54: [("r54_e%d" % i, f"A man spends {x}% of his income. His income increases by {y}% and his expenditure also increases by {z}%. Find the "
                          "percentage increase in his savings.", (lambda x=x, y=y, z=z: savings(x, y, z)), [PD(o) for o in opts], pos)
         for i, (x, y, z, opts, pos) in enumerate([
             (60, 20, 10, [30, 35, 20, 40], 2),
             (75, 16, 12, [16, 25, 28, 32], 3),
             (40, 25, 10, [25, 40, 30, 35], 4),
             (90, 30, 20, [120, 30, 100, 150], 1),
             (65, 20, 18, [F(159, 7), F(166, 7), 24, F(162, 7)], 2)], 1)],
    55: [("r55_e%d" % i, f"A solution of salt and water contains {x}% salt by weight. Of it {A} kg of water evaporates and the solution now contains "
                          f"{y}% of salt. Find the original quantity of the solution.", (lambda x=x, A=A, y=y: salt(x, A, y)), [kg(o) for o in opts], pos)
         for i, (x, A, y, opts, pos) in enumerate([
             (4, 24, 12, [32, 48, 36, 30], 3),
             (10, 30, 16, [75, 90, 96, 80], 4),
             (19, 23, 29, [F(667, 10), F(697, 10), F(617, 10), F(767, 10)], 1),
             (9, 36, 15, [80, 90, 100, 60], 2),
             (15, 27, 24, [63, 81, 72, 64], 3)], 1)],
    56: [("r56_e%d" % i, f"In a library, {x}% of the books are in Hindi, {y}% of the remaining are in English and {z}% of the remaining are in "
                          f"French. The remaining {A} books are in regional languages. What is the total number of books in the library?",
          (lambda x=x, y=y, z=z, A=A: library(x, y, z, A)), [Num(o) for o in opts], pos)
         for i, (x, y, z, A, opts, pos) in enumerate([
             (5, 20, 10, 6840, [9000, 10000, 12000, 11000], 2),
             (10, 20, 25, 16200, [27000, 32400, 30000, 25000], 3),
             (25, 20, 40, 18000, [45000, 54000, 60000, 50000], 4),
             (15, 40, 50, 3060, [12000, 12500, 10000, 15000], 1),
             (4, 75, 20, 3000, [16525, 15625, 15000, 12500], 2)], 1)],
}


def main():
    for n in range(49, 57):
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
