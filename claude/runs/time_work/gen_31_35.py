"""Rules 31-35: regenerates every row in the prompt #11 layout, links the 2018 book copies (Rule 31, the six Rule 32 rows
that had no card, Rules 33-35) and cleans their text (OCR slips, display math in options, units). Rule 32 gets a new card
built on counting complete two-day cycles - the book's 'nearest whole number p' shortcut is not reliable (Ram 10 /
Mohan 8 days needs p = 5 although 80/18 = 4.4). Missing book exercises are added as JsonImport payloads: Rule 31
Exercises 1-5, 7, 8 and Rule 32 Worked Examples (A starts / B starts) + Exercises 1-3, all with changed numbers.
Answer keys come from validate.py (250's key was wrong). Writes ruleNN/2_new_rows.json, rule32/3_rule_card.json,
rule33/3_rule_card.json and rule31/rule32 3_json_import_payload.json + 3_answers.json."""
import json, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import new_question, rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_common import card  # noqa: E402
from gen_1_4 import R, clean, fr, opts, result, xy_body  # noqa: E402
from gen_5_10 import fin_of, plain, r6  # noqa: E402


# ---------------------------------------------------------------- Rule 31: amount of work = days worked / alone time
T31 = (r"If A, B and C can do a job alone in \(x\), \(y\) and \(z\) days and they actually work \(d_1\), \(d_2\) and \(d_3\) days, then the "
       r"amount of work each does is the days worked divided by the alone time, and for a finished job<br>"
       r"\[ \frac{d_1}{x} + \frac{d_2}{y} + \frac{d_3}{z} = 1 \]")
F31 = r"\[ \frac{d_1}{x} + \frac{d_2}{y} + \frac{d_3}{z} = 1 \]"


def boys31(tm, tw, tb, men, women, d):
    left = 1 - F(men * d, tm) - F(women * d, tw)
    x = left / F(d, tb)
    trad = steps(
        ("Find one person's daily work.", rf"A man does \({fr(F(1, tm))}\), a woman \({fr(F(1, tw))}\) and a boy \({fr(F(1, tb))}\) of the job in a day."),
        ("Find what the men and women do in the time.", rf"In \({d}\) days: \({men}\) men do \({men}\times {d}\times {fr(F(1, tm))} = {fr(F(men * d, tm))}\) and "
                                                        rf"\({women}\) women do \({women}\times {d}\times {fr(F(1, tw))} = {fr(F(women * d, tw))}\).<br>"
                                                        rf"\[ \text{{Left for the boys}} = 1 - {fr(F(men * d, tm))} - {fr(F(women * d, tw))} = {fr(left)} \]"),
        ("Find the boys needed.", rf"One boy does \({d}\times {fr(F(1, tb))} = {fr(F(d, tb))}\) in \({d}\) days, so<br>\[ {fr(left)}\div {fr(F(d, tb))} = {tex(x)}\text{{ boys}} \]"))
    rule = steps(("Write the amount of work of each group.", rf"Each group's work \(= \frac{{\text{{number}}\times\text{{days worked}}}}{{\text{{alone time}}}}\); let \(b\) boys help:"),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{men}\times {d}}}{{{tm}}} + \frac{{{women}\times {d}}}{{{tw}}} + \frac{{b\times {d}}}{{{tb}}} = 1 \]"),
                 ("Solve for \\(b\\).", rf"\[ {fr(F(men * d, tm))} + {fr(F(women * d, tw))} + {fr(F(d, tb))}\,b = 1 \;\Rightarrow\; b = {tex(x)} \]"))
    fin = fin_of(x, "boys")
    rb = rbe([rf"Times: man \({tm}\), woman \({tw}\), boy \({tb}\) days; \({men}\) men, \({women}\) women, \({d}\) days.",
              rf"\(\frac{{{men}\times {d}}}{{{tm}}} + \frac{{{women}\times {d}}}{{{tw}}} + \frac{{b\times {d}}}{{{tb}}} = 1\).", rf"\(b = {tex(x)}\)."], fin)
    sc = shortcut(rf"\[ b = \left(1 - {fr(F(men * d, tm))} - {fr(F(women * d, tw))}\right)\div {fr(F(d, tb))} = {tex(x)} \]", fin)
    return result(("number", x), T31, trad, rule, fin, rb, sc)


def pairs31(ab, bc, da, db, dc):
    ab, bc = F(ab), F(bc)
    c = (1 - da / ab - (db - da) / bc) / (dc - (db - da))
    b = 1 / bc - c
    a = 1 / ab - b
    A, B, C = 1 / a, 1 / b, 1 / c
    trad = steps(
        ("Regroup the working days.", rf"A works \({da}\) days, B \({db}\) days and C \({dc}\) days. Pair them up: (A + B) for \({da}\) days, (B + C) for \({db} - {da} = {db - da}\) days, "
                                      rf"and C alone for the other \({dc} - {db - da} = {dc - (db - da)}\) days."),
        ("Find C's one-day work.", rf"\[ {da}\times {fr(1 / ab)} + {db - da}\times {fr(1 / bc)} + {dc - (db - da)}\,\text{{C}} = 1 \]"
                                   rf"\[ {fr(da / ab + (db - da) / bc)} + {dc - (db - da)}\,\text{{C}} = 1 \;\Rightarrow\; \text{{C}} = {fr(c)} \]"),
        ("Find B and A.", rf"\[ \text{{B}} = {fr(1 / bc)} - {fr(c)} = {fr(b)},\qquad \text{{A}} = {fr(1 / ab)} - {fr(b)} = {fr(a)} \]"
                          rf"So A takes \({tex(A)}\), B \({tex(B)}\) and C \({tex(C)}\) days."))
    rule = steps(("Write the amounts of work.", r"Let the alone times be \(x, y, z\). Each person's work is days worked \(\div\) alone time."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{da}}}{{x}} + \frac{{{db}}}{{y}} + \frac{{{dc}}}{{z}} = 1,\quad \frac{{1}}{{x}} + \frac{{1}}{{y}} = {fr(1 / ab)},\quad \frac{{1}}{{y}} + \frac{{1}}{{z}} = {fr(1 / bc)} \]"),
                 ("Solve.", rf"Using the two pair equations, the first becomes \({fr(da / ab + (db - da) / bc)} + \frac{{{dc - (db - da)}}}{{z}} = 1\), so \(z = {tex(C)}\); "
                            rf"then \(y = {tex(B)}\) and \(x = {tex(A)}\)."))
    fin = rf"A \({tex(A)}\) days, B \({tex(B)}\) days, C \({tex(C)}\) days"
    rb = rbe([rf"\(\frac{{{da}}}{{x}} + \frac{{{db}}}{{y}} + \frac{{{dc}}}{{z}} = 1\) with A + B \(= {tex(ab)}\), B + C \(= {tex(bc)}\) days.",
              rf"Pairing the days: \({fr(da / ab + (db - da) / bc)} + \frac{{{dc - (db - da)}}}{{z}} = 1\), so \(z = {tex(C)}\).", rf"\(y = {tex(B)}\), \(x = {tex(A)}\)."], fin)
    sc = shortcut(rf"\[ z = \frac{{{dc - (db - da)}}}{{1 - {fr(da / ab + (db - da) / bc)}}} = {tex(C)};\ y = {tex(B)};\ x = {tex(A)} \]", fin)
    return result(("triple", (A, B, C)), T31, trad, rule, fin, rb, sc)


def helped31(ta, tb, tc, k):
    cyc = F(k, ta) + F(1, tb) + F(1, tc)
    n = math.ceil(1 / cyc) - 1
    done = n * cyc
    t, day = F(n * k), 0
    while True:                                          # finish the last (part) cycle day by day
        day += 1
        rate = F(1, ta) + ((F(1, tb) + F(1, tc)) if day == k else 0)
        if done + rate >= 1:
            T = t + day - 1 + (1 - done) / rate
            break
        done += rate
    trad = steps(
        ("Find the work in one cycle.", rf"Every {k} days A works all {k} days and B and C help on the last one:<br>"
                                        rf"\[ {k}\times {fr(F(1, ta))} + {fr(F(1, tb))} + {fr(F(1, tc))} = {fr(cyc)} \]"),
        ("Count the cycles.", rf"\({fr(cyc)}\) of the job per cycle, so the job needs \(1\div {fr(cyc)} = {tex(1 / cyc)}\) cycles"
                              + (rf", that is \({tex(1 / cyc)}\times {k} = {tex(k / cyc)}\) days." if (1 / cyc).denominator == 1 else ".")),
        ("Read the answer.", rf"The job is finished after \({tex(T)}\) days."))
    rule = steps(("Write the amounts of work.", rf"In \(T\) days A works \(T\) days, and B and C work one day in every {k}, that is \(\frac{{T}}{{{k}}}\) days each."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{T}}{{{ta}}} + \frac{{T/{k}}}{{{tb}}} + \frac{{T/{k}}}{{{tc}}} = 1 \]"),
                 ("Solve.", rf"\[ T\left({fr(F(1, ta))} + {fr(F(1, k * tb))} + {fr(F(1, k * tc))}\right) = 1 \;\Rightarrow\; T = {tex(T)}\text{{ days}} \]"))
    assert T == 1 / (F(1, ta) + F(1, k * tb) + F(1, k * tc)) and (1 / cyc).denominator == 1
    fin = fin_of(T, "days")
    rb = rbe([rf"A works \(T\) days, B and C \(\frac{{T}}{{{k}}}\) days each.", rf"\(\frac{{T}}{{{ta}}} + \frac{{T}}{{{k * tb}}} + \frac{{T}}{{{k * tc}}} = 1\).", rf"\(T = {tex(T)}\)."], fin)
    sc = shortcut(rf"\[ T = 1\div\left({fr(F(1, ta))} + {fr(F(1, k * tb))} + {fr(F(1, k * tc))}\right) = {tex(T)} \]", fin)
    return result(("number", T), T31, trad, rule, fin, rb, sc)


def c_joins31(ta, tb, both, alone, with_c):
    done = both * (F(1, ta) + F(1, tb)) + F(alone, ta)
    c_work = 1 - done - F(with_c, ta)
    C = with_c / c_work
    trad = steps(
        ("Work before C joins.", rf"\[ {both}\left({fr(F(1, ta))} + {fr(F(1, tb))}\right) + {alone}\times {fr(F(1, ta))} = {fr(done)} \]"),
        ("Work done by C.", rf"In the last \({with_c}\) days A does \({fr(F(with_c, ta))}\), so C does<br>\[ 1 - {fr(done)} - {fr(F(with_c, ta))} = {fr(c_work)} \]"),
        ("Find C's time.", rf"C does \({fr(c_work)}\) in \({with_c}\) days:<br>\[ {with_c}\div {fr(c_work)} = {tex(C)}\text{{ days}} \]"))
    rule = steps(("Count each person's days.", rf"A works \({both} + {alone} + {with_c} = {both + alone + with_c}\) days, B works \({both}\) days and C works \({with_c}\) days; let C's time be \(z\)."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{both + alone + with_c}}}{{{ta}}} + \frac{{{both}}}{{{tb}}} + \frac{{{with_c}}}{{z}} = 1 \]"),
                 ("Solve.", rf"\[ \frac{{{with_c}}}{{z}} = 1 - {fr(F(both + alone + with_c, ta) + F(both, tb))} = {fr(c_work)} \;\Rightarrow\; z = {tex(C)} \]"))
    fin = fin_of(C, "days")
    rb = rbe([rf"A works \({both + alone + with_c}\), B \({both}\), C \({with_c}\) days.", rf"\(\frac{{{both + alone + with_c}}}{{{ta}}} + \frac{{{both}}}{{{tb}}} + \frac{{{with_c}}}{{z}} = 1\).",
              rf"\(z = {tex(C)}\)."], fin)
    sc = shortcut(rf"\[ z = {with_c}\div\left(1 - \frac{{{both + alone + with_c}}}{{{ta}}} - \frac{{{both}}}{{{tb}}}\right) = {tex(C)} \]", fin)
    return result(("number", C), T31, trad, rule, fin, rb, sc)


def a_left31(ta, tb, z):
    x = F(ta * (tb - z), ta + tb)
    trad = steps(
        ("Find B's work at the end.", rf"B works alone \({z}\) days: \({z}\times {fr(F(1, tb))} = {fr(F(z, tb))}\)."),
        ("Find the work done together.", rf"\[ 1 - {fr(F(z, tb))} = {fr(1 - F(z, tb))} \]Together they do \({fr(F(1, ta) + F(1, tb))}\) a day."),
        ("Find the days together.", rf"\[ {fr(1 - F(z, tb))}\div {fr(F(1, ta) + F(1, tb))} = {tex(x)}\text{{ days}} \]"))
    rule = steps(("Count each person's days.", rf"If A leaves after \(t\) days, A works \(t\) days and B works \(t + {z}\) days."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{t}}{{{ta}}} + \frac{{t + {z}}}{{{tb}}} = 1 \]"),
                 ("Solve.", rf"\[ {tb}t + {ta}(t + {z}) = {ta * tb} \;\Rightarrow\; {ta + tb}t = {ta * tb - ta * z} \;\Rightarrow\; t = {tex(x)} \]"))
    fin = fin_of(x, "days")
    rb = rbe([rf"A works \(t\), B works \(t + {z}\) days.", rf"\(\frac{{t}}{{{ta}}} + \frac{{t + {z}}}{{{tb}}} = 1\).", rf"\(t = {tex(x)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{t}}{{{ta}}} + \frac{{t + {z}}}{{{tb}}} = 1 \Rightarrow t = {tex(x)} \]", fin)
    return result(("number", x), T31, trad, rule, fin, rb, sc)


def b_first31(ta, tb, d):
    x = (1 - F(d, ta)) * tb - d
    trad = steps(("Find A's share.", rf"A works only the last \({d}\) days: \({d}\times {fr(F(1, ta))} = {fr(F(d, ta))}\)."),
                 ("Find B's share and B's days.", rf"B does \(1 - {fr(F(d, ta))} = {fr(1 - F(d, ta))}\), which takes \({fr(1 - F(d, ta))}\times {tb} = {tex((1 - F(d, ta)) * tb)}\) days."),
                 ("Take away the days with A.", rf"\[ {tex((1 - F(d, ta)) * tb)} - {d} = {tex(x)}\text{{ days alone}} \]"))
    rule = steps(("Count each person's days.", rf"If B works alone \(t\) days, B works \(t + {d}\) days in all and A works \({d}\) days."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{d}}}{{{ta}}} + \frac{{t + {d}}}{{{tb}}} = 1 \]"),
                 ("Solve.", rf"\[ \frac{{t + {d}}}{{{tb}}} = {fr(1 - F(d, ta))} \;\Rightarrow\; t + {d} = {tex((1 - F(d, ta)) * tb)} \;\Rightarrow\; t = {tex(x)} \]"))
    fin = fin_of(x, "days")
    rb = rbe([rf"A works \({d}\) days, B works \(t + {d}\) days.", rf"\(\frac{{{d}}}{{{ta}}} + \frac{{t + {d}}}{{{tb}}} = 1\).", rf"\(t = {tex(x)}\)."], fin)
    sc = shortcut(rf"\[ t = \left(1 - \frac{{{d}}}{{{ta}}}\right)\times {tb} - {d} = {tex(x)} \]", fin)
    return result(("number", x), T31, trad, rule, fin, rb, sc)


def less31(less, da, total):
    db = total - da
    x = next(F(k) for k in range(1, 1000) if F(da, k) + F(db, k + less) == 1)
    trad = steps(("Set up the times.", rf"Let A take \(x\) days; B takes \(x + {less}\) days. A works \({da}\) days and B the other \({total} - {da} = {db}\) days."),
                 ("Make a quadratic.", rf"\[ {da}(x + {less}) + {db}x = x(x + {less}) \;\Rightarrow\; x^2 - {da + db - less}x - {da * less} = 0 \]"),
                 ("Solve.", rf"\[ (x - {tex(x)})(x + {tex(F(da * less) / x)}) = 0 \;\Rightarrow\; x = {tex(x)} \]So A takes \({tex(x)}\) days and B \({tex(x + less)}\) days."))
    rule = steps(("Count each person's days.", rf"A works \({da}\) days, B works \({db}\) days; alone times \(x\) and \(x + {less}\)."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{da}}}{{x}} + \frac{{{db}}}{{x + {less}}} = 1 \]"),
                 ("Check the root.", rf"\(x = {tex(x)}\): \(\frac{{{da}}}{{{tex(x)}}} + \frac{{{db}}}{{{tex(x + less)}}} = {fr(F(da) / x)} + {fr(F(db) / (x + less))} = 1\). "
                                     rf"So A \(= {tex(x)}\), B \(= {tex(x + less)}\) days."))
    fin = rf"A \({tex(x)}\) days, B \({tex(x + less)}\) days"
    rb = rbe([rf"Alone times \(x\) and \(x + {less}\); A works \({da}\), B works \({db}\) days.", rf"\(\frac{{{da}}}{{x}} + \frac{{{db}}}{{x + {less}}} = 1\).",
              rf"\(x = {tex(x)}\), so B \(= {tex(x + less)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{da}}}{{x}} + \frac{{{db}}}{{x + {less}}} = 1 \Rightarrow x = {tex(x)},\ x + {less} = {tex(x + less)} \]", fin)
    return result(("pair", (x, x + less)), T31, trad, rule, fin, rb, sc)


def with_c31(ta, tb, T):
    c = F(1, T) - F(1, ta) - F(1, tb)
    trad = steps(("Write the one-day work.", rf"\[ \text{{A}} = {fr(F(1, ta))},\quad \text{{B}} = {fr(F(1, tb))},\quad \text{{A + B + C}} = {fr(F(1, T))} \]"),
                 ("Take away A and B.", rf"\[ \text{{C}} = {fr(F(1, T))} - {fr(F(1, ta))} - {fr(F(1, tb))} = {fr(c)} \]"),
                 ("Find C's time.", rf"\[ 1\div {fr(c)} = {tex(1 / c)}\text{{ days}} \]"))
    rule = steps(("Count each person's days.", rf"All three work the whole \({T}\) days; let C's time be \(z\)."),
                 ("Apply the specified rule.", F31 + rf"\[ \frac{{{T}}}{{{ta}}} + \frac{{{T}}}{{{tb}}} + \frac{{{T}}}{{z}} = 1 \]"),
                 ("Solve.", rf"\[ \frac{{{T}}}{{z}} = 1 - {fr(F(T, ta))} - {fr(F(T, tb))} = {fr(1 - F(T, ta) - F(T, tb))} \;\Rightarrow\; z = {tex(1 / c)} \]"))
    fin = fin_of(1 / c, "days")
    rb = rbe([rf"Each works \({T}\) days.", rf"\(\frac{{{T}}}{{{ta}}} + \frac{{{T}}}{{{tb}}} + \frac{{{T}}}{{z}} = 1\).", rf"\(z = {tex(1 / c)}\)."], fin)
    sc = shortcut(rf"\[ z = {T}\div\left(1 - \frac{{{T}}}{{{ta}}} - \frac{{{T}}}{{{tb}}}\right) = {tex(1 / c)} \]", fin)
    return result(("number", 1 / c), T31, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 32: alternate days (new card)
T32 = (r"If A and B can finish a job alone in \(x\) and \(y\) days and work on alternate days, one cycle of two days does "
       r"\(\frac{1}{x}+\frac{1}{y}\) of the job. Take \(n\) complete cycles leaving work \(r = 1 - n\left(\frac{1}{x}+\frac{1}{y}\right) \gt 0\); "
       r"the starter (alone time \(s\)) works next: if \(r \le \frac{1}{s}\) the job takes \(2n + rs\) days, otherwise \(2n + 1 + \left(r - \frac{1}{s}\right)t\) days, "
       r"where \(t\) is the other worker's time.")
CARD32 = card(
    32, "Two Workers on Alternate Days (or Hours)",
    r"If A and B can finish a job alone in \(x\) and \(y\) days and they work on alternate days (one day each, by turns), the pattern repeats "
    r"every two days. Count the complete two-day cycles first, then let the worker whose turn it is finish what is left.",
    r"\[ \text{One cycle} = \frac{1}{x} + \frac{1}{y},\qquad r = 1 - n\left(\frac{1}{x} + \frac{1}{y}\right) \gt 0 \]"
    r"where \(n\) is the largest number of complete cycles that still leaves some work. If the starter (time \(s\)) can finish \(r\) on the next day "
    r"(\(r \le \frac{1}{s}\)), the total time is \(T = 2n + rs\); otherwise \(T = 2n + 1 + \left(r - \frac{1}{s}\right)t\), where \(t\) is the other worker's time.",
    [("Work in one two-day cycle", r"\frac{1}{x} + \frac{1}{y}"), ("Complete cycles", r"n\ \text{cycles} = 2n\ \text{days}"),
     ("Work left", r"r = 1 - n\left(\frac{1}{x} + \frac{1}{y}\right)"), ("Starter's day", r"\text{does at most } \frac{1}{s}"),
     ("Other worker (if needed)", r"\left(r - \frac{1}{s}\right)t\ \text{days}")],
    "The order A, B, A, B, ... repeats every two days, so whole cycles can be counted at once. Only the last part needs care: the worker whose "
    "turn it is works first, and the last day may be only a part of a day.",
    "Keywords: 'work on alternate days', 'work at it alternately for a day (or an hour)', 'in stretches of one hour alternately'. "
    "Check who starts: the answer changes when B starts. For clock times, add the hours to the starting time.",
    r"A 5 days, B 7 days, A starts: one cycle does \(\frac{1}{5}+\frac{1}{7}=\frac{12}{35}\). Two cycles (4 days) do \(\frac{24}{35}\), leaving "
    r"\(\frac{11}{35}\). Day 5 (A) does \(\frac{7}{35}\), leaving \(\frac{4}{35}\); B needs \(\frac{4}{35}\times 7=\frac{4}{5}\) day. "
    r"Total \(5\frac{4}{5}\) days.",
    r"Do not round the last day up to a whole day, and do not forget who starts. The book's quick formula with a 'nearest whole number' "
    r"\(p = \frac{xy}{x+y}\) does not work for every pair of numbers (for 10 and 8 days it needs \(p = 5\) although \(\frac{80}{18} \approx 4.4\)), "
    r"so count the cycles instead.")


def clock(start_h, T):
    minutes = start_h * 60 + T * 60
    assert minutes.denominator == 1
    h24, m = divmod(int(minutes), 60)
    h12 = (h24 % 12) or 12
    return (F(h12), F(m)), f"{h12}:{m:02d} {'am' if h24 % 24 < 12 else 'pm'}"


def ordinal(k):
    return f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def alt32(x, y, b_first=False, names=("A", "B"), unit="days", start_hour=None, start_date=None, month="March"):
    x, y = R(x, y)
    (s, t), (sn, tn) = ((y, x), (names[1], names[0])) if b_first else ((x, y), names)
    cyc = 1 / s + 1 / t
    n = math.ceil(1 / cyc) - 1
    r = 1 - n * cyc
    if r <= 1 / s:
        T = 2 * n + r * s
        last = rf"\[ T = 2\times {n} + {fr(r)}\times {tex(s)} = {tex(T)}\text{{ {unit}}} \]"
        how = rf"{sn} works next and can do \({fr(1 / s)}\), which is enough: {sn} needs \({fr(r)}\times {tex(s)} = {tex(r * s)}\) of {'an hour' if unit == 'hours' else 'a day'}."
    else:
        T = 2 * n + 1 + (r - 1 / s) * t
        last = rf"\[ T = 2\times {n} + 1 + \left({fr(r)} - {fr(1 / s)}\right)\times {tex(t)} = {tex(T)}\text{{ {unit}}} \]"
        how = (rf"{sn} works next and does \({fr(1 / s)}\), leaving \({fr(r)} - {fr(1 / s)} = {fr(r - 1 / s)}\); then {tn} needs "
               rf"\({fr(r - 1 / s)}\times {tex(t)} = {tex((r - 1 / s) * t)}\) of {'an hour' if unit == 'hours' else 'a day'}.")
    # Traditional Method: a day-by-day table
    rows, done, k = [], F(0), 0
    word = unit[:-1].capitalize()
    while True:
        who, tt = (sn, s) if k % 2 == 0 else (tn, t)
        rate = 1 / tt
        k += 1
        if done + rate >= 1:
            part = (1 - done) / rate
            rows.append(rf"<tr><td>{k}</td><td>{who}</td><td>\({fr(1 - done)}\) (needs \({tex(part)}\) of the {unit[:-1]})</td><td>\(1\)</td></tr>")
            break
        done += rate
        rows.append(rf"<tr><td>{k}</td><td>{who}</td><td>\({fr(rate)}\)</td><td>\({fr(done)}\)</td></tr>")
    table = (f'<table border="1" cellpadding="4"><tr><th>{word}</th><th>Who works</th><th>Work that {unit[:-1]}</th><th>Work done so far</th></tr>'
             + "".join(rows) + "</table>")
    assert k - 1 + part == T
    if start_hour is not None:
        ans, txt = clock(F(start_hour), T)
        answer, fin = ("pair", ans), txt
        tail = rf"Starting at {clock(F(start_hour), 0)[1]}, \({tex(T)}\) hours later it is {txt}."
    elif start_date is not None:
        day = start_date + math.ceil(T) - 1
        answer, fin = ("number", F(day)), f"{ordinal(day)} {month}"
        tail = rf"The work ends during the \({math.ceil(T)}\)th day counted from {ordinal(start_date)} {month}, that is on {fin}."
    else:
        answer, fin = ("number", T), fin_of(T, unit)
        tail = ""
    trad = steps(("Write each person's work per " + unit[:-1] + ".", rf"{sn} does \({fr(1 / s)}\) and {tn} does \({fr(1 / t)}\) of the job; {sn} starts."),
                 ("Work " + unit[:-1] + " by " + unit[:-1] + ".", table),
                 ("Read the time.", rf"The job takes \({k - 1} + {tex(part)} = {tex(T)}\) {unit}." + (" " + tail if tail else "")))
    rule = steps(("Find the work in one cycle.", rf"\[ {fr(1 / s)} + {fr(1 / t)} = {fr(cyc)} \]"),
                 ("Count the complete cycles.", rf"\({n}\) cycles (\({2 * n}\) {unit}) do \({n}\times {fr(cyc)} = {fr(n * cyc)}\); one more cycle would reach \({fr((n + 1) * cyc)}\), "
                                                rf"which is not below 1. Work left: \(r = 1 - {fr(n * cyc)} = {fr(r)}\)."),
                 ("Finish the job.", how + last + tail))
    rb = rbe([rf"One cycle \(= {fr(cyc)}\).", rf"\(n = {n}\) cycles leave \(r = {fr(r)}\); {sn} starts.", rf"\(T = {tex(T)}\) {unit}." + (" " + tail if tail else "")], fin)
    sc = shortcut(rf"\[ n = {n},\ r = {fr(r)};\quad T = {tex(T)} \]" + (f"<br>{tail}" if tail else ""), fin)
    return result(answer, T32, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 33: C from A + B + C, A, B
T33 = (r"If A, B and C together can do a work in \(x\) days, A alone in \(a\) days and B alone in \(b\) days, then C alone does it in"
       r"<br>\[ \frac{xab}{ab - x(a+b)}\text{ days} \]")


def c33(x, a, b):
    x, a, b = R(x, a, b)
    c = 1 / x - 1 / a - 1 / b
    C = x * a * b / (a * b - x * (a + b))
    trad = steps(("Write the one-day work.", rf"\[ \text{{A + B + C}} = {fr(1 / x)},\quad \text{{A}} = {fr(1 / a)},\quad \text{{B}} = {fr(1 / b)} \]"),
                 ("Take away A and B.", rf"\[ \text{{C}} = {fr(1 / x)} - {fr(1 / a)} - {fr(1 / b)} = {fr(c)} \]"),
                 ("Find C's time.", rf"\[ 1\div {fr(c)} = {tex(1 / c)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(a = {tex(a)}\), \(b = {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ \text{C} = \frac{xab}{ab - x(a+b)} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)}\times {tex(a)}\times {tex(b)}}}{{{tex(a)}\times {tex(b)} - {tex(x)}({tex(a)} + {tex(b)})}} = "
                                            rf"\frac{{{tex(x * a * b)}}}{{{tex(a * b - x * (a + b))}}} = {tex(C)}\text{{ days}} \]"))
    fin = fin_of(C, "days")
    rb = rbe([rf"\(x = {tex(x)}, a = {tex(a)}, b = {tex(b)}\).", r"C \(= \frac{xab}{ab - x(a+b)}\).", rf"\(\frac{{{tex(x * a * b)}}}{{{tex(a * b - x * (a + b))}}} = {tex(C)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x * a * b)}}}{{{tex(a * b - x * (a + b))}}} = {tex(C)} \]", fin)
    return result(("number", C), T33, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 34: A works a days, B finishes
T34 = (r"If A and B can do a work in \(x\) and \(y\) days respectively and A leaves the work after doing it for \(a\) days, then B does "
       r"the remaining work in<br>\[ \frac{(x-a)y}{x}\text{ days} \]")


def b_rest34(x, y, a):
    x, y, a = R(x, y, a)
    v = (x - a) * y / x
    trad = steps(("Find A's share.", rf"\[ {tex(a)}\times {fr(1 / x)} = {fr(a / x)} \]"), ("Find the work left.", rf"\[ 1 - {fr(a / x)} = {fr(1 - a / x)} \]"),
                 ("Find B's time for it.", rf"B does \({fr(1 / y)}\) a day:<br>\[ {fr(1 - a / x)}\div {fr(1 / y)} = {tex(v)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(a = {tex(a)}\)."), ("Apply the specified rule.", r"\[ \text{B's days} = \frac{(x-a)y}{x} \]"),
                 ("Substitute the values.", rf"\[ \frac{{({tex(x)} - {tex(a)})\times {tex(y)}}}{{{tex(x)}}} = \frac{{{tex((x - a) * y)}}}{{{tex(x)}}} = {tex(v)}\text{{ days}} \]"))
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, a = {tex(a)}\).", r"B's days \(= \frac{(x-a)y}{x}\).", rf"\(\frac{{{tex((x - a) * y)}}}{{{tex(x)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{({tex(x)} - {tex(a)})\times {tex(y)}}}{{{tex(x)}}} = {tex(v)} \]", fin)
    return result(("number", v), T34, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 35: B works a days, A finishes
T35 = (r"If A and B can do a work in \(x\) and \(y\) days respectively and B leaves the work after doing it for \(a\) days, then A does "
       r"the remaining work in<br>\[ \frac{(y-a)x}{y}\text{ days} \]")
F35 = r"\[ \text{A's days} = \frac{(y-a)x}{y} \]"


def a_rest35(x, y, a, ab=None, bc_names=None):
    """A alone x (or found from A + B = ab), B alone y (or the B + C pair), B works a days."""
    if ab is not None:
        ab, y, a = R(ab, y, a)
        x = ab * y / (y - ab)
        a_rate = 1 / ab - 1 / y
        pre = rf"\[ \text{{A}} = {fr(1 / ab)} - {fr(1 / y)} = {fr(a_rate)} \]"
        xv, x_line = r6(ab, y)
        first = ("Find A's time first.", rf"A and B together take \({tex(ab)}\) days and B alone \({tex(y)}\) days, so by Rule 6 A alone takes:" + x_line)
        who = "B"
    elif bc_names is not None:
        x, b, c, a = R(x, *bc_names, a)
        y = b * c / (b + c)
        a_rate = 1 / x
        pre = rf"\[ \text{{A}} = {fr(1 / x)} \]"
        first = ("Treat B and C as one worker.", r"B and C together take" + xy_body(b, c)[1])
        who = "B and C"
    else:
        x, y, a = R(x, y, a)
        a_rate = 1 / x
        pre = rf"\[ \text{{A}} = {fr(1 / x)} \]"
        first = None
        who = "B"
    v = (y - a) * x / y
    trad = steps(("Find what " + who + " did.", rf"{who} works \({tex(a)}\) days: \({tex(a)}\times {fr(1 / y)} = {fr(a / y)}\), so \(1 - {fr(a / y)} = {fr(1 - a / y)}\) is left."),
                 ("Find A's one-day work.", pre),
                 ("Find A's time for the rest.", rf"\[ {fr(1 - a / y)}\div {fr(a_rate)} = {tex(v)}\text{{ days}} \]"))
    sub = rf"\[ \frac{{({tex(y)} - {tex(a)})\times {tex(x)}}}{{{tex(y)}}} = \frac{{{tex((y - a) * x)}}}{{{tex(y)}}} = {tex(v)}\text{{ days}} \]"
    rule_steps = [first] if first else []
    rule_steps.append(("Identify the values.", rf"\(x = {tex(x)}\) (A), \(y = {tex(y)}\) ({who}), \(a = {tex(a)}\)."))
    rule_steps.append(("Apply the specified rule.", F35 + sub))
    rule = steps(*rule_steps)
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, a = {tex(a)}\).", r"A's days \(= \frac{(y-a)x}{y}\).", rf"\(\frac{{{tex((y - a) * x)}}}{{{tex(y)}}} = {tex(v)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{({tex(y)} - {tex(a)})\times {tex(x)}}}{{{tex(y)}}} = {tex(v)} \]", fin)
    return result(("number", v), T35, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- text fixes, cards, plan, new questions
def tri(*rows):
    return {k: rf"A \({a}\) days, B \({b}\) days, C \({c}\) days" for k, (a, b, c) in zip("abcd", rows)}


BOOK_Q = {
    239: lambda q: q.replace("to do the work in 2 days.", "to do the work in 2 days?"),
    240: lambda q: q.replace("After A has been working at it for 5 days, and B for 7 days. C finishes it in 13 days.",
                             "After A has been working at it for 5 days and B for 7 days, C finishes it in 13 days."),
    241: lambda q: q.replace("then in how many days, the job is finished?", "in how many days is the job finished?"),
    247: lambda q: q.replace("finish ajob", "finish a job"),
    248: lambda q: q.replace("can do a work in 9 and days respectively", "can do a work in 9 and 12 days respectively")
                    .replace("they work 1 alternate days", "they work on alternate days").replace("will the work completed?", "will the work be completed?"),
    249: lambda q: q.replace("working separately cm mow", "working separately, can mow").replace("If they worn for", "If they work for")
                    .replace("whaj will", "when will"),
    250: lambda q: q.replace("A and B working, separately can plough a field m 6 am 10 hours respectively.",
                             "A and B, working separately, can plough a field in 6 and 10 hours respectively."),
}
BOOK_OPTS = {
    239: opts("boys", 8, 9, 10, 7), 244: opts("boys", 8, 10, 12, 16), 1377: opts("boys", 12, 15, 18, 20),
    240: tri((16, 48, 26), (16, 48, 24), (26, 48, 24), (16, 46, 24)),
    241: opts("days", 20, 15, 18, 24), 242: opts("days", 15, 20, 25, 30), 243: opts("days", 2, 4, 3, 6),
    245: opts("days", r"5\frac{4}{5}", r"4\frac{4}{5}", 5, 4), 246: opts("days", r"10\frac{1}{4}", 10, 8, 11),
    247: opts("days", r"4\frac{6}{7}", r"6\frac{6}{7}", 5, r"5\frac{6}{7}"), 248: opts("days", r"10\frac{1}{3}", 10, r"11\frac{1}{3}", 11),
    249: plain("6:30 pm", "8:30 pm", "3:30 pm", "4:30 pm"), 250: plain("3:30 pm", "3:20 pm", "3:10 pm", "3:40 pm"),
    251: opts("days", r"13\frac{1}{2}", r"12\frac{1}{4}", 13, r"12\frac{1}{3}"),
    252: opts("days", r"8\frac{2}{5}", r"7\frac{2}{3}", r"8\frac{3}{5}", r"7\frac{1}{3}"),
    253: opts("days", 10, 12, 8, 14),
}
CARD_FIX = {33: [("Using addition gives a wrong, usually negative or very large, denominator.",
                  "Using addition makes the denominator too large, so C's time comes out too small.")]}

PLAN = {
    31: (77, {239: lambda: boys31(20, 30, 60, 2, 8, 2), 240: lambda: pairs31(12, 16, 5, 7, 13), 241: lambda: helped31(20, 30, 60, 3),
              242: lambda: c_joins31(12, 15, 2, 1, 5), 243: lambda: a_left31(15, 10, 5), 244: lambda: boys31(20, 30, 60, 2, 8, 2),
              1377: lambda: boys31(24, 36, 72, 3, 6, 2)}),
    32: ("NEW_RULE_32", {245: lambda: alt32(5, 7), 246: lambda: alt32(9, 12), 247: lambda: alt32(5, 7, b_first=True), 248: lambda: alt32(9, 12, b_first=True),
                         249: lambda: alt32(8, 12, names=("Ganga", "Jamuna"), unit="hours", start_hour=9),
                         250: lambda: alt32(6, 10, unit="hours", start_hour=8)}),
    33: (78, {251: lambda: c33(6, 18, 27), 1378: lambda: c33(3, 8, 12), 1379: lambda: c33(6, 15, 20), 1380: lambda: c33(10, 30, 60), 1381: lambda: c33(8, 24, 48)}),
    34: (79, {252: lambda: b_rest34(25, 10, 4), 1382: lambda: b_rest34(16, 24, 4), 1383: lambda: b_rest34(36, 30, 6), 1384: lambda: b_rest34(48, 36, 12)}),
    35: (80, {253: lambda: a_rest35(15, 25, 5), 1385: lambda: a_rest35(20, 30, 6), 1386: lambda: a_rest35(None, 15, 6, ab=10),
              1387: lambda: a_rest35(None, 12, 5, ab=8), 1388: lambda: a_rest35(None, 40, 10, ab=24), 1389: lambda: a_rest35(None, 10, 4, ab="15/2"),
              1390: lambda: a_rest35(10, None, 4, bc_names=(12, 24))}),
}

NEW = {
    31: [("ex1", "A and B together can do a piece of work in 10 days, and B and C together in 20 days. A works at it for 4 days and B for 7 days, "
                 "and then C finishes it in 30 days. In how many days could each of them do the work alone?",
          lambda: pairs31(10, 20, 4, 7, 30), tri((15, 30, 45), (15, 30, 60), (12, 60, 30), (20, 20, 60)), 2),
         ("ex2", "A can do a job in 15 days, B in 30 days and C in 30 days. If A is helped on every 4th day by B and C, in how many days will "
                 "the job be finished?", lambda: helped31(15, 30, 30, 4), opts("days", 10, 11, 12, 15), 3),
         ("ex3", "A can do a job in 10 days and B in 20 days. They work together for 3 days. Then B leaves and A alone continues the work. "
                 "After 2 days C joins A and the job is completed in 3 more days. In how many days can C do it alone?",
          lambda: c_joins31(10, 20, 3, 2, 3), opts("days", 40, 50, 75, 60), 4),
         ("ex4", "A and B can do a job in 20 days and 12 days respectively. They began the work together, but A left after some days and B "
                 "finished the remaining job in 4 days. After how many days did A leave?", lambda: a_left31(20, 12, 4), opts("days", 5, 4, 6, 3), 1),
         ("ex5", "A and B can do a job in 18 days and 12 days respectively. B started the work alone, and 3 days before the job was finished "
                 "A joined B. For how many days did B work alone?", lambda: b_first31(18, 12, 3), opts("days", 6, 7, 8, 10), 2),
         ("ex7", "A can do a job in 5 days less than B. A works at it alone for 6 days and then B takes over and completes it. If altogether "
                 "18 days were needed to finish the job, how many days would each of them take alone?",
          lambda: less31(5, 6, 18), {k: rf"A \({a}\) days, B \({b}\) days" for k, (a, b) in zip("abcd", ((10, 15), (12, 17), (15, 20), (20, 25)))}, 3),
         ("ex8", "A can do a piece of work in 30 days, while B alone can do it in 20 days. With the help of C they finish the work in 10 days. "
                 "In how many days can C alone do the work?", lambda: with_c31(30, 20, 10), opts("days", 45, 50, 40, 60), 4)],
    32: [("ex_a", "A and B working alone can finish a job in 4 days and 6 days respectively. They work at it on alternate days, A starting "
                  "the work. In how many days will the job be finished?", lambda: alt32(4, 6), opts("days", r"4\frac{2}{3}", 5, r"4\frac{1}{2}", r"5\frac{1}{3}"), 1),
         ("ex_b", "A and B working alone can finish a job in 8 days and 12 days respectively. They work at it on alternate days. If B starts "
                  "the work, in how many days will the job be finished?", lambda: alt32(8, 12, b_first=True),
          opts("days", r"9\frac{1}{2}", 10, r"9\frac{1}{3}", r"9\frac{2}{3}"), 4),
         ("ex1", "Two painters, Rekha and Sunita, working separately, can paint a wall in 8 and 10 hours respectively. They paint for an hour "
                 "each by turns, Rekha starting at 9 am. At what time will the wall be finished?",
          lambda: alt32(8, 10, names=("Rekha", "Sunita"), unit="hours", start_hour=9), plain("6:00 pm", "5:48 pm", "5:36 pm", "6:12 pm"), 2),
         ("ex2", "Ravi and Mohit can do a job alone in 12 and 9 days respectively. Ravi starts the work on 1st March and they work on "
                 "alternate days. On which day of March will the job be finished?",
          lambda: alt32(12, 9, names=("Ravi", "Mohit"), start_date=1), plain("10th March", "12th March", "11th March", "9th March"), 3),
         ("ex3", "A and B, working separately, can weed a garden in 5 and 10 hours respectively. At 7 AM A starts, and they work in turns "
                 "of one hour each. When will the weeding be completed?",
          lambda: alt32(5, 10, unit="hours", start_hour=7), plain("1:00 pm", "2:00 pm", "12:30 pm", "1:30 pm"), 4)],
}


def main():
    cards = {}
    for n, (card_id, plan) in PLAN.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert (dump["rule_card"] or {}).get("id") == (None if card_id == "NEW_RULE_32" else card_id)
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(plan), (n, sorted(set(rows) ^ set(plan)))
        out = []
        for rid, fn in plan.items():
            extra = {}
            if rows[rid]["rule_id"] is None:
                q = clean(rows[rid]["question"])
                extra["question"] = BOOK_Q[rid](q) if rid in BOOK_Q else q
                assert "\\[" not in extra["question"], rid
            if rid in BOOK_OPTS:
                extra.update(BOOK_OPTS[rid])
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), card_id, extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated")
        h = CARD32 if n == 32 else dump["rule_card"]["rule_html"]
        if n in CARD_FIX:
            for a, b in CARD_FIX[n]:
                assert h.count(a) == 1, (n, a[:60])
                h = h.replace(a, b)
        if n == 32 or n in CARD_FIX:
            json.dump({"rule_name": f"Rule {n}", "rule_html": h}, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            print(f"Rule {n}: card {'created' if n == 32 else 'fixed'}")
        cards[n] = h

    for n, items in NEW.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        qs, answers = [], []
        for key, text, fn, op, pos in items:
            g = fn()
            qs.append(new_question(n, text, [op[k] for k in "abcd"], pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "time_n_work", "rule_name": f"Rule {n}", "rule_html": cards[n]}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(qs)} new questions")


if __name__ == "__main__":
    main()
