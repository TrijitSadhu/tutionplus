"""Sentences for the 5 Simple Interest Miscellaneous problems (simple style, all-new numbers). ITEMS = (key, rule card, pool, sentence);
each sentence writes its numbers in the order solve_misc reads them."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fmt import nf  # noqa: E402

M1 = lambda r1, r2, d: (f"When a bank raises its rate from {nf(r1)}% to {nf(r2)}% per annum, a trader's yearly simple interest goes up by Rs {nf(d)}. "
                        f"How much money does he keep in the bank?")
M2 = lambda P1, A1, t1, P2, t2: (f"Rs {nf(P1)} grows to Rs {nf(A1)} in {nf(t1)} years at simple interest. What will Rs {nf(P2)} grow to in {nf(t2)} years at "
                                 f"the same rate?")
M3 = lambda X1, X2, t, I: (f"A man lends Rs {nf(X1)} at one rate and Rs {nf(X2)} at a rate 1% higher. His total simple interest for {nf(t)} years is Rs {nf(I)}. "
                           f"Find the two rates.")
M4 = lambda I, T, n, t: (f"The simple interest on a loan would be Rs {nf(I)} after {nf(T)} years. If the principal becomes {nf(n)} times after {nf(t)} years, "
                         f"what will the total interest be at the end of {nf(T)} years?")
M5 = lambda P, z: (f"At the same rate and for the same time, Rs {nf(P)} earns some simple interest, and that interest, lent out in its turn, earns Rs {nf(z)}. "
                   f"How much was the first interest?")
ITEMS = [("m01", 6, "m1", M1), ("m02", 1, "m2", M2), ("m03", 3, "m3", M3), ("m04", 18, "m4", M4), ("m05", 1, "m5", M5)]
NVIS = {"m1": 3, "m2": 5, "m3": 4, "m4": 4, "m5": 2}
SENT = {k: (rule, pool, s) for k, rule, pool, s in ITEMS}
