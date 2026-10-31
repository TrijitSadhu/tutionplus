"""Simple Interest Miscellaneous (2026-10-31): the book's 5 Miscellaneous problems (pdf pages 22-23). None of them had a copy in the DB,
so all 5 are new, with all-new numbers, each filed on the stored card of the rule it uses (no new card): M1 rate rises, yearly income up
- capital (Rule 6, #428); M2 rate from one sum, amount of another (Rule 1, #423); M3 two sums at rates 1% apart, total interest - the
two rates (Rule 3, #425); M4 interest for T years, principal n times after half the time (Rule 18, #440); M5 'x is the SI on y and y
the SI on z' (book answer y^2 = xz) - written with numbers: find the first interest (Rule 1, #423). Sentences in sentences.py.
Usage: python misc/gen_misc.py (needs misc/ruleNN/0_current_rows.json from dump_rows.py)."""
import os, sys
from fractions import Fraction as F
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import gen_1_6  # noqa: E402
import gen_14_20  # noqa: E402
from fmt import M, nf  # noqa: E402
from gen_1_6 import done, num  # noqa: E402
from helpers import place  # noqa: E402
from sentences import NVIS, SENT  # noqa: E402

TH = {**{r: gen_1_6.TH[r] for r in (1, 3, 6)}, 18: gen_14_20.TH[18]}
CARD_IDS = {1: 423, 3: 425, 6: 428, 18: 440}
PICK = {
    "m01": (5, F(17, 2), 13020, 372000), "m02": (1700, 2261, F(11, 2), 5400, 7, 7668, 6), "m03": (4650, 7600, 3, 1698, 4, 5),
    "m04": (840, 12, 3, 6, 1680), "m05": (21600, 54, 1080),
}


def m1(r1, r2, d, want):
    r1, r2, d = map(F, (r1, r2, d))
    v = 100 * d / (r2 - r1)
    assert v == want
    trad = [("Extra interest on Rs 100.", rf"The rate goes up by \({nf(r2)} - {nf(r1)} = {nf(r2 - r1)}\), so Rs \(100\) earns Rs \({nf(r2 - r1)}\) more a year."),
            ("Scale up.", rf"\[ 100\times\frac{{{nf(d)}}}{{{nf(r2 - r1)}}} = {nf(v)} \]")]
    return num(6, v, trad, rf"\(r_1 - r_2 = {nf(r2)} - {nf(r1)} = {nf(r2 - r1)}\), \(t = 1\), \(SI_1 - SI_2 = {nf(d)}\).",
               rf"\[ {nf(d)} = \frac{{P\times {nf(r2 - r1)}\times 1}}{{100}} \Rightarrow P = {nf(v)} \]", "Rs", TH)


def m2(P1, A1, t1, P2, t2, want, R):
    P1, A1, t1, P2, t2 = map(F, (P1, A1, t1, P2, t2))
    rate = 100 * (A1 - P1) / (P1 * t1)
    I2 = P2 * rate * t2 / 100
    assert rate == R and P2 + I2 == want
    trad = [("The rate.", rf"Interest \(= {nf(A1)} - {nf(P1)} = {nf(A1 - P1)}\) in \({nf(t1)}\) years: \(\frac{{{nf(A1 - P1)}\times 100}}{{{nf(P1)}\times {nf(t1)}}} = {nf(rate)}\%\)."),
            ("The new amount.", rf"\[ \frac{{{nf(P2)}\times {nf(rate)}\times {nf(t2)}}}{{100}} = {nf(I2)};\quad {nf(P2)} + {nf(I2)} = {nf(P2 + I2)} \]")]
    return num(1, P2 + I2, trad, rf"First: \(P = {nf(P1)}\), \(SI = {nf(A1 - P1)}\), \(T = {nf(t1)}\); then \(P = {nf(P2)}\), \(T = {nf(t2)}\).",
               rf"\[ R = \frac{{100\times {nf(A1 - P1)}}}{{{nf(P1)}\times {nf(t1)}}} = {nf(rate)},\quad SI = \frac{{{nf(P2)}\times {nf(rate)}\times {nf(t2)}}}{{100}} = {nf(I2)} \]"
               rf"Amount \(= {nf(P2)} + {nf(I2)} = {nf(P2 + I2)}\).", "Rs", TH)


def m3(X1, X2, t, I, ra, rb):
    X1, X2, t, I = map(F, (X1, X2, t, I))
    yearly = I / t
    r = (yearly - X2 / 100) * 100 / (X1 + X2)
    assert (r, r + 1) == (ra, rb)
    whole = (X1 * r + X2 * (r + 1)) / (X1 + X2)
    trad = [("Interest of one year.", rf"\({nf(I)} \div {nf(t)} = {nf(yearly)}\). Taking away the extra \(1\%\) on Rs \({nf(X2)}\) (Rs \({nf(X2 / 100)}\)) leaves "
                                      rf"\({nf(yearly - X2 / 100)}\), which is the lower rate on the whole Rs \({nf(X1 + X2)}\)."),
            ("The rates.", rf"\[ \frac{{{nf(yearly - X2 / 100)}\times 100}}{{{nf(X1 + X2)}}} = {nf(r)}\%,\qquad {nf(r)} + 1 = {nf(r + 1)}\% \]")]
    ident = rf"\(x_1 = {nf(X1)}\) at \(r\%\), \(x_2 = {nf(X2)}\) at \((r+1)\%\); rate on the whole \(= \frac{{{nf(yearly)}\times 100}}{{{nf(X1 + X2)}}} = {nf(whole)}\%\)."
    sub = rf"\[ \frac{{{nf(X1)}r + {nf(X2)}(r+1)}}{{{nf(X1 + X2)}}} = {nf(whole)} \Rightarrow {nf(X1 + X2)}r = {nf(whole * (X1 + X2) - X2)} \Rightarrow r = {nf(r)} \]" \
          rf"The rates are \({nf(r)}\%\) and \({nf(r + 1)}\%\)."
    pct = chr(92) + "%"
    return done(3, ("pair", (r, r + 1)), f"{M(nf(r) + pct)} and {M(nf(r + 1) + pct)}", trad, ident, sub, TH)


def m4(I, T, n, t, want):
    I, T, n, t = map(F, (I, T, n, t))
    assert T == 2 * t
    x = I * t / T
    v = (n + 1) * x
    assert v == want
    trad = [("Interest of the first half.", rf"Rs \({nf(I)}\) in \({nf(T)}\) years is \({nf(I / T)}\) a year, so the first \({nf(t)}\) years give \({nf(x)}\)."),
            ("The second half.", rf"With \({nf(n)}\) times the principal, the next \({nf(T - t)}\) years give \({nf(n)}\times {nf(x)} = {nf(n * x)}\); total \(= {nf(x)} + {nf(n * x)} = {nf(v)}\).")]
    return num(18, v, trad, rf"\(x = {nf(x)}\) (interest of the first \({nf(t)}\) years), \(n = {nf(n)}\).", rf"\[ ({nf(n)} + 1)\times {nf(x)} = {nf(v)} \]", "Rs", TH)


def m5(P, z, want):
    P, z = F(P), F(z)
    y = F(isqrt(int(P * z)))
    assert y * y == P * z and y == want
    k = y / P
    trad = [("The same fraction.", r"Same rate and time, so each interest is the same fraction \(\frac{RT}{100}\) of its principal: \(\frac{y}{" + nf(P) + r"} = \frac{" + nf(z) + r"}{y}\)."),
            ("Solve.", rf"\[ y^{{2}} = {nf(P)}\times {nf(z)} = {nf(P * z)} \Rightarrow y = {nf(y)} \]Check: \({nf(y)}\) is \({nf(k * 100)}\%\) of \({nf(P)}\), and \({nf(z)}\) is \({nf(k * 100)}\%\) of \({nf(y)}\).")]
    return num(1, y, trad, rf"\(SI = \frac{{PRT}}{{100}}\) with the same \(R\) and \(T\): \(y = {nf(P)}\times\frac{{RT}}{{100}}\), \({nf(z)} = y\times\frac{{RT}}{{100}}\).",
               rf"\[ \frac{{RT}}{{100}} = \frac{{y}}{{{nf(P)}}} = \frac{{{nf(z)}}}{{y}} \Rightarrow y^{{2}} = {nf(P * z)},\quad y = {nf(y)} \]", "Rs", TH)


FN = {"m1": m1, "m2": m2, "m3": m3, "m4": m4, "m5": m5}
_below = gen_1_6.build_opts


def build_opts(g, kind, wrong):
    if kind == "pct_pair":
        a, b = g["answer"][1]
        pct = chr(92) + "%"
        f = lambda x, y: f"{M(nf(x) + pct)} and {M(nf(y) + pct)}"
        return place(f(a, b), [f(x, y) for x, y in (wrong or [(a + 1, b + 1), (a - F(1, 2), b - F(1, 2)), (a + 2, b + 2)])])
    return _below(g, kind, wrong)


gen_1_6.build_opts = build_opts
NEW = {}
for k, (rule, pool, s) in SENT.items():
    p = PICK[k]
    NEW.setdefault(rule, []).append((k, s(*p[:NVIS[pool]]), (lambda f=FN[pool], p=p: f(*p)), "pct_pair" if pool == "m3" else "Rs", None))

if __name__ == "__main__":
    gen_1_6.main({}, NEW, None, sorted(NEW), CARD_IDS)
