"""Rules 22-29 (book II. Combinations, Rules 9-16; site number = book number + 13): writes the eight rule cards, regenerates
the old rows in the prompt #13 layout and links them, and adds the book exercises that had no copy (numbers changed).
Fixes: 862 (no option held 40 lines, key on the empty option e), 864 ("can't student fail" -> "can a student fail"),
868 (display-math options such as (7)!^3 written inline as (7!)^{3}). Same outputs as gen_1_7.py."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from pc_common import D, I, comb, factorial, falling_tex, fin, nC, num, result, times  # noqa: E402
import gen_1_7  # noqa: E402
from gen_14_21 import choose_trad, ctex  # noqa: E402


# ---------------------------------------------------------------- Rule 22 (book C9): lines with collinear points
T22 = (r"There are \(n\) points in a plane, of which \(m\) are collinear (no other three are). The number of straight lines "
       r"formed by joining them is<br>\[ {}^{n}C_{2} - {}^{m}C_{2} + 1 \]")


def r22(n, m):
    a, b = comb(n, 2), comb(m, 2)
    v = a - b + 1
    trad = steps(
        ("Pretend no three points are collinear.", "Every pair of points would give its own line:" + D(rf"\frac{{{n}\times {n - 1}}}{{2}} = {a}")),
        ("Merge the lines on the collinear points.", rf"The \({m}\) collinear points give \(\frac{{{m}\times {m - 1}}}{{2}} = {b}\) pairs, but all of them lie on ONE line:"
         + D(rf"{a} - {b} + 1 = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) points, \(m = {m}\) collinear."),
        ("Apply the specified rule.", D(r"{}^{n}C_{2} - {}^{m}C_{2} + 1")),
        ("Substitute the values.", D(rf"{nC(n, 2)} - {nC(m, 2)} + 1 = {a} - {b} + 1 = {v}")))
    rb = [rf"\(n = {n}\), \(m = {m}\).", r"Lines \(= {}^{n}C_{2} - {}^{m}C_{2} + 1\).", rf"\({a} - {b} + 1 = {v}\)."]
    return result(num(v), T22, trad, rule, I(v), rb, D(rf"{nC(n, 2)} - {nC(m, 2)} + 1 = {v}"))


# ---------------------------------------------------------------- Rule 23 (book C10): cards to every other student
T23 = (r"On a new year day every student of a class sends a card to every other student. If the postman delivers \(C\) cards, "
       r"the number of students \(n\) is found from<br>\[ n(n-1) = C \]")


def r23_find(C):
    n = next(n for n in range(2, 500) if n * (n - 1) == C)
    trad = steps(
        ("Count the cards for \\(n\\) students.", r"Each student sends a card to each of the other \(n-1\) students, so \(n\) students send \(n(n-1)\) cards "
                                                  r"(A to B and B to A are two different cards)."),
        ("Form the equation.", D(rf"n(n-1) = {C} = {n}\times {n - 1}")),
        ("Read off n.", rf"\(n = {n}\) (the root \(n = -{n - 1}\) is impossible)."))
    rule = steps(
        ("Identify the value.", rf"\(C = {C}\) cards."),
        ("Apply the specified rule.", D(r"n(n-1) = C")),
        ("Substitute and solve.", D(rf"n^{{2}} - n - {C} = 0 \Rightarrow (n - {n})(n + {n - 1}) = 0") + rf"\(n = {n}\)."))
    rb = [rf"\(C = {C}\).", r"\(n(n-1) = C\).", rf"\({C} = {n}\times {n - 1}\), so \(n = {n}\)."]
    return result(num(n), T23, trad, rule, I(n), rb, D(rf"n(n-1) = {C} = {n}\times {n - 1} \Rightarrow n = {n}"))


def r23_count(n):
    C = n * (n - 1)
    trad = steps(
        ("Count one student's cards.", rf"Each of the \({n}\) students sends \({n - 1}\) cards."),
        ("Add for all students.", rf"A to B and B to A are different cards, so nothing is counted twice:" + D(rf"{n}\times {n - 1} = {C}")))
    rule = steps(
        ("Identify the value.", rf"\(n = {n}\) students."),
        ("Apply the specified rule.", D(r"C = n(n-1)")),
        ("Substitute the value.", D(rf"{n}\times ({n}-1) = {C}")))
    rb = [rf"\(n = {n}\).", r"\(C = n(n-1)\).", rf"\({n}\times {n - 1} = {C}\)."]
    return result(num(C), T23, trad, rule, I(C), rb, D(rf"{n}\times {n - 1} = {C}"))


# ---------------------------------------------------------------- Rules 24 and 25 (book C11, C12): 2^n - 1
T24 = r"If a minimum is to be secured in each of \(n\) subjects for a pass, the number of ways a student can fail is<br>\[ 2^{n} - 1 \]"
T25 = r"If there are \(n\) questions in a paper, the number of ways in which a student can solve one or more questions is<br>\[ 2^{n} - 1 \]"


def two_n(n, T, unit, verb, none_case):
    v = 2 ** n - 1
    trad = steps(
        (f"Each {unit} has two possibilities.", rf"For each of the \({n}\) {unit}s there are 2 cases ({verb}); the cases of different {unit}s combine freely:"
         + D(rf"{times(*([2] * n))} = 2^{{{n}}} = {2 ** n}")),
        ("Remove the case that does not count.", none_case + D(rf"{2 ** n} - 1 = {v}")))
    sums = " + ".join(nC(n, k) for k in range(1, n + 1))
    rule = steps(
        ("Identify the value.", rf"\(n = {n}\) {unit}s."),
        ("Apply the specified rule.", D(rf"{sums} = 2^{{n}} - 1") if n <= 6 else D(r"{}^{n}C_{1} + {}^{n}C_{2} + \cdots + {}^{n}C_{n} = 2^{n} - 1")),
        ("Substitute the value.", D(rf"2^{{{n}}} - 1 = {2 ** n} - 1 = {v}")))
    rb = [rf"\(n = {n}\).", r"Ways \(= 2^{n} - 1\).", rf"\(2^{{{n}}} - 1 = {v}\)."]
    return result(num(v), T, trad, rule, I(v), rb, D(rf"2^{{{n}}} - 1 = {v}"))


def r24(n):
    return two_n(n, T24, "subject", "pass or fail", "The only case that is not a failure is passing in every subject.")


def r25(n, unit="question", none_case="Solving no question at all is not 'one or more', so that case is removed."):
    return two_n(n, T25, unit, "attempted or not", none_case)


# ---------------------------------------------------------------- Rule 26 (book C13): exactly r from group A
T26 = (r"From \(x\) persons of group A and \(y\) persons of group B, the number of ways of choosing \(n\) persons with exactly "
       r"\(r\) from group A (and the rest from B) is<br>\[ {}^{x}C_{r}\times {}^{y}C_{n-r} \]")


def r26(x, y, n, r, A, B):
    a, b = comb(x, r), comb(y, n - r)
    v = a * b
    trad = steps(
        (f"Choose the {A}.", rf"Exactly \({r}\) of the \({x}\) {A}:" + D(ctex(x, r).split(" = ", 1)[1] if r > 1 else str(x))),
        (f"Choose the {B}.", rf"The other \({n} - {r} = {n - r}\) come from the \({y}\) {B}:" + D(ctex(y, n - r).split(" = ", 1)[1] if n - r > 1 else str(y))),
        ("Multiply (each choice of one goes with each choice of the other).", D(f"{a}\\times {b} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\) {A}, \(y = {y}\) {B}, choose \(n = {n}\) with exactly \(r = {r}\) {A}."),
        ("Apply the specified rule.", D(r"{}^{x}C_{r}\times {}^{y}C_{n-r}")),
        ("Substitute the values.", D(rf"{nC(x, r)}\times {nC(y, n - r)} = {a}\times {b} = {v}")))
    rb = [rf"\(x = {x}\), \(y = {y}\), \(n = {n}\), \(r = {r}\).", r"Ways \(= {}^{x}C_{r}\times {}^{y}C_{n-r}\).", rf"\({nC(x, r)}\times {nC(y, n - r)} = {a}\times {b} = {v}\)."]
    return result(num(v), T26, trad, rule, I(v), rb, D(rf"{nC(x, r)}\times {nC(y, n - r)} = {v}"))


def r26_one_each(counts, colours):
    v = 1
    for c in counts:
        v *= c
    trad = steps(
        ("One ball of each colour.", "Three balls of different colours means one " + ", one ".join(colours) + " ball."),
        ("Count the choices.", ", ".join(rf"{c}: \({k}\) ways" for c, k in zip(colours, counts)) + D(f"{times(*counts)} = {v}")))
    rule = steps(
        ("Identify the values.", "Groups: " + ", ".join(rf"\({k}\) {c}" for c, k in zip(colours, counts)) + "; exactly 1 from each."),
        ("Apply the specified rule.", r"Exactly \(r\) from each group: \({}^{x}C_{r}\times {}^{y}C_{s}\times\cdots\) (here every \(r = 1\))."),
        ("Substitute the values.", D(times(*[nC(k, 1) for k in counts]) + f" = {times(*counts)} = {v}")))
    rb = ["One ball from each colour group.", r"\({}^{x}C_{1}\times {}^{y}C_{1}\times {}^{z}C_{1}\).", rf"\({times(*counts)} = {v}\)."]
    return result(num(v), T26, trad, rule, I(v), rb, D(f"{times(*counts)} = {v}"))


def r26_words(x, y, r, s):
    a, b = comb(x, r), comb(y, s)
    v = a * b * factorial(r + s)
    trad = steps(
        ("Choose the letters.", rf"\({r}\) of the \({x}\) consonants: \({a}\) ways; \({s}\) of the \({y}\) vowels: \({b}\) ways."),
        ("Arrange each choice.", rf"The \({r + s}\) chosen letters (all different) form \({r + s}! = {factorial(r + s)}\) words."),
        ("Multiply.", D(f"{a}\\times {b}\\times {factorial(r + s)} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\) consonants, \(y = {y}\) vowels, exactly \({r}\) and \({s}\)."),
        ("Apply the specified rule.", r"Selections \(= {}^{x}C_{r}\times {}^{y}C_{s}\); each selection then gives \((r+s)!\) words."),
        ("Substitute the values.", D(rf"{nC(x, r)}\times {nC(y, s)}\times {r + s}! = {a}\times {b}\times {factorial(r + s)} = {v}")))
    rb = [rf"\({x}\) consonants, \({y}\) vowels, choose \({r}\) and \({s}\).", r"\({}^{x}C_{r}\times {}^{y}C_{s}\times (r+s)!\).", rf"\({a}\times {b}\times {factorial(r + s)} = {v}\)."]
    return result(num(v), T26, trad, rule, I(v), rb, D(rf"{nC(x, r)}\times {nC(y, s)}\times {r + s}! = {v}"))


def r26_at_least(x, y, n, A, B):
    """n chosen from x of A and y of B with at least one of A: add the cases 'exactly r of A'."""
    cases = [(r, comb(x, r) * comb(y, n - r)) for r in range(1, min(n, x) + 1) if n - r <= y]
    v = sum(w for _, w in cases)
    total, none = comb(x + y, n), comb(y, n)
    trad = steps(
        ("Count all the selections.", rf"\({n}\) of the \({x + y}\) children: \({total}\) ways (" + I(ctex(x + y, n)) + ")."),
        (f"Remove the selections with no {A[:-1]}.", rf"All \({n}\) from the \({y}\) {B}: \({none}\) way{'s' if none != 1 else ''}." + D(f"{total} - {none} = {v}")))
    table = '<table border="1" cellpadding="4"><tr><th>' + A.capitalize() + "</th><th>" + B.capitalize() + "</th><th>Ways</th></tr>" + "".join(
        rf"<tr><td>\({r}\)</td><td>\({n - r}\)</td><td>\({nC(x, r)}\times {nC(y, n - r)} = {w}\)</td></tr>" for r, w in cases) + "</table>"
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\) {A}, \(y = {y}\) {B}, choose \({n}\) with at least one {A[:-1]}."),
        ("Apply the specified rule.", r"Add the cases 'exactly \(r\) " + A + r"', each \({}^{x}C_{r}\times {}^{y}C_{n-r}\):" + table),
        ("Substitute the values.", D(" + ".join(str(w) for _, w in cases) + f" = {v}")))
    rb = [rf"\({x}\) {A}, \({y}\) {B}, choose \({n}\).", r"Add \({}^{x}C_{r}\times {}^{y}C_{n-r}\) for \(r = 1, 2, \ldots\)", " + ".join(str(w) for _, w in cases) + rf" \(= {v}\)."]
    return result(num(v), T26, trad, rule, I(v), rb, D(" + ".join(str(w) for _, w in cases) + f" = {v}"))


# ---------------------------------------------------------------- Rule 27 (book C14): selection of fruits
T27 = (r"A basket has \(x\) oranges, \(y\) apples, \(z\) mangoes (fruits of one kind alike) and \(n\) other fruits all of different "
       r"kinds. The number of ways of selecting fruits (at least one) is<br>\[ (x+1)(y+1)(z+1)\times 2^{n} - 1 \]")


def r27(x, y, z, n=0, names=("oranges", "apples", "mangoes")):
    base = (x + 1) * (y + 1) * (z + 1)
    v = base * 2 ** n - 1
    lines = [rf"{nm}: take \(0, 1, \ldots, {k}\) of the alike {nm}, \({k + 1}\) ways" for nm, k in zip(names, (x, y, z))]
    if n:
        lines.append(rf"each of the \({n}\) different fruits: take it or leave it, \(2^{{{n}}} = {2 ** n}\) ways")
    trad = steps(
        ("Count the choices for each kind.", "<br>".join(lines)),
        ("Multiply.", D(times(x + 1, y + 1, z + 1, *([f"2^{{{n}}}"] if n else [])) + f" = {base * 2 ** n}")),
        ("Remove the empty selection.", "Taking nothing of every kind is not a selection of fruits." + D(f"{base * 2 ** n} - 1 = {v}")))
    expr = f"({x}+1)({y}+1)({z}+1)" + (rf"\times 2^{{{n}}}" if n else "") + " - 1"
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\), \(y = {y}\), \(z = {z}\), \(n = {n}\)."),
        ("Apply the specified rule.", D(r"(x+1)(y+1)(z+1)\times 2^{n} - 1")),
        ("Substitute the values.", D(f"{expr} = {base * 2 ** n} - 1 = {v}")))
    rb = [rf"\(x = {x}\), \(y = {y}\), \(z = {z}\), \(n = {n}\).", r"Ways \(= (x+1)(y+1)(z+1)\times 2^{n} - 1\).", rf"\({expr} = {v}\)."]
    return result(num(v), T27, trad, rule, I(v), rb, D(f"{expr} = {v}"))


# ---------------------------------------------------------------- Rule 28 (book C15): divide equally
T28 = (r"The number of ways in which \(n\times m\) different things can be divided equally among \(n\) persons is<br>"
       r"\[ \frac{(nm)!}{(m!)^{n}} \]If they are divided into \(n\) equal groups (the groups not named), it is \(\frac{(nm)!}{(m!)^{n}\times n!}\).")


def r28(n, m, groups=False):
    N = n * m
    v = factorial(N) // factorial(m) ** n
    if groups:
        v //= factorial(n)
    expr = rf"\frac{{{N}!}}{{({m}!)^{{{n}}}" + (rf"\times {n}!" if groups else "") + "}"
    picks = [nC(N - i * m, m) for i in range(n)]
    trad = steps(
        ("Give out the things one share at a time.", rf"The 1st share takes \({m}\) of the \({N}\) things, the 2nd \({m}\) of the remaining \({N - m}\), and so on:"
         + D(times(*picks) + rf" = \frac{{{N}!}}{{{m}!\,{N - m}!}}\times \frac{{{N - m}!}}{{{m}!\,{N - 2 * m}!}}\times\cdots = \frac{{{N}!}}{{({m}!)^{{{n}}}}}")),
        *((("The groups have no names.", rf"Here the \({n}\) groups are not given to named persons, so the \({n}!\) orders of the same groups are one division:"
            + D(rf"\frac{{{N}!}}{{({m}!)^{{{n}}}\times {n}!}}")),) if groups else ()),
        ("Read the value.", D(f"{expr} = {v}") if v < 10 ** 12 else D(expr)))
    rule = steps(
        ("Identify the values.", rf"\(nm = {N}\) things, \(n = {n}\) {'groups' if groups else 'persons'}, \(m = {m}\) each."),
        ("Apply the specified rule.", D(r"\frac{(nm)!}{(m!)^{n}\times n!}" if groups else r"\frac{(nm)!}{(m!)^{n}}")),
        ("Substitute the values.", D(expr)))
    rb = [rf"\(nm = {N}\), \(n = {n}\), \(m = {m}\).", r"Ways \(= \frac{(nm)!}{(m!)^{n}" + (r"\times n!" if groups else "") + r"}\).", rf"\({expr}\)" + (rf" \(= {v}\)." if v < 10 ** 12 else ".")]
    return result(num(v), T28, trad, rule, fin(expr, v) if v < 10 ** 12 else I(expr), rb, D(expr))


# ---------------------------------------------------------------- Rule 29 (book C16): identical things among persons
T29 = (r"The number of ways to distribute \(n\) identical things among \(r\) persons, when any person may get any number of "
       r"things (also none), is<br>\[ {}^{n+r-1}C_{r-1} \]")


def r29(n, r, things, persons):
    v = comb(n + r - 1, r - 1)
    trad = steps(
        ("Write a distribution as a row of symbols.", rf"Put the \({n}\) identical {things} in a row and add \({r} - 1 = {r - 1}\) bars between them; the {things} before the first bar go to the "
                                                      rf"1st of the {persons}, those between the 1st and 2nd bar to the 2nd, and so on. Every distribution is one such row."),
        ("Count the rows.", rf"A row has \({n} + {r - 1} = {n + r - 1}\) places; choose which \({r - 1}\) of them hold the bars:"
         + D(rf"\frac{{{falling_tex(n + r - 1, r - 1)}}}{{{r - 1}!}} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) identical {things}, \(r = {r}\) {persons}."),
        ("Apply the specified rule.", D(r"{}^{n+r-1}C_{r-1}")),
        ("Substitute the values.", D(rf"{nC(f'{n}+{r}-1', f'{r}-1')} = {nC(n + r - 1, r - 1)} = {v}")))
    rb = [rf"\(n = {n}\), \(r = {r}\).", r"Ways \(= {}^{n+r-1}C_{r-1}\).", rf"\({nC(n + r - 1, r - 1)} = {v}\)."]
    return result(num(v), T29, trad, rule, fin(nC(n + r - 1, r - 1), v), rb, D(rf"{nC(n + r - 1, r - 1)} = {v}"))


# ---------------------------------------------------------------- cards
CARDS = {
    22: card(22, "Lines through Points with Some Collinear",
             r"There are \(n\) points in a plane, of which \(m\) are collinear (no other three are). The number of straight lines formed by "
             r"joining them is \({}^{n}C_{2} - {}^{m}C_{2} + 1\).",
             r"\[ {}^{n}C_{2} - {}^{m}C_{2} + 1 \]",
             [("All pairs", r"{}^{n}C_{2}"), ("Pairs on the line", r"{}^{m}C_{2}"), ("They give one line", "+1")],
             r"Every pair of points fixes a line, but all the pairs taken from the collinear points lie on the same single line.",
             r"'\(n\) points of which \(m\) are collinear, find the number of straight lines'.",
             r"10 points, 4 collinear: \(45 - 6 + 1 = 40\).",
             r"Forgetting the \(+1\) (the collinear points still give one line), or subtracting \({}^{m}C_{3}\) (that is for triangles)."),
    23: card(23, "Cards Sent to Every Other Student",
             r"On a new year day every student of a class sends a card to every other student. If \(C\) cards are delivered, the number of students "
             r"\(n\) satisfies \(n(n-1) = C\) (that is \(2\times {}^{n}C_{2} = C\)).",
             r"\[ n(n-1) = C \]",
             [("Students", "n"), ("Cards one student sends", "n-1"), ("Cards", r"n(n-1) = 2\times {}^{n}C_{2}")],
             r"Each pair of students exchanges TWO cards (A to B and B to A), unlike a handshake.",
             r"'Every student sends a card (greeting, message) to every other', 'the postman delivers \(C\) cards'.",
             r"600 cards: \(n(n-1) = 600 = 25\times 24\), so \(n = 25\).",
             r"Using \(\frac{n(n-1)}{2}\) as for handshakes."),
    24: card(24, "Ways to Fail in an Examination",
             r"If a minimum is to be secured in each of \(n\) subjects for a pass, the number of ways a student can fail is \(2^{n} - 1\).",
             r"\[ {}^{n}C_{1} + {}^{n}C_{2} + \cdots + {}^{n}C_{n} = 2^{n} - 1 \]",
             [("Subjects", "n"), ("Each subject", r"\text{pass or fail: } 2"), ("All outcomes", "2^{n}"), ("Fail", "2^{n} - 1")],
             r"A student fails in one or more subjects: any non-empty set of subjects. Of the \(2^{n}\) pass/fail patterns only 'pass in all' is not a failure.",
             r"'A minimum is to be secured in each of \(n\) subjects', 'in how many ways can a student fail'.",
             r"5 subjects: \(2^{5} - 1 = 31\).",
             r"Answering \(2^{n}\) (forgetting to remove the all-pass case) or \(n\)."),
    25: card(25, "Solving One or More Questions",
             r"If there are \(n\) questions in a paper, the number of ways in which a student can solve one or more of them is \(2^{n} - 1\). "
             r"The same count gives 'invite one or more of \(n\) friends'.",
             r"\[ {}^{n}C_{1} + {}^{n}C_{2} + \cdots + {}^{n}C_{n} = 2^{n} - 1 \]",
             [("Questions", "n"), ("Each question", r"\text{attempt or not: } 2"), ("All choices", "2^{n}"), ("One or more", "2^{n} - 1")],
             r"Each question is attempted or not; only the choice 'none at all' is not 'one or more'.",
             r"'Solve one or more questions', 'invite one or more friends', 'select at least one of \(n\) different things'.",
             r"6 questions: \(2^{6} - 1 = 63\).",
             r"Using \(2^{n}\) (the empty choice is not allowed) or \(n!\)."),
    26: card(26, "Exactly r Persons from One Group",
             r"From \(x\) persons of group A and \(y\) persons of group B, the number of ways of choosing \(n\) persons with exactly \(r\) from group A "
             r"is \({}^{x}C_{r}\times {}^{y}C_{n-r}\). For 'at least' add these cases (or subtract the unwanted ones from the total).",
             r"\[ {}^{x}C_{r}\times {}^{y}C_{n-r} \]",
             [("Group A", "x"), ("Group B", "y"), ("Exactly r from A", r"{}^{x}C_{r}"), ("The rest from B", r"{}^{y}C_{n-r}")],
             r"The two choices are independent: every choice from A goes with every choice from B, so the counts multiply.",
             r"'From 4 officers and 8 jawans choose 6 with exactly one officer', 'a committee of 5 men and 6 women from 8 men and 10 women', "
             r"'at least one boy' (add the cases).",
             r"4 officers, 8 jawans, 6 with exactly 1 officer: \({}^{4}C_{1}\times {}^{8}C_{5} = 4\times 56 = 224\).",
             r"Adding instead of multiplying, or for 'at least one' using \({}^{x}C_{1}\times {}^{x+y-1}C_{n-1}\), which counts some groups many times."),
    27: card(27, "Selecting Fruits of Alike Kinds",
             r"A basket has \(x\) oranges, \(y\) apples, \(z\) mangoes (fruits of the same kind are alike) and \(n\) other fruits of different kinds. "
             r"The number of ways of making a selection (at least one fruit) is \((x+1)(y+1)(z+1)\times 2^{n} - 1\).",
             r"\[ (x+1)(y+1)(z+1)\times 2^{n} - 1 \]",
             [("Oranges", "x+1 \\text{ choices } (0 \\text{ to } x)"), ("Apples", "y+1"), ("Mangoes", "z+1"), ("Different fruits", "2^{n}")],
             r"From alike things you only decide HOW MANY to take (\(0\) to \(x\)); each different fruit is taken or not; remove the empty selection.",
             r"'Selection of fruits from a basket', 'any number of alike things', 'at least one'.",
             r"4 oranges, 5 apples, 6 mangoes: \(5\times 6\times 7 - 1 = 209\).",
             r"Treating alike fruits as different (\(2^{x}\) instead of \(x+1\)), or forgetting the \(-1\)."),
    28: card(28, "Dividing Different Things Equally",
             r"The number of ways in which \(n\times m\) different things can be divided equally among \(n\) persons is \(\frac{(nm)!}{(m!)^{n}}\). "
             r"If they are only divided into \(n\) equal sets (not given to named persons), it is \(\frac{(nm)!}{(m!)^{n}\times n!}\).",
             r"\[ \frac{(nm)!}{(m!)^{n}} \]",
             [("Things", "nm"), ("Persons (shares)", "n"), ("Each gets", "m"), ("Unnamed sets", r"\div n!")],
             r"Give out the shares one after another: \({}^{nm}C_{m}\times {}^{nm-m}C_{m}\times\cdots = \frac{(nm)!}{(m!)^{n}}\). With unnamed sets the order of the sets does not matter.",
             r"'Divided equally among 3 persons' (named) or 'divided into three sets each having 4 things' (unnamed).",
             r"12 things among 3 persons: \(\frac{12!}{(4!)^{3}}\); into 3 sets: \(\frac{12!}{(4!)^{3}\times 3!}\).",
             r"Dividing by \(n!\) when the shares go to named persons, or not dividing when the sets have no names."),
    29: card(29, "Identical Things among Persons",
             r"The number of ways to distribute \(n\) identical things among \(r\) persons, when any person may get any number of things (also none), is "
             r"\({}^{n+r-1}C_{r-1}\).",
             r"\[ {}^{n+r-1}C_{r-1} \]",
             [("Identical things", "n"), ("Persons", "r"), ("Dividers", "r-1"), ("Ways", r"{}^{n+r-1}C_{r-1}")],
             r"Line up the \(n\) things and \(r-1\) dividers; every arrangement of them is one distribution, and it is fixed by where the dividers stand.",
             r"'\(n\) apples (bananas, oranges) divided among \(r\) boys (girls)' with no rule that each must get one.",
             r"20 apples among 5 boys: \({}^{24}C_{4} = 10626\).",
             r"Using \(r^{n}\) (that is for different things), or \({}^{n-1}C_{r-1}\) (that is when every person must get at least one)."),
}

OLD = {
    22: {862: (lambda: r22(10, 4), "There are 10 points in a plane out of which 4 are collinear. Find the number of straight lines formed by joining them.",
               {"c": "40"})},
    23: {863: (lambda: r23_find(600), "On a new year day every student of a class sends a card to every other student. The postman delivers 600 cards. "
                                      "How many students are there in the class?", None)},
    24: {864: (lambda: r24(5), "In an examination a minimum is to be secured in each of 5 subjects for a pass. In how many ways can a student fail?", None)},
    25: {865: (lambda: r25(6), "There are 6 questions in a question paper. In how many ways can a student solve one or more questions?", None),
         877: (lambda: r25(5, "friend", "Inviting nobody is not 'one or more', so that case is removed."),
               "Kavita has 5 friends. In how many ways can she invite one or more of them to a dinner?", None)},
    26: {866: (lambda: r26(4, 8, 6, 1, "officers", "jawans"), "From 4 officers and 8 jawans, in how many ways can 6 be chosen to include exactly one officer?", None),
         879: (lambda: r26_words(7, 4, 3, 2), None, None),
         880: (lambda: r26_at_least(6, 4, 4, "boys", "girls"), None, None),
         883: (lambda: r26(7, 3, 7, 5, "men", "women"), None, None),
         884: (lambda: r26(8, 10, 11, 5, "men", "women"), None, None),
         900: (lambda: r26_one_each([4, 3, 2], ["red", "white", "blue"]), "A box contains 4 red, 3 white and 2 blue balls. Three balls are drawn. "
                                                                         "In how many ways can three balls of different colours be selected?", None)},
    27: {867: (lambda: r27(4, 5, 6), None, None)},
    28: {868: (lambda: r28(3, 4), "In how many ways can 12 different things be divided equally among 3 persons?",
               {"a": r"\(\frac{11!}{(7!)^{3}}\)", "b": r"\(\frac{14!}{(12!)^{3}}\)", "c": r"\(\frac{4!}{(12!)^{3}}\)", "d": r"\(\frac{12!}{(4!)^{3}}\)"})},
    29: {869: (lambda: r29(20, 5, "apples", "boys"), "In how many ways can 20 apples be divided among 5 boys?", None)},
}

NEW = {
    22: [("r22_e1", "There are 11 points in a plane out of which 4 are collinear. Find the number of straight lines formed by joining them.",
          lambda: r22(11, 4), ["55", "49", "50", "51"], 3),
         ("r22_e2", "There are 14 points in a plane out of which 5 are collinear. Find the number of straight lines formed by joining them.",
          lambda: r22(14, 5), ["82", "81", "91", "72"], 1),
         ("r22_e3", "There are 9 points in a plane out of which 3 are collinear. Find the number of straight lines formed by joining them.",
          lambda: r22(9, 3), ["36", "33", "35", "34"], 4)],
    23: [("r23_e1", "On a new year day every student of a class sends a card to every other student. The postman delivers 870 cards. How many students are there in the class?",
          lambda: r23_find(870), ["29", "30", "31", "42"], 2),
         ("r23_e2", "On a new year day every student of a class sends a card to every other student. The postman delivers 1640 cards. How many students are there in the class?",
          lambda: r23_find(1640), ["40", "42", "41", "58"], 3),
         ("r23_e3", "On a new year day every student of a class sends a card to every other student. The postman delivers 702 cards. How many students are there in the class?",
          lambda: r23_find(702), ["27", "26", "28", "38"], 1),
         ("r23_e4", "On a new year day every student of a class sends a card to every other student. If there are 45 students, how many cards does the postman deliver?",
          lambda: r23_count(45), ["990", "2025", "1936", "1980"], 4)],
    24: [("r24_e1", "In an examination a minimum is to be secured in each of 7 subjects for a pass. In how many ways can a student fail?",
          lambda: r24(7), ["128", "127", "49", "7"], 2),
         ("r24_e2", "In an examination a minimum is to be secured in each of 8 subjects for a pass. In how many ways can a student fail?",
          lambda: r24(8), ["255", "256", "64", "511"], 1),
         ("r24_e3", "In an examination a minimum is to be secured in each of 9 subjects for a pass. In how many ways can a student fail?",
          lambda: r24(9), ["512", "1023", "511", "81"], 3),
         ("r24_e4", "In an examination a minimum is to be secured in each of 10 subjects for a pass. In how many ways can a student fail?",
          lambda: r24(10), ["1024", "100", "511", "1023"], 4)],
    25: [("r25_e1", "There are 9 questions in a question paper. In how many ways can a student solve one or more questions?",
          lambda: r25(9), ["511", "512", "1023", "81"], 1),
         ("r25_e2", "There are 10 questions in a question paper. In how many ways can a student solve one or more questions?",
          lambda: r25(10), ["1024", "1023", "100", "2047"], 2),
         ("r25_e3", "There are 3 questions in a question paper. In how many ways can a student solve one or more questions?",
          lambda: r25(3), ["8", "6", "7", "3"], 3),
         ("r25_e4", "There are 12 questions in a question paper. In how many ways can a student solve one or more questions?",
          lambda: r25(12), ["4096", "2047", "144", "4095"], 4)],
    26: [("r26_e1", "From 6 officers and 8 jawans, in how many ways can 5 be chosen to include exactly 2 officers?",
          lambda: r26(6, 8, 5, 2, "officers", "jawans"), ["840", "420", "1680", "896"], 1),
         ("r26_e2", "From 5 officers and 9 jawans, in how many ways can 4 be chosen to include exactly 1 officer?",
          lambda: r26(5, 9, 4, 1, "officers", "jawans"), ["360", "504", "420", "1001"], 3),
         ("r26_e3", "From 7 officers and 10 jawans, in how many ways can 6 be chosen to include exactly 3 officers?",
          lambda: r26(7, 10, 6, 3, "officers", "jawans"), ["3500", "4200", "4800", "12376"], 2)],
    27: [("r27_e1", "There are 3 oranges, 4 apples and 5 mangoes in a fruit basket. In how many ways can a person make a selection of fruits from among the fruits in the basket?",
          lambda: r27(3, 4, 5), ["120", "60", "119", "59"], 3),
         ("r27_e2", "There are 6 oranges, 7 apples and 8 mangoes in a fruit basket. In how many ways can a person make a selection of fruits from among the fruits in the basket?",
          lambda: r27(6, 7, 8), ["503", "504", "335", "336"], 1),
         ("r27_e3", "There are 2 oranges, 5 apples and 6 mangoes in a fruit basket. In how many ways can a person make a selection of fruits from among the fruits in the basket?",
          lambda: r27(2, 5, 6), ["126", "59", "60", "125"], 4),
         ("r27_e4", "In a basket there are 3 oranges, 5 apples, 7 mangoes and the remaining 2 fruits are of different kinds. In how many ways can a person "
                    "make a selection of fruits from among the fruits in the basket?",
          lambda: r27(3, 5, 7, 2), ["191", "767", "768", "383"], 2)],
    28: [("r28_e1", "In how many ways can 10 different things be divided into two sets, each having 5 things?", lambda: r28(2, 5, groups=True),
          [r"\(\frac{10!}{(5!)^{2}}\)", r"\(\frac{10!}{(5!)^{2}\times 2!}\)", r"\(\frac{10!}{5!}\)", r"\(\frac{10!}{(2!)^{5}}\)"], 2),
         ("r28_e2", "In how many ways can 14 different things be divided equally among 7 persons?", lambda: r28(7, 2),
          [r"\(\frac{14!}{(7!)^{2}}\)", r"\(\frac{14!}{(2!)^{7}\times 7!}\)", r"\(\frac{14!}{(2!)^{7}}\)", r"\(\frac{14!}{(2!)^{6}}\)"], 3),
         ("r28_e3", "In how many ways can 16 different things be divided equally among 4 persons?", lambda: r28(4, 4),
          [r"\(\frac{16!}{(4!)^{4}}\)", r"\(\frac{16!}{(4!)^{3}}\)", r"\(\frac{16!}{(4!)^{4}\times 4!}\)", r"\(\frac{16!}{4!}\)"], 1),
         ("r28_e4", "In how many ways can 21 different things be divided equally among 3 persons?", lambda: r28(3, 7),
          [r"\(\frac{21!}{(3!)^{7}}\)", r"\(\frac{21!}{(7!)^{3}\times 3!}\)", r"\(\frac{21!}{7!\times 3!}\)", r"\(\frac{21!}{(7!)^{3}}\)"], 4)],
    29: [("r29_e1", "In how many ways can 10 mangoes be divided among 3 children?", lambda: r29(10, 3, "mangoes", "children"),
          [rf"\({nC(12, 2)}\)", rf"\({nC(10, 2)}\)", rf"\({nC(13, 3)}\)", rf"\({nC(12, 3)}\)"], 1),
         ("r29_e2", "In how many ways can 14 identical pens be divided among 6 students?", lambda: r29(14, 6, "pens", "students"),
          [rf"\({nC(20, 6)}\)", rf"\({nC(14, 5)}\)", rf"\({nC(19, 6)}\)", rf"\({nC(19, 5)}\)"], 4),
         ("r29_e3", "In how many ways can 9 identical balls be divided among 4 boys?", lambda: r29(9, 4, "balls", "boys"),
          [rf"\({nC(13, 4)}\)", rf"\({nC(12, 3)}\)", rf"\({nC(9, 3)}\)", rf"\({nC(12, 4)}\)"], 2)],
}


def main():
    gen_1_7.OLD, gen_1_7.NEW, gen_1_7.CARDS = OLD, NEW, CARDS
    gen_1_7.main(range(22, 30))


if __name__ == "__main__":
    main()
