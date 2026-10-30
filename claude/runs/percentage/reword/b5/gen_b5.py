"""Percentage rewording batch 5 (2026-10-30): the 34 rows of Rules 33-37 that fail the originality gate get all-new numbers, a
sentence in the book's simple style with the setting changed (tea, petrol, heights, a clerk's salary, a trader's mark-up ...),
new options, and the explanation the gen_33_40.py builders write for the new numbers. Independent check: the solve_33_40.py
solvers; Rules 36-37 read the direction of each per cent from the nearest word, so every per cent sits next to one of
raised / increased / grows / above / marks (up) or cut / reduced / decreased / falls / discount (down) - not "rose" or "fell",
which the solver does not know. Rules 36-37 are "signed" answers: options say Increase / Decrease or Profit / Loss of the size.
Writes reword/b5/ruleNN/2_new_rows.json; check: `python reword_check.py b5`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_33_40 as g  # noqa: E402
from gen_1_8 import P  # noqa: E402

side, ud = g.other_side, g.up_down
opts = lambda *pairs: dict(zip("abcd", g.chg(pairs)))

PLAN = {
    33: [(621, r"If the price of tea goes down by \(20\%\), by how much per cent can a family use more tea and still spend the same on it?",
          lambda: side(33, 20), P),
         (1838, r"The price of petrol drops by \(25\%\). By what per cent can a taxi driver use more petrol without spending any more on it?",
          lambda: side(33, 25), P)],
    34: [(622, r"One shop's sales are \(60\%\) more than another shop's sales. By how much per cent are the second shop's sales less than "
               r"the first shop's?", lambda: side(34, 60), P),
         (1845, r"Rice costs \(20\%\) more than wheat. By what per cent is wheat cheaper than rice?", lambda: side(34, 20), P),
         (1846, r"Mohan earns \(50\%\) more than Sohan. By what per cent does Sohan earn less than Mohan?", lambda: side(34, 50), P),
         (1847, r"A cupboard is \(25\%\) taller than a table. By how much per cent is the table shorter than the cupboard?",
          lambda: side(34, 25), P),
         (1848, r"A tower is \(150\%\) taller than a house. By what per cent is the house shorter than the tower?", lambda: side(34, 150), P),
         (1849, r"A field is \(80\%\) larger than a garden. By what per cent is the garden smaller than the field?", lambda: side(34, 80), P),
         (1850, r"A van carries \(12\frac{1}{2}\%\) more load than a car. By what per cent does the car carry less than the van?",
          lambda: side(34, F(25, 2)), P)],
    35: [(623, r"Asha weighs \(20\%\) less than Meena. By how much per cent is Meena's weight more than Asha's?", lambda: side(35, 20), P),
         (1851, r"A pencil costs \(4\%\) less than a pen. By what per cent is the pen dearer than the pencil?", lambda: side(35, 4), P),
         (1852, r"A small tank holds \(40\%\) less water than a big tank. By what per cent does the big tank hold more than the small one?",
          lambda: side(35, 40), P),
         (1853, r"Ravi scored \(50\%\) fewer runs than Amit. By what per cent are Amit's runs more than Ravi's?", lambda: side(35, 50), P),
         (1854, r"A bicycle costs \(80\%\) less than a scooter. By how much per cent is the scooter's price more than the bicycle's?",
          lambda: side(35, 80), P),
         (1855, r"A girl's pocket money is \(16\frac{2}{3}\%\) less than her brother's. By what per cent is her brother's pocket money more "
                r"than hers?", lambda: side(35, F(50, 3)), P),
         (1856, r"A hall has \(10\%\) fewer seats than a theatre. By how much per cent does the theatre have more seats than the hall?",
          lambda: side(35, 10), P)],
    36: [(624, r"A clerk's salary is raised by \(20\%\) and later cut by \(20\%\). What is the net change in his salary?",
          lambda: ud(20, 20, "salary"), opts(("Increase", 4), ("Decrease", 4), ("none", 0), ("Decrease", 20))),
         (1857, r"A trader marks his goods \(15\%\) above cost and then gives a discount of \(15\%\). What is his profit or loss per cent?",
          lambda: ud(15, 15, "price"), opts(("Loss", F(9, 4)), ("Profit", F(9, 4)), ("none", 0), ("Loss", F(45, 2)))),
         (1858, r"The population of a village grows by \(25\%\) in one year and falls by \(25\%\) the next year. What is the overall "
                r"effect on the population?", lambda: ud(25, 25, "population"),
          opts(("Increase", F(25, 4)), ("none", 0), ("Decrease", F(25, 4)), ("Decrease", F(5, 2)))),
         (1859, r"A nurse's salary is increased by \(4\%\) and then reduced by \(4\%\). By how much per cent has her salary changed?",
          lambda: ud(4, 4, "salary"), opts(("Decrease", F(4, 25)), ("Increase", F(4, 25)), ("Decrease", F(8, 5)), ("none", 0))),
         (1860, r"A cook's salary is raised by \(50\%\) and then cut by \(50\%\). What is the change in his salary?",
          lambda: ud(50, 50, "salary"), opts(("none", 0), ("Increase", 25), ("Decrease", 50), ("Decrease", 25))),
         (1863, r"A driver's salary goes up by \(12\%\) and is then reduced by \(12\%\). Find the change in his salary.",
          lambda: ud(12, 12, "salary"), opts(("Increase", F(36, 25)), ("Decrease", F(36, 25)), ("Decrease", F(12, 5)), ("none", 0))),
         (1864, r"A guard's salary is increased by \(5\%\) and after that reduced by \(5\%\). What is the net change in his salary?",
          lambda: ud(5, 5, "salary"), opts(("Decrease", F(5, 2)), ("Increase", F(1, 4)), ("none", 0), ("Decrease", F(1, 4))))],
    37: [(625, r"A teacher's salary was raised by \(20\%\) and later cut by \(15\%\). What was the net change in her salary?",
          lambda: ud(20, 15, "salary"), opts(("Increase", 5), ("Decrease", 2), ("Increase", 2), ("Increase", 3))),
         (1865, r"A seller marks a bag \(30\%\) above its cost and then gives a discount of \(20\%\). What is his profit or loss per cent?",
          lambda: ud(30, 20, "price"), opts(("Profit", 4), ("Loss", 4), ("Profit", 10), ("Profit", 6))),
         (1866, r"A worker's salary is first reduced by \(40\%\) and then increased by \(30\%\). What is the overall effect on his salary?",
          lambda: ud(30, 40, "salary", down_first=True), opts(("Increase", 22), ("Decrease", 22), ("Decrease", 10), ("Decrease", 12))),
         (1868, r"A peon's salary was increased by \(8\%\) and then cut by \(15\%\). What was the change in his salary?",
          lambda: ud(8, 15, "salary"), opts(("Decrease", 7), ("Increase", F(41, 5)), ("Decrease", F(41, 5)), ("Decrease", F(19, 5)))),
         (1869, r"A manager's salary was raised by \(16\%\) and then reduced by \(25\%\). What was the change in his salary?",
          lambda: ud(16, 25, "salary"), opts(("Decrease", 9), ("Increase", 13), ("Decrease", 4), ("Decrease", 13))),
         (1870, r"A typist's salary was increased by \(40\%\) and afterwards decreased by \(15\%\). What was the change in her salary?",
          lambda: ud(40, 15, "salary"), opts(("Increase", 19), ("Increase", 25), ("Decrease", 19), ("Increase", 21))),
         (1871, r"A shopkeeper marks a lamp \(50\%\) above cost and then gives a discount of \(30\%\). What profit or loss does he make?",
          lambda: ud(50, 30, "price"), opts(("Profit", 20), ("Profit", 5), ("Loss", 5), ("Profit", 15))),
         (1872, r"A dealer marks a fan \(20\%\) above its cost and then allows a discount of \(10\%\). Find his profit or loss per cent.",
          lambda: ud(20, 10, "price"), opts(("Profit", 10), ("Loss", 8), ("Profit", 2), ("Profit", 8))),
         (1873, r"A tailor marks a suit \(45\%\) above cost and gives a discount of \(30\%\). What profit or loss does he make?",
          lambda: ud(45, 30, "price"), opts(("Profit", F(3, 2)), ("Loss", F(3, 2)), ("Profit", 15), ("Profit", F(27, 2)))),
         (1874, r"A labourer's salary is first cut by \(40\%\) and then raised by \(15\%\). What is the percentage effect on his salary?",
          lambda: ud(15, 40, "salary", down_first=True), opts(("Decrease", 25), ("Increase", 31), ("Decrease", 31), ("Decrease", 19))),
         (1875, r"The population of a village decreased by \(16\%\) in one year and increased by \(25\%\) in the next year. What is the "
                r"overall effect on the population?", lambda: ud(25, 16, "population", down_first=True),
          opts(("Decrease", 5), ("Increase", 9), ("Increase", 5), ("Increase", 4)))],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
