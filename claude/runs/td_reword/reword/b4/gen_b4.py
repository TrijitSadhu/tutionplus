"""Time & Distance rewording batch 4 (2026-10-30): the 24 rows of Rules 34-48 that fail the originality gate get all-new numbers,
a sentence in the book's simple style with the setting changed, new options, and an explanation built here for the new numbers
(prompt #9 layout). Theorem lines are kept as they were. Independent check: b4/solve_b4.py.
Writes reword/b4/ruleNN/2_new_rows.json; check: `python reword_check.py b4`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # td_reword/reword/b4
TD = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, TD)
import rw_common  # noqa: E402
from common import frac, rbe, shortcut, solution, steps, tex  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
TH34 = (r"If going \(x_1\) km/hr faster would save \(t_1\) hours and going \(x_2\) km/hr slower would cost \(t_2\) hours more, the original "
        r"speed is \[ S = \frac{x_1x_2(t_1 + t_2)}{x_1t_2 - x_2t_1} \] and the distance is \(\frac{S(S + x_1)}{x_1}t_1\).")
TH36 = (r"Average speed is always total distance divided by total time. Depending on what is given: \[ \text{I: } \frac{x_1 + x_2 + \dots}{T_1 + T_2 + \dots}, "
        r"\quad \text{II: } \frac{S_1T_1 + S_2T_2 + \dots}{T_1 + T_2 + \dots}, \quad \text{III: } \frac{x_1 + x_2 + \dots}{\frac{x_1}{S_1} + \frac{x_2}{S_2} + \dots} \]")
TH37 = (r"If a journey takes \(T\) hours, and going \(x\) km/hr faster would take \(t\) hours, then \[ \text{Original speed} = \frac{xt}{T - t}, "
        r"\qquad \text{Distance} = \text{Original speed} \times T \]")
TH38 = (r"If a car covers \(D\) km in \(T\) hours, partly at \(x\) km/hr and partly at \(y\) km/hr (\(x > y\)), the distance covered at \(x\) "
        r"km/hr is \[ \frac{(D - Ty)\,x}{x - y}\text{ km} \]")
TH39 = (r"If a distance is covered in \(T\) hours, a fraction \(f\) of it at \(x\) km/hr and the rest at \(y\) km/hr, then "
        r"\[ \text{Total distance} = \frac{T}{\frac{f}{x} + \frac{1 - f}{y}} \]")
TH40 = (r"If a thief drives off at \(x\) km/hr and the owner follows \(t\) hours later at \(y\) km/hr (\(y > x\)), the owner catches the "
        r"thief \[ \frac{xt}{y - x}\text{ hours} \] after setting off.")
TH43 = (r"If the speeds of A and B are in the ratio \(x : y\) and A takes \(T\) hours more than B over the same distance, then "
        r"\[ t_A = \frac{yT}{y - x}, \qquad t_B = \frac{xT}{y - x} \]")
TH44 = (r"If a fraction \(f\) of a journey is covered at \(S_1\) km/hr and the rest at \(S_2\) km/hr, the average speed for the whole "
        r"journey is \[ \frac{S_1S_2}{(1 - f)S_1 + fS_2} \]")
TH48 = (r"A hare is \(L\) of her own leaps ahead. While she takes \(h\) leaps the greyhound takes \(g\), and \(g_1\) of his leaps equal "
        r"\(h_1\) of hers. He overtakes her in \[ \frac{L}{\frac{h_1}{g_1} - \frac{h}{g}}\text{ of his leaps} \]")


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb_steps, fin), shortcut=shortcut(sc_body, fin))


def faster_slower(a, m1, b, m2, ask):
    a, b = F(a), F(b)
    t1, t2 = F(m1, 60), F(m2, 60)
    S = a * b * (t1 + t2) / (a * t2 - b * t1)
    T = t1 * (S + a) / a
    D = S * T
    trad = steps(("Write the distance three ways.", rf"Let the speed be \(S\) and the time \(T\): \[ D = ST = (S + {tex(a)})(T - {frac(t1)}) = (S - {tex(b)})(T + {frac(t2)}) \]"),
                 ("Expand and cancel \\(ST\\).", rf"\[ {tex(a)}T = {frac(t1)}(S + {tex(a)}),\qquad {tex(b)}T = {frac(t2)}(S - {tex(b)}) \]"),
                 ("Solve the two equations.", rf"Dividing them: \(\frac{{{tex(a)}}}{{{tex(b)}}} = \frac{{{frac(t1)}(S + {tex(a)})}}{{{frac(t2)}(S - {tex(b)})}}\), so \(S = {tex(S)}\) km/hr, "
                  rf"\(T = {tex(T)}\) h and \(D = {tex(S)}\times{tex(T)} = {tex(D)}\) km."))
    rule = steps(("Identify the values.", rf"\(x_1 = {tex(a)}\), \(t_1 = {frac(t1)}\) h, \(x_2 = {tex(b)}\), \(t_2 = {frac(t2)}\) h."),
                 ("Apply the specified rule.", r"\[ S = \frac{x_1x_2(t_1 + t_2)}{x_1t_2 - x_2t_1} \]"),
                 ("Substitute and simplify.", rf"\[ S = \frac{{{tex(a)}\times{tex(b)}\times{frac(t1 + t2)}}}{{{tex(a)}\times{frac(t2)} - {tex(b)}\times{frac(t1)}}} = {tex(S)}\text{{ km/hr}} \]"
                  + (rf"\[ D = \frac{{S(S + x_1)}}{{x_1}}t_1 = \frac{{{tex(S)}\times{tex(S + a)}}}{{{tex(a)}}}\times{frac(t1)} = {tex(D)}\text{{ km}} \]" if ask == "D" else "")))
    v, unit = (D, "km") if ask == "D" else (S, "km/hr")
    fin = rf"\({tex(v)}\) {unit}"
    return done(("number", v), TH34, trad, rule, fin, [rf"\(S = {tex(S)}\) km/hr.", rf"\(D = {tex(D)}\) km."],
                rf"\[ S = \frac{{{tex(a * b)}\times{frac(t1 + t2)}}}{{{frac(a * t2 - b * t1)}}} = {tex(S)}" + (rf",\quad D = {tex(D)}" if ask == "D" else "") + r" \]")


def avg_dist_time(d1, t1, d2, t2):
    d1, t1, d2, t2 = map(F, (d1, t1, d2, t2))
    A = (d1 + d2) / (t1 + t2)
    trad = steps(("Total distance.", rf"\[ {tex(d1)} + {tex(d2)} = {tex(d1 + d2)}\text{{ km}} \]"),
                 ("Total time.", rf"\[ {tex(t1)} + {tex(t2)} = {tex(t1 + t2)}\text{{ hours}} \]"),
                 ("Average speed.", rf"\[ \frac{{{tex(d1 + d2)}}}{{{tex(t1 + t2)}}} = {tex(A)}\text{{ km/hr}} \]"))
    rule = steps(("Use form I of the rule.", r"\[ \frac{x_1 + x_2}{T_1 + T_2} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(d1)} + {tex(d2)}}}{{{tex(t1)} + {tex(t2)}}} = {tex(A)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(A)}\) km/hr"
    return done(("number", A), TH36, trad, rule, fin, [rf"\(\frac{{{tex(d1 + d2)}}}{{{tex(t1 + t2)}}} = {tex(A)}\) km/hr."],
                rf"\[ \frac{{{tex(d1)}+{tex(d2)}}}{{{tex(t1)}+{tex(t2)}}} = {tex(A)}\text{{ km/hr}} \]")


def avg_dist_speed(parts):
    parts = [(F(d), F(s)) for d, s in parts]
    D = sum(d for d, s in parts)
    T = sum(d / s for d, s in parts)
    A = D / T
    times = " + ".join(rf"\frac{{{tex(d)}}}{{{tex(s)}}}" for d, s in parts)
    tvals = " + ".join(tex(d / s) for d, s in parts)
    trad = steps(("Time for each part.", rf"\[ {times} = {tvals} = {tex(T)}\text{{ hours}} \]"),
                 ("Total distance.", rf"\[ {' + '.join(tex(d) for d, s in parts)} = {tex(D)}\text{{ km}} \]"),
                 ("Average speed.", rf"\[ \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]"))
    rule = steps(("Use form III of the rule.", r"\[ \frac{x_1 + x_2 + x_3}{\frac{x_1}{S_1} + \frac{x_2}{S_2} + \frac{x_3}{S_3}} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(D)}}}{{{times}}} = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(A)}\) km/hr"
    return done(("number", A), TH36, trad, rule, fin, [rf"Time \(= {tex(T)}\) h, distance \(= {tex(D)}\) km.", rf"\(\frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\) km/hr."],
                rf"\[ \frac{{{tex(D)}}}{{{tvals}}} = {tex(A)}\text{{ km/hr}} \]")


def avg_time_speed(parts):
    parts = [(F(t), F(s)) for t, s in parts]
    D = sum(t * s for t, s in parts)
    T = sum(t for t, s in parts)
    A = D / T
    dists = " + ".join(rf"{tex(t)}\times{tex(s)}" for t, s in parts)
    trad = steps(("Distance for each part.", rf"\[ {dists} = {' + '.join(tex(t * s) for t, s in parts)} = {tex(D)}\text{{ km}} \]"),
                 ("Total time.", rf"\[ {' + '.join(tex(t) for t, s in parts)} = {tex(T)}\text{{ hours}} \]"),
                 ("Average speed.", rf"\[ \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]"))
    rule = steps(("Use form II of the rule.", r"\[ \frac{S_1T_1 + S_2T_2 + S_3T_3}{T_1 + T_2 + T_3} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{dists}}}{{{tex(T)}}} = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(A)}\) km/hr"
    return done(("number", A), TH36, trad, rule, fin, [rf"Distance \(= {tex(D)}\) km in \({tex(T)}\) h.", rf"\(\frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\) km/hr."],
                rf"\[ \frac{{{dists}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]")


def faster_time(T, x, t):
    T, x, t = F(T), F(x), F(t)
    S = x * t / (T - t)
    trad = steps(("The distance is the same both ways.", rf"\[ S\times{tex(T)} = (S + {tex(x)})\times{tex(t)} \]"),
                 ("Solve.", rf"\[ {tex(T)}S - {tex(t)}S = {tex(x * t)} \;\Rightarrow\; {tex(T - t)}S = {tex(x * t)} \;\Rightarrow\; S = {tex(S)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(T = {tex(T)}\), \(x = {tex(x)}\), \(t = {tex(t)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Original speed} = \frac{xt}{T - t} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(x)}\times{tex(t)}}}{{{tex(T)} - {tex(t)}}} = {tex(S)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(S)}\) km/hr"
    return done(("number", S), TH37, trad, rule, fin, [rf"\(S = \frac{{{tex(x * t)}}}{{{tex(T - t)}}} = {tex(S)}\) km/hr."],
                rf"\[ \frac{{{tex(x)}\times{tex(t)}}}{{{tex(T)}-{tex(t)}}} = {tex(S)}\text{{ km/hr}} \]")


def split_two(D, T, x, y):
    D, T, x, y = map(F, (D, T, x, y))
    d = (D - T * y) * x / (x - y)
    trad = steps(("Let \\(d\\) km be at the faster speed.", rf"\[ \frac{{d}}{{{tex(x)}}} + \frac{{{tex(D)} - d}}{{{tex(y)}}} = {tex(T)} \]"),
                 ("Clear the fractions.", rf"\[ {tex(y)}d + {tex(x)}({tex(D)} - d) = {tex(T * x * y)} \;\Rightarrow\; {tex(x - y)}d = {tex(x * D - T * x * y)} \]"),
                 ("Solve.", rf"\[ d = {tex(d)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(T = {tex(T)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{(D - Ty)\,x}{x - y} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{({tex(D)} - {tex(T)}\times{tex(y)})\times{tex(x)}}}{{{tex(x)} - {tex(y)}}} = {tex(d)}\text{{ km}} \]"))
    fin = rf"\({tex(d)}\) km"
    return done(("number", d), TH38, trad, rule, fin, [rf"\(\frac{{({tex(D)} - {tex(T * y)})\times{tex(x)}}}{{{tex(x - y)}}} = {tex(d)}\) km."],
                rf"\[ \frac{{({tex(D)} - {tex(T * y)})\times{tex(x)}}}{{{tex(x - y)}}} = {tex(d)}\text{{ km}} \]")


def frac_distance(T, f, x, y, minutes=False):
    f, x, y = F(f), F(x), F(y)
    Th = F(T, 60) if minutes else F(T)
    D = Th / (f / x + (1 - f) / y)
    tl = rf"\({T}\) minutes \(= {frac(Th)}\) h" if minutes else rf"\({T}\) hours"
    trad = steps(("Time for each part.", rf"\({frac(f)}\) of \(D\) at \({tex(x)}\): \(\frac{{{frac(f)}D}}{{{tex(x)}}}\) h; the rest at \({tex(y)}\): \(\frac{{{frac(1 - f)}D}}{{{tex(y)}}}\) h."),
                 ("They add up to the whole time.", rf"{tl}: \[ D\left({frac(f / x)} + {frac((1 - f) / y)}\right) = {frac(Th)} \;\Rightarrow\; D\times{frac(f / x + (1 - f) / y)} = {frac(Th)} \]"),
                 ("Solve.", rf"\[ D = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(T = {frac(Th)}\) h, \(f = {frac(f)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
                 ("Apply the specified rule.", r"\[ \text{Total distance} = \frac{T}{\frac{f}{x} + \frac{1 - f}{y}} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{frac(Th)}}}{{{frac(f / x)} + {frac((1 - f) / y)}}} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH39, trad, rule, fin, [rf"\(\frac{{f}}{{x}} + \frac{{1-f}}{{y}} = {frac(f / x + (1 - f) / y)}\).", rf"\(D = {tex(D)}\) km."],
                rf"\[ \frac{{{frac(Th)}}}{{{frac(f / x + (1 - f) / y)}}} = {tex(D)}\text{{ km}} \]")


def thief(x, hh, mm, y):
    x, y = F(x), F(y)
    t = hh + F(mm, 60)
    c = x * t / (y - x)
    trad = steps(("Lead of the thief.", rf"In \({hh}\) h \({mm}\) min \(= {tex(t)}\) h the thief goes \({tex(x)}\times{tex(t)} = {tex(x * t)}\) km."),
                 ("Owner gains each hour.", rf"\({tex(y)} - {tex(x)} = {tex(y - x)}\) km every hour."),
                 ("Time to close the gap.", rf"\[ \frac{{{tex(x * t)}}}{{{tex(y - x)}}} = {tex(c)}\text{{ hours}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(t)}\) h."),
                 ("Apply the specified rule.", r"\[ \frac{xt}{y - x} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(x)}\times{tex(t)}}}{{{tex(y)} - {tex(x)}}} = {tex(c)}\text{{ hours}} \]"))
    fin = rf"\({tex(c)}\) hours"
    return done(("number", c), TH40, trad, rule, fin, [rf"Lead \(= {tex(x * t)}\) km, gain \(= {tex(y - x)}\) km/hr.", rf"\({tex(c)}\) hours."],
                rf"\[ \frac{{{tex(x)}\times{tex(t)}}}{{{tex(y)}-{tex(x)}}} = {tex(c)}\text{{ hours}} \]")


def ratio_times(a, b, mins):
    T = F(mins, 60)
    ta, tb = b * T / (b - a), a * T / (b - a)
    trad = steps(("Times are in the opposite ratio of speeds.", rf"\(t_A : t_B = {b} : {a}\), so let \(t_A = {b}k\) and \(t_B = {a}k\)."),
                 ("Use the difference.", rf"\({b}k - {a}k = {mins}\) minutes \(= {frac(T)}\) h, so \(k = {frac(T / (b - a))}\) h."),
                 ("Find the times.", rf"\[ t_A = {b}\times{frac(T / (b - a))} = {tex(ta)}\text{{ hrs}},\qquad t_B = {a}\times{frac(T / (b - a))} = {tex(tb)}\text{{ hrs}} \]"))
    rule = steps(("Identify the values.", rf"\(x : y = {a} : {b}\), \(T = {frac(T)}\) h."),
                 ("Apply the specified rule.", r"\[ t_A = \frac{yT}{y - x}, \qquad t_B = \frac{xT}{y - x} \]"),
                 ("Substitute and simplify.", rf"\[ t_A = \frac{{{b}\times{frac(T)}}}{{{b - a}}} = {tex(ta)},\qquad t_B = \frac{{{a}\times{frac(T)}}}{{{b - a}}} = {tex(tb)} \]"))
    fin = rf"\({tex(ta)}\) hrs, \({tex(tb)}\) hrs"
    return done(("pair", (ta, tb)), TH43, trad, rule, fin, [rf"\(t_A = {tex(ta)}\) hrs.", rf"\(t_B = {tex(tb)}\) hrs."],
                rf"\[ t_A = \frac{{{b}\times{frac(T)}}}{{{b - a}}} = {tex(ta)},\quad t_B = {tex(tb)} \]")


def frac_avg(f, s1, s2, D):
    f, s1, s2, D = map(F, (f, s1, s2, D))
    T = f * D / s1 + (1 - f) * D / s2
    A = D / T
    trad = steps(("Distance of each part.", rf"\({frac(f)}\) of \({tex(D)}\) km \(= {tex(f * D)}\) km at \({tex(s1)}\) km/hr; the other \({tex((1 - f) * D)}\) km at \({tex(s2)}\) km/hr."),
                 ("Total time.", rf"\[ \frac{{{tex(f * D)}}}{{{tex(s1)}}} + \frac{{{tex((1 - f) * D)}}}{{{tex(s2)}}} = {tex(f * D / s1)} + {tex((1 - f) * D / s2)} = {tex(T)}\text{{ hours}} \]"),
                 ("Average speed.", rf"\[ \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(A)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(f = {frac(f)}\), \(S_1 = {tex(s1)}\), \(S_2 = {tex(s2)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{S_1S_2}{(1 - f)S_1 + fS_2} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(s1)}\times{tex(s2)}}}{{{frac(1 - f)}\times{tex(s1)} + {frac(f)}\times{tex(s2)}}} = {tex(A)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(A)}\) km/hr"
    return done(("number", A), TH44, trad, rule, fin, [rf"\(\frac{{{tex(s1 * s2)}}}{{{tex((1 - f) * s1 + f * s2)}}} = {tex(A)}\) km/hr."],
                rf"\[ \frac{{{tex(s1)}\times{tex(s2)}}}{{{frac(1 - f)}\times{tex(s1)}+{frac(f)}\times{tex(s2)}}} = {tex(A)}\text{{ km/hr}} \]")


def hare(L, h, g, g1, h1):
    L = F(L)
    gl = F(h1, g1)                      # one greyhound leap in hare leaps
    gain = gl - F(h, g)                 # per greyhound leap
    n = L / gain
    trad = steps(("Measure everything in hare leaps.", rf"\({g1}\) greyhound leaps \(= {h1}\) hare leaps, so one greyhound leap \(= {frac(gl)}\) hare leaps."),
                 ("Gain per greyhound leap.", rf"While the greyhound makes \({g}\) leaps (\({tex(g * gl)}\) hare leaps) the hare makes \({h}\); per greyhound leap he gains \({frac(gl)} - {frac(F(h, g))} = {frac(gain)}\) hare leap."),
                 ("Leaps to close the gap.", rf"\[ {tex(L)} \div {frac(gain)} = {tex(n)}\text{{ leaps}} \]"))
    rule = steps(("Identify the values.", rf"\(L = {tex(L)}\), \(h = {h}\), \(g = {g}\), \(g_1 = {g1}\), \(h_1 = {h1}\)."),
                 ("Apply the specified rule.", r"\[ \frac{L}{\frac{h_1}{g_1} - \frac{h}{g}} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(L)}}}{{{frac(gl)} - {frac(F(h, g))}}} = \frac{{{tex(L)}}}{{{frac(gain)}}} = {tex(n)}\text{{ leaps}} \]"))
    fin = rf"\({tex(n)}\) leaps"
    return done(("number", n), TH48, trad, rule, fin, [rf"Gain per greyhound leap \(= {frac(gain)}\) hare leap.", rf"\({tex(L)}\div{frac(gain)} = {tex(n)}\) leaps."],
                rf"\[ \frac{{{tex(L)}}}{{{frac(gl)} - {frac(F(h, g))}}} = {tex(n)}\text{{ leaps}} \]")


PLAN = {
    34: [(1568, r"A woman drives a certain distance. Had she gone \(3\) km/hr faster, she would have taken \(10\) minutes less; had she "
                r"gone \(3\) km/hr slower, she would have taken \(12\) minutes more. Find the distance.",
          lambda: faster_slower(3, 10, 3, 12, "D"), "km"),
         (1569, r"A man rides a certain distance on his bike. Had he gone \(10\) km/hr faster, he would have taken \(24\) minutes less; "
                r"had he gone \(10\) km/hr slower, he would have taken \(36\) minutes more. Find his usual speed.",
          lambda: faster_slower(10, 24, 10, 36, "S"), "km/hr"),
         (1571, r"A girl cycles a certain distance. Had she gone \(7\) km/hr faster, she would have taken \(20\) minutes less; had she "
                r"gone \(7\) km/hr slower, she would have taken \(40\) minutes more. Find her usual speed.",
          lambda: faster_slower(7, 20, 7, 40, "S"), "km/hr")],
    36: [(1577, r"A bus covers \(150\) km in \(4\) hours and then \(480\) km in \(6\) hours. Find its average speed for the whole trip.",
          lambda: avg_dist_time(150, 4, 480, 6), "km/hr"),
         (1579, r"A woman walks \(4\) km at \(2\) km/hr, cycles \(14\) km at \(7\) km/hr and goes by bus for \(32\) km at \(32\) km/hr. "
                r"Find her average speed for the whole trip.", lambda: avg_dist_speed([(4, 2), (14, 7), (32, 32)]), "km/hr"),
         (1580, r"A lorry covers \(240\) km in \(3\) hours and then \(210\) km in \(3\) hours. Find its average speed for the whole trip.",
          lambda: avg_dist_time(240, 3, 210, 3), "km/hr"),
         (1581, r"A car covers \(320\) km in \(7\) hours and then \(220\) km in \(3\) hours. Find its average speed for the whole trip.",
          lambda: avg_dist_time(320, 7, 220, 3), "km/hr"),
         (1582, r"On a trip a van runs for \(2\) hours at \(25\) km/hr, then for \(5\) hours at \(45\) km/hr, then for \(3\) hours at "
                r"\(15\) km/hr. Find its average speed.", lambda: avg_time_speed([(2, 25), (5, 45), (3, 15)]), "km/hr"),
         (1584, r"Ravi first walks \(10\) km at \(5\) km/hr, then cycles \(14\) km at \(7\) km/hr, and at last takes a bus for \(34\) km at \(34\) km/hr. What is his average speed over the whole trip?", lambda: avg_dist_speed([(10, 5), (14, 7), (34, 34)]), "km/hr")],
    37: [(1587, r"A bus completes a trip without stopping in \(11\) hours. Had it gone \(12\) km/hr faster, it would have taken \(8\) "
                r"hours. Find its usual speed.", lambda: faster_time(11, 12, 8), "km/hr"),
         (1588, r"A lorry completes a trip without stopping in \(8\) hours. Had it gone \(24\) km/hr faster, it would have taken \(5\) "
                r"hours. Find its usual speed.", lambda: faster_time(8, 24, 5), "km/hr"),
         (1589, r"A car completes a trip without stopping in \(11\) hours. Had it gone \(20\) km/hr faster, it would have taken \(7\) "
                r"hours. Find its usual speed.", lambda: faster_time(11, 20, 7), "km/hr")],
    38: [(1593, r"A bus goes \(400\) km in \(9\) hours. For some of the way its speed is \(60\) km/hr and for the rest it is \(40\) km/hr. What distance did it cover at \(60\) km/hr?", lambda: split_two(400, 9, 60, 40), "km")],
    39: [(1594, r"A jogger takes \(65\) minutes for a run. She runs \(\frac{1}{3}\) of the way at \(9\) km/hr and the remaining part at \(8\) km/hr. How long is the run?", lambda: frac_distance(65, F(1, 3), 9, 8, minutes=True), "km"),
         (1595, r"A rider takes \(3\) hours for a ride. He rides \(\frac{2}{3}\) of the way at \(24\) km/hr and the remaining part at \(15\) km/hr. How long is the ride?", lambda: frac_distance(3, F(2, 3), 24, 15), "km"),
         (1596, r"A walker takes \(3\) hours for a trip. She goes \(\frac{1}{3}\) of the way by cart at \(28\) km/hr and the remaining part on foot at \(7\) km/hr. How long is the trip?", lambda: frac_distance(3, F(1, 3), 28, 7), "km")],
    40: [(1601, r"A thief rides off on a stolen bike at \(24\) km/hr. The theft is noticed after \(1\) hour \(15\) minutes, and the "
                r"owner follows on another bike at \(28\) km/hr. How long after setting off will the owner catch the thief?",
          lambda: thief(24, 1, 15, 28), "hours")],
    43: [(1610, r"The speeds of Ravi and Mohan are in the ratio \(6 : 9\). Ravi takes \(50\) minutes more than Mohan for the same "
                r"distance. Find the time taken by Ravi and by Mohan.", lambda: ratio_times(6, 9, 50),
          plain(r"\(2\frac{1}{2}\) hrs, \(1\frac{2}{3}\) hrs", r"\(1\frac{2}{3}\) hrs, \(2\frac{1}{2}\) hrs", r"\(3\) hrs, \(2\) hrs",
                r"\(2\frac{1}{2}\) hrs, \(2\) hrs")),
         (1612, r"The speeds of Asha and Neha are in the ratio \(3 : 4\). Asha takes \(30\) minutes more than Neha for the same "
                r"distance. Find the time taken by Asha and by Neha.", lambda: ratio_times(3, 4, 30),
          plain(r"\(1\frac{1}{2}\) hrs, \(2\) hrs", r"\(2\frac{1}{2}\) hrs, \(2\) hrs", r"\(2\) hrs, \(1\frac{1}{2}\) hrs", r"\(3\) hrs, \(2\frac{1}{2}\) hrs"))],
    44: [(1614, r"A woman covers \(\frac{1}{3}\) of her trip at \(24\) km/hr and the rest at \(48\) km/hr. If the whole trip is \(60\) km, "
                r"what is her average speed for the whole trip?", lambda: frac_avg(F(1, 3), 24, 48, 60), "km/hr"),
         (1615, r"A van goes \(\frac{1}{4}\) of a road at \(18\) km/hr and the remaining part at \(42\) km/hr. The road is \(80\) km long. Find the average speed of the van over the road.", lambda: frac_avg(F(1, 4), 18, 42, 80), "km/hr"),
         (1616, r"A girl covers \(\frac{1}{2}\) of her trip at \(48\) km/hr and the rest at \(16\) km/hr. If the whole trip is \(260\) km, "
                r"what is her average speed for the whole trip?", lambda: frac_avg(F(1, 2), 48, 16, 260), "km/hr"),
         (1617, r"A van goes \(\frac{2}{3}\) of a road at \(40\) km/hr and the remaining part at \(28\) km/hr. The road is \(180\) km long. Find the average speed of the van over the road.", lambda: frac_avg(F(2, 3), 40, 28, 180), "km/hr")],
    48: [(1632, r"A greyhound chases a hare that is \(42\) of her own leaps ahead. The hare makes \(7\) leaps in the time the greyhound makes \(6\), and \(2\) leaps of the greyhound equal \(7\) leaps of the hare. After how many leaps does the greyhound reach the hare?", lambda: hare(42, 7, 6, 2, 7), "leaps")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
