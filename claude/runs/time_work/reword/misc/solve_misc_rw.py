"""Independent solvers for the reworded Miscellaneous rows: the book solvers of ../../solve_misc.py (keyed by row id), with
1682 read as "m4" (it was added as M4) and 274 reading its two fractions from the question instead of the book's fixed 1/2 and
3/4 ("A does p as much work as B in q of the time": A's daily work = p/q of B's; together T days; B alone)."""
from fractions import Fraction as F
from solve_misc import solve as book_solve
from validate import numbers


def solve(rid, q):
    try:
        if rid == 274:
            p, qq, T = numbers(q)[:3]
            return ("number", T * (1 + p / qq))           # B's rate b: (b + (p/q) b) T = 1
        return book_solve("m4" if rid == 1682 else rid, q)
    except (ValueError, IndexError, TypeError, ZeroDivisionError, StopIteration):
        return ("unsolved", q[:40])
