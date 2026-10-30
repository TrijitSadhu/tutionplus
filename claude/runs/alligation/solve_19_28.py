"""Independent solvers for Rules 19-28. Each reads the numbers from the question text and solves by adding up
amounts, simulating the draws step by step, searching, or a linear solve - never through the rule formula."""
import re
from fractions import Fraction as F
from validate import numbers


def root(f):
    return -f(0) / (f(1) - f(0))


def solve19(rid, q):
    pcts = [F(p) for p in re.findall(r"(\d+)%", q)]
    pairs = [(p, 100 - p) for p in pcts] if pcts else [(F(a), F(b)) for a, b in re.findall(r"(\d+)\s*:\s*(\d+)", q)]
    extra = re.search(r"(\d+)\s*litres of water is added", q)
    sizes = [F(s) for s in re.findall(r"(\d+)\s*litres", q)]
    if extra:
        sizes.remove(F(extra[1]))
    assert len(sizes) == len(pairs), (sizes, pairs)
    first = sum(s * a / (a + b) for s, (a, b) in zip(sizes, pairs))
    second = sum(s * b / (a + b) for s, (a, b) in zip(sizes, pairs)) + (F(extra[1]) if extra else 0)
    return ("ratio", first / second)


def solve20(rid, q):
    M1, x, M2, y, z = numbers(q)[:5]
    return ("number", root(lambda w: M1 * x + M2 * y - z * (M1 + M2 + w)))


def solve21(rid, q):
    if "whisky" in q:
        a, b, c = numbers(q)[:3]
        return ("number", root(lambda f: a * (1 - f) + b * f - c))
    (a1, b1), (a2, b2), (a3, b3) = [(F(a), F(b)) for a, b in re.findall(r"(\d+)\s*:\s*(\d+)", q)][:3]
    k = root(lambda k: (a1 / (a1 + b1)) * k + a2 / (a2 + b2) - a3 / (a3 + b3) * (k + 1))   # k kg of first per 1 kg of second
    return ("ratio", k)


def solve22(rid, q):
    n, Pr, m, x, y = numbers(q)[:5]
    need = n * Pr * (1 + y / 100) - m * Pr * (1 + x / 100)
    return ("number", need / (n - m))


def solve23(rid, q):
    word = re.search(r"replaced (?:with|by) (\w+)|(\w+) substituted", q)
    word = word[1] or word[2]
    parts = {w: F(c) for c, w in re.findall(r"(\d+)\\?\)?\s*parts? (?:of which are |of )?(\w+)", q)}
    added = parts[word]
    kept = [v for w, v in parts.items() if w != word][0]
    share = kept / (kept + added)
    return ("number", root(lambda f: share * (1 - f) - F(1, 2)))


def solve24(rid, q):
    v = numbers(q)
    if rid == 1192:
        L, per, cost, y = v[:4]
        x, c = cost / per, F(0)
    elif rid == 1194:
        c, L, x, y = v[:4]
    elif rid == 1195:
        n1, p1, L, n2, p2, dozen = v[:6]
        c, x, y = p1 / n1, p2 / n2, dozen / 12
    else:
        L, x, y = v[:3]
        c = F(0)
    return ("number", root(lambda w: L * x + c * w - y * (L + w)))


def solve25(rid, q):
    v = numbers(q)
    if "How many litres" in q:
        x, y, n, t = v[:4]
        return ("number", root(lambda m: n * x + m * y - t * (n + m)))
    x, y, n, m = v[:4]
    return ("number", (n * x + m * y) / (n + m))


def solve26(rid, q):
    a, b, x, total, y = numbers(q)[:5]
    old = total / (1 + y / 100)
    wa, wb = old * a / (a + b), old * b / (a + b)
    return ("number", (total - wa * (1 + x / 100) - wb) / wb * 100)


def solve27(rid, q):
    v = numbers(q)
    if "lotion" in q:
        a, b = v[:2]
        return ("number", root(lambda f: a / (a + b) * (1 - f) - F(1, 2)))
    M, p0, p1 = v[:3]
    hits = []
    for R in range(1, int(M)):
        oxygen = M * p0 / 100
        for _ in range(2):
            oxygen -= oxygen * R / M
        if oxygen == M * p1 / 100:
            hits.append(F(R))
    assert len(hits) == 1, hits
    return ("number", hits[0])


WORD = {"one-fourth": F(1, 4), "one-twentieth": F(1, 20), "One-third": F(1, 3)}


def solve28(rid, q):
    frac = next((v for w, v in WORD.items() if w in q), None)
    n = 5 if "5 times" in q else 3 if ("third" in q or "three times" in q) else 2
    if frac is not None:
        x, y = F(1), frac
    else:
        x, y = numbers(q)[:2]
    amount = x
    for _ in range(n):
        amount -= amount * y / x
    if "removed" in q:
        return ("number", 1 - amount)
    if "original quantity" in q:
        return ("ratio", amount / x)
    if re.search(r"\b(ratio|proportion)\b", q):
        return ("ratio", amount / (x - amount))
    return ("number", amount)
