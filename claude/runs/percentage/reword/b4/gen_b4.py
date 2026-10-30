"""Percentage rewording batch 4 (2026-10-30): the 31 rows of Rules 25-32 that fail the originality gate (nearly all of them the
book's "The population of a town is ... It increases by x% during the first year ..." sentence) get all-new numbers, a sentence
in the book's simple style about another place (a hill village, an island, a colony ...), new options, and the explanation the
gen_25_32.py builders write for the new numbers (they speak of a population, so the questions still do). Independent check:
the solve_25_32.py solvers, so each sentence keeps what they read: the verbs grows / rises / falls or, in the past tense,
increased / decreased (the solver does not know "rose" or "fell"), "years ago" for the past, the population as the largest
plain number, the males' rate before the females', and "number of males" only when the males are asked. The yearly rates
avoid every number of the row's old question (the gate also rejects a kept 10% or 20%).
Writes reword/b4/ruleNN/2_new_rows.json; check: `python reword_check.py b4`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_25_32 as g  # noqa: E402
from gen_1_8 import Num, P  # noqa: E402

UP, DN = g.UP, g.DN
yrs = g.years

PLAN = {
    25: [(613, r"A hill village has 6400 people. Its population grows by \(25\%\) in the first year and by \(15\%\) in the second year. "
               r"How many people will live there after two years?", lambda: yrs(6400, [(UP, 25), (UP, 15)], False), Num),
         (1804, r"An island has 7000 people. In the first year its population rises by \(20\%\), and in the second year by \(15\%\). What is "
                r"the population at the end of the second year?", lambda: yrs(7000, [(UP, 20), (UP, 15)], False), Num),
         (1805, r"A new colony starts with 12500 people. Its population grows by \(4\%\) in the first year, \(25\%\) in the second year and "
                r"\(30\%\) in the third year. What is the population after three years?", lambda: yrs(12500, [(UP, 4), (UP, 25), (UP, 30)], False), Num),
         (1806, r"A fishing village has 4800 people. Its population rises by \(5\%\) in the first year and by \(30\%\) in the next year. "
                r"How many people live there after the two years?", lambda: yrs(4800, [(UP, 5), (UP, 30)], False), Num)],
    26: [(614, r"An island has 16000 people. In the first year its population rises by \(25\%\), in the second year it falls by \(15\%\), "
               r"and in the third year it rises by \(5\%\). What is the population after the three years?",
          lambda: yrs(16000, [(UP, 25), (DN, 15), (UP, 5)], False), Num),
         (1807, r"A mining town has 40000 people. Its population grows by \(15\%\) in the first year, falls by \(25\%\) in the second year "
                r"and grows by \(30\%\) in the third year. Find the population after three years.",
          lambda: yrs(40000, [(UP, 15), (DN, 25), (UP, 30)], False), Num),
         (1808, r"A river town has 32000 people. In the first year its population rises by \(25\%\), in the second year it falls by "
                r"\(15\%\), and in the third year it rises by \(30\%\). How many people live there after three years?",
          lambda: yrs(32000, [(UP, 25), (DN, 15), (UP, 30)], False), Num),
         (1809, r"A border village has 18000 people. Its population grows by \(10\%\) in the first year, falls by \(30\%\) in the second "
                r"year and grows by \(40\%\) in the third year. What will the population be after three years?",
          lambda: yrs(18000, [(UP, 10), (DN, 30), (UP, 40)], False), Num),
         (1810, r"A port city has 60000 people. In the first year its population rises by \(5\%\), in the second year it falls by \(16\%\), "
                r"and in the third year it rises by \(30\%\). What is the population after three years?",
          lambda: yrs(60000, [(UP, 5), (DN, 16), (UP, 30)], False), Num)],
    27: [(615, r"The population of a colony increased by \(20\%\) in one year and decreased by \(15\%\) the next year. It is 5100 now. "
               r"What was it 2 years ago?", lambda: yrs(5100, [(UP, 20), (DN, 15)], True), Num),
         (1812, r"The population of an island increased by \(30\%\) in one year and decreased by \(10\%\) in the next. It is now 9360. "
                r"What was the population 2 years ago?", lambda: yrs(9360, [(UP, 30), (DN, 10)], True), Num),
         (1813, r"In a hill town the population increased by \(15\%\) in the first year and decreased by \(20\%\) in the second year, to "
                r"23000. What was the population 2 years ago?", lambda: yrs(23000, [(UP, 15), (DN, 20)], True), Num),
         (1816, r"The population of a village increased by \(30\%\) in the first year, decreased by \(15\%\) in the second year and "
                r"increased by \(40\%\) in the third year. It is 15470 now. What was it 3 years ago?",
          lambda: yrs(15470, [(UP, 30), (DN, 15), (UP, 40)], True), Num),
         (1817, r"A colony's population increased by \(40\%\) in one year and decreased by \(25\%\) the next year, ending at 6300. What "
                r"was the population 2 years ago?", lambda: yrs(6300, [(UP, 40), (DN, 25)], True), Num)],
    28: [(616, r"The population of a hill town grows by \(5\%\) in the first year and by \(30\%\) in the second year, reaching 12285. "
               r"What was the population 2 years ago?", lambda: yrs(12285, [(UP, 5), (UP, 30)], True), Num),
         (1818, r"An island's population rises by \(20\%\) in one year and by \(35\%\) in the next year. It is now 6480. What was it 2 years "
                r"ago?", lambda: yrs(6480, [(UP, 20), (UP, 35)], True), Num),
         (1819, r"The population of a new colony increased by \(15\%\) in the first year and by \(10\%\) in the second year. Now it is "
                r"25300. What was the population 2 years ago?", lambda: yrs(25300, [(UP, 15), (UP, 10)], True), Num),
         (1820, r"A village's population increased by \(30\%\) in the first year and by \(5\%\) in the second year, to 13650. Find the "
                r"population 2 years ago.", lambda: yrs(13650, [(UP, 30), (UP, 5)], True), Num)],
    29: [(617, r"A desert town has 9000 people. Its population falls by \(5\%\) in the first year, by \(30\%\) in the second and by "
               r"\(40\%\) in the third. What will it be after these three years?", lambda: yrs(9000, [(DN, 5), (DN, 30), (DN, 40)], False), Num),
         (1821, r"A mill town has 25000 people. Its population falls by \(4\%\) in the first year, \(15\%\) in the second year and \(25\%\) "
                r"in the third year. Find the population after three years.", lambda: yrs(25000, [(DN, 4), (DN, 15), (DN, 25)], False), Num),
         (1822, r"An old port has 60000 people. In the first year its population falls by \(30\%\), in the second by \(10\%\) and in the "
                r"third by \(15\%\). What is the population after three years?", lambda: yrs(60000, [(DN, 30), (DN, 10), (DN, 15)], False), Num),
         (1823, r"A dry village has 12000 people. Its population falls by \(15\%\) in the first year, \(25\%\) in the second year and "
                r"\(50\%\) in the third year. How many people are left after three years?",
          lambda: yrs(12000, [(DN, 15), (DN, 25), (DN, 50)], False), Num)],
    30: [(618, r"A village lost people for three years: its population decreased by \(10\%\) in the first year, \(25\%\) in the second "
               r"year and \(16\%\) in the third year. Now 11340 people live there. What was the population 3 years ago?",
          lambda: yrs(11340, [(DN, 10), (DN, 25), (DN, 16)], True), Num),
         (1824, r"The population of a mining town decreased by \(15\%\) in the first year, by \(30\%\) in the second and by \(25\%\) in the "
                r"third. It is 17850 now. What was it 3 years ago?", lambda: yrs(17850, [(DN, 15), (DN, 30), (DN, 25)], True), Num),
         (1825, r"An island's population decreased by \(30\%\) in the first year, \(15\%\) in the second year and \(40\%\) in the third "
                r"year, leaving 21420 people. How many people lived there 3 years ago?",
          lambda: yrs(21420, [(DN, 30), (DN, 15), (DN, 40)], True), Num),
         (1826, r"A hill village's population decreased by \(5\%\) in the first year, by \(30\%\) in the second and by \(15\%\) in the "
                r"third, to 9044. What was its population 3 years ago?", lambda: yrs(9044, [(DN, 5), (DN, 30), (DN, 15)], True), Num)],
    31: [(619, r"A village has 5000 people. If the males go up by \(4\%\) and the females by \(8\%\), the village will have 5280 people. "
               r"How many females live there?", lambda: g.males_females(5000, 4, 8, 5280, "females"), Num),
         (1827, r"A hill town has 9000 people. If the males go up by \(15\%\) and the females by \(6\%\), there will be 9810 people. Find "
                r"the number of males.", lambda: g.males_females(9000, 15, 6, 9810, "males"), Num),
         (1828, r"An island has 4500 people. If the males rise by \(8\%\) and the females by \(20\%\), the island will have 5160 people. "
                r"How many females are there?", lambda: g.males_females(4500, 8, 20, 5160, "females"), Num),
         (1829, r"A city ward has 12000 people. If the males rise by \(25\%\) and the females by \(8\%\), the ward will have 13640 people. "
                r"Find the number of males in the ward.", lambda: g.males_females(12000, 25, 8, 13640, "males"), Num)],
    32: [(620, r"If the price of sugar goes up by \(25\%\), by how much per cent must a family cut its use of sugar so that its spending "
               r"on sugar does not change?", lambda: g.cut_consumption(25), P)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
