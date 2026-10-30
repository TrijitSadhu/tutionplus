"""Percentage rewording batch 1 (2026-10-30): the 25 rows of Rules 2-8 that fail the originality gate get all-new numbers, a
sentence in the book's simple style with the setting changed, new options, and the explanation the gen_1_8.py builders write
for the new numbers. Row ids, rule links, days and times stay. Independent check: the solve_1_8.py solvers (each rule folder's
solve.py), so every sentence keeps the phrases they read ("leakage", "spending", "find the number", "original and the new",
"N parts", plain "8 quintals" / "7 kg 360 g"). Writes reword/b1/ruleNN/2_new_rows.json; check: `python reword_check.py b1`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_1_8 as g  # noqa: E402
from gen_1_8 import P, Fr, Num, Rs  # noqa: E402

plain = lambda *v: dict(zip("abcd", v))

PLAN = {
    2: [(1691, r"What fraction is equal to \(22\frac{1}{2}\%\)?", lambda: g.r2(F(45, 2)),
         plain(Fr(F(9, 20)), Fr(F(9, 40)), Fr(F(11, 40)), Fr(F(1, 4))))],
    3: [(585, r"A shopkeeper gives \(7\%\) of Rs \(900\) to charity. How much does he give?", lambda: g.r3(7, 900, Rs, "the amount"), Rs),
        (586, r"A tank holding \(350\) litres of oil loses \(6\%\) by leakage. How many litres are left in the tank?",
         lambda: g.r3_left(6, 350, "litres"), lambda v: rf"\({tex(v)}\) litres"),
        (1695, r"A man saves \(9\%\) of Rs \(3600\). How much does he save?", lambda: g.r3(9, 3600, Rs, "the amount"), Rs),
        (1701, r"A farmer sells \(45\%\) of his 8 quintals of rice. How much rice does he sell?",
         lambda: g.r3_units(45, 800, "quintal", "kg", 100, r"8\text{ quintals}"),
         plain(r"\(3\) quintals \(60\) kg", r"\(3\) quintals \(6\) kg", r"\(4\) quintals \(60\) kg", r"\(3\) quintals \(40\) kg")),
        (1702, r"A cook uses \(25\%\) of 7 kg 360 g of flour. How much flour does she use?",
         lambda: g.r3_units(25, 7360, "kg", "g", 1000, r"7\text{ kg }360\text{ g}"),
         plain(r"\(1\) kg \(480\) g", r"\(2\) kg \(840\) g", r"\(1\) kg \(840\) g", r"\(1\) kg \(804\) g"))],
    4: [(588, r"A shop sold \(42\) pens on Monday. This was \(15\%\) of all the pens it had. How many pens did it have?", lambda: g.r4(15, 42, Num, "the number of pens"), Num),
        (589, r"After spending \(64\%\) of his salary, a man has Rs \(108\) left. What was his salary?", lambda: g.r4_left(64, 108), Rs),
        (1708, r"In a school, \(35\%\) of the pupils are girls. If there are \(91\) girls, how many pupils are there in all?",
         lambda: g.r4(35, 91, Num, "the number of pupils"), Num),
        (1709, r"A team won \(45\) matches, which is \(16\frac{2}{3}\%\) of the matches it played. How many matches did it play?", lambda: g.r4(F(50, 3), 45, Num, "the number of matches"), Num),
        (1710, r"If \(12\frac{1}{2}\%\) of a sum of money is Rs \(47\), find the sum.", lambda: g.r4(F(25, 2), 47, Rs, "the sum"), Rs)],
    5: [(47, r"Find what per cent \(\frac{7}{12}\) is of \(\frac{14}{15}\).", lambda: g.r5(F(7, 12), F(14, 15), r"\frac{7}{12}", r"\frac{14}{15}"), P),
        (590, r"Express \(0.375\) as a percentage of \(1\frac{1}{4}\).", lambda: g.r5(F(3, 8), F(5, 4), "0.375", r"1\frac{1}{4}"), P),
        (591, r"\(120\) kg of rice is what per cent of \(800\) kg?", lambda: g.r5(120, 800, "120", "800"), P),
        (1714, r"A girl spends Rs \(4\frac{1}{2}\) out of Rs \(6\frac{3}{4}\). What per cent of her money does she spend?",
         lambda: g.r5(F(9, 2), F(27, 4), r"4\frac{1}{2}", r"6\frac{3}{4}"), P)],
    6: [(594, r"\(15\%\) of a number is \(36\). What is \(35\%\) of it? Also find the number.", lambda: g.r6(15, 36, y=35, both=True),
         plain(r"\(72\) and \(240\)", r"\(84\) and \(210\)", r"\(240\) and \(84\)", r"\(84\) and \(240\)")),
        (1715, r"If \(24\%\) of a number is \(66\), find \(36\%\) of the number.", lambda: g.r6(24, 66, y=36), Num),
        (1716, r"If \(28\) is \(16\frac{2}{3}\%\) of a number, what is \(83\frac{1}{3}\%\) of that number?", lambda: g.r6(F(50, 3), 28, y=F(250, 3)), Num),
        (1717, r"In a town \(36\%\) of the people, that is \(189\) people, own a car. How many people make up \(64\%\) of the town?", lambda: g.r6(36, 189, y=64), Num),
        (1718, r"A tank is \(22\frac{1}{2}\%\) full when it holds \(81\) litres. What per cent full is it when it holds \(126\) litres?", lambda: g.r6(F(45, 2), 81, y1=126), P),
        (1719, r"\(28\%\) of a number is \(98\). Then \(154\) is what per cent of the number?", lambda: g.r6(28, 98, y1=154), P)],
    7: [(595, r"The price of a litre of oil is increased by \(15\%\), and the increase is Rs \(6\). Find the original and the new price "
              r"of the oil per litre.", lambda: g.r7(6, 15, "both_up", "price"),
         plain(r"Original price = Rs \(46\), New price = Rs \(40\)", r"Original price = Rs \(40\), New price = Rs \(46\)",
               r"Original price = Rs \(40\), New price = Rs \(34\)", r"Original price = Rs \(36\), New price = Rs \(42\)"))],
    8: [(596, r"A dairy has two kinds of liquid: one holds \(16\%\) milk and the other \(40\%\) milk. A drum is filled with 3 parts of the first and 5 parts of the second. Find the percentage of milk in the drum.", lambda: g.r8(16, 40, 3, 5), P),
        (1727, r"A shop mixes 2 parts of a liquid with \(20\%\) milk and 3 parts of a liquid with \(9\%\) milk in a can. What percentage of the can is milk?", lambda: g.r8(20, 9, 2, 3), P),
        (1730, r"A bucket is filled with 3 parts of liquid P, which is \(32\%\) milk, and 6 parts of liquid Q, which is \(14\%\) milk. Find the percentage of milk in the bucket.", lambda: g.r8(32, 14, 3, 6), P)],
}

from common import tex  # noqa: E402

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
