"""Independent solvers for Rules 11-18. Each reads the numbers from the question text and solves by counting,
simulation or a linear solve - never through the rule formula gen_11_18.py uses."""
import re
from fractions import Fraction as F
from validate import numbers


def root(f):
    return -f(0) / (f(1) - f(0))


def solve11(rid, q):
    N, x, y, P = numbers(q)[:4]
    k = root(lambda k: x * k - y * (N - k) + P * N)          # overall LOSS of P%
    return ("pair", (k, N - k))


def solve12(rid, q):
    a, b, x, y = numbers(q)[:4]
    new_saving = (a + b) * (1 + x / 100) - a * (1 + y / 100)
    return ("number", (new_saving - b) / b * 100)


def solve13(rid, q):
    L, x, y, z = numbers(q)[:4]
    m = root(lambda m: x * m + y * (L - m) - z * L)
    return ("ratio", m / (L - m)) if "ratio" in q else ("pair", (m, L - m))


def solve14(rid, q):
    H, L = (int(v) for v in numbers(q)[:2])
    four = [f for f in range(H + 1) if 4 * f + 2 * (H - f) == L]
    assert len(four) == 1
    f, t = F(four[0]), F(H - four[0])
    if "chickens and goats" in q:
        return ("pair", (t, f))
    if "How many rabbits" in q:
        return ("number", f)
    if "How many pigeons" in q:
        return ("number", t)
    raise ValueError(q)


def solve15(rid, q):
    v = numbers(q)
    a, b, L = v[:3]
    P, x, y = (v[3], v[4], v[5]) if len(v) >= 6 else (L, v[3], v[4])     # "filled with B" puts back L litres
    hits = []
    for V in range(1, 2001):
        V = F(V)
        if V <= L:
            continue
        A, B = a / (a + b) * (V - L), b / (a + b) * (V - L) + P
        if A * y == B * x:
            hits.append(a * V / (a + b))
    assert len(hits) == 1, hits
    return ("number", hits[0])


def solve16(rid, q):
    L, a, b, x, y = numbers(q)[:5]
    milk, water = L * a / (a + b), L * b / (a + b)
    hits = [F(w) for w in range(0, 5001) if (water + w) * x == milk * y]
    assert len(hits) == 1
    return ("number", hits[0])


def solve17(rid, q):
    pcts = [F(p) for p in re.findall(r"(\d+)\\%", q)]
    pairs = [(p, 100 - p) for p in pcts] if pcts else [(F(a), F(b)) for a, b in re.findall(r"(\d+)\s*:\s*(\d+)", q)]
    V = 7                                                  # any equal size
    first = sum(V * a / (a + b) for a, b in pairs)
    second = sum(V * b / (a + b) for a, b in pairs)
    return ("ratio", first / second)


def solve18(rid, q):
    M, f1, N, f2 = numbers(q)[:4]
    zinc = M * f1 + N * f2
    return ("ratio", zinc / (M + N - zinc))
