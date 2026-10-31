"""Ratio and Proportion Rules 18-25 (2026-10-30). Rule 18: efficiency - days are inversely proportional to efficiency. Rule 19: water
to add to change milk : water from a : b to c : d - x(ad - bc)/(c(a + b)). Rule 20: x litres of water turn a : b into a : c - milk
ax/(c - b), water bx/(c - b). Rule 21: X : Y = x : y gives X + Y : X - Y = x + y : x - y. Rule 22: areas go as the squares of the
sides. Rule 23: volumes go as the cubes. Rule 24: each number changed by x turns a : b into c : d - xa(c - d)/(ad - bc) and
xb(c - d)/(ad - bc). Rule 25: the same when c - a = d - b - ax/(c - a), bx/(c - a). Writes the eight cards, regenerates the old
rows 727-733 (730's key said 1 : 9 for an area that grows 9 times; 733's key was on the empty option e - the numbers 18 and 24
were in no option) and adds the book's examples and exercises with no copy. Book slips: Rule 18 Exr 5 says '25% more efficient'
but answers for 25% less; Rule 22 Exr 5 asks old : new and marks 25 : 1. Usage: python gen_18_25.py"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from fmt import M, R, UU, low, nf  # noqa: E402
from gen_1_5 import main  # noqa: E402
from helpers import result  # noqa: E402

TH = {
    18: (r"If B is \(p\%\) more (or less) efficient than A, the days they take are in the inverse ratio of their efficiencies:",
         r"\[ \text{Days of B} = \text{Days of A}\times\frac{100}{100\pm p} \]"),
    19: (r"If \(x\) litres of a mixture have milk and water in the ratio \(a : b\), the water to be added to make the ratio \(c : d\) is",
         r"\[ \frac{x(ad-bc)}{c(a+b)} \]"),
    20: (r"If a mixture has milk and water in the ratio \(a : b\) and adding \(x\) litres of water makes it \(a : c\), it held",
         r"\[ \text{milk} = \frac{ax}{c-b},\qquad \text{water} = \frac{bx}{c-b} \]"),
    21: (r"If two quantities X and Y are in the ratio \(x : y\), then", r"\[ X+Y : X-Y = x+y : x-y \]"),
    22: (r"For two figures of the same shape whose sides (or any matching lengths) are in the ratio \(a : b\), the areas are in the ratio", r"\[ a^{2} : b^{2} \]"),
    23: (r"For two solids of the same shape whose sides (or any matching lengths) are in the ratio \(a : b\), the volumes are in the ratio", r"\[ a^{3} : b^{3} \]"),
    24: (r"If two numbers are in the ratio \(a : b\) and adding \(x\) to each makes the ratio \(c : d\) (with \(c-a \ne d-b\)), the numbers are",
         r"\[ \frac{xa(c-d)}{ad-bc}\quad\text{and}\quad\frac{xb(c-d)}{ad-bc} \]"),
    25: (r"If two numbers are in the ratio \(a : b\) and adding \(x\) to each makes the ratio \(c : d\) with \(c-a = d-b\), the numbers are",
         r"\[ \frac{ax}{c-a}\quad\text{and}\quad\frac{bx}{c-a} \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rsteps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def done(r, ans, fin, trad, ident, sub):
    return result(ans, T(r), steps(*trad), rsteps(r, ident, sub), fin, [ident, "Answer " + fin + "."], sub)


def num(r, v, trad, ident, sub, unit=""):
    return done(r, ("number", F(v)), UU(v, unit), trad, ident, sub)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


# ---------- Rule 18
def r18(days, p, more=True):
    days, p = F(days), F(p)
    eb = 100 + p if more else 100 - p
    v = days * 100 / eb
    trad = [("Work in efficiency units.", rf"Let A do \(100\) units a day; B does \({nf(eb)}\). The job is \(100\times {nf(days)} = {nf(100 * days)}\) units."),
            ("Days for B.", rf"\[ {nf(100 * days)} \div {nf(eb)} = {nf(v)} \]")]
    sub = rf"\[ {nf(days)}\times\frac{{100}}{{100{'+' if more else '-'}{nf(p)}}} = {nf(v)} \]"
    return num(18, v, trad, rf"A takes \({nf(days)}\) days; B is \({nf(p)}\%\) {'more' if more else 'less'} efficient.", sub, "days")


# ---------- Rule 19
def r19(x, a, b, c, d):
    x = F(x)
    milk, water = x * a / (a + b), x * b / (a + b)
    need = milk * d / c
    v = need - water
    trad = [("Milk and water now.", rf"Milk \(= {nf(milk)}\), water \(= {nf(water)}\) litres."),
            ("Water needed.", rf"For milk : water \(= {c} : {d}\) the water must be \({nf(milk)}\times\frac{{{d}}}{{{c}}} = {nf(need)}\) litres; add \({nf(need)} - {nf(water)} = {nf(v)}\).")]
    sub = rf"\[ \frac{{{nf(x)}({a}\times {d}-{b}\times {c})}}{{{c}({a}+{b})}} = \frac{{{nf(x * (a * d - b * c))}}}{{{c * (a + b)}}} = {nf(v)} \]"
    return num(19, v, trad, rf"\(x = {nf(x)}\), \(a : b = {a} : {b}\), \(c : d = {c} : {d}\).", sub, "litres")


# ---------- Rule 20
def r20(a, b, x, p, q, ask):
    """milk : water = a : b; adding x litres of water makes it p : q (written as a : c with c = qa/p)."""
    c = F(q * a, p)
    milk, water = a * F(x) / (c - b), b * F(x) / (c - b)
    trad = [("Milk does not change.", rf"Write the new ratio with the same milk term: \({p} : {q} = {a} : {nf(c)}\). The water went from \({b}\) parts to \({nf(c)}\) parts."),
            ("Value of one part.", rf"\({nf(c - b)}\) parts \(= {nf(x)}\) litres, so one part \(= {nf(F(x) / (c - b))}\); milk \(= {nf(milk)}\), water \(= {nf(water)}\).")]
    sub = rf"\[ \text{{milk}} = \frac{{{a}\times {nf(x)}}}{{{nf(c)}-{b}}} = {nf(milk)},\qquad \text{{water}} = \frac{{{b}\times {nf(x)}}}{{{nf(c)}-{b}}} = {nf(water)} \]"
    ident = rf"\(a : b = {a} : {b}\), \(x = {nf(x)}\), new ratio \({a} : {nf(c)}\)."
    if ask == "both":
        return done(20, ("pair", (milk, water)), f"milk {M(nf(milk))} litres and water {M(nf(water))} litres", trad, ident, sub)
    v, how = {"milk": (milk, "milk"), "water": (water, "water"), "start": (milk + water, "the mixture at first"),
              "end": (milk + water + x, "the mixture now")}[ask]
    trad.append(("What is asked.", rf"{how.capitalize()} \(= {nf(v)}\) litres."))
    return num(20, v, trad, ident, sub + rf"{how.capitalize()} \(= {nf(v)}\).", "litres")


# ---------- Rule 21
def r21(x, y, diff, ask, unit="Rs"):
    x, y, diff = F(x), F(y), F(diff)
    big, small = max(x, y), min(x, y)
    s = diff * (x + y) / (big - small)
    k = diff / (big - small)
    trad = [("Value of one part.", rf"The shares are \({nf(x)}k\) and \({nf(y)}k\); they differ by \({nf(big - small)}k = {nf(diff)}\), so \(k = {nf(k)}\)."),
            ("What is asked.", "")]
    sub = rf"\[ \frac{{X+Y}}{{X-Y}} = \frac{{{nf(x + y)}}}{{{nf(big - small)}}} \;\Rightarrow\; X+Y = \frac{{{nf(x + y)}}}{{{nf(big - small)}}}\times {nf(diff)} = {nf(s)} \]"
    ident = rf"\(x : y = {nf(x)} : {nf(y)}\), \(X - Y = {nf(diff)}\)."
    if ask == "sum":
        v = s
        trad[1] = ("The whole amount.", rf"\({nf(x + y)}k = {nf(v)}\).")
    else:
        v = small * k
        trad[1] = ("The smaller one.", rf"\({nf(small)}k = {nf(v)}\).")
        sub += rf"The smaller \(= \frac{{{nf(small)}}}{{{nf(x + y)}}}\times {nf(s)} = {nf(v)}\)."
    return num(21, v, trad, ident, sub, unit)


# ---------- Rules 22 and 23
def r_power(rule, a, b, root=False):
    k = 2 if rule == 22 else 3
    if root:                                            # areas (volumes) given -> sides
        x = next(i for i in range(1, 1000) if i ** k == a)
        y = next(i for i in range(1, 1000) if i ** k == b)
        trad = [("Lengths that make the areas.", rf"\({x}^{{{k}}} = {a}\) and \({y}^{{{k}}} = {b}\)."), ("Ratio.", rf"Sides \({x} : {y}\).")]
        sub = rf"\[ \sqrt{{{a}}} : \sqrt{{{b}}} = {x} : {y} \]"
        return done(rule, ("ratio", (x, y)), R(x, y), trad, rf"Areas \({a} : {b}\).", sub)
    x, y = a ** k, b ** k
    word = "area" if k == 2 else "volume"
    trad = [(f"Scale the {word}.", rf"Every length of the second is \(\frac{{{b}}}{{{a}}}\) of the first, so its {word} is \(\left(\frac{{{b}}}{{{a}}}\right)^{{{k}}} = \frac{{{y}}}{{{x}}}\) of it."),
            ("Ratio.", rf"\[ {x} : {y} \]")]
    sub = rf"\[ {a}^{{{k}}} : {b}^{{{k}}} = {x} : {y} \]"
    x2, y2 = low(x, y)
    return done(rule, ("ratio", (x2, y2)), R(x2, y2), trad, rf"Lengths \({a} : {b}\).", sub)


# ---------- Rules 24 and 25
def r24(a, b, x, c, d):
    """a : b, each number changed by x (x < 0 for a decrease) -> c : d."""
    k = F(x * (c - d), a * d - b * c) if (c - a != d - b) else F(x, c - a)
    p, q = a * k, b * k
    assert F(p + x, q + x) == F(c, d)
    sign = "+" if x > 0 else "-"
    trad = [("Write the numbers as parts.", rf"Let them be \({a}k\) and \({b}k\): \(\frac{{{a}k {sign} {abs(x)}}}{{{b}k {sign} {abs(x)}}} = \frac{{{c}}}{{{d}}}\)."),
            ("Solve.", rf"\({d}({a}k {sign} {abs(x)}) = {c}({b}k {sign} {abs(x)})\), so \(k = {nf(k)}\): the numbers are \({nf(p)}\) and \({nf(q)}\).")]
    return trad, k, p, q


def r24_build(a, b, x, c, d):
    trad, k, p, q = r24(a, b, x, c, d)
    sub = rf"\[ \frac{{{x}\times {a}({c}-{d})}}{{{a}\times {d}-{b}\times {c}}} = {nf(p)},\qquad \frac{{{x}\times {b}({c}-{d})}}{{{a}\times {d}-{b}\times {c}}} = {nf(q)} \]"
    ident = rf"\(a : b = {a} : {b}\), \(x = {x}\), \(c : d = {c} : {d}\) (\(c-a \ne d-b\))."
    return done(24, ("pair", (p, q)), f"{M(nf(p))} and {M(nf(q))}", trad, ident, sub)


def r25_build(a, b, x, c, d, s=1):
    """c : d is the ratio scaled by s so that its terms differ from a : b by the same amount."""
    cc, dd = c * s, d * s
    trad, k, p, q = r24(a, b, x, cc, dd)
    extra = rf"Write \({c} : {d}\) as \({cc} : {dd}\), so " if s != 1 else ""
    sub = extra + rf"\(c - a = {cc}-{a} = {dd}-{b} = d - b = {cc - a}\): \[ \frac{{{a}\times {x}}}{{{cc - a}}} = {nf(p)},\qquad \frac{{{b}\times {x}}}{{{cc - a}}} = {nf(q)} \]"
    ident = rf"\(a : b = {a} : {b}\), \(x = {x}\), \(c : d = {cc} : {dd}\)."
    return done(25, ("pair", (p, q)), f"{M(nf(p))} and {M(nf(q))}", trad, ident, sub)


def r25_classes(parts, x, new, now=False):
    d = new[0] - parts[0]
    assert all(n - p == d for p, n in zip(parts, new))
    k = F(x, d)
    total = sum(parts) * k
    v = total + 3 * x if now else total
    trad = [("Each class changes by the same number.", rf"Every term {'rises' if d > 0 else 'falls'} by \({abs(d)}\) (from \({' : '.join(map(str, parts))}\) to \({' : '.join(map(str, new))}\)), "
                                                       rf"and every class {'gains' if x > 0 else 'loses'} \({abs(x)}\) pupils: \({abs(d)}\) parts \(= {abs(x)}\)."),
            ("Total.", rf"One part \(= {nf(k)}\); before: \({sum(parts)}\times {nf(k)} = {nf(total)}\)" + (rf"; now \({nf(total)} {'+' if x > 0 else '-'} 3\times {abs(x)} = {nf(v)}\)." if now else "."))]
    sub = rf"\[ \frac{{({' + '.join(map(str, parts))})\times {abs(x)}}}{{{abs(d)}}} = {nf(total)} \]" + (rf"Now \(= {nf(v)}\)." if now else "")
    return num(25, v, trad, rf"Ratio \({' : '.join(map(str, parts))}\) to \({' : '.join(map(str, new))}\), change \({x}\) a class.", sub, "students")


C = card
CARDS = {
    18: C(18, "Efficiency and Days", r"More efficient means more work a day, so fewer days for the same job.", r"\[ \text{Days}_B = \text{Days}_A\times\frac{100}{100\pm p} \]",
          [("Efficiency", r"100 : 100\pm p"), ("Days", r"100\pm p : 100"), ("B's days", r"\text{A's days}\times\frac{100}{100\pm p}")],
          r"Days and efficiency are in inverse proportion: work = efficiency x days stays the same.", "'A does a job in n days; B is p% more efficient; how long does B take?'",
          r"A \(15\) days, B \(50\%\) more efficient: \(15\times\frac{100}{150}=10\) days.", r"Taking \(p\%\) off A's days instead of using the inverse ratio."),
    19: C(19, "Water to Add for a New Ratio", r"The milk stays the same; only the water grows.", r"\[ \frac{x(ad-bc)}{c(a+b)} \]",
          [("Milk", r"\frac{ax}{a+b}"), ("Water needed", r"\text{milk}\times\frac{d}{c}"), ("Water to add", r"\text{needed}-\frac{bx}{a+b}")],
          r"Work out the milk, find the water the new ratio needs, and subtract the water already there.",
          "'In x litres milk : water = a : b; how much water must be added to make it c : d?'",
          r"\(40\) litres in \(3 : 1\) to \(3 : 2\): add \(10\) litres.", r"Keeping the water fixed instead of the milk."),
    20: C(20, "Mixture Found From Water Added", r"Write both ratios with the same milk term; the change in the water term is the water added.",
          r"\[ \frac{ax}{c-b},\quad \frac{bx}{c-b} \]", [("Before", r"a : b"), ("After", r"a : c"), ("x litres", r"c-b\ \text{parts}")],
          r"If the new ratio does not show the same milk term, rescale it first (e.g. \(8 : 3\) and \(2 : 1 = 8 : 4\)).",
          "'Milk and water are a : b; on adding x litres of water the ratio becomes p : q; find the quantities.'",
          r"\(3 : 2\), add \(4\) litres, becomes \(3 : 3\): milk \(12\), water \(8\).", r"Not rescaling the new ratio to the same milk term."),
    21: C(21, "Sum From a Difference", r"Componendo and dividendo: the sum and the difference keep the same proportion as \(x+y\) and \(x-y\).",
          r"\[ X+Y : X-Y = x+y : x-y \]", [("Ratio", r"x : y"), ("Difference", r"(x-y)\ \text{parts}"), ("Sum", r"(x+y)\ \text{parts}")],
          r"One part is the difference over \(x-y\); every share follows.", "'Money is divided in the ratio x : y and one gets Rs d less; find the sum.'",
          r"\(3 : 5\), difference Rs \(20\): one part Rs \(10\), sum Rs \(80\).", r"Using \(x+y\) parts for the difference."),
    22: C(22, "Areas of Similar Figures", r"Areas go as the square of the lengths - sides, diagonals, radii, perimeters.", r"\[ a^{2} : b^{2} \]",
          [("Lengths", r"a : b"), ("Areas", r"a^{2} : b^{2}"), ("Lengths from areas", r"\sqrt{A_1} : \sqrt{A_2}")],
          r"Enlarging every length \(n\) times makes the area \(n^{2}\) times. Keep the order asked (new : old or old : new).",
          "'The sides of a hexagon are enlarged three times; ratio of the areas' / 'areas are in the ratio p : q; ratio of the sides'.",
          r"Radii \(2 : 3\): areas \(4 : 9\).", r"Using the plain ratio of lengths for the areas."),
    23: C(23, "Volumes of Similar Solids", r"Volumes go as the cube of the lengths.", r"\[ a^{3} : b^{3} \]",
          [("Lengths", r"a : b"), ("Volumes", r"a^{3} : b^{3}"), ("Doubling", r"\times 8")],
          r"Doubling every edge of a box multiplies its volume by \(8\).", "'The radii of two spheres are a : b; ratio of their volumes.'",
          r"Edges \(1 : 3\): volumes \(1 : 27\).", r"Squaring instead of cubing."),
    24: C(24, "Numbers Changed by the Same Amount", r"Write the numbers as \(ak\) and \(bk\) and solve the new ratio for \(k\).",
          r"\[ \frac{xa(c-d)}{ad-bc},\quad \frac{xb(c-d)}{ad-bc} \]", [("Numbers", r"ak,\ bk"), ("Changed", r"ak+x : bk+x = c : d"), ("Solve", r"k = \frac{x(c-d)}{ad-bc}")],
          r"Adding the same number to both terms moves the ratio towards \(1\); taking it away moves the ratio away from \(1\). For a decrease use \(-x\).",
          "'The ratio of two numbers is a : b; if each is increased by x the ratio becomes c : d; find the numbers.'",
          r"\(3 : 4\), add \(2\), becomes \(7 : 9\): \(12\) and \(16\).", r"Adding \(x\) to the ratio terms instead of to the numbers."),
    25: C(25, "Same Change When c - a = d - b", r"If both terms of the ratio rise by the same amount, that amount of parts equals \(x\).", r"\[ \frac{ax}{c-a},\quad \frac{bx}{c-a} \]",
          [("Check", r"c-a = d-b"), ("One part", r"\frac{x}{c-a}"), ("Numbers", r"a,\ b\ \text{parts}")],
          r"Rescale the new ratio if needed (\(5 : 7 = 10 : 14\)) so both terms rise by the same number of parts; works for three classes too.",
          "'The ratio of two numbers is a : b; adding x to each makes it c : d (c - a = d - b)' / 'students in three classes ...'.",
          r"\(3 : 4\), add \(6\), becomes \(4 : 5\): one part \(6\), numbers \(18\), \(24\).", r"Not checking that both terms change by the same parts."),
}
OLD = {
    727: (19, "A jug has 54 litres of milk and water in the ratio 7 : 2. How much water must be added to make the ratio 2 : 1?", lambda: r19(54, 7, 2, 2, 1), "litres"),
    728: (20, "A bottle has milk and water in the ratio 16 : 11. When 14 litres of water are added, the ratio becomes 8 : 9. How much milk and how much water were there at first?",
          lambda: r20(16, 11, 14, 8, 9, "both"), "pair"),
    729: (21, "A sum of money is split between two sisters in the ratio 4 : 9. One gets Rs 75 less than the other. What was the whole amount?", lambda: r21(4, 9, 75, "sum"), "Rs"),
    730: (22, "Each side of a pentagon is made 4 times as long. What is the ratio of the area of the new pentagon to that of the old one?", lambda: r_power(22, 4, 1), "ratio"),
    731: (23, "The edges of two cubes are in the ratio 4 : 5. Find the ratio of their volumes.", lambda: r_power(23, 4, 5), "ratio"),
    732: (24, "Two numbers are in the ratio 11 : 12. If 22 is added to each, the ratio becomes 55 : 59. Find the numbers.", lambda: r24_build(11, 12, 22, 55, 59), "pair"),
    733: (25, "Two numbers are in the ratio 29 : 18. If 18 is added to each, the ratio becomes 32 : 21. Find the numbers.", lambda: r25_build(29, 18, 18, 32, 21), "pair"),
}
NEW = {
    18: [("r18_ex", "Ravi can finish a job in 21 days. Sunil is 40% more efficient than Ravi. How many days will Sunil take to do the same job?", lambda: r18(21, 40), "days", None),
         ("r18_e1", "A can do a piece of work in 44 days. B is 10% more efficient than A. In how many days can B do it?", lambda: r18(44, 10), "days", None),
         ("r18_e2", "Meena can knit a shawl in 28 days. Geeta is 40% more efficient. How long will Geeta take to knit the same shawl?", lambda: r18(28, 40), "days", None),
         ("r18_e3", "A can finish a task in 27 days. B is 10% less efficient than A. How many days will B take?", lambda: r18(27, 10, False), "days", None),
         ("r18_e4", "A machine fills an order in 42 days. A new machine is 75% more efficient. How many days will the new machine take?", lambda: r18(42, 75), "days", None),
         ("r18_e5", "A can build a wall in 36 days. B is 20% less efficient than A. How long will B take to build it?", lambda: r18(36, 20, False), "days", None)],
    19: [("r19_ex2", "In 52 litres of a mixture, milk and water are in the ratio 9 : 4. How much water should be added to make the ratio 4 : 9?", lambda: r19(52, 9, 4, 4, 9), "litres", None),
         ("r19_e1", "A can holds 77 litres of milk and water in the ratio 8 : 3. How much water must be added to make it 4 : 3?", lambda: r19(77, 8, 3, 4, 3), "litres", None),
         ("r19_e2", "In 90 litres of a mixture milk and water are 13 : 2. How much water should be added so that the ratio becomes 3 : 1?", lambda: r19(90, 13, 2, 3, 1), "litres", None),
         ("r19_e3", "A pail has 39 litres of milk and water in the ratio 10 : 3. How much water must be poured in to turn the ratio into 3 : 10?", lambda: r19(39, 10, 3, 3, 10), "litres", None),
         ("r19_e4", "A 135 litre mixture has milk and water in the ratio 11 : 4. How much water must be added to make the ratio 9 : 5?", lambda: r19(135, 11, 4, 9, 5), "litres", None),
         ("r19_e5", "In 96 litres of milk and water the ratio is 19 : 5. How much water is needed to make it 19 : 8?", lambda: r19(96, 19, 5, 19, 8), "litres", None),
         ("r19_e6", "A drum has 84 litres of milk and water in the ratio 11 : 3. How much water must be added to get the ratio 11 : 7?", lambda: r19(84, 11, 3, 11, 7), "litres", None),
         ("r19_e7", "A 66 litre mixture holds milk and water in the ratio 8 : 3. How much water must be added to make the ratio 3 : 8?", lambda: r19(66, 8, 3, 3, 8), "litres", None),
         ("r19_e8", "In a mixture of 75 litres, milk and water are in the ratio 4 : 1. To make the ratio 2 : 3, how much more water must be added?", lambda: r19(75, 4, 1, 2, 3), "litres", None)],
    20: [("r20_ex2", "A tank has milk and water in the ratio 22 : 13. When 12 litres of water are added, the ratio becomes 22 : 17. How much milk and how much water were there?",
          lambda: r20(22, 13, 12, 22, 17, "both"), "pair", None),
         ("r20_e1", "Milk and water in a can are in the ratio 22 : 9. On adding 14 litres of water the ratio becomes 11 : 8. How much mixture was in the can at first?",
          lambda: r20(22, 9, 14, 11, 8, "start"), "litres", None),
         ("r20_e2", "A mixture has milk and water in the ratio 13 : 7. When 21 litres of water are added, the ratio becomes 13 : 14. How much mixture is there now?",
          lambda: r20(13, 7, 21, 13, 14, "end"), "litres", None),
         ("r20_e3", "Milk and water are mixed in the ratio 25 : 9. After 16 litres of water are added the ratio is 25 : 17. How much milk is in the mixture?",
          lambda: r20(25, 9, 16, 25, 17, "milk"), "litres", None),
         ("r20_e4", "A jar holds milk and water in the ratio 8 : 1. Adding 6 litres of water changes the ratio to 8 : 3. How much water was in the jar at first?",
          lambda: r20(8, 1, 6, 8, 3, "water"), "litres", None),
         ("r20_e5", "Milk and water in a mug are in the ratio 21 : 13. When 21 litres of water are added, the ratio becomes 21 : 20. How much water was there at first?",
          lambda: r20(21, 13, 21, 21, 20, "water"), "litres", None)],
    21: [("r21_ex2", "The prices of a fridge and a cooler are in the ratio 13 : 6. The fridge costs Rs 4900 more than the cooler. What is the price of the cooler?",
          lambda: r21(13, 6, 4900, "small"), "Rs", None),
         ("r21_e1", "A sum of money is shared by two brothers in the ratio 3 : 10. One gets Rs 49 less than the other. Find the sum.", lambda: r21(3, 10, 49, "sum"), "Rs", None),
         ("r21_e2", "Two friends share some money in the ratio 5 : 12. One gets Rs 21 less than the other. What is the total amount?", lambda: r21(5, 12, 21, "sum"), "Rs", None),
         ("r21_e3", "Money is divided between two people in the ratio 11 : 4. One share is Rs 28 less than the other. Find the whole sum.", lambda: r21(11, 4, 28, "sum"), "Rs", None),
         ("r21_e4", "The prices of a pen and an eraser are in the ratio 9 : 2. The pen costs Rs 14 more than the eraser. What is the price of the eraser?", lambda: r21(9, 2, 14, "small"), "Rs", None),
         ("r21_e5", "The prices of a motorbike and a cycle are in the ratio 17 : 5. The motorbike costs Rs 6000 more than the cycle. What is the price of the cycle?",
          lambda: r21(17, 5, 6000, "small"), "Rs", None)],
    22: [("r22_ex2", "The diagonals of two squares are in the ratio 7 : 5. Find the ratio of their areas.", lambda: r_power(22, 7, 5), "ratio", None),
         ("r22_ex3", "The radii of two circles are in the ratio 6 : 11. What is the ratio of their areas?", lambda: r_power(22, 6, 11), "ratio", None),
         ("r22_e1", "The sides of two squares are in the ratio 7 : 9. Find the ratio of their areas.", lambda: r_power(22, 7, 9), "ratio", None),
         ("r22_e2", "The areas of two similar triangles are in the ratio 121 : 49. What is the ratio of their sides?", lambda: r_power(22, 121, 49, root=True), "ratio", None),
         ("r22_e3", "The circumferences of two circles are in the ratio 3 : 11. Find the ratio of their areas.", lambda: r_power(22, 3, 11), "ratio", None),
         ("r22_e4", "The diagonals of two squares are in the ratio 17 : 12. What is the ratio of their areas?", lambda: r_power(22, 17, 12), "ratio", None),
         ("r22_e5", "Each side of an octagon is made 6 times as long. What is the ratio of the area of the old octagon to that of the new one?", lambda: r_power(22, 1, 6), "ratio", None),
         ("r22_e6", "The radii of two circles are in the ratio 7 : 6. Find the ratio of their areas.", lambda: r_power(22, 7, 6), "ratio", None),
         ("r22_e7", "The perimeters of two squares are in the ratio 5 : 2. What is the ratio of their areas?", lambda: r_power(22, 5, 2), "ratio", None),
         ("r22_e8", "The diameters of two circles are in the ratio 7 : 12. Find the ratio of their areas.", lambda: r_power(22, 7, 12), "ratio", None),
         ("r22_e9", "The perimeters of two regular hexagons are in the ratio 3 : 7. What is the ratio of their areas?", lambda: r_power(22, 3, 7), "ratio", None),
         ("r22_e10", "The diagonals of two squares are in the ratio 9 : 8. Find the ratio of their areas.", lambda: r_power(22, 9, 8), "ratio", None)],
    23: [("r23_e1", "The diagonals of two cubes are in the ratio 5 : 7. Find the ratio of their volumes.", lambda: r_power(23, 5, 7), "ratio", None),
         ("r23_e2", "The radii of two spheres are in the ratio 2 : 9. What is the ratio of their volumes?", lambda: r_power(23, 2, 9), "ratio", None),
         ("r23_e3", "The diameters of two balls are in the ratio 4 : 9. Find the ratio of their volumes.", lambda: r_power(23, 4, 9), "ratio", None),
         ("r23_e4", "Each edge of a box is made 3 times as long. What is the ratio of the volume of the new box to the old one?", lambda: r_power(23, 3, 1), "ratio", None),
         ("r23_e5", "The edges of two cubes are in the ratio 6 : 5. Find the ratio of their volumes.", lambda: r_power(23, 6, 5), "ratio", None)],
    24: [("r24_e1", "Two numbers are in the ratio 20 : 29. If 15 is added to each, the ratio becomes 5 : 7. Find the numbers.", lambda: r24_build(20, 29, 15, 5, 7), "pair", None),
         ("r24_e2", "The ratio of two numbers is 22 : 27. If 22 is added to each, the ratio becomes 11 : 13. Find the numbers.", lambda: r24_build(22, 27, 22, 11, 13), "pair", None),
         ("r24_e3", "Two numbers are in the ratio 11 : 19. If 17 is taken from each, the ratio becomes 15 : 29. Find the numbers.", lambda: r24_build(11, 19, -17, 15, 29), "pair", None),
         ("r24_e4", "The ratio of two numbers is 28 : 13. If 21 is subtracted from each, the ratio becomes 5 : 2. Find the numbers.", lambda: r24_build(28, 13, -21, 5, 2), "pair", None),
         ("r24_e5", "Two numbers are in the ratio 11 : 29. If 3 is taken from each, the ratio becomes 5 : 14. Find the numbers.", lambda: r24_build(11, 29, -3, 5, 14), "pair", None),
         ("r24_e6", "Two numbers are in the ratio 23 : 25. If 21 is added to each, the ratio becomes 15 : 16. Find the numbers.", lambda: r24_build(23, 25, 21, 15, 16), "pair", None)],
    25: [("r25_ex2", "The pupils in three classes are in the ratio 13 : 16 : 19. If 12 pupils join each class, the ratio becomes 16 : 19 : 22. How many pupils were there in all before?",
          lambda: r25_classes([13, 16, 19], 12, [16, 19, 22]), "students", None),
         ("r25_e1", "Two numbers are in the ratio 29 : 23. If 10 is added to each, the ratio becomes 31 : 25. Find the numbers.", lambda: r25_build(29, 23, 10, 31, 25), "pair", None),
         ("r25_e2", "Two numbers are in the ratio 21 : 25. If 5 is added to each, the ratio becomes 11 : 13. Find the numbers.", lambda: r25_build(21, 25, 5, 11, 13, s=2), "pair", None),
         ("r25_e3", "The ratio of two numbers is 24 : 17. If 6 is taken from each, the ratio becomes 3 : 2. Find the numbers.", lambda: r25_build(24, 17, -6, 3, 2, s=7), "pair", None),
         ("r25_e4", "Two numbers are in the ratio 20 : 19. If 21 is subtracted from each, the ratio becomes 17 : 16. Find the numbers.", lambda: r25_build(20, 19, -21, 17, 16), "pair", None),
         ("r25_e5", "The pupils in three classes are in the ratio 5 : 7 : 8. If 18 pupils join each class, the ratio becomes 8 : 10 : 11. How many pupils were there before?",
          lambda: r25_classes([5, 7, 8], 18, [8, 10, 11]), "students", None),
         ("r25_e6", "The pupils in three classes are in the ratio 4 : 7 : 11. If 60 pupils join each class, the ratio becomes 7 : 10 : 14. What was the total number before?",
          lambda: r25_classes([4, 7, 11], 60, [7, 10, 14]), "students", None),
         ("r25_e7", "The pupils in three classes are in the ratio 17 : 19 : 24. If 14 pupils leave each class, the ratio becomes 15 : 17 : 22. How many pupils are there in all now?",
          lambda: r25_classes([17, 19, 24], -14, [15, 17, 22], now=True), "students", None)],
}

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(18, 26))
