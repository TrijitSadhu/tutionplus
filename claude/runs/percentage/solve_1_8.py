"""Independent solvers for Percentage Rules 1-8. Each reads the numbers from the question text, then plays the story
forward as a function of the unknown (spend, lose, mix, raise the price, count the votes) and solves that linear
function for the given figure - never through the rule formula gen_1_8.py uses."""
import re
from fractions import Fraction as F
from validate import numbers

NUM = r"(?:\d+(?:\.\d+)?)?(?:\\frac\{\d+\}\{\d+\})?"
PCT = r"(?:\\\))?\s*(?:\\%|%|per cent)"          # 8%, \(12\frac{1}{2}\%\), \(33\frac{1}{3}\) per cent


def val(token):
    return numbers(token)[0]


def pcts(q):
    """Every percentage in reading order: 8%, 62 per cent, \\(12\\frac{1}{2}\\%\\)."""
    return [val(m) for m in re.findall(rf"({NUM}){PCT}", q) if re.search(r"\d", m)]


def others(q):
    """Numbers that are not percentages, in reading order."""
    out = []
    for m in re.finditer(rf"({NUM})({PCT})?", q):
        if m.group(1) and re.search(r"\d", m.group(1)) and not m.group(2):
            out.append(val(m.group(1)))
    return out


def rs(q):
    return [val(m) for m in re.findall(rf"Rs\s*\\?\(?\s*({NUM})", q) if re.search(r"\d", m)]


def unknown(f, target):
    """Solve f(u) = target for a function that is linear in u (found from two trial values)."""
    a, b = f(F(0)), f(F(1))
    return (F(target) - a) / (b - a)


def solve1(k, q):
    frac_ = numbers(q)[0]
    return ("number", unknown(lambda p: p / 100, frac_))           # the per cent p with p/100 equal to the fraction


def solve2(k, q):
    p = pcts(q)[0]
    whole = F(1)
    return ("number", whole * p / 100)


def solve3(k, q):
    if "Shobha" in q:
        n = numbers(q)
        total, sections, rates, need = n[0], n[1:4], n[4:7], n[7]
        assert sum(sections) == total
        right = sum(s * r / 100 for s, r in zip(sections, rates))
        return ("number", total * need / 100 - right)
    if "election" in q:
        share = pcts(q)[0]
        lead = int(re.search(r"(\d+) votes", q).group(1))
        mine = share if ("loses" not in q and "losing" not in q) else 100 - share
        return ("number", unknown(lambda t: t * mine / 100 - t * (100 - mine) / 100, lead))
    x = pcts(q)[0]
    m = re.search(r"(\d+) kg (\d+) g", q)
    if m:
        grams = int(m[1]) * 1000 + int(m[2])
        part = int(grams * x / 100)
        return ("pair", (F(part // 1000), F(part % 1000)))
    m = re.search(r"(\d+) quintals?", q)
    if m:
        kg = int(m[1]) * 100
        part = int(kg * x / 100)
        return ("pair", (F(part // 100), F(part % 100)))
    if "leakage" in q:
        V = others(q)[0]
        return ("number", V - V * x / 100)
    V = rs(q)[0]
    return ("number", sum(V / 100 for _ in range(100)) * x / 100)  # V rebuilt from its hundredths, then x of them


def solve4(k, q):
    x = pcts(q)[0]
    if "spending" in q:
        left = rs(q)[0]
        return ("number", unknown(lambda m: m - m * x / 100, left))
    y = others(q)[-1]
    return ("number", unknown(lambda n: n * x / 100, y))


def solve5(k, q):
    m = re.search(r"(\d+) quintal (\d+) kg of (\d+) metric tonne", q)
    p = re.search(r"(\d+) P \(paise\) of the Re", q)
    if m:
        R, N = int(m[1]) * 100 + int(m[2]), int(m[3]) * 1000       # all in kg
    elif p:
        R, N = int(p[1]), 100                                       # all in paise
    else:
        R, N = numbers(q)[:2]
    return ("number", unknown(lambda p: p / 100 * N, R))


def solve6(k, q):
    ps, rest = pcts(q), others(q)
    x, x1 = ps[0], rest[0]
    N = unknown(lambda n: n * x / 100, x1)
    if len(ps) > 1:
        y1 = N * ps[1] / 100
        return ("pair", (y1, N)) if "find the number" in q else ("number", y1)
    Y = rest[1]
    return ("number", unknown(lambda p: N * p / 100, Y))


def solve7(k, q):
    p = pcts(q)[0]
    if "marks" in q:
        d = others(q)[0]
        return ("number", unknown(lambda m: m * p / 100, d))
    d = rs(q)[-1]
    up = any(w in q for w in ("increased", "raised", "goes up"))
    sign = 1 if up else -1
    orig = unknown(lambda P: (P + sign * P * p / 100) - P, sign * d)    # new price minus old price = the change
    new = orig + sign * d
    if "original and the new" in q:
        return ("pair", (orig, new))
    return ("number", new if "new price" in q else orig)


def solve8(k, q):
    X, Y = pcts(q)[:2]
    x, y = (int(v) for v in re.findall(r"(\d+) parts", q)[:2])
    milk = sum(X / 100 for _ in range(x)) + sum(Y / 100 for _ in range(y))  # one litre per part
    return ("number", milk / (x + y) * 100)
