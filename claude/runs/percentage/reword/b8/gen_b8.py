"""Percentage rewording batch 8 (2026-10-30): the 28 rows of Rules 57-64 that fail the originality gate get all-new numbers
(searched against the book's number sets), a sentence in the book's simple style with the setting changed (sentences in
b8/sent_b8.py), new options, and the explanation the gen_57_64.py builders write for the new numbers. Independent check:
the solve_57_64.py solvers. Writes reword/b8/ruleNN/2_new_rows.json; check: `python reword_check.py b8`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_57_64 as g  # noqa: E402
import sent_b8 as s  # noqa: E402
from gen_1_8 import P  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402

plain = lambda *v: dict(zip("abcd", v))
MAKER = {642: (40, 40, 30, 637), 1972: (40, 5, 15, 3381), 1973: (40, 5, 40, 1029), 1974: (10, 15, 10, 2783)}
ADD = {643: (14, 42, 24), 1975: (24, 28, 14), 1976: (13, 32, 13), 1977: (11, 24, 16), 1978: (38, 25, 10), 1979: (28, 32, 14)}
OUT = {644: (35, 14, 49), 1980: (28, 35, 40), 1981: (5, 22, 44), 1982: (11, 20, 40), 1983: (20, 36, 45)}
MIX = {645: (13, 38, 19), 1984: (34, 24, 17), 1985: (22, 47, 11), 1986: (20, 29, 8)}
SCHOOL = {1987: (42, 44, 50), 1988: (43, 29, 62), 1989: (78, 56, 61)}
CUT = {648: (1, 2, 144), 1997: (6, 3, 416), 1998: (15, 6, 280)}

PLAN = {
    57: [(rid, s.MAKER[rid](*c), (lambda c=c: g.maker(*c)), Rsx) for rid, c in MAKER.items()],
    58: [(rid, s.ADD[rid](*c), (lambda c=c: g.water(*c)), g.L) for rid, c in ADD.items()],
    59: [(rid, s.OUT[rid](*c), (lambda c=c: g.water(*c)), g.L) for rid, c in OUT.items()],
    60: [(rid, s.MIX[rid][0](*c), (lambda c=c, rid=rid: g.add_other(*c, s.MIX[rid][1], s.MIX[rid][2])), g.KG) for rid, c in MIX.items()],
    61: [(rid, s.SCHOOL[rid][0](*c), (lambda c=c, rid=rid: g.schools(*c, s.SCHOOL[rid][1], s.SCHOOL[rid][2])), P) for rid, c in SCHOOL.items()],
    63: [(rid, s.CUT[rid][0](*c), (lambda c=c: g.cut_by_rupees(*c)), g.per_kg) for rid, c in CUT.items()],
    64: [(649, s.PCUT[649](10, 2, 360), lambda: g.cut_by_percent(10, 2, 360, "orig", "kg", "coffee"), g.per_kg),
         (1999, s.PCUT[1999](25, 4), lambda: g.cut_by_percent(25, 4, 1, "both", "orange", "oranges"),
          plain(r"Re \(\frac{1}{12}\), Re \(\frac{1}{16}\)", r"Re \(\frac{1}{20}\), Re \(\frac{1}{16}\)", r"Re \(\frac{1}{16}\), Re \(\frac{1}{12}\)",
                r"Re \(\frac{1}{16}\), Re \(\frac{1}{8}\)")),
         (2000, s.PCUT[2000](20, 4, 240), lambda: g.cut_by_percent(20, 4, 240, "both", "kg", "wheat"),
          plain(r"Rs \(15\), Rs \(12\)", r"Rs \(12\), Rs \(16\)", r"Rs \(10\), Rs \(12\)", r"Rs \(12\), Rs \(15\)"))],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
