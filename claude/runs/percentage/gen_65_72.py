"""Rules 65-72: writes the eight rule cards, regenerates the old rows 650 (Rule 65), 651 (66), 652 (67), 653 (68), 654 (69),
655 (71) and 656 (72) in the prompt #12 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer),
links them and cleans their text and options (650 had a NULL option; 655's "failed = .., passed = .." options reduced to the
pass percentage asked), and adds the book exercises (numbers changed, wording rewritten) plus Rule 70's worked example (Rule 70
had no row) as one JsonImport payload per rule."""
import json, os, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from gen_1_8 import result  # noqa: E402
from gen_33_40 import D, PD  # noqa: E402


def L(v):
    return rf"\({D(v)}\) litres"


def two(a, b):
    return rf"\({D(a)}\) and \({D(b)}\)"


# ---------------------------------------------------------------- Rule 65: split N so one part is p% of the other
T65 = r"To split a number \(N\) into two parts such that one part is \(p\%\) of the other, the parts are<br>\[ \frac{100}{100 + p}\times N\quad\text{and}\quad \frac{p}{100 + p}\times N \]"


def split(N, p):
    N, p = F(N), F(p)
    big, small = 100 * N / (100 + p), p * N / (100 + p)
    trad = steps(
        ("Form the equation.", rf"Let the larger part be \(x\); the other part is \({D(p)}\%\) of it, \(\frac{{{D(p)}}}{{100}}x\):<br>\[ x + \frac{{{D(p)}}}{{100}}x = {D(N)} \]"),
        ("Solve.", rf"\[ \frac{{{D(100 + p)}}}{{100}}x = {D(N)} \Rightarrow x = {D(big)},\qquad {D(N)} - {D(big)} = {D(small)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(N = {D(N)}\), \(p = {D(p)}\)."),
        ("Apply the specified rule.", r"\[ \frac{100}{100 + p}N\quad\text{and}\quad \frac{p}{100 + p}N \]"),
        ("Substitute the values.", rf"\[ \frac{{100}}{{{D(100 + p)}}}\times {D(N)} = {D(big)},\qquad \frac{{{D(p)}}}{{{D(100 + p)}}}\times {D(N)} = {D(small)} \]"))
    rb = [rf"\(N = {D(N)}\), \(p = {D(p)}\).", r"Parts \(= \frac{100N}{100 + p}\) and \(\frac{pN}{100 + p}\).", rf"\({D(big)}\) and \({D(small)}\)."]
    sc = rf"\[ \frac{{100\times {D(N)}}}{{{D(100 + p)}}} = {D(big)},\qquad \frac{{{D(p)}\times {D(N)}}}{{{D(100 + p)}}} = {D(small)} \]"
    return result(("pair", (big, small)), T65, trad, rule, two(big, small), rb, sc)


# ---------------------------------------------------------------- Rules 66 and 67: tank still x% empty
T66 = r"If \(X\) litres of oil are poured into a tank and it is still \(x\%\) empty, the oil needed to fill it to the brim is<br>\[ \frac{X\times x}{100 - x}\text{ litres} \]"
T67 = r"If \(X\) litres of oil are poured into a tank and it is still \(x\%\) empty, the capacity of the tank is<br>\[ \frac{X\times 100}{100 - x}\text{ litres} \]"


def tank(X, x, ask):
    X, x = F(X), F(x)
    C = X * 100 / (100 - x)
    more = C - X
    trad = steps(
        ("What the oil fills.", rf"The tank is \({D(x)}\%\) empty, so the \({D(X)}\) litres fill \(100 - {D(x)} = {D(100 - x)}\%\) of it."),
        ("Use the unitary method.", rf"\({D(100 - x)}\%\to {D(X)}\) litres, so \(100\%\to \frac{{{D(X)}\times 100}}{{{D(100 - x)}}} = {D(C)}\) litres (the capacity)."))
    if ask == "more":
        trad += "<br><br>" + rf"<b>Step 3: Find the oil still needed.</b><br>\[ {D(C)} - {D(X)} = {D(more)}\text{{ litres}} \]"
        rule = steps(
            ("Identify the values.", rf"\(X = {D(X)}\), \(x = {D(x)}\)."),
            ("Apply the specified rule.", r"\[ \frac{X\times x}{100 - x} \]"),
            ("Substitute the values.", rf"\[ \frac{{{D(X)}\times {D(x)}}}{{100 - {D(x)}}} = \frac{{{D(X * x)}}}{{{D(100 - x)}}} = {D(more)} \]"))
        rb = [rf"\(X = {D(X)}\), \(x = {D(x)}\).", r"Oil needed \(= \frac{Xx}{100 - x}\).", rf"\(\frac{{{D(X * x)}}}{{{D(100 - x)}}} = {D(more)}\) litres."]
        sc = rf"\[ \frac{{{D(X)}\times {D(x)}}}{{100 - {D(x)}}} = {D(more)}\text{{ litres}} \]"
        return result(("number", more), T66, trad, rule, L(more), rb, sc)
    rule = steps(
        ("Identify the values.", rf"\(X = {D(X)}\), \(x = {D(x)}\)."),
        ("Apply the specified rule.", r"\[ \frac{X\times 100}{100 - x} \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(X)}\times 100}}{{100 - {D(x)}}} = \frac{{{D(X * 100)}}}{{{D(100 - x)}}} = {D(C)} \]"))
    rb = [rf"\(X = {D(X)}\), \(x = {D(x)}\).", r"Capacity \(= \frac{100X}{100 - x}\).", rf"\(\frac{{{D(X * 100)}}}{{{D(100 - x)}}} = {D(C)}\) litres."]
    sc = rf"\[ \frac{{{D(X)}\times 100}}{{100 - {D(x)}}} = {D(C)}\text{{ litres}} \]"
    return result(("number", C), T67, trad, rule, L(C), rb, sc)


# ---------------------------------------------------------------- Rules 68 and 69: three successive changes
T68 = (r"If a number is successively increased by \(x\%\), \(y\%\) and \(z\%\), the single equivalent increase is<br>"
       r"\[ \left[(x + y + z) + \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\% \]")
T69 = (r"If three successive discounts of \(x\%\), \(y\%\) and \(z\%\) are allowed, the single equivalent discount is<br>"
       r"\[ \left[x + y + z - \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\% \]")


def three(n, x, y, z):
    x, y, z = F(x), F(y), F(z)
    s = 1 if n == 68 else -1
    cur, rows = F(100), []
    for p in (x, y, z):
        ch = cur * p / 100
        new = cur + s * ch
        rows.append(rf"\({D(p)}\%\) of \({D(cur)} = {D(ch)}\): \({D(cur)} {'+' if s > 0 else '-'} {D(ch)} = {D(new)}\)")
        cur = new
    v = cur - 100 if s > 0 else 100 - cur
    S1, S2, S3 = x + y + z, (x * y + y * z + z * x) / 100, x * y * z / 10000
    trad = steps(("Start from 100.", "<br>".join(rows)),
                 ("Compare with 100.", rf"\[ {'%s - 100' % D(cur) if s > 0 else '100 - %s' % D(cur)} = {D(v)} \]"))
    sg = "+" if s > 0 else "-"
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\)."),
        ("Apply the specified rule.", rf"\[ (x + y + z) {sg} \frac{{xy + yz + zx}}{{100}} + \frac{{xyz}}{{100^2}} \]"),
        ("Substitute the values.", rf"\[ {D(S1)} {sg} \frac{{{D(x * y)} + {D(y * z)} + {D(z * x)}}}{{100}} + \frac{{{D(x * y * z)}}}{{10000}} = {D(S1)} {sg} {D(S2)} + {D(S3)} = {D(v)} \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\), \(z = {D(z)}\).", rf"\((x + y + z) {sg} \frac{{xy + yz + zx}}{{100}} + \frac{{xyz}}{{100^2}}\).",
          rf"\({D(S1)} {sg} {D(S2)} + {D(S3)} = {D(v)}\%\)."]
    sc = rf"\[ {D(S1)} {sg} {D(S2)} + {D(S3)} = {D(v)}\% \]"
    return result(("number", v), T68 if n == 68 else T69, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- Rule 70: new expenditure as a ratio
T70 = (r"If the price changes by \(x\%\) and the consumption by \(y\%\), then<br>\[ \frac{\text{New expenditure}}{\text{Initial expenditure}} = "
       r"\frac{(100 \pm x)(100 \pm y)}{100^2} \]taking \(+\) for an increase and \(-\) for a decrease.")


def exp_ratio(a, b):
    """a, b = signed % changes of price and consumption."""
    a, b = F(a), F(b)
    num = (100 + a) * (100 + b)
    g = gcd(int(num), 10000)
    r = (int(num) // g, 10000 // g)
    sg = lambda v: f"+ {D(v)}" if v > 0 else f"- {D(-v)}"
    trad = steps(
        ("Take price and consumption as 100 each.", r"Initial expenditure \(= 100\times 100 = 10000\)."),
        ("Apply the changes.", rf"Price \(= 100 {sg(a)} = {D(100 + a)}\), consumption \(= 100 {sg(b)} = {D(100 + b)}\), new expenditure \(= {D(num)}\)."),
        ("Write the ratio.", rf"\[ {D(num)} : 10000 = {r[0]} : {r[1]} \]"))
    rule = steps(
        ("Identify the values.", rf"Price \({sg(a)}\%\), consumption \({sg(b)}\%\)."),
        ("Apply the specified rule.", r"\[ \frac{(100 \pm x)(100 \pm y)}{100^2} \]"),
        ("Substitute the values.", rf"\[ \frac{{(100 {sg(a)})(100 {sg(b)})}}{{100^2}} = \frac{{{D(100 + a)}\times {D(100 + b)}}}{{10000}} = \frac{{{r[0]}}}{{{r[1]}}} \]"))
    rb = [rf"Price \({sg(a)}\%\), consumption \({sg(b)}\%\).", r"Ratio \(= \frac{(100 \pm x)(100 \pm y)}{100^2}\).",
          rf"\(\frac{{{D(num)}}}{{10000}} = {r[0]} : {r[1]}\)."]
    sc = rf"\[ \frac{{{D(100 + a)}\times {D(100 + b)}}}{{10000}} = {r[0]} : {r[1]} \]"
    return result(("ratio", r), T70, trad, rule, rf"\({r[0]} : {r[1]}\)", rb, sc)


# ---------------------------------------------------------------- Rule 71: three subjects
T71 = (r"If the percentages failing in each of three subjects, in each pair and in all three are known, then<br>"
       r"\[ n(A\cup B\cup C) = n(A) + n(B) + n(C) - n(A\cap B) - n(B\cap C) - n(A\cap C) + n(A\cap B\cap C) \]"
       r"is the percentage who failed in at least one subject; the rest passed in all three.")


def three_subjects(m, e, h, me, eh, mh, al):
    m, e, h, me, eh, mh, al = map(F, (m, e, h, me, eh, mh, al))
    only_me, only_eh, only_mh = me - al, eh - al, mh - al
    only_m, only_e, only_h = m - only_me - only_mh - al, e - only_me - only_eh - al, h - only_eh - only_mh - al
    failed = only_m + only_e + only_h + only_me + only_eh + only_mh + al
    v = 100 - failed
    trad = steps(
        ("Fill in the Venn diagram from the middle.", rf"All three: \({D(al)}\). Exactly two: Maths and English \({D(me)} - {D(al)} = {D(only_me)}\), "
                                                      rf"English and Hindi \({D(eh)} - {D(al)} = {D(only_eh)}\), Maths and Hindi \({D(mh)} - {D(al)} = {D(only_mh)}\).<br>"
                                                      rf"Only one: Maths \({D(only_m)}\), English \({D(only_e)}\), Hindi \({D(only_h)}\)."),
        ("Add every region.", rf"\[ {D(only_m)} + {D(only_e)} + {D(only_h)} + {D(only_me)} + {D(only_eh)} + {D(only_mh)} + {D(al)} = {D(failed)}\% \]"),
        ("The rest passed in all three.", rf"\[ 100 - {D(failed)} = {D(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(n(M) = {D(m)}\), \(n(E) = {D(e)}\), \(n(H) = {D(h)}\), \(n(M\cap E) = {D(me)}\), \(n(E\cap H) = {D(eh)}\), "
                                 rf"\(n(M\cap H) = {D(mh)}\), \(n(M\cap E\cap H) = {D(al)}\)."),
        ("Apply the specified rule.", r"\[ n(M\cup E\cup H) = n(M) + n(E) + n(H) - n(M\cap E) - n(E\cap H) - n(M\cap H) + n(M\cap E\cap H) \]"),
        ("Substitute the values.", rf"\[ {D(m)} + {D(e)} + {D(h)} - {D(me)} - {D(eh)} - {D(mh)} + {D(al)} = {D(failed)}\% \]"
                                   rf"\[ \text{{Passed in all three}} = 100 - {D(failed)} = {D(v)}\% \]"))
    rb = ["Failed in at least one \\(= n(M) + n(E) + n(H) - \\) pairs \\(+\\) all three.",
          rf"\({D(m + e + h)} - {D(me + eh + mh)} + {D(al)} = {D(failed)}\%\).", rf"Passed \(= 100 - {D(failed)} = {D(v)}\%\)."]
    sc = rf"\[ 100 - ({D(m + e + h)} - {D(me + eh + mh)} + {D(al)}) = {D(v)}\% \]"
    return result(("number", v), T71, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- Rule 72: houses with one female
T72 = (r"In a survey \(x\%\) of houses contain two or more people. Of the houses with only one person, \(y\%\) have only a male. The percentage of "
       r"all houses with exactly one female and no male is<br>\[ \frac{(100 - x)(100 - y)}{100}\% \]")


def houses(x, y):
    x, y = F(x), F(y)
    one = 100 - x
    male = one * y / 100
    v = one - male
    trad = steps(
        ("Take 100 houses.", rf"Houses with one person \(= 100 - {D(x)} = {D(one)}\)."),
        ("Remove the one-male houses.", rf"\({D(y)}\%\) of \({D(one)} = {D(male)}\) have only a male, so \({D(one)} - {D(male)} = {D(v)}\) have only a female."))
    rule = steps(
        ("Identify the values.", rf"\(x = {D(x)}\), \(y = {D(y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{(100 - x)(100 - y)}{100}\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{D(100 - x)}\times {D(100 - y)}}}{{100}} = {D(v)}\% \]"))
    rb = [rf"\(x = {D(x)}\), \(y = {D(y)}\).", r"One female only \(= \frac{(100 - x)(100 - y)}{100}\%\).", rf"\(\frac{{{D(100 - x)}\times {D(100 - y)}}}{{100}} = {D(v)}\%\)."]
    sc = rf"\[ \frac{{{D(100 - x)}\times {D(100 - y)}}}{{100}} = {D(v)}\% \]"
    return result(("number", v), T72, trad, rule, PD(v), rb, sc)


# ---------------------------------------------------------------- rule cards
CARDS = {
    65: card(65, "Split a Number So One Part Is p% of the Other",
             r"To split \(N\) into two parts such that one part is \(p\%\) of the other, the parts are \(\frac{100}{100 + p}N\) and \(\frac{p}{100 + p}N\).",
             r"\[ \text{Parts} = \frac{100}{100 + p}\times N\quad\text{and}\quad \frac{p}{100 + p}\times N \]",
             [("Larger part", "100\\text{ shares}"), ("Smaller part", "p\\text{ shares}"), ("Whole", "100 + p\\text{ shares} = N")],
             r"The two parts are in the ratio \(100 : p\), so \(N\) is divided in that ratio.",
             "'Split N into two parts such that one part is p% of the other.'",
             r"120, \(20\%\): \(\frac{100}{120}\times 120 = 100\) and \(20\).", r"Taking \(p\%\) of \(N\) itself as one part."),
    66: card(66, "Oil Still Needed to Fill a Tank",
             r"If \(X\) litres are poured into a tank and it is still \(x\%\) empty, the oil needed to fill it to the brim is \(\frac{Xx}{100 - x}\) litres.",
             r"\[ \text{Oil needed} = \frac{X\times x}{100 - x}\text{ litres} \]",
             [("Filled part", r"(100 - x)\% = X"), ("Empty part", r"x\%"), ("Oil needed", r"\frac{X}{100 - x}\times x")],
             r"\(X\) fills \((100 - x)\%\), so each 1% holds \(\frac{X}{100 - x}\) litres and the empty \(x\%\) holds \(x\) times that.",
             "'X litres poured in, tank still x% empty: how much more to fill it?'",
             r"240 litres, \(20\%\) empty: \(\frac{240\times 20}{80} = 60\) litres.", r"Taking \(x\%\) of \(X\) (gives 48, which is wrong)."),
    67: card(67, "Capacity of a Tank Still x% Empty",
             r"If \(X\) litres are poured into a tank and it is still \(x\%\) empty, the capacity of the tank is \(\frac{100X}{100 - x}\) litres.",
             r"\[ \text{Capacity} = \frac{X\times 100}{100 - x}\text{ litres} \]",
             [("Filled part", r"(100 - x)\% = X"), ("1%", r"\frac{X}{100 - x}"), ("Capacity (100%)", r"\frac{100X}{100 - x}")],
             r"The oil poured in is \((100 - x)\%\) of the tank - Rule 4 again.",
             "'X litres poured in, tank still x% empty: find the capacity.'",
             r"240 litres, \(20\%\) empty: \(\frac{24000}{80} = 300\) litres.", r"Adding \(x\%\) of \(X\) to \(X\)."),
    68: card(68, "Three Successive Increases",
             r"If a number is increased successively by \(x\%\), \(y\%\) and \(z\%\), the single equivalent increase is "
             r"\(\left[(x + y + z) + \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\%\).",
             r"\[ \left[(x + y + z) + \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\% \]",
             [("Start", "100"), ("After three increases", r"100\times\frac{100 + x}{100}\times\frac{100 + y}{100}\times\frac{100 + z}{100}")],
             r"Multiplying out \((100 + x)(100 + y)(100 + z)\) gives exactly these three groups of terms.",
             "Three successive increases (or profits); the single equivalent % increase is asked.",
             r"\(10, 15, 20\): \(45 + 6.5 + 0.3 = 51.8\%\).", r"Adding \(x + y + z\) only."),
    69: card(69, "Three Successive Discounts",
             r"If three successive discounts of \(x\%\), \(y\%\) and \(z\%\) are allowed, the single equivalent discount is "
             r"\(\left[x + y + z - \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\%\).",
             r"\[ \left[x + y + z - \frac{xy + yz + zx}{100} + \frac{xyz}{100^2}\right]\% \]",
             [("Start", "100"), ("After three discounts", r"100\times\frac{100 - x}{100}\times\frac{100 - y}{100}\times\frac{100 - z}{100}")],
             r"Each discount is taken on the price left by the earlier ones, so the factors multiply.",
             "A discount series of x%, y%, z%: the single equivalent discount is asked.",
             r"\(20, 10, 5\): \(35 - 3.5 + 0.1 = 31.6\%\).", r"Adding the three discounts (\(35\%\))."),
    70: card(70, "New Expenditure as a Ratio",
             r"If the price changes by \(x\%\) and the consumption by \(y\%\), the new expenditure is to the initial expenditure as "
             r"\((100 \pm x)(100 \pm y) : 100^2\) (\(+\) for an increase, \(-\) for a decrease).",
             r"\[ \frac{\text{New expenditure}}{\text{Initial expenditure}} = \frac{(100 \pm x)(100 \pm y)}{100^2} \]",
             [("Initial", r"100\times 100"), ("New", r"(100 \pm x)(100 \pm y)"), ("Ratio", r"(100 \pm x)(100 \pm y) : 10000")],
             r"Expenditure \(=\) Price \(\times\) Consumption, so the two growth factors multiply.",
             "Price and consumption both change; the new expenditure is asked as a ratio of the old one.",
             r"Price \(-20\%\), consumption \(+30\%\): \(\frac{80\times 130}{10000} = \frac{26}{25}\), i.e. \(26 : 25\).",
             r"Using the wrong sign for a decrease, or writing the ratio upside down (old : new)."),
    71: card(71, "Failed in Three Subjects",
             r"With the percentages failing in each subject, each pair and all three, the percentage failing in at least one is "
             r"\(n(A) + n(B) + n(C) - n(A\cap B) - n(B\cap C) - n(A\cap C) + n(A\cap B\cap C)\); the rest passed in all three.",
             r"\[ n(A\cup B\cup C) = n(A) + n(B) + n(C) - n(A\cap B) - n(B\cap C) - n(A\cap C) + n(A\cap B\cap C) \]",
             [("Singles", r"n(A) + n(B) + n(C)"), ("Pairs (subtract)", r"n(A\cap B) + n(B\cap C) + n(A\cap C)"), ("All three (add back)", r"n(A\cap B\cap C)")],
             r"Students in two subjects are counted twice in the singles, those in all three three times; the pair and triple terms correct the count.",
             "Failing percentages in three subjects, in every pair and in all three are given; the % passing in all three is asked.",
             r"\(30 + 25 + 40 - 15 - 20 - 25 + 10 = 45\%\) failed, so \(55\%\) passed.",
             r"Forgetting to add back the students who failed in all three."),
    72: card(72, "Houses with Exactly One Female",
             r"If \(x\%\) of houses have two or more people and \(y\%\) of the one-person houses have only a male, the percentage of all houses with exactly "
             r"one female and no male is \(\frac{(100 - x)(100 - y)}{100}\%\).",
             r"\[ \text{One female only} = \frac{(100 - x)(100 - y)}{100}\% \]",
             [("One-person houses", "100 - x"), ("Only a male", r"\frac{y}{100}(100 - x)"), ("Only a female", r"\frac{(100 - x)(100 - y)}{100}")],
             r"The \(y\%\) is of the one-person houses, not of all houses.",
             "A survey of houses with one or more people; the share of all houses with just one female is asked.",
             r"\(25\%\), \(20\%\): \(\frac{75\times 80}{100} = 60\%\).", r"Taking \(y\%\) of ALL houses (\(100 - 25 - 20 = 55\%\) is wrong)."),
}

OLD = {
    65: {650: (lambda: split(120, 20), "Split the number 120 into two parts such that one part is 20% of the other.",
               {"a": two(120, 10), "b": two(90, 30), "c": two(96, 24), "d": two(100, 20)})},
    66: {651: (lambda: tank(240, 20, "more"), "240 litres of oil was poured into a tank and it was still 20% empty. How much oil must be poured into "
                                              "the tank in order to fill it to the brim?", {"a": L(32), "b": L(12), "c": L(60), "d": L(30)})},
    67: {652: (lambda: tank(240, 20, "cap"), "240 litres of oil was poured into a tank and it was still 20% empty. Find the capacity of the tank.",
               {"a": L(300), "b": L(200), "c": L(330), "d": L(305)})},
    68: {653: (lambda: three(68, 10, 15, 20), "Find a single equivalent increase if a number is successively increased by 10%, 15% and 20%.",
               {"a": PD(58), "b": PD(F(259, 5)), "c": PD(F(581, 10)), "d": PD(51)})},
    69: {654: (lambda: three(69, 20, 10, 5), "Find a single discount equivalent to a discount series of 20%, 10% and 5%.",
               {"a": PD(13), "b": PD(31), "c": PD(12), "d": PD(F(158, 5))})},
    70: {},
    71: {655: (lambda: three_subjects(30, 25, 40, 15, 20, 25, 10),
               "In an examination 30% of the students failed in Maths, 25% failed in English and 40% failed in Hindi. If 15% of the students failed "
               "in Maths and English, 20% failed in English and Hindi, 25% failed in Maths and Hindi and 10% failed in all three subjects, find the "
               "percentage of students who passed in all three subjects.", {"a": PD(45), "b": PD(60), "c": PD(55), "d": PD(35)})},
    72: {656: (lambda: houses(25, 20), "In a recent survey 25% of houses contained two or more people. Of those houses containing only one person, "
                                       "20% had only a male. What is the percentage of all houses which contain exactly one female and no male?",
               {"a": PD(60), "b": PD(40), "c": PD(20), "d": PD(80)})},
}

SPLIT = "Split the number {} into two parts such that one part is {}% of the other."
MORE = "{} litres of oil was poured into a tank and it was still {}% empty. How much oil must be poured into the tank in order to fill it to the brim?"
CAP = "{} litres of oil was poured into a tank and it was still {}% empty. Find the capacity of the tank."
UP3 = "Find a single equivalent increase if a number is successively increased by {}%, {}% and {}%."
DIS3 = "Find a single discount equivalent to a discount series of {}%, {}% and {}%."
SUBJ = ("In an examination {}% of the students failed in Maths, {}% failed in English and {}% failed in Hindi. If {}% failed in Maths and English, "
        "{}% failed in English and Hindi, {}% failed in Maths and Hindi and {}% failed in all three subjects, find the percentage of students who "
        "passed in all three subjects.")
HOUSE = ("In a recent survey {}% of houses contained two or more people. Of those houses containing only one person, {}% had only a male. "
         "What is the percentage of all houses which contain exactly one female and no male?")
EXP = "The price of {} is {} by {}% and its consumption {} by {}%. Find the new expenditure as a ratio of the initial expenditure."


def exp_q(item, a, b):
    return EXP.format(item, "increased" if a > 0 else "decreased", abs(a), "increases" if b > 0 else "decreases", abs(b))


def R(a, b):
    return rf"\({a} : {b}\)"


NEW = {
    65: [("r65_e%d" % i, SPLIT.format(N, p), (lambda N=N, p=p: split(N, p)), [two(*o) for o in opts], pos)
         for i, (N, p, opts, pos) in enumerate([(180, 20, [(150, 30), (140, 40), (120, 60), (160, 20)], 1),
                                                (135, 35, [(90, 45), (100, 35), (105, 30), (110, 25)], 2),
                                                (260, 30, [(180, 80), (208, 52), (200, 60), (220, 40)], 3),
                                                (46, 15, [(39, 7), (36, 10), (41, 5), (40, 6)], 4),
                                                (57, 14, [(50, 7), (49, 8), (48, 9), (51, 6)], 1)], 1)],
    66: [("r66_e%d" % i, MORE.format(X, x), (lambda X=X, x=x: tank(X, x, "more")), [L(o) for o in opts], pos)
         for i, (X, x, opts, pos) in enumerate([(280, 30, [84, 120, 90, 150], 2), (216, 25, [54, 64, 72, 81], 3), (88, 12, [9, 10, 11, 12], 4),
                                                (850, 15, [150, 120, 170, 180], 1), (492, 18, [90, 108, 100, 120], 2)], 1)],
    67: [("r67_e%d" % i, CAP.format(X, x), (lambda X=X, x=x: tank(X, x, "cap")), [L(o) for o in opts], pos)
         for i, (X, x, opts, pos) in enumerate([(330, 25, [400, 360, 440, 480], 3), (255, 15, [270, 280, 320, 300], 4), (396, 12, [450, 400, 420, 480], 1),
                                                (172, 14, [186, 200, 196, 180], 2), (945, 37, [1300, 1600, 1500, 1200], 3)], 1)],
    68: [("r68_e%d" % i, UP3.format(x, y, z), (lambda x=x, y=y, z=z: three(68, x, y, z)), [PD(o) for o in opts], pos)
         for i, (x, y, z, opts, pos) in enumerate([(5, 10, 20, [35, F(184, 5), F(1903, 50), F(193, 5)], 4), (10, 20, 30, [F(358, 5), 60, F(353, 5), F(363, 5)], 1),
                                                   (20, 25, 40, [85, 110, 105, 100], 2), (10, 25, 40, [75, 90, F(185, 2), 95], 3)], 1)],
    69: [("r69_e%d" % i, DIS3.format(x, y, z), (lambda x=x, y=y, z=z: three(69, x, y, z)), [PD(o) for o in opts], pos)
         for i, (x, y, z, opts, pos) in enumerate([(5, 20, 25, [50, 43, 41, 45], 2), (10, 20, 30, [60, F(252, 5), F(248, 5), F(243, 5)], 3),
                                                   (20, 25, 30, [75, 60, 52, 58], 4), (10, 25, 40, [F(119, 2), 75, F(121, 2), 55], 1)], 1)],
    70: [("r70_ex", exp_q("sugar", -10, 20), lambda: exp_ratio(-10, 20), [R(25, 27), R(27, 25), R(6, 5), R(11, 10)], 2),
         ("r70_e1", exp_q("tea", 20, 20), lambda: exp_ratio(20, 20), [R(25, 36), R(7, 5), R(36, 25), R(6, 5)], 3),
         ("r70_e2", exp_q("rice", 30, -20), lambda: exp_ratio(30, -20), [R(25, 26), R(11, 10), R(21, 20), R(26, 25)], 4),
         ("r70_e3", exp_q("sugar", -20, -25), lambda: exp_ratio(-20, -25), [R(3, 5), R(5, 3), R(11, 20), R(2, 5)], 1),
         ("r70_e4", exp_q("wheat", -20, 20), lambda: exp_ratio(-20, 20), [R(25, 24), R(24, 25), R(4, 5), R(5, 6)], 2)],
    71: [("r71_e%d" % i, SUBJ.format(*v), (lambda v=v: three_subjects(*v)), [PD(o) for o in opts], pos)
         for i, (v, opts, pos) in enumerate([((40, 30, 35, 15, 10, 20, 5), [40, 35, 30, 45], 2), ((30, 35, 40, 10, 15, 20, 8), [40, 24, 32, 30], 3),
                                             ((25, 20, 30, 8, 12, 10, 3), [58, 48, 45, 52], 4)], 1)],
    72: [("r72_e%d" % i, HOUSE.format(x, y), (lambda x=x, y=y: houses(x, y)), [PD(o) for o in opts], pos)
         for i, (x, y, opts, pos) in enumerate([(30, 20, [56, 50, 70, 44], 1), (15, 20, [65, 68, 72, 80], 2),
                                                (35, 12, [53, F(264, 5), F(286, 5), 65], 3), (50, 30, [20, 50, 15, 35], 4)], 1)],
}


def main():
    for n in range(65, 73):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, opts) in OLD[n].items():
            extra = {"question": question, **(opts or {})}
            if rows[rid]["e"] is None or rows[rid]["e"].strip():
                extra["e"] = ""
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn, op, pos in NEW[n]:
            g = fn()
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "percentage", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
