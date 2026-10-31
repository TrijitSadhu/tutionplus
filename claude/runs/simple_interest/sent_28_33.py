"""Question sentences for Simple Interest Rules 28-33 (simple style, setting changed). ITEMS = (key, number pool, sentence, old row id);
each sentence writes its numbers in the order the solver reads them (pool tuples in gen_28_33 order)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmt import nf  # noqa: E402

T28 = lambda P1, P2, r, A: (f"Two loans of Rs {nf(P1)} and Rs {nf(P2)} are given at {nf(r)}% per annum simple interest for the same time. The smaller loan earns "
                            f"Rs {nf(A)} less interest. For how many years were they given?")
T28B = lambda P1, P2, r, A: (f"A trader lends Rs {nf(P1)} to one customer and Rs {nf(P2)} to another, both at {nf(r)}% per annum simple interest for the same time. "
                             f"The first loan brings Rs {nf(A)} less interest than the second. Find the time.")
T29 = [lambda r1, t1, r2, t2, D: f"Two equal sums are deposited, one at {nf(r1)}% per annum for {nf(t1)} years and the other at {nf(r2)}% per annum for {nf(t2)} years. "
                                 f"The first earns Rs {nf(D)} more interest than the second. Find each sum.",
       lambda r1, t1, r2, t2, D: f"A father puts the same amount in two schemes: one gives {nf(r1)}% per annum simple interest for {nf(t1)} years, the other {nf(r2)}% "
                                 f"per annum for {nf(t2)} years. The first scheme pays Rs {nf(D)} more interest. How much did he put in each?"]
T29M = lambda m1, r1, m2, r2, D: (f"The simple interest on a loan for {nf(m1)} months at {nf(r1)}% per annum is Rs {nf(D)} more than the interest on the same loan for "
                                  f"{nf(m2)} months at {nf(r2)}% per annum. How much was borrowed?")
T29S = lambda t1, t2, r, D: (f"The simple interests on a deposit for {nf(t1)} years and for {nf(t2)} years at {nf(r)}% per annum differ by Rs {nf(D)}. "
                             f"Find the deposit.")
T30 = [lambda X, t, D: f"A man compares two banks for a deposit of Rs {nf(X)}. Over {nf(t)} years one bank would give him Rs {nf(D)} more interest than the other. "
                       f"By how much do their yearly rates differ?",
       lambda X, t, D: f"On a loan of Rs {nf(X)} for {nf(t)} years, two moneylenders ask for simple interests that differ by Rs {nf(D)}. Find the difference "
                       f"between their rates per cent per annum."]
T31 = [lambda A1, t1, A2, t2: f"A deposit at simple interest grows to Rs {nf(A1)} after {nf(t1)} years and to Rs {nf(A2)} after {nf(t2)} years. Find the yearly rate of interest.",
       lambda A1, t1, A2, t2: f"A shopkeeper's loan at simple interest comes to Rs {nf(A1)} in {nf(t1)} years and Rs {nf(A2)} in {nf(t2)} years. At what rate per cent "
                              f"per annum was it taken?"]
T31M = lambda A1, t1, A2, dt: (f"Money lent at simple interest grows to Rs {nf(A1)} in {nf(t1)} years, and to Rs {nf(A2)} after {nf(dt)} more years. Find the rate "
                               f"per cent per annum.")
T32 = [lambda X, t1, x1, t2, x2: f"A shopkeeper borrows Rs {nf(X)} from a bank at simple interest. After {nf(t1)} years he pays back Rs {nf(x1)}, and at the end of "
                                 f"{nf(t2)} years from the day he borrowed he pays Rs {nf(x2)} to close the loan. Find the rate of interest.",
       lambda X, t1, x1, t2, x2: f"A farmer takes a loan of Rs {nf(X)} at simple interest. At the end of {nf(t1)} years he repays Rs {nf(x1)}, and {nf(t2)} years after "
                                 f"taking the loan he pays Rs {nf(x2)} more to clear it. What is the rate of interest?"]
T33 = [lambda P, r1, r2, t, A: f"A man lends part of Rs {nf(P)} at {nf(r1)}% per annum and the rest at {nf(r2)}% per annum. The total simple interest from both "
                               f"parts in {nf(t)} years is Rs {nf(A)}. How much did he lend at {nf(r1)}%?",
       lambda P, r1, r2, t, A: f"Out of Rs {nf(P)}, a trust deposits some money at {nf(r1)}% per annum and the rest at {nf(r2)}% per annum simple interest. In "
                               f"{nf(t)} years the two parts earn Rs {nf(A)} in all. Find the part deposited at {nf(r1)}%."]

ITEMS = [(790, "28", T28, 790)] + [(f"r28_e{i}", "28" if i % 2 else "28b", T28 if i % 2 else T28B, None) for i in range(1, 6)]
ITEMS += [(791, "29", T29[0], 791), ("r29_e1", "29", T29[1], None), ("r29_e2", "29m", T29M, None), ("r29_e3", "29s", T29S, None),
          ("r29_e4", "29", T29[0], None), ("r29_e5", "29", T29[1], None), ("r29_e6", "29s", T29S, None)]
ITEMS += [(792, "30", T30[0], 792)] + [(f"r30_e{i}", "30", T30[i % 2], None) for i in range(1, 6)]
ITEMS += [(793, "31", T31[0], 793), ("r31_e1", "31", T31[1], None), ("r31_e2", "31m", T31M, None)] + [(f"r31_e{i}", "31", T31[i % 2], None) for i in range(3, 8)]
ITEMS += [(794, "32", T32[0], 794)] + [(f"r32_e{i}", "32", T32[i % 2], None) for i in range(1, 5)]
ITEMS += [(795, "33", T33[0], 795)] + [(f"r33_e{i}", "33", T33[i % 2], None) for i in range(1, 4)]
SENT = {k: (pool, s) for k, pool, s, _ in ITEMS}
NVIS = {"28": 4, "28b": 4, "29": 5, "29m": 5, "29s": 4, "30": 3, "31": 4, "31m": 4, "32": 5, "33": 5}
