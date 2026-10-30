"""Percentage rewording batch 6 (2026-10-30): the 35 rows of Rules 41-48 that fail the originality gate get all-new numbers, a
sentence in the book's simple style with the setting changed, new options, and the explanation the gen_41_48.py builders write
for the new numbers. The product rules (42-47) get new pairs of factors - bus fare and passengers, daily wage and workers, room
rent and rooms let, area sown and yield, a pen's price and pens sold - added to gen_41_48.CTX here, so the explanation names the
same two factors as the question. Independent check: the solve_41_48.py solvers (direction words next to each per cent, "bill"
and Rs for Rule 41's bill, the plain-digit phrase "gets N marks and fails by M" for Rule 48).
Writes reword/b6/ruleNN/2_new_rows.json; check: `python reword_check.py b6`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_41_48 as g  # noqa: E402
from gen_1_8 import Num, P  # noqa: E402
from gen_9_16 import Rsx  # noqa: E402
from gen_33_40 import chg  # noqa: E402

g.CTX.update({"fare": ("bus fare", "number of passengers", "takings"), "wage": ("daily wage", "number of workers", "wage bill"),
              "rent": ("rent per room", "number of rooms let", "rent collected"), "crop": ("area sown", "yield per acre", "total crop"),
              "shop": ("price of a pen", "number of pens sold", "sales")})
_k = [0]


def sopts(v, none=False):
    """Signed options: the right one, the same size the other way, (No change,) and wrong sizes; the right one moves round."""
    v = F(v)
    size, word = abs(v), ("Increase" if v > 0 else "Decrease")
    wrong = [("Decrease" if v > 0 else "Increase", size)] + ([("none", 0)] if none else [])
    for a in (2 * size, size + 1, size + 2):
        if len(wrong) < 3 and a != size:
            wrong.append((word, a))
    pos = rw_common.POS[_k[0] % len(rw_common.POS)]
    _k[0] += 1
    wrong.insert(pos - 1, (word, size))
    return dict(zip("abcd", chg(wrong)))


def prod(n, a, b, ctx):
    return lambda: g.product(n, a, b, ctx), sopts(a + b + F(a * b, 100), none=(a == -b))


def row(rid, q, pair):
    return (rid, q, pair[0], pair[1])


PLAN = {
    41: [(629, r"The stock of rice in a store is reduced by \(15\%\) in one month and reduced again by \(15\%\) in the next month. By "
               r"what per cent has the stock gone down in all?", lambda: g.twice_down(15), P),
         (1896, r"A shop can give a customer either one discount of \(44\%\) or two discounts of \(25\%\) each, one after the other. On "
                r"her bill the two offers differ by Rs 15. How much is the bill?", lambda: g.bill(44, 25, 15), Rsx)],
    42: [row(630, r"A bus company cuts its fare by \(25\%\), and the number of passengers goes up by \(10\%\). What is the effect on its "
                  r"takings?", prod(42, -25, 10, "fare")),
         row(1899, r"A factory reduces its daily wage by \(10\%\) but increases the number of workers by \(40\%\). What is the effect on "
                   r"the wage bill?", prod(42, -10, 40, "wage")),
         row(1900, r"A shop lowers the price of a pen by \(15\%\), and the number of pens sold grows by \(20\%\). What is the effect on "
                   r"its sales?", prod(42, -15, 20, "shop"))],
    43: [row(631, r"A hotel cuts its rent per room by \(30\%\), and the number of rooms let increases by \(30\%\). What is the effect on "
                  r"the rent collected?", prod(43, -30, 30, "rent")),
         row(1904, r"A ferry reduces its fare by \(14\%\), and the number of passengers increases by \(14\%\). Find the effect on its "
                   r"takings.", prod(43, -14, 14, "fare")),
         row(1905, r"A shop lowers the price of a pen by \(16\%\), and the number of pens sold goes up by \(16\%\). What happens to its "
                   r"sales?", prod(43, -16, 16, "shop")),
         row(1906, r"A mill cuts its daily wage by \(24\%\) and increases the number of workers by \(24\%\). What is the effect on the "
                   r"wage bill?", prod(43, -24, 24, "wage")),
         row(1907, r"A bus owner reduces the fare by \(28\%\), and the number of passengers grows by \(28\%\). Find the effect on the "
                   r"takings.", prod(43, -28, 28, "fare")),
         row(1908, r"A lodge cuts its rent per room by \(45\%\), and the number of rooms let increases by \(45\%\). What is the effect on "
                   r"the rent collected?", prod(43, -45, 45, "rent"))],
    44: [row(632, r"A farmer's area sown is reduced by \(15\%\) in a dry year, and the yield per acre falls by \(20\%\). What is the effect "
                  r"on his total crop?", prod(44, -15, -20, "crop")),
         row(1909, r"A shop lowers the price of a pen by \(6\%\), and the number of pens sold also falls by \(25\%\). What is the effect on "
                   r"its sales?", prod(44, -6, -25, "shop")),
         row(1910, r"A bus company cuts the fare by \(30\%\), and the number of passengers also decreases by \(5\%\). Find the effect on "
                   r"its takings.", prod(44, -30, -5, "fare")),
         row(1911, r"A hotel reduces its rent per room by \(40\%\), and the number of rooms let also falls by \(15\%\). What is the effect "
                   r"on the rent collected?", prod(44, -40, -15, "rent"))],
    45: [row(633, r"In a bad year the area sown on a farm is reduced by \(8\%\), and the yield per acre is also reduced by \(8\%\). What "
                  r"is the effect on the total crop?", prod(45, -8, -8, "crop")),
         row(1912, r"A workshop cuts its daily wage by \(4\%\) and also cuts the number of workers by \(4\%\). Find the effect on the wage "
                   r"bill.", prod(45, -4, -4, "wage")),
         row(1913, r"A bus fare is reduced by \(12\%\), and the number of passengers also falls by \(12\%\). What is the effect on the "
                   r"takings?", prod(45, -12, -12, "fare")),
         row(1914, r"A guest house lowers its rent per room by \(20\%\), and the number of rooms let also decreases by \(20\%\). What is "
                   r"the effect on the rent collected?", prod(45, -20, -20, "rent"))],
    46: [row(634, r"A bus company raises its fare by \(20\%\), and the number of passengers also increases by \(15\%\). What is the effect "
                  r"on its takings?", prod(46, 20, 15, "fare")),
         row(1915, r"A shop raises the price of a pen by \(30\%\), and the number of pens sold also grows by \(10\%\). Find the effect on "
                   r"its sales.", prod(46, 30, 10, "shop")),
         row(1916, r"A factory increases its daily wage by \(25\%\) and the number of workers by \(8\%\). What is the effect on the wage "
                   r"bill?", prod(46, 25, 8, "wage")),
         row(1917, r"A hotel raises its rent per room by \(16\%\), and the number of rooms let also goes up by \(25\%\). What is the "
                   r"effect on the rent collected?", prod(46, 16, 25, "rent"))],
    47: [row(635, r"In a good year a farmer's area sown is increased by \(20\%\), and the yield per acre also increases by \(20\%\). What "
                  r"is the effect on his total crop?", prod(47, 20, 20, "crop")),
         row(1918, r"A shop raises the price of a pen by \(12\%\), and the number of pens sold also grows by \(12\%\). What is the effect "
                   r"on its sales?", prod(47, 12, 12, "shop")),
         row(1919, r"A bus fare is raised by \(30\%\), and the number of passengers also increases by \(30\%\). Find the effect on the "
                   r"takings.", prod(47, 30, 30, "fare")),
         row(1920, r"A lodge increases its rent per room by \(5\%\), and the number of rooms let also goes up by \(5\%\). What is the "
                   r"effect on the rent collected?", prod(47, 5, 5, "rent"))],
    48: [(636, r"To pass a test, a girl needs \(35\%\) of the total marks. She gets 133 marks and fails by 21 marks. What are the total "
               r"marks?", lambda: g.max_marks(35, 133, 21), Num),
         (1921, r"A boy must score \(55\%\) to pass a science test. He gets 230 marks and fails by 45 marks. Find the maximum marks of the "
                r"test.", lambda: g.max_marks(55, 230, 45), Num),
         (1922, r"In a quiz a player needs \(32\%\) of the full marks to qualify. She gets 70 marks and fails by 26 marks. What are the "
                r"full marks?", lambda: g.max_marks(32, 70, 26), Num),
         (1923, r"To clear a typing test one needs \(15\%\) of the marks. A clerk gets 57 marks and fails by 33 marks. Find the maximum "
                r"marks.", lambda: g.max_marks(15, 57, 33), Num),
         (1924, r"A pupil needs \(28\%\) of the marks to pass a history paper. He gets 160 marks and fails by 36 marks. What is the "
                r"maximum mark of the paper?", lambda: g.max_marks(28, 160, 36), Num),
         (1925, r"For a driving test the pass mark is \(36\%\). A learner gets 250 marks and fails by 38 marks. Find the maximum marks.",
          lambda: g.max_marks(36, 250, 38), Num),
         (1926, r"A girl must get \(48\%\) to pass a music exam. She gets 105 marks and fails by 15 marks. What are the maximum marks?",
          lambda: g.max_marks(48, 105, 15), Num),
         (1927, r"The pass mark of an entrance test is \(65\%\). A boy gets 700 marks and fails by 80 marks. Find the maximum marks.",
          lambda: g.max_marks(65, 700, 80), Num)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
