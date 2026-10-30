"""Percentage rewording batch 7 (2026-10-30): the 48 rows of Rules 49-56 that fail the originality gate get all-new numbers, a
sentence in the book's simple style with the setting changed (a carpet, a photo frame, a field instead of "a rectangle"; a book
room instead of the library's languages; salty water ...), new options, and the explanation the gen_49_56.py builders write for
the new numbers. Independent check: the solve_49_56.py solvers, so each sentence keeps what they read: "fails by N" and "gets N
marks more" (plain digits) for Rule 49, plain-digit "x% in excess / deficit", "increased by x%" and "the other by y%" for the
rectangle rules 50-52, Maths before English for Rule 53, the water lost as the first plain number for Rule 55, and the books
left as the largest plain number for Rule 56. Writes reword/b7/ruleNN/2_new_rows.json; check: `python reword_check.py b7`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_49_56 as g  # noqa: E402
from gen_1_8 import Num, P  # noqa: E402

kg = g.kg
_k = [0]


def err_opts(v):
    """Rule 50 (signed): '\\(5.6\\%\\) excess' style, the right one moving round."""
    v = F(v)
    size, word = abs(v), ("excess" if v > 0 else "deficit")
    wrong = [("deficit" if v > 0 else "excess", size), (word, size + 1), (word, 2 * size)]
    pos = rw_common.POS[_k[0] % len(rw_common.POS)]
    _k[0] += 1
    wrong.insert(pos - 1, (word, size))
    return dict(zip("abcd", g.sg(wrong)))


def two(x, a, y, b, who, tail="What are the maximum marks of the test?"):
    return (rf"In a test, {who[0]} scores \({x}\%\) and fails by {a} marks, while {who[1]} scores \({y}\%\) and gets {b} marks more than "
            rf"the pass mark. {tail}")


PLAN = {
    49: [(637, two(30, 26, 48, 28, ("Ravi", "Mohan")), lambda: g.two_candidates(30, 26, 48, 28), Num),
         (1928, two(35, 33, 50, 27, ("a girl", "her friend")), lambda: g.two_candidates(35, 33, 50, 27), Num),
         (1929, two(20, 35, 36, 45, ("one pupil", "another pupil")), lambda: g.two_candidates(20, 35, 36, 45), Num),
         (1930, two(25, 18, 45, 22, ("Asha", "Meena")), lambda: g.two_candidates(25, 18, 45, 22), Num),
         (1931, two(32, 46, 50, 62, ("a boy", "his brother")), lambda: g.two_candidates(32, 46, 50, 62), Num),
         (1932, two(36, 75, 51, 30, ("one clerk", "another clerk")), lambda: g.two_candidates(36, 75, 51, 30), Num),
         (1933, r"In a test, Sita scores \(28\%\) and fails by 35 marks, while Gita scores \(64\%\) and gets 55 marks more than the pass mark. Find the pass percentage.",
          lambda: g.two_candidates(28, 35, 64, 55, "pass"), P)],
    50: [(1934, r"A carpet is measured with one side taken 10% in excess and the other 4% in deficit. What is the error per cent in its "
                r"area found from these measurements?", lambda: g.area(50, 10, 4), err_opts(F(28, 5))),
         (1935, r"While measuring a field, a man takes one side 5% in excess and the other 8% in deficit. Find the error per cent in the "
                r"area he works out.", lambda: g.area(50, 5, 8), err_opts(F(-17, 5))),
         (1936, r"The sides of a table top are measured, one 20% in excess and the other 10% in deficit. What is the error per cent in the "
                r"area worked out from them?", lambda: g.area(50, 20, 10), err_opts(8)),
         (1937, r"A tailor measures a cloth with one side 12% in excess and the other 5% in deficit. Find the error per cent in the area of "
                r"the cloth from his measures.", lambda: g.area(50, 12, 5), err_opts(F(32, 5))),
         (1938, r"One side of a plot is measured 25% in excess and the other 40% in deficit. What is the error per cent in the area found "
                r"from these figures?", lambda: g.area(50, 25, 40), err_opts(-25))],
    51: [(1939, r"A photo frame is made bigger: one side is increased by 8% and the other by 25%. By what per cent does its area go up?",
          lambda: g.area(51, 8, 25), P),
         (1940, r"To make a garden larger, one side is increased by 20% and the other by 5%. By what per cent does the garden's area grow?",
          lambda: g.area(51, 20, 5), P),
         (1941, r"A poster is printed bigger, with one side increased by 25% and the other by 4%. By what per cent is its area larger?",
          lambda: g.area(51, 25, 4), P),
         (1942, r"A farmer widens his field: one side is increased by 16% and the other by 25%. By what per cent does the area of the field "
                r"rise?", lambda: g.area(51, 16, 25), P),
         (1943, r"A room is made larger, with one side increased by 40% and the other by 10%. By what per cent does the floor area grow?",
          lambda: g.area(51, 40, 10), P),
         (1944, r"A pond is dug wider: one side is increased by 50% and the other by 30%. By what per cent does its surface area go up?",
          lambda: g.area(51, 50, 30), P)],
    52: [(1945, r"A cloth is measured with one side taken 10% in deficit and the other 20% in deficit. By what per cent is the area found "
                r"less than the true area?", lambda: g.area(52, 10, 20), P),
         (1946, r"The sides of a mat are measured, one 2% in deficit and the other 15% in deficit. Find the error per cent in its area.",
          lambda: g.area(52, 2, 15), P),
         (1947, r"A clerk measures a plot with one side 30% in deficit and the other 4% in deficit. What is the error per cent in the area "
                r"he finds?", lambda: g.area(52, 30, 4), P),
         (1948, r"Both sides of a board are measured short, one 40% in deficit and the other 15% in deficit. Find the error per cent in "
                r"the area.", lambda: g.area(52, 40, 15), P),
         (1949, r"A sheet of glass is measured with one side 16% in deficit and the other 25% in deficit. What is the error per cent in "
                r"its area?", lambda: g.area(52, 16, 25), P)],
    53: [(638, r"Of the pupils who sat a test, \(39\%\) failed in Maths, \(46\%\) failed in English and \(19\%\) failed in both. What per cent of the pupils passed in both subjects?", lambda: g.passed_both(39, 46, 19), P),
         (1950, r"In a school test \(28\%\) of the children failed in Maths, \(30\%\) in English and \(6\%\) in both. What per cent passed in both?", lambda: g.passed_both(28, 30, 6), P),
         (1951, r"Of the girls in a class, \(45\%\) failed in Maths, \(16\%\) failed in English and \(8\%\) failed in both subjects. "
                r"Find the per cent who passed in both.", lambda: g.passed_both(45, 16, 8), P),
         (1952, r"In a college exam \(34\%\) of the students failed in Maths and \(52\%\) in English, while \(12\%\) failed in both. What per cent passed in both subjects?", lambda: g.passed_both(34, 52, 12), P),
         (1953, r"At a coaching centre \(44\%\) of the boys failed in Maths, \(46\%\) in English and \(19\%\) in both. What per cent of them passed in both?", lambda: g.passed_both(44, 46, 19), P),
         (1954, r"In a village school \(26\%\) of the pupils failed in Maths, \(42\%\) failed in English and \(18\%\) failed in both. "
                r"Find the per cent of pupils who passed in both subjects.", lambda: g.passed_both(26, 42, 18), P),
         (1955, r"In a test for clerks, \(60\%\) failed in Maths, \(45\%\) in English and \(30\%\) in both. What per cent passed in both "
                r"papers?", lambda: g.passed_both(60, 45, 30), P),
         (1956, r"Of the candidates at a centre, \(32\%\) failed in Maths, \(54\%\) failed in English and \(16\%\) failed in both. What "
                r"per cent of the candidates passed in both?", lambda: g.passed_both(32, 54, 16), P)],
    54: [(639, r"A woman spends \(60\%\) of her income. Her income goes up by \(38\%\) and her spending by \(18\%\). By what per cent do her savings go up?", lambda: g.savings(60, 38, 18), P),
         (1957, r"A clerk spends \(84\%\) of his pay. His pay rises by \(22\%\) and his spending by \(14\%\). Find the per cent rise in his savings.", lambda: g.savings(84, 22, 14), P),
         (1958, r"A family spends \(48\%\) of its income. The income grows by \(17\%\) and the spending by \(4\%\). By what per cent do the savings grow?", lambda: g.savings(48, 17, 4), P),
         (1959, r"A shopkeeper spends \(90\%\) of what he earns. His earnings go up by \(37\%\) and his spending by \(21\%\). By how much per cent do his savings rise?", lambda: g.savings(90, 37, 21), P),
         (1960, r"A driver spends \(83\%\) of his income. His income rises by \(29\%\) and his spending by \(12\%\). Find the per cent increase in his savings.", lambda: g.savings(83, 29, 12), P),
         (1961, r"A nurse spends \(75\%\) of her salary. Her salary goes up by \(8\%\) and her spending by \(4\%\). By what per cent do "
                r"her savings go up?", lambda: g.savings(75, 8, 4), P)],
    55: [(640, r"A bucket of salty water is \(4\%\) salt by weight. After 36 kg of water dries up, the water left is \(16\%\) salt. How many kg of salty water were there at first?", lambda: g.salt(4, 36, 16), kg),
         (1962, r"Some sea water is \(9\%\) salt by weight. When 15 kg of the water is boiled away, it becomes \(14\%\) salt. Find the weight of the sea water at first.", lambda: g.salt(9, 15, 14), kg),
         (1963, r"A tub of salt water holds \(8\%\) salt by weight. After 45 kg of water dries up, the salt makes \(18\%\) of what is "
                r"left. How heavy was the salt water at first?", lambda: g.salt(8, 45, 18), kg),
         (1964, r"A drum of brine is \(12\%\) salt by weight. When 40 kg of water is taken out by heating, the brine becomes \(20\%\) "
                r"salt. Find the first weight of the brine.", lambda: g.salt(12, 40, 20), kg),
         (1965, r"A pan of salty water is \(12\%\) salt by weight. After 45 kg of water boils off, the salt is \(21\%\) of the weight. What did the salty water weigh at first?", lambda: g.salt(12, 45, 21), kg),
         (1966, r"A tank of salt water has \(13\%\) salt by weight. When 57 kg of water dries up, the salt is \(16\%\) of the rest. Find the weight of the salt water at first.", lambda: g.salt(13, 57, 16), kg)],
    56: [(641, r"In a school's book room \(25\%\) of the books are novels, \(36\%\) of the rest are science books and \(21\%\) of what is left are history books. The other 3792 books are comics. How many books are there in all?",
          lambda: g.library(25, 36, 21, 3792), Num),
         (1967, r"Of the books in a shop, \(25\%\) are dictionaries, \(35\%\) of the rest are atlases and \(23\%\) of the remaining are maps. The last 3003 books are story books. How many books does the shop have?", lambda: g.library(25, 35, 23, 3003), Num),
         (1968, r"In a book fair \(30\%\) of the books are on science, \(50\%\) of the rest are on history and \(15\%\) of what remains "
                r"are on art. The remaining 5950 books are novels. Find the number of books at the fair.",
          lambda: g.library(30, 50, 15, 5950), Num),
         (1969, r"A college library keeps \(23\%\) of its books on law, \(50\%\) of the rest on medicine and \(16\%\) of the remaining on music. The other 3234 books are on sports. How many books does it keep?", lambda: g.library(23, 50, 16, 3234), Num),
         (1970, r"In a store room \(20\%\) of the books are old, \(30\%\) of the rest are torn and \(45\%\) of the remaining are new "
                r"text books. The remaining 4620 books are note books. How many books are in the room?",
          lambda: g.library(20, 30, 45, 4620), Num),
         (1971, r"Of the books given to a village, \(8\%\) were on farming, \(60\%\) of the rest were for children and \(30\%\) of the "
                r"remaining were on health. The other 2576 books were on crafts. How many books were given?",
          lambda: g.library(8, 60, 30, 2576), Num)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
