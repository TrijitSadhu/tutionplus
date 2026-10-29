"""Rules 9-16: writes the eight rule cards, regenerates the old worked-example rows 597-604 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their text
(OCR "o f", PDF line breaks, display math in options, missing % signs, empty fifth option), and adds the book exercises
of these rules (numbers changed, wording rewritten) as one JsonImport payload per rule. Same output files as gen_1_8.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import P, Num, pnum, result  # noqa: E402


def Rsx(v):
    """Rupees with an exact mixed fraction when needed: Rs 18\\frac{3}{4}."""
    return rf"Rs \({tex(F(v))}\)"


# ---------------------------------------------------------------- Rules 9 and 10: original daily wage
T9 = r"When the increase per cent is given,<br>\[ \text{Original daily wage} = \frac{\text{Increased daily wage}}{100 + \%\text{ increase}}\times 100 \]"
T10 = r"When the decrease per cent is given,<br>\[ \text{Original daily wage} = \frac{\text{Decreased daily wage}}{100 - \%\text{ decrease}}\times 100 \]"


def wage(x, W, up):
    x, W = F(x), F(W)
    s, word, T = ("+", "increase", T9) if up else ("-", "decrease", T10)
    k = 100 + x if up else 100 - x
    w = W * 100 / k
    trad = steps(
        ("Form the equation.", rf"Let the daily wage before the {word} be Rs \(w\). A {word} of \({pnum(x)}\%\) gives<br>"
                               rf"\[ w {s} \frac{{{pnum(x)}}}{{100}}w = {tex(W)} \]"),
        ("Simplify.", rf"\[ \frac{{{pnum(k)}}}{{100}}w = {tex(W)} \]"),
        ("Solve.", rf"\[ w = {tex(W)}\times \frac{{100}}{{{pnum(k)}}} = {tex(w)} \]"))
    rule = steps(
        ("Identify the values.", rf"{word.capitalize()}d daily wage \(= {tex(W)}\), \(\%\) {word} \(= {pnum(x)}\)."),
        ("Apply the specified rule.", rf"\[ \text{{Original daily wage}} = \frac{{\text{{{word.capitalize()}d daily wage}}}}{{100 {s} \%\text{{ {word}}}}}\times 100 \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(W)}}}{{100 {s} {pnum(x)}}}\times 100 = \frac{{{tex(W)}\times 100}}{{{pnum(k)}}} = {tex(w)} \]"))
    rb = [rf"{word.capitalize()}d wage \(= {tex(W)}\), {word} \(= {pnum(x)}\%\).", rf"Original \(= \frac{{\text{{{word}d wage}}}}{{100 {s} {pnum(x)}}}\times 100\).",
          rf"\(\frac{{{tex(W)}\times 100}}{{{pnum(k)}}} = {tex(w)}\)."]
    sc = rf"\[ \frac{{{tex(W)}}}{{100 {s} {pnum(x)}}}\times 100 = {tex(w)} \]"
    return result(("number", w), T, trad, rule, Rsx(w), rb, sc)


# ---------------------------------------------------------------- Rule 11: working hours to restore production
T11 = (r"Production = Manpower \(\times\) Working hours. If the production falls by \(x\%\) because the manpower falls by \(x\%\), "
       r"the working hours must be increased by<br>\[ \frac{x}{100 - x}\times 100\% \]")


def hours(x):
    x = F(x)
    y = x * 100 / (100 - x)
    trad = steps(
        ("Take easy starting values.", r"Let the manpower be \(100\) units and the working hours \(100\) units, so the production is \(100\times 100 = 10000\)."),
        ("Find the new manpower.", rf"The production falls by \({pnum(x)}\%\) only because the manpower falls by \({pnum(x)}\%\): manpower \(= 100 - {pnum(x)} = {pnum(100 - x)}\)."),
        ("Find the hours that restore the production.", rf"\[ {pnum(100 - x)}\times h = 10000 \Rightarrow h = \frac{{10000}}{{{pnum(100 - x)}}} = {tex(10000 / (100 - x))} \]"),
        ("Find the increase.", rf"The hours rise from \(100\) to \({tex(10000 / (100 - x))}\), an increase of \({tex(y)}\%\)."))
    rule = steps(
        ("Identify the value.", rf"\(x = {pnum(x)}\)."),
        ("Apply the specified rule.", r"\[ \text{Increase in working hours} = \frac{x}{100 - x}\times 100\% \]"),
        ("Substitute the value.", rf"\[ \frac{{{pnum(x)}}}{{100 - {pnum(x)}}}\times 100 = \frac{{{pnum(x)}\times 100}}{{{pnum(100 - x)}}} = {tex(y)}\% \]"))
    rb = [rf"\(x = {pnum(x)}\).", r"Increase \(= \frac{x}{100 - x}\times 100\%\).", rf"\(\frac{{{pnum(x)}}}{{{pnum(100 - x)}}}\times 100 = {tex(y)}\%\)."]
    sc = rf"\[ \frac{{{pnum(x)}}}{{100 - {pnum(x)}}}\times 100 = {tex(y)}\% \]"
    return result(("number", y), T11, trad, rule, P(y), rb, sc)


# ---------------------------------------------------------------- Rules 12-15: two values more / less than a third
T12 = r"If two values are respectively \(x\%\) and \(y\%\) more than a third value, then the first is<br>\[ \frac{100 + x}{100 + y}\times 100\%\text{ of the second.} \]"
T13 = r"If two values are respectively \(x\%\) and \(y\%\) more than a third value, then the second is<br>\[ \frac{100 + y}{100 + x}\times 100\%\text{ of the first.} \]"
T14 = r"If two values are respectively \(x\%\) and \(y\%\) less than a third value, then the second is<br>\[ \frac{100 - y}{100 - x}\times 100\%\text{ of the first.} \]"
T15 = r"If two values are respectively \(x\%\) and \(y\%\) less than a third value, then the first is<br>\[ \frac{100 - x}{100 - y}\times 100\%\text{ of the second.} \]"
REL = {12: ("+", "first", T12), 13: ("+", "second", T13), 14: ("-", "second", T14), 15: ("-", "first", T15)}


def rel(n, x, y, how_much_less=False):
    """Rule n in 12-15. Asked value: the first as a % of the second (12, 15) or the second as a % of the first (13, 14);
    how_much_less=True asks by how many per cent it is less instead."""
    s, asked, T = REL[n]
    x, y = F(x), F(y)
    a, b = (100 + x, 100 + y) if s == "+" else (100 - x, 100 - y)
    num, den = (a, b) if asked == "first" else (b, a)
    other = "second" if asked == "first" else "first"
    pct = num / den * 100
    ans = 100 - pct if how_much_less else pct
    word = "more" if s == "+" else "less"
    fin = P(ans)
    trad_steps = [
        ("Take the third value as 100.", rf"First \(= 100 {s} {pnum(x)} = {pnum(a)}\), second \(= 100 {s} {pnum(y)} = {pnum(b)}\)."),
        (f"Express the {asked} as a per cent of the {other}.", rf"\[ \frac{{{pnum(num)}}}{{{pnum(den)}}}\times 100 = {tex(pct)}\% \]")]
    sym = ("100 + x", "100 + y") if s == "+" else ("100 - x", "100 - y")
    fnum, fden = sym if asked == "first" else sym[::-1]
    rule_steps = [
        ("Identify the values.", rf"\(x = {pnum(x)}\), \(y = {pnum(y)}\) ({word} than the third value)."),
        ("Apply the specified rule.", rf"\[ \text{{The {asked} is }} \frac{{{fnum}}}{{{fden}}}\times 100\%\text{{ of the {other}}} \]"),
        ("Substitute the values.", rf"\[ \frac{{{fnum.replace('x', pnum(x)).replace('y', pnum(y))}}}{{{fden.replace('x', pnum(x)).replace('y', pnum(y))}}}\times 100 "
                                   rf"= \frac{{{pnum(num)}}}{{{pnum(den)}}}\times 100 = {tex(pct)}\% \]")]
    rb = [rf"\(x = {pnum(x)}\), \(y = {pnum(y)}\).", rf"The {asked} is \(\frac{{{fnum}}}{{{fden}}}\times 100\%\) of the {other}.",
          rf"\(\frac{{{pnum(num)}}}{{{pnum(den)}}}\times 100 = {tex(pct)}\%\)."]
    sc = rf"\[ \frac{{{pnum(num)}}}{{{pnum(den)}}}\times 100 = {tex(pct)}\% \]"
    if how_much_less:
        last = (f"Find how much less the {asked} is.", rf"The {asked} is \({tex(pct)}\%\) of the {other}, so it is \(100 - {tex(pct)} = {tex(ans)}\%\) less than the {other}.")
        trad_steps.append(last)
        rule_steps.append(last)
        rb.append(rf"\(100 - {tex(pct)} = {tex(ans)}\%\) less.")
        sc = rf"\[ 100 - \frac{{{pnum(num)}}}{{{pnum(den)}}}\times 100 = 100 - {tex(pct)} = {tex(ans)}\% \]"
    return result(("number", ans), T, steps(*trad_steps), steps(*rule_steps), fin, rb, sc)


# ---------------------------------------------------------------- Rule 16: A is x% of C, B is y% of C
T16 = r"If A is \(x\%\) of C and B is \(y\%\) of C, then<br>\[ \text{A is } \frac{x}{y}\times 100\%\text{ of B.} \]"


def of_third(x, y, second_of_first=False):
    x, y = F(x), F(y)
    p, q = (y, x) if second_of_first else (x, y)
    names = ("second", "first") if second_of_first else ("first", "second")
    v = p / q * 100
    trad = steps(
        ("Take the third number as 100.", rf"First \(= {pnum(x)}\%\) of \(100 = {pnum(x)}\), second \(= {pnum(y)}\%\) of \(100 = {pnum(y)}\)."),
        (f"Express the {names[0]} as a per cent of the {names[1]}.", rf"\[ \frac{{{pnum(p)}}}{{{pnum(q)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"A = the {names[0]} number, \({pnum(p)}\%\) of C; B = the {names[1]} number, \({pnum(q)}\%\) of C."),
        ("Apply the specified rule.", r"\[ \text{A is } \frac{x}{y}\times 100\%\text{ of B} \]"),
        ("Substitute the values.", rf"\[ \frac{{{pnum(p)}}}{{{pnum(q)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"A (the {names[0]}) is \({pnum(p)}\%\) of C, B (the {names[1]}) is \({pnum(q)}\%\) of C.", r"A is \(\frac{x}{y}\times 100\%\) of B.",
          rf"\(\frac{{{pnum(p)}}}{{{pnum(q)}}}\times 100 = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{pnum(p)}}}{{{pnum(q)}}}\times 100 = {tex(v)}\% \]"
    return result(("number", v), T16, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- rule cards
def two_values_card(n, title, s, asked):
    other = "second" if asked == "first" else "first"
    word = "more" if s == "+" else "less"
    fnum, fden = ("100 + x", "100 + y") if s == "+" else ("100 - x", "100 - y")
    if asked == "second":
        fnum, fden = fden, fnum
    ex = {12: (20, 50), 13: (25, 50), 14: (30, 40), 15: (25, 40)}[n]
    a, b = (100 + ex[0], 100 + ex[1]) if s == "+" else (100 - ex[0], 100 - ex[1])
    num, den = (a, b) if asked == "first" else (b, a)
    return card(n, title,
                rf"If two values are respectively \(x\%\) and \(y\%\) {word} than a third value, then the {asked} is "
                rf"\(\frac{{{fnum}}}{{{fden}}}\times 100\%\) of the {other}.",
                rf"\[ \text{{{asked.capitalize()}}} = \frac{{{fnum}}}{{{fden}}}\times 100\%\text{{ of the {other}}} \]",
                [("Third value", "100"), ("First value", f"100 {s} x"), ("Second value", f"100 {s} y"),
                 (f"{asked.capitalize()} as % of {other}", rf"\frac{{{fnum}}}{{{fden}}}\times 100")],
                rf"Both values are measured from the same third value, so taking it as 100 turns each percentage into an actual value "
                rf"and the comparison is a simple division.",
                rf"'Two numbers are \(x\%\) and \(y\%\) {word} than a third. What percentage is the {asked} of the {other}?'",
                rf"\(x = {ex[0]}\), \(y = {ex[1]}\): \(\frac{{{num}}}{{{den}}}\times 100 = {tex(F(num * 100, den))}\%\).",
                rf"Putting the two values the wrong way up: the value asked about ('the {asked}') goes on top. When the question asks "
                rf"'how much per cent less', subtract the answer from 100.")


CARDS = {
    9: card(9, "Original Daily Wage after an Increase",
            r"When a daily wage is increased by a given per cent and the new wage is known, the original wage is the new wage "
            r"divided by \(100 + \%\) increase, times 100.",
            r"\[ \text{Original daily wage} = \frac{\text{Increased daily wage}}{100 + \%\text{ increase}}\times 100 \]",
            [("Original wage", "100"), ("Increase", "x"), ("Increased wage", "100 + x")],
            r"The new wage is \((100 + x)\%\) of the old one, so Rule 4 with \((100 + x)\%\) gives the old wage.",
            "A wage, price or salary is increased by x% and the NEW value is given; the value before the increase is asked.",
            r"Increase \(20\%\), new wage Rs 24: \(\frac{24}{120}\times 100 =\) Rs 20.",
            r"Taking \(x\%\) of the NEW wage and subtracting it (Rs 24 \(-\) 20% of 24 \(=\) Rs 19.20 is wrong)."),
    10: card(10, "Original Daily Wage after a Decrease",
             r"When a daily wage is decreased by a given per cent and the new wage is known, the original wage is the new wage "
             r"divided by \(100 - \%\) decrease, times 100.",
             r"\[ \text{Original daily wage} = \frac{\text{Decreased daily wage}}{100 - \%\text{ decrease}}\times 100 \]",
             [("Original wage", "100"), ("Decrease", "x"), ("Decreased wage", "100 - x")],
             r"The new wage is \((100 - x)\%\) of the old one, so Rule 4 with \((100 - x)\%\) gives the old wage.",
             "A wage, price or salary is decreased by x% and the NEW value is given; the value before the decrease is asked.",
             r"Decrease \(15\%\), new wage Rs 17: \(\frac{17}{85}\times 100 =\) Rs 20.",
             r"Adding \(x\%\) of the NEW wage back (Rs 17 \(+\) 15% of 17 is not the original wage)."),
    11: card(11, "Working Hours to Restore Production",
             r"Production \(=\) Manpower \(\times\) Working hours. If the production falls by \(x\%\) because the manpower falls by \(x\%\), "
             r"the working hours must be increased by \(\frac{x}{100 - x}\times 100\%\) to restore it.",
             r"\[ \text{Increase in working hours} = \frac{x}{100 - x}\times 100\% \]",
             [("Manpower", r"100 \to 100 - x"), ("Working hours", r"100 \to 100 + y"), ("Production kept the same", r"(100 - x)(100 + y) = 100\times 100")],
             r"Production is a product of two factors: when one factor shrinks to \((100 - x)\%\), the other must grow to \(\frac{100}{100 - x}\) times itself.",
             "Production (or any product of two factors) drops by x% because one factor drops; by what per cent must the other factor rise to restore it?",
             r"Fall \(25\%\): \(\frac{25}{75}\times 100 = 33\frac{1}{3}\%\).",
             r"Answering \(x\%\) itself: a \(25\%\) fall is undone by a \(33\frac{1}{3}\%\) rise, not a \(25\%\) rise."),
    12: two_values_card(12, "Two Values More than a Third: First as % of Second", "+", "first"),
    13: two_values_card(13, "Two Values More than a Third: Second as % of First", "+", "second"),
    14: two_values_card(14, "Two Values Less than a Third: Second as % of First", "-", "second"),
    15: two_values_card(15, "Two Values Less than a Third: First as % of Second", "-", "first"),
    16: card(16, "Two Percentages of the Same Third Value",
             r"If A is \(x\%\) of C and B is \(y\%\) of C, then A is \(\frac{x}{y}\times 100\%\) of B.",
             r"\[ \text{A} = \frac{x}{y}\times 100\%\text{ of B} \]",
             [("C", "100"), ("A", "x"), ("B", "y"), ("A as % of B", r"\frac{x}{y}\times 100")],
             r"C is common to both, so it cancels: \(\frac{A}{B} = \frac{xC/100}{yC/100} = \frac{x}{y}\).",
             "'Two numbers are x% and y% OF a third number. What percentage is the first of the second?' (Put the number asked about on top.)",
             r"\(20\%\) and \(25\%\) of a third: the first is \(\frac{20}{25}\times 100 = 80\%\) of the second.",
             r"Using \(100 + x\) and \(100 + y\) here: the numbers are x% OF the third, not x% MORE than it."),
}

TWO = "Two numbers are respectively"
OLD = {
    9: {597: (lambda: wage(20, 24, True), "The daily wage is increased by 20% and a person now gets Rs 24 per day. What was his daily wage before the increase?", None)},
    10: {598: (lambda: wage(15, 17, False), "The daily wage is decreased by 15% and a person now gets Rs 17 per day. What was his daily wage before the decrease?", None)},
    11: {599: (lambda: hours(25), "Due to a fall in manpower, the production in a factory decreases by 25%. By what per cent should the working hours be "
                                  "increased to restore the original production?",
               {"a": P(F(1, 33)), "b": P(F(100, 3)), "c": P(25), "d": P(F(3, 100))})},
    12: {600: (lambda: rel(12, 20, 50), f"{TWO} 20% and 50% more than a third. What percentage is the first of the second?",
               {"a": P(60), "b": P(100), "c": P(30), "d": P(80)})},
    13: {601: (lambda: rel(13, 25, 50), f"{TWO} 25% and 50% more than a third. What percentage is the second of the first?",
               {"a": P(60), "b": P(120), "c": P(30), "d": P(80)})},
    14: {602: (lambda: rel(14, 30, 40), f"{TWO} 30% and 40% less than a third number. What per cent is the second of the first?",
               {"a": P(F(600, 7)), "b": P(F(700, 6)), "c": P(75), "d": P(F(180, 7))})},
    15: {603: (lambda: rel(15, 25, 40), f"{TWO} 25% and 40% less than a third number. What per cent is the first of the second?",
               {"a": P(100), "b": P(200), "c": P(125), "d": P(130)})},
    16: {604: (lambda: of_third(20, 25), f"{TWO} 20% and 25% of a third number. What percentage is the first of the second?",
               {"a": P(12), "b": P(60), "c": P(30), "d": P(80)})},
}

NEW = {
    9: [("r9_e1", "A worker's daily wage goes up by 40% and he now earns Rs 35 a day. What was his daily wage before the rise?",
         lambda: wage(40, 35, True), [Rsx(21), Rsx(25), Rsx(28), Rsx(30)], 2),
        ("r9_e2", "After an increase of 12%, a labourer's daily wage is Rs 21. What was the daily wage before the increase?",
         lambda: wage(12, 21, True), [Rsx(F(37, 2)), Rsx(19), Rsx(F(73, 4)), Rsx(F(75, 4))], 4),
        ("r9_e3", "The daily wage of a carpenter is raised by 24% and he now gets Rs 186 per day. What was his daily wage before the raise?",
         lambda: wage(24, 186, True), [Rsx(150), Rsx(155), Rsx(162), Rsx(145)], 1),
        ("r9_e4", "A daily wage is increased by 60%, and the new wage is Rs 48 per day. Find the daily wage before the increase.",
         lambda: wage(60, 48, True), [Rsx(28), Rsx(32), Rsx(30), Rsx(36)], 3),
        ("r9_e5", "The daily wage of a driver rises by 50% to Rs 325 per day. What was it before the rise?",
         lambda: wage(50, 325, True), [Rsx(F(325, 2)), Rsx(F(650, 3)), Rsx(225), Rsx(F(425, 2))], 2)],
    10: [("r10_e1", "A worker's daily wage is cut by 25% and he now gets Rs 18 per day. What was his daily wage before the cut?",
          lambda: wage(25, 18, False), [Rsx(24), Rsx(22), Rsx(23), Rsx(27)], 1),
         ("r10_e2", "The daily wage is reduced by 16% and a person now gets Rs 42 per day. What was the daily wage before the reduction?",
          lambda: wage(16, 42, False), [Rsx(48), Rsx(58), Rsx(50), Rsx(52)], 3),
         ("r10_e3", "A daily wage falls by 28% to Rs 30 per day. What was the daily wage before the fall?",
          lambda: wage(28, 30, False), [Rsx(F(115, 3)), Rsx(F(124, 3)), Rsx(40), Rsx(F(125, 3))], 4),
         ("r10_e4", "After a decrease of 14%, a man's daily wage is Rs 43. What was his daily wage before the decrease?",
          lambda: wage(14, 43, False), [Rsx(49), Rsx(50), Rsx(57), Rsx(45)], 2),
         ("r10_e5", "The daily wage of a helper is lowered by 5% and he now receives Rs 38 per day. What did he receive per day before?",
          lambda: wage(5, 38, False), [Rsx(42), Rsx(36), Rsx(40), Rsx(F(399, 10))], 3)],
    11: [("r11_e1", "Because of a fall in manpower, the production in a factory goes down by 28%. By what per cent must the working hours be "
                    "increased to bring the production back to its original level?", lambda: hours(28),
          [P(F(350, 9)), P(28), P(F(353, 9)), P(F(325, 9))], 1),
         ("r11_e2", "The production in a factory falls by 50% because half the workers leave. By what per cent should the working hours be "
                    "increased to restore the original production?", lambda: hours(50), [P(50), P(100), P(75), P(150)], 2),
         ("r11_e3", "Due to fewer workers, a factory's production decreases by 60%. By what per cent should the working hours be increased "
                    "to restore the original production?", lambda: hours(60), [P(60), P(120), P(150), P(F(500, 3))], 3),
         ("r11_e4", "A drop in manpower reduces the production in a factory by 44%. By what per cent should the working hours be increased "
                    "to get the original production back?", lambda: hours(44), [P(44), P(F(536, 7)), P(F(570, 7)), P(F(550, 7))], 4),
         ("r11_e5", "With fewer men at work, the production in a factory decreases by 15%. By what per cent should the working hours be "
                    "increased to restore the original production?", lambda: hours(15), [P(15), P(F(300, 17)), P(F(292, 17)), P(F(308, 17))], 2)],
    12: [("r12_e1", f"{TWO} 35% and 10% more than a third. What percentage is the first of the second?", lambda: rel(12, 35, 10),
          [P(F(1350, 11)), P(125), P(F(2200, 27)), P(F(1345, 11))], 1),
         ("r12_e2", "Two numbers are 30% and 50% more than a third number. What percentage is the first of the second?", lambda: rel(12, 30, 50),
          [P(F(1500, 13)), P(60), P(F(260, 3)), P(80)], 3),
         ("r12_e3", f"{TWO} 12% and 40% more than a third. What percentage is the first of the second?", lambda: rel(12, 12, 40),
          [P(125), P(80), P(30), P(72)], 2),
         ("r12_e4", f"{TWO} 44% and 60% more than a third. What percentage is the first of the second?", lambda: rel(12, 44, 60),
          [P(F(1000, 9)), P(F(220, 3)), P(85), P(90)], 4),
         ("r12_e5", f"{TWO} 32% and 10% more than a third. What percentage is the first of the second?", lambda: rel(12, 32, 10),
          [P(F(250, 3)), P(122), P(120), P(132)], 3)],
    13: [("r13_e1", f"{TWO} 60% and 28% more than a third. What percentage is the second of the first?", lambda: rel(13, 60, 28),
          [P(80), P(125), P(F(140, 3)), P(78)], 1),
         ("r13_e2", f"{TWO} 50% and 35% more than a third. What percentage is the second of the first?", lambda: rel(13, 50, 35),
          [P(F(1000, 9)), P(90), P(70), P(85)], 2),
         ("r13_e3", f"{TWO} 15% and 38% more than a third. What percentage is the second of the first?", lambda: rel(13, 15, 38),
          [P(F(250, 3)), P(123), P(120), P(115)], 3),
         ("r13_e4", f"{TWO} 44% and 8% more than a third. What percentage is the second of the first?", lambda: rel(13, 44, 8),
          [P(72), P(F(400, 3)), P(80), P(75)], 4)],
    14: [("r14_e1", f"{TWO} 12% and 18% less than a third number. What per cent is the second of the first?", lambda: rel(14, 12, 18),
          [P(F(1025, 11)), P(F(4400, 41)), P(F(1040, 11)), P(F(200, 3))], 1),
         ("r14_e2", f"{TWO} 20% and 36% less than a third number. What per cent is the second of the first?", lambda: rel(14, 20, 36),
          [P(125), P(84), P(80), P(F(500, 9))], 3),
         ("r14_e3", "Two numbers are 20 and 28 per cent less than a third number. By how much per cent is the second number less than the first?",
          lambda: rel(14, 20, 28, True), [P(8), P(10), P(90), P(F(100, 9))], 2),
         ("r14_e4", "Two numbers are 25 and 40 per cent less than a third number. By how much per cent is the second number less than the first?",
          lambda: rel(14, 25, 40, True), [P(15), P(25), P(80), P(20)], 4)],
    15: [("r15_e1", f"{TWO} 22% and 12% less than a third number. What per cent is the first of the second?", lambda: rel(15, 22, 12),
          [P(F(4400, 39)), P(F(975, 11)), P(F(960, 11)), P(90)], 2),
         ("r15_e2", f"{TWO} 46% and 40% less than a third number. What per cent is the first of the second?", lambda: rel(15, 46, 40),
          [P(90), P(F(1000, 9)), P(85), P(115)], 1),
         ("r15_e3", f"{TWO} 36% and 20% less than a third number. What per cent is the first of the second?", lambda: rel(15, 36, 20),
          [P(125), P(56), P(84), P(80)], 4),
         ("r15_e4", f"{TWO} 45% and 34% less than a third number. By how much per cent is the first number less than the second?",
          lambda: rel(15, 45, 34, True), [P(11), P(F(250, 3)), P(F(50, 3)), P(20)], 3)],
    16: [("r16_e1", f"{TWO} 12% and 30% of a third number. What percentage is the first of the second?", lambda: of_third(12, 30),
          [P(40), P(250), P(18), P(60)], 1),
         ("r16_e2", f"{TWO} 6% and 48% of a third number. What percentage is the first of the second?", lambda: of_third(6, 48),
          [P(800), P(F(25, 2)), P(42), P(8)], 2),
         ("r16_e3", f"{TWO} 21% and 56% of a third number. What percentage is the first of the second?", lambda: of_third(21, 56),
          [P(F(800, 3)), P(35), P(F(75, 2)), P(F(125, 2))], 3),
         ("r16_e4", f"{TWO} 27% and 45% of a third number. What percentage is the first of the second?", lambda: of_third(27, 45),
          [P(F(500, 3)), P(18), P(72), P(60)], 4),
         ("r16_e5", f"{TWO} 32% and 40% of a third number. What percentage is the second of the first?", lambda: of_third(32, 40, True),
          [P(80), P(125), P(108), P(120)], 2)],
}


def main():
    for n in range(9, 17):
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
