"""Question sentences for Simple Interest Rules 14-20 (simple style, setting changed). ITEMS = (key, number pool, sentence, old row id);
each sentence writes its numbers in the order the solver reads them (pool tuples in gen_14_20 order)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmt import nf  # noqa: E402

T14 = [lambda t, x, A: f"A sum was lent at simple interest for {nf(t)} years. Had the rate been {nf(x)}% lower, it would have earned Rs {nf(A)} less. Find the sum.",
       lambda t, x, A: f"A deposit is kept for {nf(t)} years at simple interest. If the rate were {nf(x)}% less, the interest would be Rs {nf(A)} less. What is the deposit?"]
T15_PAIR = lambda X, r1, r2, I: (f"A trader divides Rs {nf(X)} into two parts. He lends one part at {nf(r1)}% per annum and the other at {nf(r2)}% per annum, and gets Rs {nf(I)} "
                                 f"as interest in one year. How much does he lend at {nf(r1)}% and how much at {nf(r2)}%?")
T15_BANK = lambda X, r1, r2, I, ask: (f"Meena puts Rs {nf(X)} in two banks, one paying {nf(r1)}% per annum and the other {nf(r2)}% per annum. In one year she earns Rs {nf(I)} "
                                      f"as interest in all. How much did she put in the bank paying {nf(ask)}%?")
T15_MAN = lambda X, r1, r2, I, ask: (f"A man has Rs {nf(X)}. He lends part of it at {nf(r1)}% per annum simple interest and the rest at {nf(r2)}% per annum. His yearly interest "
                                     f"is Rs {nf(I)}. How much did he lend at {nf(ask)}%?")
T15_MORE = lambda X1, r1, r2, t, I: (f"A farmer borrowed Rs {nf(X1)} at {nf(r1)}% per annum and some more money at {nf(r2)}% per annum, both for {nf(t)} years. He paid Rs {nf(I)} "
                                     f"as interest in all. How much did he borrow altogether?")
T15_TWO = lambda X, r1, r2, t, I: (f"A milkman borrowed Rs {nf(X)} in all from two lenders, at {nf(r1)}% and {nf(r2)}% per annum. The interest on both loans for {nf(t)} years "
                                   f"came to Rs {nf(I)}. How much did he borrow at {nf(r1)}%, and how much at {nf(r2)}%?")
T16 = [lambda X, A, t1, r, t2: f"A deposit of Rs {nf(X)} grows to Rs {nf(A)} in {nf(t1)} years at simple interest. If the bank lowers the rate by {nf(r)}% per annum, "
                               f"what will the same deposit grow to in {nf(t2)} years?",
       lambda X, A, t1, r, t2: f"A loan of Rs {nf(X)} at simple interest comes to Rs {nf(A)} after {nf(t1)} years. Had the rate been {nf(r)}% lower, how much would it "
                               f"come to after {nf(t2)} years?"]
T17 = [lambda X, A, t1, r, t2: f"A deposit of Rs {nf(X)} grows to Rs {nf(A)} in {nf(t1)} years at simple interest. If the bank raises the rate by {nf(r)}% per annum, "
                               f"what will the same deposit grow to in {nf(t2)} years?",
       lambda X, A, t1, r, t2: f"A loan of Rs {nf(X)} at simple interest comes to Rs {nf(A)} after {nf(t1)} years. Had the rate been {nf(r)}% higher, how much would it "
                               f"come to after {nf(t2)} years?"]
T18 = [lambda x, t, n: f"A loan earns Rs {nf(x)} as simple interest in {nf(t)} years. For the next {nf(t)} years the principal is made {nf(n)} times as large. "
                       f"What is the total interest at the end of {nf(2 * t)} years?",
       lambda x, t, n: f"The simple interest on a deposit is Rs {nf(x)} after {nf(t)} years. The deposit is then made {nf(n)} times as big for the next {nf(t)} years. "
                       f"Find the total interest earned in {nf(2 * t)} years."]
T19 = [lambda x, t1, t2, n: f"A loan earns Rs {nf(x)} as simple interest in {nf(t1)} years. For the next {nf(t2)} years the principal is {nf(n)} times as large. "
                            f"What is the total interest at the end of {nf(t1 + t2)} years?",
       lambda x, t1, t2, n: f"The simple interest on a deposit is Rs {nf(x)} after {nf(t1)} years. For the next {nf(t2)} years the deposit is {nf(n)} times as big. "
                            f"Find the total interest earned in {nf(t1 + t2)} years."]
T20 = [lambda X, r1, t1, r2, t2: f"A farmer lends Rs {nf(X)} to two neighbours. The interest from the first at {nf(r1)}% per annum for {nf(t1)} years equals the interest "
                                 f"from the second at {nf(r2)}% per annum for {nf(t2)} years. How much does each neighbour get?",
       lambda X, r1, t1, r2, t2: f"Rs {nf(X)} is split into two loans so that the interest on the first at {nf(r1)}% for {nf(t1)} years is the same as the interest on the "
                                 f"second at {nf(r2)}% for {nf(t2)} years. Find the two loans."]
T20_DIFF = lambda X, r1, t1, r2, t2: (f"Rs {nf(X)} is split into two loans so that the interest on the first at {nf(r1)}% for {nf(t1)} years is the same as the interest "
                                      f"on the second at {nf(r2)}% for {nf(t2)} years. Find the difference between the two loans.")
T20_THREE = lambda X, r1, t1, r2, t2, r3, t3: (f"Rs {nf(X)} is split into three loans so that the interest on the first at {nf(r1)}% for {nf(t1)} years, on the second at "
                                               f"{nf(r2)}% for {nf(t2)} years and on the third at {nf(r3)}% for {nf(t3)} years are all equal. What is the difference "
                                               f"between the largest and the smallest loan?")

ITEMS = [(776, "14", T14[0], 776)] + [(f"r14_e{i}", "14", T14[i % 2], None) for i in range(1, 6)]
ITEMS += [(777, "15", T15_PAIR, 777), ("r15_e1", "15u", T15_MORE, None),
          ("r15_e2", "15b2", lambda X, r1, r2, I: T15_BANK(X, r1, r2, I, r2), None), ("r15_e3", "15m1", lambda X, r1, r2, I: T15_MAN(X, r1, r2, I, r1), None),
          ("r15_e4", "15m2", lambda X, r1, r2, I: T15_MAN(X, r1, r2, I, r2), None), ("r15_e5", "15b1", lambda X, r1, r2, I: T15_BANK(X, r1, r2, I, r1), None),
          ("r15_e6", "15t", T15_TWO, None)]
ITEMS += [(778, "16", T16[0], 778)] + [(f"r16_e{i}", "16", T16[i % 2], None) for i in range(1, 6)]
ITEMS += [(779, "17", T17[0], 779)] + [(f"r17_e{i}", "17", T17[i % 2], None) for i in range(1, 8)]
ITEMS += [(780, "18", T18[0], 780)] + [(f"r18_e{i}", "18", T18[i % 2], None) for i in range(1, 5)]
ITEMS += [(781, "19", T19[0], 781)] + [(f"r19_e{i}", "19", T19[i % 2], None) for i in range(1, 6)]
ITEMS += [(782, "20", T20[0], 782), ("r20_e1", "20t", T20_THREE, None)] + [(f"r20_e{i}", "20", T20[i % 2], None) for i in range(2, 5)] + \
         [("r20_e5", "20d", T20_DIFF, None)]
SENT = {k: (pool, s) for k, pool, s, _ in ITEMS}
NVIS = {"14": 3, "15": 4, "15b1": 4, "15b2": 4, "15m1": 4, "15m2": 4, "15u": 5, "15t": 5, "16": 5, "17": 5, "18": 3, "19": 4, "20": 5, "20d": 5, "20t": 7}
