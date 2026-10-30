"""Percentage rewording batch 3 (2026-10-30): the 23 rows of Rules 18-24 that fail the originality gate get all-new numbers, a
sentence in the book's simple style with the setting changed (club members, trees, fish, a machine's value, savings in a box
instead of "the population of a town" and "his locker"), new options, and the explanation the gen_17_24.py builders write for
the new numbers. Independent check: the solve_17_24.py solvers, so every sentence keeps the words they read ("increase" /
"grows", "decrease" / "falls", "N years", "ago", Rs amounts). Writes reword/b3/ruleNN/2_new_rows.json; check: `python reword_check.py b3`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_17_24 as g  # noqa: E402
from gen_1_8 import Num  # noqa: E402

Rsx = g.Rsx
pop = g.population

PLAN = {
    18: [(606, r"Ravi and Mohan put Rs 2500 into a joint box. Ravi takes out \(16\%\) of it, and then Mohan takes \(25\%\) of what is left. "
               r"How much is left in the box?", lambda: g.forward(2500, [16, 25], "-", g.T18, Rsx, ["Ravi takes", "Mohan takes"]), Rsx)],
    19: [(607, r"A woman puts some money in a bank. Later she adds \(30\%\) of it, and after that she adds \(40\%\) of the new amount. Now "
               r"she has Rs 9100. How much did she put in at first?", lambda: g.backward(9100, [30, 40], "+", g.T19, Rsx, "the initial amount"), Rsx),
         (1779, r"A shop owner had some money in his safe. He added \(10\%\) of it, and later added \(40\%\) of the increased amount. Now "
                r"the safe has Rs 13860. How much was in it at first?", lambda: g.backward(13860, [10, 40], "+", g.T19, Rsx, "the initial amount"), Rsx)],
    20: [(608, r"Two years ago a boy had Rs 3500 in his piggy bank. In the first year he added \(40\%\) of it, and in the second year he "
               r"added \(30\%\) of the new amount. How much does he have now?",
          lambda: g.forward(3500, [40, 30], "+", g.T20, Rsx, ["First year", "Second year"]), Rsx),
         (1782, r"A trust had Rs 1600 in its fund. In the first year \(25\%\) of the fund was added to it, and in the second year \(35\%\) of "
                r"the new total was added. What is the fund now?", lambda: g.forward(1600, [25, 35], "+", g.T20, Rsx, ["First year", "Second year"]), Rsx),
         (1783, r"A club kept Rs 2400 in a box two years ago. It added \(15\%\) of this in the first year and \(60\%\) of the increased sum "
                r"in the second year. How much is in the box now?", lambda: g.forward(2400, [15, 60], "+", g.T20, Rsx, ["First year", "Second year"]), Rsx)],
    21: [(609, r"A club has 2000 members. If the number grows by \(10\%\) every year, how many members will it have in 3 years?",
          lambda: pop(2000, 10, 3, "+", False, Num, "number of members"), Num),
         (1788, r"A village has 6400 people. Its population increases by \(25\%\) each year. What will it be after 2 years?",
          lambda: pop(6400, 25, 2, "+", False), Num)],
    22: [(610, r"The number of students in a college increases by \(5\%\) every year. There are 9261 students now. How many were there "
               r"3 years ago?", lambda: pop(9261, 5, 3, "+", True, Num, "number of students"), Num),
         (1789, r"The sales of a shop increase by \(5\%\) a year and are now Rs 4410. What were its sales two years ago?",
          lambda: pop(4410, 5, 2, "+", True, Rsx, "sales"), Rsx),
         (1790, r"The number of trees in a park increases by \(10\%\) every year. Now there are 12100 trees. How many trees were there 2 "
                r"years ago?", lambda: pop(12100, 10, 2, "+", True, Num, "number of trees"), Num),
         (1791, r"A city's population grows by \(30\%\) every year and is now 21970. What was it 3 years ago?",
          lambda: pop(21970, 30, 3, "+", True), Num),
         (1792, r"The number of cars in a town increases by \(30\%\) each year. There are 6760 cars now. How many cars were there 2 years "
                r"ago?", lambda: pop(6760, 30, 2, "+", True, Num, "number of cars"), Num),
         (1793, r"The number of visitors to a fair grows by \(50\%\) every year. This year there are 9000 visitors. How many visitors came "
                r"2 years ago?", lambda: pop(9000, 50, 2, "+", True, Num, "number of visitors"), Num)],
    23: [(611, r"The number of birds in a forest is 8000 and falls by \(10\%\) every year. How many birds will there be in 2 years?",
          lambda: pop(8000, 10, 2, "-", False, Num, "number of birds"), Num),
         (1796, r"A village has 25000 people, and its population decreases by \(4\%\) a year. What will it be in 2 years?",
          lambda: pop(25000, 4, 2, "-", False), Num),
         (1798, r"The value of a machine is Rs 12000 and it falls by \(15\%\) each year. What will its value be after 2 years?",
          lambda: pop(12000, 15, 2, "-", False, Rsx, "value"), Rsx),
         (1799, r"A lake has 64000 fish, and the number decreases by \(25\%\) every year. How many fish will be left in 3 years?",
          lambda: pop(64000, 25, 3, "-", False, Num, "number of fish"), Num)],
    24: [(612, r"The number of workers in a mill decreases by \(5\%\) every year. Now there are 3610 workers. How many were there 2 years "
               r"ago?", lambda: pop(3610, 5, 2, "-", True, Num, "number of workers"), Num),
         (1800, r"The value of a car falls by \(20\%\) every year. It is worth Rs 51200 now. What was its value 3 years ago?",
          lambda: pop(51200, 20, 3, "-", True, Rsx, "value"), Rsx),
         (1801, r"The number of fish in a pond decreases by \(30\%\) each year. Now there are 4900 fish. How many were there 2 years ago?",
          lambda: pop(4900, 30, 2, "-", True, Num, "number of fish"), Num),
         (1802, r"The number of trees in a forest decreases by \(10\%\) every year. There are 6075 trees now. How many were there 2 years "
                r"ago?", lambda: pop(6075, 10, 2, "-", True, Num, "number of trees"), Num),
         (1803, r"The number of people in a hill village decreases by \(40\%\) each year. Now there are 21600 people. How many lived there "
                r"3 years ago?", lambda: pop(21600, 40, 3, "-", True), Num)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
