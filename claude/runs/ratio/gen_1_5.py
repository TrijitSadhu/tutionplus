"""Ratio and Proportion Rules 1-5 (2026-10-30). Rule 1: compound, duplicate, triplicate, subduplicate and subtriplicate ratios.
Rule 2: four numbers in proportion - product of the extremes = product of the means; the fourth proportional bc/a. Rule 3:
continued proportion - third proportional b^2/a, mean proportional sqrt(ac). Rule 4: the rule of three and compound proportion -
the answer is the third term times the ratios of the changed quantities. Rule 5: two numbers in the ratio a : b with sum x -
ax/(a+b) and bx/(a+b). Writes the five cards, regenerates the old rows 708-714 (the book's worked examples) with simple-style
sentences and all-new numbers, and adds the book's examples and exercises with no copy. Usage: python gen_1_5.py"""
import json, os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from fmt import B, M, R, UU, answer_json, low, nf, opts, pair_opts, ratio_opts, triple_opts  # noqa: E402
from helpers import result  # noqa: E402

TH = {
    1: (r"Ratios are compounded by multiplying the antecedents together for the new antecedent and the consequents together for the "
        r"new consequent. The duplicate, triplicate, subduplicate and subtriplicate ratios of \(a : b\) are", r"\[ a^{2} : b^{2},\quad a^{3} : b^{3},\quad \sqrt{a} : \sqrt{b},\quad \sqrt[3]{a} : \sqrt[3]{b} \]"),
    2: (r"If four quantities are in proportion, \(a : b :: c : d\), the product of the extremes equals the product of the means, so the fourth proportional is",
        r"\[ ad = bc,\qquad d = \frac{bc}{a} \]"),
    3: (r"Three quantities are in continued proportion when \(a : b = b : c\). Then the third proportional and the mean proportional are",
        r"\[ c = \frac{b^{2}}{a},\qquad b = \sqrt{ac} \]"),
    4: (r"Rule of three: set the unknown as the fourth term; for each quantity that changes, multiply by the ratio of the new to the old value "
        r"if the answer grows with it, or of the old to the new if it shrinks with it:", r"\[ \text{Required value} = \frac{\text{Product of the means}}{\text{Product of the first terms}} \]"),
    5: (r"If two numbers are in the ratio \(a : b\) and their sum is \(x\), the numbers are", r"\[ \frac{ax}{a+b}\quad\text{and}\quad\frac{bx}{a+b} \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rule_steps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def num(r, v, trad, ident, sub, unit=""):
    v = F(v)
    return result(("number", v), T(r), steps(*trad), rule_steps(r, ident, sub), UU(v, unit), [ident, rf"Answer \(= {nf(v)}\)."], sub)


def rat(r, a, b, trad, ident, sub):
    return result(("ratio", (a, b)), T(r), steps(*trad), rule_steps(r, ident, sub), R(a, b), [ident, rf"Ratio \(= {a} : {b}\)."], sub)


# ---------- Rule 1
def r1_comp(pairs):
    top = 1
    bot = 1
    for a, b in pairs:
        top *= a
        bot *= b
    a, b = low(top, bot)
    ups = r" \times ".join(str(p) for p, _ in pairs)
    dns = r" \times ".join(str(q) for _, q in pairs)
    trad = [("Write each ratio as a fraction.", ", ".join(rf"\(\frac{{{p}}}{{{q}}}\)" for p, q in pairs) + "."),
            ("Multiply the fractions.", rf"\[ \frac{{{ups}}}{{{dns}}} = \frac{{{top}}}{{{bot}}} = \frac{{{a}}}{{{b}}} \]")]
    return rat(1, a, b, trad, "Ratios " + ", ".join(R(p, q) for p, q in pairs) + ".", rf"\[ ({ups}) : ({dns}) = {top} : {bot} = {a} : {b} \]")


def root(n, k):
    r = round(n ** (1 / k))
    assert r ** k == n
    return r


def r1_power(a, b, kind):
    name = {2: "duplicate", 3: "triplicate", -2: "subduplicate", -3: "subtriplicate"}[kind]
    X = " " + B + "times "
    if kind > 0:
        x, y = a ** kind, b ** kind
        ta, tb = X.join([str(a)] * kind), X.join([str(b)] * kind)
        trad = [("Compound the ratio with itself.", f"The {name} ratio is " + R(a, b) + f" compounded with itself {'once more' if kind == 2 else 'twice more'}: "
                 + B + "[ " + ta + " : " + tb + f" = {x} : {y} " + B + "]")]
        sub = B + "[ " + f"{a}^{{{kind}}} : {b}^{{{kind}}} = {x} : {y} " + B + "]"
    else:
        k = -kind
        x, y = root(a, k), root(b, k)
        trad = [("Find the numbers that make the terms.", M(X.join([str(x)] * k) + f" = {a}") + " and " + M(X.join([str(y)] * k) + f" = {b}") + "."),
                ("Write the ratio of those numbers.", f"The {name} ratio is " + R(x, y) + ".")]
        rt = B + "sqrt" + ("" if k == 2 else "[3]")
        sub = B + "[ " + rt + "{" + str(a) + "} : " + rt + "{" + str(b) + "}" + f" = {x} : {y} " + B + "]"
    return rat(1, x, y, trad, f"{name.capitalize()} ratio of " + R(a, b) + ".", sub)


# ---------- Rule 2
def r2_find(a, b, c, d):
    """a : b :: c : d with exactly one of them None (the unknown)."""
    t = [a, b, c, d]
    i = t.index(None)
    t = [F(s) if s is not None else None for s in t]
    a2, b2, c2, d2 = t
    if i == 3:
        v = b2 * c2 / a2
    elif i == 0:
        v = b2 * c2 / d2
    elif i == 1:
        v = a2 * d2 / c2
    else:
        v = a2 * d2 / b2
    show = [nf(s) if s is not None else "x" for s in t]
    full = [nf(s) if s is not None else nf(v) for s in t]
    ext = "a\\times d" if i in (1, 2) else "b\\times c"
    trad = [("Write the proportion as equal fractions.", rf"\[ \frac{{{show[0]}}}{{{show[1]}}} = \frac{{{show[2]}}}{{{show[3]}}} \]"),
            ("Solve for x.", rf"\[ x = {nf(v)} \]Check: \(\frac{{{full[0]}}}{{{full[1]}}} = \frac{{{full[2]}}}{{{full[3]}}}\).")]
    ident = rf"\({show[0]} : {show[1]} :: {show[2]} : {show[3]}\)."
    if i == 3:
        sub = rf"\[ x = \frac{{{show[1]}\times {show[2]}}}{{{show[0]}}} = {nf(v)} \]"
    elif i == 0:
        sub = rf"\[ x\times {show[3]} = {show[1]}\times {show[2]} \;\Rightarrow\; x = {nf(v)} \]"
    else:
        sub = rf"\[ {show[0]}\times {show[3]} = {show[1]}\times {show[2]} \;\Rightarrow\; x = {nf(v)} \]"
    return num(2, v, trad, ident, sub)


def r2_mean(a, d):
    """a : x :: x : d (the same unknown twice)."""
    a, d = F(a), F(d)
    p = a * d
    v = F(isqrt(p.numerator), isqrt(p.denominator))
    assert v * v == p
    trad = [("Write the proportion as equal fractions.", rf"\[ \frac{{{nf(a)}}}{{x}} = \frac{{x}}{{{nf(d)}}} \]"),
            ("Solve.", rf"\(x\times x = {nf(a)}\times {nf(d)} = {nf(p)}\), and \({nf(v)}\times {nf(v)} = {nf(p)}\), so \(x = {nf(v)}\).")]
    return num(2, v, trad, rf"\({nf(a)} : x :: x : {nf(d)}\) - the means are both \(x\).", rf"\[ x^{{2}} = {nf(a)}\times {nf(d)} = {nf(p)} \;\Rightarrow\; x = {nf(v)} \]")


# ---------- Rule 3
def fr(v):
    v = F(v)
    return nf(v) if v.denominator == 1 or (v * 100).denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def r3_third(a, b):
    a, b = F(a), F(b)
    v = b * b / a
    trad = [("Continued proportion.", rf"\({fr(a)} : {fr(b)} = {fr(b)} : x\), so \(\frac{{{fr(a)}}}{{{fr(b)}}} = \frac{{{fr(b)}}}{{x}}\)."),
            ("Solve.", rf"\[ x = \frac{{{fr(b)}}}{{{fr(a)}}}\times {fr(b)} = {nf(v)} \]")]
    return num(3, v, trad, rf"\(a = {fr(a)}\), \(b = {fr(b)}\).", rf"\[ c = \frac{{{fr(b)}^{{2}}}}{{{fr(a)}}} = \frac{{{fr(b * b)}}}{{{fr(a)}}} = {nf(v)} \]")


def r3_mean(a, c):
    a, c = F(a), F(c)
    p = a * c
    v = F(isqrt(p.numerator), isqrt(p.denominator))
    assert v * v == p
    trad = [("Continued proportion.", rf"\({fr(a)} : x = x : {fr(c)}\), so \(x\times x = {fr(a)}\times {fr(c)} = {fr(p)}\)."),
            ("Find the number.", rf"\({fr(v)}\times {fr(v)} = {fr(p)}\), so \(x = {fr(v)}\).")]
    return num(3, v, trad, rf"\(a = {fr(a)}\), \(c = {fr(c)}\).", rf"\[ b = \sqrt{{{fr(a)}\times {fr(c)}}} = \sqrt{{{fr(p)}}} = {fr(v)} \]")


# ---------- Rule 4
def r4_chain(base, unit, factors, after=None):
    """base value for the old situation; factors = [(what, old, new, 'up' if the answer grows with it else 'down')]."""
    v = F(base)
    rows, ratios = [], []
    for what, old, new, way in factors:
        old, new = F(old), F(new)
        prev = v
        if way == "up":
            one = v / old
            v = one * new
            rows.append((rf"Change {what} from \({nf(old)}\) to \({nf(new)}\).",
                         rf"For {what} \(= 1\) it is \({nf(prev)} \div {nf(old)} = {nf(one)}\); for \({nf(new)}\) it is \({nf(one)}\times {nf(new)} = {nf(v)}\)."))
            ratios.append((new, old))
        else:
            one = v * old
            v = one / new
            rows.append((rf"Change {what} from \({nf(old)}\) to \({nf(new)}\).",
                         rf"For {what} \(= 1\) it is \({nf(prev)}\times {nf(old)} = {nf(one)}\); for \({nf(new)}\) it is \({nf(one)} \div {nf(new)} = {nf(v)}\)."))
            ratios.append((old, new))
    means = r" \times ".join(nf(p) for p, _ in ratios)
    firsts = r" \times ".join(nf(q) for _, q in ratios)
    sub = rf"\[ \frac{{{nf(base)}\times {means}}}{{{firsts}}} = {nf(v)} \]"
    ident = "Third term " + UU(base, unit) + "; " + ", ".join(rf"{w}: \({nf(o)} \to {nf(n)}\) ({'more' if d == 'up' else 'less'})" for w, o, n, d in factors) + "."
    if after:
        label, fn = after
        w = fn(v)
        rows.append((label, rf"\[ {nf(w)} \]"))
        sub += label + rf" \({nf(w)}\)."
        v = w
    return num(4, v, rows, ident, sub, unit)


def r4_short(n, d1, d2):
    """a group promises a job in d1 days; n stay away; the rest take d2 days -> the group at first."""
    n, d1, d2 = map(F, (n, d1, d2))
    v = n * d2 / (d2 - d1)
    trad = [("The work in man-days.", rf"\(x\) workers for \({nf(d1)}\) days \(=\) \((x-{nf(n)})\) workers for \({nf(d2)}\) days: \({nf(d1)}x = {nf(d2)}(x-{nf(n)})\)."),
            ("Solve.", rf"\({nf(d2 - d1)}x = {nf(n * d2)}\), so \(x = {nf(v)}\).")]
    sub = rf"Workers \(\propto \frac{{1}}{{\text{{days}}}}\): \(x : (x-{nf(n)}) = {nf(d2)} : {nf(d1)}\); the terms differ by \({nf(n)}\) and \({nf(d2 - d1)}\), so \(x = \frac{{{nf(d2)}\times {nf(n)}}}{{{nf(d2 - d1)}}} = {nf(v)}\)."
    return num(4, v, trad, rf"\({nf(n)}\) absent, \({nf(d1)}\) days planned, \({nf(d2)}\) days taken.", sub)


# ---------- Rule 5
def r5_split(a, b, x, ask, unit=""):
    a, b, x = map(F, (a, b, x))
    k = x / (a + b)
    p, q = a * k, b * k
    trad = [("Value of one part.", rf"The numbers are \({nf(a)}k\) and \({nf(b)}k\): \({nf(a + b)}k = {nf(x)}\), so \(k = {nf(k)}\)."),
            ("The numbers.", rf"\({nf(a)}\times {nf(k)} = {nf(p)}\) and \({nf(b)}\times {nf(k)} = {nf(q)}\).")]
    sub = rf"\[ \frac{{{nf(a)}\times {nf(x)}}}{{{nf(a + b)}}} = {nf(p)},\qquad \frac{{{nf(b)}\times {nf(x)}}}{{{nf(a + b)}}} = {nf(q)} \]"
    ident = rf"\(a = {nf(a)}\), \(b = {nf(b)}\), \(x = {nf(x)}\)."
    if ask == "both":
        fin = (f"Rs {M(nf(p))} and Rs {M(nf(q))}" if unit == "Rs" else f"{M(nf(p))} and {M(nf(q))}" + (f" {unit}" if unit else ""))
        return result(("pair", (p, q)), T(5), steps(*trad), rule_steps(5, ident, sub), fin, [ident, rf"Numbers \(= {nf(p)}\) and \({nf(q)}\)."], sub)
    extra = {"first": (p, "The first"), "second": (q, "The second"), "diff": (abs(p - q), "Difference"), "prod": (p * q, "Product")}[ask]
    v, label = extra
    trad.append((f"{label}.", rf"\[ {nf(v)} \]"))
    return num(5, v, trad, ident, sub + rf"{label} \(= {nf(v)}\).", unit)


C = card
CARDS = {
    1: C(1, "Compound, Duplicate and Triplicate Ratios", r"Multiply antecedents together and consequents together; a ratio compounded with itself gives its duplicate.",
         r"\[ (a : b)(c : d) = ac : bd \]", [("Duplicate", r"a^{2} : b^{2}"), ("Triplicate", r"a^{3} : b^{3}"), ("Subduplicate / subtriplicate", r"\sqrt{a} : \sqrt{b},\ \sqrt[3]{a} : \sqrt[3]{b}")],
         r"Treat each ratio as a fraction; compounding is multiplying the fractions. Always reduce the result to lowest terms.",
         "'Find the ratio compounded of ...' / 'Find the duplicate (subduplicate, triplicate, subtriplicate) ratio of ...'.",
         r"\(2 : 3\) and \(9 : 10\): \(18 : 30 = 3 : 5\).", r"Adding the terms instead of multiplying them."),
    2: C(2, "Four Numbers in Proportion", r"\(a : b :: c : d\) means \(\frac{a}{b} = \frac{c}{d}\); the extremes are \(a, d\) and the means \(b, c\).", r"\[ ad = bc \]",
         [("Proportion", r"a : b :: c : d"), ("Cross product", r"ad = bc"), ("Fourth proportional", r"d = \frac{bc}{a}")],
         r"Multiplying both sides of \(\frac{a}{b} = \frac{c}{d}\) by \(bd\) gives \(ad = bc\), whichever term is missing.",
         "'Find a fourth proportional to a, b and c' / 'Find the missing number: a : ? :: c : d'.", r"\(4, 6, 10\): \(\frac{6\times 10}{4}=15\).",
         r"Dividing by the wrong term (the first term goes in the denominator for the fourth proportional)."),
    3: C(3, "Third and Mean Proportionals", r"In continued proportion \(a : b = b : c\), the middle term is shared.", r"\[ c = \frac{b^{2}}{a},\quad b = \sqrt{ac} \]",
         [("Continued proportion", r"a : b = b : c"), ("Third proportional", r"\frac{b^{2}}{a}"), ("Mean proportional", r"\sqrt{ac}")],
         r"The mean proportional between two numbers is the square root of their product.", "'Find the third proportional to a and b' / 'Find the mean proportional between a and c'.",
         r"Third proportional to \(4\) and \(6\): \(9\); mean proportional between \(4\) and \(9\): \(6\).", r"Using \(\frac{a+c}{2}\) for the mean proportional."),
    4: C(4, "Rule of Three and Compound Proportion", r"Set the unknown as the fourth term; arrange each pair of like quantities so the ratio moves the answer the right way.",
         r"\[ \text{Required} = \frac{\text{Product of the means}}{\text{Product of the first terms}} \]",
         [("More gives more", r"\times\frac{\text{new}}{\text{old}}"), ("More gives less", r"\times\frac{\text{old}}{\text{new}}"), ("Several changes", r"\text{multiply all the ratios}")],
         r"Ask for each changed quantity: does the answer grow or shrink with it? More men need fewer days; more work needs more days; a higher price buys less.",
         "'If 15 books cost Rs 35, what do 21 cost?' / 'If m men do w units in d days ...' (compound proportion).",
         r"\(8\) workers, \(12\) days; \(6\) workers take \(12\times\frac{8}{6}=16\) days.", r"Using a direct ratio where the quantities are inversely related."),
    5: C(5, "Dividing a Sum in a Ratio", r"Split the sum into \(a+b\) equal parts; each number gets its share of parts.", r"\[ \frac{ax}{a+b},\quad \frac{bx}{a+b} \]",
         [("Parts", r"a+b"), ("One part", r"\frac{x}{a+b}"), ("Numbers", r"a\times\text{part},\ b\times\text{part}")],
         r"The difference of the two numbers is \(\frac{(a-b)x}{a+b}\) and their product is \(\frac{abx^{2}}{(a+b)^{2}}\).",
         "'Two numbers are in the ratio a : b and their sum is x; find the numbers (or their difference / product).'",
         r"Ratio \(2 : 3\), sum \(40\): \(16\) and \(24\).", r"Dividing the sum by \(a\) or \(b\) instead of \(a+b\)."),
}
OLD = {   # row: (rule, question, builder, options kind)
    708: (2, "Find the fourth proportional to 9, 12 and 21.", lambda: r2_find(9, 12, 21, None), ""),
    709: (3, "Three numbers are in continued proportion. The first is 12 and the second is 18. What is the third?", lambda: r3_third(12, 18), ""),
    710: (3, "A number x makes 7 : x = x : 63 a true proportion. What is x?", lambda: r3_mean(7, 63), ""),
    711: (4, "If 12 pens cost Rs 54, what will 20 pens cost?", lambda: r4_chain(54, "Rs", [("the pens", 12, 20, "up")]), "Rs"),
    712: (4, "If 18 workers can paint a hall in 20 days, how many days will 24 workers take to paint it?",
          lambda: r4_chain(20, "days", [("the workers", 18, 24, "down")]), "days"),
    713: (5, "Two numbers are in the ratio 5 : 3 and their sum is 336. Find the numbers.", lambda: r5_split(5, 3, 336, "both"), "pair"),
    714: (5, "In a club the ratio of men to women is 4 : 7. If there are 286 members, how many women are there?", lambda: r5_split(4, 7, 286, "second"), ""),
}
NEW = {   # rule: [(key, question, builder, options kind, wrong options or None)]
    1: [("r1_ex", "Find the ratio compounded of 5 : 6, 8 : 15, 9 : 4 and 2 : 3.", lambda: r1_comp([(5, 6), (8, 15), (9, 4), (2, 3)]), "ratio", None),
        ("r1_e1", "What is the compound ratio of 2 : 3, 9 : 14 and 7 : 12?", lambda: r1_comp([(2, 3), (9, 14), (7, 12)]), "ratio", None),
        ("r1_e2", "What single ratio do 4 : 9, 27 : 16 and 8 : 3 make when they are compounded?", lambda: r1_comp([(4, 9), (27, 16), (8, 3)]), "ratio", None),
        ("r1_e3", "Find the ratio compounded of 7 : 10, 15 : 28, 16 : 9 and 9 : 4.", lambda: r1_comp([(7, 10), (15, 28), (16, 9), (9, 4)]), "ratio", None),
        ("r1_e4", "What is the subduplicate ratio of 36 : 121?", lambda: r1_power(36, 121, -2), "ratio", None),
        ("r1_e5", "Find the subtriplicate ratio of 64 : 125.", lambda: r1_power(64, 125, -3), "ratio", None),
        ("r1_e6", "What is the duplicate ratio of 11 : 13?", lambda: r1_power(11, 13, 2), "ratio", None),
        ("r1_e7", "Find the triplicate ratio of 2 : 7.", lambda: r1_power(2, 7, 3), "ratio", None)],
    2: [("r2_e1", "Find a fourth proportional to 4, 18 and 22.", lambda: r2_find(4, 18, 22, None), "", None),
        ("r2_e2", "Find the missing number: 8 : ? :: 6 : 27.", lambda: r2_find(8, None, 6, 27), "", None),
        ("r2_e3", "What is the fourth proportional to 15, 18 and 35?", lambda: r2_find(15, 18, 35, None), "", None),
        ("r2_e4", "Find a fourth proportional to the numbers 6, 11 and 24.", lambda: r2_find(6, 11, 24, None), "", None),
        ("r2_e5", "Find the fourth proportional to 16, 26 and 40.", lambda: r2_find(16, 26, 40, None), "", None),
        ("r2_e6", "What is the fourth proportional to 35, 42 and 55?", lambda: r2_find(35, 42, 55, None), "", None),
        ("r2_e7", "Find the missing number: ? : 17 :: 24 : 68.", lambda: r2_find(None, 17, 24, 68), "", None),
        ("r2_e8", "Find x if 9 : 27 = 5 : x.", lambda: r2_find(9, 27, 5, None), "", None),
        ("r2_e9", "Find x if 96 : 8 = x : 7.", lambda: r2_find(96, 8, None, 7), "", None),
        ("r2_e10", "Find a fourth proportional to 1, 4 and 5.", lambda: r2_find(1, 4, 5, None), "", None),
        ("r2_e11", "Find a fourth proportional to 400, 60 and 47.", lambda: r2_find(400, 60, 47, None), "", None),
        ("r2_e12", "Find a fourth proportional to 3.5, 2.1 and 2.5.", lambda: r2_find(F("3.5"), F("2.1"), F("2.5"), None), "", None),
        ("r2_e13", r"Which number can go in both blanks: \(\frac{18}{?} = \frac{?}{50}\)?", lambda: r2_mean(18, 50), "", None)],
    3: [("r3_e1", "Find the third proportional to 4 and 10.", lambda: r3_third(4, 10), "", None),
        ("r3_e2", "What is the third proportional to 1.6 and 2.4?", lambda: r3_third(F("1.6"), F("2.4")), "", None),
        ("r3_e3", "Find the third proportional to the numbers 144 and 60.", lambda: r3_third(144, 60), "", None),
        ("r3_e4", "Find the mean proportional between 6 and 150.", lambda: r3_mean(6, 150), "", None),
        ("r3_e5", r"What is the mean proportional between \(\frac{5}{27}\) and \(\frac{12}{125}\)?", lambda: r3_mean(F(5, 27), F(12, 125)), "frac",
         [F(1, 15), F(4, 15), F(2, 45)]),
        ("r3_e6", "Find the mean proportional between 0.2 and 2000.", lambda: r3_mean(F("0.2"), 2000), "", None),
        ("r3_e7", "Find the third proportional to 6 and 15.", lambda: r3_third(6, 15), "", None)],
    4: [("r4_ex3", "A camp had food for 240 people for 50 days. After 14 days, 60 people left. How long will the rest of the food last for those who stay?",
         lambda: r4_chain(36, "days", [("the people", 240, 180, "down")]), "days", None),
        ("r4_ex4", "If 6 tractors can plough 90 acres in 15 days, how many acres can 10 tractors plough in 12 days?",
         lambda: r4_chain(90, "acres", [("the tractors", 6, 10, "up"), ("the days", 15, 12, "up")]), "acres", None),
        ("r4_e1", "If 24 men do a job in 35 days, in how many days will 28 men do a job twice as big?",
         lambda: r4_chain(35, "days", [("the men", 24, 28, "down"), ("the work", 1, 2, "up")]), "days", None),
        ("r4_e2", "When rice is Rs 4.50 a kg, 48 people can be fed for 18 days at a certain cost. How many people can be fed for 24 days at the same cost "
                  "when rice is Rs 3.60 a kg?", lambda: r4_chain(48, "people", [("the days", 18, 24, "down"), ("the price", F("4.5"), F("3.6"), "down")]), "people", None),
        ("r4_e3", "A family of 6 can live on Rs 9000 for 30 days. How long can a family of 8 live on Rs 10800?",
         lambda: r4_chain(30, "days", [("the family", 6, 8, "down"), ("the money", 9000, 10800, "up")]), "days", None),
        ("r4_e4", "If 500 copies of a book of 12 sheets need 15 reams of paper, how many reams are needed for 2000 copies of a book of 18 sheets?",
         lambda: r4_chain(15, "reams", [("the copies", 500, 2000, "up"), ("the sheets", 12, 18, "up")]), "reams", None),
        ("r4_e5", "6 cows eat 24 kg of fodder in 8 days. At the same rate, how long will 45 kg of fodder last 9 cows?",
         lambda: r4_chain(8, "days", [("the fodder", 24, 45, "up"), ("the cows", 6, 9, "down")]), "days", None),
        ("r4_e6", "Carrying 600 kg of goods for 50 km costs Rs 90. What will it cost to carry 720 kg for 45 km at half that rate?",
         lambda: r4_chain(90, "Rs", [("the weight", 600, 720, "up"), ("the distance", 50, 45, "up"), ("the rate", 1, F(1, 2), "up")]), "Rs", None),
        ("r4_e7", r"If 240 men can do a job in 20 days, how many men can do \(\frac{1}{3}\) of the job in 16 days?",
         lambda: r4_chain(240, "men", [("the days", 20, 16, "down"), ("the work", 1, F(1, 3), "up")]), "men", None),
        ("r4_e8", "If 18 men take 12 days to mow 144 hectares, how long will 24 men take to mow 240 hectares?",
         lambda: r4_chain(12, "days", [("the men", 18, 24, "down"), ("the land", 144, 240, "up")]), "days", None),
        ("r4_e9", "How many oxen are needed to plough 150 hectares in 25 days, if 12 oxen plough 18 hectares in 6 days?",
         lambda: r4_chain(12, "oxen", [("the land", 18, 150, "up"), ("the days", 6, 25, "down")]), "oxen", None),
        ("r4_e10", "If 8 men can do a job in 24 days working 10 hours a day, how many men are needed to do 5 times the job in 40 days working 8 hours a day?",
         lambda: r4_chain(8, "men", [("the work", 1, 5, "up"), ("the days", 24, 40, "down"), ("the hours a day", 10, 8, "down")]), "men", None),
        ("r4_e11", "I walk a certain distance in 40 days, resting 8 hours a day. How long will I take to walk 3 times as far, walking 2 times as fast and "
                   "resting 14 hours a day?", lambda: r4_chain(40, "days", [("the distance", 1, 3, "up"), ("the speed", 1, 2, "down"), ("the walking hours a day", 16, 10, "down")]),
         "days", None),
        ("r4_e12", "A camp of 1800 soldiers has food for 20 weeks at 40 dag a day per man. How many soldiers must leave so that the food lasts 30 weeks at "
                   "32 dag a day per man?", lambda: r4_chain(1800, "", [("the weeks", 20, 30, "down"), ("the daily share", 40, 32, "down")],
                                                             after=("Soldiers who must leave: 1800 minus that:", lambda v: 1800 - v)), "", None),
        ("r4_e13", "A group of workers agree to finish a job in 12 days, but 8 of them stay away and the rest finish it in 16 days. How many workers were there at first?",
         lambda: r4_short(8, 12, 16), "", None),
        ("r4_e14", "A man walks 480 km in 30 days, resting 12 hours a day. How long will he take to walk 630 km if he rests 15 hours a day and walks 2 times as fast?",
         lambda: r4_chain(30, "days", [("the distance", 480, 630, "up"), ("the speed", 1, 2, "down"), ("the walking hours a day", 12, 9, "down")]), "days", None),
        ("r4_e15", "Two teams of 8 and 12 workers dig two ponds of 40 and 54 cubic metres. The first team takes 10 days. In how many days will the second team finish?",
         lambda: r4_chain(10, "days", [("the earth", 40, 54, "up"), ("the workers", 8, 12, "down")]), "days", None),
        ("r4_e16", "If 12 masons build a wall 60 m long in 20 days of 9 hours each, in how many days of 8 hours will 18 masons build a wall 48 m long?",
         lambda: r4_chain(20, "days", [("the length", 60, 48, "up"), ("the masons", 12, 18, "down"), ("the hours a day", 9, 8, "down")]), "days", None)],
    5: [("r5_e1", "Two numbers in the ratio 7 : 6 add up to 520. Find the numbers.", lambda: r5_split(7, 6, 520, "both"), "pair", None),
        ("r5_e2", "Two numbers are in the ratio 5 : 8 and their sum is 728. What is the difference between them?", lambda: r5_split(5, 8, 728, "diff"), "", None),
        ("r5_e3", "Two numbers in the ratio 3 : 7 have a sum of 60. Find their product.", lambda: r5_split(3, 7, 60, "prod"), "", None),
        ("r5_e4", "The ratio of boys to girls in a camp is 9 : 11. If there are 500 children, how many more girls than boys are there?",
         lambda: r5_split(9, 11, 500, "diff"), "", None),
        ("r5_e5", "The ratio of the village and town people of a district is 7 : 4. If the district has 990000 people, how many live in the town?",
         lambda: r5_split(7, 4, 990000, "second"), "", None)],
}


def build_opts(g, kind, wrong):
    a = g["answer"]
    if a[0] == "ratio":
        return ratio_opts(*a[1], wrong)
    if a[0] == "pair":
        return pair_opts(*a[1], "Rs" if kind == "pair_rs" else "", wrong)
    if a[0] == "triple":
        return triple_opts(*a[1], "", wrong)
    if a[0] == "terms":
        from fmt import terms_opts
        return terms_opts(a[1], wrong)
    if kind == "frac":
        f = lambda v: M(nf(v))
        from helpers import place
        return place(f(a[1]), [f(w) for w in wrong])
    return opts(a[1], kind if kind not in ("pair", "ratio") else "", wrong)


def main(old=OLD, new=NEW, cards=CARDS, rules=range(1, 6)):
    for rule in rules:
        folder = os.path.join(HERE, f"rule{rule:02d}")
        ids = [rid for rid, v in old.items() if v[0] == rule]
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(ids), (rule, sorted(rows), ids)
        if ids:
            out = []
            for rid in ids:
                _, q, fn, kind = old[rid]
                g = fn()
                op, _ = build_opts(g, kind, None)
                extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
                extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
                out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
            json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cc = {"rule_name": f"Rule {rule}", "rule_html": cards[rule]}
        json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, kind, wrong in new.get(rule, []):
            g = fn()
            op, pos = build_opts(g, kind, wrong)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        json.dump({"rules_html": [{"chapter": "ratio_n_proportion", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(ids)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
