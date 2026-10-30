from solve_30_36 import solve34 as _solve


def solve(k, q):
    try:
        return _solve(k, q)
    except Exception:                       # a broken (mutated) question must count as unsolved, not crash the check
        return ("unsolved", q[:40])
