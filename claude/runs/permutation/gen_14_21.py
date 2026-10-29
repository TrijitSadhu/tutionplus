"""Rules 14-21 (book II. Combinations, Rules 1-8; site number = book number + 13): writes the eight rule cards,
regenerates the old rows in the prompt #13 layout and links them, and adds the book's worked examples and exercises that had
no copy (numbers changed). Fixes: 905 (no option held 25, key on the empty option e), 875 (the number of students was lost:
15 gives the stored answer 90), 855 ('10 identical boxes' -> '10 different boxes', as the answer 252 needs; the book has the
same slip). Rule 18 Exr 2 (a figure) is written as a rectangle cut by stated numbers of lines. Rule 20 Exr 2 and 3 have wrong
book answers; the new versions use other numbers and the right answers. Same outputs as gen_1_7.py."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, steps  # noqa: E402
from pc_common import D, I, comb, factorial, falling_tex, fin, nC, num, result, times  # noqa: E402
import gen_1_7  # noqa: E402


def pair(a, b):
    return ("pair", (a, b))


def ctex(n, r):
    """{}^{n}C_{r} = \\frac{n(n-1)...}{r!} = value."""
    if r == 0:
        return rf"{nC(n, 0)} = 1"
    return rf"{nC(n, r)} = \frac{{{falling_tex(n, r)}}}{{{r}!}} = {comb(n, r)}" if r > 1 else rf"{nC(n, 1)} = {n}"


def choose_trad(n, r, things):
    """First-principles count of r-selections from n: ordered picks / orders of the same group."""
    if r == 1:
        return ("Pick one.", rf"Any one of the \({n}\) {things}: \({n}\) ways.")
    return ("Pick them one at a time, then forget the order.",
            rf"Picking \({r}\) of the \({n}\) {things} one after another gives \({falling_tex(n, r)}\) ordered picks, but each group of \({r}\) "
            rf"is picked in \({r}! = {factorial(r)}\) different orders:" + D(rf"\frac{{{falling_tex(n, r)}}}{{{factorial(r)}}} = {comb(n, r)}"))


# ---------------------------------------------------------------- Rule 14 (book C1): nCr directly
T14 = (r"\[ {}^{n}C_{r} = \frac{n!}{r!\,(n-r)!} \]<br>\[ {}^{n}C_{r-1} + {}^{n}C_{r} = {}^{n+1}C_{r} \]<br>"
       r"If \({}^{n}C_{x} = {}^{n}C_{y}\), then either \(x = y\) or \(x + y = n\).")


def r14_equal(n, a, b, c, d):
    """nC(a r + b) = nC(c r + d): find r (the case x = y gives no whole number)."""
    from fractions import Fraction as Fr
    r_same = Fr(d - b, a - c) if a != c else None
    r = Fr(n - b - d, a + c)
    assert r.denominator == 1 and (r_same is None or r_same.denominator != 1)
    r = int(r)
    x, y = a * r + b, c * r + d
    if r_same is not None:
        r_same = rf"\frac{{{r_same.numerator}}}{{{r_same.denominator}}}"
    lx = (f"{a}r" if a != 1 else "r") + (f" + {b}" if b else "")
    ly = (f"{c}r" if c != 1 else "r") + (f" + {d}" if d else "")
    trad = steps(
        ("Use the meaning of a selection.", rf"Choosing \(k\) of \({n}\) things is the same as choosing the \({n} - k\) that are left out, "
                                            rf"so \({nC(n, 'k')}\) and \({nC(n, f'{n}-k')}\) count the same groups. Two different selection sizes give the same count only in that case."),
        ("Try equal sizes.", rf"\({lx} = {ly}\) gives \(r = {r_same}\), which is not a whole number." if r_same is not None else "The two sizes can not be equal."),
        ("Use the left-out sizes.", rf"\(({lx}) + ({ly}) = {n}\) gives \({a + c}r + {b + d} = {n}\), so \(r = {r}\) (sizes \({x}\) and \({y}\), and \({x} + {y} = {n}\))."))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\), \(x = {lx}\), \(y = {ly}\)."),
        ("Apply the specified rule.", r"If \({}^{n}C_{x} = {}^{n}C_{y}\), then \(x = y\) or \(x + y = n\)."),
        ("Substitute the values.", rf"\({lx} = {ly}\) gives \(r = {r_same}\) (not possible); \({lx} + {ly} = {n}\) gives \(r = {r}\)."))
    rb = [rf"\(n = {n}\), \(x = {lx}\), \(y = {ly}\).", r"\(x = y\) or \(x + y = n\).", rf"\(x + y = {n}\Rightarrow r = {r}\)."]
    return result(num(r), T14, trad, rule, I(f"r = {r}"), rb, D(rf"{lx} + {ly} = {n} \Rightarrow r = {r}"))


def r14_ratio(r1, k, r2, p, q):
    """nC(r1) : (n-k)C(r2) = p : q, find n (try n upward)."""
    n = next(n for n in range(max(r1, k + r2), 200) if comb(n, r1) * q == comb(n - k, r2) * p)
    trad = steps(
        ("Write both counts as products.", rf"\({nC('n', r1)}\) and \({nC(f'n-{k}', r2)}\) are 'picks in order divided by the orders':"
         + D(rf"{nC('n', r1)} = \frac{{n(n-1)\cdots(n-{r1 - 1})}}{{{r1}!}},\qquad {nC(f'n-{k}', r2)} = \frac{{(n-{k})(n-{k + 1})\cdots(n-{k + r2 - 1})}}{{{r2}!}}")),
        ("Cancel the common factors.", rf"The factors \((n-{k})\cdots(n-{r1 - 1})\) appear in both, so the ratio is"
         + D(rf"\frac{{{''.join('n' if i == 0 else f'(n-{i})' for i in range(k))}\times {r2}!}}{{{r1}!}} = \frac{{{p}}}{{{q}}}")),
        ("Solve.", rf"With \(n = {n}\): \(\frac{{{times(*range(n, n - k, -1))}\times {factorial(r2)}}}{{{factorial(r1)}}} = \frac{{{p}}}{{{q}}}\) ✓, so \(n = {n}\)."))
    rule = steps(
        ("Identify the values.", rf"\({nC('n', r1)} : {nC(f'n-{k}', r2)} = {p} : {q}\)."),
        ("Apply the specified rule.", D(r"{}^{n}C_{r} = \frac{n!}{r!\,(n-r)!}")),
        ("Substitute the values.", D(rf"\frac{{n!}}{{{r1}!\,(n-{r1})!}}\times \frac{{{r2}!\,(n-{k + r2})!}}{{(n-{k})!}} = \frac{{{p}}}{{{q}}} \Rightarrow n = {n}")
         + rf"Check: \({nC(n, r1)} = {comb(n, r1)}\), \({nC(n - k, r2)} = {comb(n - k, r2)}\), ratio \({comb(n, r1)} : {comb(n - k, r2)} = {p} : {q}\)."))
    rb = [rf"\({nC('n', r1)} : {nC(f'n-{k}', r2)} = {p} : {q}\).", r"\({}^{n}C_{r} = \frac{n!}{r!\,(n-r)!}\); cancel and solve.",
          rf"\(n = {n}\): \({comb(n, r1)} : {comb(n - k, r2)} = {p} : {q}\)."]
    return result(num(n), T14, trad, rule, I(f"n = {n}"), rb, D(rf"{nC(n, r1)} : {nC(n - k, r2)} = {comb(n, r1)} : {comb(n - k, r2)} = {p} : {q} \Rightarrow n = {n}"))


# ---------------------------------------------------------------- Rule 15 (book C2): simple selections
T15 = (r"The number of combinations (selections, groups) of \(n\) different things taken \(r\) at a time is<br>"
       r"\[ {}^{n}C_{r} = \frac{n!}{r!\,(n-r)!} = \frac{n(n-1)\cdots(n-r+1)}{r!} \]")


def r15(n, r, things, how=""):
    v = comb(n, r)
    trad = steps(choose_trad(n, r, things), *((("Read the answer.", how),) if how else ()))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) {things}, choose \(r = {r}\)."),
        ("Apply the specified rule.", D(r"{}^{n}C_{r} = \frac{n!}{r!\,(n-r)!}")),
        ("Substitute the values.", D(ctex(n, r))))
    rb = [rf"\(n = {n}\), \(r = {r}\).", r"\({}^{n}C_{r} = \frac{n!}{r!\,(n-r)!}\).", rf"\({ctex(n, r)}\)."]
    return result(num(v), T15, trad, rule, I(v), rb, D(ctex(n, r)))


def r15_or(a, b, A, B):
    v = a + b
    trad = steps(
        ("List the choices.", rf"The person is either one of the \({a}\) {A} or one of the \({b}\) {B}; these two lists do not overlap."),
        ("Add.", D(f"{a} + {b} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {a} + {b} = {v}\) persons in all, choose \(r = 1\)."),
        ("Apply the specified rule.", D(r"{}^{n}C_{r} = \frac{n!}{r!\,(n-r)!}")),
        ("Substitute the values.", D(rf"{nC(v, 1)} = {v}")))
    rb = [rf"\(n = {v}\), \(r = 1\).", r"\({}^{n}C_{1} = n\).", rf"\({nC(v, 1)} = {v}\)."]
    return result(num(v), T15, trad, rule, I(v), rb, D(rf"{nC(v, 1)} = {v}"))


# ---------------------------------------------------------------- Rule 16 (book C3): triangles from a polygon
T16 = r"The number of triangles that can be formed by joining the vertices of a polygon of \(m\) sides is<br>\[ \frac{m(m-1)(m-2)}{6} \]"


def r16(m):
    v = comb(m, 3)
    trad = steps(
        ("A triangle is three vertices.", rf"No three vertices of a polygon lie on one line, so any \(3\) of the \({m}\) vertices make a triangle."),
        choose_trad(m, 3, "vertices"))
    rule = steps(
        ("Identify the value.", rf"\(m = {m}\) sides."),
        ("Apply the specified rule.", D(r"\frac{m(m-1)(m-2)}{6}")),
        ("Substitute the value.", D(rf"\frac{{{m}\times {m - 1}\times {m - 2}}}{{6}} = {v}")))
    rb = [rf"\(m = {m}\).", r"Triangles \(= \frac{m(m-1)(m-2)}{6}\).", rf"\(\frac{{{m}\times {m - 1}\times {m - 2}}}{{6}} = {v}\)."]
    return result(num(v), T16, trad, rule, I(v), rb, D(rf"\frac{{{m}\times {m - 1}\times {m - 2}}}{{6}} = {v}"))


# ---------------------------------------------------------------- Rule 17 (book C4): diagonals
T17 = r"The number of diagonals of a polygon of \(m\) sides is<br>\[ \frac{m(m-3)}{2} \]"


def r17(m, circle=False):
    v = m * (m - 3) // 2
    if circle:
        trad = steps(
            ("Count the handshakes of one person.", rf"Each of the \({m}\) people shakes hands with everyone except himself and his two neighbours: \({m} - 3 = {m - 3}\) handshakes."),
            ("Every handshake is counted twice.", rf"Adding over all \({m}\) people counts each handshake once for each of the two people:" + D(rf"\frac{{{m}\times {m - 3}}}{{2}} = {v}")))
        what = rf"the \({m}\) people are the vertices of a polygon and a handshake between non-neighbours is a diagonal"
    else:
        trad = steps(
            ("Count the diagonals at one vertex.", rf"From a vertex, lines go to the other \({m - 1}\) vertices; \(2\) of them are sides, so \({m} - 3 = {m - 3}\) are diagonals."),
            ("Every diagonal is counted twice.", rf"Adding over all \({m}\) vertices counts each diagonal from both ends:" + D(rf"\frac{{{m}\times {m - 3}}}{{2}} = {v}")))
        what = rf"\(m = {m}\) sides"
    rule = steps(
        ("Identify the value.", what[0].upper() + what[1:] + (rf", so \(m = {m}\)." if circle else ".")),
        ("Apply the specified rule.", D(r"\frac{m(m-3)}{2}")),
        ("Substitute the value.", D(rf"\frac{{{m}\times ({m}-3)}}{{2}} = \frac{{{m}\times {m - 3}}}{{2}} = {v}")))
    rb = [rf"\(m = {m}\).", r"Diagonals \(= \frac{m(m-3)}{2}\).", rf"\(\frac{{{m}\times {m - 3}}}{{2}} = {v}\)."]
    return result(num(v), T17, trad, rule, I(v), rb, D(rf"\frac{{{m}\times {m - 3}}}{{2}} = {v}"))


# ---------------------------------------------------------------- Rule 18 (book C5): rectangles from two sets of lines
T18 = r"If there are \(m\) horizontal and \(n\) vertical lines, the number of different rectangles formed is<br>\[ {}^{m}C_{2}\times {}^{n}C_{2} \]"


def r18(m, n, mname="horizontal", nname="vertical", note=""):
    a, b = comb(m, 2), comb(n, 2)
    v = a * b
    trad = steps(
        ("A rectangle is fixed by its sides.", rf"Its top and bottom come from the {mname} lines and its left and right sides from the {nname} lines." + note),
        ("Choose the two " + mname + " lines.", rf"Pair each of the \({m}\) lines with each other one: \(\frac{{{m}\times {m - 1}}}{{2}} = {a}\) pairs."),
        ("Choose the two " + nname + " lines.", rf"\(\frac{{{n}\times {n - 1}}}{{2}} = {b}\) pairs."),
        ("Multiply.", D(f"{a}\\times {b} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(m = {m}\) {mname} lines, \(n = {n}\) {nname} lines."),
        ("Apply the specified rule.", D(r"{}^{m}C_{2}\times {}^{n}C_{2}")),
        ("Substitute the values.", D(rf"{nC(m, 2)}\times {nC(n, 2)} = {a}\times {b} = {v}")))
    rb = [rf"\(m = {m}\), \(n = {n}\).", r"Rectangles \(= {}^{m}C_{2}\times {}^{n}C_{2}\).", rf"\({nC(m, 2)}\times {nC(n, 2)} = {a}\times {b} = {v}\)."]
    return result(num(v), T18, trad, rule, I(v), rb, D(rf"{nC(m, 2)}\times {nC(n, 2)} = {v}"))


# ---------------------------------------------------------------- Rule 19 (book C6): handshakes
T19 = (r"In a party every person shakes hands with every other person. If there are \(H\) handshakes in all, the number of "
       r"persons \(n\) is found from<br>\[ \frac{n(n-1)}{2} = H \]")


def r19_find(H):
    n = next(n for n in range(2, 500) if n * (n - 1) // 2 == H)
    trad = steps(
        ("Count the handshakes for \\(n\\) persons.", r"Each person shakes \(n-1\) hands; adding over all \(n\) persons counts every handshake twice, so there are \(\frac{n(n-1)}{2}\) handshakes."),
        ("Form the equation.", D(rf"\frac{{n(n-1)}}{{2}} = {H}\ \Rightarrow\ n(n-1) = {2 * H} = {n}\times {n - 1}")),
        ("Read off n.", rf"\(n = {n}\) (the negative root \(n = -{n - 1}\) is impossible)."))
    rule = steps(
        ("Identify the value.", rf"\(H = {H}\)."),
        ("Apply the specified rule.", D(r"\frac{n(n-1)}{2} = H")),
        ("Substitute and solve.", D(rf"n(n-1) = {2 * H} \Rightarrow n^{{2}} - n - {2 * H} = 0 \Rightarrow (n - {n})(n + {n - 1}) = 0") + rf"\(n = {n}\)."))
    rb = [rf"\(H = {H}\).", r"\(\frac{n(n-1)}{2} = H\).", rf"\(n(n-1) = {2 * H} = {n}\times {n - 1}\), so \(n = {n}\)."]
    return result(num(n), T19, trad, rule, I(n), rb, D(rf"n(n-1) = {2 * H} = {n}\times {n - 1} \Rightarrow n = {n}"))


def r19_count(n):
    H = n * (n - 1) // 2
    trad = steps(
        ("Count one person's handshakes.", rf"Each of the \({n}\) persons shakes hands with the other \({n - 1}\)."),
        ("Every handshake is counted twice.", rf"Adding over all persons counts each handshake once for each of the two people:" + D(rf"\frac{{{n}\times {n - 1}}}{{2}} = {H}")))
    rule = steps(
        ("Identify the value.", rf"\(n = {n}\) persons."),
        ("Apply the specified rule.", D(r"H = \frac{n(n-1)}{2}")),
        ("Substitute the value.", D(rf"\frac{{{n}\times ({n}-1)}}{{2}} = \frac{{{n}\times {n - 1}}}{{2}} = {H}")))
    rb = [rf"\(n = {n}\).", r"\(H = \frac{n(n-1)}{2}\).", rf"\(\frac{{{n}\times {n - 1}}}{{2}} = {H}\)."]
    return result(num(H), T19, trad, rule, I(H), rb, D(rf"\frac{{{n}\times {n - 1}}}{{2}} = {H}"))


# ---------------------------------------------------------------- Rule 20 (book C7): particular members included / excluded
T20 = (r"\(m\) members are to be selected from \(n\). The number of selections in which \(r\) particular members are always<br>"
       r"(i) included is \[ {}^{n-r}C_{m-r} \] (ii) excluded is \[ {}^{n-r}C_{m} \]")


def r20(n, m, r, both=True, what="members"):
    inc, exc = comb(n - r, m - r), comb(n - r, m)
    who = "the particular member" if r == 1 else f"the {r} particular {what}"
    trad = steps(
        (f"(i) {who.capitalize()} included.", rf"Put {who} in first. The other \({m} - {r} = {m - r}\) places are filled from the \({n} - {r} = {n - r}\) others:"
         + D(rf"\frac{{{falling_tex(n - r, m - r)}}}{{{m - r}!}} = {inc}")),
        *(((f"(ii) {who.capitalize()} excluded.", rf"Leave {who} out. All \({m}\) are chosen from the \({n - r}\) others:"
            + D(rf"\frac{{{falling_tex(n - r, m)}}}{{{m}!}} = {exc}")),) if both else ()))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\), \(m = {m}\) to select, \(r = {r}\) particular {what}."),
        ("Apply the specified rule.", r"(i) \({}^{n-r}C_{m-r}\)" + (r"; (ii) \({}^{n-r}C_{m}\)." if both else ".")),
        ("Substitute the values.", D(rf"{nC(n - r, m - r)} = {inc}" + (rf",\qquad {nC(n - r, m)} = {exc}" if both else ""))))
    rb = [rf"\(n = {n}\), \(m = {m}\), \(r = {r}\).", r"Included \({}^{n-r}C_{m-r}\)" + (r", excluded \({}^{n-r}C_{m}\)." if both else "."),
          rf"\({nC(n - r, m - r)} = {inc}\)" + (rf" and \({nC(n - r, m)} = {exc}\)." if both else ".")]
    if both:
        return result(pair(inc, exc), T20, trad, rule, I(inc) + " and " + I(exc), rb, D(rf"{nC(n - r, m - r)} = {inc},\quad {nC(n - r, m)} = {exc}"))
    return result(num(inc), T20, trad, rule, I(inc), rb, D(rf"{nC(n - r, m - r)} = {inc}"))


# ---------------------------------------------------------------- Rule 21 (book C8): triangles with collinear points
T21 = (r"There are \(n\) points in a plane, of which \(m\) are collinear (and no other three are). The number of triangles "
       r"formed with the points as vertices is<br>\[ {}^{n}C_{3} - {}^{m}C_{3} \]")


def r21(n, m):
    a, b = comb(n, 3), comb(m, 3)
    v = a - b
    trad = steps(
        ("Pretend no three points are collinear.", "Any three points would then make a triangle:" + D(rf"\frac{{{falling_tex(n, 3)}}}{{6}} = {a}")),
        ("Remove the triples on the line.", rf"Three of the \({m}\) collinear points lie on one line and make no triangle:" + D(rf"\frac{{{falling_tex(m, 3)}}}{{6}} = {b}")),
        ("Subtract.", D(f"{a} - {b} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) points, \(m = {m}\) collinear."),
        ("Apply the specified rule.", D(r"{}^{n}C_{3} - {}^{m}C_{3}")),
        ("Substitute the values.", D(rf"{nC(n, 3)} - {nC(m, 3)} = {a} - {b} = {v}")))
    rb = [rf"\(n = {n}\), \(m = {m}\).", r"Triangles \(= {}^{n}C_{3} - {}^{m}C_{3}\).", rf"\({a} - {b} = {v}\)."]
    return result(num(v), T21, trad, rule, I(v), rb, D(rf"{nC(n, 3)} - {nC(m, 3)} = {v}"))


# ---------------------------------------------------------------- cards
CARDS = {
    14: card(14, "Combinations: Direct Use of nCr",
             r"The number of selections of \(r\) things from \(n\) different things is \({}^{n}C_{r}\). Two useful facts: "
             r"\({}^{n}C_{r-1} + {}^{n}C_{r} = {}^{n+1}C_{r}\), and if \({}^{n}C_{x} = {}^{n}C_{y}\) then \(x = y\) or \(x + y = n\).",
             r"\[ {}^{n}C_{r} = \frac{n!}{r!\,(n-r)!} \]",
             [("Selections", r"{}^{n}C_{r}"), ("Same as leaving out", r"{}^{n}C_{n-r}"), ("Pascal", r"{}^{n}C_{r-1} + {}^{n}C_{r} = {}^{n+1}C_{r}"), ("Equal values", r"x = y \text{ or } x + y = n")],
             r"Choosing \(r\) things is the same as choosing the \(n-r\) that are left out, so \({}^{n}C_{r} = {}^{n}C_{n-r}\); that is why equal values need \(x = y\) or \(x + y = n\).",
             r"Equations such as \({}^{15}C_{3r} = {}^{15}C_{r+3}\), or a ratio of two \(C\)'s: write both as products, cancel, and solve.",
             r"\({}^{15}C_{3r} = {}^{15}C_{r+3}\): \(3r = r+3\) gives \(r = \frac{3}{2}\) (no), so \(3r + r + 3 = 15\) and \(r = 3\).",
             r"Stopping at \(x = y\) when it gives no whole number; or confusing \({}^{n}C_{r}\) with \({}^{n}P_{r} = r!\times {}^{n}C_{r}\)."),
    15: card(15, "Simple Combinations",
             r"The number of ways of selecting \(r\) things out of \(n\) different things (order does not matter) is \({}^{n}C_{r}\). "
             r"Selecting \(r\) of \(n\) boxes for identical balls, one ball per box, is also \({}^{n}C_{r}\).",
             r"\[ {}^{n}C_{r} = \frac{n!}{r!\,(n-r)!} \]",
             [("Different things", "n"), ("To choose", "r"), ("Ordered picks", r"{}^{n}P_{r}"), ("Groups", r"{}^{n}C_{r} = \frac{{}^{n}P_{r}}{r!}")],
             r"Counting ordered picks gives \({}^{n}P_{r}\); each group of \(r\) appears in \(r!\) orders, so divide by \(r!\).",
             r"'Committee', 'group', 'team', 'choose \(r\) questions', 'select'. If the order of choosing does not matter, it is a combination.",
             r"A group of 6 from 8 men and 7 women: \({}^{15}C_{6} = 5005\).",
             r"Using \({}^{n}P_{r}\) for a committee (order does not matter), or multiplying when the choice is 'this OR that' (then add)."),
    16: card(16, "Triangles from the Vertices of a Polygon",
             r"The number of triangles formed by joining the vertices of a polygon of \(m\) sides is \({}^{m}C_{3} = \frac{m(m-1)(m-2)}{6}\).",
             r"\[ \frac{m(m-1)(m-2)}{6} \]",
             [("Vertices", "m"), ("A triangle", r"3 \text{ vertices}"), ("Triangles", r"{}^{m}C_{3}")],
             r"No three vertices of a polygon are on one line, so every choice of 3 vertices gives exactly one triangle.",
             r"'Triangles formed by joining the vertices (angular points) of a hexagon / octagon / polygon of \(m\) sides'.",
             r"Polygon of 12 sides: \(\frac{12\times 11\times 10}{6} = 220\).",
             r"Dividing by 2 instead of 6 (that is for lines), or counting only triangles with a side on the polygon."),
    17: card(17, "Diagonals of a Polygon",
             r"The number of diagonals of a polygon of \(m\) sides is \(\frac{m(m-3)}{2}\), that is \({}^{m}C_{2} - m\).",
             r"\[ \frac{m(m-3)}{2} \]",
             [("Lines joining vertices", r"{}^{m}C_{2}"), ("Sides", "m"), ("Diagonals", r"{}^{m}C_{2} - m = \frac{m(m-3)}{2}")],
             r"From each vertex, \(m-3\) diagonals go out (not to itself and not to its two neighbours); each diagonal has two ends.",
             r"'Diagonals of a hexagon / decagon'; also 'people round a circle shake hands with everyone except their neighbours'.",
             r"Polygon of 12 sides: \(\frac{12\times 9}{2} = 54\).",
             r"Forgetting to subtract the sides, or forgetting to halve."),
    18: card(18, "Rectangles from Two Sets of Parallel Lines",
             r"If there are \(m\) horizontal and \(n\) vertical lines, the number of different rectangles formed is \({}^{m}C_{2}\times {}^{n}C_{2}\). "
             r"For any two sets of parallel lines, the same count gives the parallelograms.",
             r"\[ {}^{m}C_{2}\times {}^{n}C_{2} \]",
             [("Horizontal lines", "m"), ("Vertical lines", "n"), ("Two sides from each set", r"{}^{m}C_{2},\ {}^{n}C_{2}"), ("Rectangles", r"{}^{m}C_{2}\times {}^{n}C_{2}")],
             r"A rectangle is fixed by its two horizontal sides and its two vertical sides; any choice of two lines from each set gives one.",
             r"'Chess board with 9 horizontal and 9 vertical lines', '10 parallel lines cut by 13 other parallel lines', a grid in a figure "
             r"(count the lines, including the outer sides).",
             r"Chess board: \({}^{9}C_{2}\times {}^{9}C_{2} = 36\times 36 = 1296\).",
             r"Counting squares or small cells instead of all rectangles, or forgetting the outer boundary lines of the figure."),
    19: card(19, "Handshakes in a Party",
             r"In a party every person shakes hands with every other person. With \(n\) persons the number of handshakes is "
             r"\(H = {}^{n}C_{2} = \frac{n(n-1)}{2}\); given \(H\), find \(n\) from \(\frac{n(n-1)}{2} = H\).",
             r"\[ \frac{n(n-1)}{2} = H \]",
             [("Persons", "n"), ("Handshakes", r"H = {}^{n}C_{2}"), ("Equation", r"n(n-1) = 2H")],
             r"Every handshake is a pair of persons, so the handshakes are the selections of 2 persons from \(n\).",
             r"'Every person shakes hands with every other', 'each member gave a handshake to the remaining members', matches in a round robin.",
             r"\(210\) handshakes: \(n(n-1) = 420 = 21\times 20\), so \(n = 21\).",
             r"Using \(n(n-1)\) (that counts each handshake twice - it is the card-sending Rule 23)."),
    20: card(20, "Particular Members Always Included or Excluded",
             r"\(m\) members are to be selected from \(n\). The number of selections in which \(r\) particular members are always included "
             r"is \({}^{n-r}C_{m-r}\), and always excluded is \({}^{n-r}C_{m}\).",
             r"\[ \text{Included: } {}^{n-r}C_{m-r},\qquad \text{Excluded: } {}^{n-r}C_{m} \]",
             [("Total members", "n"), ("To select", "m"), ("Particular members", "r"), ("Included / excluded", r"{}^{n-r}C_{m-r}\ /\ {}^{n-r}C_{m}")],
             r"If the \(r\) are included, only \(m-r\) places are left, filled from the \(n-r\) others; if excluded, all \(m\) come from the \(n-r\) others.",
             r"'A particular member is always included (excluded)', 'two particular persons must be in every team'.",
             r"5 of 10 with one particular member: included \({}^{9}C_{4} = 126\), excluded \({}^{9}C_{5} = 126\).",
             r"Choosing from \(n\) instead of \(n-r\) (the particular members are already decided)."),
    21: card(21, "Triangles from Points with Some Collinear",
             r"There are \(n\) points in a plane, of which \(m\) are collinear (no other three are). The number of triangles with these points as "
             r"vertices is \({}^{n}C_{3} - {}^{m}C_{3}\).",
             r"\[ {}^{n}C_{3} - {}^{m}C_{3} \]",
             [("Points", "n"), ("Collinear points", "m"), ("All triples", r"{}^{n}C_{3}"), ("Triples on the line", r"{}^{m}C_{3}")],
             r"Any three points make a triangle unless all three lie on the same line; those \({}^{m}C_{3}\) triples are removed.",
             r"'\(n\) points in a plane of which \(m\) are collinear, find the number of triangles'.",
             r"10 points, 4 collinear: \(120 - 4 = 116\).",
             r"Subtracting \({}^{m}C_{2}\) (that is for lines, Rule 22), or not subtracting at all."),
}

OLD = {
    14: {},
    15: {855: (lambda: r15(10, 5, "boxes", r"Each choice of \(5\) boxes, one ball in each, is one way of distributing the identical balls."),
               "Find the number of ways in which 5 identical balls can be distributed among 10 different boxes, if not more than one ball can go into a box.", None),
         876: (lambda: r15(10, 6, "questions"), "In a test paper there are 10 questions in all. In how many different ways can you choose 6 questions to answer?", None),
         905: (lambda: r15_or(10, 15, "women", "men"), "There are 10 women and 15 men in an office. In how many ways can a person be selected?", {"c": "25"}),
         906: (lambda: r15(6, 3, "persons"), None, None)},
    16: {856: (lambda: r16(12), "Find the number of triangles formed by joining the vertices of a polygon of 12 sides.", None),
         911: (lambda: r16(8), None, None)},
    17: {857: (lambda: r17(12), "Find the number of diagonals of a polygon of 12 sides.", None),
         875: (lambda: r17(15, circle=True), "15 students are sitting around a circle. Each person shakes hands with everyone except his or her two neighbours. "
                                             "How many handshakes are exchanged?", None),
         913: (lambda: r17(10), "Find the number of diagonals of a decagon.", None)},
    18: {858: (lambda: r18(9, 9), "On a chess board there are 9 vertical and 9 horizontal lines. Find the number of rectangles formed on the chess board.", None),
         912: (lambda: r18(9, 9), None, None)},
    19: {859: (lambda: r19_find(210), "In a party every person shakes hands with every other person. If there was a total of 210 handshakes in the party, "
                                      "find the number of persons who were present in the party.", None),
         874: (lambda: r19_count(12), "There are 12 persons in a group and each of them shakes hands with every other person. Find the number of handshakes.", None)},
    20: {860: (lambda: r20(10, 5, 1), "There are 5 members in a delegation which is to be sent abroad. The total number of members is 10. In how many ways "
                                      "can the selection be made so that a particular member is always (i) included (ii) excluded?",
               {"a": r"\(126\), \(126\)", "b": r"\(120\), \(126\)", "c": r"\(126\), \(136\)", "d": r"\(136\), \(160\)"}),
         910: (lambda: r20(10, 5, 2, both=False, what="persons"), None, None)},
    21: {861: (lambda: r21(10, 4), "There are 10 points in a plane out of which 4 are collinear. Find the number of triangles formed by the points as vertices.", None)},
}

NEW = {
    14: [("r14_x1", r"If \({}^{19}C_{3r} = {}^{19}C_{r+3}\), find \(r\).", lambda: r14_equal(19, 3, 0, 1, 3),
          [r"\(r = 3\)", r"\(r = 4\)", r"\(r = 5\)", r"\(r = 2\)"], 2),
         ("r14_e1", r"Find \(n\) if \({}^{n}C_{5} : {}^{n-2}C_{3} = 9 : 2\).", lambda: r14_ratio(5, 2, 3, 9, 2),
          [r"\(n = 9\)", r"\(n = 12\)", r"\(n = 10\)", r"\(n = 11\)"], 3)],
    15: [("r15_e1", "How many groups of 5 persons can be formed from 9 men and 6 women?", lambda: r15(15, 5, "persons"), ["3003", "3030", "5005", "360360"], 1),
         ("r15_e2", "There are 12 apples in a basket. Find the number of ways in which 4 apples can be chosen from the basket.", lambda: r15(12, 4, "apples"),
          ["11880", "495", "792", "220"], 2),
         ("r15_e3", "There are 20 students in a class. Find the number of ways in which a committee of 4 students can be formed.", lambda: r15(20, 4, "students"),
          ["116280", "1140", "4845", "5845"], 3)],
    16: [("r16_e1", "Find the number of triangles formed by joining the vertices of a pentagon.", lambda: r16(5), ["10", "5", "15", "20"], 1),
         ("r16_e2", "Find the number of triangles formed by joining the vertices of a nonagon (9 sides).", lambda: r16(9), ["72", "126", "36", "84"], 4),
         ("r16_e3", "Find the number of triangles formed by joining the vertices of a decagon.", lambda: r16(10), ["90", "120", "240", "210"], 2)],
    17: [("r17_e1", "Find the number of diagonals of a pentagon.", lambda: r17(5), ["10", "2", "5", "7"], 3),
         ("r17_e2", "Find the number of diagonals of a nonagon (9 sides).", lambda: r17(9), ["27", "36", "18", "54"], 1),
         ("r17_e3", "Find the number of diagonals of a polygon of 11 sides.", lambda: r17(11), ["55", "88", "33", "44"], 4),
         ("r17_e4", "How many diagonals are there in a polygon of 15 sides?", lambda: r17(15), ["105", "90", "180", "75"], 2)],
    18: [("r18_x2", "A figure is formed by 5 horizontal lines and 7 vertical lines. Count the total number of rectangles in the figure.", lambda: r18(5, 7),
          ["210", "35", "420", "105"], 1),
         ("r18_e1", "8 parallel lines are intersected by 11 other parallel lines. Find the number of parallelograms thus formed.",
          lambda: r18(8, 11, "first set of", "second set of"), ["616", "3080", "1540", "1320"], 3),
         ("r18_e2", "ABCD is a rectangle. Inside it, 4 lines are drawn parallel to AB and 6 lines parallel to AD, dividing it into small rectangles. "
                    "How many rectangles are there in the whole figure?",
          lambda: r18(6, 8, "lines parallel to AB", "lines parallel to AD",
                      r" Counting the sides of ABCD, there are \(4 + 2 = 6\) lines parallel to AB and \(6 + 2 = 8\) lines parallel to AD."),
          ["150", "210", "35", "420"], 4)],
    19: [("r19_e1", "9 men entered a hall at the same time. If each person shook hands with every other person, find the total number of handshakes.",
          lambda: r19_count(9), ["72", "36", "45", "81"], 2),
         ("r19_e2", "In a party every person shakes hands with every other person. If there was a total of 66 handshakes, find the number of persons present.",
          lambda: r19_find(66), ["12", "11", "13", "33"], 1),
         ("r19_e3", "In a party every person shakes hands with every other person. If there was a total of 190 handshakes, find the number of persons present.",
          lambda: r19_find(190), ["19", "21", "95", "20"], 4),
         ("r19_e4", "In a party every person shakes hands with every other person. If there was a total of 153 handshakes, find the number of persons present.",
          lambda: r19_find(153), ["17", "19", "18", "16"], 3),
         ("r19_e5", "At a meeting each member shook hands with every other member. If the total number of handshakes was 55, how many members were present?",
          lambda: r19_find(55), ["10", "11", "12", "9"], 2)],
    20: [("r20_e1", "There are 5 members in a delegation which is to be sent abroad. The total number of members is 9. In how many ways can the selection "
                    "be made so that a particular member is always (i) included (ii) excluded?",
          lambda: r20(9, 5, 1), [r"\(70\), \(56\)", r"\(56\), \(70\)", r"\(126\), \(70\)", r"\(70\), \(126\)"], 1),
         ("r20_e2", "There are 4 members in a delegation which is to be sent abroad. The total number of members is 10. In how many ways can the selection "
                    "be made so that a particular member is always (i) included (ii) excluded?",
          lambda: r20(10, 4, 1), [r"\(126\), \(84\)", r"\(84\), \(210\)", r"\(84\), \(126\)", r"\(36\), \(126\)"], 3),
         ("r20_e3", "There are 6 members in a delegation which is to be sent abroad. The total number of members is 14. In how many ways can the selection "
                    "be made so that 2 particular members are always (i) included (ii) excluded?",
          lambda: r20(14, 6, 2), [r"\(495\), \(792\)", r"\(924\), \(495\)", r"\(1001\), \(924\)", r"\(495\), \(924\)"], 4)],
    21: [("r21_e1", "There are 13 points in a plane out of which 4 are collinear. Find the number of triangles formed by the points as vertices.",
          lambda: r21(13, 4), ["286", "282", "278", "290"], 2),
         ("r21_e2", "There are 15 points in a plane out of which 6 are collinear. Find the number of triangles formed by the points as vertices.",
          lambda: r21(15, 6), ["435", "455", "440", "420"], 1),
         ("r21_e3", "There are 11 points in a plane out of which 5 are collinear. Find the number of triangles formed by the points as vertices.",
          lambda: r21(11, 5), ["165", "160", "150", "155"], 4)],
}


def main():
    gen_1_7.OLD, gen_1_7.NEW, gen_1_7.CARDS = OLD, NEW, CARDS
    gen_1_7.main(range(14, 22))


if __name__ == "__main__":
    main()
