"""Independent solver for the Percentage Miscellaneous rows (old row ids) and new questions (keys m01 ...): reads the numbers from
the question in order and works each problem out from first principles - counting people, trial values, money on a base of 100 -
not through the rule formulas."""
import re
from fractions import Fraction as F


def nums(q):
    fr = [F(int(a), int(b)) for a, b in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)]
    q = re.sub(r"\\frac\{\d+\}\{\d+\}", " FRAC ", q)
    out, fi = [], 0
    for t in re.findall(r"FRAC|\d+(?:\.\d+)?", q):
        if t == "FRAC":
            out.append(fr[fi]); fi += 1
        else:
            out.append(F(t))
    return out


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def passage(q):
    n, g, b, gt_pct, both_pct, be_pct = [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)[:6]]
    girls, boys = n * g / (g + b), n * b / (g + b)
    gt = bt = girls * gt_pct / 100
    gb, be = girls * both_pct / 100, boys * be_pct / 100
    ge, bb = girls - gt - gb, boys - bt - be
    return dict(girls=girls, boys=boys, gt=gt, bt=bt, gb=gb, be=be, ge=ge, bb=bb, n=n)


def solve(k, q):
    try:
        v = nums(q)
        half = F(1, 2) if "half" in q else None
        if k == 662:
            x, y, yearly = v[:3]
            return ("number", lin(lambda inc: inc * (1 - x / 100) * (1 - y / 100) * half * 12 - yearly))
        if k == 663:
            x, spent, left = v[0], v[1], v[2]
            fifth = F(1, 5) if "one-fifth" in q else None
            return ("number", lin(lambda a: a * x / 100 * fifth - spent - left))
        if k == 664:
            p, first, right, a, b = v[:5]
            for blocks in range(1, 1000):
                rest = blocks * b
                if (right + blocks * a) * 100 == p * (first + rest):
                    return ("number", first + rest)
            return ("unsolved", "no count")
        if k == 665:
            n, oa, both = v[:3]
            only_a = n * oa / 100
            return ("number", n - only_a)
        if k == 666:
            a, b, cm, cf, adult_f = v[:5]
            fem = lin(lambda f: f * (1 - cf / 100) - adult_f)
            return ("number", fem + fem * a / b)
        if k == 667:
            r1, r2, r3, u1, u2, u3, total = v[:7]
            kk = lin(lambda t: r1 * t * (1 + u1 / 100) + r2 * t * (1 + u2 / 100) + r3 * t * (1 + u3 / 100) - total)
            return ("number", r1 * kk)
        if k == 668:
            p1, p2, total = v[:3]
            return ("number", lin(lambda c: c * p2 / 100 * p1 / 100 + c * p2 / 100 + c - total) * p2 / 100 * p1 / 100)
        if k in (669, 672):
            if k == 669:
                N, Rv = v[0], v[1]
            else:
                Rv, N = v[0], v[1]
            return ("number", Rv / N * 100)
        if k == 670:
            x, V, kk = v[:3]
            return ("number", lin(lambda n: kk * n - x * V / 100))
        if k == 671:
            x, y = v[:2]
            return ("number", (x / 100) * (y / 100))
        if k == 673:
            x, V, kk = v[:3]
            for n in range(1, 10000):
                if x * V / 100 / n == kk:
                    return ("number", F(n))
            return ("unsolved", "no number")
        if k == 674:
            x, c = v[:2]
            return ("number", lin(lambda n: n * x / 100 + c - n))
        if k == 675:
            d, fr_ = v[0], v[1]
            return ("number", d * fr_ * 100)
        if k == 676:
            x = v[0]
            cost = F(100)
            sp = cost * (1 + x / 100) * (1 - v[1] / 100)
            return ("signed", (sp - cost) / cost * 100)
        if k == 677:
            x = v[0]
            b = F(100); a = b * x / 100
            return ("number", b / a * 100)
        if k == 678:
            W, up, down = v[:3]
            got = W * (1 + up / 100)
            return ("number", got - got * (1 - down / 100))
        if k == 679:
            x, V = v[:2]
            return ("number", V - V * x / 100)
        if k == "m01":
            n, oa, both = v[:3]
            return ("number", n - n * oa / 100 - both)
        if k == "m02":
            n, gp, only_b, only_b_boys, girls_both = v[:5]
            boys = lin(lambda b: b + b * gp / 100 - n)
            return ("number", (n - boys) - (only_b - only_b_boys) - girls_both)
        if k in ("m09", "m10", "m11", "m12", "m13"):
            t = passage(q)
            return {"m09": ("number", t["ge"]), "m10": ("number", t["bt"] + t["bb"]), "m11": ("number", (t["gt"] + t["bt"]) / t["n"] * 100),
                    "m12": ("number", t["gb"] + t["bb"]), "m13": ("number", t["bt"] + t["be"])}[k]
        if k == "m22":
            x, y = v[:2]
            P_ = F(100)
            Q = P_ * x / y                                   # x% of P = y% of Q
            return ("number", Q / P_ * 100)
        if k == "m28":
            x, y = v[:2]
            b = F(100); a = b * y / x
            return ("ratio", a / b)
        if k == "m26":
            a = v[0]
            L = 100 * (1 + a / 100)
            Bn = 10000 / L
            return ("number", 100 - Bn)
        if k == "m30":
            t = v[0]
            y = F(100); x = t * y
            return ("number", (x - y) / x * 100)
        if k == "m27":
            x, final = v[0], v[2]
            return ("number", lin(lambda p: p * (1 + x / 100) * (1 - v[1] / 100) - final))
        if k == "m31":
            e, m_, bf, passed = v[:4]
            failed_one = (100 - e) + (100 - m_) - bf
            return ("number", lin(lambda n: n * (100 - failed_one) / 100 - passed))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
