"""Rules 25-32: writes the eight rule cards, regenerates the old worked-example rows 613-620 in the prompt #12 layout
(Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer), links them, cleans their text and odd
distractors, and adds the book exercises of these rules (numbers changed, wording rewritten; also Rule 27's second
worked example, which had no copy) as one JsonImport payload per rule. Same output files as gen_1_8.py."""
import json, os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_8 import P, Num, pnum, result  # noqa: E402

YEARS = ["first", "second", "third"]


def brackets(changes, symbolic=False):
    letters = "xyz"
    return "".join(rf"(100 {'+' if s > 0 else '-'} {letters[i] if symbolic else pnum(p)})" for i, (s, p) in enumerate(changes))


def hundreds(k):
    return r"\times ".join(["100"] * k)


def years_formula(changes, past):
    k = len(changes)
    if past:
        return rf"\frac{{P\times {hundreds(k)}}}{{{brackets(changes, True)}}}"
    return rf"\frac{{P\times {brackets(changes, True)}}}{{{hundreds(k)}}}"


def theorem(changes, past):
    k = len(changes)
    words = [f"{'increases' if s > 0 else 'decreases'} by \\({'xyz'[i]}\\%\\) during the {YEARS[i]} year" for i, (s, _) in enumerate(changes)]
    if past:
        return (rf"If the population of a town {', '.join(words)}, and the present population is \(P\), then the population {k} years ago was"
                rf"<br>\[ {years_formula(changes, True)} \]")
    return rf"The population of a town is \(P\). If it {', '.join(words)}, then the population after {k} years will be<br>\[ {years_formula(changes, False)} \]"


def years(P0, changes, past, theorem_text=None):
    """changes = [(+1, 10), (-1, 20), ...] one per year. past=False: P0 now, find P after; past=True: P0 now, find P len(changes) years ago."""
    P0 = F(P0)
    changes = [(s, F(p)) for s, p in changes]
    k = len(changes)
    factor = F(1)
    for s, p in changes:
        factor *= (100 + s * p) / 100
    ans = P0 / factor if past else P0 * factor
    rows = []
    if past:
        cur = P0
        for i in range(k - 1, -1, -1):
            s, p = changes[i]
            keep = 100 + s * p
            before = cur * 100 / keep
            rows.append(rf"End of year {i + 1}: \({tex(cur)}\) is \({pnum(keep)}\%\) of the population at the start of that year, so the start was "
                        rf"\(\frac{{{tex(cur)}\times 100}}{{{pnum(keep)}}} = {tex(before)}\)")
            cur = before
        trad = steps(("Work backwards one year at a time.", "<br>".join(rows)),
                     ("Read off the population.", rf"The population {k} years ago was \({tex(ans)}\)."))
    else:
        cur = P0
        for i, (s, p) in enumerate(changes):
            ch = cur * p / 100
            new = cur + s * ch
            rows.append(rf"Year {i + 1}: \({pnum(p)}\%\) of \({tex(cur)} = {tex(ch)}\), so \({tex(cur)} {'+' if s > 0 else '-'} {tex(ch)} = {tex(new)}\)")
            cur = new
        trad = steps(("Follow the population year by year.", "<br>".join(rows)),
                     ("Read off the population.", rf"After {k} years the population is \({tex(ans)}\)."))
    nums = brackets(changes)
    subst = (rf"\frac{{{tex(P0)}\times {hundreds(k)}}}{{{nums}}} = {tex(ans)}" if past else rf"\frac{{{tex(P0)}\times {nums}}}{{{hundreds(k)}}} = {tex(ans)}")
    rule = steps(
        ("Identify the values.", rf"\(P = {tex(P0)}\), " + ", ".join(rf"year {i + 1}: \({'+' if s > 0 else '-'}{pnum(p)}\%\)" for i, (s, p) in enumerate(changes)) + "."),
        ("Apply the specified rule.", rf"\[ {years_formula(changes, past)} \]"),
        ("Substitute the values.", rf"\[ {subst} \]"))
    rb = [rf"\(P = {tex(P0)}\); changes " + ", ".join(rf"\({'+' if s > 0 else '-'}{pnum(p)}\%\)" for s, p in changes) + ".",
          rf"Population \(= {years_formula(changes, past)}\).", rf"\({subst}\)."]
    sc = rf"\[ {subst} \]"
    return result(("number", ans), theorem_text or theorem(changes, past), trad, rule, Num(ans), rb, sc)


# ---------------------------------------------------------------- Rule 31: males and females
T31 = (r"The population of a town is \(P_1\). If the males increase by \(x\%\) and the females by \(y\%\), the population becomes \(P_2\). Then<br>"
       r"\[ \text{Males} = \frac{P_2\times 100 - P_1(100 + y)}{x - y},\qquad \text{Females} = \frac{P_2\times 100 - P_1(100 + x)}{y - x} \]")


def males_females(P1, x, y, P2, ask):
    """ask: 'males', 'females' or 'ratio' (males : females)."""
    P1, x, y, P2 = F(P1), F(x), F(y), F(P2)
    m = (P2 * 100 - P1 * (100 + y)) / (x - y)
    f = (P2 * 100 - P1 * (100 + x)) / (y - x)
    trad = steps(
        ("Form the equation.", rf"Let the number of females be \(f\); then the males are \({tex(P1)} - f\).<br>"
                               rf"\[ \frac{{{pnum(100 + x)}}}{{100}}({tex(P1)} - f) + \frac{{{pnum(100 + y)}}}{{100}}f = {tex(P2)} \]"),
        ("Clear the fractions.", rf"\[ {pnum(100 + x)}\times {tex(P1)} - {pnum(100 + x)}f + {pnum(100 + y)}f = {tex(P2 * 100)} \]"
                                 rf"\[ {pnum(y - x)}f = {tex(P2 * 100)} - {tex(P1 * (100 + x))} = {tex(P2 * 100 - P1 * (100 + x))} \]"),
        ("Solve.", rf"\[ f = {tex(f)},\qquad \text{{males}} = {tex(P1)} - {tex(f)} = {tex(m)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(P_1 = {tex(P1)}\), \(P_2 = {tex(P2)}\), \(x = {pnum(x)}\) (males), \(y = {pnum(y)}\) (females)."),
        ("Apply the specified rule.", r"\[ \text{Males} = \frac{P_2\times 100 - P_1(100 + y)}{x - y},\qquad \text{Females} = \frac{P_2\times 100 - P_1(100 + x)}{y - x} \]"),
        ("Substitute the values.", rf"\[ \text{{Males}} = \frac{{{tex(P2)}\times 100 - {tex(P1)}\times {pnum(100 + y)}}}{{{pnum(x)} - {pnum(y)}}} = {tex(m)} \]"
                                   rf"\[ \text{{Females}} = \frac{{{tex(P2)}\times 100 - {tex(P1)}\times {pnum(100 + x)}}}{{{pnum(y)} - {pnum(x)}}} = {tex(f)} \]"))
    rb = [rf"\(P_1 = {tex(P1)}\), \(P_2 = {tex(P2)}\), \(x = {pnum(x)}\), \(y = {pnum(y)}\).",
          rf"Males \(= \frac{{{tex(P2)}\times 100 - {tex(P1)}\times {pnum(100 + y)}}}{{{pnum(x - y)}}} = {tex(m)}\).",
          rf"Females \(= {tex(P1)} - {tex(m)} = {tex(f)}\)."]
    sc = rf"\[ \text{{Males}} = \frac{{{tex(P2 * 100)} - {tex(P1 * (100 + y))}}}{{{pnum(x - y)}}} = {tex(m)},\qquad \text{{Females}} = {tex(f)} \]"
    if ask == "ratio":
        g = gcd(int(m), int(f))
        a, b = int(m) // g, int(f) // g
        last = ("Form the ratio.", rf"\[ \text{{Males}} : \text{{Females}} = {tex(m)} : {tex(f)} = {a} : {b} \]")
        trad = trad + "<br><br>" + rf"<b>Step 4: {last[0]}</b><br>{last[1]}"
        rule = rule + "<br><br>" + rf"<b>Step 4: {last[0]}</b><br>{last[1]}"
        rb.append(rf"Ratio \(= {tex(m)} : {tex(f)} = {a} : {b}\).")
        sc = rf"\[ {tex(m)} : {tex(f)} = {a} : {b} \]"
        return result(("ratio", (a, b)), T31, trad, rule, rf"\({a} : {b}\)", rb, sc)
    v = m if ask == "males" else f
    return result(("number", v), T31, trad, rule, rf"\({tex(v)}\) {ask}", rb, sc)


# ---------------------------------------------------------------- Rule 32: price rises -> cut consumption
T32 = (r"If the price of a commodity increases by \(r\%\), then the reduction in consumption, so as not to increase the expenditure, is<br>"
       r"\[ \frac{r}{100 + r}\times 100\% \]")


def cut_consumption(r):
    r = F(r)
    v = r / (100 + r) * 100
    c = 10000 / (100 + r)
    trad = steps(
        ("Take easy starting values.", r"Let the price be \(100\) and the consumption \(100\) units, so the expenditure is \(100\times 100 = 10000\)."),
        ("Find the consumption that keeps the expenditure the same.", rf"The new price is \({pnum(100 + r)}\), so the consumption allowed is<br>"
                                                                       rf"\[ \frac{{10000}}{{{pnum(100 + r)}}} = {tex(c)} \]"),
        ("Find the reduction.", rf"\[ 100 - {tex(c)} = {tex(v)}\text{{ units out of 100, i.e. }} {tex(v)}\% \]"))
    rule = steps(
        ("Identify the value.", rf"\(r = {pnum(r)}\)."),
        ("Apply the specified rule.", r"\[ \text{Reduction} = \frac{r}{100 + r}\times 100\% \]"),
        ("Substitute the value.", rf"\[ \frac{{{pnum(r)}}}{{100 + {pnum(r)}}}\times 100 = \frac{{{pnum(r)}\times 100}}{{{pnum(100 + r)}}} = {tex(v)}\% \]"))
    rb = [rf"\(r = {pnum(r)}\).", r"Reduction \(= \frac{r}{100 + r}\times 100\%\).", rf"\(\frac{{{pnum(r)}}}{{{pnum(100 + r)}}}\times 100 = {tex(v)}\%\)."]
    sc = rf"\[ \frac{{{pnum(r)}}}{{100 + {pnum(r)}}}\times 100 = {tex(v)}\% \]"
    return result(("number", v), T32, trad, rule, P(v), rb, sc)


# ---------------------------------------------------------------- rule cards
def pop_card(n, title, changes, past, statement_extra, pattern, example, mistake):
    k = len(changes)
    ups = [s for s, _ in changes]
    return card(n, title,
                theorem(changes, past).split("<br>")[0] + statement_extra,
                rf"\[ {years_formula(changes, past)} \]",
                [(f"Year {i + 1}", rf"\times\frac{{100 {'+' if s > 0 else '-'} {'xyz'[i]}}}{{100}}") for i, s in enumerate(ups)]
                + [("Going back a year" if past else "After all the years", r"\text{divide by the factor}" if past else r"\text{multiply the factors}")],
                "Each year's change is on that year's population, so the yearly factors multiply"
                + (" - and going back in time divides by them." if past else "."),
                pattern, example, mistake)


CARDS = {
    25: pop_card(25, "Population Formula V: Different Rates of Increase", [(1, 0), (1, 0), (1, 0)], False,
                 " (use one bracket per year).",
                 "The population (or any amount) grows by DIFFERENT percentages in different years; the population after those years is asked.",
                 r"\(8000\), \(+10\%\) then \(+20\%\): \(\frac{8000\times 110\times 120}{100\times 100} = 10560\).",
                 r"Adding the rates (\(10 + 20 = 30\%\)) instead of multiplying the factors."),
    26: pop_card(26, "Population Formula VI: Increase, Decrease, Increase", [(1, 0), (-1, 0), (1, 0)], False,
                 " (a year with a decrease uses \\(100 - y\\)).",
                 "The population rises in one year, falls in the next and rises again; the population at the end is asked.",
                 r"\(10000\), \(+10\%\), \(-20\%\), \(+30\%\): \(\frac{10000\times 110\times 80\times 130}{100\times 100\times 100} = 11440\).",
                 r"Netting the rates (\(10 - 20 + 30 = 20\%\)) - a rise and a fall of different sizes do not cancel like that."),
    27: pop_card(27, "Population Formula VII: Past Population after a Rise and Falls", [(1, 0), (-1, 0), (-1, 0)], True,
                 " (use only as many brackets as there are years).",
                 "The population rose and then fell (or the other way round) over some years, the population at the END is given and the population "
                 "at the BEGINNING is asked.",
                 r"\(+5\%\) then \(-5\%\), end population \(7980\): \(\frac{7980\times 100\times 100}{105\times 95} = 8000\).",
                 r"Assuming a rise and an equal fall cancel: \(+5\%\) then \(-5\%\) leaves \(99.75\%\), not \(100\%\)."),
    28: pop_card(28, "Population Formula VIII: Past Population after Increases", [(1, 0), (1, 0), (1, 0)], True,
                 " (use one bracket per year).",
                 "The population increased by given percentages in the past years; the present population is given and an EARLIER population is asked.",
                 r"\(+10\%\), \(+20\%\), now \(26400\): \(\frac{26400\times 100\times 100}{110\times 120} = 20000\).",
                 r"Subtracting the percentages from the present population instead of dividing by the yearly factors."),
    29: pop_card(29, "Population Formula IX: Different Rates of Decrease", [(-1, 0), (-1, 0), (-1, 0)], False,
                 " (use one bracket per year).",
                 "The population falls by different percentages in different years; the population after those years is asked.",
                 r"\(8000\), \(-10\%\), \(-15\%\), \(-20\%\): \(\frac{8000\times 90\times 85\times 80}{100\times 100\times 100} = 4896\).",
                 r"Subtracting \(10 + 15 + 20 = 45\%\) of the original population."),
    30: pop_card(30, "Population Formula X: Past Population after Decreases", [(-1, 0), (-1, 0), (-1, 0)], True,
                 " (use one bracket per year).",
                 "The population fell by given percentages in the past years; the present population is given and the population some years AGO is asked.",
                 r"\(-20\%\), \(-30\%\), \(-40\%\), now \(67200\): \(\frac{67200\times 100\times 100\times 100}{80\times 70\times 60} = 200000\).",
                 r"Adding the percentages back to the present population instead of dividing by the yearly factors."),
    31: card(31, "Population Formula XI: Males and Females",
             r"The population of a town is \(P_1\). If the males increase by \(x\%\) and the females by \(y\%\) and the population becomes \(P_2\), "
             r"the numbers of males and females are found as below.",
             r"\[ \text{Males} = \frac{P_2\times 100 - P_1(100 + y)}{x - y},\qquad \text{Females} = \frac{P_2\times 100 - P_1(100 + x)}{y - x} \]",
             [("Males", r"m \to \frac{100 + x}{100}m"), ("Females", r"f \to \frac{100 + y}{100}f"), ("Total", r"m + f = P_1,\ \text{new total} = P_2")],
             r"If everyone grew at \(y\%\), the town would reach \(\frac{P_1(100 + y)}{100}\); the gap up to \(P_2\) comes only from the males growing "
             r"at \(x\%\) instead of \(y\%\).",
             "Two groups (males and females, boys and girls) grow by different percentages, the old and new totals are given, and one group or their ratio is asked.",
             r"\(P_1 = 8000\), males \(+6\%\), females \(+10\%\), \(P_2 = 8600\): females \(= \frac{860000 - 8000\times 106}{10 - 6} = 3000\).",
             r"Swapping \(x\) and \(y\): the MALES formula uses \(100 + y\) (the females' rate) on top."),
    32: card(32, "Price Rise: Cut in Consumption to Keep Expenditure the Same",
             r"If the price of a commodity increases by \(r\%\), then the consumption must be reduced by \(\frac{r}{100 + r}\times 100\%\) so that the "
             r"expenditure does not increase.",
             r"\[ \text{Reduction in consumption} = \frac{r}{100 + r}\times 100\% \]",
             [("Price", r"100 \to 100 + r"), ("Expenditure kept", r"100\times 100"), ("New consumption", r"\frac{10000}{100 + r}")],
             r"Expenditure \(=\) Price \(\times\) Consumption. When the price is \(\frac{100 + r}{100}\) times as much, the consumption must be "
             r"\(\frac{100}{100 + r}\) of what it was.",
             "The price (or duty, tax) on an item rises by r%; by how much per cent must the consumption be cut so the spending stays the same?",
             r"Price up \(20\%\): \(\frac{20}{120}\times 100 = 16\frac{2}{3}\%\).",
             r"Answering \(r\%\) itself: a \(20\%\) price rise needs only a \(16\frac{2}{3}\%\) cut."),
}

UP, DN = 1, -1
OLD = {
    25: {613: (lambda: years(8000, [(UP, 10), (UP, 20)], False), "The population of a town is 8000. It increases by 10% during the first year and by "
                                                                 "20% during the second year. What is the population after two years?", None)},
    26: {614: (lambda: years(10000, [(UP, 10), (DN, 20), (UP, 30)], False),
               "The population of a town is 10000. It increases by 10% during the first year. During the second year it decreases by 20%, and it "
               "increases by 30% during the third year. What is the population after 3 years?", None)},
    27: {615: (lambda: years(7980, [(UP, 5), (DN, 5)], True), "During one year the population of a locality increases by 5%, but during the next "
                                                               "year it decreases by 5%. If the population at the end of the second year was 7980, "
                                                               "find the population at the beginning of the first year.", None)},
    28: {616: (lambda: years(26400, [(UP, 10), (UP, 20)], True),
               "The population of a town increases by 10% during the first year and by 20% during the second year. The present population of "
               "the town is 26400. Find the population of the town two years ago.", {"a": Num(22000), "b": Num(21000), "c": Num(20000), "d": Num(18000)})},
    29: {617: (lambda: years(8000, [(DN, 10), (DN, 15), (DN, 20)], False),
               "The population of a town is 8000. It decreases by 10% during the first year, 15% during the second year and 20% during the third "
               "year. What will be the population after 3 years?", None)},
    30: {618: (lambda: years(67200, [(DN, 20), (DN, 30), (DN, 40)], True),
               "The population of a town decreases by 20% during the first year, by 30% during the second year and again by 40% during the third "
               "year. If the present population of the town is 67200, what was the population three years ago?",
               {"a": Num(300000), "b": Num(210000), "c": Num(200000), "d": Num(240000)})},
    31: {619: (lambda: males_females(8000, 6, 10, 8600, "females"),
               "The population of a town is 8000. If the males increase by 6% and the females by 10%, the population will be 8600. Find the number "
               "of females in the town.", None)},
    32: {620: (lambda: cut_consumption(20), "If the price of a commodity is raised by 20%, by how much per cent must a householder reduce his "
                                            "consumption of that commodity so as not to increase his expenditure?",
               {"a": P(F(25, 9)), "b": P(F(16, 9)), "c": P(F(20, 3)), "d": P(F(50, 3))})},
}

NEW = {
    25: [("r25_e1", "The population of a town is 9000. It increases by 10% during the first year and by 5% during the second year. What is the "
                    "population after two years?", lambda: years(9000, [(UP, 10), (UP, 5)], False), [Num(10350), Num(10395), Num(10935), Num(10500)], 2),
         ("r25_e2", "The population of a town is 16000. It increases by 10% during the first year, by 15% during the second year and by 20% "
                    "during the third year. What is the population after three years?",
          lambda: years(16000, [(UP, 10), (UP, 15), (UP, 20)], False), [Num(23200), Num(24828), Num(24288), Num(22880)], 3),
         ("r25_e3", "The population of a village is 5600. It increases by 25% during the first year and by 20% during the second year. What is "
                    "the population after two years?", lambda: years(5600, [(UP, 25), (UP, 20)], False), [Num(8400), Num(8120), Num(8800), Num(8040)], 1)],
    26: [("r26_e1", "The population of a town is 120000. It increases by 10% during the first year. During the second year it decreases by 10%, "
                    "and it increases by 20% during the third year. What is the population after 3 years?",
          lambda: years(120000, [(UP, 10), (DN, 10), (UP, 20)], False), [Num(144000), Num(145260), Num(132000), Num(142560)], 4),
         ("r26_e2", "The population of a town is 20000. It increases by 5% during the first year, decreases by 20% during the second year and "
                    "increases by 10% during the third year. What is the population after 3 years?",
          lambda: years(20000, [(UP, 5), (DN, 20), (UP, 10)], False), [Num(18480), Num(19000), Num(18840), Num(17480)], 1),
         ("r26_e3", "The population of a town is 24000. It increases by 25% during the first year. During the second year it decreases by 20%, "
                    "and it increases by 15% during the third year. What is the population after 3 years?",
          lambda: years(24000, [(UP, 25), (DN, 20), (UP, 15)], False), [Num(28000), Num(27600), Num(26700), Num(30000)], 2),
         ("r26_e4", "The population of a town is 50000. It increases by 20% during the first year, decreases by 25% during the second year and "
                    "increases by 10% during the third year. What is the population after 3 years?",
          lambda: years(50000, [(UP, 20), (DN, 25), (UP, 10)], False), [Num(52500), Num(45900), Num(49500), Num(50000)], 3)],
    27: [("r27_e1", "The population of a town increases by 20% during one year and decreases by 20% during the next year. If it has 38400 "
                    "inhabitants at present, find the number of inhabitants two years ago.",
          lambda: years(38400, [(UP, 20), (DN, 20)], True), [Num(36000), Num(40000), Num(41600), Num(38000)], 2),
         ("r27_e2", "During one year the population of a locality increases by 25%, but during the next year it decreases by 12%. If the "
                    "population at the end of the second year was 33000, find the population at the beginning of the first year.",
          lambda: years(33000, [(UP, 25), (DN, 12)], True), [Num(29040), Num(33300), Num(30000), Num(28000)], 3),
         ("r27_e3", "During one year the population of a locality increases by 10%, but during the next year it decreases by 5%. If the "
                    "population at the end of the second year was 20900, find the population at the beginning of the first year.",
          lambda: years(20900, [(UP, 10), (DN, 5)], True), [Num(21000), Num(19000), Num(19900), Num(20000)], 4),
         ("r27_e4", "The population of a town increases by 30% during one year and decreases by 30% during the next year. If it has 45500 "
                    "inhabitants at present, find the number of inhabitants two years ago.",
          lambda: years(45500, [(UP, 30), (DN, 30)], True), [Num(50000), Num(49500), Num(52000), Num(48000)], 1),
         ("r27_e5", "The population of a town increases by 25% during one year and decreases by 25% during the next year. If it has 37500 "
                    "inhabitants at present, find the number of inhabitants two years ago.",
          lambda: years(37500, [(UP, 25), (DN, 25)], True), [Num(36000), Num(40000), Num(42000), Num(38000)], 2),
         ("r27_e6", "During the first year the population of a town increases by 25%, during the second year it decreases by 10% and during the "
                    "third year it decreases by 20%. If the population at the end of the third year is 27000, find the population at the beginning "
                    "of the first year.", lambda: years(27000, [(UP, 25), (DN, 10), (DN, 20)], True), [Num(29700), Num(32400), Num(30000), Num(25000)], 3),
         ("r27_e7", "The population of a town increases by 15% during the first year and decreases by 20% during the second year. If the present "
                    "population is 64400, what was it 2 years ago?", lambda: years(64400, [(UP, 15), (DN, 20)], True),
          [Num(68000), Num(72000), Num(74000), Num(70000)], 4)],
    28: [("r28_e1", "The population of a town increases by 10% during the first year and by 10% during the second year. The present population "
                    "of the town is 14520. Find the population of the town two years ago.", lambda: years(14520, [(UP, 10), (UP, 10)], True),
          [Num(11800), Num(12000), Num(12200), Num(11616)], 2),
         ("r28_e2", "The population of a town increases by 25% during the first year and by 20% during the second year. The present population "
                    "of the town is 9000. Find the population of the town two years ago.", lambda: years(9000, [(UP, 25), (UP, 20)], True),
          [Num(6300), Num(5400), Num(6000), Num(6600)], 3),
         ("r28_e3", "The population of a town increases by 20% during the first year and by 15% during the second year. The present population "
                    "of the town is 41400. Find the population of the town two years ago.", lambda: years(41400, [(UP, 20), (UP, 15)], True),
          [Num(30000), Num(28980), Num(31000), Num(33000)], 1)],
    29: [("r29_e1", "The population of a town is 40000. It decreases by 10% during the first year, 5% during the second year and 20% during the "
                    "third year. What will be the population after 3 years?", lambda: years(40000, [(DN, 10), (DN, 5), (DN, 20)], False),
          [Num(26000), Num(27630), Num(28800), Num(27360)], 4),
         ("r29_e2", "The population of a town is 80000. It decreases by 5% during the first year, 20% during the second year and 25% during the "
                    "third year. What will be the population after 3 years?", lambda: years(80000, [(DN, 5), (DN, 20), (DN, 25)], False),
          [Num(45600), Num(40000), Num(46500), Num(48000)], 1),
         ("r29_e3", "The population of a town is 5000. It decreases by 20% during the first year, 30% during the second year and 40% during the "
                    "third year. What will be the population after 3 years?", lambda: years(5000, [(DN, 20), (DN, 30), (DN, 40)], False),
          [Num(1500), Num(1680), Num(1860), Num(2000)], 2)],
    30: [("r30_e1", "The population of a town decreases by 5% during the first year, by 10% during the second year and by 20% during the third "
                    "year. If the present population of the town is 34200, what was the population three years ago?",
          lambda: years(34200, [(DN, 5), (DN, 10), (DN, 20)], True), [Num(48000), Num(52000), Num(50000), Num(45000)], 3),
         ("r30_e2", "The population of a town decreases by 20% during the first year, by 10% during the second year and by 25% during the third "
                    "year. If the present population of the town is 16200, what was the population three years ago?",
          lambda: years(16200, [(DN, 20), (DN, 10), (DN, 25)], True), [Num(28000), Num(32400), Num(25000), Num(30000)], 4),
         ("r30_e3", "The population of a town decreases by 20% during the first year, by 25% during the second year and by 40% during the third "
                    "year. If the present population of the town is 9000, what was the population three years ago?",
          lambda: years(9000, [(DN, 20), (DN, 25), (DN, 40)], True), [Num(25000), Num(24000), Num(27000), Num(20000)], 1)],
    31: [("r31_e1", "The population of a town is 7000. If the males increase by 5% and the females by 10%, the population will be 7550. "
                    "Find the number of males in the town.", lambda: males_females(7000, 5, 10, 7550, "males"),
          [Num(4000), Num(3000), Num(2500), Num(3500)], 2),
         ("r31_e2", "The population of a town is 6000. If the males increase by 6% and the females by 12%, the population will be 6600. "
                    "Find the number of females in the town.", lambda: males_females(6000, 6, 12, 6600, "females"),
          [Num(2000), Num(3500), Num(4000), Num(4500)], 3),
         ("r31_e3", "The population of a town is 10000. If the males increase by 10% and the females by 15%, the population will be 11200. "
                    "Find the number of males in the town.", lambda: males_females(10000, 10, 15, 11200, "males"),
          [Num(4000), Num(5500), Num(6500), Num(6000)], 4),
         ("r31_e4", "In a certain year the population of a town was 7500. The next year the number of males increased by 6% and the number of "
                    "females by 10%, and the total population rose to 8150. What was the ratio of males to females in the first year?",
          lambda: males_females(7500, 6, 10, 8150, "ratio"), [r"\(1 : 2\)", r"\(2 : 1\)", r"\(2 : 3\)", r"\(3 : 5\)"], 1)],
    32: [("r32_e1", "If the duty on imported tea is increased by 50 per cent, by how much per cent must a man reduce his consumption of tea so "
                    "as not to increase his expenditure on it?", lambda: cut_consumption(50), [P(50), P(F(100, 3)), P(25), P(F(200, 3))], 2),
         ("r32_e2", "If the price of a commodity is raised by 5%, by how much per cent must a householder reduce his consumption of it so as not "
                    "to increase his expenditure?", lambda: cut_consumption(5), [P(5), P(F(85, 21)), P(F(100, 21)), P(F(110, 21))], 3),
         ("r32_e3", r"If the price of a commodity is raised by \(37\frac{1}{2}\%\), by how much per cent must a householder reduce his consumption "
                    r"of it so as not to increase his expenditure?", lambda: cut_consumption(F(75, 2)),
          [P(F(300, 11)), P(F(75, 2)), P(F(305, 11)), P(30)], 1),
         ("r32_e4", "If the price of a commodity is raised by 30%, by how much per cent must a householder reduce his consumption of it so as not "
                    "to increase his expenditure?", lambda: cut_consumption(30), [P(30), P(F(274, 13)), P(25), P(F(300, 13))], 4),
         ("r32_e5", r"If the price of a commodity is raised by \(33\frac{1}{3}\%\), by how much per cent must a householder reduce his "
                    r"consumption of it so as not to increase his expenditure?", lambda: cut_consumption(F(100, 3)),
          [P(F(100, 3)), P(20), P(25), P(30)], 3),
         ("r32_e6", r"If the price of a commodity is raised by \(14\frac{2}{7}\%\), by how much per cent must a householder reduce his "
                    r"consumption of it so as not to increase his expenditure?", lambda: cut_consumption(F(100, 7)),
          [P(F(100, 7)), P(F(25, 2)), P(F(50, 3)), P(F(100, 9))], 2),
         ("r32_e7", "The price of petrol has gone up by 60%. By what per cent should a family cut its use of petrol so as not to increase its "
                    "expenditure on petrol?", lambda: cut_consumption(60), [P(60), P(40), P(35), P(F(75, 2))], 4)],
}


def main():
    for n in range(25, 33):
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
