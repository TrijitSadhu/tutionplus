"""Ratio and Proportion Rules 6-11 (2026-10-30). Rule 6: coins - number of each = amount / value of one coin of each kind (or of one
'set' in the ratio). Rule 7: strength of milk = milk / whole mixture. Rule 8: equal quantities of two mixtures put together - add
the fractions of milk and of water. Rule 9: two mixtures put together in the ratio x : y. Rule 10: two (or three) numbers in a
ratio with a known difference - one part = difference / difference of the terms. Rule 11: an amount shared in a : b : c.
Writes the six cards, regenerates the old rows 715-720 (715's key was on the empty option e: the answer, 20 coins of each, was in
no option) and adds the book's examples and exercises with no copy. Usage: python gen_6_11.py"""
import os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from fmt import M, R, UU, low, nf  # noqa: E402
from gen_1_5 import main  # noqa: E402
from helpers import result  # noqa: E402

TH = {
    6: (r"If coins of several kinds are in a bag, take one 'set' of coins in the given ratio (or one coin of each kind when the numbers are equal); then",
        r"\[ \text{Number of sets} = \frac{\text{Amount in rupees}}{\text{Value of one set in rupees}} \]"),
    7: (r"The strength of milk in a mixture is the part of the mixture that is milk:", r"\[ \text{Strength} = \frac{\text{Quantity of milk}}{\text{Total quantity of the mixture}} \]"),
    8: (r"If equal quantities of two mixtures with milk : water \(= a : b\) and \(c : d\) are put together, the new mixture has milk : water",
        r"\[ \left(\frac{a}{a+b}+\frac{c}{c+d}\right) : \left(\frac{b}{a+b}+\frac{d}{c+d}\right) \]"),
    9: (r"If mixtures with water : milk \(= x_1 : y_1\) and \(x_2 : y_2\) are put together in the ratio \(x : y\), the new mixture has water : milk",
        r"\[ \text{Water} = x x_1(x_2+y_2) + y x_2(x_1+y_1) \]\[ \text{Milk} = x y_1(x_2+y_2) + y y_2(x_1+y_1) \]"),
    10: (r"If two numbers are in the ratio \(a : b\) and their difference is \(x\), the numbers are (for \(a \lt b\); swap for \(a \gt b\))",
         r"\[ \frac{ax}{b-a}\quad\text{and}\quad\frac{bx}{b-a} \]"),
    11: (r"If three numbers are in the ratio \(a : b : c\) and their sum is \(x\), the numbers are", r"\[ \frac{ax}{a+b+c},\quad \frac{bx}{a+b+c},\quad \frac{cx}{a+b+c} \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rsteps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def num(r, v, trad, ident, sub, unit=""):
    v = F(v)
    return result(("number", v), T(r), steps(*trad), rsteps(r, ident, sub), UU(v, unit), [ident, rf"Answer \(= {nf(v)}\)."], sub)


def rat(r, a, b, trad, ident, sub):
    return result(("ratio", (a, b)), T(r), steps(*trad), rsteps(r, ident, sub), R(a, b), [ident, rf"Ratio \(= {a} : {b}\)."], sub)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def rs(p):
    """paise -> rupees as written: Re 1, Rs 2, 50 paise."""
    return "Re 1" if p == 100 else f"Rs {p // 100}" if p % 100 == 0 else f"{p} paise"


# ---------- Rule 6
def r6_sets(counts, paise, total, ask):
    """counts = number ratio of the coins (equal numbers: all 1); paise = value of each kind; ask = index of the kind asked or 'each'/'all'."""
    total = F(total)
    one = sum(F(c * p, 100) for c, p in zip(counts, paise))
    n = total / one
    parts = " + ".join(rf"{c}\times {frc(F(p, 100))}" if c != 1 else frc(F(p, 100)) for c, p in zip(counts, paise))
    trad = [("Value of one set.", f"One set is " + ", ".join(f"{c} coin{'s' if c > 1 else ''} of {rs(p)}" for c, p in zip(counts, paise))
             + rf": \({parts} = {nf(one)}\) rupees."),
            ("Number of sets.", rf"\[ {nf(total)} \div {nf(one)} = {nf(n)} \]")]
    ident = rf"Amount Rs \({nf(total)}\); one set is worth Rs \({nf(one)}\)."
    sub = rf"\[ \frac{{{nf(total)}}}{{{nf(one)}}} = {nf(n)} \]"
    if ask == "each":
        trad[-1] = ("Number of each kind.", rf"\({nf(total)} \div {nf(one)} = {nf(n)}\) coins of each kind.")
        return num(6, n, trad, ident, sub, "coins of each kind")
    if ask == "all":
        each = [c * n for c in counts]
        trad.append(("Coins of each kind.", ", ".join(rf"\({c}\times {nf(n)} = {nf(e)}\)" for c, e in zip(counts, each)) + "."))
        fin = f"{M(nf(each[0]))}, {M(nf(each[1]))} and {M(nf(each[2]))}"
        return result(("triple", tuple(each)), T(6), steps(*trad), rsteps(6, ident, sub + rf"Coins: \({nf(each[0])}, {nf(each[1])}, {nf(each[2])}\)."), fin,
                      [ident, rf"Coins \(= {nf(each[0])}, {nf(each[1])}, {nf(each[2])}\)."], sub)
    v = counts[ask] * n
    trad.append((f"Coins of {rs(paise[ask])}.", rf"\[ {counts[ask]}\times {nf(n)} = {nf(v)} \]"))
    return num(6, v, trad, ident, sub + rf"Coins of {rs(paise[ask])} \(= {counts[ask]}\times {nf(n)} = {nf(v)}\).", "coins")


def r6_values(vr, paise, coins, ask):
    """the VALUES of the kinds are in the ratio vr; there are `coins` coins in all; ask = 'amount' or the index of a kind."""
    k_counts = [F(v * 100, p) for v, p in zip(vr, paise)]           # coins for value parts of Re 1 each
    k = F(coins) / sum(k_counts)
    trad = [("Coins for each value part.", "A value part of Re 1 is " + ", ".join(rf"\({nf(c)}\) coin{'s' if c != 1 else ''} of {rs(p)}" for c, p in zip(k_counts, paise))
             + rf"; with the parts \({' : '.join(map(str, vr))}\) the numbers of coins are " + " : ".join(rf"\({nf(v * c)}\)" for v, c in zip(vr, [F(100, p) for p in paise])) + "."),
            ("One part.", rf"\[ {nf(coins)} \div {nf(sum(v * F(100, p) for v, p in zip(vr, paise)))} = {nf(F(coins) / sum(v * F(100, p) for v, p in zip(vr, paise)))} \]")]
    unit = F(coins) / sum(v * F(100, p) for v, p in zip(vr, paise))
    ident = rf"Values in the ratio \({' : '.join(map(str, vr))}\), \({nf(coins)}\) coins in all."
    if ask == "amount":
        v = unit * sum(vr)
        trad.append(("Total amount.", rf"Each value part is Rs \({nf(unit)}\): \({sum(vr)}\times {nf(unit)} = {nf(v)}\) rupees."))
        sub = rf"Number of sets \(= {nf(unit)}\); amount \(= {nf(unit)}\times {sum(vr)} = {nf(v)}\)."
        return num(6, v, trad, ident, sub, "")
    v = unit * vr[ask] * F(100, paise[ask])
    trad.append((f"Coins of {rs(paise[ask])}.", rf"\[ {vr[ask]}\times {nf(F(100, paise[ask]))}\times {nf(unit)} = {nf(v)} \]"))
    sub = rf"Number of sets \(= {nf(unit)}\); coins of {rs(paise[ask])} \(= {nf(vr[ask] * F(100, paise[ask]))}\times {nf(unit)} = {nf(v)}\)."
    return num(6, v, trad, ident, sub, "coins")


# ---------- Rule 7
def r7(w1, m1, w2, m2):
    s1, s2 = F(m1, m1 + w1), F(m2, m2 + w2)
    a, b = low(s1, s2)
    trad = [("Strength of each mixture.", rf"First: \(\frac{{{m1}}}{{{m1}+{w1}}} = {frc(s1)}\); second: \(\frac{{{m2}}}{{{m2}+{w2}}} = {frc(s2)}\)."),
            ("Compare them.", rf"\[ {frc(s1)} : {frc(s2)} = {a} : {b} \]")]
    return rat(7, a, b, trad, rf"Milk \({m1}\), mixture \({m1 + w1}\); milk \({m2}\), mixture \({m2 + w2}\).", rf"\[ \frac{{{m1}}}{{{m1 + w1}}} : \frac{{{m2}}}{{{m2 + w2}}} = {a} : {b} \]")


# ---------- Rule 8
def r8(a, b, c, d):
    milk, water = F(a, a + b) + F(c, c + d), F(b, a + b) + F(d, c + d)
    x, y = low(milk, water)
    L = (a + b) * (c + d) // gcd(a + b, c + d)
    trad = [("Take equal amounts.", rf"Take \({L}\) litres of each mixture. First: milk \({nf(F(a * L, a + b))}\), water \({nf(F(b * L, a + b))}\); "
                                    rf"second: milk \({nf(F(c * L, c + d))}\), water \({nf(F(d * L, c + d))}\)."),
            ("Add them.", rf"Milk \(= {nf(milk * L)}\), water \(= {nf(water * L)}\): \[ {nf(milk * L)} : {nf(water * L)} = {x} : {y} \]")]
    sub = rf"\[ \left(\frac{{{a}}}{{{a + b}}}+\frac{{{c}}}{{{c + d}}}\right) : \left(\frac{{{b}}}{{{a + b}}}+\frac{{{d}}}{{{c + d}}}\right) = {frc(milk)} : {frc(water)} = {x} : {y} \]"
    return rat(8, x, y, trad, rf"Milk : water \(= {a} : {b}\) and \({c} : {d}\), equal quantities.", sub)


# ---------- Rule 9
def r9(x1, y1, x2, y2, x, y):
    w = x * x1 * (x2 + y2) + y * x2 * (x1 + y1)
    m = x * y1 * (x2 + y2) + y * y2 * (x1 + y1)
    a, b = low(w, m)
    q1, q2 = F(x, x + y), F(y, x + y)
    trad = [("Fractions of each vessel.", rf"Water : milk is \({x1} : {y1}\) in the first and \({x2} : {y2}\) in the second; the mixture takes "
                                          rf"\({frc(q1)}\) of the first and \({frc(q2)}\) of the second."),
            ("Water and milk in the mixture.", rf"Water \(= {frc(q1)}\times\frac{{{x1}}}{{{x1 + y1}}} + {frc(q2)}\times\frac{{{x2}}}{{{x2 + y2}}} = {frc(q1 * F(x1, x1 + y1) + q2 * F(x2, x2 + y2))}\); "
                                               rf"milk \(= {frc(q1 * F(y1, x1 + y1) + q2 * F(y2, x2 + y2))}\)."),
            ("Ratio.", rf"\[ {frc(q1 * F(x1, x1 + y1) + q2 * F(x2, x2 + y2))} : {frc(q1 * F(y1, x1 + y1) + q2 * F(y2, x2 + y2))} = {a} : {b} \]")]
    sub = (rf"\[ \text{{Water}} = {x}\times {x1}\times {x2 + y2} + {y}\times {x2}\times {x1 + y1} = {w} \]"
           rf"\[ \text{{Milk}} = {x}\times {y1}\times {x2 + y2} + {y}\times {y2}\times {x1 + y1} = {m} \]"
           rf"\[ {w} : {m} = {a} : {b} \]")
    return rat(9, a, b, trad, rf"\(x_1 : y_1 = {x1} : {y1}\), \(x_2 : y_2 = {x2} : {y2}\), \(x : y = {x} : {y}\).", sub)


# ---------- Rule 10
def r10(a, b, x, ask, unit=""):
    """two numbers a : b, the larger is x more than the smaller."""
    a, b, x = F(a), F(b), F(x)
    k = x / abs(b - a)
    p, q = a * k, b * k
    trad = [("Value of one part.", rf"The numbers are \({nf(a)}k\) and \({nf(b)}k\); they differ by \({nf(abs(b - a))}k = {nf(x)}\), so \(k = {nf(k)}\)."),
            ("The numbers.", rf"\({nf(a)}\times {nf(k)} = {nf(p)}\), \({nf(b)}\times {nf(k)} = {nf(q)}\).")]
    ident = rf"\(a = {nf(a)}\), \(b = {nf(b)}\), difference \(x = {nf(x)}\)."
    sub = rf"\[ \frac{{{nf(a)}\times {nf(x)}}}{{{nf(abs(b - a))}}} = {nf(p)},\qquad \frac{{{nf(b)}\times {nf(x)}}}{{{nf(abs(b - a))}}} = {nf(q)} \]"
    if ask == "both":
        return result(("pair", (p, q)), T(10), steps(*trad), rsteps(10, ident, sub), f"{M(nf(p))} and {M(nf(q))}", [ident, rf"Numbers \(= {nf(p)}\), \({nf(q)}\)."], sub)
    lo, hi = min(p, q), max(p, q)
    v, how = {"sum": (p + q, rf"\({nf(p)} + {nf(q)} = {nf(p + q)}\)"), "prod": (p * q, rf"\({nf(p)}\times {nf(q)} = {nf(p * q)}\)"),
              "rem": (hi % lo, rf"\({nf(hi)} = {nf(hi // lo)}\times {nf(lo)} + {nf(hi % lo)}\)"),
              "sub": ((p * q) % (p + q), rf"product \({nf(p * q)}\), sum \({nf(p + q)}\): \({nf(p * q)} = {nf((p * q) // (p + q))}\times {nf(p + q)} + {nf((p * q) % (p + q))}\)"),
              "larger": (hi, rf"the larger is \({nf(hi)}\)")}[ask]
    trad.append(("What is asked.", how + "."))
    return num(10, v, trad, ident, sub + how + ".", unit)


def r10_three(parts, i, j, x, ask, times=1, unit="Rs"):
    """three amounts in the ratio parts; amount j is x more than amount i; ask = index wanted (times = 12 for a year)."""
    k = F(x, parts[j] - parts[i])
    vals = [p * k for p in parts]
    v = vals[ask] * times
    names = "PQR"
    trad = [("Value of one part.", rf"The amounts are " + ", ".join(rf"\({p}k\)" for p in parts) + rf"; \({names[j]} - {names[i]} = {parts[j] - parts[i]}k = {nf(x)}\), so \(k = {nf(k)}\)."),
            (f"{names[ask]}'s amount.", rf"\({parts[ask]}\times {nf(k)} = {nf(vals[ask])}\)" + (rf"; in a year \({nf(vals[ask])}\times {times} = {nf(v)}\)." if times != 1 else "."))]
    ident = rf"Ratio \({' : '.join(map(str, parts))}\); {names[j]} \(-\) {names[i]} \(= {nf(x)}\)."
    sub = rf"\[ \frac{{{parts[ask]}\times {nf(x)}}}{{{parts[j]}-{parts[i]}}} = {nf(vals[ask])} \]" + (rf"Year: \({nf(vals[ask])}\times {times} = {nf(v)}\)." if times != 1 else "")
    return num(10, v, trad, ident, sub, unit)


# ---------- Rule 11
def r11(parts, x, ask, unit="Rs"):
    x = F(x)
    k = x / sum(parts)
    vals = [p * k for p in parts]
    names = "XYZ"
    trad = [("Value of one part.", rf"\({' + '.join(map(str, parts))} = {sum(parts)}\) parts; one part \(= {nf(x)} \div {sum(parts)} = {nf(k)}\)."),
            ("The shares.", ", ".join(rf"{n} \(= {p}\times {nf(k)} = {nf(v)}\)" for n, p, v in zip(names, parts, vals)) + ".")]
    ident = rf"Ratio \({' : '.join(map(str, parts))}\), sum \(x = {nf(x)}\)."
    sub = "".join(rf"\[ \frac{{{p}\times {nf(x)}}}{{{sum(parts)}}} = {nf(v)} \]" for p, v in zip(parts, vals))
    if ask == "ratio_of_diffs":
        a, b = low(vals[1] - vals[0], vals[2] - vals[1])
        trad.append(("Compare the differences.", rf"\((Y-X) : (Z-Y) = {nf(vals[1] - vals[0])} : {nf(vals[2] - vals[1])} = {a} : {b}\)."))
        return rat(11, a, b, trad, ident, sub + rf"\((Y-X) : (Z-Y) = {a} : {b}\).")
    if ask == "hcf":
        g = gcd(*map(int, vals))
        trad.append(("HCF.", rf"The HCF of \({', '.join(nf(v) for v in vals)}\) is \({g}\)."))
        return num(11, g, trad, ident, sub + rf"HCF \(= {g}\).", "")
    if isinstance(ask, tuple):
        i, j = ask
        v = vals[j] - vals[i]
        trad.append(("Difference.", rf"\({nf(vals[j])} - {nf(vals[i])} = {nf(v)}\)."))
        return num(11, v, trad, ident, sub + rf"Difference \(= {nf(v)}\).", unit)
    return num(11, vals[ask], trad, ident, sub, unit)


C = card
CARDS = {
    6: C(6, "Number of Coins", r"Group the coins into 'sets' that follow the given ratio; count the sets from the amount.", r"\[ \frac{\text{Amount}}{\text{Value of one set}} \]",
         [("Equal numbers", r"\text{set} = 1+0.5+0.25"), ("Numbers in a : b : c", r"\text{set} = a\,v_1+b\,v_2+c\,v_3"), ("Values in a : b : c", r"\text{coins} = \frac{a}{v_1} : \frac{b}{v_2} : \frac{c}{v_3}")],
         r"Write every coin's value in rupees first. When the VALUES (not the numbers) are in a ratio, turn them into numbers by dividing by each coin's value.",
         "'A bag contains an equal number of Re 1, 50 paise and 25 paise coins worth Rs x; how many of each?'",
         r"Equal numbers of Re 1 and 50 paise worth Rs \(45\): \(45 \div 1.5 = 30\) of each.", r"Mixing up the ratio of the numbers with the ratio of the values."),
    7: C(7, "Strength of Milk", r"Strength is the fraction of the whole mixture that is milk.", r"\[ \frac{\text{milk}}{\text{milk}+\text{water}} \]",
         [("Mixture 1", r"\frac{m_1}{m_1+w_1}"), ("Mixture 2", r"\frac{m_2}{m_2+w_2}"), ("Ratio", r"\frac{m_1}{m_1+w_1} : \frac{m_2}{m_2+w_2}")],
         r"Divide by the WHOLE mixture (milk + water), not by the water.", "'One man adds a litres of water to b litres of milk and another c litres to d litres; ratio of the strengths?'",
         r"\(2\) water + \(8\) milk and \(5\) water + \(15\) milk: \(\frac{4}{5} : \frac{3}{4} = 16 : 15\).", r"Using milk : water instead of milk : mixture."),
    8: C(8, "Equal Quantities of Two Mixtures", r"With equal amounts, add the fraction of milk from each and the fraction of water from each.",
         r"\[ \left(\tfrac{a}{a+b}+\tfrac{c}{c+d}\right) : \left(\tfrac{b}{a+b}+\tfrac{d}{c+d}\right) \]",
         [("Mixture 1", r"\frac{a}{a+b}\ \text{milk}"), ("Mixture 2", r"\frac{c}{c+d}\ \text{milk}"), ("Together", r"\text{add milk, add water}")],
         r"When \(a+b = c+d\) the answer is simply \((a+c) : (b+d)\); otherwise use the fractions.", "'Two vessels contain equal quantities of mixtures in the ratios a : b and c : d; both are mixed.'",
         r"\(3 : 1\) and \(1 : 1\): \(\frac{3}{4}+\frac{1}{2} : \frac{1}{4}+\frac{1}{2} = 5 : 3\).", r"Adding the ratios term by term when the totals differ."),
    9: C(9, "Two Mixtures in a Given Ratio", r"Weight each vessel's water and milk by how much of that vessel is used.",
         r"\[ xx_1(x_2+y_2)+yx_2(x_1+y_1) : xy_1(x_2+y_2)+yy_2(x_1+y_1) \]",
         [("Vessel 1", r"\frac{x}{x+y}\ \text{of the mix}"), ("Vessel 2", r"\frac{y}{x+y}\ \text{of the mix}"), ("Water : milk", r"\text{weighted sums}")],
         r"It is Rule 8 with unequal amounts: \(\frac{x}{x+y}\) of the first mixture and \(\frac{y}{x+y}\) of the second.",
         "'Two vessels with water : milk = a : b and c : d are mixed in the ratio x : y; find water : milk.'",
         r"\(1 : 1\) and \(1 : 3\) mixed \(1 : 1\): \(\frac{1}{4}+\frac{1}{8} : \frac{1}{4}+\frac{3}{8} = 3 : 5\).", r"Ignoring the ratio in which the vessels are mixed."),
    10: C(10, "Numbers in a Ratio With a Known Difference", r"The difference of the two numbers is the difference of their parts.", r"\[ \frac{ax}{b-a},\quad \frac{bx}{b-a} \]",
          [("Parts", r"a,\ b"), ("One part", r"\frac{x}{b-a}"), ("Numbers", r"a\times\text{part},\ b\times\text{part}")],
          r"With three amounts in \(a : b : c\), any known difference fixes one part, and then all three amounts.",
          "'Two numbers are in the ratio a : b and the larger exceeds the smaller by x; find the numbers.'",
          r"\(5 : 8\), difference \(12\): one part \(4\), numbers \(20\) and \(32\).", r"Dividing by \(a+b\) (that is for a known sum)."),
    11: C(11, "Sharing in Three Parts", r"Split the amount into \(a+b+c\) equal parts.", r"\[ \frac{ax}{a+b+c},\ \frac{bx}{a+b+c},\ \frac{cx}{a+b+c} \]",
          [("Parts", r"a+b+c"), ("One part", r"\frac{x}{a+b+c}"), ("Shares", r"a,\ b,\ c\ \text{parts}")],
          r"Differences of shares are differences of parts times one part.", "'Rs x is divided among A, B and C in the ratio a : b : c; find B's share.'",
          r"Rs \(600\) in \(1 : 2 : 3\): Rs \(100, 200, 300\).", r"Dividing by the number of people instead of the sum of the parts."),
}
OLD = {
    715: (6, "A purse holds an equal number of Rs 5 coins, Rs 2 coins and Re 1 coins, worth Rs 176 in all. How many coins of each kind are there?",
          lambda: r6_sets([1, 1, 1], [500, 200, 100], 176, "each"), "coins of each kind"),
    716: (7, "One woman mixes 6 litres of water into 22 litres of milk, and another mixes 13 litres of water into 39 litres of milk. "
             "What is the ratio of the strengths of milk in the two mixtures?", lambda: r7(6, 22, 13, 39), "ratio"),
    717: (8, "Two jugs hold equal amounts of milk and water mixtures, in the ratios 12 : 17 and 11 : 18. The two are poured together. "
             "What is the ratio of milk to water in the new mixture?", lambda: r8(12, 17, 11, 18), "ratio"),
    719: (10, "Two numbers are in the ratio 7 : 12, and the larger is 45 more than the smaller. Find the numbers.", lambda: r10(7, 12, 45, "both"), "pair"),
    720: (11, "A prize of Rs 1215 is shared among X, Y and Z in the ratio 7 : 9 : 11. How much does Y get?", lambda: r11([7, 9, 11], 1215, 1), "Rs"),
}
NEW = {
    6: [("r6_ex2", "A box has Re 1, 50 paise and 25 paise coins whose values are in the ratio 2 : 3 : 5. There are 560 coins in all. What is the total amount in the box in rupees?",
         lambda: r6_values([2, 3, 5], [100, 50, 25], 560, "amount"), "", None),
        ("r6_e1", "A bag has Re 1, 50 paise and 25 paise coins in the ratio 6 : 5 : 4 by number. The total amount is Rs 285. How many coins of each kind are there?",
         lambda: r6_sets([6, 5, 4], [100, 50, 25], 285, "all"), "", None),
        ("r6_e2", "A jar has 50 paise, 20 paise and 10 paise coins in the ratio 2 : 3 : 5 by number. The money in it is Rs 84. How many 50 paise coins are there?",
         lambda: r6_sets([2, 3, 5], [50, 20, 10], 84, 0), "coins", None),
        ("r6_e3", "A bag has Re 1, 50 paise and 25 paise coins whose values are in the ratio 5 : 6 : 4. There are 660 coins in all. How many 25 paise coins are there?",
         lambda: r6_values([5, 6, 4], [100, 50, 25], 660, 2), "coins", None),
        ("r6_e4", "A box holds Re 1, 50 paise and 25 paise coins in the ratio 3 : 8 : 12 by number. The total is Rs 470. How many 50 paise coins are there?",
         lambda: r6_sets([3, 8, 12], [100, 50, 25], 470, 1), "coins", None),
        ("r6_e5", "A bag has an equal number of Re 1, 50 paise and 25 paise coins, worth Rs 64.75 in all. How many coins of each kind are there?",
         lambda: r6_sets([1, 1, 1], [100, 50, 25], F("64.75"), "each"), "coins of each kind", None),
        ("r6_e6", "A tin has an equal number of 50 paise, 25 paise, 20 paise and 5 paise coins, worth Rs 52 in all. How many coins of each kind are there?",
         lambda: r6_sets([1, 1, 1, 1], [50, 25, 20, 5], 52, "each"), "coins of each kind", None)],
    7: [("r7_e1", "A milkman adds 11 litres of water to 33 litres of milk, and another adds 7 litres of water to 28 litres of milk. Find the ratio of the strengths of milk in the two mixtures.",
         lambda: r7(11, 33, 7, 28), "ratio", None),
        ("r7_e2", "In one can, 14 litres of water are mixed with 26 litres of milk; in another, 17 litres of water with 23 litres of milk. What is the ratio of the strengths of milk?",
         lambda: r7(14, 26, 17, 23), "ratio", None),
        ("r7_e3", "A shop mixes 9 litres of water with 16 litres of milk, and another shop mixes 7 litres of water with 18 litres of milk. Compare the strengths of milk in the two mixtures.",
         lambda: r7(9, 16, 7, 18), "ratio", None),
        ("r7_e4", "One pail has 19 litres of water in 57 litres of milk, and another has 11 litres of water in 66 litres of milk. Find the ratio of the strengths of milk.",
         lambda: r7(19, 57, 11, 66), "ratio", None),
        ("r7_e5", "A dairy adds 27 litres of water to 45 litres of milk in one tank and 32 litres of water to 48 litres of milk in another. What is the ratio of the strengths of milk?",
         lambda: r7(27, 45, 32, 48), "ratio", None)],
    8: [("r8_e1", "Two cans hold equal amounts of milk and water mixtures in the ratios 21 : 11 and 11 : 14. They are poured into one drum. Find the ratio of milk to water in the drum.",
         lambda: r8(21, 11, 11, 14), "ratio", None),
        ("r8_e2", "Equal amounts of two mixtures, with milk and water in the ratios 4 : 1 and 3 : 2, are mixed. What is the ratio of milk to water now?", lambda: r8(4, 1, 3, 2), "ratio", None),
        ("r8_e3", "Two bottles hold equal quantities of milk and water mixtures in the ratios 21 : 11 and 11 : 12. Both are mixed well. Find the ratio of milk to water in the mixture.",
         lambda: r8(21, 11, 11, 12), "ratio", None),
        ("r8_e4", "Equal quantities of two mixtures with milk to water 2 : 5 and 3 : 4 are put together. What is the new ratio of milk to water?", lambda: r8(2, 5, 3, 4), "ratio", None),
        ("r8_e5", "Two pots hold equal amounts of mixtures with milk and water in the ratios 11 : 4 and 2 : 3. They are mixed together. Find the ratio of milk to water.",
         lambda: r8(11, 4, 2, 3), "ratio", None)],
    9: [("r9_ex", "Two cans hold water and milk in the ratios 1 : 3 and 3 : 5. They are mixed in the ratio 2 : 1. What is the ratio of water to milk in the new mixture?",
         lambda: r9(1, 3, 3, 5, 2, 1), "ratio", None),
        ("r9_e1", "Mixtures with water and milk in the ratios 1 : 4 and 2 : 3 are mixed in the ratio 1 : 2. Find the ratio of water to milk in the result.", lambda: r9(1, 4, 2, 3, 1, 2), "ratio", None),
        ("r9_e2", "Two jars hold water and milk in the ratios 2 : 5 and 3 : 4. They are mixed in the ratio 3 : 2. What is the ratio of water to milk now?", lambda: r9(2, 5, 3, 4, 3, 2), "ratio", None),
        ("r9_e3", "Water and milk are in the ratio 1 : 5 in one tank and 3 : 5 in another. The tanks are emptied into a vat in the ratio 3 : 4. Find the ratio of water to milk in the vat.",
         lambda: r9(1, 5, 3, 5, 3, 4), "ratio", None),
        ("r9_e4", "Two mixtures have water and milk in the ratios 3 : 7 and 1 : 4. They are mixed in the ratio 1 : 2. What is the ratio of water to milk in the new mixture?",
         lambda: r9(3, 7, 1, 4, 1, 2), "ratio", None),
        ("r9_e5", "Two cans with water and milk in the ratios 2 : 11 and 2 : 13 are mixed in the ratio 7 : 11. Find the ratio of water to milk in the mixture.", lambda: r9(2, 11, 2, 13, 7, 11), "ratio", None)],
    10: [("r10_ex2", "The incomes of P, Q and R are in the ratio 4 : 9 : 11. Q earns Rs 350 more than P. What is R's income?", lambda: r10_three([4, 9, 11], 0, 1, 350, 2), "Rs", None),
         ("r10_e1", "Two numbers are in the ratio 17 : 6, and the larger is 77 more than the smaller. What is the sum of the numbers?", lambda: r10(17, 6, 77, "sum"), "", None),
         ("r10_e2", "Two numbers are in the ratio 3 : 8, and the larger is 25 more than the smaller. What is the remainder when the larger is divided by the smaller?",
          lambda: r10(3, 8, 25, "rem"), "", None),
         ("r10_e3", "Two numbers are in the ratio 15 : 16, and the larger exceeds the smaller by 17. Find the product of the numbers.", lambda: r10(15, 16, 17, "prod"), "", None),
         ("r10_e4", "Two numbers are in the ratio 5 : 2, and the larger is 18 more than the smaller. What is the least number that must be taken from their product "
                    "so that the rest divides exactly by their sum?", lambda: r10(5, 2, 18, "sub"), "", None),
         ("r10_e5", "The savings of P, Q and R are in the ratio 5 : 11 : 19, and Q has Rs 246 more than P. How much does R have?", lambda: r10_three([5, 11, 19], 0, 1, 246, 2), "Rs", None),
         ("r10_e6", "The prices of a cycle and a fan are in the ratio 7 : 4. The cycle costs Rs 1800 more than the fan. What is the price of the cycle?",
          lambda: r10(7, 4, 1800, "larger", "Rs"), "Rs", None),
         ("r10_e7", "The monthly pay of P, Q and R is in the ratio 3 : 4 : 7. R gets Rs 1600 a month more than P. What is Q's pay for a year?",
          lambda: r10_three([3, 4, 7], 0, 2, 1600, 1, times=12), "Rs", None)],
    11: [("r11_e1", "Rs 1260 is shared among X, Y and Z in the ratio 4 : 9 : 1. What is the difference between the shares of Y and X?", lambda: r11([4, 9, 1], 1260, (0, 1)), "Rs", None),
         ("r11_e2", "Rs 2700 is divided among X, Y and Z in the ratio 3 : 8 : 16. What is the ratio of (Y's share minus X's share) to (Z's share minus Y's share)?",
          lambda: r11([3, 8, 16], 2700, "ratio_of_diffs"), "ratio", None),
         ("r11_e3", "Rs 840 is divided among X, Y and Z in the ratio 2 : 3 : 7. Find the HCF of the three shares.", lambda: r11([2, 3, 7], 840, "hcf"), "", None),
         ("r11_e4", "Rs 1425 is shared among X, Y and Z in the ratio 4 : 7 : 8. What is Z's share?", lambda: r11([4, 7, 8], 1425, 2), "Rs", None),
         ("r11_e5", "Rs 1890 is shared among X, Y and Z in the ratio 2 : 5 : 7. How much does Z get?", lambda: r11([2, 5, 7], 1890, 2), "Rs", None),
         ("r11_e6", "A fund of Rs 1404 is divided among X, Y and Z in the ratio 5 : 6 : 7. Find Z's share.", lambda: r11([5, 6, 7], 1404, 2), "Rs", None)],
}

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(6, 12))
