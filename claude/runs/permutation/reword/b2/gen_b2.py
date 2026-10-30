"""P&C rewording batch 2 (2026-10-30): the 22 rows of Rules 30 and 32-36 that fail the originality gate get a new n, a
sentence in the book's simple style with the setting changed (a swimming test, a chess club, a football team ...), new
options, and the explanation the gen_30_36.py builders write for the new n. Independent check: the solve_30_36.py solvers
(n = the first number in the question, or "polygon of N sides"; "(ii)" marks a two-part answer).
Writes reword/b2/ruleNN/2_new_rows.json; check: `python reword_check.py b2`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_30_36 as g  # noqa: E402
from pc_common import I  # noqa: E402

plain = lambda *v: dict(zip("abcd", v))
pr = lambda a, b: rf"\({a}\), \({b}\)"

PLAN = {
    30: [(870, r"How many four-sided figures can be drawn by joining the corners of a polygon of 7 sides?", lambda: g.r30(7), I),
         (2166, r"The corners of a polygon of 6 sides are joined in fours. How many quadrilaterals can be made this way?", lambda: g.r30(6), I),
         (2168, r"A garden has a fence shaped like a polygon of 10 sides. How many quadrilaterals can be marked out using its corners as corners?",
          lambda: g.r30(10), I),
         (2169, r"How many quadrilaterals have all four corners among the corners of a polygon of 12 sides?", lambda: g.r30(12), I)],
    32: [(871, r"There are 14 points on a sheet of paper, no three of them on one straight line. How many triangles can be drawn with corners "
               r"at these points?", lambda: g.r32(14), I),
         (2174, r"A child marks 7 dots on a board so that no three lie on a line. How many triangles can be formed by joining the dots?",
          lambda: g.r32(7), I),
         (2175, r"15 pegs stand on a board, and no three of them are in a straight line. How many triangles can be made with three of the "
                r"pegs as corners?", lambda: g.r32(15), I),
         (2176, r"Take 13 points in a plane with no three of them in a line. How many triangles have their corners at these points?",
          lambda: g.r32(13), I)],
    33: [(872, r"5 girls take a swimming test, and each of them either passes or fails. In how many ways can the results come out?",
          lambda: g.r33(5), I),
         (2177, r"4 boys sit a driving test in which each one passes or fails. In how many different ways can the results be given?",
          lambda: g.r33(4), I),
         (2178, r"7 candidates appear for a typing test, and each passes or fails. In how many ways can the list of results be made?",
          lambda: g.r33(7), I),
         (2179, r"9 pupils take a music test, each one passing or failing. In how many ways can the results be announced?",
          lambda: g.r33(9), I)],
    34: [(873, r"In a chess club 4 games are played, and each game can be won, lost or drawn. In how many ways can the results of the games "
               r"turn out?", lambda: g.r34(4), I),
         (2180, r"5 football matches are to be played, and each can end in a win, a loss or a draw. In how many ways can the results be "
                r"decided?", lambda: g.r34(5), I),
         (2181, r"A team plays 9 hockey matches; each match ends in a win, a loss or a draw. How many different sets of results are possible?",
          lambda: g.r34(9), I),
         (2182, r"10 games of chess are played in a contest, each one won, lost or drawn. In how many ways can the results come out?",
          lambda: g.r34(10), I)],
    35: [(2183, r"A table tennis contest has 7 matches, each won or lost. (i) In how many ways can the results be forecast? (ii) How many of "
                r"these forecasts have every result right?", lambda: g.r35(7, "pair"),
          plain(pr(128, 7), pr(64, 1), pr(128, 1), pr(256, 1))),
         (2184, r"A tennis event has 4 matches, and each match is won or lost. In how many ways can a fan forecast the results?",
          lambda: g.r35(4), I),
         (2185, r"In a badminton league 10 matches will be played, each won or lost. How many different forecasts of the results can be made?",
          lambda: g.r35(10), I),
         (2186, r"There are 5 boxing bouts on a card, each won or lost. In how many ways can someone forecast all the results?",
          lambda: g.r35(5), I)],
    36: [(2187, r"A football team will play 4 matches; each can be a win, a loss or a draw. (i) How many forecasts get every result right? "
                r"(ii) How many forecasts get every result wrong?", lambda: g.r36(4, "pair"),
          plain(pr(1, 81), pr(4, 16), pr(1, 8), pr(1, 16))),
         (2188, r"A cricket side has 8 matches to play, each a win, a loss or a draw. How many different forecasts will have all the "
                r"results correct?", lambda: g.r36(8, "correct"), I),
         (2189, r"A hockey team is to play 9 matches, each ending in a win, a loss or a draw. (i) How many forecasts will have all results "
                r"correct? (ii) How many will have all results wrong?", lambda: g.r36(9, "pair"),
          plain(pr(1, 512), pr(1, 19683), pr(9, 512), pr(1, 511)))],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
