"""Rewording batch 5 (2026-10-29): the 74 regular rows of Time & Work Rules 31-40 that copied the book get all-new numbers and a
sentence in the book's simple style with the job/object changed (the owner's choice), new options, and an explanation
regenerated with the same rule generator for the new numbers. Row ids, rule links, days and times stay. 1397 was done in the
pilot; the Miscellaneous rows are left for their own batch. 239 and 244 are the same book question (the owner keeps both), so
they get different numbers. Numbers keep the order the Rule 31-40 solvers read them in, and each sentence keeps the phrase its
solver uses to tell the question types apart ("assist", "C finishes it", "helped on every", "C joins A", "joined B",
"days less than B", "help of C", "B starts", "working together", "B and C start", "together", "In all").
Writes reword/b5/ruleNN/2_new_rows.json; check: `python reword_check.py b5` (simple gate - SIMPLE_STYLE marker)."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/b5
sys.path.insert(0, os.path.dirname(HERE))
import rw_common  # noqa: E402
from gen_31_35 import (a_left31, a_rest35, alt32, b_first31, b_rest34, boys31, c33, c_joins31, helped31, less31,  # noqa: E402
                       pairs31, with_c31)
from gen_36_40 import r36, r37, r38, r39, r40  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (job changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-29)")
plain = lambda *v: dict(zip("abcd", v))

PLAN = {
    31: [(239, "A man, a woman or a boy can paint a house in 18 days, 22 days or 33 days respectively. How many boys must "
               "assist 3 men and 2 women to paint it in 2 days?", lambda: boys31(18, 22, 33, 3, 2, 2), "boys"),
         (244, "A man, a woman or a boy can build a wall in 11 days, 44 days or 55 days respectively. How many boys must "
               "assist 3 men and 2 women to build it in 2 days?", lambda: boys31(11, 44, 55, 3, 2, 2), "boys"),
         (1377, "A man, a woman or a boy can clean a park in 21 days, 54 days or 70 days respectively. How many boys must "
                "assist 4 men and 9 women to clean it in 2 days?", lambda: boys31(21, 54, 70, 4, 9, 2), "boys"),
         (240, "A and B together can lay a road in 10 days, which B and C together can lay in 24 days. After A has worked on "
               "it for 3 days and B for 6 days, C finishes it in 26 days. In how many days could each of them lay the road "
               "alone?", lambda: pairs31(10, 24, 3, 6, 26), "days"),
         (1668, "A and B together can paint a school in 9 days, and B and C together in 12 days. A paints for 3 days and B "
                "for 5 days, and then C finishes it in 11 days. In how many days could each of them paint the school alone?",
                lambda: pairs31(9, 12, 3, 5, 11), "days"),
         (241, "A can plough a field in 24 days, B in 32 days and C in 96 days. If A is helped on every 3rd day by B and C, in "
               "how many days is the field ploughed?", lambda: helped31(24, 32, 96, 3), "days"),
         (1669, "A can weave a carpet in 24 days, B in 28 days and C in 42 days. If A is helped on every 2nd day by B and C, "
                "in how many days will the carpet be finished?", lambda: helped31(24, 28, 42, 2), "days"),
         (242, "A can build a shed in 14 days, B in 35 days. They work together for 4 days. Then B leaves and A alone "
               "continues. After 1 day C joins A and the shed is finished in 6 more days. In how many days can C build it "
               "alone?", lambda: c_joins31(14, 35, 4, 1, 6), "days"),
         (1670, "A can paint a hall in 12 days and B in 36 days. They paint together for 3 days. Then B leaves and A alone "
                "continues. After 1 day C joins A and the hall is finished in 5 more days. In how many days can C paint it "
                "alone?", lambda: c_joins31(12, 36, 3, 1, 5), "days"),
         (243, "A and B can dig a pond in 26 days and 13 days respectively. They began digging together, but A left after some "
               "days and B finished the rest in 4 days. After how many days did A leave?", lambda: a_left31(26, 13, 4), "days"),
         (1671, "A and B can tile a floor in 28 days and 21 days respectively. They began together, but A left after some days "
                "and B finished the rest of the floor in 7 days. After how many days did A leave?",
                lambda: a_left31(28, 21, 7), "days"),
         (1672, "A and B can stitch a set of curtains in 11 days and 33 days respectively. B started the stitching alone, and "
                "5 days before it was finished A joined B. For how many days did B work alone?",
                lambda: b_first31(11, 33, 5), "days"),
         (1673, "A can repair a road in 7 days less than B. A works at it alone for 8 days and then B takes over and finishes "
                "it. If 17 days were needed in all, how many days would each of them take alone?",
                lambda: less31(7, 8, 17), "days"),
         (1674, "A can plaster a house in 54 days, while B alone can plaster it in 27 days. With the help of C they plaster it "
                "in 12 days. In how many days can C alone plaster the house?", lambda: with_c31(54, 27, 12), "days")],
    32: [(245, "A and B working alone can paint a fence in 6 days and 12 days respectively. They work at it on alternate "
               "days. If A starts, in how many days will the fence be painted?", lambda: alt32(6, 12), "days"),
         (246, "A and B working separately can build a wall in 8 and 15 days respectively. A starts and they work on "
               "alternate days. In how many days will the wall be built?", lambda: alt32(8, 15), "days"),
         (247, "A and B working alone can weave a rug in 10 days and 14 days respectively. They work at it on alternate days. "
               "If B starts the weaving, in how many days will the rug be finished?", lambda: alt32(10, 14, b_first=True),
               "days"),
         (248, "A and B working separately can dig a well in 10 and 5 days respectively. B starts the digging and they work on "
               "alternate days. In how many days will the well be dug?", lambda: alt32(10, 5, b_first=True), "days"),
         (249, "Two girls, Rita and Gita, working separately, can paint a room in 11 and 10 hours respectively. If they work "
               "for an hour by turns, Rita beginning at 7 am, when will the painting be finished?",
               lambda: alt32(11, 10, names=("Rita", "Gita"), unit="hours", start_hour=7),
               plain("6:30 pm", "5:30 pm", "4:30 pm", "5:00 pm")),
         (250, "A and B, working separately, can clean a hall in 12 and 11 hours respectively. At 9 am A starts the work and "
               "they work in turns of an hour each. When will the cleaning be finished?",
               lambda: alt32(12, 11, unit="hours", start_hour=9), plain("8:00 pm", "9:30 pm", "8:30 pm", "7:30 pm")),
         (1675, "A and B working alone can plant a garden in 12 days and 8 days respectively. They work at it on alternate "
                "days, A starting the work. In how many days will the garden be planted?", lambda: alt32(12, 8), "days"),
         (1676, "A and B working alone can repair a boat in 6 days and 9 days respectively. They work at it on alternate days. "
                "If B starts the repair, in how many days will the boat be ready?", lambda: alt32(6, 9, b_first=True), "days"),
         (1677, "Two tailors, Meena and Leela, working separately, can stitch a dress in 14 and 7 hours respectively. They "
                "stitch for an hour each by turns, Meena starting at 6 am. At what time will the dress be finished?",
                lambda: alt32(14, 7, names=("Meena", "Leela"), unit="hours", start_hour=6),
                plain("4:00 pm", "2:30 pm", "3:00 pm", "3:30 pm")),
         (1678, "Kiran and Sunil can paint a house alone in 13 and 10 days respectively. Kiran starts the work on 3rd March "
                "and they work on alternate days. On which day of March will the house be painted?",
                lambda: alt32(13, 10, names=("Kiran", "Sunil"), start_date=3),
                plain("14th March", "13th March", "15th March", "12th March")),
         (1679, "A and B, working separately, can mow a lawn in 11 and 15 hours respectively. At 8 am A starts, and they "
                "work in turns of an hour each. When will the mowing be finished?",
                lambda: alt32(11, 15, unit="hours", start_hour=8), plain("8:12 pm", "8:36 pm", "9:36 pm", "7:36 pm")),],
    33: [(251, "A, B and C together can build a shed in 7 days. A alone can build it in 12 days and B alone in 42 days. In "
               "what time can C alone build the shed?", lambda: c33(7, 12, 42), "days"),
         (1378, "A, B and C together can paint a hall in 14 days. A alone can paint it in 30 days and B alone in 70 days. In "
                "what time can C alone paint the hall?", lambda: c33(14, 30, 70), "days"),
         (1379, "A, B and C together can dig a canal in 11 days. A alone can dig it in 44 days and B alone in 55 days. In "
                "what time can C alone dig the canal?", lambda: c33(11, 44, 55), "days"),
         (1380, "A, B and C together can weave a carpet in 6 days. A alone can weave it in 14 days and B alone in 42 days. "
                "In what time can C alone weave the carpet?", lambda: c33(6, 14, 42), "days"),
         (1381, "A, B and C together can tile a courtyard in 6 days. A alone can tile it in 11 days and B alone in 33 days. "
                "In what time can C alone tile the courtyard?", lambda: c33(6, 11, 33), "days")],
    34: [(252, "A can paint a wall in 45 days and B can paint it in 27 days. If A paints for 5 days and then leaves, in how "
               "many days will B paint the rest of the wall?", lambda: b_rest34(45, 27, 5), "days"),
         (1382, "A can build a fence in 14 days and B can build it in 42 days. If A works for 8 days and then leaves, in how "
                "many days will B build the rest?", lambda: b_rest34(14, 42, 8), "days"),
         (1383, "A can plough a field in 54 days and B can plough it in 42 days. If A ploughs for 9 days and then leaves, in "
                "how many days will B plough the rest?", lambda: b_rest34(54, 42, 9), "days"),
         (1384, "A can repair a road in 19 days and B can repair it in 38 days. If A works for 11 days and then leaves, in how "
                "many days will B repair the rest?", lambda: b_rest34(19, 38, 11), "days")],
    35: [(253, "A can paint a school in 33 days and B alone can paint it in 11 days. If B paints for 7 days and then leaves, "
               "in how many days will A paint the rest?", lambda: a_rest35(33, 11, 7), "days"),
         (1385, "A can build a boat in 32 days and B alone can build it in 26 days. If B works for 13 days and then leaves, in "
                "how many days will A alone finish the boat?", lambda: a_rest35(32, 26, 13), "days"),
         (1386, "A and B working together can dig a well in 14 days, and B alone could dig it in 49 days. If B digs for 4 "
                "days, in how many days could A alone finish the well?", lambda: a_rest35(None, 49, 4, ab=14), "days"),
         (1387, "A and B working together can paint a house in 18 days, and B alone could paint it in 42 days. If B paints "
                "for 14 days, in how many days could A alone finish the house?", lambda: a_rest35(None, 42, 14, ab=18), "days"),
         (1388, "A and B working together can lay a floor in 17 days, and B alone could lay it in 34 days. If B works for 4 "
                "days, in how many days could A alone finish the floor?", lambda: a_rest35(None, 34, 4, ab=17), "days"),
         (1389, "A and B working together can weave a carpet in 20 days, and B alone could weave it in 50 days. If B weaves "
                "for 5 days, in how many days could A alone finish the carpet?", lambda: a_rest35(None, 50, 5, ab=20), "days"),
         (1390, "A can build a wall in 21 days, B in 14 days and C in 18 days. B and C start the work and have to leave after "
                "3 days. How long will A alone take to build the rest of the wall?",
                lambda: a_rest35(21, None, 3, bc_names=(14, 18)), "days")],
    36: [(254, "A and B can paint a house in 14 days and 56 days. Both start together, but B leaves 4 days before the house "
               "is painted. Find the time in which the house is painted.", lambda: r36(14, 56, 4), "days"),
         (1391, "A and B can build a wall in 20 days and 44 days respectively. Both start together, but B leaves 4 days before "
                "the wall is built. Find the time in which the wall is built.", lambda: r36(20, 44, 4), "days"),
         (1392, "A and B can dig a pond in 28 days and 49 days respectively. Both start together, but B leaves 6 days before "
                "the pond is dug. Find the time in which the pond is dug.", lambda: r36(28, 49, 6), "days"),
         (1393, "A and B can lay a road in 24 days and 56 days respectively. Both start together, but B leaves 4 days before "
                "the road is finished. Find the time in which the road is finished.", lambda: r36(24, 56, 4), "days"),
         (1394, "A and B can tile a hall in 12 days and 42 days respectively. Both start together, but B leaves 3 days before "
                "the tiling is done. Find the time in which the tiling is done.", lambda: r36(12, 42, 3), "days"),
         (1680, "A and B can weave a carpet in 26 days and 66 days respectively. Both start together, but B leaves 3 days "
                "before the carpet is finished. Find the time in which the carpet is finished.", lambda: r36(26, 66, 3),
                "days")],
    37: [(255, "A and B can paint a fence in 13 days and 26 days respectively. Both start together, but A leaves 11 days "
               "before the fence is painted. Find the time in which the fence is painted.", lambda: r37(13, 26, 11), "days"),
         (1395, "A and B can build a shed in 18 days and 40 days respectively. Both start together, but A leaves 11 days "
                "before the shed is built. Find the time in which the shed is built.", lambda: r37(18, 40, 11), "days"),
         (1396, "A can plough a field in 16 days and B in 36 days. They begin together. But 10 days before the ploughing is "
                "finished, A leaves. In how many days is the field ploughed?", lambda: r37(16, 36, 10), "days"),
         (1398, "A can dig a trench in 22 days and B in 32 days. They begin together. But 5 days before the digging is "
                "finished, A leaves. In how many days is the trench dug?", lambda: r37(22, 32, 5), "days"),
         (1399, "A can repair a bridge in 22 days and B in 40 days. They begin together. But 9 days before the repair is "
                "finished, A leaves. In how many days is the bridge repaired?", lambda: r37(22, 40, 9), "days")],
    38: [(256, "A can paint a hall in 48 days. A paints for 9 days only and leaves. B paints the rest in 13 days. In how many "
               "days can B alone paint the hall?", lambda: r38(48, 9, 13), "days"),
         (257, "A can build a wall in 24 days. He works at it for 13 days and then B alone finishes the wall in 11 days. The "
               "two together could build the wall in:", lambda: r38(24, 13, 11, together=True), "days"),
         (1400, "A can lay a floor in 39 days. A works for 13 days only and leaves. B lays the rest in 24 days. In how many "
                "days can B alone lay the floor?", lambda: r38(39, 13, 24), "days"),
         (1401, "A can dig a canal in 68 days. A digs for 14 days only and leaves. B digs the rest in 27 days. In how many "
                "days can B alone dig the canal?", lambda: r38(68, 14, 27), "days"),
         (1402, "A can weave a set of mats in 68 days. A weaves for 17 days only and leaves. B weaves the rest in 15 days. In "
                "how many days can B alone weave the mats?", lambda: r38(68, 17, 15), "days"),
         (1403, "A can repair a roof in 44 days. A works for 11 days only and leaves. B repairs the rest in 12 days. In how "
                "many days can B alone repair the roof?", lambda: r38(44, 11, 12), "days"),
         (1404, "A can plaster a house in 56 days. A works for 14 days only and leaves. B plasters the rest in 27 days. In "
                "how many days can B alone plaster the house?", lambda: r38(56, 14, 27), "days"),
         (1405, "A can stitch a tent in 26 days. He stitches for 10 days and then B alone finishes the tent in 36 days. In "
                "how many days could the two together stitch the tent?", lambda: r38(26, 10, 36, together=True), "days")],
    39: [(258, "A and B can paint a school in 36 days and 24 days respectively. They start together, but after some days A "
               "leaves. B alone paints the rest in 14 days. After how many days does A leave?", lambda: r39(36, 24, 14), "days"),
         (1406, "A and B can build a road in 44 days and 28 days respectively. They start together, but after some days A "
                "leaves. B alone builds the rest in 10 days. After how many days does A leave?",
                lambda: r39(44, 28, 10), "days"),
         (1407, "A and B can dig a well in 35 days and 21 days respectively. They start together, but after some days A "
                "leaves. B alone digs the rest in 5 days. After how many days does A leave?", lambda: r39(35, 21, 5), "days"),
         (1408, "A and B can lay a pipeline in 26 days and 42 days respectively. They start together, but after some days A "
                "leaves. B alone lays the rest in 8 days. After how many days does A leave?", lambda: r39(26, 42, 8), "days"),
         (1409, "A and B can tile a hall in 32 days and 28 days respectively. They start together, but after some days A "
                "leaves. B alone tiles the rest in 13 days. After how many days does A leave?",
                lambda: r39(32, 28, 13), "days"),
         (1410, "A and B can paint a bridge in 33 days and 44 days respectively. They start together, but after some days A "
                "leaves. B alone paints the rest in 16 days. After how many days does A leave?",
                lambda: r39(33, 44, 16), "days")],
    40: [(259, "Ram can paint a house in 34 days. Shyam can paint the same house in 12 days. Ram starts painting alone and "
               "after 11 days Shyam joins him. How many days will they now take together to paint the rest?",
               lambda: r40(34, 12, 11, "Ram", "Shyam"), "days"),
         (260, "Mahesh and Umesh can complete a wall in 18 and 40 days respectively. Umesh starts building it, and after 11 "
               "days Mahesh joins him. In all, how many days does the wall take?",
               lambda: r40(40, 18, 11, "Umesh", "Mahesh", total=True), "days"),
         (1411, "A can build a shed in 44 days. B can build the same shed in 20 days. A started working alone and after 12 "
                "days B joined him. How many days will they now take together to build the rest?",
                lambda: r40(44, 20, 12), "days"),
         (1412, "A can dig a pond in 19 days. B can dig the same pond in 38 days. A started digging alone and after 4 days B "
                "joined him. How many days will they now take together to dig the rest?", lambda: r40(19, 38, 4), "days"),
         (1413, "A can lay a floor in 21 days. B can lay the same floor in 28 days. A started working alone and after 7 days "
                "B joined him. How many days will they now take together to lay the rest?", lambda: r40(21, 28, 7), "days"),
         (1414, "A can weave a carpet in 21 days. B can weave the same carpet in 42 days. A started weaving alone and after 3 "
                "days B joined him. How many days will they now take together to weave the rest?",
                lambda: r40(21, 42, 3), "days"),
         (1415, "A can repair a road in 27 days. B can repair the same road in 36 days. A started working alone and after 13 "
                "days B joined him. How many days will they now take together to repair the rest?",
                lambda: r40(27, 36, 13), "days"),
         (1681, "Nikhil and Rohan can complete a fence in 21 and 42 days respectively. Rohan starts building it, and after 3 "
                "days Nikhil joins him. In all, how many days does the fence take?",
                lambda: r40(42, 21, 3, "Rohan", "Nikhil", total=True), "days")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
