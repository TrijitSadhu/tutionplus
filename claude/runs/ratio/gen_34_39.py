"""Ratio and Proportion Rules 34-39 (2026-10-30). Rule 34 / 35: the number added to (taken from) both terms of a : b to make c : d -
(ad - bc)/(c - d) and (bc - ad)/(c - d). Rule 36: part of a mixture drawn off and replaced by liquid B - the liquids at first. Rule 37:
the same, asking what the vessel holds. Rule 38: workers cut in the ratio p : q and pay raised r : s - the wage bill goes from pr to
qs. Rule 39: two candles of the same height burning out in T1 and T2 hours - the time when their heights are x : y. Writes the six
cards, regenerates the old rows 741-745 (744's key said 21 : 10 - the bill falls in the ratio 21 : 20) and adds the book's examples
and exercises with no copy. Number sets searched against the book (scratch ratio_search4.py). Book slip: Rule 37 Exr 2 (5 : 4 with
liquid A poured in cannot become 4 : 5; its answer 72 litres gives 2 : 1) - written with numbers that work. Rule 38 questions ask
for the ratio of the old wage bill to the new one. Usage: python gen_34_39.py"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from fmt import M, R, UU, low, nf  # noqa: E402
from gen_1_5 import main  # noqa: E402
from helpers import place, result  # noqa: E402

TH = {
    34: (r"The number that must be added to both terms of the ratio \(a : b\) to make it \(c : d\) is", r"\[ \frac{ad-bc}{c-d} \]"),
    35: (r"The number that must be taken from both terms of the ratio \(a : b\) to make it \(c : d\) is", r"\[ \frac{bc-ad}{c-d} \]"),
    36: (r"If a vessel holds liquids A and B in the ratio \(a : b\), and \(q\) litres of the mixture are replaced by liquid B so that the ratio becomes "
         r"\(c : d\), the liquid A at first is", r"\[ a\times\left[\frac{q}{a+b}+\frac{qc}{ad-bc}\right] \]"),
    37: (r"If a vessel holds liquids A and B in the ratio \(a : b\), and \(q\) litres are replaced by liquid B so that the ratio becomes \(c : d\), the vessel holds",
         r"\[ \frac{q(a+b)}{a}\times\left[\frac{a}{a+b}+\frac{ac}{ad-bc}\right]\ \text{litres} \]"),
    38: (r"If the number of workers is cut in the ratio \(p : q\) and their pay is raised in the ratio \(r : s\), the wage bill changes in the ratio",
         r"\[ \text{old bill} : \text{new bill} = pr : qs \]"),
    39: (r"If two candles of the same height burn out in \(T_1\) and \(T_2\) hours (\(T_1 \gt T_2\)), their heights are in the ratio \(x : y\) after",
         r"\[ \frac{T_1T_2\left(\frac{x}{y}-1\right)}{\frac{x}{y}T_1-T_2}\ \text{hours} \]"),
}


def T(r):
    return TH[r][0] + "<br>" + TH[r][1]


def rsteps(r, ident, sub):
    return steps(("Identify the values.", ident), ("Apply the specified rule.", TH[r][1]), ("Substitute the values.", sub))


def done(r, ans, fin, trad, ident, sub):
    return result(ans, T(r), steps(*trad), rsteps(r, ident, sub), fin, [ident, "Answer " + fin + "."], sub)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


# ---------- Rules 34 and 35
def r34(a, b, c, d, sub=False):
    v = F(b * c - a * d, c - d) if sub else F(a * d - b * c, c - d)
    sg = "-" if sub else "+"
    trad = [("Set up the proportion.", rf"\(\frac{{{a} {sg} x}}{{{b} {sg} x}} = \frac{{{c}}}{{{d}}}\), so \({d}({a} {sg} x) = {c}({b} {sg} x)\)."),
            ("Solve.", rf"\({d * a} {sg} {d}x = {c * b} {sg} {c}x\) gives \(x = {nf(v)}\). Check: \(\frac{{{nf(a + (-v if sub else v))}}}{{{nf(b + (-v if sub else v))}}} = \frac{{{c}}}{{{d}}}\).")]
    rule = 35 if sub else 34
    sub_t = (rf"\[ \frac{{{b}\times {c}-{a}\times {d}}}{{{c}-{d}}} = \frac{{{b * c - a * d}}}{{{c - d}}} = {nf(v)} \]" if sub else
             rf"\[ \frac{{{a}\times {d}-{b}\times {c}}}{{{c}-{d}}} = \frac{{{a * d - b * c}}}{{{c - d}}} = {nf(v)} \]")
    return done(rule, ("number", v), M(nf(v)), trad, rf"\(a : b = {a} : {b}\), \(c : d = {c} : {d}\).", sub_t)


# ---------- Rules 36 and 37
def solve_vessel(a, b, q, c, d, filler="B"):
    """vessel a x and b x; q litres out; q of the filler in; ratio c : d -> x."""
    def ratio_after(x):
        A = a * x - F(q * a, a + b)
        Bq = b * x - F(q * b, a + b)
        return (A + q, Bq) if filler == "A" else (A, Bq + q)
    # linear in x: d * A' - c * B' = 0
    f = lambda x: d * ratio_after(x)[0] - c * ratio_after(x)[1]
    x = -f(F(0)) / (f(F(1)) - f(F(0)))
    return x


def r36(a, b, q, c, d, ask):
    x = solve_vessel(a, b, q, c, d)
    A, Bq, tot = a * x, b * x, (a + b) * x
    trad = [("Let the vessel hold the parts.", rf"Let A \(= {a}x\) and B \(= {b}x\) litres. The \({q}\) litres drawn off carry \({frc(F(q * a, a + b))}\) of A and \({frc(F(q * b, a + b))}\) of B."),
            ("Form the equation.", rf"\(\frac{{{a}x - {frc(F(q * a, a + b))}}}{{{b}x - {frc(F(q * b, a + b))} + {q}}} = \frac{{{c}}}{{{d}}}\), which gives \(x = {nf(x)}\)."),
            ("The liquids.", rf"A \(= {nf(A)}\), B \(= {nf(Bq)}\), the vessel \(= {nf(tot)}\) litres.")]
    raw = a * (F(q, a + b) + F(q * c, a * d - b * c))
    sub = rf"\[ {a}\left[\frac{{{q}}}{{{a + b}}}+\frac{{{q}\times {c}}}{{{a}\times {d}-{b}\times {c}}}\right] = {nf(raw)} \]"
    ident = rf"\(a : b = {a} : {b}\), \(q = {q}\), \(c : d = {c} : {d}\)."
    if ask == "A":
        return done(36, ("number", A), UU(A, "litres"), trad, ident, sub)
    if ask == "B":
        return done(36, ("number", Bq), UU(Bq, "litres"), trad, ident, sub + rf"B \(= \frac{{{b}}}{{{a}}}\times {nf(A)} = {nf(Bq)}\).")
    return done(36, ("pair", (Bq, tot)), f"B {M(nf(Bq))} litres, vessel {M(nf(tot))} litres", trad, ident, sub + rf"B \(= {nf(Bq)}\), vessel \(= {nf(tot)}\).")


def r37(a, b, q, c, d, filler="B"):
    x = solve_vessel(a, b, q, c, d, filler)
    tot = (a + b) * x
    P, Q = ("P", "Q")
    added = f"{q} litres of {P if filler == 'A' else Q}"
    trad = [("Let the drum hold the parts.", rf"Let {P} \(= {a}x\) and {Q} \(= {b}x\). The \({q}\) litres taken out carry \({frc(F(q * a, a + b))}\) of {P} and \({frc(F(q * b, a + b))}\) of {Q}."),
            ("Form the equation.", (rf"\(\frac{{{a}x - {frc(F(q * a, a + b))} + {q}}}{{{b}x - {frc(F(q * b, a + b))}}}\)" if filler == "A" else
                                    rf"\(\frac{{{a}x - {frc(F(q * a, a + b))}}}{{{b}x - {frc(F(q * b, a + b))} + {q}}}\)") + rf" \(= \frac{{{c}}}{{{d}}}\) gives \(x = {nf(x)}\)."),
            ("What the drum holds.", rf"\({a + b}x = {nf(tot)}\) litres.")]
    if filler == "B":
        raw = F(q * (a + b), a) * (F(a, a + b) + F(a * c, a * d - b * c))
        sub = rf"\[ \frac{{{q}({a}+{b})}}{{{a}}}\left[\frac{{{a}}}{{{a + b}}}+\frac{{{a}\times {c}}}{{{a}\times {d}-{b}\times {c}}}\right] = {nf(raw)} \]"
    else:                                               # P is the filler: the same with the roles of the liquids swapped
        raw = F(q * (a + b), b) * (F(b, a + b) + F(b * d, b * c - a * d))
        sub = rf"P is the filler, so swap the liquids: \[ \frac{{{q}({b}+{a})}}{{{b}}}\left[\frac{{{b}}}{{{a + b}}}+\frac{{{b}\times {d}}}{{{b}\times {c}-{a}\times {d}}}\right] = {nf(raw)} \]"
    assert raw == tot, (raw, tot)
    return done(37, ("number", tot), UU(tot, "litres"), trad, rf"\(a : b = {a} : {b}\), \(q = {q}\), \(c : d = {c} : {d}\); {added} poured in.", sub)


# ---------- Rule 38
def r38(p, q, r, s):
    x, y = low(p * r, q * s)
    word = "falls" if x > y else "rises" if x < y else "stays the same"
    trad = [("Bill = workers x pay.", rf"Let the workers be \({p}m\) and pay \({r}w\) before; \({q}m\) and \({s}w\) after."),
            ("Compare.", rf"Old bill \(= {p * r}mw\), new bill \(= {q * s}mw\): \[ {p * r} : {q * s} = {x} : {y} \]the bill {word}.")]
    sub = rf"\[ {p}\times {r} : {q}\times {s} = {p * r} : {q * s} = {x} : {y} \]"
    return done(38, ("ratio", (x, y)), R(x, y), trad, rf"Workers \({p} : {q}\), pay \({r} : {s}\).", sub)


# ---------- Rule 39
def r39(T1, T2, x, y):
    T1, T2 = F(T1), F(T2)
    k = F(x, y)
    t = T1 * T2 * (k - 1) / (k * T1 - T2)
    hh, mm = int(t), (t - int(t)) * 60
    assert mm.denominator == 1
    trad = [("Height left after t hours.", rf"Take the height as \(1\). After \(t\) hours the first is \(1 - \frac{{t}}{{{nf(T1)}}}\) and the second \(1 - \frac{{t}}{{{nf(T2)}}}\)."),
            ("Form the equation.", rf"\(1 - \frac{{t}}{{{nf(T1)}}} = {frc(k)}\left(1 - \frac{{t}}{{{nf(T2)}}}\right)\), which gives \(t = {frc(t)}\) hours."),
            ("Hours and minutes.", rf"\({frc(t)}\) hours \(= {hh}\) hours \({mm}\) minutes.")]
    sub = rf"\[ \frac{{{nf(T1)}\times {nf(T2)}\left({frc(k)}-1\right)}}{{{frc(k)}\times {nf(T1)}-{nf(T2)}}} = {frc(t)} \]"
    return done(39, ("pair", (F(hh), mm)), rf"\({hh}\) hours \({mm}\) minutes", trad, rf"\(T_1 = {nf(T1)}\), \(T_2 = {nf(T2)}\), \(x : y = {x} : {y}\).", sub)


C = card
CARDS = {
    34: C(34, "Number Added to Both Terms", r"Put \(x\) into both terms and solve the proportion.", r"\[ \frac{ad-bc}{c-d} \]",
          [("Proportion", r"\frac{a+x}{b+x} = \frac{c}{d}"), ("Cross product", r"d(a+x) = c(b+x)"), ("x", r"\frac{ad-bc}{c-d}")],
          r"Adding the same number to both terms moves the ratio towards \(1\).", "'Find the number which, when added to the terms of the ratio a : b, makes it c : d.'",
          r"\(11 : 23\) to \(4 : 7\): \(\frac{77-92}{-3} = 5\).", r"Sign slips: keep \(ad-bc\) over \(c-d\)."),
    35: C(35, "Number Taken From Both Terms", r"Take \(x\) from both terms and solve the proportion.", r"\[ \frac{bc-ad}{c-d} \]",
          [("Proportion", r"\frac{a-x}{b-x} = \frac{c}{d}"), ("Cross product", r"d(a-x) = c(b-x)"), ("x", r"\frac{bc-ad}{c-d}")],
          r"Taking the same number from both terms moves the ratio away from \(1\).", "'Find the number which, when subtracted from the terms of the ratio a : b, makes it c : d.'",
          r"\(11 : 23\) to \(3 : 7\): \(\frac{69-77}{-4} = 2\).", r"Using the formula for adding."),
    36: C(36, "Mixture Partly Replaced - the Liquids", r"The liquid drawn off carries both liquids in the old ratio; only liquid B is put back.",
          r"\[ a\left[\frac{q}{a+b}+\frac{qc}{ad-bc}\right] \]",
          [("Taken out", r"\frac{qa}{a+b}\ \text{of A},\ \frac{qb}{a+b}\ \text{of B}"), ("Put back", r"q\ \text{of B}"), ("New ratio", r"c : d")],
          r"Write A and B as \(ax\) and \(bx\), take out their shares of \(q\), add \(q\) to B, and solve the new ratio for \(x\).",
          "'A bucket has liquids A and B in the ratio a : b; q litres are replaced by B and the ratio becomes c : d; how much of A was there?'",
          r"\(7 : 5\), \(9\) litres replaced, \(7 : 9\): A \(= 21\) litres.", r"Forgetting that the drawn-off mixture also takes some of B."),
    37: C(37, "Mixture Partly Replaced - the Vessel", r"Same working as Rule 36; give \((a+b)x\), the whole vessel.",
          r"\[ \frac{q(a+b)}{a}\left[\frac{a}{a+b}+\frac{ac}{ad-bc}\right] \]",
          [("Parts", r"ax,\ bx"), ("After", r"ax-\frac{qa}{a+b} : bx-\frac{qb}{a+b}+q"), ("Vessel", r"(a+b)x")],
          r"When the ratio is simply reversed (\(a : b\) to \(b : a\)), the vessel is \(\frac{(a+b)^{2}}{a^{2}-b^{2}}\) times the A in the drawn-off mixture. If A is the filler, swap the roles.",
          "'A vessel contains liquids A and B in the ratio a : b; q litres are removed and replaced by B; the ratio becomes c : d; what does the vessel hold?'",
          r"\(5 : 3\), \(16\) litres, \(3 : 5\): \(40\) litres.", r"Adding the filler to the wrong liquid."),
    38: C(38, "Workers and Wages", r"The wage bill is (number of workers) x (pay of each).", r"\[ pr : qs \]",
          [("Workers", r"p : q"), ("Pay", r"r : s"), ("Bill", r"pr : qs")],
          r"Compound the two ratios: the bill falls if \(pr \gt qs\), rises if \(pr \lt qs\).",
          "'An employer reduces the number of his employees in the ratio p : q and increases their wages in the ratio r : s; how does the bill change?'",
          r"\(9 : 8\) and \(14 : 15\): \(126 : 120 = 21 : 20\) - a fall.", r"Adding the ratios instead of multiplying them."),
    39: C(39, "Two Candles", r"Each candle loses a fixed part of its height every hour.", r"\[ \frac{T_1T_2\left(\frac{x}{y}-1\right)}{\frac{x}{y}T_1-T_2} \]",
          [("First after t", r"1-\frac{t}{T_1}"), ("Second after t", r"1-\frac{t}{T_2}"), ("Condition", r"1-\frac{t}{T_1} = \frac{x}{y}\left(1-\frac{t}{T_2}\right)")],
          r"The candle that burns longer (\(T_1\)) is the taller one later on. Turn the hours into hours and minutes at the end.",
          "'Two candles of the same height burn out in T1 and T2 hours; after how many hours is the first twice (x : y times) the second?'",
          r"\(4\) and \(3\) hours, twice: \(\frac{12}{5}\) hours \(= 2\) h \(24\) min.", r"Using the burning times the wrong way round."),
}
ADD = lambda a, b, c, d: f"What number must be added to each term of the ratio {a} : {b} to make it {c} : {d}?"
SUB = lambda a, b, c, d: f"What number must be taken from each term of the ratio {a} : {b} so that it becomes {c} : {d}?"
BKT = lambda a, b, q, c, d: f"A tank holds two liquids A and B in the ratio {a} : {b}. When {q} litres of the mixture are drawn off and the tank is filled up with liquid B, the ratio becomes {c} : {d}. How much of liquid A was in the tank at first?"
BKTB = lambda a, b, q, c, d: f"A tank holds two liquids A and B in the ratio {a} : {b}. When {q} litres of the mixture are drawn off and the tank is filled up with liquid B, the ratio becomes {c} : {d}. How much of liquid B was in the tank at first?"
BKT2 = lambda a, b, q, c, d: f"A tank holds two liquids A and B in the ratio {a} : {b}. When {q} litres of the mixture are drawn off and the tank is filled up with liquid B, the ratio becomes {c} : {d}. How much of liquid B was there at first, and how much does the tank hold?"
VSL = lambda a, b, q, c, d: f"A drum holds liquids P and Q in the ratio {a} : {b}. {q} litres of the mixture are taken out and the same amount of Q is poured in. Now the ratio is {c} : {d}. How much does the drum hold?"
VSLA = lambda a, b, q, c, d: f"A drum holds liquids P and Q in the ratio {a} : {b}. {q} litres of the mixture are taken out and the same amount of P is poured in. Now the ratio is {c} : {d}. How much does the drum hold?"
WG = lambda p, q, r, s: f"A factory cuts the number of its workers in the ratio {p} : {q} and raises their pay in the ratio {r} : {s}. Find the ratio of the old wage bill to the new one."
CN = lambda T1, T2, x, y: f"Two candles of the same height are lit together. The first burns away in {T1} hours and the second in {T2} hours. After how long will the heights of the first and second candles be in the ratio {x} : {y}?"
PICK = {"741": (19, 24, 8, 9), "r34_e1": (7, 31, 11, 15), "r34_e2": (22, 37, 14, 19), "r34_e3": (16, 31, 7, 10), "r34_e4": (14, 43, 2, 3), "r34_e5": (11, 42, 4, 5),
        "r34_e6": (29, 48, 10, 11), "742": (15, 26, 6, 17), "r35_e1": (17, 18, 4, 5), "r35_e2": (29, 33, 13, 17), "r35_e3": (31, 40, 2, 3), "r35_e4": (21, 25, 5, 6),
        "r35_e5": (25, 34, 8, 17), "r35_e6": (25, 34, 10, 19), "r35_e7": (9, 19, 4, 9), "r36_ex": (3, 2, 25, 3, 7), "r36_e1": (7, 8, 15, 7, 23), "r36_e2": (4, 11, 15, 2, 7),
        "r36_e3": (11, 4, 30, 11, 7), "r36_e4": (5, 4, 36, 5, 13), "r36_e5": (4, 5, 18, 2, 7), "743": (9, 7, 32, 3, 13), "r37_e1": (12, 5, 17, 9, 8), "r37_e2": (11, 8, 19, 13, 6),
        "r37_e3": (11, 5, 16, 5, 3), "r37_e4": (11, 7, 18, 11, 25), "r37_e5": (7, 11, 18, 13, 23), "744": (12, 11, 7, 16), "r38_e1": (14, 11, 17, 19), "r38_e2": (11, 7, 9, 17),
        "r38_e3": (17, 14, 7, 10), "r38_e4": (13, 11, 11, 19), "r38_e5": (19, 8, 9, 20), "745": (12, 9, 2, 1), "r39_e1": (6, 4, 2, 1), "r39_e2": (10, 4, 2, 1),
        "r39_e3": (9, 8, 2, 1), "r39_e4": (7, 6, 2, 1), "r39_e5": (9, 6, 2, 1)}
ASK36 = {"r36_ex": ("A", BKT), "r36_e1": ("B", BKTB), "r36_e2": ("A", BKT), "r36_e3": ("B", BKTB), "r36_e4": ("both", BKT2), "r36_e5": ("A", BKT)}


def item(key):
    p = PICK[key]
    rule = {"741": 34, "742": 35, "743": 37, "744": 38, "745": 39}.get(key) or int(key[1:3])
    if rule in (34, 35):
        return rule, (SUB if rule == 35 else ADD)(*p), (lambda p=p, s=(rule == 35): r34(*p, sub=s)), ""
    if rule == 36:
        ask, t = ASK36[key]
        return rule, t(*p), (lambda p=p, ask=ask: r36(*p, ask)), "pair" if ask == "both" else "litres"
    if rule == 37:
        fil = "A" if key == "r37_e2" else "B"
        return rule, (VSLA if fil == "A" else VSL)(*p), (lambda p=p, fil=fil: r37(*p, fil)), "litres"
    if rule == 38:
        return rule, WG(*p), (lambda p=p: r38(*p)), "ratio"
    return rule, CN(*p), (lambda p=p: r39(*p)), "time"


OLD, NEW = {}, {r: [] for r in range(34, 40)}
for key in PICK:
    rule, q, fn, kind = item(key)
    if key.isdigit():
        OLD[int(key)] = (rule, q, fn, kind)
    else:
        NEW[rule].append((key, q, fn, kind, None))


def time_opts(h, m):
    f = lambda hh, mm: rf"\({hh}\) hours \({mm}\) minutes"
    cands = [(h + 1, m), (h, (m + 30) % 60), (h - 1 if h else h + 2, m), (h + 1, (m + 15) % 60)]
    wrong = []
    for c in cands:
        if c != (h, m) and c not in wrong:
            wrong.append(c)
    return place(f(h, m), [f(*w) for w in wrong[:3]])


import gen_1_5  # noqa: E402
_build = gen_1_5.build_opts


def build_opts(g, kind, wrong):
    if kind == "time":
        h, m = g["answer"][1]
        return time_opts(int(h), int(m))
    return _build(g, kind, wrong)


gen_1_5.build_opts = build_opts

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(34, 40))
