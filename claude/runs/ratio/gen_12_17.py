"""Ratio and Proportion Rules 12-17 (2026-10-30). Rule 12: two alloys melted together - per cent of a metal in the new alloy, or the
ratio in which to melt them for a wanted ratio. Rule 13: a mixture of x litres in the ratio a : b - ax/(a+b) and bx/(a+b). Rule 14:
per cent of a metal in an alloy - a/(a+b) x 100%. Rule 15: A : B and B : C joined - ac : bc : bd. Rule 16: four or five quantities
joined the same way. Rule 17: hound and hare - leaps per time times length of a leap. Writes the six cards, regenerates the old
rows 722-726 and adds the book's examples and exercises with no copy. Rule 12 Exr 2 and 3 are left out: their wanted ratio lies
outside the two alloys and they ask for 'gold' in a silver-copper alloy; Exr 5 (book answer 'can't be determined') is written with
a wanted ratio that can be made. Usage: python gen_12_17.py"""
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
    12: (r"If alloys A and B have two metals in the ratios \(a : b\) and \(c : d\) and are melted together in the ratio \(x : y\), the first metal makes up",
         r"\[ \frac{\frac{ax}{a+b}+\frac{cy}{c+d}}{x+y}\times 100\% \]"),
    13: (r"If a mixture of \(x\) litres has milk and water in the ratio \(a : b\), it holds", r"\[ \frac{ax}{a+b}\ \text{litres of milk and}\ \frac{bx}{a+b}\ \text{litres of water} \]"),
    14: (r"If an alloy has metals A and B in the ratio \(a : b\), the per cent of A in it is", r"\[ \frac{a}{a+b}\times 100\% \]"),
    15: (r"If the first and second quantities are in the ratio \(a : b\) and the second and third in the ratio \(c : d\), the three are in the ratio",
         r"\[ ac : bc : bd \]"),
    16: (r"If the first : second \(= a : b\), second : third \(= c : d\) and third : fourth \(= e : f\), the four are in the ratio",
         r"\[ ace : bce : bde : bdf \]"),
    17: (r"If a hound takes \(p\) leaps while a hare takes \(q\), and \(m\) leaps of the hound equal \(n\) leaps of the hare, then",
         r"\[ \text{speed of hound} : \text{speed of hare} = pn : qm \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rsteps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def done(r, ans, fin, trad, ident, sub):
    return result(ans, T(r), steps(*trad), rsteps(r, ident, sub), fin, [ident, "Answer " + fin + "."], sub)


def num(r, v, trad, ident, sub, unit=""):
    return done(r, ("number", F(v)), UU(v, unit), trad, ident, sub)


def rat(r, a, b, trad, ident, sub):
    return done(r, ("ratio", (a, b)), R(a, b), trad, ident, sub)


def terms(ts):
    g = 0
    for t in ts:
        g = gcd(g, t)
    return [t // g for t in ts]


# ---------- Rule 12
def r12_percent(a, b, c, d, x, y, second=False):
    """per cent of the first metal (second=True: the second metal) when the alloys are melted in the ratio x : y."""
    p1, p2 = (F(b, a + b), F(d, c + d)) if second else (F(a, a + b), F(c, c + d))
    v = (p1 * x + p2 * y) / (x + y) * 100
    trad = [("Take amounts.", rf"Take \({x}\) kg of A and \({y}\) kg of B: the metal in them is \({x}\times {frc(p1)} + {y}\times {frc(p2)} = {frc(p1 * x + p2 * y)}\) kg."),
            ("Per cent.", rf"\[ \frac{{{frc(p1 * x + p2 * y)}}}{{{x + y}}}\times 100 = {nf(v)}\% \]")]
    sub = rf"\[ \frac{{{frc(p1)}\times {x} + {frc(p2)}\times {y}}}{{{x}+{y}}}\times 100\% = {nf(v)}\% \]"
    return num(12, v, trad, rf"Alloys \({a} : {b}\) and \({c} : {d}\), melted \({x} : {y}\).", sub, "%")


def r12_mix(a, b, c, d, e, f):
    """ratio x : y in which alloys a : b and c : d must be melted to give e : f."""
    p, q, t = F(a, a + b), F(c, c + d), F(e, e + f)
    x, y = low(abs(q - t), abs(t - p))
    trad = [("Fraction of the first metal.", rf"A: \({frc(p)}\), B: \({frc(q)}\), wanted: \({frc(t)}\)."),
            ("Balance.", rf"With \(x\) of A and \(y\) of B: \({frc(p)}x + {frc(q)}y = {frc(t)}(x+y)\), so \({frc(abs(p - t))}x = {frc(abs(t - q))}y\)."),
            ("Ratio.", rf"\[ x : y = {frc(abs(q - t))} : {frc(abs(t - p))} = {x} : {y} \]")]
    sub = rf"\[ \frac{{\frac{{{a}x}}{{{a + b}}}+\frac{{{c}y}}{{{c + d}}}}}{{x+y}} = \frac{{{e}}}{{{e + f}}} \;\Rightarrow\; x : y = {x} : {y} \]"
    return rat(12, x, y, trad, rf"Alloys \({a} : {b}\) and \({c} : {d}\); wanted \({e} : {f}\).", sub)


def r12_equal(a, b, c, d):
    g, k = F(a, a + b) + F(c, c + d), F(b, a + b) + F(d, c + d)
    x, y = low(g, k)
    trad = [("One unit of each.", rf"Gold \(= {frc(F(a, a + b))} + {frc(F(c, c + d))} = {frc(g)}\), copper \(= {frc(F(b, a + b))} + {frc(F(d, c + d))} = {frc(k)}\)."),
            ("Ratio.", rf"\[ {frc(g)} : {frc(k)} = {x} : {y} \]")]
    sub = rf"With \(x = y\): \[ \frac{{{a}}}{{{a + b}}}+\frac{{{c}}}{{{c + d}}} : \frac{{{b}}}{{{a + b}}}+\frac{{{d}}}{{{c + d}}} = {x} : {y} \]"
    return rat(12, x, y, trad, rf"Alloys \({a} : {b}\) and \({c} : {d}\), equal amounts.", sub)


# ---------- Rule 13
def r13(x, a, b, ask):
    x = F(x)
    k = x / (a + b)
    milk, water = a * k, b * k
    trad = [("Value of one part.", rf"\({a}+{b} = {a + b}\) parts make \({nf(x)}\) litres: one part \(= {nf(k)}\) litres."),
            ("Milk and water.", rf"Milk \(= {a}\times {nf(k)} = {nf(milk)}\), water \(= {b}\times {nf(k)} = {nf(water)}\).")]
    sub = rf"\[ \frac{{{a}\times {nf(x)}}}{{{a + b}}} = {nf(milk)},\qquad \frac{{{b}\times {nf(x)}}}{{{a + b}}} = {nf(water)} \]"
    ident = rf"\(x = {nf(x)}\), \(a : b = {a} : {b}\)."
    if ask == "both":
        return done(13, ("pair", (milk, water)), f"milk {M(nf(milk))} litres and water {M(nf(water))} litres", trad, ident, sub)
    return num(13, milk if ask == "milk" else water, trad, ident, sub, "litres")


# ---------- Rule 14
def r14(a, b, which):
    """per cent of the first (which=0) or second (which=1) metal of an alloy a : b."""
    v = F([a, b][which] * 100, a + b)
    trad = [("Parts.", rf"Out of \({a}+{b} = {a + b}\) parts, \({[a, b][which]}\) are this metal."),
            ("Per cent.", rf"\[ \frac{{{[a, b][which]}}}{{{a + b}}}\times 100 = {nf(v)}\% \]")]
    return num(14, v, trad, rf"\(a : b = {a} : {b}\).", rf"\[ \frac{{{[a, b][which]}}}{{{a}+{b}}}\times 100\% = {nf(v)}\% \]", "%")


# ---------- Rule 15
def join3(a, b, c, d):
    return terms([a * c, b * c, b * d])


def r15_sum(a, b, c, d, s, ask):
    ts = join3(a, b, c, d)
    k = F(s, sum(ts))
    v3 = [t * k for t in ts]
    trad = [("Join the ratios.", rf"Make the middle terms equal: \({a} : {b} = {a * c} : {b * c}\) and \({c} : {d} = {b * c} : {b * d}\), so the three are \({' : '.join(map(str, ts))}\)."),
            ("One part.", rf"\({' + '.join(map(str, ts))} = {sum(ts)}\) parts make \({s}\): one part \(= {nf(k)}\); the numbers are \({', '.join(nf(t) for t in v3)}\).")]
    sub = rf"\[ {a}\times {c} : {b}\times {c} : {b}\times {d} = {' : '.join(map(str, ts))} \]"
    ident = rf"\({a} : {b}\) and \({c} : {d}\), sum \({s}\)."
    v, how = {"second": (v3[1], "the second number"), "third_less_sum": (v3[2] - v3[0] - v3[1], "third minus (first + second)"),
              "first_plus_second": (v3[0] + v3[1], "first + second")}[ask]
    trad.append(("What is asked.", rf"{how.capitalize()} \(= {nf(v)}\)."))
    return num(15, v, trad, ident, sub + rf"{how.capitalize()} \(= {nf(v)}\).")


def r15_money(a, b, c, d, have, i, ask, names):
    ts = join3(a, b, c, d)
    k = F(have, ts[i])
    v = ts[ask] * k
    trad = [("Join the ratios.", rf"{names[0]} : {names[1]} \(= {a} : {b}\) and {names[1]} : {names[2]} \(= {c} : {d}\) give \({' : '.join(map(str, ts))}\)."),
            ("Use the known share.", rf"{names[i]}'s \({ts[i]}\) parts are Rs \({nf(have)}\): one part \(= {nf(k)}\); {names[ask]} \(= {ts[ask]}\times {nf(k)} = {nf(v)}\).")]
    sub = rf"\[ {a}\times {c} : {b}\times {c} : {b}\times {d} = {' : '.join(map(str, ts))} \]{names[ask]} \(= \frac{{{ts[ask]}}}{{{ts[i]}}}\times {nf(have)} = {nf(v)}\)."
    return num(15, v, trad, rf"\({a} : {b}\), \({c} : {d}\); {names[i]} has Rs \({nf(have)}\).", sub, "Rs")


# ---------- Rule 16
def joinall(pairs):
    """[(a, b), (c, d), ...] for 1st:2nd, 2nd:3rd, ... -> all terms in whole numbers (lowest)."""
    ts = [F(1)]
    for a, b in pairs:
        ts.append(ts[-1] * F(b, a))
    den = 1
    for t in ts:
        den = den * t.denominator // gcd(den, t.denominator)
    return terms([int(t * den) for t in ts])


def r16_terms(pairs, names="PQRST"):
    ts = joinall(pairs)
    n = len(ts)
    raw = []
    for j in range(n):
        p = 1
        for i, (a, b) in enumerate(pairs):
            p *= b if i < j else a
        raw.append(p)
    trad = [("Make each common term equal.", "; ".join(rf"{names[i]} : {names[i + 1]} \(= {a} : {b}\)" for i, (a, b) in enumerate(pairs)) + "."),
            ("Multiply through.", rf"Writing every quantity against the same scale gives \({' : '.join(map(str, raw))}\), which is \({' : '.join(map(str, ts))}\) in lowest terms.")]
    sub = rf"\[ {' : '.join(map(str, raw))} = {' : '.join(map(str, ts))} \]"
    fin = M(" : ".join(map(str, ts)))
    return done(16, ("terms", tuple(ts)), fin, trad, "Ratios " + ", ".join(R(a, b) for a, b in pairs) + ".", sub)


def r16_share(pairs, total, ask, names="PQRST"):
    ts = joinall(pairs)
    k = F(total, sum(ts))
    v = ts[ask] * k
    trad = [("Join the ratios.", rf"{' : '.join(names[:len(ts)])} \(= {' : '.join(map(str, ts))}\)."),
            ("Share.", rf"\({' + '.join(map(str, ts))} = {sum(ts)}\) parts; one part \(= {nf(total)} \div {sum(ts)} = {nf(k)}\); {names[ask]} \(= {ts[ask]}\times {nf(k)} = {nf(v)}\).")]
    sub = rf"{' : '.join(names[:len(ts)])} \(= {' : '.join(map(str, ts))}\); \[ \frac{{{ts[ask]}}}{{{sum(ts)}}}\times {nf(total)} = {nf(v)} \]"
    return num(16, v, trad, "Ratios " + ", ".join(R(a, b) for a, b in pairs) + rf", total Rs \({nf(total)}\).", sub, "Rs")


# ---------- Rule 17
def r17(p, q, m, n, a="hound", b="hare"):
    x, y = low(p * n, q * m)
    trad = [("Length of a leap.", rf"\({m}\) leaps of the {a} \(=\) \({n}\) leaps of the {b}, so one leap of the {a} \(= {frc(F(n, m))}\) leaps of the {b}."),
            ("Distance in the same time.", rf"While the {b} makes \({q}\) leaps, the {a} makes \({p}\) leaps \(= {p}\times {frc(F(n, m))} = {frc(F(p * n, m))}\) of the {b}'s leaps."),
            ("Compare.", rf"\[ {frc(F(p * n, m))} : {q} = {x} : {y} \]")]
    return rat(17, x, y, trad, rf"\(p = {p}\), \(q = {q}\), \(m = {m}\), \(n = {n}\).", rf"\[ {p}\times {n} : {q}\times {m} = {p * n} : {q * m} = {x} : {y} \]")


C = card
CARDS = {
    12: C(12, "Two Alloys Melted Together", r"Track the first metal: its fraction in each alloy, weighted by how much of each alloy is used.",
          r"\[ \frac{\frac{ax}{a+b}+\frac{cy}{c+d}}{x+y}\times 100\% \]",
          [("Alloy A", r"\frac{a}{a+b}\ \text{of the metal}"), ("Alloy B", r"\frac{c}{c+d}\ \text{of the metal}"), ("Mix x : y", r"\text{weighted average}")],
          r"To reach a wanted ratio, the wanted fraction must lie between the two alloys' fractions - the mixing ratio is the alligation of the three fractions.",
          "'Two alloys contain gold and silver in the ratios a : b and c : d; they are mixed in the ratio x : y; find the per cent of silver' / 'in what ratio must they be mixed'.",
          r"\(1 : 1\) and \(3 : 1\) melted equally: \(\frac{1}{2}+\frac{3}{4} : \frac{1}{2}+\frac{1}{4} = 5 : 3\).", r"Adding the ratio terms of alloys with different totals."),
    13: C(13, "Milk and Water in a Mixture", r"Divide the mixture into \(a+b\) equal parts.", r"\[ \frac{ax}{a+b},\quad \frac{bx}{a+b} \]",
          [("Parts", r"a+b"), ("One part", r"\frac{x}{a+b}"), ("Milk, water", r"a\ \text{and}\ b\ \text{parts}")],
          r"The same as sharing a sum in a ratio; check that milk + water = the whole mixture.", "'In a mixture of x litres, milk and water are in the ratio a : b; find the milk (water).'",
          r"\(40\) litres in \(3 : 1\): milk \(30\), water \(10\).", r"Dividing by \(a\) instead of \(a+b\)."),
    14: C(14, "Per Cent of a Metal in an Alloy", r"The metal's share of the parts, as a per cent.", r"\[ \frac{a}{a+b}\times 100\% \]",
          [("Parts", r"a+b"), ("Metal A", r"\frac{a}{a+b}"), ("Per cent", r"\times 100")],
          r"The two per cents add up to \(100\%\).", "'An alloy contains copper and zinc in the ratio a : b; what per cent is copper?'",
          r"\(3 : 2\): \(60\%\) and \(40\%\).", r"Taking \(\frac{a}{b}\times 100\)."),
    15: C(15, "Joining Two Ratios", r"Make the shared middle term the same in both ratios, then read the three terms.", r"\[ ac : bc : bd \]",
          [("A : B", r"a : b\ \to\ ac : bc"), ("B : C", r"c : d\ \to\ bc : bd"), ("A : B : C", r"ac : bc : bd")],
          r"Multiply the first ratio by \(c\) and the second by \(b\) so that B is \(bc\) in both. Reduce to lowest terms.",
          "'The sum of three numbers is s; first : second = a : b and second : third = c : d; find the second.'",
          r"\(2 : 3\) and \(4 : 5\): \(8 : 12 : 15\).", r"Writing \(a : b : d\) without making the middle terms equal."),
    16: C(16, "Joining Three or More Ratios", r"Carry the common term along: each new ratio is scaled to the term before it.", r"\[ ace : bce : bde : bdf \]",
          [("Pattern", r"\text{numerators of the left, denominators of the right}"), ("Four terms", r"ace : bce : bde : bdf"), ("Five terms", r"aceg : bceg : bdeg : bdfg : bdfh")],
          r"Each term takes the consequents of the ratios before it and the antecedents of the ratios after it.",
          "'If A : B = a : b, B : C = c : d and C : D = e : f, find A : B : C : D' / 'find D's share of Rs x'.",
          r"\(1 : 2\), \(3 : 4\), \(5 : 6\): \(15 : 30 : 40 : 48\).", r"Forgetting to reduce, or mixing up which terms to multiply."),
    17: C(17, "Hound and Hare", r"Speed = (leaps in the same time) x (length of one leap).", r"\[ pn : qm \]",
          [("Leaps in the same time", r"p : q"), ("Length of a leap", r"\frac{n}{m} : 1"), ("Speeds", r"pn : qm")],
          r"Measure both animals' leaps in the hare's leaps; then compare the ground each covers in the same time.",
          "'A hound takes p leaps for every q of the hare, but m leaps of the hound equal n of the hare; compare their speeds.'",
          r"\(5\) for \(6\), \(4\) equal \(5\): \(25 : 24\).", r"Multiplying \(p\) by \(m\) instead of \(n\)."),
}
OLD = {
    722: (13, "A can holds 72 litres of milk and water in the ratio 7 : 5. How much milk and how much water does it hold?", lambda: r13(72, 7, 5, "both"), "pair"),
    723: (14, "An alloy has tin and lead in the ratio 9 : 16. What per cent of the alloy is tin?", lambda: r14(9, 16, 0), "%"),
    724: (15, "Three numbers add up to 206. The first and second are in the ratio 4 : 7, and the second and third in the ratio 3 : 10. Find the second number.",
          lambda: r15_sum(4, 7, 3, 10, 206, "second"), ""),
    725: (16, "If P : Q = 5 : 6, Q : R = 9 : 14 and R : S = 7 : 11, find P : Q : R : S.", lambda: r16_terms([(5, 6), (9, 14), (7, 11)]), "terms"),
    726: (17, "A dog chasing a cat takes 13 leaps for every 15 leaps of the cat, but 11 leaps of the dog cover as much ground as 12 leaps of the cat. "
              "Compare the speeds of the dog and the cat.", lambda: r17(13, 15, 11, 12, "dog", "cat"), "ratio"),
}
NEW = {
    12: [("r12_ex", "Two alloys have silver and copper in the ratios 4 : 1 and 7 : 3. In what ratio must they be melted together to get silver and copper in the ratio 7 : 2?",
          lambda: r12_mix(4, 1, 7, 3, 7, 2), "ratio", None),
         ("r12_e1", "Alloy P has gold and silver in the ratio 2 : 5 and alloy Q in the ratio 3 : 7. A new alloy is made by melting P and Q in the ratio 7 : 5. "
                    "What per cent of the new alloy is silver?", lambda: r12_percent(2, 5, 3, 7, 7, 5, second=True), "%", None),
         ("r12_e2", "Two alloys have tin and lead in the ratios 3 : 1 and 5 : 1. In what ratio must they be mixed to get tin and lead in the ratio 4 : 1?",
          lambda: r12_mix(3, 1, 5, 1, 4, 1), "ratio", None),
         ("r12_e3", "Two alloys have copper and zinc in the ratios 5 : 2 and 3 : 1. In what ratio should they be melted together so that copper and zinc are in the ratio 8 : 3?",
          lambda: r12_mix(5, 2, 3, 1, 8, 3), "ratio", None),
         ("r12_e4", "Two alloys are made of gold and copper in the ratios 5 : 3 and 3 : 13. If equal amounts of the two are melted together, what is the ratio of gold "
                    "to copper in the new alloy?", lambda: r12_equal(5, 3, 3, 13), "ratio", None)],
    13: [("r13_e1", "A tub holds 96 litres of milk and water in the ratio 5 : 3. How much milk is in it?", lambda: r13(96, 5, 3, "milk"), "litres", None),
         ("r13_e2", "In 104 litres of a mixture, milk and water are in the ratio 7 : 6. How much water is there?", lambda: r13(104, 7, 6, "water"), "litres", None),
         ("r13_e3", "A 150 litre mixture has milk and water in the ratio 11 : 4. Find the quantity of milk.", lambda: r13(150, 11, 4, "milk"), "litres", None),
         ("r13_e4", "A tank has 720 litres of milk and water in the ratio 17 : 7. How much of it is water?", lambda: r13(720, 17, 7, "water"), "litres", None),
         ("r13_e5", "A drum is filled with 132 litres of milk and water mixed in the ratio 13 : 9. How many litres of milk are there?", lambda: r13(132, 13, 9, "milk"), "litres", None)],
    14: [("r14_e1", "An alloy has zinc and nickel in the ratio 7 : 3. What per cent of it is nickel?", lambda: r14(7, 3, 1), "%", None),
         ("r14_e2", "An alloy has copper and tin in the ratio 5 : 11. What per cent of the alloy is copper?", lambda: r14(5, 11, 0), "%", None),
         ("r14_e3", "In an alloy, lead and tin are in the ratio 19 : 6. What is the percentage of tin?", lambda: r14(19, 6, 1), "%", None),
         ("r14_e4", "An alloy is made of zinc and copper in the ratio 9 : 11. What percentage of it is zinc?", lambda: r14(9, 11, 0), "%", None)],
    15: [("r15_ex2", "The money with Asha and Bina is in the ratio 9 : 11, and with Bina and Chitra in the ratio 5 : 13. If Asha has Rs 630, how much does Chitra have?",
          lambda: r15_money(9, 11, 5, 13, 630, 0, 2, ["Asha", "Bina", "Chitra"]), "Rs", None),
         ("r15_e1", "Three numbers add up to 221. The first and second are in the ratio 3 : 4, and the second and third in the ratio 2 : 3. Find the second number.",
          lambda: r15_sum(3, 4, 2, 3, 221, "second"), "", None),
         ("r15_e2", "The sum of three numbers is 341. The first is to the second as 5 : 8, and the second is to the third as 4 : 9. What is the second number?",
          lambda: r15_sum(5, 8, 4, 9, 341, "second"), "", None),
         ("r15_e3", "Three numbers add up to 238. The ratio of the first to the second is 3 : 4 and of the second to the third is 2 : 5. "
                    "By how much is the third number more than the sum of the first two?", lambda: r15_sum(3, 4, 2, 5, 238, "third_less_sum"), "", None),
         ("r15_e4", "The sum of three numbers is 264. The first and second are in the ratio 1 : 4, and the second and third in the ratio 2 : 3. Find the sum of the first two numbers.",
          lambda: r15_sum(1, 4, 2, 3, 264, "first_plus_second"), "", None),
         ("r15_e5", "The money with Ravi and Mohan is in the ratio 5 : 6, and with Mohan and Kiran in the ratio 8 : 9. If Ravi has Rs 400, how much does Kiran have?",
          lambda: r15_money(5, 6, 8, 9, 400, 0, 2, ["Ravi", "Mohan", "Kiran"]), "Rs", None)],
    16: [("r16_ex2", "If P : Q = 7 : 9, Q : R = 3 : 11, R : S = 13 : 12 and S : T = 2 : 3, find P : Q : R : S : T.", lambda: r16_terms([(7, 9), (3, 11), (13, 12), (2, 3)]), "terms", None),
         ("r16_e1", "If P : Q = 1 : 3, Q : R = 3 : 11 and R : S = 11 : 13, find P : Q : R : S.", lambda: r16_terms([(1, 3), (3, 11), (11, 13)]), "terms", None),
         ("r16_e2", "If P : Q = 3 : 4, Q : R = 6 : 7 and R : S = 14 : 15, find P : Q : R : S.", lambda: r16_terms([(3, 4), (6, 7), (14, 15)]), "terms", None),
         ("r16_e3", "If P : Q = 3 : 4, Q : R = 2 : 5 and R : S = 5 : 6, what is P's share of a property worth Rs 5800?", lambda: r16_share([(3, 4), (2, 5), (5, 6)], 5800, 0), "Rs", None),
         ("r16_e4", "If P : Q = 3 : 4, Q : R = 2 : 3, R : S = 4 : 5 and S : T = 5 : 6, find T's share of Rs 11800.",
          lambda: r16_share([(3, 4), (2, 3), (4, 5), (5, 6)], 11800, 4), "Rs", None),
         ("r16_e5", "If P : Q = 13 : 6, Q : R = 4 : 7 and R : S = 3 : 11, find P : Q : R : S.", lambda: r16_terms([(13, 6), (4, 7), (3, 11)]), "terms", None)],
    17: [("r17_e1", "A fox chasing a rabbit takes 16 leaps for every 19 leaps of the rabbit, but 13 leaps of the fox are as long as 15 leaps of the rabbit. Compare their speeds.",
          lambda: r17(16, 19, 13, 15, "fox", "rabbit"), "ratio", None),
         ("r17_e2", "A cheetah takes 12 leaps for every 19 leaps of a deer, but 11 leaps of the cheetah equal 17 leaps of the deer. Compare the speeds of the cheetah and the deer.",
          lambda: r17(12, 19, 11, 17, "cheetah", "deer"), "ratio", None),
         ("r17_e3", "A wolf chasing a goat takes 16 leaps for every 21 leaps of the goat, but 13 leaps of the wolf equal 17 leaps of the goat. Compare their speeds.",
          lambda: r17(16, 21, 13, 17, "wolf", "goat"), "ratio", None),
         ("r17_e4", "A dog takes 7 leaps for every 11 leaps of a fox, but 2 leaps of the dog are as long as 3 leaps of the fox. Compare the speeds of the dog and the fox.",
          lambda: r17(7, 11, 2, 3, "dog", "fox"), "ratio", None),
         ("r17_e5", "A tiger takes 3 leaps for every 8 leaps of a monkey, but 1 leap of the tiger equals 3 leaps of the monkey. Compare the speeds of the tiger and the monkey.",
          lambda: r17(3, 8, 1, 3, "tiger", "monkey"), "ratio", None)],
}

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(12, 18))
