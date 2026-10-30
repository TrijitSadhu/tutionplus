"""Independent Rule 9 solver: total profit x(N - q) + y q = P N, solved as a linear equation in q."""
from validate import numbers


def solve(rid, q):
    N, x, y, P = numbers(q)[:4]
    f = lambda k: x * (N - k) + y * k - P * N
    return ("number", -f(0) / (f(1) - f(0)))
