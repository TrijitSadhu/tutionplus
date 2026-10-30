"""Time & Distance rewording batch 2 (2026-10-30): the 21 rows of Rules 4-11 that fail the originality gate get all-new numbers,
a sentence in the book's simple style with the setting changed, new options, and an explanation built here for the new numbers
(prompt #9 layout). Theorem lines are kept as they were, except 1468 (the old line gave the meeting point, the question asks the
whole distance). Independent check: b2/solve_b2.py. Writes reword/b2/ruleNN/2_new_rows.json; check: `python reword_check.py b2`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # td_reword/reword/b2
TD = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, TD)
import rw_common  # noqa: E402
from common import frac, rbe, shortcut, solution, steps, tex  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
TH4 = (r"For a fixed distance, <br>\[D=\frac{x y}{y-x}\times(t_1+t_2)\]<br>where \(x\) is the slower speed, \(y\) is the faster speed, "
       r"\(t_1\) is the late time, and \(t_2\) is the early time.")
TH5 = (r"If a person walks at \(x\) km/hr and is late by \(t_1\) hours, and after increasing speed by \(y\) km/hr is still late by "
       r"\(t_2\) hours, then<br>\[ D = \frac{x(x+y)}{y} \times (t_1 - t_2) \]")
TH6 = (r"When a person goes to a destination at speed \(x\) km/hr and returns at speed \(y\) km/hr, taking total time \(T\) hours, "
       r"the one-way distance is \[D=T\times\frac{xy}{x+y}.\]")
TH7 = (r"For a journey completed in \(T\) hours, with the first half of the distance covered at \(S_1\) km/hr and the second half at "
       r"\(S_2\) km/hr, the total distance is \[D=\frac{2TS_1S_2}{S_1+S_2}.\]")
TH8 = (r"When two trains travel towards each other from stations \(A\) and \(B\) that are \(D\) km apart, and the train from \(B\) "
       r"starts \(t\) hours earlier, the meeting distance from \(A\) is \[ \frac{(D - t y)x}{x+y} \] where \(x\) is the speed from "
       r"\(A\), and \(y\) is the speed from \(B\).")
TH9 = (r"If the first person starts \(h\) hours earlier at \(x\) km/hr and they meet \(t\) hours after the second person (speed "
       r"\(y\) km/hr) starts from the other end, the distance between the two places is \[ D = x(h + t) + yt. \]")
TH10 = r"If the new speed is \(\frac{a}{b}\) of the usual speed, then usual time is \(T=\frac{\Delta t}{\frac{b}{a}-1}\)."
TH11 = (r"When a faster person starts \(t\) hours after a slower one, the distance from the start at which they meet is "
        r"\[ D = \frac{t x y}{y-x} \] where \(x\) is slower speed, \(y\) faster speed, and \(t\) is the delay.")


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb_steps, fin), shortcut=shortcut(sc_body, fin))


def h(m):
    return F(m, 60)


def late_early(x, l, y, e):
    x, y = F(x), F(y)
    D = x * y / (y - x) * h(l + e)
    trad = steps(("Write the two journey times.", rf"At \({tex(x)}\) km/hr the time is \(\frac{{D}}{{{tex(x)}}}\) h; at \({tex(y)}\) km/hr it is \(\frac{{D}}{{{tex(y)}}}\) h."),
                 ("Their difference is the late time plus the early time.", rf"\({l} + {e} = {l + e}\) minutes \(= {frac(h(l + e))}\) h, so "
                  rf"\[ \frac{{D}}{{{tex(x)}}} - \frac{{D}}{{{tex(y)}}} = {frac(h(l + e))} \;\Rightarrow\; D\times{frac(1 / x - 1 / y)} = {frac(h(l + e))} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t_1 + t_2 = {l + e}\) min \(= {frac(h(l + e))}\) h."),
                 ("Apply the specified rule.", r"\[ D=\frac{x y}{y-x}\times(t_1+t_2) \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}}\times{frac(h(l + e))} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH4, trad, rule, fin, [rf"\(t_1 + t_2 = {frac(h(l + e))}\) h.", rf"\(D = \frac{{{tex(x * y)}}}{{{tex(y - x)}}}\times{frac(h(l + e))} = {tex(D)}\) km."],
                rf"\[ \frac{{{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}}\times\frac{{{l + e}}}{{60}} = {tex(D)}\text{{ km}} \]")


def still_late(x, l1, inc, l2):
    x, inc = F(x), F(inc)
    y = x + inc
    D = x * y / inc * h(l1 - l2)
    trad = steps(("Write the two journey times.", rf"At \({tex(x)}\) km/hr the time is \(\frac{{D}}{{{tex(x)}}}\) h; at \({tex(y)}\) km/hr it is \(\frac{{D}}{{{tex(y)}}}\) h."),
                 ("The faster trip saves the difference of the delays.", rf"\({l1} - {l2} = {l1 - l2}\) minutes \(= {frac(h(l1 - l2))}\) h:<br>"
                  rf"\[ \frac{{D}}{{{tex(x)}}} - \frac{{D}}{{{tex(y)}}} = {frac(h(l1 - l2))} \;\Rightarrow\; D\times{frac(1 / x - 1 / y)} = {frac(h(l1 - l2))} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), increase \(y = {tex(inc)}\), \(t_1 - t_2 = {l1 - l2}\) min \(= {frac(h(l1 - l2))}\) h."),
                 ("Apply the specified rule.", r"\[ D = \frac{x(x+y)}{y} \times (t_1 - t_2) \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{{tex(x)}\times{tex(y)}}}{{{tex(inc)}}}\times{frac(h(l1 - l2))} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH5, trad, rule, fin, [rf"New speed \(= {tex(y)}\) km/hr; \(t_1 - t_2 = {frac(h(l1 - l2))}\) h.", rf"\(D = \frac{{{tex(x)}\times{tex(y)}}}{{{tex(inc)}}}\times{frac(h(l1 - l2))} = {tex(D)}\) km."],
                rf"\[ \frac{{{tex(x)}\times{tex(y)}}}{{{tex(inc)}}}\times\frac{{{l1 - l2}}}{{60}} = {tex(D)}\text{{ km}} \]")


def there_back(x, y, T, ttext=None):
    x, y, T = F(x), F(y), F(T)
    D = T * x * y / (x + y)
    ttext = ttext or rf"\({tex(T)}\) hours"
    trad = steps(("Write the total time.", rf"Going takes \(\frac{{D}}{{{tex(x)}}}\) h and coming back \(\frac{{D}}{{{tex(y)}}}\) h; together they make {ttext} \(= {tex(T)}\) h."),
                 ("Add the two times.", rf"\[ D\left({frac(1 / x)} + {frac(1 / y)}\right) = {tex(T)} \;\Rightarrow\; D\times{frac(1 / x + 1 / y)} = {tex(T)} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(T = {tex(T)}\) h."),
                 ("Apply the specified rule.", r"\[ D=T\times\frac{xy}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ D = {tex(T)}\times\frac{{{tex(x)}\times{tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH6, trad, rule, fin, [rf"\(\frac{{xy}}{{x+y}} = {tex(x * y / (x + y))}\).", rf"\(D = {tex(T)}\times{tex(x * y / (x + y))} = {tex(D)}\) km."],
                rf"\[ {tex(T)}\times\frac{{{tex(x)}\times{tex(y)}}}{{{tex(x)}+{tex(y)}}} = {tex(D)}\text{{ km}} \]")


def halves(T, a, b):
    T, a, b = F(T), F(a), F(b)
    D = 2 * T * a * b / (a + b)
    trad = steps(("Let each half be \\(d\\) km.", rf"Time \(= \frac{{d}}{{{tex(a)}}} + \frac{{d}}{{{tex(b)}}} = d\times{frac(1 / a + 1 / b)}\) h, and this is \({tex(T)}\) h."),
                 ("Solve for one half.", rf"\[ d = {tex(T)} \div {frac(1 / a + 1 / b)} = {tex(D / 2)}\text{{ km}} \]"),
                 ("Total distance.", rf"\[ 2\times{tex(D / 2)} = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(T = {tex(T)}\), \(S_1 = {tex(a)}\), \(S_2 = {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ D=\frac{2TS_1S_2}{S_1+S_2} \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{2\times{tex(T)}\times{tex(a)}\times{tex(b)}}}{{{tex(a)} + {tex(b)}}} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH7, trad, rule, fin, [rf"\(D = \frac{{2\times{tex(T)}\times{tex(a)}\times{tex(b)}}}{{{tex(a + b)}}} = {tex(D)}\) km."],
                rf"\[ \frac{{2\times{tex(T)}\times{tex(a)}\times{tex(b)}}}{{{tex(a)}+{tex(b)}}} = {tex(D)}\text{{ km}} \]")


def head_start_meet(D, x, t, y):
    D, x, t, y = F(D), F(x), F(t), F(y)
    gap = D - t * y
    tm = gap / (x + y)
    d = x * tm
    trad = steps((f"Head start of the train from B.", rf"In \({tex(t)}\) h it covers \({tex(t)}\times{tex(y)} = {tex(t * y)}\) km, leaving \({tex(D)} - {tex(t * y)} = {tex(gap)}\) km between them."),
                 ("Time until they meet.", rf"They close the gap at \({tex(x)} + {tex(y)} = {tex(x + y)}\) km/hr: \[ \frac{{{tex(gap)}}}{{{tex(x + y)}}} = {tex(tm)}\text{{ h}} \]"),
                 ("Distance of the meeting point from A.", rf"\[ {tex(x)}\times{tex(tm)} = {tex(d)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(t)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{(D - t y)x}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{({tex(D)} - {tex(t)}\times{tex(y)})\times{tex(x)}}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex(gap * x)}}}{{{tex(x + y)}}} = {tex(d)}\text{{ km}} \]"))
    fin = rf"\({tex(d)}\) km"
    return done(("number", d), TH8, trad, rule, fin, [rf"Gap after the head start \(= {tex(gap)}\) km.", rf"\(\frac{{{tex(gap)}\times{tex(x)}}}{{{tex(x + y)}}} = {tex(d)}\) km."],
                rf"\[ \frac{{({tex(D)} - {tex(t * y)})\times{tex(x)}}}{{{tex(x + y)}}} = {tex(d)}\text{{ km}} \]")


def late_start_total(x, hh, y, t):
    x, hh, y, t = F(x), F(hh), F(y), F(t)
    D = x * (hh + t) + y * t
    trad = steps(("Distance of the first person.", rf"He walks \({tex(hh)} + {tex(t)} = {tex(hh + t)}\) h at \({tex(x)}\) km/hr: \({tex(x * (hh + t))}\) km."),
                 ("Distance of the second person.", rf"\({tex(t)}\) h at \({tex(y)}\) km/hr: \({tex(y * t)}\) km."),
                 ("They have covered the whole distance between them.", rf"\[ {tex(x * (hh + t))} + {tex(y * t)} = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(h = {tex(hh)}\), \(y = {tex(y)}\), \(t = {tex(t)}\)."),
                 ("Apply the specified rule.", r"\[ D = x(h + t) + yt \]"),
                 ("Substitute and simplify.", rf"\[ D = {tex(x)}\times{tex(hh + t)} + {tex(y)}\times{tex(t)} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH9, trad, rule, fin, [rf"\(D = {tex(x)}\times{tex(hh + t)} + {tex(y)}\times{tex(t)} = {tex(D)}\) km."],
                rf"\[ {tex(x)}({tex(hh)} + {tex(t)}) + {tex(y)}\times{tex(t)} = {tex(D)}\text{{ km}} \]")


def slow_walk(a, b, d):
    p = F(a, b)
    T = d / (1 / p - 1)
    trad = steps(("Time grows when speed falls.", rf"At \({frac(p)}\) of the speed, the same walk takes \(\frac{{{b}}}{{{a}}}\) of the usual time \(T\)."),
                 ("The extra time is the delay.", rf"\[ \frac{{{b}}}{{{a}}}T - T = {d} \;\Rightarrow\; {frac(1 / p - 1)}T = {d} \]"),
                 ("Solve.", rf"\[ T = {tex(T)}\text{{ minutes}} \]"))
    rule = steps(("Identify the values.", rf"\(\frac{{a}}{{b}} = {frac(p)}\), \(\Delta t = {d}\) minutes."),
                 ("Apply the specified rule.", r"\[ T=\frac{\Delta t}{\frac{b}{a}-1} \]"),
                 ("Substitute and simplify.", rf"\[ T = \frac{{{d}}}{{\frac{{{b}}}{{{a}}} - 1}} = \frac{{{d}}}{{{frac(1 / p - 1)}}} = {tex(T)}\text{{ minutes}} \]"))
    fin = rf"\({tex(T)}\) minutes"
    return done(("number", T), TH10, trad, rule, fin, [rf"\(\frac{{b}}{{a}} - 1 = {frac(1 / p - 1)}\).", rf"\(T = {d}\div{frac(1 / p - 1)} = {tex(T)}\) minutes."],
                rf"\[ T = \frac{{{d}}}{{{frac(1 / p - 1)}}} = {tex(T)}\text{{ minutes}} \]")


def catch_up(D, x, late, early):
    D, x = F(D), F(x)
    tb = D / x - late - early
    y = D / tb
    meet = late * x * y / (y - x)
    trad = steps(("Find the faster person's speed.", rf"The slower one takes \(\frac{{{tex(D)}}}{{{tex(x)}}} = {tex(D / x)}\) h. The faster one starts \({late}\) h later and arrives \({early}\) h earlier, "
                  rf"so takes \({tex(D / x)} - {late} - {early} = {tex(tb)}\) h: speed \(\frac{{{tex(D)}}}{{{tex(tb)}}} = {tex(y)}\) km/hr."),
                 ("When does the faster one catch up?", rf"After the faster one starts, the gap \({late}\times{tex(x)} = {tex(late * x)}\) km closes at \({tex(y)} - {tex(x)} = {tex(y - x)}\) km/hr: \(\frac{{{tex(late * x)}}}{{{tex(y - x)}}} = {tex(late * x / (y - x))}\) h."),
                 ("Meeting distance.", rf"\[ {tex(y)}\times{tex(late * x / (y - x))} = {tex(meet)}\text{{ km}} \]"))
    rule = steps(("Find the faster speed.", rf"\(y = \frac{{{tex(D)}}}{{{tex(tb)}}} = {tex(y)}\) km/hr; \(x = {tex(x)}\), delay \(t = {late}\) h."),
                 ("Apply the specified rule.", r"\[ D = \frac{t x y}{y-x} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{late}\times{tex(x)}\times{tex(y)}}}{{{tex(y)} - {tex(x)}}} = {tex(meet)}\text{{ km}} \]"))
    fin = rf"\({tex(meet)}\) km"
    return done(("number", meet), TH11, trad, rule, fin, [rf"Faster speed \(= {tex(y)}\) km/hr.", rf"\(\frac{{{late}\times{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}} = {tex(meet)}\) km."],
                rf"\[ \frac{{{late}\times{tex(x)}\times{tex(y)}}}{{{tex(y)}-{tex(x)}}} = {tex(meet)}\text{{ km}} \]")


PLAN = {
    4: [(1443, r"A woman rides her bicycle from home to the library. At \(15\) km/hr she is late by \(8\) min, but at \(20\) km/hr "
               r"she reaches \(7\) min early. Find the distance from her home to the library.", lambda: late_early(15, 8, 20, 7), "km"),
        (1444, r"A man cycles from his house to the factory. At \(10\) km/hr he is late by \(34\) min, but at \(20\) km/hr he "
               r"reaches \(17\) min early. Find the distance from his house to the factory.", lambda: late_early(10, 34, 20, 17), "km"),
        (1445, r"A student cycles to a town. At \(8\) km/hr she is late by \(26\) min, but at \(9\) km/hr she arrives \(4\) min "
               r"early. Find the distance to the town.", lambda: late_early(8, 26, 9, 4), "km"),
        (1446, r"Sita walks at \(6\) km/hr and reaches \(22\) minutes late. If she walks at \(9\) km/hr, she reaches \(28\) "
               r"minutes early. How far does Sita have to walk?", lambda: late_early(6, 22, 9, 28), "km")],
    5: [(1447, r"A girl cycling at \(24\) km/hr reaches her college \(25\) minutes late. Next time she rides \(6\) km/hr faster, "
               r"but is still \(9\) minutes late. Find the distance of the college from her home.", lambda: still_late(24, 25, 6, 9), "km"),
        (1448, r"A man driving at \(24\) km/hr reaches his office \(30\) minutes late. Next day he drives \(6\) km/hr faster, but "
               r"is still \(9\) minutes late. Find the distance of his office from his home.", lambda: still_late(24, 30, 6, 9), "km"),
        (1449, r"A boy cycling at \(12\) km/hr reaches the station \(27\) minutes late. Next time he rides \(6\) km/hr faster, but "
               r"is still \(12\) minutes late. Find the distance of the station from his home.", lambda: still_late(12, 27, 6, 12), "km"),
        (1450, r"A jogger running at \(12\) km/hr reaches the park \(22\) minutes late. If she runs at \(18\) km/hr, she is still "
               r"\(7\) minutes late. Find the distance of the park from her house.", lambda: still_late(12, 22, 6, 7), "km")],
    6: [(1451, r"A girl cycles to the lake at \(18\) km/hr and comes back home by bus at \(36\) km/hr. If she takes \(3\) hours in "
               r"all, how far is the lake from her home?", lambda: there_back(18, 36, 3), "km"),
        (1452, r"A man walks to a fair at \(2\frac{1}{2}\) km an hour and rides back at \(8\frac{1}{2}\) km an hour. How far did he "
               r"walk, if the whole trip took \(8\) hours \(48\) minutes?",
         lambda: there_back(F(5, 2), F(17, 2), F(44, 5), r"\(8\) hours \(48\) minutes"), "km"),
        (1453, r"A man walks to a village at \(3\) km an hour and rides back at \(8\) km an hour. How far did he walk, if the "
               r"whole trip took \(11\) hours?", lambda: there_back(3, 8, 11), "km"),
        (1454, r"A woman cycles to the temple at \(10\) km an hour and rides back at \(15\) km an hour. How far did she cycle, if "
               r"the whole trip took \(2\) hours?", lambda: there_back(10, 15, 2), "km")],
    7: [(1456, "A truck finishes a trip in 9 hours. For the first half of the distance its speed is 40 km/hr, and for the second "
               "half it is 50 km/hr. Find the total distance.", lambda: halves(9, 40, 50), "km"),
        (1457, "A bus takes 7 hours for a trip. It goes the first half of the distance at 21 km/hr and the rest at 28 km/hr. "
               "Find the total distance.", lambda: halves(7, 21, 28), "km"),
        (1458, "A lorry needs 3 hours for a trip. It drives half the distance at 36 km/hr and the other half at 60 km/hr. How "
               "long is the whole trip?", lambda: halves(3, 36, 60), "km"),
        (1459, "A van needs 5 hours for a trip. It goes half the way at 48 km/hr and the other half at 72 km/hr. How long is the "
               "whole trip?", lambda: halves(5, 48, 72), "km")],
    8: [(1464, r"Two towns \(P\) and \(Q\) are \(160\) km apart. A bus leaves \(P\) for \(Q\) at \(30\) km/hr. Another bus leaves "
               r"\(Q\) \(2\) hours earlier and goes towards \(P\) at \(50\) km/hr. At what distance from \(P\) will they meet?",
         lambda: head_start_meet(160, 30, 2, 50), "km")],
    9: [(1468, r"A man sets out from town P towards town Q at 16 km/h. A woman leaves town Q \(1\frac{1}{2}\) hours later and "
               r"rides towards P at 11 km/h. If they meet 3 hours after the woman started, how far apart are P and Q?",
         lambda: late_start_total(16, F(3, 2), 11, 3), "km")],
    10: [(1473, r"Walking at \(\frac{3}{5}\) of her usual speed, a woman is 18 minutes late. What is her usual time?",
          lambda: slow_walk(3, 5, 18), "minutes"),
         (1475, r"By cycling at \(\frac{3}{4}\) of his usual speed, a boy reaches school 27 minutes later than usual. His usual "
                r"time is:", lambda: slow_walk(3, 4, 27), "minutes")],
    11: [(1478, r"A sets out from town P to town Q, a distance of \(36\) km, walking at \(4\) km/hr. B starts from P \(2\) hours "
                r"later and reaches Q \(1\) hour before A does. At what distance from P do A and B meet?",
          lambda: catch_up(36, 4, 2, 1), "km")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
