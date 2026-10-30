"""Independent solver for Profit and Loss Rule 42: reads the number bought, the price, the first part (a count or a fraction) and the
two rates, works out the real money - cost of all, takings from each part - and compares; not through the weighted-rate formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        N = F(re.search(r"buys (\d+)", q).group(1))
        price = F(re.search(r"Rs (\d+)", q).group(1))
        fr = re.search(r"\\frac\{(\d+)\}\{(\d+)\}", q)
        first = N * F(int(fr.group(1)), int(fr.group(2))) if fr else F(re.search(r"sells (\d+)", q).group(1))
        x, y = [F(t) for t in re.findall(r"(\d+(?:\.\d+)?)%", q)][:2]
        cost = N * price
        takings = first * price * (1 + x / 100) + (N - first) * price * (1 + y / 100)
        return ("number", (takings - cost) / cost * 100)
    except Exception:
        return ("unsolved", q[:40])
