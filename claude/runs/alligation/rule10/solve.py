"""Independent Rule 10 solver: profit x q minus loss y (N - q) equals P N, solved as a linear equation in q."""
from validate import numbers


def solve(rid, q):
    N, x, y, P = numbers(q)[:4]
    f = lambda k: x * k - y * (N - k) - P * N
    k = -f(0) / (f(1) - f(0))
    return ("pair", (k, N - k))
