"""Percentage rewording batch 9 (2026-10-30): the 46 rows of Rules 65-76 that fail the originality gate get all-new numbers
(searched against the book's number sets), a sentence in the book's simple style with the setting changed (sentences in
b9/sent_b9.py), new options, and the explanation the gen_65_72.py / gen_73_77.py builders write for the new numbers.
Independent check: the solve_65_72.py / solve_73_77.py solvers. Writes reword/b9/ruleNN/2_new_rows.json; check:
`python reword_check.py b9`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_65_72 as g  # noqa: E402
import gen_73_77 as h  # noqa: E402
import sent_b9 as s  # noqa: E402
from gen_1_8 import P  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402
from gen_33_40 import PD  # noqa: E402

plain = lambda *v: dict(zip("abcd", v))
_k = [0]


def split_opts(a, b):
    """Two parts: the right pair and three pairs with the same total (never the right pair reversed)."""
    wrong = [(a + 5, b - 5), (a - 5, b + 5), (a + 10, b - 10)]
    pos = rw_common.POS[_k[0] % len(rw_common.POS)]
    _k[0] += 1
    wrong.insert(pos - 1, (a, b))
    return dict(zip("abcd", (g.two(x, y) for x, y in wrong)))


SPLIT = {650: (297, 35, 220, 77), 2003: (235, 25, 188, 47), 2004: (65, 30, 50, 15), 2005: (138, 50, 92, 46), 2006: (245, 25, 196, 49),
         2007: (90, 50, 60, 30)}
MORE = {651: (621, 54), 2008: (120, 20), 2009: (612, 20), 2010: (504, 55), 2011: (429, 22), 2012: (720, 10)}
CAP = {652: (322, 8), 2013: (580, 20), 2014: (730, 27), 2015: (567, 46), 2016: (525, 25), 2017: (276, 8)}
UP3 = {653: (36, 38, 25), 2018: (23, 25, 8), 2019: (36, 9, 25), 2020: (12, 35, 10), 2021: (20, 28, 45)}
DISC3 = {654: (18, 44, 25), 2022: (10, 6, 45), 2023: (25, 12, 44), 2024: (35, 16, 10), 2025: (15, 20, 38)}
HOUSE = {656: (40, 17), 2034: (28, 24), 2035: (18, 26), 2036: (37, 40), 2037: (24, 5)}
INC = {657: (30, 25, 650), 2038: (25, 24, 1150), 2039: (25, 16, 500), 2040: (20, 30, 1800), 2041: (32, 20, 350)}
WT = {658: (3, 7, 37, 16, 58), 2043: (2, 3, 19, 34, 134)}
USE = {660: (40, 5, 16), 2050: (35, 23, 45), 2051: (20, 17, 56), 2052: (30, 14, 26), 2053: (50, 21, 60)}

PLAN = {
    65: [(rid, s.SPLIT[rid](N, p), (lambda N=N, p=p: g.split(N, p)), split_opts(a, b)) for rid, (N, p, a, b) in SPLIT.items()],
    66: [(rid, s.MORE[rid](*c), (lambda c=c: g.tank(*c, "more")), g.L) for rid, c in MORE.items()],
    67: [(rid, s.CAP[rid](*c), (lambda c=c: g.tank(*c, "cap")), g.L) for rid, c in CAP.items()],
    68: [(rid, s.UP3[rid](*c), (lambda c=c: g.three(68, *c)), PD) for rid, c in UP3.items()],
    69: [(rid, s.DISC3[rid](*c), (lambda c=c: g.three(69, *c)), PD) for rid, c in DISC3.items()],
    72: [(rid, s.HOUSE[rid](*c), (lambda c=c: g.houses(*c)), PD) for rid, c in HOUSE.items()],
    73: [(657, s.INC[657][0](*INC[657]), lambda: h.incomes(*INC[657], s.INC[657][1], both=True),
          plain(r"Neha Rs 26000, Rina Rs 19500", r"Neha Rs 19500, Rina Rs 26000", r"Neha Rs 19500, Rina Rs 25350", r"Neha Rs 18000, Rina Rs 24000"))]
        + [(rid, s.INC[rid][0](*c), (lambda c=c, rid=rid: h.incomes(*c, s.INC[rid][1])), Rsx) for rid, c in INC.items() if rid != 657],
    74: [(rid, s.WT[rid](*c), (lambda c=c: h.weights(*c)), P) for rid, c in WT.items()],
    75: [(659, s.SAVE[659](36, 30, 12600), lambda: h.from_savings(36, 30, 12600, "all"),
          plain(r"Income Rs 28125, food Rs 10125, rent Rs 5400", r"Income Rs 25000, food Rs 9000, rent Rs 4800",
                r"Income Rs 28125, food Rs 10125, rent Rs 8437.50", r"Income Rs 31250, food Rs 11250, rent Rs 6000"))],
    76: [(rid, s.USE[rid](*c), (lambda c=c: h.new_use(*c)), h.KG) for rid, c in USE.items()],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
