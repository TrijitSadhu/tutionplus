"""Rewording batch 2 (2026-10-29): the 50 regular rows of Time & Work Rules 6-10 that copied the book get a fresh sentence and
all-new numbers (copyright - the owner's rule), new options, and an explanation regenerated with the same rule generator for
the new numbers. Row ids, rule links, days and times stay. The Miscellaneous rows of these rules (262, 263, 264, 265, 267) are
left for the Miscellaneous batch; 1258 and 1268 were done in the pilot. Number sets were picked so that no book sentence holds
the same set (originality.Book.numbers_together). Writes reword/b2/ruleNN/2_new_rows.json; check: `python reword_check.py b2`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/b2
sys.path.insert(0, os.path.dirname(HERE))
from rw_common import write_batch  # noqa: E402
from gen_5_10 import (a_finishes6, ab_from_abc6, ab_from_chain, ac_and_b, c_from_groups, called_off6, children9,  # noqa: E402
                      equiv9, frac_b6, mb_time9, mw8, orig10, other_alone, r7, ratio9, three6, times9)

AC_B = ("A and C together", "B alone")

PLAN = {
    6: [(199, "Papering a room is a 12-day job for the pair A and B, but a 21-day job for A on his own. Working by himself, how long would B take?", lambda: other_alone(12, 21), "days"),
        (200, "Working as a pair, A and B could mow a sports ground in 30 days. With C helping, the three of them mow it in 18 "
              "days. If C mowed it alone, how many days would it take?", lambda: c_from_groups(30, 18), "days"),
        (1260, "A and B paint a warehouse together in 33 days; when C joins them the job takes 22 days. How long would C need to "
               "paint it single-handed?", lambda: c_from_groups(33, 22), "days"),
        (1269, "Two workers, A and B, complete an order together in 45 days, and adding a third worker C brings this down to 30 "
               "days. How many days would C alone take for the order?", lambda: c_from_groups(45, 30), "days"),
        (201, "B alone takes 15 hours to clean a hall; B and C together take 5 hours; A, B and C together take 3 hours. If only A "
              "and B clean it, how many hours will they need?", lambda: ab_from_chain(15, 5, 3), "hours"),
        (1261, "A printing job takes B 12 hours by himself, B and C 4 hours together, and all three of A, B and C just 3 hours. "
               "How long would A and B take as a pair?", lambda: ab_from_chain(12, 4, 3), "hours"),
        (202, "Laying a lawn takes 7 days for the pair A-B, 21 days for the pair B-C and 6 days when A, B and C all work. Find the "
              "time for the pair A-C and the time for B working alone.", lambda: ac_and_b(7, 21, 6), "days", AC_B),
        (1262, "For a fencing job, A with B needs 9 days, B with C needs 36 days, and the whole trio needs 8 days. What time would "
               "A and C need as a pair, and what time would B need on his own?", lambda: ac_and_b(9, 36, 8), "days", AC_B),
        (203, r"After working alone for 13 days A has finished \(\frac{3}{8}\) of a job. B then joins him and together they complete what is left in 15 days. How many days would B need to do the whole job without A?", lambda: frac_b6("3/8", 13, 15), "days"),
        (1263, r"After 11 days of working alone, A has done \(\frac{1}{3}\) of a carpentry order. From then on B helps, and the rest takes them 11 days. On his own, how long would B need for the full order?", lambda: frac_b6("1/3", 11, 11), "days"),
        (204, "Fitting out a shop would take A and B 21 days as a pair and B 28 days alone. The pair works for 7 days, then B leaves. For how many further days must A keep working?", lambda: a_finishes6(21, 28, 7), "days"),
        (1264, "Wiring an office block is a 26-day job for A and B together and a 39-day job for B alone. Both work for the first 13 days, after which B moves to another site. How long does A spend finishing the wiring?", lambda: a_finishes6(26, 39, 13), "days"),
        (207, "Repainting a school would take A and B 22 days together, or B 33 days alone. B begins by himself and paints for 11 days; A then takes over on his own. How many days of painting are left for A?", lambda: a_finishes6(22, 33, 11, True), "days"),
        (1267, "A garden can be landscaped by A and B together in 28 days, or by B alone in 42 days. For the first 14 days only B works; after that A carries on alone. How many more days does A need?", lambda: a_finishes6(28, 42, 14, True), "days"),
        (205, "Together, A and B could harvest an orchard in 12 days. They pick together for 3 days, after which B leaves and A needs 45 more days to finish alone. How long would A and B each take on their own?", lambda: called_off6(12, 3, 45), "days"),
        (1265, "Working as a pair, A and B could build a stone wall in 36 days. After 12 days B leaves, and A needs 42 more days to "
               "finish on his own. Find the time each would need to build the wall alone.", lambda: called_off6(36, 12, 42), "days"),
        (206, "Varnishing a floor takes 15 days with A, B and C all working, 60 days for B alone, and 21 days for B and C together. If only A and B do it, how many days will it take?", lambda: ab_from_abc6(15, 60, 21), "days"),
        (1266, "With A, B and C painting, a mural is done in 13 days. B on his own would take 39 days, and B and C as a pair 26 days. How long would A and B need as a pair?", lambda: ab_from_abc6(13, 39, 26), "days"),
        (1259, "Alone, A would need 10 days to glaze the windows of a block of flats, B 14 days and C 35 days. With all three "
               "glazing, how many days will the job take?", lambda: three6(10, 14, 35), "days")],
    7: [(208, "Three workers split a contract. If B did it single-handed he would be 3 times as slow as A and C working as a pair; if C did it single-handed he would be 2 times as slow as A and B as a pair. All three together take 15 days. What is the time each would need working alone?", lambda: r7("each", 3, 2, 15), "days"),
        (1270, "Left to himself, B would need 4 times as long as A and C need between them, and C would need 3 times as long as A and B need between them. If all three join forces, the task is over in 22 days. How many days would A, B and C each need working solo?", lambda: r7("each", 4, 3, 22), "days"),
        (209, "Every day, A and C between them get through 2 times the work that B gets through, and A and B between them get through 3 times the work that C gets through. As a trio they finish a project in 10 days. How long would each of them need alone?", lambda: r7("each", 2, 3, 10, much=True), "days"),
        (1271, "In a day, A and C between them do 2 times the work B does, while A and B between them do 3 times the work C does. "
               "If all three finish a job in 20 days, find each person's time alone.", lambda: r7("each", 2, 3, 20, much=True), "days"),
        (210, "A trio shares a task. Measured against the pair A and C, B on his own is 2 times as slow; measured against the pair A and B, C on his own is 6 times as slow. The trio needs 20 days. If B and C were left to do it, how many days would they need?", lambda: r7("bc", 2, 6, 20), "days"),
        (1272, "For one particular task, B by himself is 2 times as slow as the pair A and C, and C by himself is 3 times as slow as the pair A and B. Working as a trio they need 14 days. How many days would the pair B and C need?", lambda: r7("bc", 2, 3, 14), "days"),
        (1273, "Alone, B is 2 times as slow as A and C together, while C alone is 3 times as slow as A and B together. A, B and C working side by side finish in 35 days. Find the time B and C would take working together.", lambda: r7("bc", 2, 3, 35), "days")],
    8: [(211, "6 men would need 35 days to reap a field, and 8 women would need exactly as long. If a mixed team of 6 men and 6 women reaps it, how many days will that take?", lambda: mw8(6, 8, 35, 6, 6), "days"),
        (1274, "Either 6 men or 7 women would need 26 days to paint a school. If 6 men and 6 women paint it together, how many "
               "days will it take?", lambda: mw8(6, 7, 26, 6, 6), "days"),
        (1275, "A dam's wall can be repaired by 7 men or, alternatively, by 8 women in 30 days. A team of 7 men and 7 women is sent "
               "instead. In how many days will they finish?", lambda: mw8(7, 8, 30, 7, 7), "days"),
        (1276, "Ploughing a farm keeps 6 men busy for 32 days; 7 women would also take 32 days. A team of 6 men and 7 women is asked to plough only half of the farm. How many days will they need?", lambda: mw8(6, 7, 32, 6, 7, part=F(1, 2)), "days"),
        (1277, "Weaving a set of carpets takes 54 days whether 4 men or 5 women do it. A team made up of 4 men and 4 women takes over the weaving. In how many days will the carpets be ready?", lambda: mw8(4, 5, 54, 4, 4), "days"),
        (1278, "Laying a path would occupy 5 men for 56 days, and 9 boys would need the same 56 days. Suppose 5 men and 5 boys lay it side by side; how many days will they take?", lambda: mw8(5, 9, 56, 5, 5, w="boys"), "days"),
        (1279, "A stitching order is a 9-day task for a group of 4 men, and equally a 9-day task for a group of 7 women. Sharing it, 4 men and 14 women will finish in how many days?", lambda: mw8(4, 7, 9, 4, 14), "days")],
    9: [(212, "Between them, 11 men and 20 boys finish a job in 11 days; a smaller team of 8 men and 6 boys needs 21 days for the same job. Working at these rates, how many days would 9 men and 15 boys need?", lambda: mb_time9(11, 20, 11, 8, 6, 21, 9, 15), "days"),
        (1280, "Ploughing a field takes 11 days when 4 men and 12 boys work, but only 4 days when 14 men and 24 boys work. If 3 men and 15 boys are sent instead, how long will the ploughing take?", lambda: mb_time9(4, 12, 11, 14, 24, 4, 3, 15), "days"),
        (213, "A road is surfaced by 7 men and 11 boys in 9 days, and the same road could be surfaced by 6 men and 18 boys in 8 "
              "days. Find the ratio of a man's daily work to a boy's daily work.", lambda: ratio9(7, 11, 9, 6, 18, 8), "ratio"),
        (1281, "A fence goes up in 8 days with 9 men and 7 boys at work, and in 10 days with 3 men and 14 boys. What is the ratio of one man's daily output to one boy's?", lambda: ratio9(9, 7, 8, 3, 14, 10), "ratio"),
        (1284, "Building a hall takes 19 men and 15 boys 5 days, while 7 men and 9 boys take 12 days. In what ratio does a boy's daily work stand to a man's?", lambda: ratio9(19, 15, 5, 7, 9, 12, boy_first=True), "ratio"),
        (216, "A wall can be built by hiring 8 men and 13 boys for 12 days, or by hiring 10 men and 15 boys for 10 days. Compare a boy's daily work with a man's.", lambda: ratio9(8, 13, 12, 10, 15, 10, boy_first=True), "ratio"),
        (214, "On this site 2 men get through as much work as 7 boys. A road that 16 men and 8 boys tar in 15 days would take 12 men and 6 boys how many days?", lambda: equiv9(16, 8, 15, 12, 6, 2, 7), "days"),
        (1282, "Here 3 men are as productive as 4 boys. If 27 men and 14 boys lay a pipeline in 18 days, how long would a team of 21 men and 8 boys take to lay it?", lambda: equiv9(27, 14, 18, 21, 8, 3, 4), "days"),
        (215, "Per hour, a group of 8 men and 2 boys produces 6 times the output of 1 man working beside 1 boy. What is the ratio of one man's output to one boy's?", lambda: times9(8, 2, 6), "ratio"),
        (1283, "The hourly output of 10 men and 1 boy is 4 times the hourly output of 2 men and 1 boy. In what ratio is a man's work to a boy's?", lambda: times9(10, 1, 4, 2, 1), "ratio"),
        (217, "A child needs twice as long as a man to finish a task. 16 children and 7 men together finish a task in 10 days. In "
              "how many days would 25 men finish it?", lambda: children9(16, 7, 10, 25), "days"),
        (1285, "26 children working alongside 7 men complete a site clean-up in 6 days; any child takes twice as long as a man over the same work. How many days would a team of 8 men alone need?", lambda: children9(26, 7, 6, 8), "days")],
    10: [(218, "A contractor's crew can finish a job in 45 days. Had the crew been 9 men short, the job would have run 9 days "
               "longer. How many men are in the crew?", lambda: orig10(45, 9, 9), "men"),
         (1286, "A crew finishes a project in 39 days. With 6 men fewer, the same project would last 18 days longer. How many men are in the crew?", lambda: orig10(39, 6, 18), "men"),
         (1287, "A gang of workers is able to finish a canal in 33 days. If the gang had 7 men fewer, the canal would take 11 days "
                "longer. Find the size of the gang.", lambda: orig10(33, 7, 11), "men"),
         (1288, "A survey team completes its work in 55 days. If 4 men were taken off the team, the work would take 11 days more. Find the number of men in the team.", lambda: orig10(55, 4, 11), "men"),
         (1289, "With its full strength a crew can pave a square in 42 days; with 10 men missing it would need 14 more days. What "
                "is the full strength of the crew?", lambda: orig10(42, 10, 14), "men")],
}


def main():
    write_batch(HERE, PLAN)


if __name__ == "__main__":
    main()
