"""Average Rules 12-17 (2026-10-30). Rule 12 / 13: pass and fail averages - number passed n(T - F)/(P - F), number failed
n(P - T)/(P - F). Rule 14: odd n results, the first and last (n + 1)/2 share the middle one - it is (n + 1)/2 (b + c) - na. Rule 15:
the middle number when the first and last groups do not share it - total of all minus the two group totals. Rule 16: the nth
innings raises the average by y - average after n innings x - y(n - 1). Rule 17: runs needed next to raise the average to y -
n(y - x) + y. Writes the six cards, regenerates the old rows 506-510 with simple-style sentences, new settings and all-new
numbers, and adds the book's exercises that had no copy (Rule 14 Exr 2-5 have inconsistent numbers in the book - the new ones are
consistent; Rule 14 Exr 6 is a Rule 15 question and is filed there). Usage: python gen_12_17.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_6_11 import UU, answer_json, nf, opts  # noqa: E402
from helpers import result  # noqa: E402

T12 = (r"If the average mark of \(n\) candidates is \(T\), the average of those who passed is \(P\) and of those who failed is \(F\), "
       r"the number who passed is<br>\[ \frac{n(T-F)}{P-F} \]")
T13 = (r"If the average mark of \(n\) candidates is \(T\), the average of those who passed is \(P\) and of those who failed is \(F\), "
       r"the number who failed is<br>\[ \frac{n(P-T)}{P-F} \]")
T14 = (r"If the average of \(n\) results (\(n\) odd) is \(a\), the average of the first \(\frac{n+1}{2}\) is \(b\) and of the last "
       r"\(\frac{n+1}{2}\) is \(c\), the middle (\(\frac{n+1}{2}\)th) result is<br>\[ \frac{n+1}{2}(b+c)-na \]")
T15 = (r"If the average of \(n\) results is \(a\), the first \(p\) average \(b\) and the last \(q\) average \(c\) (with \(p+q=n-1\)), "
       r"the one result between them is<br>\[ na-(pb+qc) \]")
T16 = (r"If a batsman scores \(x\) in his \(n\)th innings and this raises his average by \(y\), his average after \(n\) innings is"
       r"<br>\[ x-y(n-1) \]")
T17 = (r"If a cricketer's average after \(n\) innings is \(x\), the runs he must score in the next innings to raise it to \(y\) are"
       r"<br>\[ n(y-x)+y \]")
TH = {12: T12, 13: T13, 14: T14, 15: T15, 16: T16, 17: T17}


def apply(r):
    return ("Apply the specified rule.", TH[r].split("<br>")[1])


def r12_pass(n, T, P, Fl, ask="passed"):
    n, T, P, Fl = map(F, (n, T, P, Fl))
    p = n * (T - Fl) / (P - Fl)
    f = n - p
    if ask == "passed":
        trad = steps(("Let the number who passed be \\(p\\).", rf"Then \({tex(n)}-p\) failed. Total marks \(= {tex(n)}\times {nf(T)} = {nf(n * T)}\)."),
                     ("Form the equation.", rf"\[ {nf(P)}p + {nf(Fl)}({tex(n)}-p) = {nf(n * T)} \]"),
                     ("Solve.", rf"\[ {nf(P - Fl)}p = {nf(n * T)} - {nf(n * Fl)} = {nf(n * (T - Fl))} \;\Rightarrow\; p = {nf(p)} \]"))
        rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(T = {nf(T)}\), \(P = {nf(P)}\), \(F = {nf(Fl)}\)."), apply(12),
                     ("Substitute the values.", rf"\[ \frac{{{tex(n)}({nf(T)}-{nf(Fl)})}}{{{nf(P)}-{nf(Fl)}}} = \frac{{{nf(n * (T - Fl))}}}{{{nf(P - Fl)}}} = {nf(p)} \]"))
        return result(("number", p), T12, trad, rule, UU(p), [rf"\(T-F = {nf(T - Fl)}\).", rf"\(P-F = {nf(P - Fl)}\).", rf"Passed \(= {nf(p)}\)."],
                      rf"\[ \frac{{{tex(n)}\times {nf(T - Fl)}}}{{{nf(P - Fl)}}} = {nf(p)} \]")
    trad = steps(("Let the number who failed be \\(f\\).", rf"Then \({tex(n)}-f\) passed. Total marks \(= {tex(n)}\times {nf(T)} = {nf(n * T)}\)."),
                 ("Form the equation.", rf"\[ {nf(P)}({tex(n)}-f) + {nf(Fl)}f = {nf(n * T)} \]"),
                 ("Solve.", rf"\[ {nf(P - Fl)}f = {nf(n * P)} - {nf(n * T)} = {nf(n * (P - T))} \;\Rightarrow\; f = {nf(f)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(T = {nf(T)}\), \(P = {nf(P)}\), \(F = {nf(Fl)}\)."), apply(13),
                 ("Substitute the values.", rf"\[ \frac{{{tex(n)}({nf(P)}-{nf(T)})}}{{{nf(P)}-{nf(Fl)}}} = \frac{{{nf(n * (P - T))}}}{{{nf(P - Fl)}}} = {nf(f)} \]"))
    return result(("number", f), T13, trad, rule, UU(f), [rf"\(P-T = {nf(P - T)}\).", rf"\(P-F = {nf(P - Fl)}\).", rf"Failed \(= {nf(f)}\)."],
                  rf"\[ \frac{{{tex(n)}\times {nf(P - T)}}}{{{nf(P - Fl)}}} = {nf(f)} \]")


def r14_middle(n, a, b, c):
    n, a, b, c = map(F, (n, a, b, c))
    k = (n + 1) / 2
    v = k * (b + c) - n * a
    assert v > 0
    trad = steps(("Totals.", rf"All \({tex(n)}\): \({tex(n)}\times {nf(a)} = {nf(n * a)}\). First \({tex(k)}\): \({tex(k)}\times {nf(b)} = {nf(k * b)}\). "
                             rf"Last \({tex(k)}\): \({tex(k)}\times {nf(c)} = {nf(k * c)}\)."),
                 ("The middle one is counted twice.", rf"The first \({tex(k)}\) and the last \({tex(k)}\) together cover all \({tex(n)}\) results with the "
                                                      rf"\({tex(k)}\)th one twice: \[ {nf(k * b)} + {nf(k * c)} - {nf(n * a)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(\frac{{n+1}}{{2}} = {tex(k)}\), \(a = {nf(a)}\), \(b = {nf(b)}\), \(c = {nf(c)}\)."), apply(14),
                 ("Substitute the values.", rf"\[ {tex(k)}({nf(b)}+{nf(c)}) - {tex(n)}\times {nf(a)} = {nf(k * (b + c))} - {nf(n * a)} = {nf(v)} \]"))
    return result(("number", v), T14, trad, rule, UU(v), [rf"\({tex(k)}(b+c) = {nf(k * (b + c))}\).", rf"\(na = {nf(n * a)}\).", rf"Middle \(= {nf(v)}\)."],
                  rf"\[ {tex(k)}({nf(b)}+{nf(c)}) - {nf(n * a)} = {nf(v)} \]")


def r15_between(n, a, p, b, q, c):
    n, a, p, b, q, c = map(F, (n, a, p, b, q, c))
    assert p + q == n - 1
    v = n * a - (p * b + q * c)
    trad = steps(("Total of all.", rf"\[ {tex(n)}\times {nf(a)} = {nf(n * a)} \]"),
                 ("Totals of the two groups.", rf"First \({tex(p)}\): \({tex(p)}\times {nf(b)} = {nf(p * b)}\); last \({tex(q)}\): \({tex(q)}\times {nf(c)} = {nf(q * c)}\)."),
                 ("The one left over.", rf"\[ {nf(n * a)} - ({nf(p * b)} + {nf(q * c)}) = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(a = {nf(a)}\), \(p = {tex(p)}\), \(b = {nf(b)}\), \(q = {tex(q)}\), \(c = {nf(c)}\)."), apply(15),
                 ("Substitute the values.", rf"\[ {tex(n)}\times {nf(a)} - ({tex(p)}\times {nf(b)} + {tex(q)}\times {nf(c)}) = {nf(n * a)} - {nf(p * b + q * c)} = {nf(v)} \]"))
    return result(("number", v), T15, trad, rule, UU(v), [rf"All \(= {nf(n * a)}\).", rf"Two groups \(= {nf(p * b + q * c)}\).", rf"Between \(= {nf(v)}\)."],
                  rf"\[ {nf(n * a)} - {nf(p * b + q * c)} = {nf(v)} \]")


def r15_others(n, a, p, b, q, c):
    """the one number between the groups is left out: the average of the other n - 1."""
    n, a, p, b, q, c = map(F, (n, a, p, b, q, c))
    mid = n * a - (p * b + q * c)
    v = (p * b + q * c) / (n - 1)
    trad = steps(("Totals of the two groups.", rf"First \({tex(p)}\): \({tex(p)}\times {nf(b)} = {nf(p * b)}\); last \({tex(q)}\): \({tex(q)}\times {nf(c)} = {nf(q * c)}\)."),
                 ("The other numbers.", rf"These \({tex(p + q)}\) numbers are all except the one left out; their total is \({nf(p * b + q * c)}\)."),
                 ("Their average.", rf"\[ {nf(p * b + q * c)} \div {tex(p + q)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(a = {nf(a)}\), \(p = {tex(p)}\), \(b = {nf(b)}\), \(q = {tex(q)}\), \(c = {nf(c)}\)."), apply(15),
                 ("Substitute the values.", rf"The number between the groups is \({nf(n * a)} - {nf(p * b + q * c)} = {nf(mid)}\); without it: "
                                            rf"\[ \frac{{{nf(n * a)} - {nf(mid)}}}{{{tex(n - 1)}}} = \frac{{{nf(n * a - mid)}}}{{{tex(n - 1)}}} = {nf(v)} \]"))
    return result(("number", v), T15, trad, rule, UU(v), [rf"Left-out number \(= {nf(mid)}\).", rf"Others' total \(= {nf(n * a - mid)}\).", rf"Average \(= {nf(v)}\)."],
                  rf"\[ \frac{{{nf(n * a - mid)}}}{{{tex(n - 1)}}} = {nf(v)} \]")


def r16_after(n, x, y):
    n, x, y = map(F, (n, x, y))
    A = x - n * y                                     # average before the nth innings
    v = A + y
    trad = steps(("Let the average before this innings be \\(A\\).", rf"Total after \({tex(n - 1)}\) innings \(= {tex(n - 1)}A\)."),
                 ("Form the equation.", rf"After the \({tex(n)}\)th innings the average is \(A+{nf(y)}\): \[ {tex(n - 1)}A + {nf(x)} = {tex(n)}(A+{nf(y)}) \]"),
                 ("Solve.", rf"\[ A = {nf(x)} - {tex(n)}\times {nf(y)} = {nf(A)}, \quad A+{nf(y)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(x)}\), \(y = {nf(y)}\)."), apply(16),
                 ("Substitute the values.", rf"\[ {nf(x)} - {nf(y)}({tex(n)}-1) = {nf(x)} - {nf(y * (n - 1))} = {nf(v)} \]"))
    return result(("number", v), T16, trad, rule, UU(v), [rf"\(y(n-1) = {nf(y * (n - 1))}\).", rf"\(x = {nf(x)}\).", rf"New average \(= {nf(v)}\)."],
                  rf"\[ {nf(x)} - {nf(y)}\times {tex(n - 1)} = {nf(v)} \]")


def r17_next(n, x, y):
    n, x, y = map(F, (n, x, y))
    v = (n + 1) * y - n * x
    trad = steps(("Runs so far.", rf"\[ {tex(n)}\times {nf(x)} = {nf(n * x)} \]"), ("Runs needed after the next innings.", rf"\[ {tex(n + 1)}\times {nf(y)} = {nf((n + 1) * y)} \]"),
                 ("In the next innings.", rf"\[ {nf((n + 1) * y)} - {nf(n * x)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(x)}\), \(y = {nf(y)}\)."), apply(17),
                 ("Substitute the values.", rf"\[ {tex(n)}({nf(y)}-{nf(x)})+{nf(y)} = {nf(n * (y - x))}+{nf(y)} = {nf(v)} \]"))
    return result(("number", v), T17, trad, rule, UU(v, "runs"), [rf"So far \(= {nf(n * x)}\).", rf"Needed \(= {nf((n + 1) * y)}\).", rf"Next innings \(= {nf(v)}\) runs."],
                  rf"\[ {tex(n)}({nf(y)}-{nf(x)})+{nf(y)} = {nf(v)} \]")


CARDS = {
    12: card(12, "Number Who Passed", r"Pass and fail averages on either side of the overall average share the candidates like an alligation.", r"\[ \frac{n(T-F)}{P-F} \]",
             [("Total marks", r"nT = pP+(n-p)F"), ("Solve for p", r"p(P-F) = n(T-F)"), ("Passed", r"\frac{n(T-F)}{P-F}")],
             r"Each passed candidate is \(P-F\) marks above a failed one; the overall average sits \(T-F\) above \(F\), so the share who passed is \(\frac{T-F}{P-F}\).",
             "'The average of n candidates is T, of those passed P and of those failed F; how many passed?'",
             r"\(50\) candidates, \(T=40\), \(P=45\), \(F=20\): \(\frac{50\times 20}{25}=40\) passed.", r"Putting \(P-T\) on top (that gives the number who failed)."),
    13: card(13, "Number Who Failed", r"The same sharing, read from the passed side.", r"\[ \frac{n(P-T)}{P-F} \]",
             [("Total marks", r"nT = (n-f)P+fF"), ("Solve for f", r"f(P-F) = n(P-T)"), ("Failed", r"\frac{n(P-T)}{P-F}")],
             r"The overall average is \(P-T\) below the pass average; the failed share is that gap over the whole gap \(P-F\). Passed + failed \(= n\) is a quick check.",
             "'The average of n candidates is T, of those passed P and of those failed F; how many failed?'",
             r"\(50\) candidates, \(T=40\), \(P=45\), \(F=20\): \(\frac{50\times 5}{25}=10\) failed.", r"Putting \(T-F\) on top (that gives the number who passed)."),
    14: card(14, "Middle Result - Groups Share It", r"For an odd number of results, the first half and the last half (each with the middle one) count the middle result twice.",
             r"\[ \frac{n+1}{2}(b+c)-na \]",
             [("First half", r"\frac{n+1}{2}\ \text{at}\ b"), ("Last half", r"\frac{n+1}{2}\ \text{at}\ c"), ("Middle", r"\frac{n+1}{2}(b+c)-na")],
             r"The two half-totals add up to the total of all plus the middle result once more, so subtracting the total of all leaves the middle result.",
             "'The average of 11 results is a; of the first 6 is b and of the last 6 is c; find the 6th.'",
             r"\(7\) results average \(20\), first \(4\) average \(18\), last \(4\) average \(25\): \(4(43)-140=32\).", r"Using \(\frac{n-1}{2}\) when the groups share the middle one."),
    15: card(15, "One Result Between Two Groups", r"When the two groups do not include the result between them, take both group totals from the total of all.",
             r"\[ na-(pb+qc) \]", [("All", r"n\ \text{at}\ a"), ("Groups", r"p\ \text{at}\ b,\ q\ \text{at}\ c"), ("Between", r"na-(pb+qc)")],
             r"The first \(p\), the one between and the last \(q\) make up all \(n\), so the one left over is what the group totals do not cover.",
             "'The average of 11 results is a; of the first five is b and of the last five is c; find the 6th.'",
             r"\(9\) results average \(30\), first \(4\) average \(28\), last \(4\) average \(31\): \(270-236=34\).", r"Adding the middle result into one of the groups when it is not in either."),
    16: card(16, "Innings That Raises the Average", r"The new score pays for the rise of every innings, its own included.", r"\[ x-y(n-1) \]",
             [("Before", r"(n-1)A"), ("After", r"(n-1)A+x = n(A+y)"), ("New average", r"A+y = x-y(n-1)")],
             r"The score \(x\) lifts the average of all \(n\) innings by \(y\); \(y(n-1)\) of it goes to the old innings and what is left, \(x-y(n-1)\), is the new average itself.",
             "'A batsman in his nth innings makes a score of x and thereby increases his average by y; find his average after n innings.'",
             r"\(12\)th innings \(80\), average up by \(4\): \(80-4\times 11=36\).", r"Multiplying by \(n\) in place of \(n-1\) (that gives the old average)."),
    17: card(17, "Runs Needed to Raise the Average", r"The next score must lift every innings so far and also stand at the new average itself.", r"\[ n(y-x)+y \]",
             [("So far", r"nx"), ("Needed", r"(n+1)y"), ("Next innings", r"(n+1)y-nx = n(y-x)+y")],
             r"Each of the \(n\) innings already played must go up by \(y-x\), and the new innings itself must equal \(y\).",
             "'A cricketer has completed n innings with average x; how many runs must he make in the next innings to raise his average to y?'",
             r"\(10\) innings averaging \(30\), target \(33\): \(10\times 3+33=63\).", r"Forgetting the \(+y\) for the new innings itself."),
}
OLD = {   # row: (rule, question, builder, unit)
    506: (12, "In a test taken by 150 students, the average mark is 42. The students who passed have an average of 48 and those who failed have an average of 18. "
              "How many students passed?", lambda: r12_pass(150, 42, 48, 18), ""),
    507: (13, "In a test taken by 84 people, the average score is 54. Those who passed averaged 62 and those who failed averaged 41. How many people failed?",
          lambda: r12_pass(84, 54, 62, 41, "failed"), ""),
    508: (14, "The average of 13 numbers is 44. The average of the first 7 is 41 and the average of the last 7 is 51. What is the 7th number?",
          lambda: r14_middle(13, 44, 41, 51), ""),
    509: (16, "A batsman scores 79 runs in his 13th innings and this raises his average by 4. What is his average after 13 innings?", lambda: r16_after(13, 79, 4), ""),
    510: (17, "A cricketer has played 12 innings with an average of 31.5 runs. How many runs must she score in the next innings to bring her average up to 34?",
          lambda: r17_next(12, F("31.5"), 34), "runs"),
}
PASS_Q = ("In an examination taken by {n} candidates, the average mark is {T}. The average of those who passed is {P} and of those who failed is {F}. "
          "How many candidates {ask}?")
NEW = {   # rule: [(key, question, builder, unit, wrong options or None)]
    12: [(f"r12_e{i}", PASS_Q.format(n=n, T=T, P=P, F=Fl, ask="passed"), (lambda n=n, T=T, P=P, Fl=Fl: r12_pass(n, T, P, Fl)), "", None)
         for i, (n, T, P, Fl) in enumerate([(60, 46, 50, 30), (96, 37, 40, 24), (72, 29, 33, 17), (55, 43, 47, 36), (91, 23, 26, 13)], 1)],
    13: [(f"r13_e{i}", PASS_Q.format(n=n, T=T, P=P, F=Fl, ask="failed"), (lambda n=n, T=T, P=P, Fl=Fl: r12_pass(n, T, P, Fl, "failed")), "", None)
         for i, (n, T, P, Fl) in enumerate([(132, 24, 31, 19), (99, 17, 26, 15), (88, 22, 25, 19), (138, 38, 42, 19), (105, 27, 34, 13)], 1)],
    14: [("r14_e1", "The average of 15 numbers is 40. The first 8 of them average 43 and the last 8 average 38. Find the 8th number.", lambda: r14_middle(15, 40, 43, 38), "", None),
         ("r14_e2", "The average of 21 numbers is 30. The average of the first 11 is 28 and that of the last 11 is 34. What is the 11th number?", lambda: r14_middle(21, 30, 28, 34), "", None),
         ("r14_e3", "A set of 9 numbers has an average of 26. The first 5 have an average of 24 and the last 5 an average of 31. Find the 5th number.", lambda: r14_middle(9, 26, 24, 31), "", None),
         ("r14_e4", "The average of 19 numbers is 55. The first 10 average 57 and the last 10 average 56. What is the 10th number?", lambda: r14_middle(19, 55, 57, 56), "", None),
         ("r14_e5", "The average of 17 numbers is 34. The average of the first 9 is 36 and of the last 9 is 37. Find the 9th number.", lambda: r14_middle(17, 34, 36, 37), "", None)],
    15: [("r15_ex", "The average of 9 results is 47. The first 4 average 44 and the last 4 average 45. Find the 5th result.", lambda: r15_between(9, 47, 4, 44, 4, 45), "", None),
         ("r15_e1", "The average of 11 numbers is 42.6. The first 3 of them average 41.2 and the last 7 average 43.5. If the 4th number is left out, what is the average of the other 10?",
          lambda: r15_others(11, F("42.6"), 3, F("41.2"), 7, F("43.5")), "", [F("42.6"), F("42.18"), F("43.01")]),
         ("r15_e2", "The average of 10 results is 41. The first 5 average 38 and the last 4 average 44. Find the 6th result.", lambda: r15_between(10, 41, 5, 38, 4, 44), "", None),
         ("r15_e3", "The average of 13 results is 33. The first 6 average 30 and the last 6 average 29. Find the 7th result.", lambda: r15_between(13, 33, 6, 30, 6, 29), "", None),
         ("r15_e4", "The average of 14 results is 27. The first 6 average 25 and the last 7 average 26. Find the 7th result.", lambda: r15_between(14, 27, 6, 25, 7, 26), "", None),
         ("r15_e5", "The average of 23 results is 21. The first 11 average 18 and the last 11 average 20. What is the 12th result?", lambda: r15_between(23, 21, 11, 18, 11, 20), "", None)],
    16: [("r16_e1", "A batsman makes 97 runs in his 18th innings and so raises his average by 3. What is his average after 18 innings?", lambda: r16_after(18, 97, 3), "", None),
         ("r16_e2", "In her 15th innings a batter is out 4 runs short of a century, and this raises her average by 3. What is her average after 15 innings?",
          lambda: r16_after(15, 96, 3), "", None),
         ("r16_e3", "A batsman scores 104 runs in his 25th innings, which raises his average by 2. Find his average after 25 innings.", lambda: r16_after(25, 104, 2), "", None),
         ("r16_e4", "A batter makes 87 in the 11th innings and the average goes up by 5. What is the average after 11 innings?", lambda: r16_after(11, 87, 5), "", None),
         ("r16_e5", "A batsman scores 79 runs in his 36th innings and his average rises by 1. What is his average after 36 innings?", lambda: r16_after(36, 79, 1), "", None)],
    17: [("r17_e1", "A cricketer has an average of 24 runs from 16 innings. How many runs must he make in the next innings to raise the average to 28?",
          lambda: r17_next(16, 24, 28), "runs", None),
         ("r17_e2", "After 24 innings a batter's average is 38.5 runs. How many runs are needed in the next innings to make the average 39?",
          lambda: r17_next(24, F("38.5"), 39), "runs", None),
         ("r17_e3", "A batsman has played 23 innings with an average of 20 runs. How many runs must he score in the next innings to lift his average to 23?",
          lambda: r17_next(23, 20, 23), "runs", None),
         ("r17_e4", "A cricketer's average after 22 innings is 33.5 runs. How many runs must she make in her next innings to raise it to 34?",
          lambda: r17_next(22, F("33.5"), 34), "runs", None),
         ("r17_e5", "A batsman has an average of 27 runs after 16 innings. How many runs must he score in the next innings to raise his average to 30?",
          lambda: r17_next(16, 27, 30), "runs", None)],
}


def main():
    for rule in range(12, 18):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        ids = [rid for rid, v in OLD.items() if v[0] == rule]
        if ids:
            dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
            assert dump["rule_card"] is None
            rows = {r["id"]: r for r in dump["rows"]}
            assert sorted(rows) == sorted(ids)
            out = []
            for rid in ids:
                _, q, fn, unit = OLD[rid]
                g = fn()
                op, _ = opts(g["answer"][1], unit)
                extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
                extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
                out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
            json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
        json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, unit, wrong in NEW[rule]:
            g = fn()
            op, pos = opts(g["answer"][1], unit, wrong)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        json.dump({"rules_html": [{"chapter": "average", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(ids)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
