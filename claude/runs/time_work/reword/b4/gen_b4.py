"""Rewording batch 4 (2026-10-29): the 52 regular rows of Time & Work Rules 21-30 that copied the book get all-new numbers and a
sentence in the book's simple style with the job/object changed (the owner's choice: easy wording, not a hard rewrite), new
options, and an explanation regenerated with the same rule generator for the new numbers. Row ids, rule links, days and times
stay. The Miscellaneous rows of these rules are left for the Miscellaneous batch. Number sets were picked so that no book
sentence holds the same set (originality.Book.numbers_together); numbers keep the order the Rule 21-30 solvers read them in.
Writes reword/b4/ruleNN/2_new_rows.json; check: `python reword_check.py b4` (simple gate - SIMPLE_STYLE marker)."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/b4
sys.path.insert(0, os.path.dirname(HERE))
import rw_common  # noqa: E402
from gen_21_30 import abc23, eff29, food22, leave21, leave25, part28, remain27, sqrt30, team24, twocase26  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (job changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-29)")

PLAN = {
    21: [(230, "A, B and C can paint a house in 12, 26 and 39 days respectively. They all begin together. A works till the "
               "house is finished, but C leaves 4 days and B 2 days before it is finished. In how many days is the house "
               "painted?", lambda: leave21(12, 26, 39, 4, 2), "days"),
         (1335, "A, B and C can build a wall in 12, 24 and 36 days respectively. They start together, but C leaves 5 days "
                "before the wall is finished and B leaves 2 days before it is finished. In how many days is the wall built?",
                lambda: leave21(12, 24, 36, 5, 2), "days"),
         (1336, "A, B and C can dig a well in 8, 30 and 48 days respectively. They start digging together, but C stops 2 days "
                "before the end and B stops 1 day before the end. In how many days is the well dug?",
                lambda: leave21(8, 30, 48, 2, 1), "days"),
         (1337, "A, B and C can tile a floor in 11, 33 and 55 days respectively. They begin together, but C leaves 3 days "
                "before the tiling is done and B leaves 2 days before it is done. Find the number of days the tiling takes.",
                lambda: leave21(11, 33, 55, 3, 2), "days"),
         (1338, "A, B and C can repair a road in 9, 14 and 42 days respectively. They start together, but C leaves 4 days "
                "before the repair is complete and B leaves 2 days before it is complete. In how many days is the road "
                "repaired?", lambda: leave21(9, 14, 42, 4, 2), "days")],
    22: [(231, "A hostel has enough food for 160 men for 46 days. After 40 days, 120 men go home. For how many days will the "
               "rest of the food last for the men who stay?", lambda: food22(160, 46, 40, 120), "days"),
         (1339, "A camp has enough rice for 600 men for 45 days. After 24 days, 240 men leave the camp. For how many days will "
                "the remaining rice last for the men still there?", lambda: food22(600, 45, 24, 240), "days"),
         (1340, "A ship carries enough food for 500 men for 38 days. After 8 days, 200 men get off at a port. For how many "
                "days will the rest of the food last for the men left on board?", lambda: food22(500, 38, 8, 200), "days"),
         (1341, "A fort has enough food for 360 men for 45 days. After 29 days, 200 men march away. For how many days will "
                "the remaining food last for the rest of the men?", lambda: food22(360, 45, 29, 200), "days"),
         (1342, "A relief camp has enough food for 240 men for 36 days. After 27 days, 120 men return to their village. For "
                "how many days will the rest of the food last for those who remain?", lambda: food22(240, 36, 27, 120), "days"),
         (1343, "A school hostel has enough food for 180 men for 16 days. After 6 days, 120 men go on leave. For how many days "
                "will the remaining food last for the others?", lambda: food22(180, 16, 6, 120), "days")],
    23: [(232, "A takes as much time as B and C together to build a wall. A and B together build it in 11 days. C alone "
               "can build it in 22 days. In how many days can B alone build the wall?", lambda: abc23(11, 22), "days"),
         (1344, "A takes as much time as B and C together to paint a hall. A and B together paint it in 13 days. C alone can "
                "paint it in 39 days. In how many days can B alone paint the hall?", lambda: abc23(13, 39), "days"),
         (1345, "A can plough a field in the same time in which B and C together can plough it. If A and B together could "
                "plough it in 12 days, and C alone in 21 days, in what time could B alone plough it?",
                lambda: abc23(12, 21), "days"),
         (1346, "A can weave a carpet in the same time in which B and C together can weave it. If A and B together could weave "
                "it in 14 days, and C alone in 70 days, in what time could B alone weave it?", lambda: abc23(14, 70), "days"),
         (1347, "A can repair a boat in the same time in which B and C together can repair it. If A and B together could "
                "repair it in 21 days, and C alone in 70 days, in what time could B alone repair it?",
                lambda: abc23(21, 70), "days"),
         (1348, "A can stitch a tent in the same time in which B and C together can stitch it. If A and B together could "
                "stitch it in 8 days, and C alone in 24 days, in how many days can A alone stitch the tent?",
                lambda: abc23(8, 24, "A"), "days")],
    24: [(233, "A team of 36 men is supposed to build a road in 23 days. After 10 days, 6 more men were added and the road "
               "was finished 1 day early. By how many days would the work have been delayed if the 6 extra men had not been "
               "added?", lambda: team24(36, 23, 10, 6, 1), "days"),
         (1349, "A team of 27 men is supposed to build a bridge in 46 days. After 23 days, 9 more men were added and the bridge "
                "was finished 2 days early. By how many days would the work have been delayed without the 9 extra men?",
                lambda: team24(27, 46, 23, 9, 2), "days"),
         (1350, "A team of 14 men is supposed to paint a hospital in 51 days. After 46 days, 7 more men joined and the painting "
                "was finished 1 day early. By how many days would the work have been delayed without the 7 extra men?",
                lambda: team24(14, 51, 46, 7, 1), "days"),
         (1351, "A team of 25 men is supposed to lay a pipeline in 48 days. After 20 days, 9 more men joined and the pipeline "
                "was finished 3 days early. By how many days would the work have been delayed without the 9 extra men?",
                lambda: team24(25, 48, 20, 9, 3), "days"),
         (1352, "A team of 12 men is supposed to build a shed in 24 days. After 19 days, 15 more men joined and the shed was "
                "finished 1 day early. In how many days would the shed have been finished without the 15 extra men?",
                lambda: team24(12, 24, 19, 15, 1, delay=False), "days"),
         (1353, "A team of 20 men is supposed to dig a canal in 42 days. After 37 days, 10 more men joined and the canal was "
                "finished 1 day early. In how many days would the canal have been dug without the 10 extra men?",
                lambda: team24(20, 42, 37, 10, 1, delay=False), "days")],
    25: [(234, "A, B and C can paint a school in 24, 30 and 48 days respectively. They started together, but A left after 3 "
               "days, and B left 3 days before the painting was finished. In how many days was the school painted?",
               lambda: leave25(24, 30, 48, 3, 3), "days"),
         (1354, "A, B and C can build a house in 21, 39 and 45 days respectively. They started together, but A left after 7 "
                "days, and B left 2 days before the house was finished. In how many days was the house built?",
                lambda: leave25(21, 39, 45, 7, 2), "days"),
         (1355, "A, B and C can lay a floor in 8, 40 and 35 days respectively. They work at it together. A stops after 3 "
                "days and B stops 5 days before the floor is finished. In what time was the floor laid?",
                lambda: leave25(8, 40, 35, 3, 5), "days"),
         (1356, "A, B and C can clean a park in 15, 26 and 50 days respectively. They work at it together. A stops after 3 "
                "days and B stops 2 days before the park is clean. In what time was the park cleaned?",
                lambda: leave25(15, 26, 50, 3, 2), "days"),
         (1357, "A, B and C can wire a building in 12, 21 and 44 days respectively. They work at it together. A stops after 5 "
                "days and B stops 4 days before the wiring is done. In what time was the wiring finished?",
                lambda: leave25(12, 21, 44, 5, 4), "days"),
         (1358, "A, B and C can plaster a hall in 12, 33 and 42 days respectively. They work at it together. A stops after 4 "
                "days and B stops 3 days before the plastering is done. In what time was the hall plastered?",
                lambda: leave25(12, 33, 42, 4, 3), "days")],
    26: [(235, "A started painting a house and left after working for 8 days. Then B came and finished the painting in 36 "
               "days. If A had left after 13 days, B would have finished the rest in 21 days. In how many days can each of "
               "them alone paint the whole house?", lambda: twocase26(8, 36, 13, 21), "days"),
         (1359, "A started building a wall and left after working for 3 days. Then B came and finished the wall in 36 days. If "
                "A had left after 7 days, B would have finished the rest in 24 days. In how many days can each of them alone "
                "build the whole wall?", lambda: twocase26(3, 36, 7, 24), "days"),
         (1360, "A started weaving a carpet and left after working for 7 days. Then B came and finished it in 28 days. If A "
                "had left after 13 days, B would have finished the rest in 16 days. In how many days can each of them alone "
                "weave the whole carpet?", lambda: twocase26(7, 28, 13, 16), "days"),
         (1361, "A started digging a pond and left after working for 9 days. Then B came and finished it in 25 days. If A had "
                "left after 12 days, B would have finished the rest in 10 days. In how many days can each of them alone dig "
                "the whole pond?", lambda: twocase26(9, 25, 12, 10), "days")],
    27: [(1362, "A can build a wall in 9 days and B in 15 days. They work together for 3 days and then A leaves. How long will "
                "B take to build the rest of the wall?", lambda: remain27(9, 15, 3), "days"),
         (1363, "A can paint a fence in 30 days and B in 20 days. They paint together for 9 days and then A leaves B to finish "
                "alone. How long will B take to paint the rest?", lambda: remain27(30, 20, 9), "days"),
         (1364, "A can plough a field in 28 days and B in 42 days. They plough together for 14 days and then A leaves B to "
                "finish alone. How long will B take to plough the rest?", lambda: remain27(28, 42, 14), "days"),
         (1365, "A can tile a hall in 21 days and B in 42 days. They work together for 11 days and then A leaves B to finish "
                "alone. How long will B take to tile the rest of the hall?", lambda: remain27(21, 42, 11), "days"),
         (1667, "A can stitch a set of curtains in 18 days and B in 30 days. They stitch together for 9 days and then A leaves "
                "B to finish alone. How long will B take to finish the curtains?", lambda: remain27(18, 30, 9), "days")],
    28: [(236, r"A can paint \(\frac{2}{3}\) of a wall in 20 days. In how many days can he paint \(\frac{3}{10}\) of the wall?",
          lambda: part28("2/3", 20, "3/10"), "days"),
         (1366, r"A can dig \(\frac{2}{3}\) of a trench in 12 days. In how many days can he dig \(\frac{1}{2}\) of the trench?",
          lambda: part28("2/3", 12, "1/2"), "days"),
         (1367, r"Ram can knit \(\frac{2}{9}\) of a sweater in 10 days. In how many days can he knit \(\frac{1}{3}\) of the "
                r"sweater?", lambda: part28("2/9", 10, "1/3", "Ram"), "days"),
         (1368, r"Vinay can type \(\frac{3}{7}\) of a book in 24 days. In how many days can he type \(\frac{1}{7}\) of the book?",
          lambda: part28("3/7", 24, "1/7", "Vinay"), "days"),
         (1369, r"Sudhir can plant \(\frac{1}{8}\) of a garden in 12 days. In how many days can he plant \(\frac{1}{12}\) of the "
                r"garden?", lambda: part28("1/8", 12, "1/12", "Sudhir"), "days")],
    29: [(237, "32 men, working 5 hours a day, can build a wall in 15 days. Find the number of days in which 50 men working 4 "
               "hours a day can build a wall twice as long. Assume that 3 men of the first group do as much work in 2 hours "
               "as 4 men of the second group do in 3 hours.", lambda: eff29(32, 5, 15, 50, 4, 2, 3, 2, 4, 3), "days"),
         (1370, "30 men, working 5 hours a day, can lay a road in 18 days. Find the number of days in which 45 men working 9 "
                "hours a day can lay a road twice as long. Assume that 1 man of the first group does as much work in 1 hour as "
                "3 men of the second group do in 1 hour.", lambda: eff29(30, 5, 18, 45, 9, 2, 1, 1, 3, 1), "days"),
         (1371, "30 men, working 7 hours a day, can dig a canal in 12 days. Find the number of days in which 35 men working 9 "
                "hours a day can dig a canal twice as long. Assume that 1 man of the first group does as much work in 2 hours "
                "as 2 men of the second group do in 3 hours.", lambda: eff29(30, 7, 12, 35, 9, 2, 1, 2, 2, 3), "days"),
         (1372, "20 men, working 7 hours a day, can paint a building in 10 days. Find the number of days in which 30 men "
                "working 7 hours a day can paint a building twice as big. Assume that 1 man of the first group does as much "
                "work in 2 hours as 2 men of the second group do in 3 hours.", lambda: eff29(20, 7, 10, 30, 7, 2, 1, 2, 2, 3),
                "days")],
    30: [(238, "A alone would take 28 hours more to paint a hall than A and B together. B alone would take 7 hours more than "
               "A and B together. How long would A and B take to paint the hall together?", lambda: sqrt30(28, 7), "hours"),
         (1373, "A alone would take 25 hours more to clean a factory than A and B together. B alone would take 16 hours more "
                "than A and B together. How long would A and B take to clean it together?", lambda: sqrt30(25, 16), "hours"),
         (1374, "A alone would take 20 hours more to repair a machine than A and B together. B alone would take 5 hours more "
                "than A and B together. How long would A and B take to repair it together?", lambda: sqrt30(20, 5), "hours"),
         (1375, "A alone would take 54 hours more to print a set of books than A and B together. B alone would take 6 hours "
                "more than A and B together. How long would A and B take to print them together?", lambda: sqrt30(54, 6),
                "hours"),
         (1376, "A alone would take 50 hours more to load a ship than A and B together. B alone would take 18 hours more than "
                "A and B together. How long would A and B take to load it together?", lambda: sqrt30(50, 18), "hours")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
