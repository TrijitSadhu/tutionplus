"""Average Rules 31-43 (2026-10-30). 31 / 32: squares / cubes of 1 to n - (n + 1)(2n + 1)/6, n(n + 1)^2/4. 33 / 34: first n even / odd
numbers - n + 1, n. 35: squares of the first n even numbers - 2(n + 1)(2n + 1)/3. 36 / 37: squares of the even / odd numbers up to n -
(n + 1)(n + 2)/3, n(n + 2)/3. 38: numbers read wrongly - A + (right - wrong)/n. 39 / 40: geometric / harmonic mean. 41: a series with
common difference 2 - (first + last)/2. 42: overlapping averages differ by x - the two odd ones out differ by (count) x. 43: n
consecutive odd (or even) numbers - largest - smallest = 2(n - 1). Writes the cards, regenerates the old rows 519-526 (525's key was
on the empty option e) and adds the book's examples / exercises with no copy. Book slips: Rule 36 Exr 4 (35 -> 420, not 408),
Rule 40 Exr 3 (5040/319, not 5040/299), Rule 41 Exr (i) leaves 34 out of its series, Rule 43 says "consecutive numbers" where its
formula needs consecutive odd (or even) numbers - the new questions say so. Usage: python gen_31_43.py"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps, tex  # noqa: E402
from gen_6_11 import UU, nf  # noqa: E402
from gen_18_30 import listing, main, money_s  # noqa: E402
from helpers import result  # noqa: E402


def th(statement, formula):
    return statement + "<br>" + formula


TH = {
    31: th(r"The average of the squares of the natural numbers \(1\) to \(n\) is", r"\[ \frac{(n+1)(2n+1)}{6} \]"),
    32: th(r"The average of the cubes of the natural numbers \(1\) to \(n\) is", r"\[ \frac{n(n+1)^{2}}{4} \]"),
    33: th(r"The average of the first \(n\) even numbers \(2, 4, \ldots, 2n\) is", r"\[ n+1 \]"),
    34: th(r"The average of the first \(n\) odd numbers \(1, 3, \ldots, 2n-1\) is", r"\[ n \]"),
    35: th(r"The average of the squares of the first \(n\) even numbers is", r"\[ \frac{2(n+1)(2n+1)}{3} \]"),
    36: th(r"The average of the squares of the even numbers \(2, 4, \ldots, n\) (\(n\) the last even number) is", r"\[ \frac{(n+1)(n+2)}{3} \]"),
    37: th(r"The average of the squares of the odd numbers \(1, 3, \ldots, n\) (\(n\) the last odd number) is", r"\[ \frac{n(n+2)}{3} \]"),
    38: th(r"If the average of \(n\) numbers was found to be \(A\) with some numbers read wrongly, the correct average is",
           r"\[ A + \frac{(\text{sum of correct numbers}) - (\text{sum of wrong numbers})}{n} \]"),
    39: th(r"The geometric mean of \(n\) numbers \(x_1, x_2, \ldots, x_n\) is", r"\[ \sqrt[n]{x_1\times x_2\times \cdots\times x_n} \]"),
    40: th(r"The harmonic mean of \(n\) numbers \(x_1, x_2, \ldots, x_n\) is", r"\[ \frac{n}{\frac{1}{x_1}+\frac{1}{x_2}+\cdots+\frac{1}{x_n}} \]"),
    41: th(r"The average of a series with common difference \(2\) (or any common difference) is", r"\[ \frac{\text{first term}+\text{last term}}{2} \]"),
    42: th(r"If the average of the first and second of three numbers is \(x\) more (or less) than the average of the second and third, the first and "
           r"third differ by \(2x\); with groups of \(k\) items that share all but one, the odd ones out differ by", r"\[ kx \]"),
    43: th(r"If \(n\) consecutive odd (or even) numbers have any average, the difference between the largest and the smallest is", r"\[ 2(n-1) \]"),
}


def R(rule, v, trad, rb, sub, unit=""):
    rule_steps = steps(("Identify the values.", rb), ("Apply the specified rule.", TH[rule].split("<br>")[1]), ("Substitute the values.", sub))
    fin = money_s(v) if unit == "Rs" else UU(v, unit)
    return result(("number", F(v)), TH[rule], trad, rule_steps, fin, [rb, rf"Answer \(= {nf(v)}\)."], sub)


def powers(rule, xs, p, rb, sub_expr):
    """the average of x^p over the list xs, added up term by term."""
    terms = [x ** p for x in xs]
    v = F(sum(terms), len(terms))
    shown = listing(terms)
    trad = steps(("Write the terms.", rf"{shown} - that is \({len(terms)}\) terms."), ("Add them.", rf"Sum \(= {sum(terms)}\)."),
                 ("Average.", rf"\[ {sum(terms)} \div {len(terms)} = {nf(v)} \]"))
    return R(rule, v, trad, rb, rf"\[ {sub_expr} = {nf(v)} \]")


def r31(n):
    return powers(31, range(1, n + 1), 2, rf"\(n = {n}\).", rf"\frac{{({n}+1)(2\times {n}+1)}}{{6}} = \frac{{{n + 1}\times {2 * n + 1}}}{{6}}")


def r32(n):
    return powers(32, range(1, n + 1), 3, rf"\(n = {n}\).", rf"\frac{{{n}({n}+1)^{{2}}}}{{4}} = \frac{{{n}\times {(n + 1) ** 2}}}{{4}}")


def r33(n):
    return powers(33, range(2, 2 * n + 1, 2), 1, rf"\(n = {n}\) even numbers, \(2\) to \({2 * n}\).", rf"{n}+1")


def r34(n):
    return powers(34, range(1, 2 * n, 2), 1, rf"\(n = {n}\) odd numbers, \(1\) to \({2 * n - 1}\).", rf"n = {n}")


def r35(n):
    return powers(35, range(2, 2 * n + 1, 2), 2, rf"\(n = {n}\) even numbers, \(2\) to \({2 * n}\).",
                  rf"\frac{{2({n}+1)(2\times {n}+1)}}{{3}} = \frac{{2\times {n + 1}\times {2 * n + 1}}}{{3}}")


def r36(n):
    return powers(36, range(2, n + 1, 2), 2, rf"Last even number \(n = {n}\).", rf"\frac{{({n}+1)({n}+2)}}{{3}} = \frac{{{n + 1}\times {n + 2}}}{{3}}")


def r37(n):
    return powers(37, range(1, n + 1, 2), 2, rf"Last odd number \(n = {n}\).", rf"\frac{{{n}({n}+2)}}{{3}} = \frac{{{n}\times {n + 2}}}{{3}}")


def r38(n, A, wrong, right, unit=""):
    n, A = F(n), F(A)
    w, c = sum(map(F, wrong)), sum(map(F, right))
    v = A + (c - w) / n
    trad = steps(("Total as worked out.", rf"\[ {tex(n)}\times {nf(A)} = {nf(n * A)} \]"),
                 ("Put the right numbers in.", rf"Take out \({' + '.join(nf(t) for t in wrong)} = {nf(w)}\), put in \({' + '.join(nf(t) for t in right)} = {nf(c)}\): "
                                               rf"\[ {nf(n * A)} - {nf(w)} + {nf(c)} = {nf(n * A - w + c)} \]"),
                 ("Correct average.", rf"\[ {nf(n * A - w + c)} \div {tex(n)} = {nf(v)} \]"))
    sub = rf"\[ {nf(A)} + \frac{{{nf(c)} - {nf(w)}}}{{{tex(n)}}} = {nf(A)} {'+' if c >= w else '-'} {nf(abs(c - w) / n)} = {nf(v)} \]"
    return R(38, v, trad, rf"\(n = {tex(n)}\), \(A = {nf(A)}\), correct \(= {nf(c)}\), wrong \(= {nf(w)}\).", sub, unit)


TIMES = " " + chr(92) + "times "


def r39(xs):
    P = 1
    for x in xs:
        P *= x
    k = len(xs)
    g = round(P ** (1 / k))
    assert g ** k == P
    prod = TIMES.join(map(str, xs))
    trad = steps(("Multiply.", rf"\[ {prod} = {P} \]"),
                 ("Find the number whose power gives the product.", rf"\[ {TIMES.join([str(g)] * k)} = {P} \]so the {'cube' if k == 3 else str(k) + 'th'} root is \({g}\)."))
    root = "" if k == 2 else str(k)
    sub = rf"\[ \sqrt[{root}]{{{prod}}} = \sqrt[{root}]{{{P}}} = {g} \]"
    return R(39, g, trad, rf"\(n = {k}\), numbers " + ", ".join(rf"\({x}\)" for x in xs) + ".", sub)


def r40(xs):
    k = len(xs)
    S = sum(F(1, x) for x in xs)
    v = k / S
    trad = steps(("Reciprocals.", ", ".join(rf"\(\frac{{1}}{{{x}}}\)" for x in xs) + rf"; their sum is \({tex(S) if S.denominator == 1 else chr(92) + 'frac{' + str(S.numerator) + '}{' + str(S.denominator) + '}'}\)."),
                 ("Harmonic mean.", rf"The number of terms over that sum: \[ {k} \div \frac{{{S.numerator}}}{{{S.denominator}}} = \frac{{{k * S.denominator}}}{{{S.numerator}}} = {nf(v)} \]"))
    sub = rf"\[ \frac{{{k}}}{{{'+'.join(chr(92) + 'frac{1}{' + str(x) + '}' for x in xs)}}} = {nf(v)} \]"
    return R(40, v, trad, rf"\(n = {k}\), numbers " + ", ".join(rf"\({x}\)" for x in xs) + ".", sub)


def r41(first, last, step=2):
    xs = list(range(first, last + 1, step))
    v = F(sum(xs), len(xs))
    trad = steps(("Add them.", rf"{listing(xs)}: sum \(= {sum(xs)}\), count \(= {len(xs)}\)."), ("Average.", rf"\[ {sum(xs)} \div {len(xs)} = {nf(v)} \]"))
    return R(41, v, trad, rf"First term \({first}\), last term \({last}\).", rf"\[ \frac{{{first}+{last}}}{{2}} = {nf(v)} \]")


def r42(k, x, unit=""):
    """two groups of k items share k - 1 of them; their averages differ by x -> the odd ones out differ by kx."""
    k, x = F(k), F(x)
    v = k * x
    trad = steps(("Totals.", rf"Each group has \({tex(k)}\) items, so its total is \({tex(k)}\) times its average; the totals differ by \({tex(k)}\times {nf(x)} = {nf(v)}\)."),
                 ("Cancel the shared items.", rf"The shared items are in both totals, so the whole difference \({nf(v)}\) is between the two items that are not shared."))
    return R(42, v, trad, rf"Items in each average \(= {tex(k)}\), difference of averages \(x = {nf(x)}\).", rf"\[ {tex(k)}\times {nf(x)} = {nf(v)} \]", unit)


def r42_temp(a1, a2, thu):
    """Mon-Wed average a1, Tue-Thu average a2, Thursday given -> Monday."""
    a1, a2, thu = map(F, (a1, a2, thu))
    d = 3 * (a2 - a1)
    v = thu - d
    trad = steps(("Totals.", rf"Mon + Tue + Wed \(= 3\times {nf(a1)} = {nf(3 * a1)}\); Tue + Wed + Thu \(= 3\times {nf(a2)} = {nf(3 * a2)}\)."),
                 ("Take one from the other.", rf"Thu \(-\) Mon \(= {nf(3 * a2)} - {nf(3 * a1)} = {nf(d)}\), so Mon \(= {nf(thu)} - {nf(d)} = {nf(v)}\)."))
    sub = rf"Thu \(-\) Mon \(= 3\times ({nf(a2)}-{nf(a1)}) = {nf(d)}\); Mon \(= {nf(thu)} - {nf(d)} = {nf(v)}\)."
    return R(42, v, trad, rf"Three days in each average, \(x = {nf(a2 - a1)}\), Thursday \(= {nf(thu)}\).", sub, "°C")


def r42_ratio(a1, a2, frac):
    """Mon-Wed average a1, Tue-Thu average a2, Thursday = frac of Monday -> Thursday."""
    a1, a2, frac = map(F, (a1, a2, frac))
    d = 3 * (a1 - a2)                                  # Mon - Thu
    mon = d / (1 - frac)
    v = frac * mon
    fr = rf"\frac{{{frac.numerator}}}{{{frac.denominator}}}"
    trad = steps(("Totals.", rf"Mon + Tue + Wed \(= {nf(3 * a1)}\); Tue + Wed + Thu \(= {nf(3 * a2)}\), so Mon \(-\) Thu \(= {nf(d)}\)."),
                 ("Use the link.", rf"Thu \(= {fr}\) Mon, so Mon \(- {fr}\) Mon \(= {nf(d)}\): Mon \(= {nf(mon)}\), Thu \(= {nf(v)}\)."))
    sub = rf"Mon \(-\) Thu \(= 3\times ({nf(a1)}-{nf(a2)}) = {nf(d)}\); with Thu \(= {fr}\) Mon: Mon \(= {nf(mon)}\), Thu \(= {nf(v)}\)."
    return R(42, v, trad, rf"Three days in each average, \(x = {nf(a1 - a2)}\), Thu \(= {fr}\) Mon.", sub, "°C")


def r43(n, avg):
    n, avg = int(n), F(avg)
    lo = avg - (n - 1)
    xs = [lo + 2 * i for i in range(n)]
    v = xs[-1] - xs[0]
    trad = steps(("Write the numbers.", rf"\({n}\) numbers \(2\) apart averaging \({nf(avg)}\): \({nf(xs[0])}, {nf(xs[1])}, \ldots, {nf(xs[-1])}\)."),
                 ("Difference.", rf"\[ {nf(xs[-1])} - {nf(xs[0])} = {nf(v)} \]"))
    return R(43, v, trad, rf"\(n = {n}\).", rf"\[ 2({n}-1) = {nf(v)} \]")


C = card
CARDS = {
    31: C(31, "Average of Squares 1 to n", r"Sum of the squares over the count.", r"\[ \frac{(n+1)(2n+1)}{6} \]",
          [("Sum", r"\frac{n(n+1)(2n+1)}{6}"), ("Count", r"n"), ("Average", r"\frac{(n+1)(2n+1)}{6}")],
          r"Dividing the known sum of squares by \(n\) leaves \(\frac{(n+1)(2n+1)}{6}\).", "'Find the average of the squares of the natural numbers from 1 to n.'",
          r"\(1\) to \(5\): \(\frac{6\times 11}{6}=11\).", r"Squaring the average \(\frac{n+1}{2}\) instead."),
    32: C(32, "Average of Cubes 1 to n", r"Sum of the cubes over the count.", r"\[ \frac{n(n+1)^{2}}{4} \]",
          [("Sum", r"\left(\frac{n(n+1)}{2}\right)^{2}"), ("Count", r"n"), ("Average", r"\frac{n(n+1)^{2}}{4}")],
          r"The sum of the first \(n\) cubes is the square of the sum of the first \(n\) numbers.", "'Find the average of the cubes of the natural numbers till n.'",
          r"\(1\) to \(4\): \(\frac{4\times 25}{4}=25\).", r"Dividing by \(2\) instead of \(4\)."),
    33: C(33, "Average of the First n Even Numbers", r"\(2, 4, \ldots, 2n\) average to the mean of the first and last.", r"\[ n+1 \]",
          [("First", r"2"), ("Last", r"2n"), ("Average", r"\frac{2+2n}{2} = n+1")], r"Sum \(= n(n+1)\), count \(= n\).",
          "'Find the average of the first n even numbers.'", r"First \(30\) even numbers: \(31\).", r"Answering \(n\) (that is the odd-number case)."),
    34: C(34, "Average of the First n Odd Numbers", r"\(1, 3, \ldots, 2n-1\) average to the mean of the first and last.", r"\[ n \]",
          [("First", r"1"), ("Last", r"2n-1"), ("Average", r"\frac{1+2n-1}{2} = n")], r"Sum \(= n^{2}\), count \(= n\).",
          "'Find the average of the first n odd numbers.'", r"First \(30\) odd numbers: \(30\).", r"Answering \(n+1\)."),
    35: C(35, "Average of Squares of the First n Even Numbers", r"Each even square is \(4\) times a square.", r"\[ \frac{2(n+1)(2n+1)}{3} \]",
          [("Terms", r"(2k)^{2} = 4k^{2}"), ("Sum", r"4\times\frac{n(n+1)(2n+1)}{6}"), ("Average", r"\frac{2(n+1)(2n+1)}{3}")],
          r"Four times the average of the squares \(1\) to \(n\).", "'Find the average of the squares of the first n even numbers.'",
          r"First \(4\) even numbers: \(\frac{2\times 5\times 9}{3}=30\).", r"Putting the last even number \(2n\) in place of \(n\)."),
    36: C(36, "Average of Squares of Even Numbers up to n", r"Here \(n\) is the last even number (from \(1\) to \(n\), use the largest even number).",
          r"\[ \frac{(n+1)(n+2)}{3} \]", [("Count", r"\frac{n}{2}"), ("Same as", r"\text{Rule 35 with } \frac{n}{2}"), ("Average", r"\frac{(n+1)(n+2)}{3}")],
          r"With \(m = \frac{n}{2}\) even numbers, Rule 35 gives \(\frac{2(m+1)(2m+1)}{3} = \frac{(n+2)(n+1)}{3}\).",
          "'Find the average of the squares of the even numbers from 1 to n.'", r"Up to \(8\): \(\frac{9\times 10}{3}=30\).", r"Using an odd end such as \(11\) as \(n\)."),
    37: C(37, "Average of Squares of Odd Numbers up to n", r"Here \(n\) is the last odd number.", r"\[ \frac{n(n+2)}{3} \]",
          [("Count", r"\frac{n+1}{2}"), ("Sum", r"\frac{n(n+1)(n+2)}{6}"), ("Average", r"\frac{n(n+2)}{3}")],
          r"From \(1\) to an even end, use the largest odd number below it.", "'Find the average of the squares of the odd numbers from 1 to n.'",
          r"Up to \(7\): \(\frac{7\times 9}{3}=21\).", r"Using an even end such as \(20\) as \(n\)."),
    38: C(38, "Correcting a Wrong Average", r"Fix the total, then share it again.", r"\[ A + \frac{\text{correct} - \text{wrong}}{n} \]",
          [("Wrong total", r"nA"), ("Fixed total", r"nA - \text{wrong} + \text{correct}"), ("Correct average", r"A + \frac{\text{correct}-\text{wrong}}{n}")],
          r"Only the misread numbers change the total; the average moves by that change shared over all \(n\).",
          "'The average was found to be A, but a number x was read as y; find the correct average.'",
          r"\(10\) numbers average \(40\); \(36\) read as \(63\): \(40-\frac{27}{10}=37.3\).", r"Dividing the error by \(n-1\)."),
    39: C(39, "Geometric Mean", r"The \(n\)th root of the product - used for growth rates and ratios.", r"\[ \sqrt[n]{x_1x_2\cdots x_n} \]",
          [("Product", r"x_1x_2\cdots x_n"), ("Root", r"n\text{th root}"), ("GM", r"\sqrt[n]{\text{product}}")],
          r"For numbers in a constant ratio the geometric mean is the middle one.", "'Find the geometric mean of a, b and c.'",
          r"\(2, 6, 18\): \(\sqrt[3]{216}=6\).", r"Taking the square root of a product of three numbers."),
    40: C(40, "Harmonic Mean", r"The count divided by the sum of the reciprocals - used for average speeds over equal distances.",
          r"\[ \frac{n}{\frac{1}{x_1}+\cdots+\frac{1}{x_n}} \]", [("Reciprocals", r"\frac{1}{x_i}"), ("Their sum", r"\sum\frac{1}{x_i}"), ("HM", r"\frac{n}{\sum 1/x_i}")],
          r"It is never more than the geometric mean, which is never more than the ordinary average.", "'Find the harmonic mean of a, b, c and d.'",
          r"\(3, 6\): \(\frac{2}{\frac{1}{3}+\frac{1}{6}}=4\).", r"Forgetting the \(n\) on top."),
    41: C(41, "Average of an Evenly Spaced Series", r"Equal steps: the average is the mean of the first and last terms.", r"\[ \frac{\text{first}+\text{last}}{2} \]",
          [("Pairs", r"\text{first}+\text{last} = \text{second}+\text{last but one}"), ("Count", r"\text{any}"), ("Average", r"\frac{\text{first}+\text{last}}{2}")],
          r"Works for a difference of \(2\) (odd or even numbers) and for any other common difference (see Rules 27 and 28).",
          "'Find the average of the series a, a+2, ..., l.'", r"\(15, 17, \ldots, 35\): \(25\).", r"Using a term in the middle of an even count."),
    42: C(42, "Overlapping Averages", r"When two groups share all but one item each, only the unshared items make the difference.", r"\[ kx \]",
          [("Group 1", r"a+(\text{shared})"), ("Group 2", r"c+(\text{shared})"), ("Difference", r"a-c = kx")],
          r"Averages over \(k\) items differ by \(x\), so the totals differ by \(kx\), and the shared items cancel.",
          "'The average of the first and second of three numbers is x more than that of the second and third' / temperatures of Mon-Wed and Tue-Thu.",
          r"Averages of \(4\) subjects differ by \(5\): the odd ones out differ by \(20\).", r"Answering \(x\) instead of \(kx\)."),
    43: C(43, "Spread of Consecutive Odd or Even Numbers", r"Numbers \(2\) apart: \(n\) of them span \(n-1\) steps.", r"\[ 2(n-1) \]",
          [("Steps", r"n-1"), ("Each step", r"2"), ("Largest - smallest", r"2(n-1)")],
          r"The average does not matter - only the count. For numbers \(1\) apart the spread would be \(n-1\).",
          "'The average of n consecutive odd numbers is x; find the difference between the largest and the smallest.'",
          r"\(6\) consecutive even numbers: \(10\).", r"Using \(2n\) instead of \(2(n-1)\)."),
}
OLD = {   # row: (rule, question, builder, unit)
    519: (32, "What is the mean of the cubes of the whole numbers from 1 to 9?", lambda: r32(9), ""),
    520: (33, "Take the first 75 even natural numbers. What is their mean?", lambda: r33(75), ""),
    521: (34, "Take the first 25 odd natural numbers 1, 3, 5, and so on. What is their mean?", lambda: r34(25), ""),
    522: (35, "What is the mean of the squares of the first 8 even natural numbers?", lambda: r35(8), ""),
    523: (38, "The average of 6 numbers was worked out as 32, but one number, 27, had been copied as 72. What is the correct average?",
          lambda: r38(6, 32, [72], [27]), ""),
    524: (40, "Three numbers are 21, 28 and 84. What is their harmonic mean?", lambda: r40([21, 28, 84]), ""),
    525: (41, "Find the mean of the odd numbers 141, 143, 145, 147, 149, 151.", lambda: r41(141, 151), ""),
    526: (43, "The average of 9 consecutive odd numbers is 37. What is the difference between the largest and the smallest of them?", lambda: r43(9, 37), ""),
}
NEW = {   # rule: [(key, question, builder, unit, wrong options or None)]
    31: [("r31_ex", "What is the mean of the squares of the whole numbers from 1 to 11?", lambda: r31(11), "", None),
         ("r31_e1", r"Work out the mean of the thirteen squares \(1^{2}\) up to \(13^{2}\).", lambda: r31(13), "", None),
         ("r31_e2", "The squares of the numbers 1 to 17 are written down. What is their average?", lambda: r31(17), "", None),
         ("r31_e3", "What is the mean of the squares of the first 25 natural numbers?", lambda: r31(25), "", None),
         ("r31_e4", "Find the average of the squares of all the counting numbers up to 29.", lambda: r31(29), "", None)],
    32: [("r32_e1", r"Work out the mean of the twelve cubes \(1^{3}\) up to \(12^{3}\).", lambda: r32(12), "", None),
         ("r32_e2", "The cubes of the numbers 1 to 11 are written down. What is their average?", lambda: r32(11), "", None),
         ("r32_e3", "What is the mean of the cubes of the first 20 natural numbers?", lambda: r32(20), "", None),
         ("r32_e4", "Find the average of the cubes of all the counting numbers up to 19.", lambda: r32(19), "", None),
         ("r32_e5", "What is the mean of the cubes of the whole numbers from 1 to 6?", lambda: r32(6), "", None)],
    33: [("r33_e1", "What is the average of the first 44 even natural numbers?", lambda: r33(44), "", None),
         ("r33_e2", "The first 90 even numbers are added and the sum is divided by 90. What is the answer?", lambda: r33(90), "", None),
         ("r33_e3", "Find the mean of the first 23 even numbers.", lambda: r33(23), "", None),
         ("r33_e4", "Take the first 37 even natural numbers. What is their average?", lambda: r33(37), "", None)],
    34: [("r34_e1", "What is the average of the first 19 odd natural numbers?", lambda: r34(19), "", None),
         ("r34_e2", "The first 42 odd numbers are added and the sum is divided by 42. What is the answer?", lambda: r34(42), "", None),
         ("r34_e3", "Find the mean of the first 71 odd numbers.", lambda: r34(71), "", None),
         ("r34_e4", "Take the first 33 odd natural numbers. What is their average?", lambda: r34(33), "", None)],
    35: [("r35_e1", "Find the average of the squares of the first 13 even natural numbers.", lambda: r35(13), "", None),
         ("r35_e2", "The first 16 even numbers are squared. What is the mean of these squares?", lambda: r35(16), "", None),
         ("r35_e3", "What is the average of the squares of the first 20 even numbers?", lambda: r35(20), "", None),
         ("r35_e4", "Square each of the first 25 even natural numbers. What is the average of the results?", lambda: r35(25), "", None)],
    36: [("r36_ex", "What is the mean of the squares of the even numbers from 2 to 14?", lambda: r36(14), "", None),
         ("r36_e1", "Find the average of the squares of all the even numbers from 1 to 17.", lambda: r36(16), "", None),
         ("r36_e2", "The even numbers from 2 to 20 are squared. What is the mean of the squares?", lambda: r36(20), "", None),
         ("r36_e3", "What is the average of the squares of the even numbers up to 28?", lambda: r36(28), "", None),
         ("r36_e4", "Find the mean of the squares of the even numbers lying between 1 and 33.", lambda: r36(32), "", None),
         ("r36_e5", "Square every even number from 2 to 38. What is the average of these squares?", lambda: r36(38), "", None)],
    37: [("r37_ex", "What is the mean of the squares of the odd numbers from 1 to 9?", lambda: r37(9), "", None),
         ("r37_e1", "Find the average of the squares of all the odd numbers from 1 to 26.", lambda: r37(25), "", None),
         ("r37_e2", "The odd numbers from 1 to 27 are squared. What is the mean of the squares?", lambda: r37(27), "", None),
         ("r37_e3", "What is the average of the squares of the odd numbers up to 31?", lambda: r37(31), "", None),
         ("r37_e4", "Find the mean of the squares of the odd numbers lying between 1 and 33, both included.", lambda: r37(33), "", None),
         ("r37_e5", "Square every odd number from 1 to 40. What is the average of these squares?", lambda: r37(39), "", None)],
    38: [("r38_e1", "The average weight of 25 boys was found to be 48.6 kg, but one weight had been read as 64 kg instead of 46 kg. What is the correct average?",
          lambda: r38(25, F("48.6"), [64], [46], "kg"), "kg", None),
         ("r38_e2", "The average weight of 12 parcels was worked out as 7.5 kg. Later it was found that one parcel of 19 kg had been entered as 13 kg. Find the correct average.",
          lambda: r38(12, F("7.5"), [13], [19], "kg"), "kg", None),
         ("r38_e3", "The average of 8 numbers came out as 50, but three of them, 14, 37 and 58, had been copied as 41, 73 and 85. What is the correct average?",
          lambda: r38(8, 50, [41, 73, 85], [14, 37, 58]), "", None),
         ("r38_e4", "The average weight of 16 girls was found to be 39.5 kg. One weight of 44 kg had been written as 28 kg. Find the correct average weight.",
          lambda: r38(16, F("39.5"), [28], [44], "kg"), "kg", None),
         ("r38_e5", "The average weight of 20 students was worked out as 61 kg, but one weight was taken as 74 kg instead of 54 kg. What is the correct average?",
          lambda: r38(20, 61, [74], [54], "kg"), "kg", None)],
    39: [("r39_ex", "Three numbers are 3, 9 and 27. Find their geometric mean.", lambda: r39([3, 9, 27]), "", None),
         ("r39_e1", "What is the geometric mean of the three numbers 7, 14 and 28?", lambda: r39([7, 14, 28]), "", None),
         ("r39_e2", "Three numbers, 2, 8 and 32, are multiplied and the cube root is taken. What is this geometric mean?", lambda: r39([2, 8, 32]), "", None),
         ("r39_e3", "Three numbers 16, 36 and 81 are given. What is their geometric mean?", lambda: r39([16, 36, 81]), "", None),
         ("r39_e4", "Find the geometric mean of the numbers 12, 18 and 27.", lambda: r39([12, 18, 27]), "", None)],
    40: [("r40_e1", "Four numbers are 7, 14, 21 and 42. What is their harmonic mean?", lambda: r40([7, 14, 21, 42]), "", None),
         ("r40_e2", "Work out the harmonic mean of the three numbers 14, 21 and 42.", lambda: r40([14, 21, 42]), "", None),
         ("r40_e3", "What is the harmonic mean of the four numbers 10, 15, 20 and 30?", lambda: r40([10, 15, 20, 30]), "", None)],
    41: [("r41_e1", r"Find the average of the series 214, 216, 218, \(\ldots\), 234.", lambda: r41(214, 234), "", None),
         ("r41_e2", r"What is the mean of the odd numbers 157, 159, 161, \(\ldots\), 175?", lambda: r41(157, 175), "", None),
         ("r41_e3", "What is the mean of these numbers: 302, 304, 306, 308, 310, 312, 314, 316?", lambda: r41(302, 316), "", None),
         ("r41_e4", r"Find the mean of the series 361, 363, 365, \(\ldots\), 383.", lambda: r41(361, 383), "", None),
         ("r41_e5", r"What is the average of the even numbers 426, 428, 430, \(\ldots\), 448?", lambda: r41(426, 448), "", None)],
    42: [("r42_ex", "Of three numbers, the mean of the first and second is 8 more than the mean of the second and third. By how much is the first number more than the third?",
          lambda: r42(2, 8), "", None),
         ("r42_e1", "The average of the first two of three numbers is 21 more than the average of the last two. What is the difference between the first and the last number?",
          lambda: r42(2, 21), "", None),
         ("r42_e2", "For three numbers, the mean of the 1st and 2nd exceeds the mean of the 2nd and 3rd by 14. How much bigger is the 1st number than the 3rd?",
          lambda: r42(2, 14), "", None),
         ("r42_e3", "Of three numbers, the average of the first and the second is 18 more than the average of the second and the third. Find the first number minus the third.",
          lambda: r42(2, 18), "", None),
         ("r42_e4", "The mean of the first and middle of three numbers is 11 greater than the mean of the middle and last. What is the first number minus the last?",
          lambda: r42(2, 11), "", None),
         ("r42_e5", "Meera's average mark in Hindi and Geography is 62, and her average in Hindi and Art is 71. By how many marks is her Art mark more than her Geography mark?",
          lambda: r42(2, 9), "", None),
         ("r42_e6", "Ravi's average mark in Maths, Physics, Chemistry and English is 12 less than his average in Maths, Chemistry, English and Biology. "
                    "How many more marks did he get in Biology than in Physics?", lambda: r42(4, 12), "", None),
         ("r42_e7", "The average temperature on Monday, Tuesday and Wednesday was 20°C, and on Tuesday, Wednesday and Thursday it was 21°C. "
                    "If Thursday was 26°C, what was the temperature on Monday?", lambda: r42_temp(20, 21, 26), "°C", None),
         ("r42_e8", "The mean temperature of Monday, Tuesday and Wednesday was 28°C and that of Tuesday, Wednesday and Thursday was 30°C. "
                    "Thursday was 35°C. Find Monday's temperature.", lambda: r42_temp(28, 30, 35), "°C", None),
         ("r42_e9", r"The mean temperature from Monday to Wednesday was 30°C and from Tuesday to Thursday it was 28°C. If Thursday's temperature was "
                    r"\(\frac{3}{4}\) of Monday's, what was the temperature on Thursday?", lambda: r42_ratio(30, 28, F(3, 4)), "°C", None)],
    43: [("r43_e1", "The average of 5 consecutive even numbers is 54. What is the difference between the largest and the smallest?", lambda: r43(5, 54), "", None),
         ("r43_e2", "11 consecutive odd numbers have an average of 75. By how much does the largest exceed the smallest?", lambda: r43(11, 75), "", None),
         ("r43_e3", "The mean of 13 consecutive even numbers is 40. Find the difference between the greatest and the least of them.", lambda: r43(13, 40), "", None),
         ("r43_e4", "20 consecutive odd numbers have a mean of 60. What is the gap between the largest and the smallest of them?", lambda: r43(20, 60), "", None)],
}

if __name__ == "__main__":
    main(OLD, NEW, CARDS, range(31, 44))
