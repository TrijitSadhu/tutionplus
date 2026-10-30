"""Time & Distance rewording batch 1 (2026-10-30): the 27 rows of Rules 1-3 that fail the originality gate get all-new numbers,
a sentence in the book's simple style with the setting changed (the owner's style), new options, and an explanation built
here for the new numbers in the prompt #9 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final
Answer). The Theorem line of each row is kept as it was (1442's names its new rest interval). Row ids, rule links, days and
times stay. The Time & Distance audit had no parameterised generators for these rules, so the builders below are new; the
independent check is b1/solve_b1.py. Writes reword/b1/ruleNN/2_new_rows.json; check: `python reword_check.py b1`."""
import os, sys
from fractions import Fraction as F
from math import lcm

HERE = os.path.dirname(os.path.abspath(__file__))                      # td_reword/reword/b1
TD = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, TD)
import rw_common  # noqa: E402
from common import frac, rbe, shortcut, solution, steps, tex  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
TIMES = chr(92) + "times"

TH_D = r"When speed and time are known, distance is calculated as \[ D = S \times T \]"
TH_T = r"When distance and speed are known, time is calculated as \[ T = \frac{D}{S} \]"
TH_S = r"When distance and time are known, speed is calculated as \[ S = \frac{D}{T} \]"
TH_KM = r"To convert km/hr to m/sec, use \[ x\text{ km/hr} = x \times \frac{5}{18}\text{ m/sec} \]"
TH_MS = r"To convert m/sec to km/hr, use \[ x\text{ m/sec} = x \times \frac{18}{5}\text{ km/hr} \]"
TH_SDT_MS = r"Speed is \( S = \frac{D}{T} \), and \( x\text{ m/sec} = x \times \frac{18}{5}\text{ km/hr} \)."
TH_CMP = r"To compare speeds, convert both to the same unit using \[ x\text{ m/sec} = x \times \frac{18}{5}\text{ km/hr} \]"
TH_WHEEL = (r"Distance covered = circumference × number of revolutions; speed is \( S = \frac{D}{T} \), and "
            r"\( x\text{ m/sec} = x \times \frac{18}{5}\text{ km/hr} \).")
TH_SD = r"Speed is \( S = \frac{D}{T} \), and distance covered is \( D = S \times T \)."
TH_DS = r"Distance is \( D = S \times T \), and required speed is \( S = \frac{D}{T} \)."
TH_AVG = (r"If the same distance is covered at two speeds \(x\) km/hr and \(y\) km/hr, then average speed for the whole journey is "
          r"\[\frac{2xy}{x+y}\text{ km/hr}.\]")
TH_AVG2 = r"For equal distances at speeds \(x\) and \(y\), average speed = \(\frac{2xy}{x+y}\)."
TH_AVG3 = r"If two equal distances are covered at speeds \(x\) and \(y\), average speed = \(\frac{2xy}{x+y}\)."
TH_REST = (r"When a person walks at \(x\) km/hr and rests for \(t\) hours after every kilometre, total time to cover \(y\) km is "
           r"\[ \text{Total time}=\frac{y}{x}+(y-1)t \]")


def done(answer, theorem, trad, rule, fin, rb_steps, sc_body):
    return dict(answer=answer, solution=solution(theorem, trad, rule, fin), rbe=rbe(rb_steps, fin), shortcut=shortcut(sc_body, fin))


def hm(minutes):
    """Whole minutes -> (hours, minutes) and the text '6 hrs 4 min'."""
    h, m = divmod(int(minutes), 60)
    return (F(h), F(m)), f"{h} hrs {m} min"


# ---------------------------------------------------------------- Rule 1: speed, distance, time
def dist_st(S, mins, who="man"):
    S, mins = F(S), F(mins)
    T = mins / 60
    D = S * T
    trad = steps(("Work out the distance in one minute.", rf"In \(60\) minutes the {who} goes \({tex(S)}\) km, so in \(1\) minute "
                  rf"\[ \frac{{{tex(S)}}}{{60}} = {frac(S / 60)}\text{{ km}} \]"),
                 (f"Scale up to {tex(mins)} minutes.", rf"\[ {tex(mins)} \times {frac(S / 60)} = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"Speed \(S = {tex(S)}\) km/hr.<br>Time \(T = {tex(mins)}\) minutes."),
                 ("Convert time to hours.", rf"\[ T = \frac{{{tex(mins)}}}{{60}} = {frac(T)}\text{{ hour}} \]"),
                 ("Apply the specified rule.", r"\[ D = S \times T \]"),
                 ("Substitute and simplify.", rf"\[ D = {tex(S)} \times {frac(T)} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH_D, trad, rule, fin, [rf"\(D = S\times T = {tex(S)}\times\frac{{{tex(mins)}}}{{60}} = {tex(D)}\) km."],
                rf"\[ D = {tex(S)} \times \frac{{{tex(mins)}}}{{60}} = {tex(D)}\text{{ km}} \]")


def time_ds(D, S):
    D, S = F(D), F(S)
    T = D / S
    trad = steps(("Find how far it goes in one hour.", rf"It covers \({tex(S)}\) km every hour."),
                 ("Count the hours needed.", rf"\[ {tex(D)} \div {tex(S)} = {tex(T)}\text{{ hours}} \]"))
    rule = steps(("Identify the values.", rf"Distance \(D = {tex(D)}\) km.<br>Speed \(S = {tex(S)}\) km/hr."),
                 ("Apply the specified rule.", r"\[ T = \frac{D}{S} \]"),
                 ("Substitute and simplify.", rf"\[ T = \frac{{{tex(D)}}}{{{tex(S)}}} = {tex(T)}\text{{ hours}} \]"))
    fin = rf"\({tex(T)}\) hours"
    return done(("number", T), TH_T, trad, rule, fin, [rf"\(T = \frac{{D}}{{S}} = \frac{{{tex(D)}}}{{{tex(S)}}} = {tex(T)}\) hours."],
                rf"\[ T = \frac{{{tex(D)}}}{{{tex(S)}}} = {tex(T)}\text{{ hours}} \]")


def speed_dt(D, T):
    D, T = F(D), F(T)
    S = D / T
    trad = steps(("Share the distance over the hours.", rf"\({tex(D)}\) km are covered in \({tex(T)}\) equal hours."),
                 ("Distance in one hour.", rf"\[ {tex(D)} \div {tex(T)} = {tex(S)}\text{{ km}} \]So the speed is \({tex(S)}\) km/hr."))
    rule = steps(("Identify the values.", rf"Distance \(D = {tex(D)}\) km.<br>Time \(T = {tex(T)}\) hours."),
                 ("Apply the specified rule.", r"\[ S = \frac{D}{T} \]"),
                 ("Substitute and simplify.", rf"\[ S = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(S)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(S)}\) km/hr"
    return done(("number", S), TH_S, trad, rule, fin, [rf"\(S = \frac{{D}}{{T}} = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(S)}\) km/hr."],
                rf"\[ S = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(S)}\text{{ km/hr}} \]")


def kmh_to_ms(x):
    x = F(x)
    v = x * 5 / 18
    trad = steps(("Write the speed in metres and seconds.", rf"\({tex(x)}\) km in one hour \(= {tex(x * 1000)}\) m in \(3600\) seconds."),
                 ("Metres in one second.", rf"\[ \frac{{{tex(x * 1000)}}}{{3600}} = {tex(v)}\text{{ m/sec}} \]"))
    rule = steps(("Identify the value.", rf"\(x = {tex(x)}\) km/hr."),
                 ("Apply the specified rule.", r"\[ x\text{ km/hr} = x \times \frac{5}{18}\text{ m/sec} \]"),
                 ("Substitute and simplify.", rf"\[ {tex(x)} \times \frac{{5}}{{18}} = {tex(v)}\text{{ m/sec}} \]"))
    fin = rf"\({tex(v)}\) m/sec"
    return done(("number", v), TH_KM, trad, rule, fin, [rf"\({tex(x)}\times\frac{{5}}{{18}} = {tex(v)}\) m/sec."],
                rf"\[ {tex(x)} \times \frac{{5}}{{18}} = {tex(v)}\text{{ m/sec}} \]")


def ms_to_kmh(x):
    x = F(x)
    v = x * 18 / 5
    trad = steps(("Distance in one hour, in metres.", rf"\({tex(x)}\) m every second \(\Rightarrow {tex(x)} \times 3600 = {tex(x * 3600)}\) m in an hour."),
                 ("Change metres to km.", rf"\[ \frac{{{tex(x * 3600)}}}{{1000}} = {tex(v)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the value.", rf"\(x = {tex(x)}\) m/sec."),
                 ("Apply the specified rule.", r"\[ x\text{ m/sec} = x \times \frac{18}{5}\text{ km/hr} \]"),
                 ("Substitute and simplify.", rf"\[ {tex(x)} \times \frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH_MS, trad, rule, fin, [rf"\({tex(x)}\times\frac{{18}}{{5}} = {tex(v)}\) km/hr."],
                rf"\[ {tex(x)} \times \frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]")


def metres_to_kmh(m, t, unit="seconds"):
    """m metres in t seconds (or minutes) -> km/hr."""
    m, t = F(m), F(t)
    secs = t if unit == "seconds" else t * 60
    ms = m / secs
    v = ms * 18 / 5
    per_hr = m * 3600 / secs
    tline = "" if unit == "seconds" else rf"\(T = {tex(t)}\) minutes \(= {tex(secs)}\) seconds.<br>"
    trad = steps(("Distance in one hour.", rf"In {tex(secs)} seconds it covers {tex(m)} m, so in \(3600\) seconds it covers "
                  rf"\[ {tex(m)} \times \frac{{3600}}{{{tex(secs)}}} = {tex(per_hr)}\text{{ m}} \]"),
                 ("Change metres to km.", rf"\[ \frac{{{tex(per_hr)}}}{{1000}} = {tex(v)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"Distance \(D = {tex(m)}\) m.<br>" + tline + (rf"Time \(T = {tex(secs)}\) seconds." if not tline else "")),
                 ("Find the speed in m/sec.", rf"\[ S = \frac{{D}}{{T}} = \frac{{{tex(m)}}}{{{tex(secs)}}} = {tex(ms)}\text{{ m/sec}} \]"),
                 ("Convert to km/hr.", rf"\[ {tex(ms)} \times \frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH_SDT_MS, trad, rule, fin, [rf"\(S = \frac{{{tex(m)}}}{{{tex(secs)}}} = {tex(ms)}\) m/sec.", rf"\({tex(ms)}\times\frac{{18}}{{5}} = {tex(v)}\) km/hr."],
                rf"\[ \frac{{{tex(m)}}}{{{tex(secs)}}} \times \frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]")


def compare(kmh, ms):
    kmh, ms = F(kmh), F(ms)
    other = ms * 18 / 5
    r = kmh / other
    p, q = r.numerator, r.denominator
    trad = steps(("Put both speeds in m/sec.", rf"\({tex(kmh)}\) km/hr \(= \frac{{{tex(kmh * 1000)}}}{{3600}} = {tex(kmh * 5 / 18)}\) m/sec; the other is \({tex(ms)}\) m/sec."),
                 ("Compare.", rf"\[ {tex(kmh * 5 / 18)} : {tex(ms)} = {p} : {q} \]"))
    rule = steps(("Convert the m/sec speed.", rf"\[ {tex(ms)} \times \frac{{18}}{{5}} = {tex(other)}\text{{ km/hr}} \]"),
                 ("Write the ratio.", rf"\[ {tex(kmh)} : {tex(other)} = {p} : {q} \]"))
    fin = rf"\({p} : {q}\)"
    return done(("ratio", (p, q)), TH_CMP, trad, rule, fin, [rf"\({tex(ms)}\times\frac{{18}}{{5}} = {tex(other)}\) km/hr.", rf"\({tex(kmh)} : {tex(other)} = {p} : {q}\)."],
                rf"\[ {tex(kmh)} : {tex(ms)}\times\frac{{18}}{{5}} = {p} : {q} \]")


def signal(D, mins, secs):
    """D km in mins minutes secs seconds -> km per second."""
    D = F(D)
    T = F(mins * 60 + secs)
    v = D / T
    trad = steps(("Change the time to seconds.", rf"\({mins}\) minutes \({secs}\) seconds \(= {mins}\times 60 + {secs} = {tex(T)}\) seconds."),
                 ("Distance in one second.", rf"\[ {tex(D)} \div {tex(T)} = {tex(v)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"Distance \(D = {tex(D)}\) km.<br>Time \(T = {tex(T)}\) seconds."),
                 ("Apply the specified rule.", r"\[ S = \frac{D}{T} \]"),
                 ("Substitute and simplify.", rf"\[ S = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(v)}\text{{ km/sec}} \]"))
    fin = rf"\({tex(v)}\) km/sec"
    return done(("number", v), TH_S, trad, rule, fin, [rf"\(T = {tex(T)}\) seconds.", rf"\(S = \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(v)}\) km/sec."],
                rf"\[ \frac{{{tex(D)}}}{{{tex(T)}}} = {tex(v)}\text{{ km/sec}} \]")


def wheel(circ, rev, secs):
    circ = F(circ)
    D = circ * rev
    ms = D / secs
    v = ms * 18 / 5
    trad = steps(("Distance in the given time.", rf"Each turn covers \({tex(circ)}\) m, so \({rev}\) turns cover \[ {rev} \times {tex(circ)} = {tex(D)}\text{{ m in }} {secs}\text{{ seconds}} \]"),
                 ("Distance in one hour.", rf"\[ {tex(D)} \times \frac{{3600}}{{{secs}}} = {tex(D * 3600 / secs)}\text{{ m}} = {tex(v)}\text{{ km}} \]"))
    rule = steps(("Distance covered.", rf"\[ D = {tex(circ)} \times {rev} = {tex(D)}\text{{ m}} \]"),
                 ("Speed in m/sec.", rf"\[ S = \frac{{D}}{{T}} = \frac{{{tex(D)}}}{{{secs}}} = {tex(ms)}\text{{ m/sec}} \]"),
                 ("Convert to km/hr.", rf"\[ {tex(ms)} \times \frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH_WHEEL, trad, rule, fin, [rf"\(D = {tex(circ)}\times{rev} = {tex(D)}\) m.", rf"\(S = \frac{{{tex(D)}}}{{{secs}}}\times\frac{{18}}{{5}} = {tex(v)}\) km/hr."],
                rf"\[ \frac{{{tex(circ)}\times{rev}}}{{{secs}}}\times\frac{{18}}{{5}} = {tex(v)}\text{{ km/hr}} \]")


def sound(v, secs):
    v = F(v)
    m = v * secs
    km = m / 1000
    trad = steps(("Distance in metres.", rf"Sound goes \({tex(v)}\) m every second, so in \({secs}\) seconds \[ {tex(v)} \times {secs} = {tex(m)}\text{{ m}} \]"),
                 ("Change to km.", rf"\[ \frac{{{tex(m)}}}{{1000}} = {tex(km)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"Speed \(S = {tex(v)}\) m/sec.<br>Time \(T = {secs}\) seconds."),
                 ("Apply the specified rule.", r"\[ D = S \times T \]"),
                 ("Substitute and simplify.", rf"\[ D = {tex(v)} \times {secs} = {tex(m)}\text{{ m}} = {tex(km)}\text{{ km}} \]"))
    fin = rf"\({tex(km)}\) km"
    return done(("number", km), TH_D, trad, rule, fin, [rf"\(D = {tex(v)}\times{secs} = {tex(m)}\) m \(= {tex(km)}\) km."],
                rf"\[ D = {tex(v)} \times {secs} = {tex(m)}\text{{ m}} = {tex(km)}\text{{ km}} \]")


def prop_dist(d, h1, h2):
    d = F(d)
    S = d / h1
    D = S * h2
    trad = steps(("Distance in one hour.", rf"\[ {tex(d)} \div {h1} = {tex(S)}\text{{ km}} \]"),
                 (f"Distance in {h2} hours.", rf"\[ {tex(S)} \times {h2} = {tex(D)}\text{{ km}} \]"))
    rule = steps(("Find the speed.", rf"\[ S = \frac{{D}}{{T}} = \frac{{{tex(d)}}}{{{h1}}} = {tex(S)}\text{{ km/hr}} \]"),
                 ("Find the new distance.", rf"\[ D = S \times T = {tex(S)} \times {h2} = {tex(D)}\text{{ km}} \]"))
    fin = rf"\({tex(D)}\) km"
    return done(("number", D), TH_SD, trad, rule, fin, [rf"\(S = \frac{{{tex(d)}}}{{{h1}}} = {tex(S)}\) km/hr.", rf"\(D = {tex(S)}\times{h2} = {tex(D)}\) km."],
                rf"\[ \frac{{{tex(d)}}}{{{h1}}} \times {h2} = {tex(D)}\text{{ km}} \]")


def kmh_min_to_m(kmh, mins):
    kmh = F(kmh)
    m = kmh * 1000 * mins / 60
    trad = steps(("Metres in one minute.", rf"\({tex(kmh)}\) km an hour \(= {tex(kmh * 1000)}\) m in \(60\) minutes \(= {tex(kmh * 1000 / 60)}\) m a minute."),
                 (f"Metres in {mins} minutes.", rf"\[ {tex(kmh * 1000 / 60)} \times {mins} = {tex(m)}\text{{ m}} \]"))
    rule = steps(("Identify the values.", rf"Speed \(S = {tex(kmh)}\) km/hr.<br>Time \(T = \frac{{{mins}}}{{60}}\) hour."),
                 ("Apply the specified rule.", r"\[ D = S \times T \]"),
                 ("Substitute and simplify.", rf"\[ D = {tex(kmh)} \times \frac{{{mins}}}{{60}} = {tex(m / 1000)}\text{{ km}} = {tex(m)}\text{{ m}} \]"))
    fin = rf"\({tex(m)}\) metres"
    return done(("number", m), TH_D, trad, rule, fin, [rf"\(D = {tex(kmh)}\times\frac{{{mins}}}{{60}} = {tex(m / 1000)}\) km \(= {tex(m)}\) m."],
                rf"\[ {tex(kmh)} \times \frac{{{mins}}}{{60}} \times 1000 = {tex(m)}\text{{ m}} \]")


def new_speed(m1, s1, m2):
    s1 = F(s1)
    D = s1 * m1 / 60
    s2 = D / (F(m2) / 60)
    trad = steps(("Find the distance.", rf"\[ {tex(s1)} \times \frac{{{m1}}}{{60}} = {tex(D)}\text{{ km}} \]"),
                 (f"Speed for {m2} minutes.", rf"In \({m2}\) minutes the same \({tex(D)}\) km must be covered, so in \(60\) minutes \[ {tex(D)} \times \frac{{60}}{{{m2}}} = {tex(s2)}\text{{ km}} \]"))
    rule = steps(("Distance.", rf"\[ D = S \times T = {tex(s1)} \times \frac{{{m1}}}{{60}} = {tex(D)}\text{{ km}} \]"),
                 ("Required speed.", rf"\[ S = \frac{{D}}{{T}} = \frac{{{tex(D)}}}{{{frac(F(m2, 60))}}} = {tex(s2)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(s2)}\) km/hr"
    return done(("number", s2), TH_DS, trad, rule, fin, [rf"\(D = {tex(s1)}\times\frac{{{m1}}}{{60}} = {tex(D)}\) km.", rf"\(S = {tex(D)}\div\frac{{{m2}}}{{60}} = {tex(s2)}\) km/hr."],
                rf"\[ \frac{{{tex(s1)}\times{m1}}}{{{m2}}} = {tex(s2)}\text{{ km/hr}} \]")


# ---------------------------------------------------------------- Rule 2: average speed over equal distances
def avg_speed(x, y, theorem=TH_AVG, d=None):
    x, y = F(x), F(y)
    A = 2 * x * y / (x + y)
    L = F(d) if d is not None else F(lcm(int(x), int(y)))      # a distance both speeds divide
    t1, t2 = L / x, L / y
    trad = steps(("Take a convenient distance each way." if d is None else "Use the distances given.",
                  rf"Let each part be \({tex(L)}\) km." if d is None else rf"Each part is \({tex(L)}\) km."),
                 ("Time for each part.", rf"\[ \frac{{{tex(L)}}}{{{tex(x)}}} = {tex(t1)}\text{{ h}},\qquad \frac{{{tex(L)}}}{{{tex(y)}}} = {tex(t2)}\text{{ h}} \]"),
                 ("Average speed = total distance ÷ total time.", rf"\[ \frac{{{tex(2 * L)}}}{{{tex(t1 + t2)}}} = {tex(A)}\text{{ km/hr}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) km/hr, \(y = {tex(y)}\) km/hr."),
                 ("Apply the specified rule.", r"\[ \text{Average speed} = \frac{2xy}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{2 \times {tex(x)} \times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex(2 * x * y)}}}{{{tex(x + y)}}} = {tex(A)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(A)}\) km/hr"
    return done(("number", A), theorem, trad, rule, fin, [rf"\(\frac{{2xy}}{{x+y}} = \frac{{2\times{tex(x)}\times{tex(y)}}}{{{tex(x + y)}}} = {tex(A)}\) km/hr."],
                rf"\[ \frac{{2\times{tex(x)}\times{tex(y)}}}{{{tex(x)}+{tex(y)}}} = {tex(A)}\text{{ km/hr}} \]")


def return_speed(x, A):
    x, A = F(x), F(A)
    y = A * x / (2 * x - A)
    L = F(lcm(int(x), int(y))) if x.denominator == y.denominator == 1 else x * y      # a distance both speeds divide
    trad = steps(("Take a convenient distance each way.", rf"Let each way be \({tex(L)}\) km. Going takes \(\frac{{{tex(L)}}}{{{tex(x)}}} = {tex(L / x)}\) h."),
                 ("Time for the whole trip at the average speed.", rf"\[ \frac{{{tex(2 * L)}}}{{{tex(A)}}} = {tex(2 * L / A)}\text{{ h}} \]so the return takes \({tex(2 * L / A)} - {tex(L / x)} = {tex(2 * L / A - L / x)}\) h."),
                 ("Return speed.", rf"\[ \frac{{{tex(L)}}}{{{tex(2 * L / A - L / x)}}} = {tex(y)}\text{{ km/hr}} \]"))
    rule = steps(("Apply the specified rule.", rf"\[ {tex(A)} = \frac{{2\times{tex(x)}\times y}}{{{tex(x)} + y}} \]"),
                 ("Solve for y.", rf"\[ {tex(A)}({tex(x)} + y) = {tex(2 * x)}y \;\Rightarrow\; {tex(A * x)} = {tex(2 * x - A)}y \;\Rightarrow\; y = {tex(y)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(y)}\) km/hr"
    return done(("number", y), TH_AVG2, trad, rule, fin, [rf"\({tex(A)}({tex(x)} + y) = {tex(2 * x)}y\).", rf"\(y = \frac{{{tex(A * x)}}}{{{tex(2 * x - A)}}} = {tex(y)}\) km/hr."],
                rf"\[ y = \frac{{{tex(A)}\times{tex(x)}}}{{2\times{tex(x)} - {tex(A)}}} = {tex(y)}\text{{ km/hr}} \]")


# ---------------------------------------------------------------- Rule 3: rests on the way
def rests(x, t, y):
    """x km/hr, rest t minutes after every km, y km in all; the last km needs no rest."""
    x, t = F(x), F(t)
    walk = F(y) * 60 / x
    total = walk + (y - 1) * t
    ans, txt = hm(total)
    trad = steps(("Walking time.", rf"\({y}\) km at \({tex(x)}\) km/hr take \(\frac{{{y}}}{{{tex(x)}}}\) h \(= {tex(walk)}\) minutes."),
                 ("Count the rests.", rf"He rests after each km except the last one: \({y} - 1 = {y - 1}\) rests of \({tex(t)}\) minutes \(= {tex((y - 1) * t)}\) minutes."),
                 ("Add.", rf"\[ {tex(walk)} + {tex((y - 1) * t)} = {tex(total)}\text{{ minutes}} = \text{{{txt}}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) km/hr, \(t = {tex(t)}\) minutes, \(y = {y}\) km."),
                 ("Apply the specified rule.", r"\[ \text{Total time}=\frac{y}{x}+(y-1)t \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{y}}}{{{tex(x)}}}\text{{ h}} + {y - 1}\times{tex(t)}\text{{ min}} = {tex(walk)} + {tex((y - 1) * t)} = {tex(total)}\text{{ min}} = \text{{{txt}}} \]"))
    fin = txt
    return done(("pair", ans), TH_REST, trad, rule, fin, [rf"Walking \(= {tex(walk)}\) min, rests \(= {y - 1}\times{tex(t)} = {tex((y - 1) * t)}\) min.", f"Total \\(= {tex(total)}\\) min \\(=\\) {txt}."],
                rf"\[ {tex(walk)} + {y - 1}\times{tex(t)} = {tex(total)}\text{{ min}} \]")


def rests_every(x, t, k, y):
    """x km/hr, stops t minutes at the end of every k-th km, y km in all; no stop at the destination."""
    x, t = F(x), F(t)
    walk = F(y) * 60 / x
    stops = (y - 1) // k
    total = walk + stops * t
    ans, txt = hm(total)
    theorem = (r"Total time = riding time + (number of rests × rest time). Here the rest is taken after every "
               rf"\({k}\)th km, so we count the rest points before the destination.")
    trad = steps(("Riding time.", rf"\[ \frac{{{y}}}{{{tex(x)}}}\text{{ h}} = {tex(walk)}\text{{ minutes}} \]"),
                 ("Count the stops.", rf"He stops at km \({k}, {2 * k}, \dots\) before reaching \({y}\) km: \(\left\lfloor\frac{{{y} - 1}}{{{k}}}\right\rfloor = {stops}\) stops of \({tex(t)}\) minutes."),
                 ("Add.", rf"\[ {tex(walk)} + {stops}\times{tex(t)} = {tex(total)}\text{{ minutes}} = \text{{{txt}}} \]"))
    rule = steps(("Riding time.", rf"\(\frac{{{y}}}{{{tex(x)}}}\) h \(= {tex(walk)}\) minutes."),
                 ("Rest time.", rf"\({stops}\) rest points \(\times {tex(t)}\) minutes \(= {tex(stops * t)}\) minutes."),
                 ("Total.", rf"\[ {tex(walk)} + {tex(stops * t)} = {tex(total)}\text{{ min}} = \text{{{txt}}} \]"))
    fin = txt
    return done(("pair", ans), theorem, trad, rule, fin, [rf"Riding \(= {tex(walk)}\) min; \({stops}\) stops \(= {tex(stops * t)}\) min.", f"Total \\(=\\) {txt}."],
                rf"\[ {tex(walk)} + {stops}\times{tex(t)} = {tex(total)}\text{{ min}} \]")


PLAN = {
    1: [(1416, "Find the distance covered by a girl cycling for 18 minutes at a speed of 20 km/hr.", lambda: dist_st(20, 18, "girl"), "km"),
        (1417, "Find the time a bus takes to cover 225 km at a speed of 50 km/hr.", lambda: time_ds(225, 50), "hours"),
        (1418, "A ship sails 476 km in 14 hours. Find the speed of the ship.", lambda: speed_dt(476, 14), "km/hr"),
        (1419, "A cheetah can run at 45 km/hr. How fast is that in metres per second?", lambda: kmh_to_ms(45), "m/sec"),
        (1420, "A train moves at 25 m/sec. What is this speed in km/hr?", lambda: ms_to_kmh(25), "km/hr"),
        (1421, "A bus moves at 63 km an hour. How many metres does it go each second?", lambda: kmh_to_ms(63), "m/sec"),
        (1422, "A scooter takes 25 seconds to go 350 metres. What is its speed in km per hour?",
         lambda: metres_to_kmh(350, 25), "km/hr"),
        (1423, "How many km per hour does a girl run who crosses a park 1100 m long in 6 minutes?",
         lambda: metres_to_kmh(1100, 6, "minutes"), "km/hr"),
        (1424, "Compare the speeds of two buses, one going at 63 km an hour and the other at 14 m a second.",
         lambda: compare(63, 14), ""),
        (1425, "A radio signal travels 72000 km to a satellite and takes 1 minute 36 seconds. Find the speed of the signal "
               "per second.", lambda: signal(72000, 1, 36), "km/sec"),
        (1426, "The wheel of a cart, 1.75 metres round, turns 16 times in 2 seconds. Find the speed of the cart in km per hour.",
         lambda: wheel(F(7, 4), 16, 2), "km/hr"),
        (1427, "Sound travels 330 metres a second. How many kilometres away is a storm if the thunder is heard 9 seconds after "
               "the flash?", lambda: sound(330, 9), "km"),
        (1428, "What is the length of a road that a cyclist going at 24 km an hour can cover in 4 minutes?",
         lambda: dist_st(24, 4, "cyclist"), "km"),
        (1429, "A boy crosses a playground 700 m long in 4 minutes. His speed in kilometres per hour is",
         lambda: metres_to_kmh(700, 4, "minutes"), "km/hr"),
        (1430, r"If a woman walks \(13\frac{1}{2}\) km in 3 hours, the distance she walks in 8 hours is",
         lambda: prop_dist(F(27, 2), 3, 8), "km"),
        (1431, "A car goes at 72 km/hr. How many metres will it go in 25 minutes?", lambda: kmh_min_to_m(72, 25), "metres"),
        (1432, "A bus covers a distance in 35 minutes at an average speed of 72 km per hour. The speed it must keep to cut the "
               "journey time to 28 minutes is", lambda: new_speed(35, 72, 28), "km/hr")],
    2: [(1433, r"A man drives to a town by car at \(70\) km/hr and comes back on a motorbike at \(42\) km/hr. Find his average "
               r"speed for the whole journey.", lambda: avg_speed(70, 42), "km/hr"),
        (1434, r"A woman drives to her office by car at \(60\) km/hr and comes back by bus at \(40\) km/hr. Find her average "
               r"speed for the whole trip.", lambda: avg_speed(60, 40), "km/hr"),
        (1435, r"A boy cycles to the market at \(12\) km/hr and walks back home at \(6\) km/hr. Find his average speed for "
               r"the whole trip.", lambda: avg_speed(12, 6), "km/hr"),
        (1436, r"A man goes to the airport by taxi at \(55\) km/hr and comes back by bus at \(33\) km/hr. Find his average "
               r"speed for the whole journey.", lambda: avg_speed(55, 33), "km/hr"),
        (1437, r"A bus goes from town P to town Q at \(84\) km/hr and comes back more slowly. If its average speed for the "
               r"round trip is \(70\) km/hr, its speed on the way back is:", lambda: return_speed(84, 70), "km/hr"),
        (1438, r"On a trip a woman drives the first \(180\) km at \(36\) km an hour and the next \(180\) km at \(45\) km an "
               r"hour. Her average speed in km per hour for these \(360\) km is", lambda: avg_speed(36, 45, TH_AVG3, d=180), "km/hr")],
    3: [(1439, r"A man walks at a speed of \(9\) km per hour. After every km he rests for \(9\) minutes. How long will he take "
               r"to walk \(18\) km?", lambda: rests(9, 9, 18), plain("3 hrs 33 min", "4 hrs 33 min", "4 hrs 3 min", "3 hrs 3 min")),
        (1440, r"A woman walks at a speed of \(3\) km per hour. After every km she rests for \(11\) minutes. How long will she "
               r"take to walk \(13\) km?", lambda: rests(3, 11, 13), plain("6 hrs 32 min", "5 hrs 32 min", "6 hrs 43 min", "6 hrs 21 min")),
        (1441, r"A boy walks at a speed of \(8\) km per hour. After every km he rests for \(5\) minutes. How long will he take "
               r"to walk \(24\) km?", lambda: rests(8, 5, 24), plain("4 hrs 55 min", "5 hrs 15 min", "3 hrs 55 min", "5 hrs")),
        (1442, r"A cyclist rides at \(16\) km an hour but stops for \(4\) minutes at the end of every \(4\)th kilometre. How "
               r"long will he take to ride \(52\) kilometres?", lambda: rests_every(16, 4, 4, 52),
         plain("3 hrs 59 min", "4 hrs 3 min", "4 hrs 11 min", "3 hrs 55 min"))],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
