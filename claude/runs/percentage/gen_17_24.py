"""Rules 17-24: writes the eight rule cards, regenerates the old worked-example rows 605-612 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their text and
fixes 606 (no option held Rs 576), and adds the book exercises of these rules (numbers changed, wording rewritten)
as one JsonImport payload per rule. Same output files as gen_1_8.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, money, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import Num, pnum, result  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402


def dec(v):
    """Exact two-place decimals as decimals (36.40, 145.60), anything else as a mixed number."""
    v = F(v)
    return money(v) if (v * 100).denominator == 1 else tex(v)


def metres(v):
    return rf"\({tex(F(v))}\) m"


def prod_tex(factors):
    """[(100, '-', 20), (100, '-', 'y')] -> (100 - 20)(100 - y)"""
    return "".join(rf"(100 {s} {p if isinstance(p, str) else pnum(p)})" for _, s, p in factors)


def hundreds(k):
    return r"\times ".join(["100"] * k)


# ---------------------------------------------------------------- Rules 17 and 18: successive shares taken (of the remaining)
T17 = (r"If \(x\%\) of a quantity is taken by the first, \(y\%\) of the remaining by the second and \(z\%\) of the remaining by the third, "
       r"and \(A\) is left, then the quantity in the beginning was<br>\[ \frac{A\times 100\times 100\times 100}{(100 - x)(100 - y)(100 - z)} \]"
       r"(use as many brackets as there are steps).")
T18 = (r"If the initial quantity is \(A\) and \(x\%\) of it is taken by the first, \(y\%\) of the remaining by the second and \(z\%\) of the "
       r"remaining by the third, then the quantity left is<br>\[ \frac{A\times (100 - x)(100 - y)(100 - z)}{100\times 100\times 100} \]"
       r"(use as many brackets as there are steps).")
# ---------------------------------------------------------------- Rules 19 and 20: successive additions (of the increased amount)
T19 = (r"If \(x\%\) of a quantity is added, then \(y\%\) of the increased quantity is added, then \(z\%\) of the increased quantity is added, "
       r"and it becomes \(A\), then the initial amount is<br>\[ \frac{A\times 100\times 100\times 100}{(100 + x)(100 + y)(100 + z)} \]"
       r"(use as many brackets as there are steps).")
T20 = (r"If the initial quantity is \(A\) and \(x\%\) of it is added, then \(y\%\) of the increased quantity is added, then \(z\%\) of the "
       r"increased quantity is added, the quantity becomes<br>\[ \frac{A\times (100 + x)(100 + y)(100 + z)}{100\times 100\times 100} \]"
       r"(use as many brackets as there are steps).")


def forward(A, pcts_, sign, theorem, fmt, words):
    """A changes by each p% in turn (sign '-' takes p% of what is there, '+' adds it). words = one phrase per step."""
    A = F(A)
    rows, cur = [], A
    for p, w in zip(pcts_, words):
        ch = cur * F(p) / 100
        new = cur - ch if sign == "-" else cur + ch
        rows.append(rf"{w}: \({pnum(p)}\%\) of \({dec(cur)} = {dec(ch)}\), so \({dec(cur)} {sign} {dec(ch)} = {dec(new)}\)")
        cur = new
    factors = [(100, sign, F(p)) for p in pcts_]
    k = len(pcts_)
    trad = steps(("Follow the amount step by step.", "<br>".join(rows)),
                 ("Read off the result.", rf"The amount at the end is \({dec(cur)}\)."))
    rule = steps(
        ("Identify the values.", rf"\(A = {dec(A)}\), " + ", ".join(rf"\({pnum(p)}\%\)" for p in pcts_) + "."),
        ("Apply the specified rule.", rf"\[ \frac{{A\times {prod_tex([(100, sign, v) for v in ('x', 'y', 'z')[:k]])}}}{{{hundreds(k)}}} \]"),
        ("Substitute the values.", rf"\[ \frac{{{dec(A)}\times {prod_tex(factors)}}}{{{hundreds(k)}}} = {dec(cur)} \]"))
    rb = [rf"\(A = {dec(A)}\); steps " + ", ".join(rf"\({pnum(p)}\%\)" for p in pcts_) + ".",
          rf"Result \(= \frac{{A\times {prod_tex(factors)}}}{{{hundreds(k)}}}\).", rf"\(= {dec(cur)}\)."]
    sc = rf"\[ \frac{{{dec(A)}\times {prod_tex(factors)}}}{{{hundreds(k)}}} = {dec(cur)} \]"
    return result(("number", cur), theorem, trad, rule, fmt(cur), rb, sc)


def backward(final, pcts_, sign, theorem, fmt, start_name="the amount at first", note=""):
    """The amount after changing by each p% in turn is `final`; find the starting amount."""
    final = F(final)
    k = len(pcts_)
    factors = [(100, sign, F(p)) for p in pcts_]
    start = final
    for p in pcts_:
        start = start * 100 / (100 - F(p) if sign == "-" else 100 + F(p))
    rows, cur = [], final
    for i in range(k - 1, -1, -1):
        p = F(pcts_[i])
        keep = 100 - p if sign == "-" else 100 + p
        before = cur * 100 / keep
        what = "is left after" if sign == "-" else "is reached after"
        rows.append(rf"\({dec(cur)}\) {what} step {i + 1}, so it is \({pnum(keep)}\%\) of the amount before that step: "
                    rf"\(\frac{{{dec(cur)}\times 100}}{{{pnum(keep)}}} = {dec(before)}\)")
        cur = before
    trad = steps(("Work backwards one step at a time.", "<br>".join(rows)),
                 ("Read off the start.", rf"So {start_name} was \({dec(start)}\)."))
    rule = steps(
        ("Identify the values.", note + rf"\(A = {dec(final)}\), " + ", ".join(rf"\({pnum(p)}\%\)" for p in pcts_) + "."),
        ("Apply the specified rule.", rf"\[ \frac{{A\times {hundreds(k)}}}{{{prod_tex([(100, sign, v) for v in ('x', 'y', 'z')[:k]])}}} \]"),
        ("Substitute the values.", rf"\[ \frac{{{dec(final)}\times {hundreds(k)}}}{{{prod_tex(factors)}}} = {dec(start)} \]"))
    rb = [rf"\(A = {dec(final)}\); steps " + ", ".join(rf"\({pnum(p)}\%\)" for p in pcts_) + ".",
          rf"Start \(= \frac{{A\times {hundreds(k)}}}{{{prod_tex(factors)}}}\).", rf"\(= {dec(start)}\)."]
    sc = rf"\[ \frac{{{dec(final)}\times {hundreds(k)}}}{{{prod_tex(factors)}}} = {dec(start)} \]"
    return result(("number", start), theorem, trad, rule, fmt(start), rb, sc)


# ---------------------------------------------------------------- Rules 21-24: population formulas I-IV
T21 = r"If the original population of a town is \(P\) and the annual increase is \(r\%\), then the population in \(n\) years is<br>\[ P\left(1 + \frac{r}{100}\right)^n \]"
T22 = r"If the annual increase in the population of a town is \(r\%\) and the present population is \(P_n\), then the population \(n\) years ago was<br>\[ \frac{P_n}{\left(1 + \frac{r}{100}\right)^n} \]"
T23 = r"If the original population of a town is \(P\) and the annual decrease is \(r\%\), then the population in \(n\) years will be<br>\[ P\left(1 - \frac{r}{100}\right)^n \]"
T24 = r"If the annual decrease in the population of a town is \(r\%\) and the present population is \(P_n\), then the population \(n\) years ago was<br>\[ \frac{P_n}{\left(1 - \frac{r}{100}\right)^n} \]"


def population(P, r, n, sign, past, fmt=Num, thing="population"):
    P, r = F(P), F(r)
    f = (100 + r if sign == "+" else 100 - r) / 100
    T = {("+", False): T21, ("+", True): T22, ("-", False): T23, ("-", True): T24}[(sign, past)]
    ans = P / f ** n if past else P * f ** n
    word = "increase" if sign == "+" else "decrease"
    if past:
        rows, cur = [], P
        for i in range(n):
            before = cur / f
            rows.append(rf"\({tex(cur)}\) is \({pnum(100 * f)}\%\) of the {thing} a year earlier: \(\frac{{{tex(cur)}\times 100}}{{{pnum(100 * f)}}} = {tex(before)}\)")
            cur = before
        trad = steps(("Each year multiplies the " + thing + " by " + rf"\(\frac{{{pnum(100 * f)}}}{{100}}\).",
                      rf"An annual {word} of \({pnum(r)}\%\) makes each year's {thing} \({pnum(100 * f)}\%\) of the year before."),
                     ("Go back one year at a time.", "<br>".join(rows)))
    else:
        rows, cur = [], P
        for i in range(n):
            ch = cur * r / 100
            new = cur + ch if sign == "+" else cur - ch
            rows.append(rf"Year {i + 1}: \({tex(cur)} {sign} \frac{{{pnum(r)}}}{{100}}\times {tex(cur)} = {tex(cur)} {sign} {tex(ch)} = {tex(new)}\)")
            cur = new
        trad = steps(("Work out the change one year at a time.", rf"Each year's {word} is \({pnum(r)}\%\) of that year's {thing}."),
                     ("Year by year.", "<br>".join(rows)))
    s = sign
    sym = rf"\left(1 {s} \frac{{r}}{{100}}\right)^n"
    num = rf"\left(1 {s} \frac{{{pnum(r)}}}{{100}}\right)^{{{n}}}"
    frac_f = rf"\left(\frac{{{pnum(100 * f)}}}{{100}}\right)^{{{n}}}"
    if past:
        formula, subst = rf"\frac{{P_n}}{{{sym}}}", rf"\frac{{{tex(P)}}}{{{num}}} = \frac{{{tex(P)}}}{{{frac_f}}} = {tex(ans)}"
    else:
        formula, subst = rf"P{sym}", rf"{tex(P)}{num} = {tex(P)}\times {frac_f} = {tex(ans)}"
    rule = steps(
        ("Identify the values.", rf"\({'P_n' if past else 'P'} = {tex(P)}\), \(r = {pnum(r)}\), \(n = {n}\)."),
        ("Apply the specified rule.", rf"\[ {formula} \]"),
        ("Substitute the values.", rf"\[ {subst} \]"))
    rb = [rf"\({'P_n' if past else 'P'} = {tex(P)}\), \(r = {pnum(r)}\), \(n = {n}\).", rf"\({formula}\).", rf"\({subst}\)."]
    sc = rf"\[ {subst} \]"
    return result(("number", ans), T, trad, rule, fmt(ans), rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    17: card(17, "Starting Amount when Shares Are Taken from What Remains",
             r"\(x\%\) of a quantity is taken by the first, \(y\%\) of the remaining by the second and \(z\%\) of the remaining by the third. "
             r"If \(A\) is left, the quantity at the beginning was \(\frac{A\times 100\times 100\times 100}{(100 - x)(100 - y)(100 - z)}\).",
             r"\[ \text{Initial quantity} = \frac{A\times 100\times 100\times 100}{(100 - x)(100 - y)(100 - z)} \]",
             [("After the first", r"\frac{100 - x}{100}\text{ of it is left}"), ("After the second", r"\frac{100 - y}{100}\text{ of that is left}"),
              ("Left at the end", r"A")],
             r"Each step keeps a fixed fraction of what was there, so the amount left is the start times all those fractions; dividing by them gives the start back.",
             "Money lost, spent, given away (or wire stolen, used) one after another, each 'of the remainder', and the amount LEFT is given; the starting amount is asked.",
             r"Loses \(12\frac{1}{2}\%\), spends \(70\%\) of the rest, left with Rs 210: \(\frac{210\times 100\times 100}{87\frac{1}{2}\times 30} =\) Rs 800.",
             r"Adding the percentages (\(12\frac{1}{2} + 70\)) - every later percentage is of the REMAINDER, not of the original amount."),
    18: card(18, "Amount Left when Shares Are Taken from What Remains",
             r"If the initial quantity is \(A\) and \(x\%\) of it is taken by the first, \(y\%\) of the remaining by the second and \(z\%\) of the "
             r"remaining by the third, then \(\frac{A(100 - x)(100 - y)(100 - z)}{100\times 100\times 100}\) is left.",
             r"\[ \text{Left} = \frac{A\times (100 - x)(100 - y)(100 - z)}{100\times 100\times 100} \]",
             [("Start", "A"), ("After the first", r"A\times\frac{100 - x}{100}"), ("After the second", r"A\times\frac{100 - x}{100}\times\frac{100 - y}{100}")],
             r"Each share leaves \((100 - p)\%\) of what was there, so the fractions multiply.",
             "The starting amount is given, shares are taken one after another 'of the remaining', and the amount LEFT is asked.",
             r"Rs 1200, \(20\%\) then \(40\%\) of the rest: \(\frac{1200\times 80\times 60}{100\times 100} =\) Rs 576.",
             r"Subtracting \(20\% + 40\% = 60\%\) of Rs 1200 (gives Rs 480, which is wrong)."),
    19: card(19, "Starting Amount after Successive Additions",
             r"\(x\%\) of a quantity is added, then \(y\%\) of the increased quantity, then \(z\%\) of the increased quantity. If it becomes \(A\), "
             r"the initial amount is \(\frac{A\times 100\times 100\times 100}{(100 + x)(100 + y)(100 + z)}\).",
             r"\[ \text{Initial amount} = \frac{A\times 100\times 100\times 100}{(100 + x)(100 + y)(100 + z)} \]",
             [("After the first addition", r"\frac{100 + x}{100}\text{ times}"), ("After the second", r"\frac{100 + y}{100}\text{ times that}"), ("Final", "A")],
             r"Each addition multiplies the amount by \(\frac{100 + p}{100}\); divide the final amount by all these factors to get the start.",
             "Money is added (deposited) in steps, each a percentage of the INCREASED amount, and the final amount is given; the initial amount is asked.",
             r"Add \(50\%\), then \(20\%\) of the new amount, final Rs 18000: \(\frac{18000\times 100\times 100}{150\times 120} =\) Rs 10000.",
             r"Taking \(50\% + 20\% = 70\%\) and dividing by 170."),
    20: card(20, "Final Amount after Successive Additions",
             r"If the initial quantity is \(A\) and \(x\%\) of it is added, then \(y\%\) of the increased quantity, then \(z\%\) of the increased "
             r"quantity, it becomes \(\frac{A(100 + x)(100 + y)(100 + z)}{100\times 100\times 100}\).",
             r"\[ \text{Final amount} = \frac{A\times (100 + x)(100 + y)(100 + z)}{100\times 100\times 100} \]",
             [("Start", "A"), ("After the first addition", r"A\times\frac{100 + x}{100}"), ("After the second", r"A\times\frac{100 + x}{100}\times\frac{100 + y}{100}")],
             r"Each addition is on the amount already there, so the growth factors multiply (like compound interest).",
             "The starting amount and the percentages added each year (or step) are given; the amount at the end is asked.",
             r"Rs 4800, add \(20\%\) then \(25\%\): \(\frac{4800\times 120\times 125}{100\times 100} =\) Rs 7200.",
             r"Adding \(20\% + 25\% = 45\%\) of Rs 4800 (gives Rs 6960, which is wrong)."),
    21: card(21, "Population Formula I: Future Population (Increase)",
             r"If the original population of a town is \(P\) and the annual increase is \(r\%\), then the population in \(n\) years is \(P\left(1 + \frac{r}{100}\right)^n\).",
             r"\[ \text{Population after } n \text{ years} = P\left(1 + \frac{r}{100}\right)^n \]",
             [("Now", "P"), ("After 1 year", r"P\left(1 + \frac{r}{100}\right)"), ("After n years", r"P\left(1 + \frac{r}{100}\right)^n")],
             r"Each year's increase is on that year's population, so the factor \(1 + \frac{r}{100}\) is applied once per year.",
             "Population (or income, sales, value) grows by r% every year; the value after n years is asked.",
             r"\(15625\), \(4\%\), 3 years: \(15625\times\frac{26}{25}\times\frac{26}{25}\times\frac{26}{25} = 17576\).",
             r"Adding \(n\times r\%\) (simple growth) instead of multiplying by the factor each year."),
    22: card(22, "Population Formula II: Past Population (Increase)",
             r"If the annual increase in the population of a town is \(r\%\) and the present population is \(P_n\), then the population \(n\) years ago was "
             r"\(\frac{P_n}{\left(1 + \frac{r}{100}\right)^n}\).",
             r"\[ \text{Population } n \text{ years ago} = \frac{P_n}{\left(1 + \frac{r}{100}\right)^n} \]",
             [("Now", "P_n"), ("1 year ago", r"\frac{P_n}{1 + \frac{r}{100}}"), ("n years ago", r"\frac{P_n}{\left(1 + \frac{r}{100}\right)^n}")],
             r"Going back a year undoes one growth factor, so divide by it once per year.",
             "The present population (or income) and the yearly growth rate are given; the value some years AGO is asked.",
             r"\(17576\), \(4\%\), 3 years ago: \(\frac{17576\times 25\times 25\times 25}{26\times 26\times 26} = 15625\).",
             r"Subtracting \(r\%\) of the present value each year - a \(4\%\) rise is undone by dividing by \(1.04\), not by taking off \(4\%\)."),
    23: card(23, "Population Formula III: Future Population (Decrease)",
             r"If the original population of a town is \(P\) and the annual decrease is \(r\%\), then the population in \(n\) years will be \(P\left(1 - \frac{r}{100}\right)^n\).",
             r"\[ \text{Population after } n \text{ years} = P\left(1 - \frac{r}{100}\right)^n \]",
             [("Now", "P"), ("After 1 year", r"P\left(1 - \frac{r}{100}\right)"), ("After n years", r"P\left(1 - \frac{r}{100}\right)^n")],
             r"Each year's fall is on that year's population, so the factor \(1 - \frac{r}{100}\) is applied once per year.",
             "Population (or the value of a machine) falls by r% every year; the value after n years is asked.",
             r"\(40000\), \(5\%\), 2 years: \(40000\times\frac{19}{20}\times\frac{19}{20} = 36100\).",
             r"Subtracting \(n\times r\%\) of the original population."),
    24: card(24, "Population Formula IV: Past Population (Decrease)",
             r"If the annual decrease in the population of a town is \(r\%\) and the present population is \(P_n\), then the population \(n\) years ago was "
             r"\(\frac{P_n}{\left(1 - \frac{r}{100}\right)^n}\).",
             r"\[ \text{Population } n \text{ years ago} = \frac{P_n}{\left(1 - \frac{r}{100}\right)^n} \]",
             [("Now", "P_n"), ("1 year ago", r"\frac{P_n}{1 - \frac{r}{100}}"), ("n years ago", r"\frac{P_n}{\left(1 - \frac{r}{100}\right)^n}")],
             r"Going back a year undoes one fall, so divide by \(1 - \frac{r}{100}\) once per year.",
             "The present population and the yearly rate of DECREASE are given; the population some years ago is asked.",
             r"\(57600\), \(4\%\), 2 years ago: \(\frac{57600\times 25\times 25}{24\times 24} = 62500\).",
             r"Adding \(r\%\) of the present population back each year - divide by \(\frac{100 - r}{100}\) instead."),
}

LOSS = ["first step", "second step", "third step"]
OLD = {
    17: {605: (lambda: backward(210, [F(25, 2), 70], "-", T17, Rsx, "his money at first"),
               r"A man loses \(12\frac{1}{2}\%\) of his money and, after spending 70% of the remainder, he is left with Rs 210. How much had he at first?", None)},
    18: {606: (lambda: forward(1200, [20, 40], "-", T18, Rsx, ["Pankaj takes", "Chandan takes"]),
               "Pankaj and Chandan deposit Rs 1200 in a common fund. 20% of the initial amount is taken by Pankaj and 40% of the remaining amount "
               "is taken by Chandan. How much is left in the common fund?",
               {"a": Rsx(480), "b": Rsx(576), "c": Rsx(624), "d": Rsx(720)})},
    19: {607: (lambda: backward(18000, [50, 20], "+", T19, Rsx, "the initial amount"),
               "A man deposited 50% of the initial amount in his locker. After some time he again deposited 20% of the increased amount. "
               "Now the amount is Rs 18000. What was the initial amount?",
               {"a": Rsx(100), "b": Rsx(30000), "c": Rsx(10000), "d": Rsx(12000)})},
    20: {608: (lambda: forward(4800, [20, 25], "+", T20, Rsx, ["First year", "Second year"]),
               "A man had Rs 4800 in his locker two years ago. In the first year he deposited 20% of the amount in his locker. In the second year "
               "he deposited 25% of the increased amount in his locker. Find the amount at present in his locker.", None)},
    21: {609: (lambda: population(15625, 4, 3, "+", False), "If the annual increase in the population of a town is 4% and the present number of "
                                                            "people is 15625, what will the population be in 3 years?", None)},
    22: {610: (lambda: population(17576, 4, 3, "+", True), "If the annual increase in the population of a town is 4% and the present population "
                                                           "is 17576, what was it three years ago?", None)},
    23: {611: (lambda: population(40000, 5, 2, "-", False), "If the annual decrease in the population of a town is 5% and the present number of "
                                                            "people is 40000, what will the population be in 2 years?", None)},
    24: {612: (lambda: population(57600, 4, 2, "-", True), "If the annual decrease in the population of a town is 4% and the present population "
                                                           "is 57600, what was it two years ago?", None)},
}

NEW = {
    17: [("r17_e1", "A builder buys some cable. 20% of it is stolen, and he uses 75% of what remains. He is left with 36 m 40 cm of cable. "
                    "How much cable did he buy?", lambda: backward(F(364, 10), [20, 75], "-", T17, metres, "the cable bought (in metres)", "36 m 40 cm = 36.40 m. "),
          [metres(172), metres(182), metres(190), metres(160)], 2),
         ("r17_e2", "A woman spends 40% of her income on food, 25% of the remainder on rent and 20% of what is then left on her children's "
                    "education. She saves the remaining Rs 5400. What is her income?",
          lambda: backward(5400, [40, 25, 20], "-", T17, Rsx, "her income"), [Rsx(15000), Rsx(13500), Rsx(18000), Rsx(16000)], 1),
         ("r17_e3", "A man loses 20% of his money and then spends 65% of the remainder. He is left with Rs 840. How much had he at first?",
          lambda: backward(840, [20, 65], "-", T17, Rsx, "his money at first"), [Rsx(2800), Rsx(3200), Rsx(2400), Rsx(3000)], 4),
         ("r17_e4", "A man loses 12% of his money and, after spending 45% of the remainder, has Rs 2178 left. How much had he at first?",
          lambda: backward(2178, [12, 45], "-", T17, Rsx, "his money at first"), [Rsx(4000), Rsx(4800), Rsx(4500), Rsx(5000)], 3)],
    18: [("r18_e1", "A man earns Rs 36000. He spends 25% of it on board and lodging, 20% of the remainder on other needs and 10% of the rest "
                    "in charity. How much is left with him in the end?",
          lambda: forward(36000, [25, 20, 10], "-", T18, Rsx, ["Board and lodging", "Other needs", "Charity"]),
          [Rsx(18440), Rsx(19440), Rsx(16200), Rsx(19940)], 2),
         ("r18_e2", "A man's income is Rs 24000. He spends 15% of it on board and lodging, 20% of the remainder on other necessities and 5% of "
                    "the rest in charity. Find the amount left with him at the end.",
          lambda: forward(24000, [15, 20, 5], "-", T18, Rsx, ["Board and lodging", "Necessities", "Charity"]),
          [Rsx(15054), Rsx(14504), Rsx(15504), Rsx(16320)], 3),
         ("r18_e3", "Out of an income of Rs 18000, a man spends 35% on board and lodging, 40% of the remainder on other necessities and 25% of "
                    "the rest in charity. How much does he have left at the end?",
          lambda: forward(18000, [35, 40, 25], "-", T18, Rsx, ["Board and lodging", "Necessities", "Charity"]),
          [Rsx(5265), Rsx(5625), Rsx(5256), Rsx(4265)], 1),
         ("r18_e4", "A man had Rs 4500 at first. He loses 30% of his money and then spends 60% of the remainder. How much is he left with?",
          lambda: forward(4500, [30, 60], "-", T18, Rsx, ["He loses", "He spends"]), [Rsx(1350), Rsx(1620), Rsx(1800), Rsx(1260)], 4)],
    19: [("r19_e1", "A man deposited 25% of the initial amount in his locker. Later he deposited 20% of the increased amount. Now the amount "
                    "is Rs 9000. What was the initial amount?", lambda: backward(9000, [25, 20], "+", T19, Rsx, "the initial amount"),
          [Rsx(6500), Rsx(6000), Rsx(5400), Rsx(7200)], 2),
         ("r19_e2", "A woman adds 60% of the initial amount to her savings box, and some time later adds 25% of the increased amount. The box "
                    "now holds Rs 24000. What was the initial amount?", lambda: backward(24000, [60, 25], "+", T19, Rsx, "the initial amount"),
          [Rsx(14400), Rsx(10000), Rsx(12000), Rsx(13000)], 3),
         ("r19_e3", "A man deposited 10% of the initial amount in his locker and later 30% of the increased amount. The amount is now Rs 7150. "
                    "How much was the initial amount?", lambda: backward(7150, [10, 30], "+", T19, Rsx, "the initial amount"),
          [Rsx(5000), Rsx(5500), Rsx(4500), Rsx(5200)], 1),
         ("r19_e4", "A man deposited 8% of the initial amount in his locker. After some time he deposited 25% of the increased amount. Now the "
                    "amount becomes Rs 10800. What was the initial amount?", lambda: backward(10800, [8, 25], "+", T19, Rsx, "the initial amount"),
          [Rsx(8100), Rsx(7500), Rsx(8640), Rsx(8000)], 4),
         ("r19_e5", "A man deposited 16% of the initial amount in his locker and later deposited 50% of the increased amount. Now he has "
                    "Rs 26100 in the locker. What was the initial amount?", lambda: backward(26100, [16, 50], "+", T19, Rsx, "the initial amount"),
          [Rsx(14500), Rsx(15000), Rsx(16000), Rsx(15500)], 2)],
    20: [("r20_e1", "A man had Rs 1500 in his locker two years ago. In the first year he deposited 10% of the amount in the locker, and in the "
                    "second year 30% of the increased amount. Find the amount in the locker now.",
          lambda: forward(1500, [10, 30], "+", T20, Rsx, ["First year", "Second year"]), [Rsx(2100), Rsx(2415), Rsx(2145), Rsx(2154)], 3),
         ("r20_e2", "Two years ago a woman had Rs 2000 in her locker. In the first year she added 20% of the amount, and in the second year "
                    "45% of the increased amount. How much is in the locker now?",
          lambda: forward(2000, [20, 45], "+", T20, Rsx, ["First year", "Second year"]), [Rsx(3480), Rsx(3300), Rsx(3840), Rsx(3408)], 1),
         ("r20_e3", "A man had Rs 3800 in his locker two years ago. In the first year he deposited 50% of the amount in his locker. In the "
                    "second year he deposited 20% of the increased amount. Find the amount at present in his locker.",
          lambda: forward(3800, [50, 20], "+", T20, Rsx, ["First year", "Second year"]), [Rsx(6480), Rsx(6650), Rsx(7600), Rsx(6840)], 4),
         ("r20_e4", "A man had Rs 900 in his locker two years ago. In the first year he deposited 40% of the amount, and in the second year "
                    "80% of the increased amount. Find the amount now in his locker.",
          lambda: forward(900, [40, 80], "+", T20, Rsx, ["First year", "Second year"]), [Rsx(2286), Rsx(2268), Rsx(2160), Rsx(1980)], 2)],
    21: [("r21_e1", "The population of a town is 48000. It increases by 5 per cent every year. What will it be in 2 years?",
          lambda: population(48000, 5, 2, "+", False), [Num(52800), Num(52290), Num(52920), Num(50400)], 3),
         ("r21_e2", "The population of a town is 40000 and it grows by 3 per cent annually. What will the population be in 2 years?",
          lambda: population(40000, 3, 2, "+", False), [Num(42436), Num(42400), Num(42346), Num(41200)], 1),
         ("r21_e3", "A village has 8000 people, and its population increases by 5 per cent annually. What will the population be in 3 years?",
          lambda: population(8000, 5, 3, "+", False), [Num(9200), Num(9216), Num(9621), Num(9261)], 4),
         ("r21_e4", "The population of a town is 125000. It increases by 4 per cent annually. What will it be in 3 years?",
          lambda: population(125000, 4, 3, "+", False), [Num(140000), Num(140608), Num(140806), Num(135200)], 2)],
    22: [("r22_e1", "If the annual increase in the population of a town is 3% and the present population is 53045, what was it two years ago?",
          lambda: population(53045, 3, 2, "+", True), [Num(51500), Num(49500), Num(50000), Num(48000)], 3),
         ("r22_e2", "If the annual increase in the population of a town is 5% and the present population is 19845, what was it two years ago?",
          lambda: population(19845, 5, 2, "+", True), [Num(18000), Num(18900), Num(17000), Num(18500)], 1),
         ("r22_e3", "If the annual increase in the population of a town is 10% and the present population is 13310, what was it three years ago?",
          lambda: population(13310, 10, 3, "+", True), [Num(11000), Num(9000), Num(12100), Num(10000)], 4),
         ("r22_e4", "If the annual increase in the population of a town is 20% and the present population is 25920, what was it two years ago?",
          lambda: population(25920, 20, 2, "+", True), [Num(20736), Num(18000), Num(17280), Num(21600)], 2),
         ("r22_e5", "If the annual increase in the population of a town is 20% and the present population is 86400, what was it three years ago?",
          lambda: population(86400, 20, 3, "+", True), [Num(60000), Num(48000), Num(50000), Num(72000)], 3),
         ("r22_e6", "The sales of a company grow by 25% every year. If its sales were Rs 3125000 in the year 2005, what were its sales in the year 2003?",
          lambda: population(3125000, 25, 2, "+", True, Rsx, "sales"), [Rsx(2000000), Rsx(2500000), Rsx(1875000), Rsx(1600000)], 1),
         ("r22_e7", "The population of a village grows by 10% every year. If the present population is 6050, what was it two years ago?",
          lambda: population(6050, 10, 2, "+", True), [Num(5500), Num(4840), Num(4500), Num(5000)], 4)],
    23: [("r23_e1", "If the annual decrease in the population of a town is 2% and the present number of people is 50000, what will the "
                    "population be in 2 years?", lambda: population(50000, 2, 2, "-", False), [Num(48000), Num(48020), Num(48200), Num(47020)], 2),
         ("r23_e2", "The population of a town is 25000 and it falls by 10% every year. What will the population be in 3 years?",
          lambda: population(25000, 10, 3, "-", False), [Num(18225), Num(17500), Num(18252), Num(20250)], 1),
         ("r23_e3", "If the annual decrease in the population of a town is 6% and the present number of people is 75000, what will the "
                    "population be in 2 years?", lambda: population(75000, 6, 2, "-", False), [Num(66000), Num(66720), Num(66270), Num(70500)], 3),
         ("r23_e4", "If the annual decrease in the population of a town is 20% and the present number of people is 62500, what will the "
                    "population be in 3 years?", lambda: population(62500, 20, 3, "-", False), [Num(25000), Num(40000), Num(33000), Num(32000)], 4)],
    24: [("r24_e1", "If the annual decrease in the population of a town is 10% and the present population is 72900, what was it three years ago?",
          lambda: population(72900, 10, 3, "-", True), [Num(90000), Num(100000), Num(97200), Num(110000)], 2),
         ("r24_e2", "If the annual decrease in the population of a town is 20% and the present population is 32000, what was it two years ago?",
          lambda: population(32000, 20, 2, "-", True), [Num(50000), Num(40000), Num(48000), Num(45000)], 1),
         ("r24_e3", "If the annual decrease in the population of a town is 5% and the present population is 54150, what was it two years ago?",
          lambda: population(54150, 5, 2, "-", True), [Num(59565), Num(57000), Num(62000), Num(60000)], 4),
         ("r24_e4", "If the annual decrease in the population of a town is 25% and the present population is 27000, what was it three years ago?",
          lambda: population(27000, 25, 3, "-", True), [Num(48000), Num(54000), Num(64000), Num(72000)], 3)],
}


def main():
    for n in range(17, 25):
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
