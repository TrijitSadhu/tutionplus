"""Percentage rewording batch 2 (2026-10-30): the 27 rows of Rules 12-16 ("two values x% and y% more / less than / of a third
value") get all-new numbers and a sentence about real things (ropes, bags, pens, jars ...) that still says "the first", "the
second" and "a third", the words the gen_9_16.py explanations use. Every row of these rules failed the gate because all of them
copied the book's one sentence. Independent check: b2/solve_b2.py (works with actual values, the third one taken as 7).
Writes reword/b2/ruleNN/2_new_rows.json; check: `python reword_check.py b2`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import rw_common  # noqa: E402
import gen_9_16 as g  # noqa: E402
from gen_1_8 import P  # noqa: E402

PLURAL = {"box": "boxes", "bus": "buses"}


def sentence(obj, measure, clause1, clause2, ask, how_less=False):
    """clause1 / clause2 describe the first and the second against the third ('is 8% longer than a third rope');
    ask = 'first of second' (the first as a per cent of the second) or 'second of first'."""
    a, b = ask.split(" of ")
    head = rf"The first of two {PLURAL.get(obj, obj + 's')} {clause1}, and the second {clause2}. "
    if how_less:
        return head + rf"By what per cent is the {a} {obj}'s {measure} less than the {b} {obj}'s?"
    return head + rf"What per cent of the {b} {obj}'s {measure} is the {a} {obj}'s {measure}?"


def up(obj, measure, word, x, y, ask):          # Rules 12-13
    return sentence(obj, measure, rf"{word[0]} \({x}\%\) {word[1]} than a third {obj}", rf"{word[0]} \({y}\%\) {word[1]} than the third", ask)


def down(obj, measure, word, x, y, ask, how_less=False):          # Rules 14-15
    return sentence(obj, measure, rf"{word[0]} \({x}\%\) {word[1]} than a third {obj}", rf"{word[0]} \({y}\%\) {word[1]} than the third",
                    ask, how_less)


def part(obj, measure, verb, x, y, ask):          # Rule 16
    return sentence(obj, measure, rf"{verb} \({x}\%\) of what a third {obj} {verb}", rf"{verb} \({y}\%\) of it", ask)


PLAN = {
    12: [(600, up("rope", "length", ("is", "longer"), 8, 35, "first of second"), lambda: g.rel(12, 8, 35), P),
         (1746, up("bag", "weight", ("weighs", "more"), 40, 12, "first of second"), lambda: g.rel(12, 40, 12), P),
         (1747, up("shirt", "price", ("costs", "more"), 20, 25, "first of second"), lambda: g.rel(12, 20, 25), P),
         (1748, up("field", "crop", ("gives", "more"), 14, 90, "first of second"), lambda: g.rel(12, 14, 90), P),
         (1749, up("worker", "pay", ("earns", "more"), 65, 50, "first of second"), lambda: g.rel(12, 65, 50), P),
         (1750, up("tank", "capacity", ("holds", "more"), 26, 5, "first of second"), lambda: g.rel(12, 26, 5), P)],
    13: [(601, up("box", "weight", ("weighs", "more"), 20, 26, "second of first"), lambda: g.rel(13, 20, 26), P),
         (1751, up("house", "price", ("costs", "more"), 75, 40, "second of first"), lambda: g.rel(13, 75, 40), P),
         (1752, up("shop", "income", ("earns", "more"), 80, 62, "second of first"), lambda: g.rel(13, 80, 62), P),
         (1753, up("road", "length", ("is", "longer"), 16, 45, "second of first"), lambda: g.rel(13, 16, 45), P),
         (1754, up("farm", "crop", ("gives", "more"), 50, 20, "second of first"), lambda: g.rel(13, 50, 20), P)],
    14: [(602, down("pen", "price", ("costs", "less"), 10, 46, "second of first"), lambda: g.rel(14, 10, 46), P),
         (1755, down("car", "fuel use", ("uses", "less"), 15, 32, "second of first"), lambda: g.rel(14, 15, 32), P),
         (1756, down("tree", "height", ("is", "shorter"), 40, 55, "second of first"), lambda: g.rel(14, 40, 55), P),
         (1757, down("bulb", "power", ("uses", "less"), 16, 37, "second of first", True), lambda: g.rel(14, 16, 37, True), P),
         (1758, down("coat", "price", ("costs", "less"), 5, 24, "second of first", True), lambda: g.rel(14, 5, 24, True), P)],
    15: [(603, down("ladder", "length", ("is", "shorter"), 28, 10, "first of second"), lambda: g.rel(15, 28, 10), P),
         (1759, down("phone", "price", ("costs", "less"), 37, 16, "first of second"), lambda: g.rel(15, 37, 16), P),
         (1760, down("bus", "load", ("carries", "less"), 65, 30, "first of second"), lambda: g.rel(15, 65, 30), P),
         (1761, down("pump", "output", ("lifts", "less"), 28, 4, "first of second"), lambda: g.rel(15, 28, 4), P),
         (1762, down("lamp", "power", ("uses", "less"), 60, 50, "first of second", True), lambda: g.rel(15, 60, 50, True), P)],
    16: [(604, part("jar", "contents", "holds", 18, 24, "first of second"), lambda: g.of_third(18, 24), P),
         (1763, part("pipe", "flow", "gives", 14, 35, "first of second"), lambda: g.of_third(14, 35), P),
         (1764, part("girl", "pay", "earns", 9, 36, "first of second"), lambda: g.of_third(9, 36), P),
         (1765, part("plot", "area", "covers", 26, 65, "first of second"), lambda: g.of_third(26, 65), P),
         (1766, part("well", "water", "gives", 33, 55, "first of second"), lambda: g.of_third(33, 55), P),
         (1767, part("crate", "load", "holds", 28, 35, "second of first"), lambda: g.of_third(28, 35, True), P)],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
