"""Independent Rule 8 solver: solves x*t + y*(T - t) = D for the hours t spent on the bus."""
from validate import numbers


def solve(rid, q):
    D, T, x, y = numbers(q)[:4]
    f = lambda t: x * t + y * (T - t) - D
    t = -f(0) / (f(1) - f(0))
    bus, train = x * t, y * (T - t)
    s = q.strip()
    if "ratio" in s:
        return ("ratio", bus / train)
    if "respectively" in s:
        return ("pair", (bus, train))
    if s.endswith("by train?"):
        return ("number", train)
    if s.endswith("by bus?"):
        return ("number", bus)
    raise ValueError(q)
