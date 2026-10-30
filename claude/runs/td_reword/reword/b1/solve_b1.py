"""Independent solver for Time & Distance rewording batch 1 (Rules 1-3), keyed by row id. It reads the numbers from the
question text in order and works in metres and seconds, simulates the trips (a chosen distance each way, minute-by-minute
walking with rests) or searches - never through the rule formulas gen_b1.py uses."""
from fractions import Fraction as F
from validate import numbers


def metres_per_sec(km_per_hr):
    return F(km_per_hr) * 1000 / 3600


def trip_average(x, y, each=F(1)):
    """Go `each` km at x and `each` km at y: total distance / total time."""
    return 2 * each / (each / x + each / y)


def walk_with_rests(x, rest_min, y, every=1):
    """Minute-by-minute: walk at x km/hr, rest after each `every` km (not at the destination); minutes in all."""
    per_km = F(60) / x
    minutes, km = F(0), 0
    while km < y:
        minutes += per_km
        km += 1
        if km < y and km % every == 0:
            minutes += rest_min
    return minutes


def solve(rid, q):
    try:
        v = numbers(q)
        if rid in (1416, 1428):                        # minutes, km/hr -> km
            mins, S = v[:2]
            return ("number", metres_per_sec(S) * mins * 60 / 1000)
        if rid == 1417:
            D, S = v[:2]
            return ("number", next(F(k, 10) for k in range(1, 10 ** 6) if S * F(k, 10) == D))
        if rid == 1418:
            D, T = v[:2]
            return ("number", D * 3600 / (T * 3600))
        if rid in (1419, 1421):
            return ("number", v[0] * 1000 / 3600)
        if rid == 1420:
            return ("number", v[0] * 3600 / 1000)
        if rid == 1422:                                # seconds, metres -> km/hr
            secs, m = v[:2]
            return ("number", m / 1000 / (secs / 3600))
        if rid in (1423, 1429):                        # metres, minutes -> km/hr
            m, mins = v[:2]
            return ("number", m / 1000 / (mins / 60))
        if rid == 1424:
            kmh, ms = v[:2]
            return ("ratio", metres_per_sec(kmh) / ms)
        if rid == 1425:                                # km, minutes, seconds -> km per second
            D, mins, secs = v[:3]
            return ("number", D / (mins * 60 + secs))
        if rid == 1426:                                # circumference m, turns, seconds -> km/hr
            c, turns, secs = v[:3]
            return ("number", c * turns / 1000 / (secs / 3600))
        if rid == 1427:                                # m/sec, seconds -> km
            ms, secs = v[:2]
            return ("number", ms * secs / 1000)
        if rid == 1430:
            d, h1, h2 = v[:3]
            return ("number", d * h2 / h1)
        if rid == 1431:                                # km/hr, minutes -> metres
            kmh, mins = v[:2]
            return ("number", metres_per_sec(kmh) * mins * 60)
        if rid == 1432:                                # minutes at km/hr, then new minutes -> km/hr
            m1, s1, m2 = v[:3]
            D = metres_per_sec(s1) * m1 * 60
            return ("number", D / (m2 * 60) * 3600 / 1000)
        if rid in (1433, 1434, 1435, 1436):
            x, y = v[:2]
            return ("number", trip_average(x, y))
        if rid == 1437:                                # go at x, average A -> back speed (search)
            x, A = v[:2]
            return ("number", next(F(k, 4) for k in range(1, 4 * 1000) if trip_average(x, F(k, 4)) == A))
        if rid == 1438:
            d1, x, d2, y = v[:4]
            return ("number", (d1 + d2) / (d1 / x + d2 / y))
        if rid in (1439, 1440, 1441):
            x, t, y = v[:3]
            h, m = divmod(int(walk_with_rests(x, t, int(y))), 60)
            return ("pair", (F(h), F(m)))
        if rid == 1442:
            x, t, k, y = v[:4]
            h, m = divmod(int(walk_with_rests(x, t, int(y), int(k))), 60)
            return ("pair", (F(h), F(m)))
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
