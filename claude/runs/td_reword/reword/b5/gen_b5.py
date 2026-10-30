"""Time & Distance rewording batch 5 (2026-10-30): the 26 old rule-less rows (801-816, 825-834, 2018 copies of book exercises with
no Traditional Method, a NULL option e and some broken keys) are linked to the rule they use - as in the Time & Work Miscellaneous
run - and get all-new numbers, a sentence in the book's simple style with the setting changed, new options, e = '' and an
explanation in the prompt #9 layout. The builders of batches 1-3 are reused; Rules 9, 11, 20, 21, 24 and 28 get new ones here.
Independent check: b5/solve_b5.py. Writes reword/b5/ruleNN/2_new_rows.json; check: `python reword_check.py b5`."""
import importlib.util, json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # td_reword/reword/b5
RW = os.path.dirname(HERE)
TD = os.path.dirname(RW)
sys.path.insert(0, RW)
sys.path.insert(0, TD)


def load(b):
    spec = importlib.util.spec_from_file_location(f"gen_{b}", os.path.join(RW, b, f"gen_{b}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g1, g2, g3 = load("b1"), load("b2"), load("b3")
import rw_common  # noqa: E402
from common import frac, rbe, regen_entry, shortcut, solution, steps, tex  # noqa: E402

rw_common.NOTE = ("old rule-less row linked to its rule; question rewritten in the book's simple style (setting changed, all-new "
                  "numbers, checked against the book) by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
done, sqrtF = g3.done, g3.sqrtF

TH9B = r"When the second train starts later, meeting distance from the first station is \[ d=\frac{x(D+ty)}{x+y}. \]"
TH20 = (r"If one-way walking and riding together take \(x\) hours, and walking both ways takes \(t\) hours more, then riding both "
        r"ways takes \(x-t\) hours.<br>\[2R=x-t\]")
TH21 = (r"When two people start from opposite ends and the second starts \(t\) hours later, the meeting time measured from the first "
        r"person's start is \[ T=\frac{x(y+t)}{x+y} \]")
TH24 = (r"The halt time per hour is determined by subtracting the with-stop speed from the no-stop speed, dividing by the no-stop "
        r"speed, and multiplying by \(60\).<br>\[ \text{Rest time per hour} = \frac{x-y}{x}\times 60 \]")
TH28 = (r"When a flight starts late and increases speed to arrive on time, the normal speed is "
        r"\[ v=\frac{2D}{t+\sqrt{t^2+\frac{4Dt}{p}}} \]")


def meet_later(D, x, t, y):
    """Rule 9: the train from A at x km/hr starts t hours before the train from B at y km/hr; distance of the meeting point from A."""
    D, x, t, y = F(D), F(x), F(t), F(y)
    lead = x * t
    tm = (D - lead) / (x + y)
    d = lead + x * tm
    trad = steps(("Start of the first train.", rf"In \({tex(t)}\) h it goes alone \({tex(x)}\times{tex(t)} = {tex(lead)}\) km, leaving \({tex(D)} - {tex(lead)} = {tex(D - lead)}\) km between them."),
                 ("Time until they meet.", rf"Both now close the gap at \({tex(x)} + {tex(y)} = {tex(x + y)}\) km/hr: \[ \frac{{{tex(D - lead)}}}{{{tex(x + y)}}} = {tex(tm)}\text{{ h}} \]"),
                 ("Distance of the meeting point from A.", rf"\[ {tex(lead)} + {tex(x)}\times{tex(tm)} = {tex(d)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(D = {tex(D)}\), \(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(t)}\) h."),
                 ("Apply the specified rule.", r"\[ d=\frac{x(D+ty)}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ d = \frac{{{tex(x)}\times({tex(D)} + {tex(t)}\times{tex(y)})}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex(x * (D + t * y))}}}{{{tex(x + y)}}} = {tex(d)}\text{{ km}} \]"))
    fin = rf"\({tex(d)}\) km"
    return done(("number", d), TH9B, trad, rule, fin, [rf"\(D + ty = {tex(D + t * y)}\).", rf"\(\frac{{{tex(x)}\times{tex(D + t * y)}}}{{{tex(x + y)}}} = {tex(d)}\) km."],
                rf"\[ \frac{{{tex(x)}({tex(D)} + {tex(t * y)})}}{{{tex(x + y)}}} = {tex(d)}\text{{ km}} \]")


def later_faster(x, t, y):
    """Rule 11: a slower one at x km/hr, a faster one at y km/hr starting t hours later the same way; where they are together."""
    x, t, y = F(x), F(t), F(y)
    tc = x * t / (y - x)
    d = y * tc
    trad = steps(("Lead of the slower one.", rf"In \({tex(t)}\) h the slower one goes \({tex(x)}\times{tex(t)} = {tex(x * t)}\) km."),
                 ("Time to close the lead.", rf"The faster one gains \({tex(y)} - {tex(x)} = {tex(y - x)}\) km every hour: \[ \frac{{{tex(x * t)}}}{{{tex(y - x)}}} = {tex(tc)}\text{{ h}} \]"),
                 ("Distance from the start.", rf"\[ {tex(y)}\times{tex(tc)} = {tex(d)}\text{{ km}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(t)}\) h."),
                 ("Apply the specified rule.", r"\[ D = \frac{t x y}{y-x} \]"),
                 ("Substitute and simplify.", rf"\[ D = \frac{{{tex(t)}\times{tex(x)}\times{tex(y)}}}{{{tex(y)} - {tex(x)}}} = {tex(d)}\text{{ km}} \]"))
    fin = rf"\({tex(d)}\) km"
    return done(("number", d), g2.TH11, trad, rule, fin, [rf"\(\frac{{{tex(t * x * y)}}}{{{tex(y - x)}}} = {tex(d)}\) km."],
                rf"\[ \frac{{{tex(t)}\times{tex(x)}\times{tex(y)}}}{{{tex(y - x)}}} = {tex(d)}\text{{ km}} \]")


def ride_both(x, t):
    """Rule 20: walk one way + ride back = x hours, walking both ways takes t hours more; riding both ways."""
    x, t = F(x), F(t)
    W = (x + t) / 2
    R = x - W
    trad = steps(("Name the one-way times.", rf"Let walking one way take \(W\) h and riding one way \(R\) h: \(W + R = {tex(x)}\)."),
                 ("Walking both ways.", rf"\(2W = {tex(x)} + {tex(t)} = {tex(x + t)}\), so \(W = {tex(W)}\) h and \(R = {tex(x)} - {tex(W)} = {tex(R)}\) h."),
                 ("Riding both ways.", rf"\[ 2R = 2\times{tex(R)} = {tex(2 * R)}\text{{ hours}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) h, \(t = {tex(t)}\) h."),
                 ("Apply the specified rule.", r"\[ \text{Riding both ways}=x-t \]"),
                 ("Substitute and simplify.", rf"\[ {tex(x)} - {tex(t)} = {tex(x - t)}\text{{ hours}} \]"))
    fin = rf"\({tex(x - t)}\) hours"
    return done(("number", x - t), TH20, trad, rule, fin, [rf"\({tex(x)} - {tex(t)} = {tex(x - t)}\) hours."], rf"\[ {tex(x)} - {tex(t)} = {tex(x - t)}\text{{ hours}} \]")


def meet_second_later(x, t, y):
    """Rule 21: A takes x hours P->Q, B starts from Q t hours after A and takes y hours; meeting time from A's start."""
    x, t, y = F(x), F(t), F(y)
    T = x * (y + t) / (x + y)
    trad = steps(("Part of the road each covers per hour.", rf"A covers \({frac(1 / x)}\) of PQ an hour, B covers \({frac(1 / y)}\)."),
                 ("A's head start.", rf"In \({tex(t)}\) h A covers \({frac(t / x)}\), leaving \({frac(1 - t / x)}\) of the road."),
                 ("Time until they meet.", rf"Together they cover \({frac(1 / x + 1 / y)}\) an hour: \({frac(1 - t / x)} \div {frac(1 / x + 1 / y)} = {tex(T - t)}\) h after B starts, "
                  rf"so \[ {tex(t)} + {tex(T - t)} = {tex(T)}\text{{ hours}} \] after A starts."))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(t = {tex(t)}\)."),
                 ("Apply the specified rule.", r"\[ T=\frac{x(y+t)}{x+y} \]"),
                 ("Substitute and simplify.", rf"\[ T = \frac{{{tex(x)}\times({tex(y)} + {tex(t)})}}{{{tex(x)} + {tex(y)}}} = {tex(T)}\text{{ hours}} \]"))
    fin = rf"\({tex(T)}\) hours"
    return done(("number", T), TH21, trad, rule, fin, [rf"\(\frac{{{tex(x)}\times{tex(y + t)}}}{{{tex(x + y)}}} = {tex(T)}\) hours."],
                rf"\[ \frac{{{tex(x)}({tex(y)} + {tex(t)})}}{{{tex(x)}+{tex(y)}}} = {tex(T)}\text{{ hours}} \]")


def halt(x, y):
    """Rule 24: average speed x km/hr without stops, y km/hr with stops; minutes stopped per hour."""
    x, y = F(x), F(y)
    m = (x - y) / x * 60
    trad = steps(("Distance in one hour with the stops.", rf"In one hour, stops included, the bus covers \({tex(y)}\) km."),
                 ("Time it is really moving.", rf"At \({tex(x)}\) km/hr those \({tex(y)}\) km take \(\frac{{{tex(y)}}}{{{tex(x)}}}\times 60 = {tex(y / x * 60)}\) minutes."),
                 ("The rest of the hour is stopping time.", rf"\[ 60 - {tex(y / x * 60)} = {tex(m)}\text{{ minutes}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
                 ("Apply the specified rule.", r"\[ \frac{x-y}{x}\times 60 \]"),
                 ("Substitute and simplify.", rf"\[ \frac{{{tex(x)} - {tex(y)}}}{{{tex(x)}}}\times 60 = {tex(m)}\text{{ minutes}} \]"))
    fin = rf"\({tex(m)}\) minutes"
    return done(("number", m), TH24, trad, rule, fin, [rf"\(\frac{{{tex(x - y)}}}{{{tex(x)}}}\times 60 = {tex(m)}\) minutes."],
                rf"\[ \frac{{{tex(x - y)}}}{{{tex(x)}}}\times 60 = {tex(m)}\text{{ minutes}} \]")


def late_flight(mins, D, p):
    """Rule 28: leaves mins minutes late from D km away, goes p km/hr faster and lands on time; usual speed."""
    D, p = F(D), F(p)
    t = F(mins, 60)
    root = sqrtF(t * t + 4 * D * t / p)
    v = 2 * D / (t + root)
    trad = steps(("Write the time condition.", rf"\({mins}\) minutes \(= {frac(t)}\) h. At the usual speed \(v\) the trip takes \(\frac{{{tex(D)}}}{{v}}\) h; at \(v + {tex(p)}\) it must take \({frac(t)}\) h less:"
                  rf"\[ \frac{{{tex(D)}}}{{v}} - \frac{{{tex(D)}}}{{v + {tex(p)}}} = {frac(t)} \]"),
                 ("Clear the fractions.", rf"\[ {tex(D)}\times{tex(p)} = {frac(t)}\,v(v + {tex(p)}) \;\Rightarrow\; v^2 + {tex(p)}v - {tex(D * p / t)} = 0 \]"),
                 ("Take the positive root.", rf"\[ v = {tex(v)}\text{{ km/hr}} \]since \({tex(v)}^2 + {tex(p)}\times{tex(v)} = {tex(D * p / t)}\)."))
    rule = steps(("Identify the values.", rf"\(t = {frac(t)}\) h, \(p = {tex(p)}\), \(D = {tex(D)}\)."),
                 ("Apply the specified rule.", r"\[ v=\frac{2D}{t+\sqrt{t^2+\frac{4Dt}{p}}} \]"),
                 ("Substitute and simplify.", rf"\[ \sqrt{{\left({frac(t)}\right)^2 + \frac{{4\times{tex(D)}\times{frac(t)}}}{{{tex(p)}}}}} = \sqrt{{{frac(root * root)}}} = {frac(root)},\qquad "
                  rf"v = \frac{{2\times{tex(D)}}}{{{frac(t)} + {frac(root)}}} = {tex(v)}\text{{ km/hr}} \]"))
    fin = rf"\({tex(v)}\) km/hr"
    return done(("number", v), TH28, trad, rule, fin, [rf"\(\sqrt{{t^2+\frac{{4Dt}}{{p}}}} = {frac(root)}\).", rf"\(v = \frac{{2D}}{{t + {frac(root)}}} = {tex(v)}\) km/hr."],
                rf"\[ \frac{{2\times{tex(D)}}}{{{frac(t)} + {frac(root)}}} = {tex(v)}\text{{ km/hr}} \]")


PLAN = {
    1: [(801, r"A girl cycles for \(45\) minutes at a speed of \(8\) km/hr. Find the distance she covers.", lambda: g1.dist_st(8, 45, "girl"), "km"),
        (802, r"Find the time taken by a bus to cover \(168\) km at a speed of \(42\) km/hr.", lambda: g1.time_ds(168, 42), "hours"),
        (803, r"A ship sails \(1386\) km in \(21\) hours. Find the speed of the ship.", lambda: g1.speed_dt(1386, 21), "km/hr"),
        (804, r"A cyclist moves at \(54\) km/hr. What is this speed in m/sec?", lambda: g1.kmh_to_ms(54), "m/sec"),
        (805, r"A cheetah runs at \(25\) m/sec. What is this speed in km/hr?", lambda: g1.ms_to_kmh(25), "km/hr")],
    2: [(806, r"A woman drives to her office at \(45\) km/hr and comes back home by bus at \(36\) km/hr. Find her average speed for the "
              r"whole trip.", lambda: g1.avg_speed(45, 36), "km/hr"),
        (807, r"A bus goes from town P to town Q at \(72\) km/hr and comes back to P at a lower speed. If its average speed for the "
              r"round trip is \(63\) km/hr, find its speed on the way back.", lambda: g1.return_speed(72, 63), "km/hr")],
    3: [(808, r"A cyclist rides at \(16\) km/hr and rests for \(5\) minutes after every km. How long will he take to ride \(24\) km?",
         lambda: g1.rests(16, 5, 24), plain("3 hrs 30 min", "4 hrs 5 min", "3 hrs 25 min", "2 hrs 45 min"))],
    4: [(809, r"A woman drives from her home to the market at \(24\) km/hr and is late by \(9\) minutes. If she drives at \(36\) km/hr, "
              r"she is \(6\) minutes early. Find the distance from her home to the market.", lambda: g2.late_early(24, 9, 36, 6), "km")],
    5: [(810, r"A girl cycling at \(12\) km/hr reaches her college \(14\) minutes late. Next day she goes \(3\) km/hr faster but is "
              r"still \(6\) minutes late. Find the distance from her house to the college.", lambda: g2.still_late(12, 14, 3, 6), "km")],
    6: [(811, r"A girl cycles to the market at \(16\) km/hr and comes back home at \(8\) km/hr. If she takes \(9\) hours in all, find "
              r"the distance between her home and the market.", lambda: g2.there_back(16, 8, 9), "km")],
    7: [(812, r"A bus finishes a trip in \(8\) hours. It covers the first half of the distance at \(30\) km/hr and the second half at "
              r"\(50\) km/hr. Find the length of the trip.", lambda: g2.halves(8, 30, 50), "km")],
    8: [(813, r"Two towns P and Q are \(320\) km apart. A bus leaves P at \(9\) am and goes towards Q at \(40\) km/hr. Another bus "
              r"leaves Q at \(8\) am and goes towards P at \(50\) km/hr. How far from P will the two buses meet?",
         lambda: g2.head_start_meet(320, 40, 1, 50), "km")],
    9: [(814, r"Two cities P and Q are \(396\) km apart. A car leaves P at \(7\) am and goes towards Q at \(36\) km/hr. Another car "
              r"leaves Q at \(8\) am and goes towards P at \(54\) km/hr. How far from P will the two cars meet?",
         lambda: meet_later(396, 36, 1, 54), "km")],
    10: [(815, r"A woman walks to the market at \(\frac{8}{11}\) of her usual speed and gets there \(18\) minutes late. How many minutes "
               r"does she usually take?", lambda: g2.slow_walk(8, 11, 18), "minutes")],
    11: [(816, r"A cyclist riding at \(20\) km/hr leaves a town at \(6\) am. Another cyclist riding at \(28\) km/hr leaves the same town "
               r"at \(8\) am and goes the same way. How far from the town will the second cyclist catch the first?",
          lambda: later_faster(20, 2, 28), "km")],
    20: [(825, r"A girl walks to a fort and rides back in \(13\) hours. Walking both ways would take her \(5\) hours more. How long "
               r"would she take if she rode both ways?", lambda: ride_both(13, 5), "hours")],
    21: [(826, r"A woman walks from P to Q in \(8\) hours. Another woman starts from Q \(1\) hour after the first one and walks to P in "
               r"\(6\) hours. After how many hours from the first woman's start will they meet?", lambda: meet_second_later(8, 1, 6), "hours")],
    22: [(827, r"A car goes from P to Q in \(5\) hours. Another car leaves Q for P \(1\) hour before the first car and takes \(10\) "
               r"hours. How long after the first car starts will they meet?", lambda: g3.cross_after(5, 1, 10), "hours")],
    23: [(828, r"A bus covers a route in \(54\) minutes at \(28\) km/hr. At what speed must it go to cover the route in \(36\) minutes?",
          lambda: g3.inverse_speed(54, 28, 36), "km/hr")],
    24: [(829, r"Without stops a bus runs at \(90\) km/hr on average, and with stops it runs at \(72\) km/hr on average. For how many "
               r"minutes per hour does the bus stop?", lambda: halt(90, 72), "minutes")],
    25: [(830, r"A cart has to cover \(120\) km in \(8\) hours. It covers \(\frac{1}{3}\) of the distance in \(\frac{1}{2}\) of the "
               r"time. At what speed must it go to cover the rest in the time left?", lambda: g3.rest_speed(120, 8, F(1, 3), F(1, 2)), "km/hr")],
    26: [(831, r"A woman goes to a fair by bus at \(21\) km/hr and walks back at \(7\) km/hr. The whole trip takes \(8\) hours. How far "
               r"is the fair?", lambda: g3.ride_walk(21, 7, 8), "km")],
    27: [(832, r"A woman travels \(280\) km in \(6\) hours, partly by air and partly by train. Had she flown all the way, she would have "
               r"saved \(\frac{2}{3}\) of her time on the train and arrived \(2\) hours early. Find the ratio of the distance by air to "
               r"the distance by train.", lambda: g3.air_train(280, 6, F(2, 3), 2), None)],
    28: [(833, r"A plane leaves \(45\) minutes late from a city \(2250\) km from where it is going. To land on time, the pilot raises "
               r"the speed by \(100\) km/hr. Find the usual speed of the plane.", lambda: late_flight(45, 2250, 100), "km/hr")],
    29: [(834, r"A train leaves a station \(2\) hours before its time. The driver runs it \(8\) km/hr slower than usual, and it reaches "
               r"the next station, \(320\) km away, on time. Find the usual speed of the train.",
          lambda: g3.early_slow(2, 8, 320, r"\(2\) hours"), "km/hr")],
}


def write_batch(here, plan):
    """rw_common.write_batch, except that the rows have no rule yet: each one is linked to its folder's rule card."""
    k = 0
    for n, rows_plan in plan.items():
        folder = os.path.join(here, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(p[0] for p in rows_plan), n
        card = dump["rule_card"]["id"]
        out = []
        for rid, question, fn, unit in rows_plan:
            r = rows[rid]
            assert r["rule_id"] is None, rid
            g = fn()
            llm = r["llm_used"] or ""
            opts = unit if isinstance(unit, dict) else rw_common.options(g["answer"], unit, rw_common.POS[k % len(rw_common.POS)])
            extra = {"question": question, **opts, "e": "",
                     "llm_used": llm if rw_common.NOTE in llm else (llm + "; " if llm else "") + rw_common.NOTE}
            k += 1
            extra = {key: v for key, v in extra.items() if v != r[key]}
            out.append(regen_entry(r, g, card, extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows linked and reworded")


if __name__ == "__main__":
    write_batch(HERE, PLAN)
