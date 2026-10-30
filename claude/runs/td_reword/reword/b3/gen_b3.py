"""Time & Distance rewording batch 3 (2026-10-30): the 23 rows of Rules 14-29 that fail the originality gate get all-new numbers,
a sentence in the book's simple style with the setting changed, new options, and an explanation built here for the new numbers
(prompt #9 layout). Theorem lines are kept, except 1501 (the old line was the two-speed rule, the question is a round trip at one
speed against two speeds) and 1537 (the old formula is replaced by the plain time statement). Independent check: b3/solve_b3.py.
Writes reword/b3/ruleNN/2_new_rows.json; check: `python reword_check.py b3`."""
import os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))                      # td_reword/reword/b3
TD = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, TD)
import rw_common  # noqa: E402
from common import frac, rbe, shortcut, solution, steps, tex  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
TH14A = r"When the faster walker returns from Q and meets the slower walker at R, the distance from P to R is \( \text{PR} = \frac{2Da}{a+b} \)."
TH14B = (r"If the faster walker B reaches Q, returns immediately, and meets A at R, then B's total distance is "
         r"\( \text{B's total distance} = \frac{2Db}{a+b} \).")
TH15 = (r"When two persons start simultaneously from opposite points, meet, and then take \(a\) and \(b\) hours to finish, their speed "
        r"ratio is \(\sqrt{b}:\sqrt{a}\).")
TH17 = r"When the same distance is travelled at two speeds, use \(D=\frac{xy}{|x-y|}\times t\), with \(t\) in hours."
TH17B = (r"If a round trip of \(2D\) km is walked at a uniform speed \(v\), and going at \(x\) and coming back at \(y\) takes \(t\) hours "
         r"longer, then \[ D\left(\frac{1}{x}+\frac{1}{y}-\frac{2}{v}\right) = t. \]")
TH18 = (r"If a carriage moving through fog passes a pedestrian walking in the same direction at \(x\) km/hr, and it is visible for \(t\) "
        r"hours up to a distance of \(d\) km, then its speed is \(x+\frac{d}{t}\) km/hr.")
TH19 = (r"If walking one way and riding back takes \(x\) and riding both ways saves \(t\), then walking both ways takes \(x+t\).<br>"
        r"\[ T_{\text{walk both}} = x+t \]")
TH22 = (r"For two opposite travellers between P and Q, if A takes \(x\) hours from P to Q, B takes \(y\) hours from Q to P and starts "
        r"\(t\) hours before A, then the meeting time after A starts is \(\frac{x(y-t)}{x+y}\) hours.")
TH23 = r"For a fixed distance, speed and time are inversely proportional, so \(S_1T_1=S_2T_2\)."
TH25 = (r"If a person must cover \(D\) km in \(T\) hours, and he has already covered \(\frac{1}{n}\) of the journey in \(m\) of the total "
        r"time, then the required speed is \[S=\frac{D(1-\frac{1}{n})}{T(1-m)}.\]")
TH26 = r"When one leg of a round trip is made at speed \( x \) km/hr and the other leg at speed \( y \) km/hr, the one-way distance is<br>\[ d=\frac{xy}{x+y}\times t \]"
TH27 = (r"If the whole journey by air would save a part \(f\) of the train time and arrive \(e\) hours early, then the train time is "
        r"\(\frac{e}{f}\), the air speed is \(\frac{D}{T-e}\), and the air distance is that speed times the air time \(T - \frac{e}{f}\).")
TH29 = (r"If a train sets off \(t\) hours ahead of its scheduled time, runs \(p\) km/hr slower than its usual speed and still reaches a "
        r"station \(D\) km away exactly on time, its usual journey time and its original speed are<br>"
        r"\[ T = \frac{t}{2}\left(\sqrt{1 + \frac{4D}{pt}} - 1\right), \qquad \text{Original speed} = \frac{2D}{\sqrt{t^2 + \frac{4Dt}{p}} - t} \]")


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb_steps, fin), shortcut=shortcut(sc_body, fin))


def sqrtF(x):
    x = F(x)
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    assert n * n == x.numerator and d * d == x.denominator, x
    return F(n, d)


def hm_text(minutes):
    h, m = divmod(int(minutes), 60)
    return (F(h), F(m)), f"{h} hours {m} minutes"


def meet_return(D, a, b, ask):
    D, a, b = F(D), F(a), F(b)
    t = 2 * D / (a + b)
    pr, bt = a * t, b * t
    trad = steps(("Together they walk twice the distance.", rf"When they meet at R, A and B together have walked \(2\times{tex(D)} = {tex(2 * D)}\) km."),
                 ("Time until they meet.", rf"\[ \frac{{{tex(2 * D)}}}{{{tex(a)} + {tex(b)}}} = {tex(t)}\text{{ hours}} \]"),
                 (("Distance from P to R." if ask == "PR" else "B's total distance."),
                  rf"\[ {tex(a)}\times{tex(t)} = {tex(pr)}\text{{ km}} \]" if ask == "PR" else rf"\[ {tex(b)}\times{tex(t)} = {tex(bt)}\text{{ km}} \]"))
    v = pr if ask == "PR" else bt
    sp = a if ask == "PR" else b
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(a = {tex(a)}\), \(b = {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{2Da}{a+b} \]" if ask == "PR" else r"\[ \frac{2Db}{a+b} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{2\times{tex(D)}\times{tex(sp)}}}{{{tex(a)} + {tex(b)}}} = {tex(v)}\text{{ km}} \]"))
    fin = rf"\({tex(v)}\) km"
    return done(("number", v), TH14A if ask == "PR" else TH14B, trad, rule, fin, [rf"Time to meet \(= {tex(t)}\) h.", rf"\(\frac{{2\times{tex(D)}\times{tex(sp)}}}{{{tex(a + b)}}} = {tex(v)}\) km."],
                rf"\[ \frac{{2\times{tex(D)}\times{tex(sp)}}}{{{tex(a)}+{tex(b)}}} = {tex(v)}\text{{ km}} \]")


def cross_times(t1, t2, s1):
    t1, t2, s1 = F(t1), F(t2), F(s1)
    k = sqrtF(t1 / t2)
    s2 = s1 * k
    trad = steps(("Let them meet after \\(T\\) hours.", rf"The first then covers the second's part in \({tex(t1)}\) h, and the second covers the first's part in \({tex(t2)}\) h:<br>"
                  rf"\[ s_1 T = s_2\times{tex(t2)},\qquad s_2 T = s_1\times{tex(t1)} \]"),
                 ("Divide the two equations.", rf"\[ \frac{{s_1}}{{s_2}} = \frac{{s_2\times{tex(t2)}}}{{s_1\times{tex(t1)}}} \;\Rightarrow\; \left(\frac{{s_1}}{{s_2}}\right)^2 = {frac(t2 / t1)} \]"),
                 ("Find the second speed.", rf"\[ \frac{{s_1}}{{s_2}} = {frac(1 / k)} \;\Rightarrow\; s_2 = {tex(s1)}\times{frac(k)} = {tex(s2)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(a = {tex(t1)}\), \(b = {tex(t2)}\), first speed \(= {tex(s1)}\) km/hr."),
                 ("Apply the specified rule.", r"\[ s_1 : s_2 = \sqrt{b} : \sqrt{a} \]"),
                 ("Substitute and simplify.", rf"\[ {tex(s1)} : s_2 = \sqrt{{{tex(t2)}}} : \sqrt{{{tex(t1)}}} = \sqrt{{{frac(t2 / t1)}}} : 1 = {frac(1 / k)} : 1 \;\Rightarrow\; s_2 = {tex(s2)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(s2)}\) km/hr"
    return done(("number", s2), TH15, trad, rule, fin, [rf"\(s_1 : s_2 = \sqrt{{{tex(t2)}}} : \sqrt{{{tex(t1)}}} = {frac(1 / k)} : 1\).", rf"\(s_2 = {tex(s2)}\) km/hr."],
                rf"\[ s_2 = {tex(s1)}\times\frac{{\sqrt{{{tex(t1)}}}}}{{\sqrt{{{tex(t2)}}}}} = {tex(s2)}\text{{ km/hr}} \]")


def two_speeds_gap(x, y, mins):
    x, y = F(x), F(y)
    t = F(mins, 60)
    D = x * y / (y - x) * t
    trad = steps(("Write the two times.", rf"At \({tex(x)}\) km/hr the trip takes \(\frac{{D}}{{{tex(x)}}}\) h, at \({tex(y)}\) km/hr \(\frac{{D}}{{{tex(y)}}}\) h."),
                 ("Their difference is the extra time.", rf"\({mins}\) minutes \(= {frac(t)}\) h: \[ D\left({frac(1 / x)} - {frac(1 / y)}\right) = {frac(t)} \;\Rightarrow\; D\times{frac(1 / x - 1 / y)} = {frac(t)} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {frac(t)}\) h."),
                 ("Apply the specified rule.", r"\[ D=\frac{xy}{|x-y|}\times t \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}}\times{frac(t)} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH17, trad, rule, fin, [rf"\(t = {frac(t)}\) h.", rf"\(D = \frac{{{tex(x * y)}}}{{{tex(y - x)}}}\times{frac(t)} = {tex(D)}\) km."],
                rf"\[ \frac{{{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}}\times\frac{{{mins}}}{{60}} = {tex(D)}\text{{ km}} \]")


def round_uniform(v, a, b, mins):
    v, a, b = F(v), F(a), F(b)
    t = F(mins, 60)
    k = 1 / a + 1 / b - 2 / v
    D = t / k
    trad = steps(("Times for each plan.", rf"At \({tex(v)}\) km/hr both ways: \(\frac{{2D}}{{{tex(v)}}}\) h. At \({tex(a)}\) out and \({tex(b)}\) back: \(\frac{{D}}{{{tex(a)}}} + \frac{{D}}{{{tex(b)}}}\) h."),
                 ("The second plan is longer by the extra time.", rf"\({mins}\) minutes \(= {frac(t)}\) h: \[ D\left({frac(1 / a)} + {frac(1 / b)} - {frac(2 / v)}\right) = {frac(t)} \;\Rightarrow\; D\times{frac(k)} = {frac(t)} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(v = {tex(v)}\), \(x = {tex(a)}\), \(y = {tex(b)}\), \(t = {frac(t)}\) h."),
                 ("Apply the specified rule.", r"\[ D\left(\frac{1}{x}+\frac{1}{y}-\frac{2}{v}\right) = t \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{{frac(t)}}}{{{frac(k)}}} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH17B, trad, rule, fin, [rf"\(\frac{{1}}{{x}}+\frac{{1}}{{y}}-\frac{{2}}{{v}} = {frac(k)}\).", rf"\(D = {frac(t)}\div{frac(k)} = {tex(D)}\) km."],
                rf"\[ D = \frac{{{frac(t)}}}{{{frac(k)}}} = {tex(D)}\text{{ km}} \]")


def fog(w, mins, metres):
    w = F(w)
    d, t = F(metres, 1000), F(mins, 60)
    v = w + d / t
    trad = steps(("How fast the carriage pulls away.", rf"In \({mins}\) minutes the gap grows to \({metres}\) m \(= {tex(d)}\) km, so it gains \(\frac{{{tex(d)}}}{{{frac(t)}}} = {tex(d / t)}\) km every hour."),
                 ("Add the walker's own speed.", rf"\[ {tex(w)} + {tex(d / t)} = {tex(v)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(w)}\) km/hr, \(d = {tex(d)}\) km, \(t = {frac(t)}\) h."),
                 ("Apply the specified rule.", r"\[ \text{Speed} = x+\frac{d}{t} \]"),
                 ("Substitute and simplify.", rf"\[ {tex(w)} + \frac{{{tex(d)}}}{{{frac(t)}}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH18, trad, rule, fin, [rf"\(\frac{{d}}{{t}} = {tex(d / t)}\).", rf"\({tex(w)} + {tex(d / t)} = {tex(v)}\) km/hr."],
                rf"\[ {tex(w)} + \frac{{{tex(d)}}}{{{frac(t)}}} = {tex(v)}\text{{ km/hr}} \]")


def walk_ride(h1, m1, h2, m2):
    T1, g = 60 * h1 + m1, 60 * h2 + m2
    ride = F(T1 - g, 2)
    walk = T1 - ride
    both = 2 * walk
    ans, txt = hm_text(both)
    trad = steps(("Riding both ways.", rf"Walk + ride \(= {T1}\) min; ride + ride \(= {T1} - {g} = {T1 - g}\) min, so one ride \(= {tex(ride)}\) min."),
                 ("One walk.", rf"\[ {T1} - {tex(ride)} = {tex(walk)}\text{{ min}} \]"),
                 ("Walking both ways.", rf"\[ 2\times{tex(walk)} = {tex(both)}\text{{ min}} = \text{{{txt}}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {h1}\) h \({m1}\) min \(= {T1}\) min, \(t = {h2}\) h \({m2}\) min \(= {g}\) min."),
                 ("Apply the specified rule.", r"\[ T_{\text{walk both}} = x+t \]"),
                 ("Substitute and simplify.", rf"\[ {T1} + {g} = {tex(both)}\text{{ min}} = \text{{{txt}}} \]"))
    return done(("pair", ans), TH19, trad, rule, txt, [rf"\(x + t = {T1} + {g} = {tex(both)}\) min.", f"\\(=\\) {txt}."],
                rf"\[ {T1} + {g} = {tex(both)}\text{{ min}} \]")


def cross_after(a, b, c):
    a, b, c = F(a), F(b), F(c)
    t = a * (c - b) / (a + c)
    trad = steps(("Work out what part of the road each covers per hour.", rf"A covers \({frac(1 / a)}\) of PQ an hour, B covers \({frac(1 / c)}\)."),
                 ("B's head start.", rf"In \({tex(b)}\) h B covers \({frac(b / c)}\), leaving \({frac(1 - b / c)}\) of the road."),
                 ("Time until they meet after A starts.", rf"\[ {frac(1 - b / c)} \div \left({frac(1 / a)} + {frac(1 / c)}\right) = {tex(t)}\text{{ hours}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(a)}\), \(y = {tex(c)}\), \(t = {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{x(y-t)}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(a)}\times({tex(c)} - {tex(b)})}}{{{tex(a)} + {tex(c)}}} = {tex(t)}\text{{ hours}} \]"))
    fin = rf"\({tex(t)}\) hrs"
    return done(("number", t), TH22, trad, rule, fin, [rf"\(\frac{{{tex(a)}\times{tex(c - b)}}}{{{tex(a + c)}}} = {tex(t)}\) hours."],
                rf"\[ \frac{{{tex(a)}({tex(c)} - {tex(b)})}}{{{tex(a)}+{tex(c)}}} = {tex(t)}\text{{ hrs}} \]")


def inverse_speed(m1, s1, m2):
    s1 = F(s1)
    s2 = s1 * m1 / m2
    D = s1 * F(m1, 60)
    trad = steps(("Find the distance.", rf"\[ {tex(s1)}\times\frac{{{m1}}}{{60}} = {tex(D)}\text{{ km}} \]"),
                 (f"Speed to cover it in {m2} minutes.", rf"\[ {tex(D)} \div \frac{{{m2}}}{{60}} = {tex(s2)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(S_1 = {tex(s1)}\), \(T_1 = {m1}\) min, \(T_2 = {m2}\) min."),
                 ("Apply the specified rule.", r"\[ S_1T_1=S_2T_2 \]"),
                 ("Substitute and simplify.", rf"\[ S_2 = \frac{{{tex(s1)}\times{m1}}}{{{m2}}} = {tex(s2)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(s2)}\) km/hr"
    return done(("number", s2), TH23, trad, rule, fin, [rf"\(S_2 = \frac{{{tex(s1)}\times{m1}}}{{{m2}}} = {tex(s2)}\) km/hr."],
                rf"\[ \frac{{{tex(s1)}\times{m1}}}{{{m2}}} = {tex(s2)}\text{{ km/hr}} \]")


def rest_speed(D, T, p, q, minutes=False):
    D, p, q = F(D), F(p), F(q)
    Th = F(T, 60) if minutes else F(T)
    left_d, left_t = D * (1 - p), Th * (1 - q)
    S = left_d / left_t
    tl = rf"\({T}\) minutes \(= {frac(Th)}\) h" if minutes else rf"\({T}\) hours"
    trad = steps(("Distance left.", rf"\({frac(p)}\) of \({tex(D)}\) km is done, so \({tex(left_d)}\) km are left."),
                 ("Time left.", rf"\({frac(q)}\) of {tl} is used, so \({tex(left_t) if not minutes else frac(left_t)}\) h is left."),
                 ("Speed needed.", rf"\[ {tex(left_d)} \div {tex(left_t) if not minutes else frac(left_t)} = {tex(S)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(T = {frac(Th) if minutes else tex(Th)}\) h, part done \(= {frac(p)}\), time used \(= {frac(q)}\)."),
                 ("Apply the specified rule.", r"\[ S=\frac{D(1-\text{part done})}{T(1-\text{time used})} \]"),
                 ("Substitute and simplify.", rf"\[ S = \frac{{{tex(D)}\times{frac(1 - p)}}}{{{frac(Th) if minutes else tex(Th)}\times{frac(1 - q)}}} = {tex(S)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(S)}\) km/hr"
    return done(("number", S), TH25, trad, rule, fin, [rf"Left: \({tex(left_d)}\) km in \({tex(left_t) if not minutes else frac(left_t)}\) h.", rf"\(S = {tex(S)}\) km/hr."],
                rf"\[ \frac{{{tex(D)}\times{frac(1 - p)}}}{{{frac(Th) if minutes else tex(Th)}\times{frac(1 - q)}}} = {tex(S)}\text{{ km/hr}} \]")


def ride_walk(x, y, T):
    x, y, T = F(x), F(y), F(T)
    d = x * y / (x + y) * T
    trad = steps(("Write the total time.", rf"Riding out takes \(\frac{{d}}{{{tex(x)}}}\) h and walking back \(\frac{{d}}{{{tex(y)}}}\) h, \({tex(T)}\) h in all."),
                 ("Add the times.", rf"\[ d\left({frac(1 / x)} + {frac(1 / y)}\right) = {tex(T)} \;\Rightarrow\; d\times{frac(1 / x + 1 / y)} = {tex(T)} \]"),
                 ("Solve.", rf"\[ d = {tex(d)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(T)}\)."),
                 ("Apply the specified rule.", r"\[ d=\frac{xy}{x+y}\times t \]"),
                 ("Substitute and simplify.", rf"\[ d = \frac{{{tex(x)}\times{tex(y)}}}{{{tex(x)} + {tex(y)}}}\times{tex(T)} = {tex(d)}\text{{ km}} \]"))
    fin = rf"\({tex(d)}\) km"
    return done(("number", d), TH26, trad, rule, fin, [rf"\(\frac{{xy}}{{x+y}} = {tex(x * y / (x + y))}\).", rf"\(d = {tex(x * y / (x + y))}\times{tex(T)} = {tex(d)}\) km."],
                rf"\[ \frac{{{tex(x)}\times{tex(y)}}}{{{tex(x)}+{tex(y)}}}\times{tex(T)} = {tex(d)}\text{{ km}} \]")


def air_train(D, T, f, e):
    D, T, f, e = F(D), F(T), F(f), F(e)
    tr = e / f
    ta = T - tr
    va = D / (T - e)
    da = va * ta
    dt = D - da
    r = da / dt
    p, q = r.numerator, r.denominator
    trad = steps(("Train time.", rf"Saving \({frac(f)}\) of the train time is \({tex(e)}\) h, so the train time was \({tex(e)}\div{frac(f)} = {tex(tr)}\) h and the air time \({tex(T)} - {tex(tr)} = {tex(ta)}\) h."),
                 ("Air speed.", rf"All by air the trip takes \({tex(T)} - {tex(e)} = {tex(T - e)}\) h: speed \(\frac{{{tex(D)}}}{{{tex(T - e)}}} = {tex(va)}\) km/hr."),
                 ("The two distances.", rf"Air: \({tex(va)}\times{tex(ta)} = {tex(da)}\) km; train: \({tex(D)} - {tex(da)} = {tex(dt)}\) km, ratio \({p} : {q}\)."))
    rule = steps(("Train time from the saving.", rf"\[ \text{{train time}} = \frac{{e}}{{f}} = \frac{{{tex(e)}}}{{{frac(f)}}} = {tex(tr)}\text{{ h}} \]"),
                 ("Air distance.", rf"\[ D_{{\text{{air}}}} = \frac{{D}}{{T-e}}\times\left(T - \frac{{e}}{{f}}\right) = \frac{{{tex(D)}}}{{{tex(T - e)}}}\times{tex(ta)} = {tex(da)}\text{{ km}} \]"),
                 ("Ratio.", rf"\[ {tex(da)} : {tex(dt)} = {p} : {q} \]"))
    fin = rf"\({p} : {q}\)"
    return done(("ratio", (p, q)), TH27, trad, rule, fin, [rf"Train time \(= {tex(tr)}\) h, air time \(= {tex(ta)}\) h.", rf"Air \(= {tex(da)}\) km, train \(= {tex(dt)}\) km: \({p} : {q}\)."],
                rf"\[ \frac{{{tex(D)}}}{{{tex(T - e)}}}\times{tex(ta)} = {tex(da)},\quad {tex(da)} : {tex(dt)} = {p} : {q} \]")


def early_slow(t, p, D, ttext):
    t, p, D = F(t), F(p), F(D)
    root = sqrtF(t * t + 4 * D * t / p)
    v = 2 * D / (root - t)
    trad = steps(("Write the time condition.", rf"At the usual speed \(v\) the trip takes \(\frac{{{tex(D)}}}{{v}}\) h; at \(v - {tex(p)}\) it takes {ttext} longer:"
                  rf"\[ \frac{{{tex(D)}}}{{v - {tex(p)}}} - \frac{{{tex(D)}}}{{v}} = {tex(t)} \]"),
                 ("Clear the fractions.", rf"\[ {tex(D)}\times{tex(p)} = {tex(t)}\,v(v - {tex(p)}) \;\Rightarrow\; v^2 - {tex(p)}v - {tex(D * p / t)} = 0 \]"),
                 ("Take the positive root.", rf"\[ v = {tex(v)}\text{{ km/hr}} \]since \({tex(v)}^2 - {tex(p)}\times{tex(v)} = {tex(D * p / t)}\)."))
    rule = steps(("Identify the values.", rf"\(t = {tex(t)}\) h, \(p = {tex(p)}\), \(D = {tex(D)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Original speed} = \frac{2D}{\sqrt{t^2 + \frac{4Dt}{p}} - t} \]"),
                 ("Substitute and simplify.", rf"\[ \sqrt{{{tex(t)}^2 + \frac{{4\times{tex(D)}\times{tex(t)}}}{{{tex(p)}}}}} = \sqrt{{{tex(root * root)}}} = {tex(root)},\qquad "
                  rf"\frac{{2\times{tex(D)}}}{{{tex(root)} - {tex(t)}}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH29, trad, rule, fin, [rf"\(\sqrt{{t^2 + \frac{{4Dt}}{{p}}}} = {tex(root)}\).", rf"\(\frac{{2D}}{{{tex(root)} - {tex(t)}}} = {tex(v)}\) km/hr."],
                rf"\[ \frac{{2\times{tex(D)}}}{{{tex(root)} - {tex(t)}}} = {tex(v)}\text{{ km/hr}} \]")


PLAN = {
    14: [(1487, r"Two friends A and B walk from P to Q, a distance of \(28\) km, at \(3\) km/hr and \(9\) km/hr. B reaches Q, turns back "
                r"at once, and meets A at R. Find the distance from P to R.", lambda: meet_return(28, 3, 9, "PR"), "km"),
         (1488, r"Two girls A and B jog from P to Q, a distance of \(14\) km, at \(4\) km/hr and \(10\) km/hr. B reaches Q, turns back "
                r"at once, and meets A at R. Find the total distance B has run.", lambda: meet_return(14, 4, 10, "B"), "km")],
    15: [(1490, r"A cyclist leaves town P for town Q just as another cyclist leaves Q for P. After they pass each other, the first "
                r"takes \(8\) hours to reach Q and the second \(2\) hours to reach P. If the first cyclist rides at \(15\) km/hr, how "
                r"fast does the second ride?", lambda: cross_times(8, 2, 15), "km/hr"),
         (1491, r"Two riders leave X and Y at the same time and ride towards each other. After they meet, one needs \(2\) hours to "
                r"reach Y and the other \(18\) hours to reach X. If the first rides at \(24\) km/hr, find the speed of the second.",
          lambda: cross_times(2, 18, 24), "km/hr"),
         (1492, r"Two runners start at the same moment from A and B and run towards each other. After passing, the runner from A "
                r"needs \(16\) hours to reach B and the runner from B needs \(9\) hours to reach A. If the runner from A goes at "
                r"\(27\) km/hr, find the speed of the runner from B.", lambda: cross_times(16, 9, 27), "km/hr")],
    17: [(1500, r"Two cyclists ride the same road at steady speeds of \(27\) km/hr and \(36\) km/hr. The slower one takes \(20\) "
                r"minutes longer. How long is the road?", lambda: two_speeds_gap(27, 36, 20), "km"),
         (1501, r"A girl walks from A to B and back at a steady \(9\) km/hr. Had she gone at \(3\) km/hr and come back at \(18\) km/hr, "
                r"she would have taken \(30\) minutes longer for the round trip. Find the distance from A to B.",
          lambda: round_uniform(9, 3, 18, 30), "km")],
    18: [(1503, r"A cart going through fog passes a jogger running at \(7\) km/hr in the same direction. The cart stays in sight for "
                r"\(3\) minutes and can be seen up to \(240\) m. What is the speed of the cart?", lambda: fog(7, 3, 240), "km/hr"),
         (1504, r"A tonga going through fog passes a man walking at \(4\) km/hr in the same direction. He can see it for \(12\) "
                r"minutes, up to a distance of \(180\) m. Find the speed of the tonga.", lambda: fog(4, 12, 180), "km/hr")],
    19: [(1509, "A woman takes 5 hours 55 minutes to walk to a fair and ride back. She would save 1 hour 35 minutes by riding both "
                "ways. How long would she take to walk both ways?", lambda: walk_ride(5, 55, 1, 35),
          plain("7 hours 10 minutes", "7 hours 30 minutes", "7 hours 50 minutes", "8 hours 30 minutes")),
         (1511, "A man takes 9 hours 40 minutes to walk to a temple and ride back. He would save 4 hours 50 minutes by riding both "
                "ways. How long would he take to walk both ways?", lambda: walk_ride(9, 40, 4, 50),
          plain("13 hours 50 minutes", "14 hours 50 minutes", "14 hours 30 minutes", "15 hours 30 minutes"))],
    22: [(1520, "A man goes from P to Q in 3 hours. Another man leaves Q for P 2 hours before the first man sets out, and takes 17 "
                "hours for the trip. How long after the first man starts will they pass each other?", lambda: cross_after(3, 2, 17),
          plain(r"\(2\frac{1}{4}\) hrs", r"\(2\frac{1}{2}\) hrs", r"\(1\frac{3}{4}\) hrs", r"\(3\) hrs"))],
    23: [(1521, r"A girl covers a fixed distance in \(49\) minutes at an average speed of \(13\) km/hr. At what speed must she go to "
                r"cover it in \(26\) minutes?", lambda: inverse_speed(49, 13, 26), "km/hr"),
         (1523, r"A man covers a fixed distance in \(39\) minutes at an average speed of \(7\) km/hr. What speed does he need to cut "
                r"the time to \(21\) minutes?", lambda: inverse_speed(39, 7, 21), "km/hr")],
    25: [(1529, r"A man has to cover \(105\) km in \(14\) hours. He covers \(\frac{1}{3}\) of the way in \(\frac{1}{2}\) of the time. What "
                r"speed does he need for the rest of the way in the time left?", lambda: rest_speed(105, 14, F(1, 3), F(1, 2)), "km/hr"),
         (1530, r"A woman has to cover \(100\) km in \(10\) hours. If she covers \(\frac{2}{5}\) of the way in \(\frac{1}{2}\) of the time, "
                r"what speed does she need for the rest of the way in the time left?", lambda: rest_speed(100, 10, F(2, 5), F(1, 2)), "km/hr"),
         (1531, r"Ravi has to cover \(9\) km in \(45\) minutes. If he covers \(\frac{1}{3}\) of the distance in \(\frac{3}{5}\) of the time, "
                r"what speed in km/hr does he need for the rest of the distance in the time left?",
          lambda: rest_speed(9, 45, F(1, 3), F(3, 5), minutes=True), "km/hr")],
    26: [(1532, r"A man rode to a town by bus at \(15\) km/hr and walked back at \(3\) km/hr. If the whole round trip took \(12\) hours, "
                r"how many kilometres did he ride?", lambda: ride_walk(15, 3, 12), "km"),
         (1534, r"A woman rode to a village by bus at \(30\) km/hr and came back by bicycle at \(15\) km/hr. If the round trip took \(3\) "
                r"hours in all, how far did she ride?", lambda: ride_walk(30, 15, 3), "km")],
    27: [(1537, r"A man covers \(440\) km in \(9\) hours, partly by air and partly by train. Had he gone all the way by air, he would "
                r"have saved \(\frac{3}{5}\) of the train time and arrived \(3\) hours early. Find the ratio of the distance by air to "
                r"the distance by train.", lambda: air_train(440, 9, F(3, 5), 3), "")],
    29: [(1541, r"A train leaves a station \(\frac{1}{2}\) hour before its usual time. The driver runs it \(10\) km/hr slower, and it "
                r"reaches the next station \(360\) km away on time. Find the usual speed of the train.",
          lambda: early_slow(F(1, 2), 10, 360, r"\(\frac{1}{2}\) h"), "km/hr"),
         (1542, r"A train leaves a station \(1\frac{1}{2}\) hours before its usual time. The driver runs it \(15\) km/hr slower, and it "
                r"reaches the next station \(450\) km away on time. Find the usual speed of the train.",
          lambda: early_slow(F(3, 2), 15, 450, r"\(1\frac{1}{2}\) h"), "km/hr"),
         (1543, r"A train leaves a station \(\frac{3}{4}\) hour before its usual time. The driver runs it \(15\) km/hr slower, and it "
                r"reaches the next station \(630\) km away on time. Find the usual speed of the train.",
          lambda: early_slow(F(3, 4), 15, 630, r"\(\frac{3}{4}\) h"), "km/hr")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
