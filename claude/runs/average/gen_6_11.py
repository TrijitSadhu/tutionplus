"""Average Rules 6-11 (2026-10-30). Rule 6: one quantity taken away - it is n(x - y) + y. Rule 7: x added to / taken from every
number - the average moves by x. Rule 8: a new quantity joins - it is n(y - x) + y. Rule 9: every number multiplied / divided by x -
the average is multiplied / divided by x. Rule 10: some members replaced and the average goes up by x - the new ones come to
y + nx. Rule 11: the same when the average goes down - y - nx. Writes the six cards, regenerates the old rows 503-505 with
simple-style sentences, new settings and all-new numbers, and adds the book's worked examples and exercises that had no copy.
Usage: python gen_6_11.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from helpers import place, result  # noqa: E402


def nf(v):
    """A number as the questions write it: 12, 2.5, 12.96 (terminating decimals), else a mixed fraction."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    for places in (1, 2):
        if (v * 10 ** places).denominator == 1:
            return f"{float(v):.{places}f}"
    return tex(v)


def UU(v, unit=""):
    return rf"\({nf(v)}\)" + (f" {unit}" if unit else "")


def opts(v, unit="", wrong=None):
    v = F(v)
    if wrong is None:
        step = max(1, abs(v) // 10) if v.denominator == 1 else F(1, 2)
        wrong = [v + step, v - step, v + 2 * step] if v - step > 0 else [v + step, v + 2 * step, v + 3 * step]
    return place(UU(v, unit), [UU(w, unit) for w in wrong])


T6 = (r"If the average of \(n\) quantities is \(x\) and one of them is taken away, so that the average of the rest becomes \(y\), "
      r"the quantity taken away is<br>\[ n(x-y)+y \]")
T7 = (r"If the average of \(n\) numbers is \(m\) and \(x\) is added to (or taken away from) every number, the new average is"
      r"<br>\[ m+x \quad\text{or}\quad m-x \]")
T8 = (r"If the average of \(n\) quantities is \(x\) and one new quantity joins them, so that the average becomes \(y\), the new "
      r"quantity is<br>\[ n(y-x)+y \]")
T9 = (r"If the average of \(n\) numbers is \(m\) and every number is multiplied (or divided) by \(x\), the new average is"
      r"<br>\[ mx \quad\text{or}\quad \frac{m}{x} \]")
T10 = (r"If the average of \(n\) persons goes up by \(x\) when some of them, together \(y\), are replaced by the same number of new "
       r"persons, the new persons together come to<br>\[ y+nx \]")
T11 = (r"If the average of \(n\) persons goes down by \(x\) when some of them, together \(y\), are replaced by the same number of new "
       r"persons, the new persons together come to<br>\[ y-nx \]")
TH = {6: T6, 7: T7, 8: T8, 9: T9, 10: T10, 11: T11}


def apply(r):
    return ("Apply the specified rule.", TH[r].split("<br>")[1])


def r6_removed(n, x, y, unit, total=None, drop=None):
    """n quantities (the one taken away included) average x (or add up to total); without it the rest average y (or x - drop)."""
    n = F(n)
    x = F(total) / n if total is not None else F(x)
    y = x - F(drop) if drop is not None else F(y)
    v = n * x - (n - 1) * y
    first = (rf"Given: \({nf(n * x)}\), so the average is \({nf(n * x)} \div {tex(n)} = {nf(x)}\)." if total is not None
             else rf"\[ {tex(n)}\times {nf(x)} = {nf(n * x)} \]")
    rest = (rf"Their average is \({nf(x)} - {nf(F(drop))} = {nf(y)}\): " if drop is not None else "") + rf"\[ {tex(n - 1)}\times {nf(y)} = {nf((n - 1) * y)} \]"
    trad = steps(("Total of all.", first), ("Total of the rest.", rest),
                 ("The one taken away.", rf"\[ {nf(n * x)} - {nf((n - 1) * y)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(x)}\), \(y = {nf(y)}\)."), apply(6),
                 ("Substitute the values.", rf"\[ {tex(n)}({nf(x)}-{nf(y)})+{nf(y)} = {nf(n * (x - y))}+{nf(y)} = {nf(v)} \]"))
    return result(("number", v), T6, trad, rule, UU(v, unit), [rf"All \(= {nf(n * x)}\).", rf"Rest \(= {nf((n - 1) * y)}\).", rf"Taken away \(= {nf(v)}\)."],
                  rf"\[ {tex(n)}({nf(x)}-{nf(y)})+{nf(y)} = {nf(v)} \]")


def r7_shift(n, mm, d, unit=""):
    """d > 0 is added to every number, d < 0 is taken away."""
    n, mm, d = F(n), F(mm), F(d)
    v = mm + d
    word, sg = ("added to", "+") if d > 0 else ("taken away from", "-")
    trad = steps(("Total before.", rf"\[ {tex(n)}\times {nf(mm)} = {nf(n * mm)} \]"),
                 ("Change in the total.", rf"\({nf(abs(d))}\) is {word} each of the \({tex(n)}\) numbers: \[ {tex(n)}\times {nf(abs(d))} = {nf(n * abs(d))} \]"),
                 ("New average.", rf"\[ \frac{{{nf(n * mm)} {sg} {nf(n * abs(d))}}}{{{tex(n)}}} = \frac{{{nf(n * v)}}}{{{tex(n)}}} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(m = {nf(mm)}\), \(x = {nf(abs(d))}\) ({word.split()[0]})."), apply(7),
                 ("Substitute the values.", rf"\[ {nf(mm)} {sg} {nf(abs(d))} = {nf(v)} \]"))
    return result(("number", v), T7, trad, rule, UU(v, unit), [rf"Old average \(= {nf(mm)}\).", rf"Each number {'+' if d > 0 else '-'}\({nf(abs(d))}\).", rf"New average \(= {nf(v)}\)."],
                  rf"\[ {nf(mm)} {sg} {nf(abs(d))} = {nf(v)} \]")


def r7_e2():
    """x numbers average 5x; x is added to each."""
    trad = steps(("Total before.", r"\[ x\times 5x = 5x^{2} \]"), ("Change in the total.", r"\(x\) is added to each of the \(x\) numbers: \[ x\times x = x^{2} \]"),
                 ("New average.", r"\[ \frac{5x^{2}+x^{2}}{x} = \frac{6x^{2}}{x} = 6x \]"))
    rule = steps(("Identify the values.", r"\(m = 5x\), and \(x\) is added."), apply(7), ("Substitute the values.", r"\[ 5x + x = 6x \]"))
    return result(("expr", F(42)), T7, trad, rule, r"\(6x\)", [r"Old average \(= 5x\).", r"Each number \(+x\).", r"New average \(= 6x\)."], r"\[ 5x+x = 6x \]")


def r7_e4():
    """x numbers average 4x; x + 2 is taken from each."""
    trad = steps(("Total before.", r"\[ x\times 4x = 4x^{2} \]"), ("Change in the total.", r"\(x+2\) is taken from each of the \(x\) numbers: \[ x(x+2) = x^{2}+2x \]"),
                 ("New average.", r"\[ \frac{4x^{2}-x^{2}-2x}{x} = \frac{3x^{2}-2x}{x} = 3x-2 \]"))
    rule = steps(("Identify the values.", r"\(m = 4x\), and \(x+2\) is taken away."), apply(7), ("Substitute the values.", r"\[ 4x-(x+2) = 3x-2 \]"))
    return result(("expr", F(19)), T7, trad, rule, r"\(3x-2\)", [r"Old average \(= 4x\).", r"Each number \(-(x+2)\).", r"New average \(= 3x-2\)."], r"\[ 4x-(x+2) = 3x-2 \]")


def r8_added(n, x, y, unit):
    n, x, y = F(n), F(x), F(y)
    v = (n + 1) * y - n * x
    trad = steps(("Total before.", rf"\[ {tex(n)}\times {nf(x)} = {nf(n * x)} \]"), ("Total after.", rf"\[ {tex(n + 1)}\times {nf(y)} = {nf((n + 1) * y)} \]"),
                 ("The new one.", rf"\[ {nf((n + 1) * y)} - {nf(n * x)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(x)}\), \(y = {nf(y)}\)."), apply(8),
                 ("Substitute the values.", rf"\[ {tex(n)}({nf(y)}-{nf(x)})+{nf(y)} = {nf(n * (y - x))}+{nf(y)} = {nf(v)} \]"))
    return result(("number", v), T8, trad, rule, UU(v, unit), [rf"Before \(= {nf(n * x)}\).", rf"After \(= {nf((n + 1) * y)}\).", rf"New one \(= {nf(v)}\)."],
                  rf"\[ {tex(n)}({nf(y)}-{nf(x)})+{nf(y)} = {nf(v)} \]")


def r9_scale(n, mm, k, op, unit=""):
    n, mm, k = F(n), F(mm), F(k)
    v = mm * k if op == "x" else mm / k
    sym, word = (r"\times", "multiplied") if op == "x" else (r"\div", "divided")
    trad = steps(("Total before.", rf"\[ {tex(n)}\times {nf(mm)} = {nf(n * mm)} \]"),
                 ("New total.", rf"Every number is {word} by \({tex(k)}\), so the total is too: \[ {nf(n * mm)} {sym} {tex(k)} = {nf(n * v)} \]"),
                 ("New average.", rf"\[ {nf(n * v)} \div {tex(n)} = {nf(v)} \]"))
    rule = steps(("Identify the values.", rf"\(m = {nf(mm)}\), \(x = {tex(k)}\) ({word})."), apply(9), ("Substitute the values.", rf"\[ {nf(mm)} {sym} {tex(k)} = {nf(v)} \]"))
    return result(("number", v), T9, trad, rule, UU(v, unit), [rf"Old average \(= {nf(mm)}\).", rf"Each number {sym[1:]} \({tex(k)}\).", rf"New average \(= {nf(v)}\)."],
                  rf"\[ {nf(mm)} {sym} {tex(k)} = {nf(v)} \]")


def r9_e1():
    """x numbers average y; each is multiplied by x + 1."""
    trad = steps(("Total before.", r"\[ x\times y = xy \]"), ("New total.", r"Every number is multiplied by \(x+1\), so the total is too: \[ xy(x+1) \]"),
                 ("New average.", r"\[ \frac{xy(x+1)}{x} = (x+1)y \]"))
    rule = steps(("Identify the values.", r"\(m = y\), multiplier \(= x+1\)."), apply(9), ("Substitute the values.", r"\[ y\times (x+1) = (x+1)y \]"))
    return result(("expr", F(24)), T9, trad, rule, r"\((x+1)y\)", [r"Old average \(= y\).", r"Each number \(\times (x+1)\).", r"New average \(= (x+1)y\)."], r"\[ y(x+1) = (x+1)y \]")


def leavers(out, lead):
    if len(out) == 1:
        return rf"{lead} leaver's \({nf(out[0])}\)"
    return rf"{lead} leavers' \({' + '.join(nf(o) for o in out)} = {nf(sum(out))}\)"


def r10_up(n, inc, out, unit, several=False):
    """the average of n goes up by inc when the members in `out` are replaced by as many new ones."""
    n, inc = F(n), F(inc)
    out = [F(o) for o in out]
    y = sum(out)
    tot = y + n * inc
    v = tot / len(out)
    trad = [("Rise in the total.", rf"The average of \({tex(n)}\) rises by \({nf(inc)}\): \[ {tex(n)}\times {nf(inc)} = {nf(n * inc)} \]"),
            ("What the new ones bring.", leavers(out, "They bring the") + rf" plus the rise: \[ {nf(y)} + {nf(n * inc)} = {nf(tot)} \]")]
    if several:
        trad.append(("Their average.", rf"\[ {nf(tot)} \div {len(out)} = {nf(v)} \]"))
    rule = [("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(inc)}\), \(y = {nf(y)}\)."), apply(10),
            ("Substitute the values.", rf"\[ {nf(y)} + {tex(n)}\times {nf(inc)} = {nf(tot)} \]" + (rf"shared by \({len(out)}\): \[ {nf(tot)} \div {len(out)} = {nf(v)} \]" if several else ""))]
    sc = rf"\[ {nf(y)} + {tex(n)}\times {nf(inc)} = {nf(tot)} \]" + (rf"\[ {nf(tot)} \div {len(out)} = {nf(v)} \]" if several else "")
    return result(("number", v), T10, steps(*trad), steps(*rule), UU(v, unit), [rf"Rise \(= {nf(n * inc)}\).", rf"New ones \(= {nf(tot)}\).", rf"Answer \(= {nf(v)}\)."], sc)


def r10_same(n, yrs):
    """the average age of n is what it was yrs years ago because a younger member took one place."""
    n, yrs = F(n), F(yrs)
    v = n * yrs
    trad = steps(("Ageing of the panel.", rf"In \({tex(yrs)}\) years each of the \({tex(n)}\) members gets \({tex(yrs)}\) years older: \[ {tex(n)}\times {tex(yrs)} = {tex(v)} \] years added to the total."),
                 ("The total did not change.", r"The average is the same as before, so the total is the same as before."),
                 ("The new member.", rf"The swap must take those \({tex(v)}\) years away: the new member is \({tex(v)}\) years younger."))
    rule = steps(("Identify the values.", rf"\(n = {tex(n)}\). Without the swap the average would now be \({tex(yrs)}\) higher; it is not, so the swap changed the "
                                          rf"average by \(x = -{tex(yrs)}\). \(y\) = the replaced member's age now."), apply(10),
                 ("Substitute the values.", rf"\[ y + {tex(n)}\times(-{tex(yrs)}) = y - {tex(v)} \]so the new member is \({tex(v)}\) years younger."))
    return result(("number", v), T10, trad, rule, rf"\({tex(v)}\) years", [rf"Expected rise \(= {tex(n)}\times {tex(yrs)}\).", r"Actual rise \(= 0\).", rf"Younger by \({tex(v)}\) years."],
                  rf"\[ {tex(n)}\times {tex(yrs)} = {tex(v)} \]")


def r11_down(n, months, out, several=False, pair=False):
    """the average age of n goes down by `months` months when the members in `out` (years) are replaced."""
    n, dec = F(n), F(months, 12)
    out = [F(o) for o in out]
    y = sum(out)
    tot = y - n * dec
    v = tot / len(out)
    if pair:
        yy, mm = int(v), (v - int(v)) * 12
        assert mm.denominator == 1
        fin, ans = rf"\({yy}\) years \({mm}\) months", ("pair", (F(yy), mm))
    else:
        fin, ans = UU(v, "years"), ("number", v)
    trad = [("Fall in the total.", rf"\({months}\) months \(= \frac{{{months}}}{{12}} = {nf(dec)}\) year; the average of \({tex(n)}\) falls by it, so the total falls by "
                                   rf"\({tex(n)}\times {nf(dec)} = {nf(n * dec)}\) years."),
            ("What the new ones bring.", leavers(out, "The") + rf" years minus the fall: \[ {nf(y)} - {nf(n * dec)} = {nf(tot)} \]")]
    if several:
        trad.append(("Their average.", rf"\[ {nf(tot)} \div {len(out)} = {nf(v)} \]"))
    if pair:
        trad.append(("In years and months.", rf"\({nf(v)}\) years \(= {yy}\) years and \({nf(v - yy)}\times 12 = {mm}\) months."))
    rule = [("Identify the values.", rf"\(n = {tex(n)}\), \(x = {nf(dec)}\) year, \(y = {nf(y)}\)."), apply(11),
            ("Substitute the values.", rf"\[ {nf(y)} - {tex(n)}\times {nf(dec)} = {nf(tot)} \]" + (rf"shared by \({len(out)}\): \[ {nf(tot)} \div {len(out)} = {nf(v)} \]" if several else ""))]
    sc = rf"\[ {nf(y)} - {tex(n)}\times \frac{{{months}}}{{12}} = {nf(tot)} \]" + (rf"\[ {nf(tot)} \div {len(out)} = {nf(v)} \]" if several else "")
    return result(ans, T11, steps(*trad), steps(*rule), fin, [rf"Fall \(= {nf(n * dec)}\) years.", rf"New ones \(= {nf(tot)}\) years.", rf"Answer \(= {nf(v)}\) years."], sc)


CARDS = {
    6: card(6, "One Quantity Taken Away", r"The total of all minus the total of the rest is the quantity that left.", r"\[ n(x-y)+y \]",
            [("All", r"n\ \text{at}\ x\Rightarrow nx"), ("Rest", r"(n-1)\ \text{at}\ y"), ("Taken away", r"nx-(n-1)y = n(x-y)+y")],
            r"Each of the \(n\) places lost \(x-y\) when the quantity left, and the one that left also took the new average \(y\) with it.",
            "'The average of n students and the teacher is x; leaving the teacher out, the average falls by d; find the teacher's age.' (count the teacher in n)",
            r"\(20\) people average \(30\); one leaves and the rest average \(29\): \(20(30-29)+29=49\).", r"Using the number of students for \(n\) and forgetting the teacher."),
    7: card(7, "Same Number Added to or Taken from Every Number", r"Adding \(x\) to every number adds \(x\) to the average; taking it away takes \(x\) off.",
            r"\[ m\pm x \]", [("Each number", r"a_i\to a_i\pm x"), ("Total", r"nm\to nm\pm nx"), ("Average", r"m\pm x")],
            r"The total changes by \(nx\) and is shared again by the same \(n\), so the average changes by exactly \(x\) - the count does not matter.",
            "'The average of n numbers is m; if x is added to (subtracted from) each, find the new average.'", r"Average \(20\), add \(4\) to each: new average \(24\).",
            r"Multiplying \(x\) by \(n\) before adding it to the average."),
    8: card(8, "A New Quantity Joins", r"The total after minus the total before is the newcomer.", r"\[ n(y-x)+y \]",
            [("Before", r"n\ \text{at}\ x\Rightarrow nx"), ("After", r"(n+1)\ \text{at}\ y"), ("Newcomer", r"(n+1)y-nx = n(y-x)+y")],
            r"The newcomer lifts each of the old \(n\) by \(y-x\) and also keeps the new average \(y\) for itself.",
            "'The average age of n boys is x; with the teacher's age included the average becomes y; find the teacher's age.'",
            r"\(15\) boys average \(12\); with the teacher the average is \(13\): \(15(13-12)+13=28\).", r"Taking \((n+1)\) in place of \(n\) in front of the bracket."),
    9: card(9, "Every Number Multiplied or Divided", r"Multiplying (dividing) every number by \(x\) multiplies (divides) the average by \(x\).",
            r"\[ mx \quad\text{or}\quad \frac{m}{x} \]", [("Each number", r"a_i\to a_i x"), ("Total", r"nm\to nmx"), ("Average", r"mx")],
            r"The total is multiplied by \(x\) and the count stays \(n\), so the average is multiplied by \(x\) too.",
            "'The average of n numbers is m; if each is multiplied (divided) by x, find the average of the new numbers.'",
            r"Average \(15\), each number times \(4\): new average \(60\).", r"Dividing by \(n\) again after multiplying the average."),
    10: card(10, "Members Replaced - the Average Goes Up", r"The new members bring what the old ones had plus the rise in the total.", r"\[ y+nx \]",
             [("Rise in total", r"n\times x"), ("Leavers", r"y"), ("New members", r"y+nx")],
             r"If the average of all \(n\) rises by \(x\), the total rises by \(nx\); only the new members can have brought that extra. When the average stays the same "
             r"after some years, the new member is younger by the rise that did not come (\(n\times\) years).",
             "'The average weight of n persons increases by x kg when a man weighing y kg is replaced; find the new man's weight.'",
             r"\(6\) men, average up by \(2\) kg when a man of \(60\) kg is replaced: \(60+12=72\) kg.", r"Adding only \(x\) (not \(nx\)) to the leaver's weight."),
    11: card(11, "Members Replaced - the Average Goes Down", r"The new members bring what the old ones had minus the fall in the total.", r"\[ y-nx \]",
             [("Fall in total", r"n\times x"), ("Leavers", r"y"), ("New members", r"y-nx")],
             r"If the average of \(n\) falls by \(x\), the total falls by \(nx\), so the newcomers together are \(nx\) less than the leavers. Change months to years first.",
             "'In a class of n boys the average age is decreased by x months when a boy aged y years is replaced by a new boy; find his age.'",
             r"\(24\) boys, average down by \(6\) months when a boy of \(20\) is replaced: \(20-24\times\frac{1}{2}=8\) years.", r"Mixing months and years in \(nx\)."),
}
OLD = {   # row: (rule, question, builder, unit)
    503: (6, "The average age of 29 players and their coach is 22 years. If the coach is left out, the average falls by 1 year. How old is the coach?",
          lambda: r6_removed(30, 22, None, "years", drop=1), "years"),
    504: (6, "The total age of 21 people in a tour group is 399 years. One of them is the guide and the rest are tourists. If the guide's age is left out, the average falls by 2 years. How old is the guide?",
          lambda: r6_removed(21, None, None, "years", total=399, drop=2), "years"),
    505: (8, "The average weight of 23 boxes on a truck is 40 kg. When one more box is loaded, the average weight goes up by 1 kg. How heavy is the new box?",
          lambda: r8_added(23, 40, 41, "kg"), "kg"),
}
NEW = {   # rule: [(key, question, builder, unit, wrong options or None)]
    6: [("r6_ex", "The average weight of 19 sacks and one box is 34 kg. When the box is taken away, the average becomes 32 kg. What does the box weigh?",
         lambda: r6_removed(20, 34, 32, "kg"), "kg", None),
        ("r6_e3", "The average score of 27 pupils and their teacher in a quiz is 41. Without the teacher's score, the average drops by 1. What did the teacher score?",
         lambda: r6_removed(28, 41, None, "", drop=1), "", None),
        ("r6_e4", "The average age of 17 nurses and a doctor is 26 years. If the doctor's age is not counted, the average goes down by 2 years. Find the doctor's age.",
         lambda: r6_removed(18, 26, None, "years", drop=2), "years", None),
        ("r6_e5", "The average age of 11 dancers and their trainer is 21 years. Leaving out the trainer, the average comes down by 1 year. How old is the trainer?",
         lambda: r6_removed(12, 21, None, "years", drop=1), "years", None)],
    7: [("r7_ex1", "The average of 13 numbers is 27. If 6 is added to each number, what is the new average?", lambda: r7_shift(13, 27, 6), "", None),
        ("r7_ex2", "The average of 9 numbers is 44. If 7 is taken away from each number, what is the new average?", lambda: r7_shift(9, 44, -7), "", None),
        ("r7_e1", "The average of 18 numbers is 36. If 8 is added to every number, find the new average.", lambda: r7_shift(18, 36, 8), "", None),
        ("r7_e2", r"The average of \(x\) numbers is \(5x\). If \(x\) is added to each number, what is the new average?", r7_e2, "expr", [r"\(5x+1\)", r"\(4x\)", r"\(7x\)"]),
        ("r7_e3", "The average of 12 numbers is 23. If 5 is subtracted from each number, find the new average.", lambda: r7_shift(12, 23, -5), "", None),
        ("r7_e4", r"The average of \(x\) numbers is \(4x\). If \(x+2\) is subtracted from each number, what is the new average?", r7_e4, "expr",
         [r"\(3x+2\)", r"\(5x+2\)", r"\(4x-2\)"])],
    8: [("r8_ex", "The average age of 26 members of a choir is 20 years. When the age of the conductor is included, the average becomes 21 years. How old is the conductor?",
         lambda: r8_added(26, 20, 21, "years"), "years", None),
        ("r8_e1", "The average age of 33 workers in a shop is 32 years. If the manager's age is included, the average becomes 33 years. What is the manager's age?",
         lambda: r8_added(33, 32, 33, "years"), "years", None),
        ("r8_e2", "The average age of 20 girls in a team is 13 years. With the coach's age included, the average becomes 15 years. How old is the coach?",
         lambda: r8_added(20, 13, 15, "years"), "years", None),
        ("r8_e3", "The average age of 29 people on a bus is 28 years. When the driver's age is included, the average becomes 29 years. Find the driver's age.",
         lambda: r8_added(29, 28, 29, "years"), "years", None),
        ("r8_e4", "The average age of 50 pupils in a class is 12.96 years. When a new pupil joins, the average becomes 13 years. How old is the new pupil?",
         lambda: r8_added(50, F("12.96"), 13, "years"), "years", None),
        ("r8_e5", "The average age of 24 children in a group is 8 years. If the leader's age is included, the average becomes 9 years. How old is the leader?",
         lambda: r8_added(24, 8, 9, "years"), "years", None)],
    9: [("r9_ex1", "The average of 14 numbers is 26. If each number is multiplied by 3, what is the average of the new numbers?", lambda: r9_scale(14, 26, 3, "x"), "", None),
        ("r9_ex2", "The average of 16 numbers is 48. If each number is divided by 6, what is the average of the new numbers?", lambda: r9_scale(16, 48, 6, "/"), "", None),
        ("r9_e1", r"The average of \(x\) numbers is \(y\). If each number is multiplied by \(x+1\), what is the average of the new numbers?", r9_e1, "expr",
         [r"\(xy\)", r"\(x+y\)", r"\((x-1)y\)"]),
        ("r9_e2", "The average of 11 numbers is 34. If each number is multiplied by 4, find the new average.", lambda: r9_scale(11, 34, 4, "x"), "", None),
        ("r9_e3", "The average of 22 numbers is 77. If each number is divided by 7, what is the new average?", lambda: r9_scale(22, 77, 7, "/"), "", None),
        ("r9_e4", "The average of 30 numbers is 336. If each number is divided by 12, find the new average.", lambda: r9_scale(30, 336, 12, "/"), "", None),
        ("r9_e5", "The average of 5 numbers is 23. If each number is multiplied by 6, what is the new average?", lambda: r9_scale(5, 23, 6, "x"), "", None)],
    10: [("r10_ex1", "The average weight of 5 boxers goes up by 2 kg when one of them, who weighs 74 kg, is replaced by a new boxer. How much does the new boxer weigh?",
          lambda: r10_up(5, 2, [74], "kg"), "kg", None),
         ("r10_ex2", "The average age of 9 members of a board goes up by 4 years when two men aged 41 and 49 years are replaced by two women. What is the average age of the two women?",
          lambda: r10_up(9, 4, [41, 49], "years", True), "years", None),
         ("r10_e1", "The average weight of 6 people goes up by 2.5 kg when a person weighing 58 kg is replaced by a new one. What is the weight of the new person?",
          lambda: r10_up(6, F("2.5"), [58], "kg"), "kg", None),
         ("r10_e2", "The average weight of 12 boys goes up by 1.5 kg when a boy weighing 47 kg is replaced by a new boy. Find the weight of the new boy.",
          lambda: r10_up(12, F("1.5"), [47], "kg"), "kg", None),
         ("r10_e3", "The average weight of 14 men goes up by 3 kg when one man weighing 55 kg is replaced by another. Find the weight of the new man.",
          lambda: r10_up(14, 3, [55], "kg"), "kg", None),
         ("r10_e4", "The average age of a panel of 9 judges is the same as it was 4 years ago, because a younger judge has taken the place of one of them. "
                    "How much younger is the new judge than the one replaced?", lambda: r10_same(9, 4), "years", None),
         ("r10_e5", "The average age of 12 members of a club goes up by 2 years when two men aged 44 and 46 years are replaced by two women. What is the average age of the two women?",
          lambda: r10_up(12, 2, [44, 46], "years", True), "years", None),
         ("r10_e6", "The average age of 13 persons in a team goes up by 1 year when three men aged 26, 30 and 34 years are replaced by three women. Find the average age of the three women.",
          lambda: r10_up(13, 1, [26, 30, 34], "years", True), "years", [34, 35, F(104, 3)]),
         ("r10_e7", "The average weight of the 10 rowers in a boat goes up by 1 kg when one of them, who weighs 62 kg, is replaced by a new rower. What does the new rower weigh?",
          lambda: r10_up(10, 1, [62], "kg"), "kg", None),
         ("r10_e8", "The average weight of 7 people goes up by 3.5 kg when one of them, weighing 61 kg, is replaced by a new person. What is the weight of the new person?",
          lambda: r10_up(7, F("3.5"), [61], "kg"), "kg", None)],
    11: [("r11_ex", "In a class of 30 boys, the average age goes down by 3 months when a boy aged 19 years is replaced by a new boy. Find the age of the new boy.",
          lambda: r11_down(30, 3, [19], pair=True), "pair", [(12, 6), (10, 6), (11, 9)]),
         ("r11_e1", "In a class of 12 boys, the average age goes down by 6 months when a boy aged 17 years is replaced by a new boy. Find the age of the new boy.",
          lambda: r11_down(12, 6, [17]), "years", None),
         ("r11_e2", "In a group of 48 girls, the average age goes down by 2 months when a girl aged 22 years is replaced by a new girl. Find the age of the new girl.",
          lambda: r11_down(48, 2, [22]), "years", None),
         ("r11_e3", "In a team of 12 players, the average age goes down by 4 months when a player aged 26 years is replaced by a new player. Find the age of the new player.",
          lambda: r11_down(12, 4, [26]), "years", None),
         ("r11_e4", "In a class of 30 students, the average age goes down by 2 months when 4 students aged 14, 15, 17 and 18 years are replaced by 4 new students. "
                    "Find the average age of the new students.", lambda: r11_down(30, 2, [14, 15, 17, 18], True), "years", None),
         ("r11_e5", "In a class of 24 pupils, the average age goes down by 3 months when 3 pupils aged 13, 14 and 15 years are replaced by 3 new pupils. "
                    "Find the average age of the new pupils.", lambda: r11_down(24, 3, [13, 14, 15], True), "years", None),
         ("r11_e6", "In a club of 20 members, the average age goes down by 6 months when 2 members aged 35 and 39 years are replaced by 2 new members. "
                    "Find the average age of the new members.", lambda: r11_down(20, 6, [35, 39], True), "years", None)],
}


def build_opts(g, unit, wrong):
    """options for one question: numbers with their unit, algebraic expressions, or years-and-months pairs."""
    v = g["answer"][1]
    if unit == "expr":
        return place(g["solution"][g["solution"].rfind("Final Answer: ") + 14:].split("</b>")[0], wrong)
    if unit == "pair":
        f = lambda p: rf"\({p[0]}\) years \({p[1]}\) months"
        return place(f((int(v[0]), int(v[1]))), [f(w) for w in wrong])
    return opts(v, unit, wrong)


def answer_json(a):
    return [a[0], [str(x) for x in a[1]] if isinstance(a[1], tuple) else str(a[1])]


def main():
    for rule in range(6, 12):
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
            op, pos = build_opts(g, unit, wrong)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        json.dump({"rules_html": [{"chapter": "average", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(ids)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
