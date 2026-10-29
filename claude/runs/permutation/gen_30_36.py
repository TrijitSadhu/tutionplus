"""Rules 30-36 (book II. Combinations, Rules 17-23; site number = book number + 13) and the Miscellaneous set.
Writes the seven rule cards, regenerates the old rows 870-873, 878 in the prompt #13 layout and links them (all keys were
right), adds the book's worked examples (Rules 31, 35, 36) and exercises that had no copy (numbers changed), and the two
Miscellaneous problems (3 questions, 'at least' selections) as new questions under Rule 26 in misc/rule26 (Rule 26's card
#242 is reused unchanged). Same outputs as gen_1_7.py."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, steps  # noqa: E402
from pc_common import D, I, comb, falling_tex, nC, num, result, times  # noqa: E402
import gen_1_7  # noqa: E402
import gen_22_29  # noqa: E402

CH = "permutation_combination"


def pair(a, b):
    return ("pair", (a, b))


def choose_n(n, r, what):
    v = comb(n, r)
    return v, (f"Choose {r} of the {n} {what}.", rf"Picking \({r}\) of the \({n}\) {what} one after another gives \({falling_tex(n, r)}\) ordered picks; "
                                                 rf"each choice is picked in \({r}!\) orders:" + D(rf"\frac{{{falling_tex(n, r)}}}{{{r}!}} = {v}"))


def simple(T, fexpr, fsub, v, trad, ident):
    rule = steps(("Identify the value.", ident), ("Apply the specified rule.", D(fexpr)), ("Substitute the value.", D(f"{fsub} = {v}")))
    rb = [ident, rf"Use \({fexpr}\).", rf"\({fsub} = {v}\)."]
    return result(num(v), T, trad, rule, I(v), rb, D(f"{fsub} = {v}"))


# ---------------------------------------------------------------- Rule 30 (book C17): quadrilaterals
T30 = r"The number of quadrilaterals that can be formed by joining the vertices of a polygon of \(n\) sides (\(n \gt 3\)) is<br>\[ \frac{n(n-1)(n-2)(n-3)}{24} \]"


def r30(n):
    v, st = choose_n(n, 4, "vertices")
    trad = steps(("A quadrilateral is four vertices.", rf"Any \(4\) of the \({n}\) vertices of a polygon (no three on a line) form exactly one quadrilateral."), st)
    return simple(T30, r"\frac{n(n-1)(n-2)(n-3)}{24}", rf"\frac{{{times(n, n - 1, n - 2, n - 3)}}}{{24}}", v, trad, rf"\(n = {n}\) sides.")


# ---------------------------------------------------------------- Rule 31 (book C18): lines from n points
T31 = r"If there are \(n\) points in a plane and no three are collinear, the number of straight lines through them is<br>\[ \frac{n(n-1)}{2} \]"


def r31(n):
    v, st = choose_n(n, 2, "points")
    trad = steps(("A line is fixed by two points.", r"No three points are on one line, so every pair of points gives a different line."), st)
    return simple(T31, r"\frac{n(n-1)}{2}", rf"\frac{{{n}\times {n - 1}}}{{2}}", v, trad, rf"\(n = {n}\) points.")


# ---------------------------------------------------------------- Rule 32 (book C19): triangles from n points
T32 = r"If there are \(n\) points in a plane and no three are collinear, the number of triangles formed with them is<br>\[ \frac{n(n-1)(n-2)}{6} \]"


def r32(n):
    v, st = choose_n(n, 3, "points")
    trad = steps(("A triangle is three points.", r"No three points are on one line, so every choice of three points gives a triangle."), st)
    return simple(T32, r"\frac{n(n-1)(n-2)}{6}", rf"\frac{{{times(n, n - 1, n - 2)}}}{{6}}", v, trad, rf"\(n = {n}\) points.")


# ---------------------------------------------------------------- Rules 33, 34: 2^n and 3^n outcomes
T33 = r"\(n\) students appear in an examination. The number of ways in which the result can be announced is<br>\[ 2^{n} \]"
T34 = r"\(n\) matches are played in a chess tournament. The number of ways in which their results can be decided is<br>\[ 3^{n} \]"


def outcomes(n, k, T, unit, cases):
    v = k ** n
    trad = steps((f"Each {unit} has {k} possible results.", f"Every {unit} ends in one of {k} ways ({cases}), whatever happens to the others."),
                 ("Multiply over all of them.", D(f"{times(*([k] * n))} = {v}")))
    return simple(T, f"{k}^{{n}}", f"{k}^{{{n}}}", v, trad, rf"\(n = {n}\) {unit}s.")


def r33(n):
    return outcomes(n, 2, T33, "student", "pass or fail")


def r34(n):
    return outcomes(n, 3, T34, "match", "win, loss or draw")


# ---------------------------------------------------------------- Rules 35, 36: forecasts
T35 = (r"A badminton tournament has \(n\) matches (each won or lost). The number of ways of forecasting the results is \(2^{n}\); "
       r"the number of forecasts with all results correct (or all wrong) is \(1^{n} = 1\).")
T36 = (r"The Indian hockey team plays \(n\) matches (each a win, loss or draw). The number of forecasts with all results correct is "
       r"\(1^{n} = 1\); with all results wrong it is \(2^{n}\).")


def r35(n, part="all"):
    """part: 'all' (number of forecasts), 'pair' (all forecasts, all-correct forecasts)."""
    tot = 2 ** n
    trad = steps(("Count the forecasts.", rf"Each of the \({n}\) matches can be forecast in \(2\) ways (win or loss):" + D(f"{times(*([2] * n))} = {tot}")),
                 *((("Forecasts with every result correct.", r"For each match only the actual result is a correct forecast: \(1\) way each, so \(1\times 1\times\cdots = 1\)."),)
                   if part == "pair" else ()))
    rule = steps(("Identify the value.", rf"\(n = {n}\) matches."),
                 ("Apply the specified rule.", r"Forecasts \(= 2^{n}\)" + (r"; all correct \(= 1^{n} = 1\)." if part == "pair" else ".")),
                 ("Substitute the value.", D(f"2^{{{n}}} = {tot}" + (r",\qquad 1^{" + str(n) + "} = 1" if part == "pair" else ""))))
    rb = [rf"\(n = {n}\).", r"Forecasts \(= 2^{n}\)" + (r", all correct \(= 1\)." if part == "pair" else "."), rf"\(2^{{{n}}} = {tot}\)" + (r", \(1^{n} = 1\)." if part == "pair" else ".")]
    if part == "pair":
        return result(pair(tot, 1), T35, trad, rule, I(tot) + " and " + I(1), rb, D(f"2^{{{n}}} = {tot},\\quad 1^{{{n}}} = 1"))
    return result(num(tot), T35, trad, rule, I(tot), rb, D(f"2^{{{n}}} = {tot}"))


def r36(n, part):
    """part: 'correct' (1), 'pair' (all correct, all wrong)."""
    wrong = 2 ** n
    items = [("All results correct.", rf"For each of the \({n}\) matches only the actual result is a correct forecast: \({times(*([1] * n))} = 1\) way.")]
    if part == "pair":
        items.append(("All results wrong.", rf"For each match the forecast can be wrong in \(2\) ways (the two results that did not happen):" + D(f"{times(*([2] * n))} = {wrong}")))
    trad = steps(*items)
    rule = steps(("Identify the value.", rf"\(n = {n}\) matches."),
                 ("Apply the specified rule.", r"All correct \(= 1^{n}\)" + (r"; all wrong \(= 2^{n}\)." if part == "pair" else ".")),
                 ("Substitute the value.", D(f"1^{{{n}}} = 1" + (f",\\qquad 2^{{{n}}} = {wrong}" if part == "pair" else ""))))
    rb = [rf"\(n = {n}\).", r"All correct \(= 1^{n}\)" + (r", all wrong \(= 2^{n}\)." if part == "pair" else "."), r"\(1^{n} = 1\)" + (rf", \(2^{{{n}}} = {wrong}\)." if part == "pair" else ".")]
    if part == "pair":
        return result(pair(1, wrong), T36, trad, rule, I(1) + " and " + I(wrong), rb, D(f"1^{{{n}}} = 1,\\quad 2^{{{n}}} = {wrong}"))
    return result(num(1), T36, trad, rule, I(1), rb, D(f"1^{{{n}}} = 1"))


# ---------------------------------------------------------------- Miscellaneous: 'at least k from group A' (Rule 26)
def at_least(x, y, n, k, A, B):
    cases = [(r, comb(x, r) * comb(y, n - r)) for r in range(k, min(n, x) + 1) if 0 <= n - r <= y]
    v = sum(w for _, w in cases)
    total = comb(x + y, n)
    bad = [(r, comb(x, r) * comb(y, n - r)) for r in range(0, k) if 0 <= n - r <= y]
    trad = steps(
        ("Count all the selections.", rf"\({n}\) of the \({x + y}\) persons: " + I(rf"{nC(x + y, n)} = {total}") + "."),
        (f"Remove the selections with fewer than {k} {A}.", "".join(rf"With \({r}\) {A}: \({nC(x, r)}\times {nC(y, n - r)} = {w}\). " for r, w in bad)
         + D(f"{total} - " + " - ".join(str(w) for _, w in bad) + f" = {v}")))
    table = ('<table border="1" cellpadding="4"><tr><th>' + A.capitalize() + "</th><th>" + B.capitalize() + "</th><th>Ways</th></tr>" + "".join(
        rf"<tr><td>\({r}\)</td><td>\({n - r}\)</td><td>\({nC(x, r)}\times {nC(y, n - r)} = {w}\)</td></tr>" for r, w in cases) + "</table>")
    rule = steps(
        ("Identify the values.", rf"\(x = {x}\) {A}, \(y = {y}\) {B}, choose \(n = {n}\) with at least \({k}\) {A}."),
        ("Apply the specified rule.", r"Add the cases 'exactly \(r\) " + A + r"', each \({}^{x}C_{r}\times {}^{y}C_{n-r}\):" + table),
        ("Substitute the values.", D(" + ".join(str(w) for _, w in cases) + f" = {v}")))
    rb = [rf"\({x}\) {A}, \({y}\) {B}, choose \({n}\), at least \({k}\) {A}.", r"Add \({}^{x}C_{r}\times {}^{y}C_{n-r}\) for \(r = " + f"{k}, {k + 1}, " + r"\ldots\)",
          " + ".join(str(w) for _, w in cases) + rf" \(= {v}\)."]
    return result(num(v), gen_22_29.T26, trad, rule, I(v), rb, D(" + ".join(str(w) for _, w in cases) + f" = {v}"))


# ---------------------------------------------------------------- cards
CARDS = {
    30: card(30, "Quadrilaterals from the Vertices of a Polygon",
             r"The number of quadrilaterals that can be formed by joining the vertices of a polygon of \(n\) sides (\(n \gt 3\)) is \({}^{n}C_{4}\).",
             r"\[ \frac{n(n-1)(n-2)(n-3)}{24} \]",
             [("Vertices", "n"), ("A quadrilateral", r"4 \text{ vertices}"), ("Quadrilaterals", r"{}^{n}C_{4}")],
             r"Any four vertices of a polygon, joined in order round the polygon, give one quadrilateral.",
             r"'Quadrilaterals formed by joining the vertices of an octagon / a polygon of \(n\) sides'.",
             r"Octagon: \(\frac{8\times 7\times 6\times 5}{24} = 70\).",
             r"Dividing by 6 (triangles) instead of 24, or using \({}^{n}P_{4}\)."),
    31: card(31, "Straight Lines through n Points",
             r"If there are \(n\) points in a plane and no three are collinear, the number of straight lines that can be drawn through them is \({}^{n}C_{2}\).",
             r"\[ \frac{n(n-1)}{2} \]",
             [("Points", "n"), ("A line", r"2 \text{ points}"), ("Lines", r"{}^{n}C_{2}")],
             r"Two points fix a line, and with no three collinear no two pairs give the same line.",
             r"'Straight lines formed by joining \(n\) points, no three collinear'.",
             r"16 points: \(\frac{16\times 15}{2} = 120\).",
             r"Using \(n(n-1)\) (each line counted twice), or forgetting the 'no three collinear' condition (then use Rule 22)."),
    32: card(32, "Triangles from n Points",
             r"If there are \(n\) points in a plane and no three are collinear, the number of triangles formed with these points is \({}^{n}C_{3}\).",
             r"\[ \frac{n(n-1)(n-2)}{6} \]",
             [("Points", "n"), ("A triangle", r"3 \text{ points}"), ("Triangles", r"{}^{n}C_{3}")],
             r"Three points not on a line form exactly one triangle, and the order of the three does not matter.",
             r"'Triangles that can be formed with \(n\) points of which no three are collinear'.",
             r"12 points: \(\frac{12\times 11\times 10}{6} = 220\).",
             r"Dividing by 2 instead of 6, or subtracting collinear triples when there are none (that is Rule 21)."),
    33: card(33, "Ways to Announce Examination Results",
             r"\(n\) students appear in an examination. The number of ways in which the result can be announced is \(2^{n}\).",
             r"\[ 2^{n} \]",
             [("Students", "n"), ("Each student", r"\text{pass or fail: } 2"), ("Results", "2^{n}")],
             r"Each student independently passes or fails, so the two cases of each student multiply.",
             r"'\(n\) students appear in an examination; in how many ways can the result be announced'.",
             r"6 students: \(2^{6} = 64\).",
             r"Using \(2n\) or \(2^{n} - 1\) (every pattern, even all pass or all fail, is a possible result)."),
    34: card(34, "Results of Chess Matches",
             r"\(n\) matches are to be played in a chess tournament. The number of ways in which their results can be decided is \(3^{n}\).",
             r"\[ 3^{n} \]",
             [("Matches", "n"), ("Each match", r"\text{win, loss or draw: } 3"), ("Results", "3^{n}")],
             r"A chess match ends in a win, a loss or a draw; the matches are independent, so the three cases of each multiply.",
             r"'\(n\) matches in a chess tournament, in how many ways can their results be decided'.",
             r"3 matches: \(3^{3} = 27\).",
             r"Using \(2^{n}\) (a draw is possible in chess) or \(n^{3}\)."),
    35: card(35, "Forecasting Badminton Results",
             r"A badminton tournament consists of \(n\) matches. The number of ways their results can be forecast is \(2^{n}\); the number of "
             r"forecasts containing all correct (or all wrong) results is \(1\).",
             r"\[ 2^{n},\qquad 1^{n} = 1 \]",
             [("Matches", "n"), ("Each match", r"\text{win or loss: } 2"), ("Forecasts", "2^{n}"), ("All correct / all wrong", "1")],
             r"A badminton match is won or lost (no draw): 2 forecasts per match, and exactly one of them is right and one wrong.",
             r"'A badminton tournament of \(n\) matches', 'forecasts', 'all correct results', 'all wrong results'.",
             r"3 matches: \(2^{3} = 8\) forecasts; \(1\) with all correct, \(1\) with all wrong.",
             r"Using \(3^{n}\) as for chess or hockey (no draw in badminton)."),
    36: card(36, "Forecasting Hockey Results",
             r"The Indian hockey team is to play \(n\) matches. The number of forecasts that contain all correct results is \(1^{n} = 1\); "
             r"the number that contain all wrong results is \(2^{n}\).",
             r"\[ \text{All correct: } 1^{n} = 1,\qquad \text{All wrong: } 2^{n} \]",
             [("Matches", "n"), ("Each match", r"\text{win, loss or draw}"), ("Correct forecasts per match", "1"), ("Wrong forecasts per match", "2")],
             r"For each match only the actual result is a correct forecast, while the two other results are wrong forecasts.",
             r"'The hockey team plays \(n\) matches; forecasts with all correct (all wrong) results'.",
             r"4 matches: all correct \(1\); all wrong \(2^{4} = 16\).",
             r"Using \(3^{n}\) (that counts all forecasts) or \(2^{n}\) for all correct."),
}

OLD = {
    30: {870: (lambda: r30(8), "Find the number of quadrilaterals that can be formed by joining the vertices of an octagon.", None)},
    31: {878: (lambda: r31(6), "Find the number of straight lines formed by joining 6 different points in a plane, no three of them being collinear.", None)},
    32: {871: (lambda: r32(12), "Find the number of triangles that can be formed with 12 points in a plane of which no three points are collinear.", None)},
    33: {872: (lambda: r33(6), None, None)},
    34: {873: (lambda: r34(3), "3 matches are to be played in a chess tournament. In how many ways can their results be decided?", None)},
    35: {}, 36: {},
}

NEW = {
    30: [("r30_e1", "Find the number of quadrilaterals that can be formed by joining the vertices of a pentagon.", lambda: r30(5), ["10", "5", "20", "1"], 2),
         ("r30_e2", "Find the number of quadrilaterals that can be formed by joining the vertices of a nonagon (9 sides).", lambda: r30(9), ["84", "252", "126", "3024"], 3),
         ("r30_e3", "Find the number of quadrilaterals that can be formed by joining the vertices of a polygon of 11 sides.", lambda: r30(11), ["330", "165", "462", "7920"], 1),
         ("r30_e4", "Find the number of quadrilaterals that can be formed by joining the vertices of a polygon of 14 sides.", lambda: r30(14), ["364", "2002", "1820", "1001"], 4)],
    31: [("r31_x1", "How many straight lines can be drawn through 20 points in a plane of which no three are collinear?", lambda: r31(20), ["380", "190", "200", "1140"], 2),
         ("r31_e1", "How many straight lines can be drawn through 13 points in a plane of which no three are collinear?", lambda: r31(13), ["78", "156", "91", "286"], 1),
         ("r31_e2", "How many straight lines can be drawn through 17 points in a plane of which no three are collinear?", lambda: r31(17), ["272", "153", "136", "680"], 3),
         ("r31_e3", "How many straight lines can be drawn through 21 points in a plane of which no three are collinear?", lambda: r31(21), ["420", "231", "1330", "210"], 4)],
    32: [("r32_e1", "Find the number of triangles that can be formed with 9 points in a plane of which no three points are collinear.", lambda: r32(9), ["84", "36", "504", "126"], 1),
         ("r32_e2", "Find the number of triangles that can be formed with 16 points in a plane of which no three points are collinear.", lambda: r32(16), ["455", "1820", "560", "680"], 3),
         ("r32_e3", "Find the number of triangles that can be formed with 11 points in a plane of which no three points are collinear.", lambda: r32(11), ["220", "165", "990", "55"], 2)],
    33: [("r33_e1", "3 students appear in an examination. In how many ways can the result be announced?", lambda: r33(3), ["6", "9", "7", "8"], 4),
         ("r33_e2", "8 students appear in an examination. In how many ways can the result be announced?", lambda: r33(8), ["256", "255", "64", "16"], 1),
         ("r33_e3", "10 students appear in an examination. In how many ways can the result be announced?", lambda: r33(10), ["1023", "100", "1024", "20"], 3)],
    34: [("r34_e1", "6 matches are to be played in a chess tournament. In how many ways can their results be decided?", lambda: r34(6), ["216", "729", "64", "18"], 2),
         ("r34_e2", "7 matches are to be played in a chess tournament. In how many ways can their results be decided?", lambda: r34(7), ["2187", "343", "128", "21"], 1),
         ("r34_e3", "8 matches are to be played in a chess tournament. In how many ways can their results be decided?", lambda: r34(8), ["512", "256", "6561", "24"], 3)],
    35: [("r35_x1", "A badminton tournament consists of 6 matches. (i) In how many ways can their results be forecast? "
                    "(ii) How many different forecasts contain all correct results?", lambda: r35(6, "pair"),
          [r"\(64\), \(1\)", r"\(729\), \(1\)", r"\(64\), \(6\)", r"\(32\), \(1\)"], 1),
         ("r35_e1", "A badminton tournament consists of 3 matches. In how many ways can their results be forecast?", lambda: r35(3), ["27", "6", "9", "8"], 4),
         ("r35_e2", "A badminton tournament consists of 8 matches. In how many ways can their results be forecast?", lambda: r35(8), ["255", "256", "6561", "16"], 2),
         ("r35_e3", "A badminton tournament consists of 9 matches. In how many ways can their results be forecast?", lambda: r35(9), ["511", "19683", "512", "81"], 3)],
    36: [("r36_x1", "The Indian hockey team is to play 5 matches for the world cup. (i) How many different forecasts will contain all correct results? "
                    "(ii) How many different forecasts will contain all wrong results?", lambda: r36(5, "pair"),
          [r"\(1\), \(243\)", r"\(5\), \(32\)", r"\(1\), \(32\)", r"\(1\), \(25\)"], 3),
         ("r36_e1", "The Indian hockey team is to play 6 matches for the world cup. How many different forecasts will contain all correct results?",
          lambda: r36(6, "correct"), ["6", "64", "729", "1"], 4),
         ("r36_e2", "The Indian hockey team is to play 7 matches for the world cup. (i) How many different forecasts will contain all correct results? "
                    "(ii) How many different forecasts will contain all wrong results?", lambda: r36(7, "pair"),
          [r"\(1\), \(2187\)", r"\(1\), \(128\)", r"\(7\), \(128\)", r"\(1\), \(127\)"], 2)],
}

MISC = [("m1", "From 5 officers and 7 jawans, in how many ways can 5 be chosen to include at least one officer?",
         lambda: at_least(5, 7, 5, 1, "officers", "jawans"), ["792", "771", "735", "21"], 2),
        ("m2_i", "From a group of 7 men and 3 women a committee of 4 persons is to be formed. In how many different ways can it be done so that "
                 "the committee has at least one woman?", lambda: at_least(3, 7, 4, 1, "women", "men"), ["175", "210", "203", "35"], 1),
        ("m2_ii", "From a group of 7 men and 3 women a committee of 4 persons is to be formed. In how many different ways can it be done so that "
                  "the committee has at least 2 men?", lambda: at_least(7, 3, 4, 2, "men", "women"), ["175", "210", "196", "203"], 4)]


def misc():
    folder = os.path.join(HERE, "misc", "rule26")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"]["rule_html"] == gen_22_29.CARDS[26], "stored Rule 26 card differs from gen_22_29.CARDS[26]"
    json.dump([], open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"))
    qs, answers = [], []
    for key, text, fn, op, pos in MISC:
        g = fn()
        qs.append(new_question(26, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": CH, "rule_name": "Rule 26", "rule_html": gen_22_29.CARDS[26]}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"misc Rule 26: {len(qs)} new questions")


def main():
    gen_1_7.OLD, gen_1_7.NEW, gen_1_7.CARDS = OLD, NEW, CARDS
    gen_1_7.main(range(30, 37))
    misc()


if __name__ == "__main__":
    main()
