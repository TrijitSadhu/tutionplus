"""Question sentences for Simple Interest Rules 34-39 (simple style, setting changed). ITEMS = (key, number pool, sentence, old row id);
each sentence writes its numbers in the order the solver reads them (pool tuples in gen_34_39 order)."""
import os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmt import M, nf  # noqa: E402


def nm(v):
    """a number for the sentence: 12, 2.5, or \\(3\\frac{1}{8}\\) when it needs a fraction."""
    s = nf(v)
    return M(s) if chr(92) in s else s


def fr(v):
    v = F(v)
    return M(rf"\frac{{{v.numerator}}}{{{v.denominator}}}")


T34 = [lambda f1, r1, f2, r2, r3, A: f"A man puts {fr(f1)} of his savings at {nm(r1)}% per annum, {fr(f2)} at {nm(r2)}% and the rest at {nm(r3)}% simple interest. "
                                     f"His yearly income from them is Rs {nm(A)}. Find his savings.",
       lambda f1, r1, f2, r2, r3, A: f"A trust lends {fr(f1)} of its fund at {nm(r1)}%, {fr(f2)} at {nm(r2)}% and the remainder at {nm(r3)}% per annum simple interest. "
                                     f"It earns Rs {nm(A)} a year. How big is the fund?"]
T34T = lambda f1, r1, f2, r2, r3, t, A: (f"Out of a sum, {fr(f1)} is lent at {nm(r1)}%, {fr(f2)} at {nm(r2)}% and the rest at {nm(r3)}% per annum. The simple interest "
                                         f"from all of it for {nm(t)} years is Rs {nm(A)}. Find the sum.")
T35 = [lambda P, I: f"A loan of Rs {nm(P)} earns Rs {nm(I)} as simple interest, and the number of years is the same as the rate per cent per annum. Find the rate.",
       lambda P, I: f"A deposit of Rs {nm(P)} gives Rs {nm(I)} as simple interest. The rate per cent per annum and the number of years are equal. What is the rate?"]
T36 = [lambda r, t, I: f"A man borrows some money at {nm(r)}% per annum simple interest for {nm(t)} years. He pays Rs {nm(I)} as interest. What is the total amount "
                       f"he pays back?",
       lambda r, t, I: f"A shop takes a loan at {nm(r)}% per annum simple interest. After {nm(t)} years the interest due is Rs {nm(I)}. How much must the shop pay "
                       f"in all to clear the loan?"]
T37 = [lambda P1, t1, P2, t2, I: f"A bank gives Rs {nm(P1)} to a farmer for {nm(t1)} years and Rs {nm(P2)} to a weaver for {nm(t2)} years, both at one rate of "
                                 f"simple interest. The two loans bring Rs {nm(I)} in all. What is the rate?",
       lambda P1, t1, P2, t2, I: f"Meena lent Rs {nm(P1)} to a friend for {nm(t1)} years and Rs {nm(P2)} to her cousin for {nm(t2)} years at a single rate. Her total "
                                 f"simple interest was Rs {nm(I)}. At what rate per cent per annum did she lend?"]
T38 = [lambda P1, r1, I1, I2, P2: f"Rs {nm(P1)} at {nm(r1)}% per annum simple interest earns Rs {nm(I1)} in some years. To earn Rs {nm(I2)} on Rs {nm(P2)} in the same "
                                  f"number of years, what rate is needed?",
       lambda P1, r1, I1, I2, P2: f"A deposit of Rs {nm(P1)} at {nm(r1)}% per annum brings Rs {nm(I1)} as simple interest over a few years. What rate would bring Rs "
                                  f"{nm(I2)} on Rs {nm(P2)} over the same years?"]
T39T2 = lambda r: f"How many years will a loan take to double itself at {nm(r)}% per annum simple interest?"
T39T3 = lambda r: f"In how many years will a deposit treble itself at {nm(r)}% per annum simple interest?"
T39R2 = lambda t: f"At what rate per cent per annum simple interest will a farmer's savings double themselves in {nm(t)} years?"
T39R3 = lambda t: f"At what rate per cent per annum simple interest will money lent by a shopkeeper treble itself in {nm(t)} years?"

ITEMS = [(796, "34", T34[0], 796)] + [(f"r34_e{i}", "34", T34[i % 2], None) for i in range(1, 6)] + [("r34_e6", "34t", T34T, None)]
ITEMS += [(797, "35", T35[0], 797)] + [(f"r35_e{i}", "35", T35[i % 2], None) for i in range(1, 6)]
ITEMS += [(f"r36_e{i}", "36", T36[i % 2], None) for i in range(0, 5)]
ITEMS += [(798, "37", T37[0], 798)] + [(f"r37_e{i}", "37", T37[i % 2], None) for i in range(1, 6)]
ITEMS += [(799, "38", T38[0], 799)] + [(f"r38_e{i}", "38", T38[i % 2], None) for i in range(1, 6)]
ITEMS += [(800, "39t2", T39T2, 800), ("r39_e1", "39r2", T39R2, None), ("r39_e2", "39r3", T39R3, None), ("r39_e3", "39t3", T39T3, None), ("r39_e4", "39r2", T39R2, None)]
SENT = {k: (pool, s) for k, pool, s, _ in ITEMS}
NVIS = {"34": 6, "34t": 7, "35": 2, "36": 3, "37": 5, "38": 5, "39t2": 1, "39t3": 1, "39r2": 1, "39r3": 1}
