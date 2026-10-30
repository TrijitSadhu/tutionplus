"""Independent solver for Average Rules 6-11, keyed by row id / payload key; reads the numbers from the question in order, builds an
actual list of members with the stated average (uneven values), makes the change the story describes (take one out, add one, shift
or scale every number, swap members) and reads the answer off the list - a linear solve for the unknown member, never the rule formula.
Algebraic questions are worked with x = 7, y = 3 (the validator compares expressions there)."""
import re
from fractions import Fraction as F

X, Y = F(7), F(3)


def nums(q):
    return [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def mean(xs):
    return F(sum(xs), len(xs))


def team(n, avg, fixed=()):
    """n uneven members averaging avg, the members in `fixed` among them."""
    n = int(n)
    fixed = [F(f) for f in fixed]
    k = n - len(fixed)
    others = [F(avg) + (i % 3 - 1) * F(i, 2) for i in range(k)]
    others[0] += n * F(avg) - sum(fixed) - sum(others)
    xs = fixed + others
    assert mean(xs) == F(avg)
    return xs


def removed(n, x, y):
    """n members average x; one leaves and the rest average y -> the one that left."""
    rest = team(n - 1, y)
    return lin(lambda z: mean(rest + [z]) - x)


def joined(n, x, y):
    old = team(n, x)
    return lin(lambda z: mean(old + [z]) - y)


def shifted(n, m, d):
    return mean([a + d for a in team(n, m)])


def scaled(n, m, f):
    return mean([a * f for a in team(n, m)])


def swapped(n, change, out):
    """n members, those in `out` replaced by as many newcomers; the average moves by `change` -> the newcomers' average."""
    old = team(n, 30 + sum(out) / len(out), out)
    stay = old[len(out):]
    k = len(out)
    tot = lin(lambda t: mean(stay + [t / k] * k) - mean(old) - change)
    return tot / k


def same_after(n, yrs):
    """the average now equals the average yrs years ago because one member was swapped for a younger one -> how much younger."""
    then = team(n, 40)
    now_old = [a + yrs for a in then]                     # everybody yrs older
    stay = now_old[1:]
    z = lin(lambda t: mean(stay + [t]) - mean(then))      # the newcomer's age that keeps the average
    return now_old[0] - z


def solve(k, q):
    try:
        v = nums(q)
        if k == 503 or k in ("r6_e3", "r6_e4", "r6_e5"):     # c people and one more average x; leaving that one out, the average drops by d
            c, x, d = v[:3]
            return ("number", removed(c + 1, x, x - d))
        if k == 504:                                           # total age of N people is T; leaving one out, the average drops by d
            N, T, d = v[:3]
            return ("number", removed(N, T / N, T / N - d))
        if k == "r6_ex":                                       # c sacks and one box average x; without the box the average is y
            c, x, y = v[:3]
            return ("number", removed(c + 1, x, y))
        if k == 505:                                           # n average x; one more joins and the average goes up by d
            n, x, d = v[:3]
            return ("number", joined(n, x, x + d))
        if k in ("r8_ex", "r8_e1", "r8_e2", "r8_e3", "r8_e4", "r8_e5"):
            n, x, y = v[:3]
            return ("number", joined(n, x, y))
        if k in ("r7_ex1", "r7_ex2", "r7_e1", "r7_e3"):
            n, m, d = v[:3]
            down = re.search(r"taken away|subtracted", q) is not None
            return ("number", shifted(n, m, -d if down else d))
        if k == "r7_e2":                                      # x numbers average cx; x is added to each
            c = F(re.search(r"is \\\((\d+)x\\\)", q)[1])
            return ("expr", shifted(X, c * X, X))
        if k == "r7_e4":                                      # x numbers average cx; x + d is taken from each
            c = F(re.search(r"is \\\((\d+)x\\\)", q)[1])
            d = F(re.search(r"x\+(\d+)", q)[1])
            return ("expr", shifted(X, c * X, -(X + d)))
        if k in ("r9_ex1", "r9_ex2", "r9_e2", "r9_e3", "r9_e4", "r9_e5"):
            n, m, f = v[:3]
            return ("number", scaled(n, m, 1 / f if "divided" in q else f))
        if k == "r9_e1":                                      # x numbers average y; each multiplied by x + d
            d = F(re.search(r"x\+(\d+)", q)[1])
            return ("expr", scaled(X, Y, X + d))
        if k in ("r10_ex1", "r10_ex2", "r10_e1", "r10_e2", "r10_e3", "r10_e5", "r10_e6", "r10_e7", "r10_e8"):
            n, up = v[:2]
            return ("number", swapped(n, up, v[2:]))
        if k == "r10_e4":
            n, yrs = v[:2]
            return ("number", same_after(n, yrs))
        if k in ("r11_ex", "r11_e1", "r11_e2", "r11_e3"):     # n members, average down by mo months, one aged a replaced
            n, mo, a = v[:3]
            age = swapped(n, -mo / 12, [a])
            if k == "r11_ex":
                yy = int(age)
                return ("pair", (F(yy), (age - yy) * 12))
            return ("number", age)
        if k in ("r11_e4", "r11_e5", "r11_e6"):               # n, months, c members aged ..., replaced by c new ones
            n, mo, c = v[:3]
            return ("number", swapped(n, -mo / 12, v[3:3 + int(c)]))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
