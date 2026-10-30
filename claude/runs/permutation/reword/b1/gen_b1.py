"""P&C rewording batch 1 (2026-10-30): the 23 rows of Rules 2, 3, 13, 16, 26 and 27 that fail the originality gate get all-new
numbers, a sentence in the book's simple style with the setting changed, new options, and the explanation the gen_*.py
builders write for the new numbers. The digit questions use digit sets without the old question's digits above 3 (the gate
rejects any kept number > 3), so their Rule 2 case tables are written here. Independent check: b1/solve_b1.py (brute-force
counts keyed by row id). Writes reword/b1/ruleNN/2_new_rows.json; check: `python reword_check.py b1`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_1_7 as g1  # noqa: E402
import gen_8_13 as g8  # noqa: E402
import gen_14_21 as g14  # noqa: E402
import gen_22_29 as g22  # noqa: E402
import gen_30_36 as g30  # noqa: E402
from pc_common import I  # noqa: E402

plain = lambda *v: dict(zip("abcd", v))
H3 = ["Hundreds", "Tens", "Units"]
H4 = ["Thousands", "Hundreds", "Tens", "Units"]

PLAN = {
    2: [(846, r"How many numbers of three digits can be made from the digits 2, 3, 6, 7, 8 and 9 if no digit is used twice?",
         lambda: g1.r2_result([("Fill the three places.", 1, 6, 3, H3, ["6 ways", "5 ways", "4 ways"])]), I),
        (2060, r"Using the digits 1, 2, 3 and 5, each at most once, how many numbers greater than 200 and less than 2000 can be written?",
         lambda: g1.r2_result([("Case I: 3-digit numbers (hundreds digit 2, 3 or 5).", 3, 3, 2, H3, ["2, 3 or 5: 3 ways", "3 ways", "2 ways"]), ("Case II: 4-digit numbers (thousands digit 1).", 1, 3, 3, H4, ["1: 1 way", "3 ways", "2 ways", "1 way"])]), I),
        (2061, r"With the digits 1, 2, 3, 7 and 8, no digit used twice in a number, how many numbers greater than 300 and less than 3000 can be made?",
         lambda: g1.r2_result([("Case I: 3-digit numbers (hundreds digit 3, 7 or 8).", 3, 4, 2, H3, ["3, 7 or 8: 3 ways", "4 ways", "3 ways"]), ("Case II: 4-digit numbers (thousands digit 1 or 2).", 2, 4, 3, H4, ["1 or 2: 2 ways", "4 ways", "3 ways", "2 ways"])]), I),
        (2062, r"Using the digits 1, 2, 3, 7 and 8, each at most once, how many even three-digit numbers can be written?",
         lambda: g1.r2_result([("Units digit 2 or 8.", 2, 4, 2, H3, ["4 ways", "3 ways", "2 or 8: 2 ways"])]), I),
        (2063, r"Each of the digits 1, 2, 3, 7, 8 and 9 may be used once at most. How many three-digit numbers greater than 700 can be written?",
         lambda: g1.r2_result([("Hundreds digit 7, 8 or 9.", 3, 5, 2, H3, ["7, 8 or 9: 3 ways", "5 ways", "4 ways"])]), I),
        (2064, r"A child writes positive numbers using one or more of the digits 1, 2, 3 and 7, never using a digit twice in a number. How many such numbers are there?",
         lambda: g1.r2_result([(f"{k}-digit numbers.", 1, 4, k, [f"Place {i}" for i in range(1, k + 1)], [f"{4 - i} ways" for i in range(k)]) for k in range(1, 5)]), I)],
    3: [(847, r"A boy has 7 letters to post and there are 2 post boxes near his house. In how many ways can he post the letters?",
         lambda: g1.r3(2, 7, "letters", "post boxes"), I),
        (2065, r"Three prizes are to be given among 5 girls, and a girl may win more than one prize. In how many ways can the prizes be given?",
         lambda: g1.r3(5, 3, "prizes", "girls"), I),
        (2068, r"How many numbers of four digits can be written with the digits 1, 2, 3, 6 and 7 if a digit may be used more than once?",
         lambda: g1.r3(5, 4, "places of the number", "digits"), I)],
    13: [(2107, r"A shelf is to hold 12 books: 2 single books and three sets of 5, 3 and 2 volumes. In how many ways can the books be arranged so "
                r"that the volumes of each set stay together?",
          lambda: g8.r13_groups([("the 5-volume set", 5), ("the 3-volume set", 3), ("the 2-volume set", 2)], singles=2, what="volumes"),
          plain(r"\(5!\times 3!\times 2!\)", r"\(5!\times 5!\times 3!\times 2!\)", r"\(2!\times 5!\times 3!\times 2!\)", r"\(12!\)"))],
    16: [(856, r"How many triangles can be drawn by joining the corners of a polygon of 10 sides?", lambda: g14.r16(10), I)],
    26: [(866, r"From 3 teachers and 9 students, in how many ways can a group of 5 be picked with exactly one teacher in it?",
          lambda: g22.r26(3, 9, 5, 1, "teachers", "students"), I),
         (2152, r"A team of 4 is to be chosen from 9 boys and 3 girls. In how many ways can it be done if the team must have exactly 2 boys?",
         lambda: g22.r26(9, 3, 4, 2, "boys", "girls"), I),
         (2153, r"From 6 men and 7 women, in how many ways can 3 people be picked so that exactly one of them is a man?",
          lambda: g22.r26(6, 7, 3, 1, "men", "women"), I),
         (2154, r"A club has 11 players and 5 coaches. In how many ways can a group of 4 be formed with exactly 2 players?",
         lambda: g22.r26(11, 5, 4, 2, "players", "coaches"), I),
         (2190, r"A group of 4 is to be picked from 4 doctors and 8 nurses. In how many ways can it be done if it must have at least one doctor?",
          lambda: g30.at_least(4, 8, 4, 1, "doctors", "nurses"), I),
         (2191, r"From 2 girls and 9 boys a team of 3 is to be formed. In how many ways can it be done so that the team has at least one girl?",
          lambda: g30.at_least(2, 9, 3, 1, "girls", "boys"), I),
         (2192, r"A committee of 5 is to be made from 6 men and 5 women. In how many ways can it be done so that it has at least 2 men?",
          lambda: g30.at_least(6, 5, 5, 2, "men", "women"), I)],
    27: [(867, r"A basket has 3 guavas, 8 bananas and 2 pears, the fruits of each kind being alike. In how many ways can a person pick some "
               r"fruit from the basket?", lambda: g22.r27(3, 8, 2, names=("guavas", "bananas", "pears")), I),
         (2156, r"A box holds 9 red, 11 blue and 5 green marbles, the marbles of one colour being alike. In how many ways can a child take some of the marbles?",
         lambda: g22.r27(9, 11, 5, names=("red marbles", "blue marbles", "green marbles")), I)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
