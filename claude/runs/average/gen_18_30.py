"""Average Rules 18-30 (2026-10-30). 18: equal distances at x and y - 2xy/(x + y). 19: three equal parts - 3xyz/(xy + yz + zx).
20: A km at x, B km at y, C km at z - total distance over total time. 21: fractions of the distance at x, y, z - 1/(a/x + b/y + c/z).
22: the other part's head count n(y - x)/(x - z). 23: the first part's head count n(x - z)/(y - x). 24: mess bill - the original
average from the rise in the bill and the fall in the average. 25: first n natural numbers - (n + 1)/2. 26: a bag weighed with
the balls - old average + rise x (n + 1). 27 / 28: consecutive numbers - the middle number / the mean of the two middle numbers.
29 / 30: odd (even) numbers from 1 to n - (last + 1)/2, (last + 2)/2. Writes the cards, regenerates the old rows 511-518 with
simple-style sentences and all-new numbers (516's key was on the empty option e), and adds the book's examples / exercises with
no copy (Rule 23 Exr 5 asks for the whole class; the book prints the number of boys). Usage: python gen_18_30.py"""
import json, os, sys
from fractions import Fraction as F
from math import lcm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_6_11 import UU, answer_json, nf, opts  # noqa: E402
from helpers import place, result  # noqa: E402

KMH = "km/hr"


def ops(v, unit="", wrong=None):
    v = F(v)
    if wrong is None and v.denominator != 1:
        wrong = [v + 1, v - 1, v + 2] if v > 1 else [v + 1, v + 2, v + 3]
    if unit == "Rs":
        if wrong is None:
            step = max(1, v // 10)
            wrong = [v + step, v - step, v + 2 * step]
        return place(money_s(v), [money_s(w) for w in wrong])
    return opts(v, unit, wrong)


def money_s(v):
    return "Rs " + chr(92) + "(" + nf(v) + chr(92) + ")"


def th(statement, formula):
    return statement + "<br>" + formula


TH = {
    18: th(r"If a distance is covered at \(x\) km/hr and the same distance again at \(y\) km/hr (half the way at each speed, or there "
           r"and back), the average speed is", r"\[ \frac{2xy}{x+y} \]"),
    19: th(r"If three equal distances are covered at \(x\), \(y\) and \(z\) km/hr, the average speed is", r"\[ \frac{3xyz}{xy+yz+zx} \]"),
    20: th(r"If \(A\) km are covered at \(x\) km/hr, \(B\) km at \(y\) km/hr and \(C\) km at \(z\) km/hr, the average speed is",
           r"\[ \frac{A+B+C}{\frac{A}{x}+\frac{B}{y}+\frac{C}{z}} \]"),
    21: th(r"If the fractions \(a\), \(b\) and \(c\) of a distance (\(a+b+c=1\)) are covered at \(x\), \(y\) and \(z\) km/hr, the average speed is",
           r"\[ \frac{1}{\frac{a}{x}+\frac{b}{y}+\frac{c}{z}} \]"),
    22: th(r"If the average of a whole group is \(x\), the \(n\) members of one part average \(y\) and the rest average \(z\), the number in the rest is",
           r"\[ \frac{n(y-x)}{x-z} \]"),
    23: th(r"If the average of a whole group is \(x\), one part averages \(y\), the rest average \(z\) and there are \(n\) in the rest, the number in the first part is",
           r"\[ \frac{n(x-z)}{y-x} \]"),
    24: th(r"If \(N\) people share a bill, \(z\) more join, the bill rises by \(y\) and the share of each falls by \(x\), the old share is "
           r"\(\frac{x(N+z)+y}{z}\) and the original bill is", r"\[ N\times\frac{x(N+z)+y}{z} \]"),
    25: th(r"The average of the first \(n\) natural numbers is", r"\[ \frac{n+1}{2} \]"),
    26: th(r"If \(n\) objects average \(a\) and, with their bag weighed in as one more object, the average rises by \(r\), the bag weighs",
           r"\[ a + r(n+1) \]"),
    27: th(r"The average of an odd number of consecutive numbers (or consecutive odd / even numbers) is", r"\[ \text{the middle number} \]"),
    28: th(r"The average of an even number of consecutive numbers (or consecutive odd / even numbers) is the mean of the two middle numbers:",
           r"\[ \frac{\text{smaller middle} + \text{larger middle}}{2} \]"),
    29: th(r"The average of the odd numbers from \(1\) to \(n\) (\(n\) odd) is", r"\[ \frac{n+1}{2} \]"),
    30: th(r"The average of the even numbers from \(2\) to \(n\) (\(n\) even) is", r"\[ \frac{n+2}{2} \]"),
}


def apply(r):
    return ("Apply the specified rule.", TH[r].split("<br>")[1])


def R(rule, v, trad, rb, sub, unit, extra_rb=()):
    """result with the usual three-step Specified Rule (identify / apply / substitute)."""
    rule_steps = steps(("Identify the values.", rb), apply(rule), ("Substitute the values.", sub))
    fin = money_s(v) if unit == "Rs" else UU(v, unit)
    return result(("number", F(v)), TH[rule], trad, rule_steps, fin, list(extra_rb) or [rb, rf"Answer \(= {nf(v)}\)."], sub)


def times_table(parts):
    """parts of (distance, speed) -> rows 'd km at s km/hr: d/s hr'."""
    return "<br>".join(rf"\({nf(d)}\) km at \({nf(s)}\) km/hr: \(\frac{{{nf(d)}}}{{{nf(s)}}} = {nf(d / s)}\) hr" for d, s in parts)


def r18(x, y):
    x, y = F(x), F(y)
    D = lcm(int(x), int(y))
    v = 2 * x * y / (x + y)
    trad = steps(("Take a distance.", rf"Let each way be \({D}\) km (a number both speeds divide)."),
                 ("Time for each way.", times_table([(D, x), (D, y)])),
                 ("Average speed.", rf"\[ \frac{{2\times {D}}}{{{nf(D / x)}+{nf(D / y)}}} = \frac{{{2 * D}}}{{{nf(D / x + D / y)}}} = {nf(v)} \]"))
    return R(18, v, trad, rf"\(x = {nf(x)}\), \(y = {nf(y)}\).", rf"\[ \frac{{2\times {nf(x)}\times {nf(y)}}}{{{nf(x)}+{nf(y)}}} = \frac{{{nf(2 * x * y)}}}{{{nf(x + y)}}} = {nf(v)} \]", KMH)


def r19(x, y, z):
    x, y, z = map(F, (x, y, z))
    D = lcm(int(x), int(y), int(z))
    v = 3 * x * y * z / (x * y + y * z + z * x)
    tt = D / x + D / y + D / z
    trad = steps(("Take a distance.", rf"Let each part be \({D}\) km."), ("Time for each part.", times_table([(D, x), (D, y), (D, z)])),
                 ("Average speed.", rf"\[ \frac{{3\times {D}}}{{{nf(tt)}}} = \frac{{{3 * D}}}{{{nf(tt)}}} = {nf(v)} \]"))
    sub = (rf"\[ \frac{{3\times {nf(x)}\times {nf(y)}\times {nf(z)}}}{{{nf(x * y)}+{nf(y * z)}+{nf(z * x)}}} = \frac{{{nf(3 * x * y * z)}}}{{{nf(x * y + y * z + z * x)}}} = {nf(v)} \]")
    return R(19, v, trad, rf"\(x = {nf(x)}\), \(y = {nf(y)}\), \(z = {nf(z)}\).", sub, KMH)


def r20(parts):
    parts = [(F(d), F(s)) for d, s in parts]
    D = sum(d for d, _ in parts)
    T = sum(d / s for d, s in parts)
    v = D / T
    trad = steps(("Time for each stretch.", times_table(parts)), ("Totals.", rf"Distance \(= {nf(D)}\) km, time \(= {nf(T)}\) hr."),
                 ("Average speed.", rf"\[ \frac{{{nf(D)}}}{{{nf(T)}}} = {nf(v)} \]"))
    top = "+".join(nf(d) for d, _ in parts)
    bot = "+".join(rf"\frac{{{nf(d)}}}{{{nf(s)}}}" for d, s in parts)
    return R(20, v, trad, ", ".join(rf"\({nf(d)}\) km at \({nf(s)}\)" for d, s in parts) + ".", rf"\[ \frac{{{top}}}{{{bot}}} = \frac{{{nf(D)}}}{{{nf(T)}}} = {nf(v)} \]", KMH)


def fr(f):
    f = F(f)
    return str(f.numerator) if f.denominator == 1 else rf"\frac{{{f.numerator}}}{{{f.denominator}}}"


def r21(parts):
    """parts of (fraction of the distance, speed); the fractions add up to 1."""
    parts = [(F(f), F(s)) for f, s in parts]
    assert sum(f for f, _ in parts) == 1
    D = lcm(*[(f / s).denominator for f, s in parts])
    T = sum(f * D / s for f, s in parts)
    v = D / T
    trad = steps(("Take a distance.", rf"Let the whole way be \({D}\) km, so the parts are " + ", ".join(rf"\({nf(f * D)}\) km" for f, _ in parts) + "."),
                 ("Time for each part.", times_table([(f * D, s) for f, s in parts])),
                 ("Average speed.", rf"\[ \frac{{{D}}}{{{nf(T)}}} = {nf(v)} \]"))
    bot = "+".join(rf"\frac{{{f.numerator}}}{{{f.denominator}\times {nf(s)}}}" for f, s in parts)
    sub = rf"\[ \frac{{1}}{{{bot}}} = \frac{{1}}{{{fr(T / D)}}} = {nf(v)} \]"
    return R(21, v, trad, ", ".join(rf"\({fr(f)}\) at \({nf(s)}\)" for f, s in parts) + ".", sub, KMH)


def r22(x, n, y, z, unit="Rs"):
    """overall average x; n members of the first part average y; the rest average z -> how many in the rest."""
    x, n, y, z = map(F, (x, n, y, z))
    m = n * (y - x) / (x - z)
    f = (lambda t: rf"Rs {nf(t)}") if unit == "Rs" else nf
    trad = steps(("Let the others be \\(m\\).", rf"Total \(= {tex(n)}\times {nf(y)} + {nf(z)}m = {nf(x)}({tex(n)}+m)\)."),
                 ("Solve.", rf"\[ {nf(x - z)}m = {tex(n)}({nf(y)}-{nf(x)}) = {nf(n * (y - x))} \;\Rightarrow\; m = {nf(m)} \]"))
    sub = rf"\[ \frac{{{tex(n)}({nf(y)}-{nf(x)})}}{{{nf(x)}-{nf(z)}}} = \frac{{{nf(n * (y - x))}}}{{{nf(x - z)}}} = {nf(m)} \]"
    return R(22, m, trad, rf"\(x = {nf(x)}\), \(n = {tex(n)}\), \(y = {nf(y)}\), \(z = {nf(z)}\).", sub, "")


def r23(x, y, z, n, total=False):
    """overall x; boys average y; girls average z; n girls -> the number of boys (or of all)."""
    x, y, z, n = map(F, (x, y, z, n))
    b = n * (x - z) / (y - x)
    v = b + n if total else b
    trad = [("Let the boys be \\(b\\).", rf"Total age \(= {nf(y)}b + {nf(z)}\times {tex(n)} = {nf(x)}(b+{tex(n)})\)."),
            ("Solve.", rf"\[ {nf(y - x)}b = {tex(n)}({nf(x)}-{nf(z)}) = {nf(n * (x - z))} \;\Rightarrow\; b = {nf(b)} \]")]
    sub = rf"\[ \frac{{{tex(n)}({nf(x)}-{nf(z)})}}{{{nf(y)}-{nf(x)}}} = \frac{{{nf(n * (x - z))}}}{{{nf(y - x)}}} = {nf(b)} \]"
    if total:
        trad.append(("The whole class.", rf"\[ {nf(b)} + {tex(n)} = {nf(v)} \]"))
        sub += rf"Whole class \(= {nf(b)}+{tex(n)} = {nf(v)}\)."
    return R(23, v, steps(*trad), rf"\(x = {nf(x)}\), \(y = {nf(y)}\), \(z = {nf(z)}\), \(n = {tex(n)}\).", sub, "")


def r24(N, z, y, x):
    """N people, z more join, the bill rises by y, the share falls by x -> the original bill."""
    N, z, y, x = map(F, (N, z, y, x))
    A = (x * (N + z) + y) / z
    v = N * A
    trad = steps(("Let the old share be \\(A\\).", rf"Old bill \(= {tex(N)}A\); new bill \(= {tex(N)}A + {nf(y)} = {tex(N + z)}(A - {nf(x)})\)."),
                 ("Solve.", rf"\[ {tex(z)}A = {tex(N + z)}\times {nf(x)} + {nf(y)} = {nf(x * (N + z) + y)} \;\Rightarrow\; A = {nf(A)} \]"),
                 ("Original bill.", rf"\[ {tex(N)}\times {nf(A)} = {nf(v)} \]"))
    sub = rf"\[ {tex(N)}\times\frac{{{nf(x)}({tex(N)}+{tex(z)})+{nf(y)}}}{{{tex(z)}}} = {tex(N)}\times {nf(A)} = {nf(v)} \]"
    return R(24, v, trad, rf"\(N = {tex(N)}\), \(z = {tex(z)}\), \(y = {nf(y)}\), \(x = {nf(x)}\).", sub, "Rs")


def r25(n):
    n = F(n)
    S = n * (n + 1) / 2
    v = S / n
    trad = steps(("Pair the numbers.", rf"\(1+{tex(n)}\), \(2+{tex(n - 1)}\), ... each pair makes \({tex(n + 1)}\); there are \({nf(n / 2)}\) pairs, so the sum is "
                                       rf"\({nf(n / 2)}\times {tex(n + 1)} = {nf(S)}\)."),
                 ("Average.", rf"\[ {nf(S)} \div {tex(n)} = {nf(v)} \]"))
    return R(25, v, trad, rf"\(n = {tex(n)}\).", rf"\[ \frac{{{tex(n)}+1}}{{2}} = {nf(v)} \]", "")


def r26(n, a, r, unit):
    n, a, r = map(F, (n, a, r))
    v = (n + 1) * (a + r) - n * a
    trad = steps(("Total of the objects.", rf"\[ {tex(n)}\times {nf(a)} = {nf(n * a)} \]"),
                 ("Total with the container.", rf"\({tex(n + 1)}\) items now average \({nf(a + r)}\): \[ {tex(n + 1)}\times {nf(a + r)} = {nf((n + 1) * (a + r))} \]"),
                 ("The container.", rf"\[ {nf((n + 1) * (a + r))} - {nf(n * a)} = {nf(v)} \]"))
    return R(26, v, trad, rf"\(n = {tex(n)}\), \(a = {nf(a)}\), \(r = {nf(r)}\).", rf"\[ {nf(a)} + {nf(r)}\times {tex(n + 1)} = {nf(a)} + {nf(r * (n + 1))} = {nf(v)} \]", unit)


def series(first, last, step):
    return list(range(first, last + 1, step))


def listing(xs):
    return ", ".join(str(t) for t in xs) if len(xs) <= 8 else ", ".join(str(t) for t in xs[:3]) + r", \(\ldots\), " + ", ".join(str(t) for t in xs[-2:])


def r27(first, last, step):
    xs = series(first, last, step)
    assert len(xs) % 2 == 1
    v = F(sum(xs), len(xs))
    mid = xs[len(xs) // 2]
    trad = steps(("Add them.", rf"{listing(xs)}: sum \(= {sum(xs)}\), count \(= {len(xs)}\)."), ("Average.", rf"\[ {sum(xs)} \div {len(xs)} = {nf(v)} \]"))
    return R(27, v, trad, rf"\({len(xs)}\) numbers (odd count); the middle one is number \({len(xs) // 2 + 1}\).", rf"\[ \text{{middle number}} = {mid} \]", "")


def r28(first, last, step):
    xs = series(first, last, step)
    assert len(xs) % 2 == 0
    v = F(sum(xs), len(xs))
    a, b = xs[len(xs) // 2 - 1], xs[len(xs) // 2]
    trad = steps(("Add them.", rf"{listing(xs)}: sum \(= {sum(xs)}\), count \(= {len(xs)}\)."), ("Average.", rf"\[ {sum(xs)} \div {len(xs)} = {nf(v)} \]"))
    return R(28, v, trad, rf"\({len(xs)}\) numbers (even count); the middle two are \({a}\) and \({b}\).", rf"\[ \frac{{{a}+{b}}}{{2}} = {nf(v)} \]", "")


def r29(n):
    xs = series(1, n, 2)
    v = F(sum(xs), len(xs))
    trad = steps(("Count and pair them.", rf"\(1, 3, \ldots, {n}\) are \({len(xs)}\) numbers; \(1+{n} = 3+{n - 2} = \ldots = {n + 1}\), so the sum is "
                                          rf"\(\frac{{{len(xs)}\times {n + 1}}}{{2}} = {sum(xs)}\)."),
                 ("Average.", rf"\[ {sum(xs)} \div {len(xs)} = {nf(v)} \]"))
    return R(29, v, trad, rf"Last odd number \(n = {n}\).", rf"\[ \frac{{{n}+1}}{{2}} = {nf(v)} \]", "")


def r30(n):
    xs = series(2, n, 2)
    v = F(sum(xs), len(xs))
    trad = steps(("Count and pair them.", rf"\(2, 4, \ldots, {n}\) are \({len(xs)}\) numbers; \(2+{n} = 4+{n - 2} = \ldots = {n + 2}\), so the sum is "
                                          rf"\(\frac{{{len(xs)}\times {n + 2}}}{{2}} = {sum(xs)}\)."),
                 ("Average.", rf"\[ {sum(xs)} \div {len(xs)} = {nf(v)} \]"))
    return R(30, v, trad, rf"Last even number \(n = {n}\).", rf"\[ \frac{{{n}+2}}{{2}} = {nf(v)} \]", "")


C = card
CARDS = {
    18: C(18, "Average Speed - Two Equal Distances", r"Equal distances at two speeds: the average speed is the harmonic mean of the speeds, not the plain mean.",
          r"\[ \frac{2xy}{x+y} \]", [("Time", r"\frac{d}{x}+\frac{d}{y}"), ("Distance", r"2d"), ("Average", r"\frac{2xy}{x+y}")],
          r"More time is spent at the lower speed, so the average is pulled below \(\frac{x+y}{2}\). Half the way at each speed and there-and-back are the same case.",
          "'goes at x km/hr and returns at y km/hr' / 'half the journey at x, the other half at y'.", r"\(40\) and \(60\): \(\frac{2\times 40\times 60}{100}=48\) km/hr.",
          r"Taking \(\frac{x+y}{2}\)."),
    19: C(19, "Average Speed - Three Equal Distances", r"Three equal parts at three speeds.", r"\[ \frac{3xyz}{xy+yz+zx} \]",
          [("Time", r"\frac{d}{x}+\frac{d}{y}+\frac{d}{z}"), ("Distance", r"3d"), ("Average", r"\frac{3xyz}{xy+yz+zx}")],
          r"It is the harmonic mean of the three speeds: \(\frac{3}{\frac{1}{x}+\frac{1}{y}+\frac{1}{z}}\).",
          "'divides the journey into three equal parts at x, y and z km/hr' / 'first, second and third km at ...'.",
          r"\(10, 20, 60\): \(\frac{3\times 12000}{200+1200+600}=18\) km/hr.", r"Adding the three speeds and dividing by \(3\)."),
    20: C(20, "Average Speed - Given Distances", r"Total distance divided by total time.", r"\[ \frac{A+B+C}{\frac{A}{x}+\frac{B}{y}+\frac{C}{z}} \]",
          [("Times", r"\frac{A}{x},\ \frac{B}{y},\ \frac{C}{z}"), ("Distance", r"A+B+C"), ("Average", r"\frac{\text{distance}}{\text{time}}")],
          r"Each stretch's time is its distance over its speed; the average speed is never the mean of the speeds unless the times are equal.",
          "'covers A km at x km/hr, B km at y km/hr and C km at z km/hr; find the average speed'.", r"\(10\) km at \(5\), \(20\) km at \(10\): \(\frac{30}{2+2}=7.5\) km/hr.",
          r"Averaging the speeds instead of dividing distance by time."),
    21: C(21, "Average Speed - Fractions of the Distance", r"Parts of the whole distance (fractions or per cents) at different speeds.",
          r"\[ \frac{1}{\frac{a}{x}+\frac{b}{y}+\frac{c}{z}} \]", [("Whole way", r"1"), ("Time", r"\frac{a}{x}+\frac{b}{y}+\frac{c}{z}"), ("Average", r"\frac{1}{\text{time}}")],
          r"Take the whole distance as \(1\) (or \(100\) for per cents); each part's time is its share over its speed.",
          "'covers a fraction / p% of the distance at x km/hr, the next ... at y km/hr and the rest at z km/hr'.",
          r"Half at \(10\), half at \(40\): \(\frac{1}{0.05+0.0125}=16\) km/hr.", r"Forgetting to work out the remaining fraction."),
    22: C(22, "Head Count of the Other Part", r"Like an alligation: the two part averages sit on either side of the overall average.", r"\[ \frac{n(y-x)}{x-z} \]",
          [("Above average", r"n\ \text{at}\ y\ \text{give}\ n(y-x)"), ("Below average", r"m\ \text{at}\ z\ \text{take}\ m(x-z)"), ("Balance", r"m = \frac{n(y-x)}{x-z}")],
          r"What the higher part has above the overall average must equal what the lower part lacks below it.",
          "'average salary of all is x, of the n officers y, of the others z; how many others?'",
          r"All \(50\), \(10\) officers at \(90\), others at \(40\): \(\frac{10\times 40}{10}=40\).", r"Swapping \(y-x\) and \(x-z\)."),
    23: C(23, "Head Count of the First Part", r"The same balance, read from the part whose count is known.", r"\[ \frac{n(x-z)}{y-x} \]",
          [("Known part", r"n\ \text{at}\ z\ \text{lacks}\ n(x-z)"), ("Other part", r"b\ \text{at}\ y\ \text{gives}\ b(y-x)"), ("Balance", r"b = \frac{n(x-z)}{y-x}")],
          r"Check: \(b\) at \(y\) and \(n\) at \(z\) must average exactly \(x\). Add \(n\) when the whole group is asked.",
          "'average of the class is x, of the boys y, of the girls z; there are n girls; how many boys?'",
          r"Class \(12\), boys \(14\), girls \(9\), \(20\) girls: \(\frac{20\times 3}{2}=30\) boys.", r"Giving the number of boys when the whole class is asked."),
    24: C(24, "Mess Bill When Members Join", r"Write the new bill two ways: the old bill plus the rise, and the new members times the new share.",
          r"\[ N\times\frac{x(N+z)+y}{z} \]", [("Old", r"NA"), ("New", r"NA+y = (N+z)(A-x)"), ("Old share", r"A = \frac{x(N+z)+y}{z}")],
          r"The bill goes up although each share goes down, because more people share it.",
          "'There were N students; z more join, the expenses rise by Rs y a day while the average falls by Rs x; find the original expenditure.'",
          r"\(20\) students, \(5\) join, bill up Rs \(30\), share down Re \(1\): \(A=\frac{25+30}{5}=11\), bill Rs \(220\).", r"Giving the old share \(A\) instead of the bill \(NA\)."),
    25: C(25, "Average of the First n Natural Numbers", r"The numbers \(1\) to \(n\) are evenly spaced, so their average is the mean of the first and the last.",
          r"\[ \frac{n+1}{2} \]", [("Sum", r"\frac{n(n+1)}{2}"), ("Count", r"n"), ("Average", r"\frac{n+1}{2}")],
          r"Pair the first with the last, the second with the last but one: every pair makes \(n+1\).", "'Find the average of the first n natural numbers.'",
          r"\(1\) to \(9\): \(5\); \(1\) to \(10\): \(5.5\).", r"Writing \(\frac{n}{2}\)."),
    26: C(26, "Container Weighed With Its Contents", r"Counting the container as one more item, it must bring the new average for itself and the rise for every old item.",
          r"\[ a + r(n+1) \]", [("Before", r"na"), ("After", r"(n+1)(a+r)"), ("Container", r"a + r(n+1)")],
          r"Each of the \(n+1\) items, the container included, now stands \(r\) above the old average.",
          "'The average weight of n balls is a; with the bag included the average rises by r; find the weight of the bag.'",
          r"\(20\) balls at \(4\) g, rise \(0.5\) g: \(4+0.5\times 21=14.5\) g.", r"Multiplying \(r\) by \(n\) instead of \(n+1\)."),
    27: C(27, "Odd Count of Consecutive Numbers", r"For an odd count of evenly spaced numbers the average is the middle one.", r"\[ \text{average} = \text{middle number} \]",
          [("Numbers", r"m-k,\ \ldots,\ m,\ \ldots,\ m+k"), ("Pairs", r"(m-j)+(m+j) = 2m"), ("Average", r"m")],
          r"Numbers equally far below and above the middle cancel out. Works for consecutive, consecutive odd and consecutive even numbers.",
          "'Find the average of 7 (or any odd count of) consecutive numbers.'", r"\(15, 17, 19, 21, 23\): average \(19\).", r"Using it for an even count."),
    28: C(28, "Even Count of Consecutive Numbers", r"For an even count there are two middle numbers; the average is their mean.",
          r"\[ \frac{\text{two middle numbers}}{2} \]", [("Middle pair", r"a,\ b"), ("Average", r"\frac{a+b}{2}"), ("Shortcut", r"a+0.5\ \text{or}\ a+1")],
          r"Consecutive numbers: smaller middle \(+0.5\); consecutive odd or even: smaller middle \(+1\).", "'Find the average of 10 consecutive numbers ...'",
          r"\(31\) to \(36\): \(\frac{33+34}{2}=33.5\).", r"Picking one middle number."),
    29: C(29, "Average of Odd Numbers from 1 to n", r"The odd numbers \(1, 3, \ldots, n\) are evenly spaced.", r"\[ \frac{n+1}{2} \]",
          [("Count", r"\frac{n+1}{2}"), ("Sum", r"\left(\frac{n+1}{2}\right)^{2}"), ("Average", r"\frac{n+1}{2}")],
          r"Mean of the first and last odd numbers: \(\frac{1+n}{2}\).", "'What is the average of the odd numbers from 1 to n?'",
          r"\(1\) to \(21\): \(11\).", r"Using \(\frac{n}{2}\)."),
    30: C(30, "Average of Even Numbers from 2 to n", r"The even numbers \(2, 4, \ldots, n\) are evenly spaced.", r"\[ \frac{n+2}{2} \]",
          [("Count", r"\frac{n}{2}"), ("Sum", r"\frac{n}{2}\left(\frac{n}{2}+1\right)"), ("Average", r"\frac{n+2}{2}")],
          r"Mean of the first and last even numbers: \(\frac{2+n}{2}\).", "'What is the average of the even numbers from 1 to n?'",
          r"\(2\) to \(40\): \(21\).", r"Using \(\frac{n+1}{2}\)."),
}
OLD = {   # row: (rule, question, builder, unit)
    511: (18, "A bus goes from a town to a city at 36 km/hr and comes back by the same road at 45 km/hr. What is its average speed for the round trip?",
          lambda: r18(36, 45), KMH),
    512: (19, "A trip is split into three equal stretches, which are driven at 60 km/hr, 45 km/hr and 36 km/hr. Find the average speed for the whole trip.",
          lambda: r19(60, 45, 36), KMH),
    513: (20, "A man walks 10 km at 5 km/hr, cycles 21 km at 7 km/hr and then rides 32 km at 8 km/hr. Find his average speed over the whole distance.",
          lambda: r20([(10, 5), (21, 7), (32, 8)]), KMH),
    515: (21, r"A girl walks the first \(\frac{1}{4}\) of a path at 3 km/hr, the next \(\frac{1}{2}\) at 4 km/hr and the rest at 6 km/hr. What is her average speed?",
          lambda: r21([(F(1, 4), 3), (F(1, 2), 4), (F(1, 4), 6)]), KMH),
    514: (22, "In a factory the average daily wage of all the workers is Rs 150. The 12 supervisors get Rs 420 a day on average and the other workers get Rs 130. "
              "How many other workers are there?", lambda: r22(150, 12, 420, 130), ""),
    516: (24, "A hostel had 30 students. When 6 more joined, the daily mess bill went up by Rs 54, but the average cost for each student fell by Rs 2. "
              "What was the daily mess bill at first?", lambda: r24(30, 6, 54, 2), "Rs"),
    517: (25, "What is the mean of all the whole numbers from 1 to 85?", lambda: r25(85), ""),
    518: (26, "The average weight of 60 marbles is 8 g. When the box holding them is counted in as one more item, the average weight goes up by 0.2 g. How heavy is the box?",
          lambda: r26(60, 8, F("0.2"), "g"), "g"),
}
NEW = {   # rule: [(key, question, builder, unit, wrong options or None)]
    18: [("r18_e1", "A woman drives from her home to her office at 50 km/hr and drives back the same way at 75 km/hr. Find her average speed for the whole journey.",
          lambda: r18(50, 75), KMH, None),
         ("r18_e2", "A man cycles to a village at 14 km/hr and returns by the same path at 21 km/hr. Find his average speed for the trip there and back.",
          lambda: r18(14, 21), KMH, None),
         ("r18_e3", "A boat goes up a river to a jetty at 6 km/hr and comes back down at 10 km/hr. What is its average speed for the whole trip?", lambda: r18(6, 10), KMH, None),
         ("r18_e4", "Rita walks half of a trip at 4 km/hr and the other half at 6 km/hr. What is her average speed for the whole trip?", lambda: r18(4, 6), KMH, None),
         ("r18_e5", "A runner covers the first half of a race at 18 km/hr and the second half at 9 km/hr. What is the runner's average speed over the race?",
          lambda: r18(18, 9), KMH, None)],
    19: [("r19_e1", "A delivery van covers three equal parts of a route at 18 km/hr, 12 km/hr and 9 km/hr. What is its average speed for the whole route?",
          lambda: r19(18, 12, 9), KMH, None),
         ("r19_e2", "A walker splits a hike into three equal parts and covers them at 3 km/hr, 5 km/hr and 6 km/hr. Find the average speed for the hike.",
          lambda: r19(3, 5, 6), KMH, None),
         ("r19_e3", "A car runs over three equal sections of a road at 24 km/hr, 40 km/hr and 60 km/hr. Find its average speed over the road.", lambda: r19(24, 40, 60), KMH, None),
         ("r19_e4", "A cyclist rides the first km at 21 km/hr, the second km at 15 km/hr and the third km at 10 km/hr. What is the average speed over the 3 km?",
          lambda: r19(21, 15, 10), KMH, None)],
    20: [("r20_e1", "A man covers 14 km at 7 km/hr, 30 km at 10 km/hr and 20 km at 5 km/hr. What is his average speed for the whole distance?",
          lambda: r20([(14, 7), (30, 10), (20, 5)]), KMH, None),
         ("r20_e2", "A lorry runs 8 km at 4 km/hr through a market, 27 km at 9 km/hr on a hill road and 45 km at 15 km/hr on the plain. Find its average speed.",
          lambda: r20([(8, 4), (27, 9), (45, 15)]), KMH, None),
         ("r20_e3", "A woman rows 22 km at 11 km/hr, walks 36 km at 12 km/hr and rides 26 km at 13 km/hr. Find her average speed for the whole distance.",
          lambda: r20([(22, 11), (36, 12), (26, 13)]), KMH, None)],
    21: [("r21_e1", r"A man covers each \(\frac{1}{3}\) of a distance at a different speed: 14 km/hr, 10 km/hr and 7 km/hr. Find his average speed.",
          lambda: r21([(F(1, 3), 14), (F(1, 3), 10), (F(1, 3), 7)]), KMH, None),
         ("r21_e2", r"A girl cycles the first \(\frac{2}{5}\) of a road at 4 km/hr, the next \(\frac{2}{5}\) at 28 km/hr and the rest at 7 km/hr. Find her average speed.",
          lambda: r21([(F(2, 5), 4), (F(2, 5), 28), (F(1, 5), 7)]), KMH, None),
         ("r21_e3", "A man covers 30% of a distance at 6 km/hr, the next 50% at 10 km/hr and the remaining distance at 4 km/hr. Find his average speed.",
          lambda: r21([(F(30, 100), 6), (F(50, 100), 10), (F(20, 100), 4)]), KMH, None),
         ("r21_e4", "A train runs 40% of a journey at 20 km/hr, the next 40% at 16 km/hr and the rest at 10 km/hr. What is its average speed for the journey?",
          lambda: r21([(F(40, 100), 20), (F(40, 100), 16), (F(20, 100), 10)]), KMH, None),
         ("r21_e5", "On a trip through a city, a taxi keeps 40 km/hr for 50% of the distance, 30 km/hr for 30% and 20 km/hr for the rest. Find its average speed.",
          lambda: r21([(F(50, 100), 40), (F(30, 100), 30), (F(20, 100), 20)]), KMH, None)],
    22: [("r22_e1", "In a bank the average monthly pay of all the staff is Rs 240. The 20 managers get Rs 600 on average and the other staff get Rs 210. How many other staff are there?",
          lambda: r22(240, 20, 600, 210), "", None),
         ("r22_e2", "The average pay of all the teachers of a school is Rs 175. The 18 senior teachers average Rs 455 and the others Rs 147. How many other teachers are there?",
          lambda: r22(175, 18, 455, 147), "", None),
         ("r22_e3", "The average salary in an office is Rs 310. The 21 officers average Rs 730 and the clerks average Rs 280. How many clerks are there?",
          lambda: r22(310, 21, 730, 280), "", None),
         ("r22_e4", "In a shop the average wage of all the workers is Rs 260. The 28 skilled workers average Rs 380 and the rest Rs 245. How many other workers are there?",
          lambda: r22(260, 28, 380, 245), "", None),
         ("r22_e5", "The average daily earning of all the drivers of a firm is Rs 190. The 15 senior drivers average Rs 500 and the others Rs 140. How many other drivers are there?",
          lambda: r22(190, 15, 500, 140), "", None)],
    23: [("r23_ex", "The average age of a class is 17 years. The boys average 19 years and the girls 14 years. If there are 24 girls, how many boys are there?",
          lambda: r23(17, 19, 14, 24), "", None),
         ("r23_e1", "The average age of the members of a club is 15 years. The boys average 20 years and the girls 11 years. There are 15 girls. How many boys are there?",
          lambda: r23(15, 20, 11, 15), "", None),
         ("r23_e2", "In a hall the average age is 32 years. The men average 35 years and the women 26 years. If there are 22 women, how many men are there?",
          lambda: r23(32, 35, 26, 22), "", None),
         ("r23_e3", "The average age of a team is 13 years. The boys average 15 years and the girls 10 years. If 14 of them are girls, how many are boys?",
          lambda: r23(13, 15, 10, 14), "", None),
         ("r23_e4", "The average weight of a group is 40 kg. The boys average 43 kg and the girls 35 kg. With 18 girls in the group, how many boys are there?",
          lambda: r23(40, 43, 35, 18), "", None),
         ("r23_e5", "The average age of a class is 10 years. The boys average 12 years and the girls 7 years. If there are 24 girls, how many students are there in all?",
          lambda: r23(10, 12, 7, 24, total=True), "", None)],
    24: [("r24_e1", "A hostel has 50 students. When 10 more join, the daily mess bill rises by Rs 80 but the average cost a head falls by Rs 3. Find the original daily bill.",
          lambda: r24(50, 10, 80, 3), "Rs", None),
         ("r24_e2", "A camp has 24 members. When 8 more come, the daily food bill goes up by Rs 40, while each person's share goes down by Re 1. What was the daily bill at first?",
          lambda: r24(24, 8, 40, 1), "Rs", None),
         ("r24_e3", "There were 28 boys in a hostel. After 7 more boys came, the mess bill rose by Rs 31.5 a day but the cost per boy fell by Rs 1.5. Find the original bill.",
          lambda: r24(28, 7, F("31.5"), F("1.5")), "Rs", None),
         ("r24_e4", "A mess fed 45 workers. When 4 more workers joined, the bill went up by Rs 27 a day and the cost per worker came down by Re 1. Find the original daily bill.",
          lambda: r24(45, 4, 27, 1), "Rs", None)],
    25: [("r25_e1", "Add the natural numbers from 1 up to 74 and divide by how many there are. What is the result?", lambda: r25(74), "", None),
         ("r25_e2", "What is the average of the first 47 counting numbers?", lambda: r25(47), "", None),
         ("r25_e3", "Find the mean of the natural numbers 1 to 119.", lambda: r25(119), "", None),
         ("r25_e4", "The numbers 1 to 150 are written on cards. What is the average of the numbers on the cards?", lambda: r25(150), "", None)],
    26: [("r26_e1", "25 apples have an average weight of 150 g. When the crate is weighed in as one more item, the average goes up by 4 g. What does the crate weigh?",
          lambda: r26(25, 150, 4, "g"), "g", None),
         ("r26_e2", "45 eggs weigh 50 g each on average. If the tray is counted as one more item, the average weight rises by 1 g. Find the weight of the tray.",
          lambda: r26(45, 50, 1, "g"), "g", None),
         ("r26_e3", "The average weight of 36 books is 400 g. When the carton is counted in with them, the average weight goes up by 10 g. How heavy is the carton?",
          lambda: r26(36, 400, 10, "g"), "g", None)],
    27: [("r27_e1", "What is the mean of these numbers: 114, 115, 116, 117, 118, 119, 120, 121, 122?", lambda: r27(114, 122, 1), "", None),
         ("r27_e2", "Find the average of the consecutive numbers 243, 244, 245, 246, 247, 248, 249.", lambda: r27(243, 249, 1), "", None),
         ("r27_e3", "Find the average of the odd numbers 157, 159, 161, 163, 165, 167, 169.", lambda: r27(157, 169, 2), "", None),
         ("r27_e4", r"Find the average of the 11 consecutive odd numbers 301, 303, 305, \(\ldots\), 321.", lambda: r27(301, 321, 2), "", None),
         ("r27_e5", r"Find the average of the 13 consecutive even numbers 218, 220, 222, \(\ldots\), 242.", lambda: r27(218, 242, 2), "", None)],
    28: [("r28_e1", r"Find the average of the 10 consecutive numbers 116, 117, 118, \(\ldots\), 125.", lambda: r28(116, 125, 1), "", None),
         ("r28_e2", r"Find the average of the 12 consecutive numbers 241, 242, 243, \(\ldots\), 252.", lambda: r28(241, 252, 1), "", None),
         ("r28_e3", "Six numbers follow one after another, from 163 to 168. What is their mean?", lambda: r28(163, 168, 1), "", None),
         ("r28_e4", "Find the average of the odd numbers 121, 123, 125, 127, 129 and 131.", lambda: r28(121, 131, 2), "", None),
         ("r28_e5", "Find the average of the odd numbers 255, 257, 259, 261, 263, 265, 267, 269.", lambda: r28(255, 269, 2), "", None),
         ("r28_e6", "Find the average of the odd numbers 401, 403, 405, 407, 409, 411, 413, 415.", lambda: r28(401, 415, 2), "", None),
         ("r28_e7", "Find the average of the even numbers 134, 136, 138, 140, 142 and 144.", lambda: r28(134, 144, 2), "", None),
         ("r28_e8", "Find the average of the even numbers 170, 172, 174, 176, 178, 180, 182, 184.", lambda: r28(170, 184, 2), "", None)],
    29: [("r29_ex", "What is the mean of the odd numbers from 1 up to 45?", lambda: r29(45), "", None),
         ("r29_e1", "Find the mean of all the odd numbers between 1 and 57, both included.", lambda: r29(57), "", None),
         ("r29_e2", "All the odd numbers from 1 to 99 are added and the sum is divided by how many there are. What is the answer?", lambda: r29(99), "", None),
         ("r29_e3", "What is the average of every odd number from 1 up to 121?", lambda: r29(121), "", None),
         ("r29_e4", "Find the average of the odd numbers lying from 1 to 67.", lambda: r29(67), "", None)],
    30: [("r30_ex", "What is the mean of the even numbers from 2 up to 64?", lambda: r30(64), "", None),
         ("r30_e1", "Find the mean of all the even numbers between 1 and 36, both ends counted.", lambda: r30(36), "", None),
         ("r30_e2", "All the even numbers from 1 to 100 are added and the sum is divided by how many there are. What is the answer?", lambda: r30(100), "", None),
         ("r30_e3", "What is the average of every even number from 1 up to 58?", lambda: r30(58), "", None),
         ("r30_e4", "Find the average of the even numbers lying from 1 to 84.", lambda: r30(84), "", None)],
}


def main(old=OLD, new=NEW, cards=CARDS, rules=range(18, 31)):
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
                _, q, fn, unit = old[rid]
                g = fn()
                op, _ = ops(g["answer"][1], unit)
                extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
                extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
                out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
            json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cc = {"rule_name": f"Rule {rule}", "rule_html": cards[rule]}
        json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, unit, wrong in new[rule]:
            g = fn()
            op, pos = ops(g["answer"][1], unit, wrong)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        json.dump({"rules_html": [{"chapter": "average", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(ids)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
