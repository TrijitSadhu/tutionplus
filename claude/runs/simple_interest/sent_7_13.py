"""Question sentences for Simple Interest Rules 7-13 (simple style, setting changed). ITEMS = (key, number pool, sentence, old row id);
each sentence writes its numbers in the order the solver reads them (pool tuples in solve_7_13 / gen_7_13 order)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmt import nf  # noqa: E402

T7 = [lambda A, t, r: f"A farmer owes Rs {nf(A)}, due in {nf(t)} years. He clears it by equal payments at the end of each year, with simple interest at {nf(r)}% per annum. How much does he pay each year?",
      lambda A, t, r: f"What equal yearly payment will clear a debt of Rs {nf(A)} due in {nf(t)} years, if simple interest is {nf(r)}% per annum?",
      lambda A, t, r: f"A shopkeeper must repay Rs {nf(A)} at the end of {nf(t)} years. He pays an equal sum every year, and money earns {nf(r)}% per annum simple interest. What is each yearly payment?"]
T8 = [lambda r1, t1, r2, t2, t12, r3, I, T: f"A savings scheme gives {nf(r1)}% per annum simple interest in the first {nf(t1)} years, then {nf(r2)}% per annum for {nf(t2)} "
                                           f"more years, and {nf(r3)}% per annum once {nf(t12)} years are over. A deposit brings Rs {nf(I)} as interest after {nf(T)} years. "
                                           f"How much was deposited?",
      lambda r1, t1, r2, t2, t12, r3, I, T: f"A trader took a loan at {nf(r1)}% per annum for the first {nf(t1)} years, {nf(r2)}% per annum for the next {nf(t2)} years and "
                                           f"{nf(r3)}% per annum beyond {nf(t12)} years. He paid Rs {nf(I)} as simple interest in all, at the end of {nf(T)} years. How much was the loan?"]
T9R = [lambda x, t: f"Money a shopkeeper lent has grown to {nf(x)} times itself in {nf(t)} years at simple interest. At what rate per cent per annum was it lent?",
       lambda x, t: f"Money kept at simple interest is {nf(x)} times as much after {nf(t)} years. Find the yearly rate."]
T9T = [lambda x, r: f"In how many years will a sum of money become {nf(x)} times itself at {nf(r)}% per annum simple interest?",
       lambda x, r: f"How long will a deposit take to become {nf(x)} times itself at {nf(r)}% per annum simple interest?"]
T10 = [lambda r1, A1, r2, A2: f"A sum lent at {nf(r1)}% per annum simple interest amounts to Rs {nf(A1)} after some years. Lent for the same years at {nf(r2)}% per annum, "
                              f"it would amount to Rs {nf(A2)}. Find the time.",
       lambda r1, A1, r2, A2: f"A man deposits money for a few years. At {nf(r1)}% per annum simple interest it grows to Rs {nf(A1)}, and at {nf(r2)}% per annum it grows to "
                              f"Rs {nf(A2)}. For how many years is it deposited?"]
T11 = [lambda r1, A1, r2, A2: f"Some money lent at {nf(r1)}% per annum simple interest amounts to Rs {nf(A1)}. Lent for the same time at {nf(r2)}% per annum, it amounts to "
                              f"Rs {nf(A2)}. How much money was lent?",
       lambda r1, A1, r2, A2: f"At {nf(r1)}% per annum simple interest a deposit grows to Rs {nf(A1)}, and at {nf(r2)}% per annum it grows to Rs {nf(A2)} in the same time. Find the deposit."]
T12 = [lambda t, x, A: f"A sum was lent at simple interest for {nf(t)} years. Had the rate been {nf(x)}% higher, it would have earned Rs {nf(A)} more. Find the sum.",
       lambda t, x, A: f"A deposit is kept for {nf(t)} years at simple interest. If the rate were {nf(x)}% more, the interest would be Rs {nf(A)} more. What is the deposit?"]
T13 = [lambda A1, t1, A2, t2: f"Money lent at simple interest grows to Rs {nf(A1)} after {nf(t1)} years and to Rs {nf(A2)} after {nf(t2)} years. How much was lent?",
       lambda A1, t1, A2, t2: f"A deposit at simple interest becomes Rs {nf(A1)} in {nf(t1)} years and Rs {nf(A2)} in {nf(t2)} years. Find the deposit."]
T13P = [lambda A1, t1, A2, t2: f"A shop's loan at simple interest comes to Rs {nf(A1)} after {nf(t1)} years and Rs {nf(A2)} after {nf(t2)} years. What were the loan and the yearly rate?",
        lambda A1, t1, A2, t2: f"A farmer's loan at simple interest grows to Rs {nf(A1)} after {nf(t1)} years and to Rs {nf(A2)} after {nf(t2)} years. "
                               f"Find the sum borrowed and the rate per cent per annum."]

ITEMS = [(769, "7", T7[0], 769)] + [(f"r7_e{i}", "7", T7[i % 3], None) for i in range(1, 7)]
ITEMS += [(770, "8", T8[0], 770)] + [(f"r8_e{i}", "8", T8[i % 2], None) for i in range(1, 6)]
ITEMS += [(771, "9r2", lambda t: f"Money lent by a cooperative society doubles itself in {nf(t)} years at simple interest. Find the rate per cent per annum.", 771),
          ("r9_x2", "9r3", lambda t: f"A deposit in a post office trebles itself in {nf(t)} years at simple interest. What is the rate of interest?", None),
          ("r9_x3", "9t", T9T[0], None)]
ITEMS += [(f"r9_e{i}", "9r", T9R[i % 2], None) for i in range(1, 5)]
ITEMS += [("r9_e5", "9t", T9T[1], None),
          ("r9_e6", "9t2", lambda r: f"How many years will a sum take to double itself at {nf(r)}% per annum simple interest?", None),
          ("r9_e7", "9t3", lambda r: f"In what time will money lent at {nf(r)}% per annum simple interest become three times itself?", None)]
ITEMS += [(772, "10", T10[0], 772)] + [(f"r10_e{i}", "10", T10[i % 2], None) for i in range(1, 6)]
ITEMS += [(773, "10", T11[0], 773)] + [(f"r11_e{i}", "10", T11[i % 2], None) for i in range(1, 5)]
ITEMS += [(774, "12", T12[0], 774)] + [(f"r12_e{i}", "12", T12[i % 2], None) for i in range(1, 6)]
ITEMS += [(775, "13", T13P[0], 775)] + [(f"r13_e{i}", "13", T13[i % 2], None) for i in range(1, 5)] + [(f"r13_e{i}", "13", T13P[i % 2], None) for i in range(5, 8)]
SENT = {k: (pool, s) for k, pool, s, _ in ITEMS}
