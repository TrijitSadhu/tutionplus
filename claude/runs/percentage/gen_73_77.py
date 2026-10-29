"""Rules 73-77 (the last rules of the chapter): writes the five rule cards, regenerates the old worked-example rows 657-661 in the
prompt #12 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their text
and options (657 now asks for both incomes its options give; 660 had no option holding 24 kg), and adds the book exercises
(numbers changed, wording rewritten) as one JsonImport payload per rule. Rule 77's answer is of kind "signed"."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import P, result  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402
from gen_33_40 import D, PD  # noqa: E402


def KG(v):
    return rf"\({D(v)}\) kg"


# ---------------------------------------------------------------- Rule 73: A more than B, B less than C
T73 = (r"If the monthly income of A is \(x\%\) more than that of B, B's is \(y\%\) less than that of C, and the difference between the incomes "
       r"of A and C is Rs \(M\), then the monthly incomes of B and C are<br>"
       r"\[ \text{Rs }\frac{100(100 - y)M}{(100 + x)(100 - y) - 100^2}\quad\text{and}\quad \text{Rs }\frac{100^2 M}{(100 + x)(100 - y) - 100^2} \]")


def incomes(x, y, M, names=("A", "B", "C"), both=False):
    x, y, M = F(x), F(y), F(M)
    A_, B_, C_ = names
    den = (100 + x) * (100 - y) - 10000
    B = 100 * (100 - y) * M / abs(den)
    C = 10000 * M / abs(den)
    b100 = 100 - y
    a100 = b100 * (100 + x) / 100
    trad = steps(
        (f"Take {C_}'s income as 100.", rf"{B_} \(= 100 - {D(y)} = {D(b100)}\), {A_} \(= {D(b100)} + \frac{{{D(x)}}}{{100}}\times {D(b100)} = {D(a100)}\)."),
        ("Match the difference.", rf"{A_} \(-\) {C_} \(= {D(a100 - 100)}\) on this scale, and it is really Rs \({D(M)}\), so each unit is "
                                  rf"\(\frac{{{D(M)}}}{{{D(abs(a100 - 100))}}} = {D(M / abs(a100 - 100))}\) rupees."),
        ("Scale up.", rf"{B_} \(= {D(b100)}\times {D(M / abs(a100 - 100))} = {D(B)}\), {C_} \(= 100\times {D(M / abs(a100 - 100))} = {D(C)}\)."))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(M = {D(M)}\)."),
        ("Apply the specified rule.", r"\[ B = \frac{100(100 - y)M}{(100 + x)(100 - y) - 100^2},\qquad C = \frac{100^2 M}{(100 + x)(100 - y) - 100^2} \]"),
        ("Substitute the values.", rf"\[ (100 + {D(x)})(100 - {D(y)}) - 10000 = {D((100 + x) * (100 - y))} - 10000 = {D(den)} \]"
                                   rf"\[ {B_} = \frac{{100\times {D(100 - y)}\times {D(M)}}}{{{D(den)}}} = {D(B)},\qquad {C_} = \frac{{10000\times {D(M)}}}{{{D(den)}}} = {D(C)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(M = {D(M)}\).", rf"Denominator \((100 + x)(100 - y) - 100^2 = {D(den)}\).",
          rf"{B_} \(= {D(B)}\), {C_} \(= {D(C)}\)."]
    sc = rf"\[ {B_} = \frac{{100\times {D(100 - y)}\times {D(M)}}}{{{D(den)}}} = {D(B)} \]"
    if both:
        return result(("pair", (B, C)), T73, trad, rule, rf"{B_} Rs \({D(B)}\), {C_} Rs \({D(C)}\)", rb, sc)
    return result(("number", B), T73, trad, rule, Rsx(B), rb, sc)


# ---------------------------------------------------------------- Rule 74: two weights in a ratio
T74 = (r"If the weights of A and B are in the ratio \(a : b\), A's weight increases by \(x\%\) and the total becomes \(W\) kg with an increase of "
       r"\(y\%\), then B's weight increases by<br>\[ \left[\left(\frac{100 + y}{100}\right)\left(1 + \frac{a}{b}\right) - "
       r"\left\{\frac{a}{b}\left(\frac{100 + x}{100}\right) + 1\right\}\right]\times 100\% \]")


def weights(a, b, x, y, W):
    a, b, x, y, W = map(F, (a, b, x, y, W))
    k = W / ((a + b) * (100 + y) / 100)
    A0, B0 = a * k, b * k
    A1 = A0 * (100 + x) / 100
    B1 = W - A1
    v = (B1 - B0) / B0 * 100
    f = ((100 + y) / 100) * (1 + a / b) - (a / b * (100 + x) / 100 + 1)
    assert f * 100 == v
    trad = steps(
        ("Find the old weights.", rf"Let the weights be \({D(a)}k\) and \({D(b)}k\). The total \({D(a + b)}k\) rose by \({D(y)}\%\) to \({D(W)}\):<br>"
                                  rf"\[ {D(a + b)}k\times \frac{{{D(100 + y)}}}{{100}} = {D(W)} \Rightarrow k = {D(k)} \]A \(= {D(A0)}\) kg, B \(= {D(B0)}\) kg."),
        ("Find the new weights.", rf"A \(= {D(A0)}\times \frac{{{D(100 + x)}}}{{100}} = {D(A1)}\) kg, so B \(= {D(W)} - {D(A1)} = {D(B1)}\) kg."),
        ("Find B's increase.", rf"\[ \frac{{{D(B1)} - {D(B0)}}}{{{D(B0)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(a : b = {D(a)} : {D(b)}\), \(x = {D(x)}\), \(y = {D(y)}\)."),
        ("Apply the specified rule.", r"\[ \left[\left(\frac{100 + y}{100}\right)\left(1 + \frac{a}{b}\right) - \left\{\frac{a}{b}\left(\frac{100 + x}{100}\right) + 1\right\}\right]\times 100 \]"),
        ("Substitute the values.", rf"\[ \left[\frac{{{D(100 + y)}}}{{100}}\times \frac{{{D(a + b)}}}{{{D(b)}}} - \left\{{\frac{{{D(a)}}}{{{D(b)}}}\times \frac{{{D(100 + x)}}}{{100}} + 1\right\}}\right]\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(a : b = {D(a)} : {D(b)}\), \(x = {D(x)}\), \(y = {D(y)}\).", "Apply the weight-ratio rule.", rf"B's weight increases by \({tex(v)}\%\)."]
    sc = rf"\[ \left[\frac{{{D(100 + y)}}}{{100}}\times \frac{{{D(a + b)}}}{{{D(b)}}} - \left\{{\frac{{{D(a)}}}{{{D(b)}}}\times \frac{{{D(100 + x)}}}{{100}} + 1\right\}}\right]\times 100 = {tex(v)}\% \]"
    return result(("number", v), T74, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- Rule 75: income from savings
T75 = (r"A person spends \(x\%\) of his monthly income on item A and \(y\%\) of the remaining on item B and saves the rest, Rs \(S\) a month. Then<br>"
       r"\[ \text{Income} = \frac{S\times 100^2}{(100 - x)(100 - y)},\qquad \text{A} = \frac{S\times x\times 100}{(100 - x)(100 - y)},\qquad "
       r"\text{B} = \frac{y\times S}{100 - y} \]")


def from_savings(x, y, S, ask, yearly=False):
    """ask: 'income', 'B' or 'all' (income, A, B)."""
    x, y, S = F(x), F(y), F(S)
    s = S / 12 if yearly else S
    I = s * 10000 / ((100 - x) * (100 - y))
    A = s * x * 100 / ((100 - x) * (100 - y))
    B = y * s / (100 - y)
    pre = rf"Monthly savings \(= \frac{{{D(S)}}}{{12}} = {D(s)}\).<br>" if yearly else ""
    trad = steps(
        ("Follow Rs 100 of income.", pre + rf"Item A takes \({D(x)}\), leaving \({D(100 - x)}\); item B takes \({D(y)}\%\) of it, \({D((100 - x) * y / 100)}\), "
                                     rf"leaving \({D((100 - x) * (100 - y) / 100)}\) saved."),
        ("Scale to the real savings.", rf"Saving \({D((100 - x) * (100 - y) / 100)}\) goes with income 100, so saving \({D(s)}\) goes with<br>"
                                       rf"\[ \frac{{{D(s)}\times 100}}{{{D((100 - x) * (100 - y) / 100)}}} = {D(I)} \]"
                                       rf"Item A \(= \frac{{{D(x)}}}{{100}}\times {D(I)} = {D(A)}\), item B \(= {D(I)} - {D(A)} - {D(s)} = {D(B)}\)."))
    rule = steps(
        ("Identify the values.", pre + rf"\(x = {D(x)}\), \(y = {D(y)}\), \(S = {D(s)}\)."),
        ("Apply the specified rule.", r"\[ \text{Income} = \frac{S\times 100^2}{(100 - x)(100 - y)},\quad \text{A} = \frac{Sx\times 100}{(100 - x)(100 - y)},\quad \text{B} = \frac{yS}{100 - y} \]"),
        ("Substitute the values.", rf"\[ \text{{Income}} = \frac{{{D(s)}\times 10000}}{{{D(100 - x)}\times {D(100 - y)}}} = {D(I)},\quad "
                                   rf"\text{{A}} = \frac{{{D(s)}\times {D(x)}\times 100}}{{{D(100 - x)}\times {D(100 - y)}}} = {D(A)},\quad "
                                   rf"\text{{B}} = \frac{{{D(y)}\times {D(s)}}}{{{D(100 - y)}}} = {D(B)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(S = {D(s)}\) a month.", "Apply the savings rule.", rf"Income \({D(I)}\), A \({D(A)}\), B \({D(B)}\)."]
    if ask == "income":
        sc = rf"\[ \frac{{{D(s)}\times 10000}}{{{D(100 - x)}\times {D(100 - y)}}} = {D(I)} \]"
        return result(("number", I), T75, trad, rule, Rsx(I), rb, sc)
    if ask == "B":
        sc = rf"\[ \frac{{{D(y)}\times {D(s)}}}{{100 - {D(y)}}} = {D(B)} \]"
        return result(("number", B), T75, trad, rule, Rsx(B), rb, sc)
    sc = rf"\[ \text{{Income}} = {D(I)},\quad \text{{A}} = {D(A)},\quad \text{{B}} = {D(B)} \]"
    return result(("triple", (I, A, B)), T75, trad, rule, rf"income Rs \({D(I)}\), food Rs \({D(A)}\), rent Rs \({D(B)}\)", rb, sc)


# ---------------------------------------------------------------- Rule 76: price up x%, spending up only y%
T76 = (r"When the price of an item is increased by \(x\%\) and a family cuts its consumption so that the expenditure is only \(y\%\) more than before, "
       r"and \(W\) kg were used per month before, the new monthly consumption is<br>\[ \frac{100 + y}{100 + x}\times W\text{ kg} \]")


def new_use(x, y, W):
    x, y, W = F(x), F(y), F(W)
    v = (100 + y) / (100 + x) * W
    trad = steps(
        ("Take the old price as Rs 100 per kg.", rf"Old expenditure \(= 100\times {D(W)} = {D(100 * W)}\)."),
        ("Apply the changes.", rf"New price \(= {D(100 + x)}\); new expenditure \(= {D(100 * W)}\times \frac{{{D(100 + y)}}}{{100}} = {D(W * (100 + y))}\)."),
        ("Find the new consumption.", rf"\[ \frac{{{D(W * (100 + y))}}}{{{D(100 + x)}}} = {D(v)}\text{{ kg}} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(W = {D(W)}\)."),
        ("Apply the specified rule.", r"\[ \frac{100 + y}{100 + x}\times W \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(100 + y)}}}{{{D(100 + x)}}}\times {D(W)} = {D(v)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(W = {D(W)}\).", r"New use \(= \frac{100 + y}{100 + x}W\).", rf"\(\frac{{{D(100 + y)}}}{{{D(100 + x)}}}\times {D(W)} = {D(v)}\) kg."]
    sc = rf"\[ \frac{{{D(100 + y)}}}{{{D(100 + x)}}}\times {D(W)} = {D(v)}\text{{ kg}} \]"
    return result(("number", v), T76, trad, rule, KG(v), rb, sc)


# ---------------------------------------------------------------- Rule 77: price up x%, consumption down x%
T77 = (r"If the price of an item is increased by \(x\%\) and the consumption is reduced by \(x\%\), the expenditure changes by<br>"
       r"\[ -\left(\frac{x}{10}\right)^2\% \]the minus sign showing a decrease.")


def same_up_down(x):
    x = F(x)
    v = -(x / 10) ** 2
    new = (100 + x) * (100 - x)
    trad = steps(
        ("Take price and consumption as 100 each.", r"Old expenditure \(= 100\times 100 = 10000\)."),
        ("Apply the changes.", rf"Price \(= {D(100 + x)}\), consumption \(= {D(100 - x)}\), new expenditure \(= {D(new)}\)."),
        ("Compare.", rf"\[ \frac{{{D(new)} - 10000}}{{10000}}\times 100 = {D(v)}\% \]so the expenditure decreases by \({D(-v)}\%\)."))
    rule = steps(
        ("Identify the value.", rf"\(x = {D(x)}\)."),
        ("Apply the specified rule.", r"\[ -\left(\frac{x}{10}\right)^2\% \]"),
        ("Substitute the value.", rf"\[ -\left(\frac{{{D(x)}}}{{10}}\right)^2 = -({D(x / 10)})^2 = {D(v)}\% \]"))
    rb = [rf"\(x = {D(x)}\).", r"Change \(= -\left(\frac{x}{10}\right)^2\%\).", rf"\(-({D(x / 10)})^2 = {D(v)}\%\), a decrease."]
    sc = rf"\[ -\left(\frac{{{D(x)}}}{{10}}\right)^2 = {D(v)}\%\text{{ (decrease)}} \]"
    return result(("signed", v), T77, trad, rule, rf"a decrease of \({D(-v)}\%\)", rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    73: card(73, "Incomes Linked through a Third Person",
             r"If A's income is \(x\%\) more than B's, B's is \(y\%\) less than C's and A and C differ by Rs \(M\), then B \(= \frac{100(100 - y)M}{(100 + x)(100 - y) - 100^2}\) "
             r"and C \(= \frac{100^2 M}{(100 + x)(100 - y) - 100^2}\).",
             r"\[ B = \frac{100(100 - y)M}{(100 + x)(100 - y) - 100^2},\qquad C = \frac{100^2 M}{(100 + x)(100 - y) - 100^2} \]",
             [("C", "100"), ("B", "100 - y"), ("A", r"\frac{(100 - y)(100 + x)}{100}"), ("A - C", "M\\text{ rupees}")],
             r"With C as 100, every income is a number on one scale; the given difference fixes the size of one unit.",
             "Three people's incomes linked by 'more than' and 'less than'; the difference between two of them is given.",
             r"\(15\%\) more, \(10\%\) less, difference Rs 350: \(103.5 - 100 = 3.5\) units \(=\) Rs 350, so Shyam \(= 90\times 100 =\) Rs 9000.",
             r"Taking both percentages on the same person."),
    74: card(74, "Two Weights in a Ratio",
             r"If A and B weigh in the ratio \(a : b\), A's weight rises by \(x\%\) and the total rises by \(y\%\), then B's weight rises by "
             r"\(\left[\left(\frac{100 + y}{100}\right)\left(1 + \frac{a}{b}\right) - \left\{\frac{a}{b}\left(\frac{100 + x}{100}\right) + 1\right\}\right]\times 100\%\).",
             r"\[ \left[\left(\frac{100 + y}{100}\right)\left(1 + \frac{a}{b}\right) - \left\{\frac{a}{b}\left(\frac{100 + x}{100}\right) + 1\right\}\right]\times 100\% \]",
             [("Old weights", "ak,\\ bk"), ("New total", r"(a + b)k\frac{100 + y}{100}"), ("New B", r"\text{new total} - ak\frac{100 + x}{100}")],
             r"The total's increase is a weighted average of the two increases (Rule 8 / alligation), so B's increase can be found from A's and the total's.",
             "Two weights (or amounts) in a ratio; one rises by x% and the total by y%: B's % rise is asked.",
             r"\(3 : 5\), A \(+20\%\), total \(+25\%\): \(\left[1.25\times\frac{8}{5} - (0.6\times 1.2 + 1)\right]\times 100 = 28\%\).",
             r"Subtracting the two percentages (\(25 - 20\))."),
    75: card(75, "Income from Savings after Two Spends",
             r"A person spends \(x\%\) of the income on A and \(y\%\) of the remaining on B and saves Rs \(S\). Income \(= \frac{S\times 100^2}{(100 - x)(100 - y)}\), "
             r"A \(= \frac{Sx\times 100}{(100 - x)(100 - y)}\), B \(= \frac{yS}{100 - y}\).",
             r"\[ \text{Income} = \frac{S\times 100^2}{(100 - x)(100 - y)} \]",
             [("Income", "100"), ("After A", "100 - x"), ("Saved", r"\frac{(100 - x)(100 - y)}{100}")],
             r"Savings are what is left after both spends, so they are a fixed fraction of the income (Rule 17 again).",
             "Spending on food (or items) then a % of the remaining on rent (or clothes); savings given - income or one expense asked. Yearly savings: divide by 12 first.",
             r"\(20\%\) food, \(25\%\) of the rest on rent, saves Rs 6000: income \(= \frac{6000\times 10000}{80\times 75} =\) Rs 10000.",
             r"Taking \(y\%\) of the income instead of the remainder, or forgetting to turn yearly savings into monthly."),
    76: card(76, "Price Up, Spending Up Less",
             r"When the price rises by \(x\%\) and the family lets its spending rise by only \(y\%\), the new monthly consumption is \(\frac{100 + y}{100 + x}\times W\) kg.",
             r"\[ \text{New consumption} = \frac{100 + y}{100 + x}\times W \]",
             [("Expenditure", r"\times\frac{100 + y}{100}"), ("Price", r"\times\frac{100 + x}{100}"), ("Consumption", r"\times\frac{100 + y}{100 + x}")],
             r"Consumption \(=\) Expenditure \(\div\) Price, so its factor is the spending factor divided by the price factor.",
             "Price up x%, spending allowed to go up only y%, old consumption W kg: the new consumption is asked.",
             r"\(25\%\), \(20\%\), 25 kg: \(\frac{120}{125}\times 25 = 24\) kg.", r"Subtracting the percentages (\(25 - 20 = 5\%\))."),
    77: card(77, "Price Up x%, Consumption Down x%",
             r"If the price of an item rises by \(x\%\) and the consumption is cut by \(x\%\), the expenditure always DECREASES, by \(\left(\frac{x}{10}\right)^2\%\).",
             r"\[ \text{Change in expenditure} = -\left(\frac{x}{10}\right)^2\% \]",
             [("Price", "100 + x"), ("Consumption", "100 - x"), ("Expenditure", r"10000 - x^2")],
             r"\((100 + x)(100 - x) = 10000 - x^2\), a fall of \(\frac{x^2}{100}\%\) = \(\left(\frac{x}{10}\right)^2\%\) (Rule 43).",
             "Price up by some % and consumption down by the SAME %: what happens to the spending?",
             r"\(20\%\): \(-(2)^2 = -4\%\), a decrease of \(4\%\).", r"Saying the spending is unchanged."),
}

OLD = {
    73: {657: (lambda: incomes(15, 10, 350, ("Ram", "Shyam", "Sohan"), both=True),
               "Ram's monthly income is 15% more than that of Shyam. Shyam's monthly income is 10% less than that of Sohan. If the difference between "
               "the monthly incomes of Ram and Sohan is Rs 350, what are the monthly incomes of Shyam and Sohan?",
               {"a": "Shyam Rs 9000, Sohan Rs 10000", "b": "Shyam Rs 3900, Sohan Rs 11890", "c": "Shyam Rs 9300, Sohan Rs 12000",
                "d": "Shyam Rs 1900, Sohan Rs 10400"})},
    74: {658: (lambda: weights(3, 5, 20, 25, 80), "The weights of two persons A and B are in the ratio 3 : 5. A's weight increases by 20% and the total "
                                                  "weight of A and B together becomes 80 kg, with an increase of 25%. By what per cent did the weight of B increase?",
               {"a": PD(82), "b": PD(28), "c": PD(32), "d": PD(48)})},
    75: {659: (lambda: from_savings(20, 25, 6000, "all"),
               "Mr Raju spends 20% of his monthly income on food and 25% of the remaining on room rent. He saves the remaining amount. If the saving "
               "amount is Rs 6000, find the monthly income of Raju, the amount spent on food and the amount spent on room rent.",
               {"a": "Income Rs 2200, food Rs 2000, rent Rs 2000", "b": "Income Rs 2200, food Rs 2000, rent Rs 3000",
                "c": "Income Rs 10000, food Rs 2000, rent Rs 1000", "d": "Income Rs 10000, food Rs 2000, rent Rs 2000"})},
    76: {660: (lambda: new_use(25, 20, 25), "When the price of tea was increased by 25%, a family reduced its consumption in such a way that the "
                                            "expenditure on tea was only 20% more than before. If 25 kg were consumed per month before, find the new monthly consumption.",
               {"a": KG(22), "b": KG(24), "c": KG(23), "d": KG(20)})},
    77: {661: (lambda: same_up_down(20), "The price of sugar is increased by 20% and a housewife reduces her consumption of sugar by 20%. What happens "
                                         "to her expenditure on sugar?",
               {"a": "remains unaltered", "b": r"decreases by \(20\%\)", "c": r"decreases by \(4\%\)", "d": r"increases by \(4\%\)"})},
}

INC = ("Naresh's monthly income is {}% more than that of Raghu. Raghu's monthly income is {}% less than that of Vishal. If the difference between "
       "the monthly incomes of Naresh and Vishal is Rs {}, what is the monthly income of Raghu?")
WT = ("The weights of two friends {} and {} are in the ratio {} : {}. {}'s weight increases by {}% and the total weight of the two together becomes "
      "{} kg, with an increase of {}%. By what per cent did the weight of {} increase?")
USE = ("When the price of {} was increased by {}%, a family reduced its consumption in such a way that the expenditure on {} was only {}% more "
       "than before. If {} kg were consumed per month before, find the new monthly consumption.")
EXPQ = "The price of {} is increased by {}% and a housewife reduces her consumption of {} by {}%. What happens to her expenditure on {}?"


def wt(n1, n2, a, b, x, y, k):
    W = F((a + b) * k * (100 + y), 100)
    return WT.format(n1, n2, a, b, n1, x, D(W), y, n2), (lambda: weights(a, b, x, y, W))


def ex77(item, x, opts, pos):
    return EXPQ.format(item, x, item, x, item), (lambda: same_up_down(x)), opts, pos


def ch(rows):
    return ["remains unchanged" if s == 0 else rf"{'increases' if s > 0 else 'decreases'} by \({D(v)}\%\)" for s, v in rows]


NEW = {
    73: [("r73_e%d" % i, INC.format(x, y, M), (lambda x=x, y=y, M=M: incomes(x, y, M, ("Naresh", "Raghu", "Vishal"))), [Rsx(o) for o in opts], pos)
         for i, (x, y, M, opts, pos) in enumerate([(20, 10, 600, [6750, 7500, 6000, 7200], 1), (50, 20, 3000, [15000, 12000, 10000, 18000], 2),
                                                   (40, 25, 900, [18000, 12000, 13500, 15000], 3), (25, 10, 1500, [12000, 9000, 13500, 10800], 4)], 1)],
    74: [("r74_e%d" % i, *wt(*args), [PD(o) for o in opts], pos)
         for i, (args, opts, pos) in enumerate([(("Ram", "Shyam", 2, 3, 10, 16, 10), [20, 22, 16, 24], 1),
                                                (("Seeta", "Geeta", 1, 3, 20, 25, 15), [25, F(80, 3), 30, F(85, 3)], 2),
                                                (("Rinku", "Sunil", 3, 5, 30, 20, 10), [12, 16, 14, 15], 3),
                                                (("Ashok", "Vinod", 1, 4, 15, 12, 20), [12, F(21, 2), F(47, 4), F(45, 4)], 4)], 1)],
    75: [("r75_e1", "Mr Yadav spends 40% of his monthly salary on consumable items and 50% of the remaining on clothes and transport. He saves the "
                    "remaining amount. If his savings at the end of the year were Rs 43200, how much per month does he spend on clothes and transport?",
          lambda: from_savings(40, 50, 43200, "B", yearly=True), [Rsx(3600), Rsx(7200), Rsx(2400), Rsx(4800)], 1),
         ("r75_e2", "Pankaj spends 20% of his monthly salary on entertainment and 25% of the remaining on board and lodging. He saves the remaining "
                    "amount. If his monthly savings are Rs 2400, find his monthly salary.", lambda: from_savings(20, 25, 2400, "income"),
          [Rsx(3600), Rsx(4000), Rsx(4800), Rsx(3200)], 2),
         ("r75_e3", "Mr Yadav spends 25% of his monthly salary on consumable items and 20% of the remaining on clothes and transport. He saves the "
                    "remaining amount. If his savings at the end of the year were Rs 54000, how much per month does he spend on clothes and transport?",
          lambda: from_savings(25, 20, 54000, "B", yearly=True), [Rsx(1500), Rsx(900), Rsx(1125), Rsx(1350)], 3),
         ("r75_e4", "Mr Yadav spends 20% of his monthly salary on consumable items and 10% of the remaining on clothes and transport. He saves the "
                    "remaining amount. If his savings at the end of the year were Rs 25920, how much per month does he spend on clothes and transport?",
          lambda: from_savings(20, 10, 25920, "B", yearly=True), [Rsx(216), Rsx(300), Rsx(270), Rsx(240)], 4)],
    76: [("r76_e%d" % i, USE.format(item, x, item, y, W), (lambda x=x, y=y, W=W: new_use(x, y, W)), [KG(o) for o in opts], pos)
         for i, (item, x, y, W, opts, pos) in enumerate([("rice", 40, 12, 25, [20, 22, 21, 18], 1), ("tea", 25, 10, 30, [27, F(132, 5), F(128, 5), 24], 2),
                                                         ("wheat", 50, 20, 20, [15, 18, 16, 14], 3), ("coffee", 20, 8, 40, [34, 32, 38, 36], 4)], 1)],
    77: [("r77_e%d" % i, *ex77(item, x, ch(rows), pos))
         for i, (item, x, rows, pos) in enumerate([("coffee", 5, [(0, 0), (1, F(1, 4)), (-1, F(1, 4)), (-1, F(5, 2))], 3),
                                                   ("tea", 12, [(-1, F(36, 25)), (0, 0), (1, F(36, 25)), (-1, F(12, 5))], 1),
                                                   ("sugar", 35, [(0, 0), (-1, F(49, 4)), (1, F(49, 4)), (-1, F(7, 2))], 2),
                                                   ("groundnut oil", 40, [(0, 0), (1, 16), (-1, 4), (-1, 16)], 4)], 1)],
}


def main():
    for n in range(73, 78):
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
