"""Rules 33-40: writes the eight rule cards, regenerates the old worked-example rows 621-628 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their options
(display math, missing % signs, 624/625 now say increase or decrease; 625 had no option holding 4.5%), and adds the book
exercises (numbers changed, wording rewritten) plus the worked examples of Rules 36 and 37 that had no copy, as one
JsonImport payload per rule. Answers that are a change with a direction are of kind "signed" (validate.py)."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import P, pnum, result  # noqa: E402


def D(v):
    """Exact decimals as decimals (1.44, 4.5, 26.5), anything else as a mixed number (33\\frac{1}{3})."""
    v = F(v)
    if (v * 100).denominator == 1 and v.denominator != 1:
        return f"{float(v):.2f}".rstrip("0").rstrip(".")
    return tex(v)


def PD(v):
    return rf"\({D(v)}\%\)"


def change(word, v):
    """'Decrease of 1%' style option / answer."""
    return rf"{word} of \({D(v)}\%\)"


# ---------------------------------------------------------------- Rules 33-35: one change seen from the other side
T33 = (r"If the price of a commodity decreases by \(r\%\), then the increase in consumption, so as not to decrease the expenditure on it, is<br>"
       r"\[ \frac{r}{100 - r}\times 100\% \]")
T34 = r"If the first value is \(r\%\) more than the second value, then the second is<br>\[ \frac{r}{100 + r}\times 100\%\text{ less than the first.} \]"
T35 = r"If the first value is \(r\%\) less than the second value, then the second is<br>\[ \frac{r}{100 - r}\times 100\%\text{ more than the first.} \]"


def other_side(n, r, restore=False):
    """n = 33 (price falls -> consumption up; restore=True: price cut -> rise needed to restore it), 34 (more -> less), 35 (less -> more)."""
    r = F(r)
    s = "+" if n == 34 else "-"
    base = 100 + r if n == 34 else 100 - r
    v = r / base * 100
    T = {33: T33, 34: T34, 35: T35}[n]
    if n == 33 and not restore:
        c = 10000 / base
        trad = steps(
            ("Take easy starting values.", r"Let the price be \(100\) and the consumption \(100\) units, so the expenditure is \(100\times 100 = 10000\)."),
            ("Find the consumption that keeps the expenditure the same.", rf"The new price is \({pnum(base)}\), so the consumption must be<br>"
                                                                           rf"\[ \frac{{10000}}{{{pnum(base)}}} = {tex(c)} \]"),
            ("Find the increase.", rf"\[ {tex(c)} - 100 = {tex(v)}\text{{ units out of 100, i.e. }} {tex(v)}\% \]"))
    elif n == 33:
        trad = steps(
            ("Take the old price as 100.", rf"After the cut of \({pnum(r)}\%\) the price is \({pnum(base)}\)."),
            ("Find the rise needed.", rf"To get back to \(100\) the price must go up by \({pnum(r)}\) on \({pnum(base)}\):<br>"
                                      rf"\[ \frac{{{pnum(r)}}}{{{pnum(base)}}}\times 100 = {tex(v)}\% \]"))
    else:
        first, second = ("first", "second")
        trad = steps(
            ("Take the second value as 100.", rf"The first value is \(100 {s} {pnum(r)} = {pnum(base)}\)."),
            ("Compare the second with the first.", rf"The difference is \({pnum(r)}\), and it is now measured on the first value \({pnum(base)}\):<br>"
                                                   rf"\[ \frac{{{pnum(r)}}}{{{pnum(base)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the value.", rf"\(r = {pnum(r)}\)."),
        ("Apply the specified rule.", rf"\[ \frac{{r}}{{100 {s} r}}\times 100\% \]"),
        ("Substitute the value.", rf"\[ \frac{{{pnum(r)}}}{{100 {s} {pnum(r)}}}\times 100 = \frac{{{pnum(r)}\times 100}}{{{pnum(base)}}} = {tex(v)}\% \]"))
    rb = [rf"\(r = {pnum(r)}\).", rf"Answer \(= \frac{{r}}{{100 {s} r}}\times 100\%\).", rf"\(\frac{{{pnum(r)}}}{{{pnum(base)}}}\times 100 = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{pnum(r)}}}{{100 {s} {pnum(r)}}}\times 100 = {tex(v)}\% \]"
    return result(("number", v), T, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rules 36 and 37: an increase and a decrease
T36 = (r"If a value is first increased by \(x\%\) and then decreased by \(x\%\) (or the other way round), the net change is always a decrease "
       r"equal to<br>\[ \frac{x^2}{100}\% \]")
T37 = (r"If a value is first increased by \(x\%\) and then decreased by \(y\%\) (in either order), the net change is<br>"
       r"\[ \left(x - y - \frac{xy}{100}\right)\% \]an increase if the sign is positive and a decrease if it is negative.")
WORDS = {"salary": ("an increase", "a decrease", "Increase", "Decrease"), "population": ("an increase", "a decrease", "Increase", "Decrease"),
         "price": ("a profit", "a loss", "Profit", "Loss")}


def up_down(x, y, ctx, down_first=False):
    """x = the increase, y = the decrease; ctx = 'salary', 'population' or 'price' (mark-up then discount: profit / loss)."""
    x, y = F(x), F(y)
    net = x - y - x * y / 100
    same = x == y
    T = T36 if same else T37
    order = [(-1, y), (1, x)] if down_first else [(1, x), (-1, y)]
    cur, rows = F(100), []
    for s, p in order:
        ch = cur * p / 100
        new = cur + s * ch
        rows.append(rf"{'up' if s > 0 else 'down'} \({D(p)}\%\): \({D(cur)} {'+' if s > 0 else '-'} \frac{{{D(p)}}}{{100}}\times {D(cur)} = "
                    rf"{D(cur)} {'+' if s > 0 else '-'} {D(ch)} = {D(new)}\)")
        cur = new
    up_w, down_w, Up, Down = WORDS[ctx]
    word = up_w if net > 0 else down_w
    trad = steps(("Start from 100.", "<br>".join(rows)),
                 ("Compare with 100.", rf"\[ {D(cur)} - 100 = {D(net)} \]So there is {word} of \({D(abs(net))}\%\)."))
    if same:
        rule = steps(
            ("Identify the value.", rf"The same \(x = {D(x)}\) is added and taken away."),
            ("Apply the specified rule.", r"\[ \text{Decrease} = \frac{x^2}{100}\% \]"),
            ("Substitute the value.", rf"\[ \frac{{{D(x)}^2}}{{100}} = \frac{{{D(x * x)}}}{{100}} = {D(-net)}\% \]"))
        rb = [rf"\(x = {D(x)}\).", r"Decrease \(= \frac{x^2}{100}\%\).", rf"\(\frac{{{D(x)}^2}}{{100}} = {D(-net)}\%\), {down_w}."]
        sc = rf"\[ \frac{{{D(x)}^2}}{{100}} = {D(-net)}\%\text{{ ({down_w[2:]})}} \]"
    else:
        rule = steps(
            ("Identify the values.", rf"Increase \(x = {D(x)}\), decrease \(y = {D(y)}\) (the order does not matter)."),
            ("Apply the specified rule.", r"\[ \left(x - y - \frac{xy}{100}\right)\% \]"),
            ("Substitute the values.", rf"\[ {D(x)} - {D(y)} - \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(x - y)} - {D(x * y / 100)} = {D(net)} \]"
                                       rf"The sign is {'positive' if net > 0 else 'negative'}, so it is {word}."))
        rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\).", r"Effect \(= x - y - \frac{xy}{100}\).",
              rf"\({D(x)} - {D(y)} - \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(net)}\), {word}."]
        sc = rf"\[ {D(x)} - {D(y)} - \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(net)}\%\text{{ ({word[2:] if word.startswith('a ') else word[3:]})}} \]"
    fin = rf"{word} of \({D(abs(net))}\%\)"
    return result(("signed", net), T, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rules 38-40: two successive changes in the same direction
T38 = r"If a value is increased successively by \(x\%\) and \(x\%\), the final increase is<br>\[ \left(2x + \frac{x^2}{100}\right)\% \]"
T39 = r"If a value is increased successively by \(x\%\) and \(y\%\), the final increase is<br>\[ \left(x + y + \frac{xy}{100}\right)\% \]"
T40 = r"If a value is decreased successively by \(x\%\) and \(y\%\), the final decrease is<br>\[ \left(x + y - \frac{xy}{100}\right)\% \]"


def successive(n, x, y=None):
    x = F(x)
    y = x if y is None else F(y)
    s = -1 if n == 40 else 1
    v = x + y + s * x * y / 100
    cur, rows = F(100), []
    for p in (x, y):
        ch = cur * p / 100
        new = cur + s * ch
        rows.append(rf"\({D(p)}\%\) of \({D(cur)}\) is \({D(ch)}\): \({D(cur)} {'+' if s > 0 else '-'} {D(ch)} = {D(new)}\)")
        cur = new
    trad = steps(("Start from 100.", "<br>".join(rows)),
                 ("Compare with 100.", rf"\[ {'%s - 100' % D(cur) if s > 0 else '100 - %s' % D(cur)} = {D(v)} \]"
                                       rf"So the total {'increase' if s > 0 else 'decrease'} is \({D(v)}\%\)."))
    sg = "+" if s > 0 else "-"
    if n == 38:
        rule = steps(
            ("Identify the value.", rf"\(x = {D(x)}\), applied twice."),
            ("Apply the specified rule.", r"\[ \left(2x + \frac{x^2}{100}\right)\% \]"),
            ("Substitute the value.", rf"\[ 2\times {D(x)} + \frac{{{D(x)}^2}}{{100}} = {D(2 * x)} + {D(x * x / 100)} = {D(v)}\% \]"))
        rb = [rf"\(x = {D(x)}\).", r"Increase \(= 2x + \frac{x^2}{100}\).", rf"\(2\times {D(x)} + \frac{{{D(x)}^2}}{{100}} = {D(v)}\%\)."]
        sc = rf"\[ 2\times {D(x)} + \frac{{{D(x)}^2}}{{100}} = {D(v)}\% \]"
    else:
        rule = steps(
            ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\)."),
            ("Apply the specified rule.", rf"\[ \left(x + y {sg} \frac{{xy}}{{100}}\right)\% \]"),
            ("Substitute the values.", rf"\[ {D(x)} + {D(y)} {sg} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(x + y)} {sg} {D(x * y / 100)} = {D(v)}\% \]"))
        rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\).", rf"Total \(= x + y {sg} \frac{{xy}}{{100}}\).",
              rf"\({D(x)} + {D(y)} {sg} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(v)}\%\)."]
        sc = rf"\[ {D(x)} + {D(y)} {sg} \frac{{{D(x)}\times {D(y)}}}{{100}} = {D(v)}\% \]"
    return result(("number", v), {38: T38, 39: T39, 40: T40}[n], trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    33: card(33, "Price Fall: Extra Consumption to Keep Expenditure the Same",
             r"If the price of a commodity decreases by \(r\%\), the consumption must increase by \(\frac{r}{100 - r}\times 100\%\) so that the "
             r"expenditure does not decrease. The same number answers 'by what per cent must the reduced price rise to get back to the old price?'",
             r"\[ \text{Increase in consumption} = \frac{r}{100 - r}\times 100\% \]",
             [("Price", r"100 \to 100 - r"), ("Expenditure kept", r"100\times 100"), ("New consumption", r"\frac{10000}{100 - r}")],
             r"Expenditure \(=\) Price \(\times\) Consumption: when the price becomes \(\frac{100 - r}{100}\) of itself, the consumption must become "
             r"\(\frac{100}{100 - r}\) times as much.",
             "The price of an item falls by r%; by how much per cent can (must) the consumption rise so the spending stays the same? Also: a price is cut by r%, by what per cent must it rise to come back?",
             r"Price down \(10\%\): \(\frac{10}{90}\times 100 = 11\frac{1}{9}\%\).",
             r"Answering \(r\%\): after a \(10\%\) fall, a \(10\%\) rise on the LOWER price does not get back to the start."),
    34: card(34, "r% More, Seen from the Other Side",
             r"If the first value is \(r\%\) more than the second value, then the second is \(\frac{r}{100 + r}\times 100\%\) less than the first.",
             r"\[ \text{Second is } \frac{r}{100 + r}\times 100\%\text{ less than the first} \]",
             [("Second value", "100"), ("First value", "100 + r"), ("Gap measured on the first", r"\frac{r}{100 + r}\times 100")],
             r"The gap is the same \(r\), but 'less than the first' measures it on the bigger value \(100 + r\).",
             "'A is r% more than B. By how much per cent is B less than A?' (salaries, prices, two numbers).",
             r"A is \(25\%\) more than B: B is \(\frac{25}{125}\times 100 = 20\%\) less than A.",
             r"Answering \(r\%\) again - the base has changed from B to A."),
    35: card(35, "r% Less, Seen from the Other Side",
             r"If the first value is \(r\%\) less than the second value, then the second is \(\frac{r}{100 - r}\times 100\%\) more than the first.",
             r"\[ \text{Second is } \frac{r}{100 - r}\times 100\%\text{ more than the first} \]",
             [("Second value", "100"), ("First value", "100 - r"), ("Gap measured on the first", r"\frac{r}{100 - r}\times 100")],
             r"The gap is the same \(r\), but 'more than the first' measures it on the smaller value \(100 - r\).",
             "'A is r% less than B. By how much per cent is B more than A?'",
             r"A is \(30\%\) less than B: B is \(\frac{30}{70}\times 100 = 42\frac{6}{7}\%\) more than A.",
             r"Answering \(r\%\) again - the base has changed from B to A."),
    36: card(36, "Equal Increase and Decrease: Always a Loss",
             r"If a value is first increased by \(x\%\) and then decreased by \(x\%\) (or decreased first and then increased), the net change is always a "
             r"DECREASE of \(\frac{x^2}{100}\%\).",
             r"\[ \text{Net decrease} = \frac{x^2}{100}\% \]",
             [("Start", "100"), ("After +x%", "100 + x"), ("After -x%", r"(100 + x)\frac{100 - x}{100} = 100 - \frac{x^2}{100}")],
             r"The decrease is taken on a bigger (or the increase on a smaller) value, so the two changes never cancel.",
             "Salary raised and then cut by the same %, goods marked up and then discounted by the same %, population up and down by the same %.",
             r"Up \(10\%\), down \(10\%\): \(\frac{10^2}{100} = 1\%\) decrease. Marked up \(12\%\), discount \(12\%\): loss \(1.44\%\).",
             r"Saying 'no change' because the two percentages are equal."),
    37: card(37, "An Increase and a Decrease: Net Effect",
             r"If a value is increased by \(x\%\) and decreased by \(y\%\) (in either order), the net change is \(\left(x - y - \frac{xy}{100}\right)\%\): "
             r"an increase if positive, a decrease if negative.",
             r"\[ \text{Net effect} = \left(x - y - \frac{xy}{100}\right)\% \]",
             [("Start", "100"), ("After +x% and -y%", r"100\times\frac{100 + x}{100}\times\frac{100 - y}{100}"),
              ("Net effect", r"x - y - \frac{xy}{100}")],
             r"The two factors multiply: \(\frac{(100 + x)(100 - y)}{100} = 100 + x - y - \frac{xy}{100}\). The order of the changes does not matter.",
             "A salary (price, population) rises by x% and falls by y%, or goods are marked up x% and sold at a y% discount: find the net % change or profit/loss.",
             r"Up \(10\%\), down \(5\%\): \(10 - 5 - \frac{50}{100} = 4.5\%\) increase. Marked up \(20\%\), discount \(10\%\): \(8\%\) profit.",
             r"Writing \(x - y\) and forgetting \(-\frac{xy}{100}\), or reading a negative result as a gain."),
    38: card(38, "Two Equal Successive Increases",
             r"If a value is increased successively by \(x\%\) and \(x\%\), the final increase is \(\left(2x + \frac{x^2}{100}\right)\%\).",
             r"\[ \text{Final increase} = \left(2x + \frac{x^2}{100}\right)\% \]",
             [("Start", "100"), ("After the first x%", "100 + x"), ("After the second x%", r"100 + 2x + \frac{x^2}{100}")],
             r"The second increase is also taken on the first increase, which adds the extra \(\frac{x^2}{100}\).",
             "Prices marked up x% and then raised x% again, or two equal yearly increases: the total % increase (profit) is asked.",
             r"\(20\%\) and \(20\%\): \(40 + \frac{400}{100} = 44\%\).",
             r"Answering \(2x\) (\(40\%\)) and missing the \(\frac{x^2}{100}\)."),
    39: card(39, "Two Successive Increases",
             r"If a value is increased successively by \(x\%\) and \(y\%\), the final increase is \(\left(x + y + \frac{xy}{100}\right)\%\).",
             r"\[ \text{Final increase} = \left(x + y + \frac{xy}{100}\right)\% \]",
             [("Start", "100"), ("After x%", "100 + x"), ("After y% more", r"100 + x + y + \frac{xy}{100}")],
             r"The second increase acts on the already-increased value, adding \(\frac{xy}{100}\) on top of \(x + y\).",
             "Two successive increases (marked up, then raised again; two yearly growths): the single equivalent increase or profit is asked.",
             r"\(15\%\) then \(10\%\): \(15 + 10 + \frac{150}{100} = 26.5\%\).",
             r"Adding \(x + y\) only."),
    40: card(40, "Two Successive Decreases",
             r"If a value is decreased successively by \(x\%\) and \(y\%\), the final decrease is \(\left(x + y - \frac{xy}{100}\right)\%\).",
             r"\[ \text{Final decrease} = \left(x + y - \frac{xy}{100}\right)\% \]",
             [("Start", "100"), ("After x% off", "100 - x"), ("After y% off", r"100 - x - y + \frac{xy}{100}")],
             r"The second decrease is taken on the already-reduced value, so it is smaller than \(y\%\) of the original by \(\frac{xy}{100}\).",
             "Population (price, value) decreases by x% and then by y%: the total % decrease is asked.",
             r"\(10\%\) then \(20\%\): \(10 + 20 - \frac{200}{100} = 28\%\).",
             r"Adding \(x + y\) - the total fall is always less than that."),
}

OLD = {
    33: {621: (lambda: other_side(33, 10), "If the price of sugar falls by 10%, by how much per cent must a householder increase its consumption so as "
                                           "not to decrease the expenditure on this item?",
               {"a": P(F(80, 3)), "b": P(F(9, 100)), "c": P(F(100, 9)), "d": P(F(45, 6))})},
    34: {622: (lambda: other_side(34, 25), "If A's salary is 25% more than that of B, then by how much per cent is B's salary less than that of A?",
               {"a": P(20), "b": P(30), "c": P(45), "d": P(34)})},
    35: {623: (lambda: other_side(35, 30), "If A's salary is 30% less than that of B, then by how much per cent is B's salary more than that of A?",
               {"a": P(F(7, 300)), "b": P(F(300, 7)), "c": P(F(700, 3)), "d": P(F(30, 17))})},
    36: {624: (lambda: up_down(10, 10, "salary"), "The salary of a worker is first increased by 10% and thereafter it is reduced by 10%. What is "
                                                  "the change in his salary?",
               {"a": change("Decrease", 10), "b": change("Increase", 1), "c": "No change", "d": change("Decrease", 1)})},
    37: {625: (lambda: up_down(10, 5, "salary"), "The salary of a worker was first increased by 10% and thereafter decreased by 5%. What was the "
                                                 "change in his salary?",
               {"a": change("Increase", 5), "b": change("Decrease", F(9, 2)), "c": change("Increase", F(9, 2)), "d": change("Increase", F(11, 2))})},
    38: {626: (lambda: successive(38, 20), "A shopkeeper marks the prices of his goods at 20% higher than the original price. Due to an increase in "
                                           "demand he again increases them by 20%. What profit does he get?",
               {"a": PD(54), "b": PD(44), "c": PD(F(34, 3)), "d": PD(F(22, 5))})},
    39: {627: (lambda: successive(39, 15, 10), "A shopkeeper marks the prices at 15% higher than the original price. Due to an increase in demand, "
                                               "he further increases the price by 10%. How much per cent profit will he get?",
               {"a": PD(F(64, 25)), "b": PD(F(128, 5)), "c": PD(F(53, 20)), "d": PD(F(53, 2))})},
    40: {628: (lambda: successive(40, 10, 20), "The population of a town is decreased by 10% and 20% in two successive years. By what per cent is "
                                               "the population decreased after two years?",
               {"a": PD(F(14, 5)), "b": PD(28), "c": PD(32), "d": PD(F(111, 5))})},
}


def chg(pairs):
    return [change(w, v) if w != "none" else "No change" for w, v in pairs]


NEW = {
    33: [("r33_e1", "If the price of rice falls by 40%, by how much per cent must a householder increase its consumption so as not to decrease "
                    "the expenditure on it?", lambda: other_side(33, 40), [P(40), P(F(200, 3)), P(F(200, 7)), P(60)], 2),
         ("r33_e2", "If the price of tea falls by 50%, by how much per cent must a householder increase its consumption so as not to decrease "
                    "the expenditure on it?", lambda: other_side(33, 50), [P(50), P(75), P(100), P(200)], 3),
         ("r33_e3", "If the price of salt falls by 4%, by how much per cent must a householder increase its consumption so as not to decrease "
                    "the expenditure on it?", lambda: other_side(33, 4), [P(F(25, 6)), P(4), P(F(50, 13)), P(5)], 1),
         ("r33_e4", "If the price of wheat falls by 35%, by how much per cent must a householder increase its consumption so as not to decrease "
                    "the expenditure on it?", lambda: other_side(33, 35), [P(35), P(F(700, 27)), P(F(704, 13)), P(F(700, 13))], 4),
         ("r33_e5", r"If the price of oil falls by \(37\frac{1}{2}\%\), by how much per cent must a householder increase its consumption so as not "
                    r"to decrease the expenditure on it?", lambda: other_side(33, F(75, 2)), [P(F(75, 2)), P(60), P(F(300, 11)), P(F(125, 2))], 2),
         ("r33_e6", r"If the price of coffee falls by \(9\frac{1}{11}\%\), by how much per cent must a householder increase its consumption so as "
                    r"not to decrease the expenditure on it?", lambda: other_side(33, F(100, 11)), [P(F(100, 11)), P(F(25, 3)), P(10), P(F(100, 9))], 3),
         ("r33_e7", "The price of an article is cut by 20%. To bring it back to the former value, by what per cent must the new price be increased?",
          lambda: other_side(33, 20, restore=True), [P(20), P(F(50, 3)), P(24), P(25)], 4)],
    34: [("r34_e1", "If A's salary is 40% more than that of B, then by how much per cent is B's salary less than that of A?",
          lambda: other_side(34, 40), [P(F(200, 7)), P(40), P(30), P(F(197, 7))], 1),
         ("r34_e2", "If A's salary is 30% more than that of B, then by how much per cent is B's salary less than that of A?",
          lambda: other_side(34, 30), [P(30), P(F(300, 13)), P(F(70, 3)), P(F(300, 7))], 2),
         ("r34_e3", "If A's salary is 15% more than that of B, then by how much per cent is B's salary less than that of A?",
          lambda: other_side(34, 15), [P(15), P(F(300, 17)), P(F(300, 23)), P(F(40, 3))], 3),
         ("r34_e4", "One number is 100% more than another. By how much per cent is the second number less than the first?",
          lambda: other_side(34, 100), [P(100), P(F(100, 3)), P(F(200, 3)), P(50)], 4),
         ("r34_e5", "One number is 75% more than another. By how much per cent is the second number less than the first?",
          lambda: other_side(34, 75), [P(F(300, 7)), P(75), P(F(295, 7)), P(F(400, 7))], 1),
         ("r34_e6", r"One number is \(33\frac{1}{3}\%\) more than another. By how much per cent is the second number less than the first?",
          lambda: other_side(34, F(100, 3)), [P(F(100, 3)), P(25), P(20), P(50)], 2)],
    35: [("r35_e1", "If A's salary is 2% less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, 2), [P(2), P(F(100, 51)), P(F(100, 49)), P(F(99, 49))], 3),
         ("r35_e2", "If A's salary is 36% less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, 36), [P(36), P(F(450, 17)), P(64), P(F(225, 4))], 4),
         ("r35_e3", "If A's salary is 45% less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, 45), [P(F(900, 11)), P(45), P(F(900, 29)), P(55)], 1),
         ("r35_e4", "If A's salary is 60% less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, 60), [P(60), P(150), P(F(75, 2)), P(F(200, 3))], 2),
         ("r35_e5", r"If A's salary is \(12\frac{1}{2}\%\) less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, F(25, 2)), [P(F(25, 2)), P(F(100, 9)), P(F(100, 7)), P(F(99, 7))], 3),
         ("r35_e6", "If A's salary is 75% less than that of B, then by how much per cent is B's salary more than that of A?",
          lambda: other_side(35, 75), [P(75), P(F(400, 3)), P(400), P(300)], 4)],
    36: [("r36_ex2", "A shopkeeper marks the price of his goods 18% higher than the cost price. After that, he allows a discount of 18%. "
                     "What is his percentage profit or loss?", lambda: up_down(18, 18, "price"),
          chg([("Loss", F(81, 25)), ("Profit", F(81, 25)), ("none", 0), ("Loss", F(162, 5))]), 1),
         ("r36_ex3", "The population of a town increases by 35% in the first year and decreases by 35% in the next year. What is the effect "
                     "on the population of the town?", lambda: up_down(35, 35, "population"),
          chg([("Increase", F(49, 4)), ("Decrease", F(49, 4)), ("none", 0), ("Decrease", F(49, 40))]), 2),
         ("r36_e1", "The salary of a worker is first increased by 3% and thereafter it is reduced by 3%. What is the change in his salary?",
          lambda: up_down(3, 3, "salary"), chg([("Increase", F(9, 100)), ("Decrease", F(9, 10)), ("Decrease", F(9, 100)), ("Increase", 9)]), 3),
         ("r36_e2", "The salary of a worker is first increased by 30% and thereafter it is reduced by 30%. What is the change in his salary?",
          lambda: up_down(30, 30, "salary"), chg([("Increase", 9), ("Decrease", F(9, 10)), ("Decrease", 6), ("Decrease", 9)]), 4),
         ("r36_e3", "A shopkeeper raises the price of his goods by 17% and then sells them at a discount of 17%. What is his percentage profit or loss?",
          lambda: up_down(17, 17, "price"), chg([("Loss", F(289, 100)), ("Profit", F(289, 100)), ("Loss", F(189, 100)), ("Profit", F(189, 100))]), 1),
         ("r36_e4", "A trader marks his goods 11% above the cost price and then gives a discount of 11%. What is his percentage profit or loss?",
          lambda: up_down(11, 11, "price"), chg([("Profit", F(121, 100)), ("Loss", F(121, 100)), ("Loss", F(221, 100)), ("Profit", F(221, 100))]), 2),
         ("r36_e5", "The salary of a worker is first increased by 23% and thereafter it is reduced by 23%. What is the change in his salary?",
          lambda: up_down(23, 23, "salary"), chg([("Increase", F(529, 100)), ("Decrease", F(429, 100)), ("Decrease", F(529, 100)), ("Increase", F(429, 100))]), 3),
         ("r36_e6", "The salary of a worker is first increased by 40% and thereafter it is reduced by 40%. What is the change in his salary?",
          lambda: up_down(40, 40, "salary"), chg([("Increase", 16), ("Decrease", F(8, 5)), ("Increase", F(8, 5)), ("Decrease", 16)]), 4)],
    37: [("r37_ex2", "A shopkeeper marks the prices of his goods at 25% higher than the original price. After that, he allows a discount of 15%. "
                     "What profit or loss does he make?", lambda: up_down(25, 15, "price"),
          chg([("Profit", F(25, 4)), ("Loss", F(25, 4)), ("Profit", 10), ("Profit", F(15, 4))]), 1),
         ("r37_ex3", "The salary of a worker is first decreased by 25% and then increased by 20%. What is the percentage effect on his salary?",
          lambda: up_down(20, 25, "salary", down_first=True), chg([("Increase", 10), ("Decrease", 10), ("Decrease", 5), ("Decrease", 15)]), 2),
         ("r37_ex4", "The population of a town was reduced by 10% in one year. In the next year it was increased by 20%. What is the percentage "
                     "effect on the population over the two years?", lambda: up_down(20, 10, "population", down_first=True),
          chg([("Decrease", 8), ("Increase", 10), ("Increase", 8), ("Increase", 12)]), 3),
         ("r37_e1", "The salary of a worker was first increased by 9% and thereafter decreased by 5%. What was the change in his salary?",
          lambda: up_down(9, 5, "salary"), chg([("Decrease", F(71, 20)), ("Increase", F(89, 20)), ("Decrease", F(89, 20)), ("Increase", F(71, 20))]), 4),
         ("r37_e2", "The salary of a worker was first increased by 12% and thereafter decreased by 20%. What was the change in his salary?",
          lambda: up_down(12, 20, "salary"), chg([("Decrease", F(52, 5)), ("Increase", F(52, 5)), ("Decrease", 8), ("Decrease", F(28, 5))]), 1),
         ("r37_e3", "The salary of a worker was first increased by 25% and thereafter decreased by 16%. What was the change in his salary?",
          lambda: up_down(25, 16, "salary"), chg([("Decrease", 5), ("Increase", 5), ("Increase", 9), ("Decrease", 9)]), 2),
         ("r37_e4", "A shopkeeper marks the prices of his goods at 40% higher than the original price. After that, he allows a discount of 25%. "
                    "What profit or loss does he make?", lambda: up_down(40, 25, "price"),
          chg([("Profit", 15), ("Loss", 5), ("Profit", 5), ("Profit", 10)]), 3),
         ("r37_e5", "A shopkeeper marks the prices of his goods at 60% higher than the original price. After that, he allows a discount of 30%. "
                    "What profit or loss does he make?", lambda: up_down(60, 30, "price"),
          chg([("Profit", 30), ("Loss", 12), ("Profit", 18), ("Profit", 12)]), 4),
         ("r37_e6", "A shopkeeper marks the prices of his goods at 35% higher than the original price. After that, he allows a discount of 20%. "
                    "What profit or loss does he make?", lambda: up_down(35, 20, "price"),
          chg([("Profit", 8), ("Profit", 15), ("Loss", 8), ("Profit", 7)]), 1),
         ("r37_e7", "If the salary of a worker is first decreased by 25% and then increased by 10%, what is the percentage effect on his salary?",
          lambda: up_down(10, 25, "salary", down_first=True), chg([("Decrease", 15), ("Decrease", F(35, 2)), ("Increase", F(35, 2)), ("Decrease", F(25, 2))]), 2),
         ("r37_e8", "The population of a town was reduced by 20% in the year 2010. In 2011 it was increased by 30%. What is the percentage effect "
                    "on the population at the beginning of 2012?", lambda: up_down(30, 20, "population", down_first=True),
          chg([("Decrease", 4), ("Increase", 10), ("Increase", 4), ("Increase", 6)]), 3)],
    38: [("r38_e1", "A shopkeeper marks the prices of his goods at 4% higher than the original price. Due to an increase in demand he again "
                    "increases them by 4%. What profit does he get?", lambda: successive(38, 4), [PD(8), PD(F(204, 25)), PD(F(42, 5)), PD(16)], 2),
         ("r38_e2", "A shopkeeper marks the prices of his goods at 30% higher than the original price. Due to an increase in demand he again "
                    "increases them by 30%. What profit does he get?", lambda: successive(38, 30), [PD(60), PD(66), PD(69), PD(72)], 3),
         ("r38_e3", "A shopkeeper marks the prices of his goods at 12% higher than the original price. Due to an increase in demand he again "
                    "increases them by 12%. What profit does he get?", lambda: successive(38, 12), [PD(F(636, 25)), PD(24), PD(F(126, 5)), PD(F(611, 25))], 1),
         ("r38_e4", "A shopkeeper marks the prices of his goods at 18% higher than the original price. Due to an increase in demand he again "
                    "increases them by 18%. What profit does he get?", lambda: successive(38, 18), [PD(36), PD(F(1971, 50)), PD(F(806, 25)), PD(F(981, 25))], 4),
         ("r38_e5", "A shopkeeper marks the prices of his goods at 35% higher than the original price. Due to an increase in demand he again "
                    "increases them by 35%. What profit does he get?", lambda: successive(38, 35), [PD(70), PD(F(329, 4)), PD(F(321, 4)), PD(F(289, 4))], 2)],
    39: [("r39_e1", "A shopkeeper marks the prices at 4% higher than the original price. Due to an increase in demand, he further increases the "
                    "price by 10%. How much per cent profit will he get?", lambda: successive(39, 4, 10), [PD(14), PD(F(351, 25)), PD(15), PD(F(72, 5))], 4),
         ("r39_e2", "A shopkeeper marks the prices at 5% higher than the original price. Due to an increase in demand, he further increases the "
                    "price by 20%. How much per cent profit will he get?", lambda: successive(39, 5, 20), [PD(26), PD(25), PD(F(51, 2)), PD(F(105, 4))], 1),
         ("r39_e3", "A shopkeeper marks the prices at 25% higher than the original price. Due to an increase in demand, he further increases the "
                    "price by 12%. How much per cent profit will he get?", lambda: successive(39, 25, 12), [PD(37), PD(40), PD(43), PD(42)], 2),
         ("r39_e4", "A shopkeeper marks the prices at 10% higher than the original price. Due to an increase in demand, he further increases the "
                    "price by 30%. How much per cent profit will he get?", lambda: successive(39, 10, 30), [PD(40), PD(F(85, 2)), PD(43), PD(33)], 3),
         ("r39_e5", "A shopkeeper marks the prices at 30% higher than the original price. Due to an increase in demand, he further increases the "
                    "price by 20%. How much per cent profit will he get?", lambda: successive(39, 30, 20), [PD(50), PD(60), PD(52), PD(56)], 4)],
    40: [("r40_e1", "The population of a town decreases by 4% and 10% in two successive years. By what per cent is the population decreased "
                    "after two years?", lambda: successive(40, 4, 10), [PD(F(68, 5)), PD(14), PD(F(72, 5)), PD(F(32, 5))], 1),
         ("r40_e2", "The population of a town decreases by 6% and 5% in two successive years. By what per cent is the population decreased "
                    "after two years?", lambda: successive(40, 6, 5), [PD(11), PD(F(107, 10)), PD(F(113, 10)), PD(F(103, 10))], 2),
         ("r40_e3", "The population of a town decreases by 10% and 30% in two successive years. By what per cent is the population decreased "
                    "after two years?", lambda: successive(40, 10, 30), [PD(40), PD(43), PD(37), PD(34)], 3),
         ("r40_e4", "The population of a town decreases by 30% and 40% in two successive years. By what per cent is the population decreased "
                    "after two years?", lambda: successive(40, 30, 40), [PD(70), PD(82), PD(52), PD(58)], 4),
         ("r40_e5", "The population of a town decreases by 30% and 50% in two successive years. By what per cent is the population decreased "
                    "after two years?", lambda: successive(40, 30, 50), [PD(65), PD(80), PD(95), PD(60)], 1)],
}


def main():
    for n in range(33, 41):
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
