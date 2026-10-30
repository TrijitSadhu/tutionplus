"""Independent Rule 5 solver: keeps track of how much of each component there is, and solves the balance
as a linear equation in the added amount (no rule formula)."""
from fractions import Fraction as F
from validate import numbers


def linear_root(f):
    return -f(0) / (f(1) - f(0))


def solve(rid, q):
    v = numbers(q)
    if rid in (839, 1104, 1107, 1111, 1105, 1109):          # n units with x% of the substance that is added
        n, x, y = v[:3]
        return ("number", linear_root(lambda a: n * x / 100 + a - (n + a) * y / 100))
    if rid in (1106, 1108):                                 # unleaded u1% of n litres becomes u2% after adding leaded
        u1, n, u2 = v[:3]
        return ("number", linear_root(lambda a: (n + a) * u2 / 100 - n * u1 / 100) * 1000)   # answer in ml
    if rid == 1110:                                         # wheat w1% of n quintals becomes w2% after adding barley
        w1, n, w2 = v[:3]
        return ("number", linear_root(lambda a: (n + a) * w2 / 100 - n * w1 / 100))
    if rid == 1112:                                         # n litres with alc% alcohol, add w litres of water
        n, alc, w = v[:3]
        return ("number", n * alc / 100 / (n + w) * 100)
    if rid in (1113, 1114, 1115):                           # n units, milk:water a:b -> c:d by adding water
        n, a, b, c, d = v[:5]
        milk, water = n * a / (a + b), n * b / (a + b)
        return ("number", linear_root(lambda w: milk * d - (water + w) * c))
    raise KeyError(rid)
