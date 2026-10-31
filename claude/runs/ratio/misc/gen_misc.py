"""Ratio and Proportion Miscellaneous (2026-10-30): the book's 35 Miscellaneous problems (pdf pages 24-29). 13 of them are the old
rows 746-758 (M1, M2(i), M3, M4, M6, M7, M9-M14, M26), rewritten here; the other 23 had no copy and are added. Every question is filed
on the stored card of the rule it uses (no new card). Sentences (all-new numbers, gate-tested) are in sentences.py. Book notes: M29 and
M33 have 'data inadequate' answers (no total given) - written with the total, so they have a number for an answer; M23 is written
with x and y. Old keys that were wrong: 752 (key on option e - 81 ml was in no option), 753 (keyed 2 : 3, gold : copper is 3 : 2).
Usage: python misc/gen_misc.py (needs misc/ruleNN/0_current_rows.json from dump_rows.py)."""
import json, os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
from common import new_question, regen_entry, steps  # noqa: E402
from fmt import M, R, UU, answer_json, low, nf, opts, pair_opts, ratio_opts, terms_opts  # noqa: E402
from helpers import place, result  # noqa: E402
import gen_1_5, gen_6_11, gen_12_17, gen_18_25, gen_26_33  # noqa: E402
from sentences import SENT  # noqa: E402

TH = {**{r: gen_1_5.TH[r] for r in (1, 2, 4, 5)}, **{r: gen_6_11.TH[r] for r in (6, 11)}, **{r: gen_12_17.TH[r] for r in (12, 15, 16)},
      **{r: gen_18_25.TH[r] for r in (19, 25)}, 32: gen_26_33.TH[32]}


def make(rule, ans, fin, trad, ident, sub):
    th = TH[rule][0] + "<br>" + TH[rule][1]
    rs = steps(("Identify the values.", ident), ("Apply the specified rule.", TH[rule][1]), ("Substitute the values.", sub))
    return result(ans, th, steps(*trad), rs, fin, [ident, "Answer " + fin + "."], sub)


def num(rule, v, trad, ident, sub, unit=""):
    return make(rule, ("number", F(v)), UU(v, unit), trad, ident, sub)


def rat(rule, a, b, trad, ident, sub):
    return make(rule, ("ratio", (a, b)), R(a, b), trad, ident, sub)


def terms(rule, ts, trad, ident, sub):
    return make(rule, ("terms", tuple(ts)), M(" : ".join(map(str, ts))), trad, ident, sub)


def frc(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


BUILD = {
    746: lambda: num(11, 57, [("Write the numbers as parts.", r"Let them be \(4x, 7x, 8x\): \(16x^{2}+49x^{2}+64x^{2} = 129x^{2} = 1161\), so \(x^{2} = 9\), \(x = 3\)."),
                              ("Add them.", r"The numbers are \(12, 21, 24\); their sum is \(57\).")],
                     r"Ratio \(4 : 7 : 8\), sum of squares \(1161\).", r"One part \(= \sqrt{1161 \div 129} = 3\): \[ (4+7+8)\times 3 = 57 \]"),
    747: lambda: rat(16, 7, 13, [("Chain the ratios.", r"\(\frac{P}{S} = \frac{P}{Q}\times\frac{Q}{R}\times\frac{R}{S} = \frac{7}{12}\times\frac{6}{11}\times\frac{22}{13}\)."),
                                 ("Multiply.", r"\[ \frac{7\times 6\times 22}{12\times 11\times 13} = \frac{924}{1716} = \frac{7}{13} \]")],
                     r"\(7 : 12\), \(6 : 11\), \(22 : 13\).", r"\[ 7\times 6\times 22 : 12\times 11\times 13 = 924 : 1716 = 7 : 13 \]"),
    "m02b": lambda: terms(16, [24, 26, 30, 33], [("Walk along the chain.", r"Take P \(= 12\): Q \(= 13\), R \(= 13\times\frac{15}{13} = 15\), S \(= 15\times\frac{11}{10} = \frac{33}{2}\)."),
                                                ("Whole numbers.", r"Double every term: \(24 : 26 : 30 : 33\).")],
                          r"\(12 : 13\), \(13 : 15\), \(10 : 11\).", r"\[ 12\times 13\times 10 : 13\times 13\times 10 : 13\times 15\times 10 : 13\times 15\times 11 = 24 : 26 : 30 : 33 \]"),
    748: lambda: make(5, ("pair", (F(42), F(105))), f"{M('42')} and {M('105')}",
                      [("Turn the condition into a ratio.", r"\(\frac{x}{3} : \frac{y}{5} = 2 : 3\) gives \(\frac{5x}{3y} = \frac{2}{3}\), so \(x : y = 2 : 5\)."),
                       ("Share 147.", r"\(2+5 = 7\) parts; one part \(= 21\): \(42\) and \(105\).")],
                      r"\(x : y = 2 : 5\), sum \(147\).", r"\[ \frac{2\times 147}{7} = 42,\qquad \frac{5\times 147}{7} = 105 \]"),
    749: lambda: num(32, 600, [("Make the parts.", r"If \(6a = 8b = 9c\), the parts are as \(\frac{1}{6} : \frac{1}{8} : \frac{1}{9} = 12 : 9 : 8\)."),
                               ("Share 1450.", r"\(12+9+8 = 29\) parts; one part \(= 50\); the parts are \(600, 450, 400\). Largest \(= 600\).")],
                     r"Multipliers \(6, 8, 9\).", r"\[ \frac{1}{6} : \frac{1}{8} : \frac{1}{9} = 12 : 9 : 8;\quad \frac{12}{29}\times 1450 = 600 \]"),
    "m05": lambda: num(15, 600, [("Take C's share as 20 parts.", r"B \(= \frac{2}{5}\times 20 = 8\), A \(= \frac{3}{4}\times 8 = 6\): A : B : C \(= 6 : 8 : 20 = 3 : 4 : 10\)."),
                                 ("Share Rs 1020.", r"\(3+4+10 = 17\) parts; one part \(= 60\); C \(= 600\).")],
                       r"A : B \(= 3 : 4\), B : C \(= 2 : 5\).", r"\[ 3\times 2 : 4\times 2 : 4\times 5 = 6 : 8 : 20 = 3 : 4 : 10;\quad \frac{10}{17}\times 1020 = 600 \]", "Rs"),
    750: lambda: rat(2, 5, 3, [("Write the equality.", r"\(\frac{15}{100}p = \frac{25}{100}q\)."), ("Ratio.", r"\(\frac{p}{q} = \frac{25}{15} = \frac{5}{3}\).")],
                     r"\(15\% \text{ of } p = 25\% \text{ of } q\).", r"\[ 15p = 25q \;\Rightarrow\; p : q = 25 : 15 = 5 : 3 \]"),
    751: lambda: rat(15, 28, 33, [("Join the ratios.", r"A : B \(= 11 : 6 = 33 : 18\), B : C \(= 9 : 14 = 18 : 28\), so A : B : C \(= 33 : 18 : 28\)."), ("C : A.", r"\(28 : 33\).")],
                     r"\(11 : 6\) and \(9 : 14\).", r"\[ 11\times 9 : 6\times 9 : 6\times 14 = 99 : 54 : 84 = 33 : 18 : 28 \]so C : A \(= 28 : 33\)."),
    "m08": lambda: num(11, 160, [("Call the equal amount x.", r"A \(= 2(x-30)\), B \(= 3(x-20)\), C \(= 4(x-10)\); together \(9x - 160 = 830\), so \(x = 110\)."),
                                 ("A's share.", r"\(2(110-30) = 160\).")],
                       r"Total Rs \(830\).", r"\[ 2(x-30)+3(x-20)+4(x-10) = 830 \;\Rightarrow\; x = 110,\ A = 160 \]", "Rs"),
    752: lambda: num(19, 50, [("Juice and water now.", r"Juice \(= 450\times\frac{8}{9} = 400\) ml, water \(= 50\) ml."),
                              ("Water needed.", r"For \(4 : 1\) the water must be \(100\) ml; add \(100 - 50 = 50\) ml.")],
                     r"\(x = 450\), \(8 : 1\) to \(4 : 1\).", r"\[ \frac{450(8\times 1-1\times 4)}{4(8+1)} = \frac{1800}{36} = 50 \]", "ml"),
    753: lambda: rat(12, 4, 3, [("Weigh x of silver and y of tin.", r"\(13x + 6y = 10(x+y)\), so \(3x = 4y\)."), ("Ratio.", r"\(x : y = 4 : 3\).")],
                     r"Silver \(13\), tin \(6\), alloy \(10\) (times as heavy as water).", r"\[ \frac{13x+6y}{x+y} = 10 \;\Rightarrow\; x : y = (10-6) : (13-10) = 4 : 3 \]"),
    754: lambda: terms(15, [1, 4, 10], [("Take R as 10.", r"Q \(= \frac{2}{5}\times 10 = 4\), P \(= \frac{1}{4}\times 4 = 1\)."), ("Ratio.", r"P : Q : R \(= 1 : 4 : 10\).")],
                       r"P : Q \(= 1 : 4\), Q : R \(= 2 : 5\).", r"\[ 1\times 2 : 4\times 2 : 4\times 5 = 2 : 8 : 20 = 1 : 4 : 10 \]"),
    755: lambda: num(5, 5200, [("One part.", r"Babu's \(8\) parts are Rs \(3200\): one part \(= 400\)."), ("The sum.", r"\(13\times 400 = 5200\).")],
                     r"Ratio \(5 : 8\), Babu Rs \(3200\).", r"\[ \frac{5+8}{8}\times 3200 = 5200 \]", "Rs"),
    756: lambda: rat(5, 3, 1, [("Parts must divide 15.", r"Broken : unbroken \(= a : b\) means \(15\) eggs make \(a+b\) equal parts, so \(a+b\) must divide \(15\)."),
                               ("Check each.", r"\(2 : 1\) (3 parts), \(1 : 4\) (5), \(3 : 2\) (5) are possible; \(3 : 1\) needs 4 parts, and 4 does not divide 15.")],
                     r"\(15\) eggs; ratios \(2 : 1, 1 : 4, 3 : 2, 3 : 1\).", r"\(x = 15\) must be \((a+b)\) times a whole number: \(\frac{15}{3+1}\) is not whole, so \(3 : 1\) cannot be."),
    757: lambda: rat(5, 1, 3, [("Desks first.", r"\(9500 \div 1500\) gives \(6\) desks for Rs \(9000\); Rs \(500\) is left."),
                               ("Stools.", r"\(500 \div 250 = 2\) stools: stools : desks \(= 2 : 6 = 1 : 3\).")],
                     r"Desks Rs \(1500\), stools Rs \(250\), Rs \(9500\).", r"\[ 2 : 6 = 1 : 3 \]"),
    "m15": lambda: num(15, 17200, [("Join the ratios.", r"A : B \(= 1 : 0.8 = 5 : 4\), B : C \(= 1 : 0.75 = 4 : 3\), so A : B : C \(= 5 : 4 : 3\)."),
                                   ("Share.", r"\(12\) parts make Rs \(51600\); one part \(= 4300\); B \(= 4\times 4300 = 17200\).")],
                       r"A : B \(= 100 : 80\), B : C \(= 100 : 75\).", r"\[ 5 : 4 : 3;\quad \frac{4}{12}\times 51600 = 17200 \]", "Rs"),
    "m16": lambda: num(11, 2400, [("A's share.", r"A \(= \frac{1}{3}(B+C)\), so A is \(\frac{1}{4}\) of the whole: A \(= 1800\)."),
                                  ("B and C.", r"B \(= \frac{1}{5}(A+C)\), so B is \(\frac{1}{6}\) of the whole: B \(= 1200\); C \(= 7200-1800-1200 = 4200\). C \(-\) A \(= 2400\).")],
                      r"Total Rs \(7200\).", r"A : B : C \(= 1800 : 1200 : 4200 = 3 : 2 : 7\); \[ \frac{7-3}{12}\times 7200 = 2400 \]", "Rs"),
    "m17": lambda: num(4, F("21.6"), [("Weight of 1 m.", r"\(40.5 \div 15 = 2.7\) kg."), ("8 m.", r"\(8\times 2.7 = 21.6\) kg.")],
                       r"\(15\) m : \(8\) m \(::\) \(40.5\) kg : x.", r"\[ x = \frac{8\times 40.5}{15} = 21.6 \]", "kg"),
    "m18": lambda: num(15, 2430, [("Join the ratios.", r"Asha : Bina \(= 25 : 45\), Bina : Chitra \(= 45 : 81\), so Asha : Chitra \(= 25 : 81\)."),
                                  ("Chitra.", r"\(\frac{81}{25}\times 750 = 2430\).")],
                      r"\(5 : 9\) and \(5 : 9\); Asha Rs \(750\).", r"\[ 5\times 5 : 9\times 5 : 9\times 9 = 25 : 45 : 81;\quad \frac{81}{25}\times 750 = 2430 \]", "Rs"),
    "m19": lambda: num(25, 195, [("Each term rises by 1 part.", r"\(3 : 4 : 6\) to \(4 : 5 : 7\): every term rises by \(1\), and every class gains \(15\), so one part \(= 15\)."),
                                 ("Total before.", r"\((3+4+6)\times 15 = 195\).")],
                       r"\(3 : 4 : 6\) to \(4 : 5 : 7\), \(15\) added.", r"\[ \frac{(3+4+6)\times 15}{1} = 195 \]", "pupils"),
    "m20": lambda: num(11, 2250, [("Pay now in parts.", r"Last year \(3k\) and \(4k\). Now Hari \(= 3k\times\frac{3}{2} = 4.5k\), Ravi \(= 4k\times\frac{6}{5} = 4.8k\)."),
                                  ("Use the total.", r"\(9.3k = 4650\), so \(k = 500\); Hari now \(= 4.5\times 500 = 2250\).")],
                      r"Now Hari : Ravi \(= 4.5 : 4.8 = 15 : 16\), total Rs \(4650\).", r"\[ \frac{15}{31}\times 4650 = 2250 \]", "Rs"),
    "m21": lambda: num(15, 12, [("Join the ratios.", r"\(1 : 2 = 3 : 6\) and \(3 : 4 = 6 : 8\): the numbers are \(3x, 6x, 8x\)."),
                                ("Use the squares.", r"\(9x^{2}+36x^{2}+64x^{2} = 109x^{2} = 436\), so \(x = 2\); the second number is \(12\).")],
                     r"\(1 : 2\) and \(3 : 4\); sum of squares \(436\).", r"\[ 1\times 3 : 2\times 3 : 2\times 4 = 3 : 6 : 8;\quad 6\times 2 = 12 \]"),
    "m22": lambda: rat(1, 9, 1, [("a : b.", r"\(\frac{bc}{ca} = \frac{1}{3}\), so \(\frac{b}{a} = \frac{1}{3}\): a : b \(= 3 : 1\)."),
                                 ("The asked ratio.", r"\(\frac{a}{bc} : \frac{b}{ca} = \frac{a^{2}}{abc} : \frac{b^{2}}{abc} = a^{2} : b^{2} = 9 : 1\).")],
                     r"bc : ca : ab \(= 1 : 3 : 4\).", r"\(\frac{a}{bc} : \frac{b}{ca}\) is the duplicate ratio of a : b: \[ 3^{2} : 1^{2} = 9 : 1 \]"),
    "m23": lambda: make(5, ("expr", F(21, 4)), M(r"\frac{xy}{y+1}"),
                        [("Write the numbers.", r"First \(= y\) times the second. If the second is \(s\), then \(ys + s = x\), so \(s = \frac{x}{y+1}\)."),
                         ("The first.", r"\(ys = \frac{xy}{y+1}\).")],
                        r"Ratio first : second \(= y : 1\), sum \(x\).", r"\[ \frac{y\times x}{y+1} = \frac{xy}{y+1} \]"),
    "m24": lambda: num(6, 36, [("Value of one set.", r"\(2\times 1 + 3\times 0.5 + 4\times 0.25 + 5\times 0.1 = 5\) rupees."),
                               ("Sets and coins.", r"\(45 \div 5 = 9\) sets; 25 paise coins \(= 4\times 9 = 36\).")],
                     r"Numbers \(2 : 3 : 4 : 5\), Rs \(45\).", r"\[ \frac{45}{5} = 9;\quad 4\times 9 = 36 \]", "coins"),
    "m25": lambda: rat(1, 7, 12, [("New numbers.", r"Boys \(7k\times 1.10 = 7.7k\), girls \(8k\times 1.65 = 13.2k\)."), ("Ratio.", r"\(7.7 : 13.2 = 77 : 132 = 7 : 12\).")],
                       r"\(7 : 8\) compounded with \(110 : 165\).", r"\[ 7\times 110 : 8\times 165 = 770 : 1320 = 7 : 12 \]"),
    758: lambda: num(11, 2400, [("Write the shares as parts.", r"X \(= 5k\), Y \(= 11k\), Z \(= 8k\); after the gift \(5k : 11k+300 : 8k-300 = 5 : 14 : 5\)."),
                                ("Solve.", r"X and Z become equal: \(5k = 8k - 300\), so \(k = 100\); total \(= 24k = 2400\).")],
                     r"\(5 : 11 : 8\) to \(5 : 14 : 5\), Rs \(300\) moved.", r"\[ 5k = 8k-300 \Rightarrow k = 100;\quad (5+11+8)\times 100 = 2400 \]", "Rs"),
    "m27": lambda: rat(2, 5, 3, [("Equation.", r"\(\frac{25}{100}x = \frac{15}{100}y\)."), ("Ratio.", r"\(y : x = 25 : 15 = 5 : 3\).")],
                       r"\(25\%\) of x \(= 15\%\) of y.", r"\[ 25x = 15y \;\Rightarrow\; y : x = 5 : 3 \]"),
    "m28": lambda: num(5, 24, [("The first number.", r"\(30\%\) of it is \(21\), so it is \(70\)."), ("The second.", r"\(7\) parts \(= 70\), one part \(= 10\), second \(= 60\); \(40\%\) of \(60 = 24\).")],
                       r"Ratio \(7 : 6\).", r"\[ 60\times\frac{40}{100} = 24 \]"),
    "m29": lambda: num(11, 750, [("One part.", r"\(3+7+15 = 25\) parts make Rs \(6250\): one part \(= 250\)."), ("P.", r"\(3\times 250 = 750\).")],
                       r"Ratio \(3 : 7 : 15\), Rs \(6250\).", r"\[ \frac{3\times 6250}{25} = 750 \]", "Rs"),
    "m30": lambda: rat(2, 3, 2, [("Equation.", r"\(y + 0.4x = 1.6y\), so \(0.4x = 0.6y\)."), ("Ratio.", r"\(x : y = 0.6 : 0.4 = 3 : 2\).")],
                       r"\(40\%\) of x \(= 60\%\) of y.", r"\[ 40x = 60y \;\Rightarrow\; x : y = 3 : 2 \]"),
    "m31": lambda: rat(2, 5, 9, [("Equation.", r"\(y - 0.45x = \frac{3}{4}y\), so \(0.45x = 0.25y\)."), ("Ratio.", r"\(x : y = 0.25 : 0.45 = 5 : 9\).")],
                       r"\(45\%\) of x \(= 25\%\) of y.", r"\[ 45x = 25y \;\Rightarrow\; x : y = 5 : 9 \]"),
    "m32": lambda: rat(2, 1, 3, [("Equation.", r"\(y + 0.3x = \frac{11}{10}y\), so \(0.3x = 0.1y\)."), ("Ratio.", r"\(x : y = 0.1 : 0.3 = 1 : 3\).")],
                       r"\(30\%\) of x \(= 10\%\) of y.", r"\[ 30x = 10y \;\Rightarrow\; x : y = 1 : 3 \]"),
    "m33": lambda: num(11, 2000, [("One part.", r"\(3+5+6 = 14\) parts make Rs \(5600\): one part \(= 400\)."), ("Q.", r"\(5\times 400 = 2000\).")],
                       r"Ratio \(3 : 5 : 6\), Rs \(5600\).", r"\[ \frac{5\times 5600}{14} = 2000 \]", "Rs"),
    "m34": lambda: rat(2, 18, 17, [("Put a = 3k, b = 4k.", r"\(2a+3b = 6k+12k = 18k\), \(3a+2b = 9k+8k = 17k\)."), ("Ratio.", r"\(18 : 17\).")],
                       r"a : b \(= 3 : 4\).", r"\[ \frac{2\times 3+3\times 4}{3\times 3+2\times 4} = \frac{18}{17} \]"),
    "m35": lambda: num(6, 288, [("Value of one set.", r"\(3\times 1 + 4\times 0.5 + 8\times 0.25 = 7\) rupees."), ("Sets and coins.", r"\(252 \div 7 = 36\) sets; 25 paise coins \(= 8\times 36 = 288\).")],
                       r"Numbers \(3 : 4 : 8\), Rs \(252\).", r"\[ \frac{252}{7} = 36;\quad 8\times 36 = 288 \]", "coins"),
}
UNIT = {748: "pair", "m05": "Rs", "m08": "Rs", 752: "ml", 755: "Rs", "m15": "Rs", "m16": "Rs", "m17": "kg", "m18": "Rs", "m19": "pupils", "m20": "Rs",
        "m24": "coins", 758: "Rs", "m29": "Rs", "m33": "Rs", "m35": "coins"}
E = lambda s: M(s)
WRONG = {"m23": [E(r"\frac{x}{y+1}"), E(r"\frac{xy}{y-1}"), E(r"\frac{x+y}{y+1}")]}


def options(key, g):
    a = g["answer"]
    if key == 756:                                     # the one ratio that cannot be
        return place(R(3, 1), [R(2, 1), R(1, 4), R(3, 2)])
    if key in WRONG:
        return place(g["solution"][g["solution"].rfind("Final Answer: ") + 14:].split("</b>")[0], WRONG[key])
    if a[0] == "ratio":
        return ratio_opts(*a[1])
    if a[0] == "terms":
        return terms_opts(a[1])
    if a[0] == "pair":
        return pair_opts(*a[1])
    return opts(a[1], UNIT.get(key, ""))


def main():
    by_rule = {}
    for key, (rule, q) in SENT.items():
        by_rule.setdefault(rule, []).append((key, q))
    for rule, items in sorted(by_rule.items()):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"], rule
        rows = {r["id"]: r for r in dump["rows"]}
        olds = [k for k, _ in items if isinstance(k, int)]
        assert sorted(rows) == sorted(olds), (rule, sorted(rows), olds)
        out, qs, answers = [], [], []
        for key, q in items:
            g = BUILD[key]()
            op, pos = options(key, g)
            if isinstance(key, int):
                extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
                extra = {k: v for k, v in extra.items() if v != rows[key][k]}
                out.append(regen_entry(rows[key], g, dump["rule_card"]["id"], extra))
            else:
                qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
                answers.append([key, answer_json(g["answer"])])
        if out:
            json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        if qs:
            json.dump({"rules_html": [{"chapter": "ratio_n_proportion", "rule_name": f"Rule {rule}", "rule_html": dump["rule_card"]["rule_html"]}], "questions": qs},
                      open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(out)} old rows, {len(qs)} new questions")


if __name__ == "__main__":
    main()
