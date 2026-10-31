"""Question sentences for Simple Interest Rules 21-27 (simple style, setting changed). ITEMS = (key, number pool, sentence, old row id);
each sentence writes its numbers in the order the solver reads them (pool tuples in gen_21_27 order)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmt import nf  # noqa: E402

T21 = [lambda n, r, m: f"A sum of money becomes {nf(n)} times itself at {nf(r)}% per annum simple interest. At what rate per cent would it become {nf(m)} times "
                       f"itself in the same time?",
       lambda n, r, m: f"Money lent at simple interest grows to {nf(n)} times itself at {nf(r)}% per annum. What rate would make it {nf(m)} times itself in the same "
                       f"number of years?"]
T22 = [lambda A1, r1, P, A2, r2: f"A sum grew to Rs {nf(A1)} at {nf(r1)}% simple interest in the same time that Rs {nf(P)} grew to Rs {nf(A2)} at {nf(r2)}%. Find the sum.",
       lambda A1, r1, P, A2, r2: f"A deposit became Rs {nf(A1)} at {nf(r1)}% per annum simple interest, in the time it took Rs {nf(P)} to become Rs {nf(A2)} at "
                                 f"{nf(r2)}% per annum. What was the deposit?"]
T23 = [lambda A1, t, r, A2: f"A loan at simple interest comes to Rs {nf(A1)} in {nf(t)} years at {nf(r)}% per annum. In how many years will it come to Rs {nf(A2)} at "
                            f"the same rate?",
       lambda A1, t, r, A2: f"A deposit grows to Rs {nf(A1)} in {nf(t)} years at {nf(r)}% per annum simple interest. After how many years will it be Rs {nf(A2)}?"]
T24_RATIO = lambda X, t1, t2, t3, r: (f"A man puts Rs {nf(X)} in the names of his three daughters so that each gets the same amount after {nf(t1)}, {nf(t2)} and "
                                      f"{nf(t3)} years respectively at {nf(r)}% simple interest. In what ratio is the money divided?")
T24_DIFF = lambda X, t1, t2, t3, r: (f"Rs {nf(X)} is divided into three parts whose amounts after {nf(t1)}, {nf(t2)} and {nf(t3)} years at {nf(r)}% per annum simple "
                                     f"interest are equal. Find the difference between the largest and the smallest part.")
T24_PARTS = lambda X, t1, t2, t3, r: (f"Rs {nf(X)} is split into three parts so that, after {nf(t1)}, {nf(t2)} and {nf(t3)} years, they amount to the same sum at "
                                      f"{nf(r)}% per annum simple interest. Find the three parts.")
T24_RATES = lambda X, r1, t1, r2, t2, r3, t3: (f"Rs {nf(X)} is split into three parts. The first is lent at {nf(r1)}% for {nf(t1)} years, the second at {nf(r2)}% for "
                                               f"{nf(t2)} years and the third at {nf(r3)}% for {nf(t3)} years, and all three amounts come out equal. Find the three parts.")
T24_SONS = lambda X, a1, a2, M, r: (f"A father leaves Rs {nf(X)} to his two sons, aged {nf(a1)} and {nf(a2)} years, so that each receives the same amount when he "
                                    f"turns {nf(M)}, at {nf(r)}% per annum simple interest. How much is set aside for each son now?")
T25 = [lambda A, t, r: f"What sum will grow to Rs {nf(A)} in {nf(t)} years at {nf(r)}% per annum simple interest?",
       lambda A, t, r: f"A farmer must repay Rs {nf(A)} after {nf(t)} years on a loan at {nf(r)}% per annum simple interest. How much did he borrow?"]
T26 = [lambda r, t, A: f"A shopkeeper gives a loan at {nf(r)}% per annum simple interest. The interest he earns in {nf(t)} years is Rs {nf(A)} short of the loan itself. "
                       f"How big is the loan?",
       lambda r, t, A: f"A deposit earns {nf(r)}% per annum simple interest. In {nf(t)} years its interest falls short of the deposit by Rs {nf(A)}. What is the deposit?"]
T27 = [lambda n, t, m: f"A cooperative bank deposit is {nf(n)} times as large after {nf(t)} years of simple interest. After how many years will it be {nf(m)} times as large?",
       lambda n, t, m: f"Money lent at simple interest grows to {nf(n)} times itself in {nf(t)} years. How long will it take to grow to {nf(m)} times itself?"]
T27D = lambda t, m: f"A deposit doubles itself in {nf(t)} years at simple interest. After how many years will it be {nf(m)} times itself?"

ITEMS = [(783, "21", T21[0], 783)] + [(f"r21_e{i}", "21", T21[i % 2], None) for i in range(1, 6)]
ITEMS += [(784, "22", T22[0], 784)] + [(f"r22_e{i}", "22", T22[i % 2], None) for i in range(1, 6)]
ITEMS += [(785, "23", T23[0], 785)] + [(f"r23_e{i}", "23", T23[i % 2], None) for i in range(1, 6)]
ITEMS += [(786, "24r", T24_RATIO, 786), ("r24_e1", "24d", T24_DIFF, None), ("r24_e2", "24p", T24_PARTS, None), ("r24_e3", "24v", T24_RATES, None),
          ("r24_e4", "24p", T24_PARTS, None), ("r24_e5", "24s", T24_SONS, None)]
ITEMS += [(787, "25", T25[0], 787)] + [(f"r25_e{i}", "25", T25[i % 2], None) for i in range(1, 6)]
ITEMS += [(788, "26", T26[0], 788)] + [(f"r26_e{i}", "26", T26[i % 2], None) for i in range(1, 6)]
ITEMS += [(789, "27d", T27D, 789)] + [(f"r27_e{i}", "27", T27[i % 2], None) for i in range(1, 5)] + [("r27_e5", "27d", T27D, None), ("r27_e6", "27d", T27D, None)]
SENT = {k: (pool, s) for k, pool, s, _ in ITEMS}
NVIS = {"21": 3, "22": 5, "23": 4, "24r": 5, "24d": 5, "24p": 5, "24v": 7, "24s": 5, "25": 3, "26": 3, "27": 3, "27d": 2}
