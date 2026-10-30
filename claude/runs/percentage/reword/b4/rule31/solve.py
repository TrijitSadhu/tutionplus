from solve_25_32 import solve31 as _solve


def solve(k, q):
    try:
        return _solve(k, q)
    except Exception:                       # a broken (mutated) question must count as unsolved, not crash the check
        return ("unsolved", q[:40])
