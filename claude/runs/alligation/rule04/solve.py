"""Independent Rule 4 solver: reads the gain % from the text, then finds water/spirit by simulating one litre
of spirit at Rs 100 and asking how much free water makes the sale at Rs 100 per litre return that gain."""
import re
from fractions import Fraction as F


def solve(rid, q):
    m = re.search(r"(\d+)\\frac\{(\d+)\}\{(\d+)\}", q)
    g = F(int(m[1])) + F(int(m[2]), int(m[3])) if m else F(re.search(r"gain\s*\\?\(?\s*(\d+(?:\.\d+)?)", q)[1])
    # 1 litre spirit costs 100; with w litres of water the sale is 100*(1 + w); gain = 100*w / 100 = w
    w = g / 100
    return ("ratio", w / 1)
