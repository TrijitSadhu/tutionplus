"""Rewording batch 1 (2026-10-29): the 47 regular rows of Time & Work Rules 1-5 that copied the book get a fresh sentence and
all-new numbers (copyright - the owner's rule), new options, and an explanation regenerated with the same rule generator for
the new numbers. Row ids, rule links, days and times stay. The 6 Miscellaneous rows of these rules (266, 268, 269, 272, 277,
1682) are left for the Miscellaneous batch. Number sets were picked so that no book sentence holds the same set
(originality.Book.numbers_together). Writes reword/b1/ruleNN/2_new_rows.json; check with `python reword_check.py b1`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/b1
TW = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, TW)
sys.path.insert(0, os.path.dirname(HERE))
from rw_common import write_batch  # noqa: E402
from gen_1_4 import (b_from_pairs, c_as_ab, frac_then_help, from_fractions, k_works, men_for_days, separately,  # noqa: E402
                     stages3, then_c, together3, toys, trees, two, wmb)
from gen_5_10 import c_missing5, groups5, half5, three5, twice_thrice5  # noqa: E402

# rule -> [(row id, new question, generator call, unit of the answer)]
PLAN = {
    1: [(181, "A painting contract can be completed by 18 men in 14 days. If the client is happy to wait 36 days instead, how many "
              "men are enough for the job?", lambda: men_for_days(18, 14, 36), "men"),
        (1229, "Laying the floor tiles of a hall would keep 26 men busy for 9 days. The builder now wants to spread the same tiling "
               "over 18 days. How many men will he need?", lambda: men_for_days(26, 9, 18), "men"),
        (1233, "A drainage trench needs 6 days of digging by a gang of 35 men. If the council allows 14 days for it, how small can "
               "the gang be?", lambda: men_for_days(35, 6, 14), "men"),
        (182, "Felling trees for a new road, 20 men bring down 50 trees in a 5-hour shift. Next day 6 men are off sick. How many "
              "trees can the others bring down in a 9-hour shift?", lambda: trees(20, 50, 5, 6, 9), "trees"),
        (1230, "A clearing team of 16 men removes 36 trees in 9 hours. Tomorrow 4 men will be at another site; how many trees can "
               "be removed by the men left behind in 7 hours?", lambda: trees(16, 36, 9, 4, 7), "trees"),
        (1234, "Over a 5-hour morning shift, 24 men fell 40 trees. After lunch, 9 of them are moved to planting duty. Working at "
               "the same pace, what is the tree count the rest can fell in the next 8 hours?", lambda: trees(24, 40, 5, 9, 8), "trees"),
        (1235, "Processing 66 trees keeps a sawmill crew of 11 men busy for 3 hours. Once 7 of the men take the afternoon off, "
               "what number of trees can be processed in 5 hours by those still at work?", lambda: trees(11, 66, 3, 7, 5), "trees"),
        (183, "A needs 9 days to paint one room. At the same pace, how many days will A need to paint 4 rooms of the same size?",
         lambda: k_works(9, 4), "days"),
        (1231, "Tailor A stitches one batch of school uniforms in 6 days. How long will A take to stitch 5 such batches?",
         lambda: k_works(6, 5), "days"),
        (1236, "A can write one chapter of a report in 11 days. At this rate, how long will 3 chapters of equal length take A?",
         lambda: k_works(11, 3), "days")],
    2: [(184, "Making 14 toys takes 7 men 4 days at 9 hours a day. With 15 men available for only 3 hours a day, how long will an "
              "order of 25 toys take?", lambda: toys(7, 14, 4, 9, 15, 25, 3), "days"),
        (1238, "In a workshop, 10 men turn out 16 toys over 5 days, putting in 8 hours each day. If 25 men take on an order of 30 "
               "toys and work 5 hours a day, how many days will the order take?", lambda: toys(10, 16, 5, 8, 25, 30, 5), "days"),
        (1239, "A craft unit of 12 men turns out 40 toys in 6 days on a 5-hour daily shift. Another unit has 14 men on a 9-hour "
               "shift. How many days will it take them to make 70 toys?", lambda: toys(12, 40, 6, 5, 14, 70, 9), "days"),
        (185, "A woman would need 10 hours for a piece of stitching, a man 5 hours and a boy 20 hours. An order kept 10 men busy "
              "for 7 days at 5 hours a day. Suppose 4 men, 4 women and 4 boys share a repeat of the order at 5 hours a day; how "
              "many days will it take?", lambda: wmb(10, 5, 20, 5, 10, 7, 4, 5), "days"),
        (1237, "In 18 hours a woman finishes what a man finishes in 9 hours and a boy in 36 hours. Putting in 4 hours daily, 14 men "
               "complete a contract in 9 days. If 4 men, 4 women and 4 boys take on the same contract and put in 9 hours daily, how "
               "many days will they need?", lambda: wmb(18, 9, 36, 4, 14, 9, 4, 9), "days")],
    3: [(186, "Pairs of workers on a project report these times: A with B finish in 21 days, B with C in 24 days, and C with A in "
              "56 days. How many days would each of them need working alone?", lambda: separately(21, 24, 56), "days"),
        (1242, "Tiling a courtyard, the pair A-B needs 18 days, the pair B-C needs 20 days and the pair C-A needs 45 days. Find "
               "how long each of A, B and C would take if they worked alone.", lambda: separately(18, 20, 45), "days"),
        (187, "Working as pairs on a job, A with B would finish in 7 days, B with C in 8 days and C with A in 42 days. All three "
              "begin together; A is called away after 5 days, B carries on with C for 2 more days and is then called away too. "
              "How many days of C's work alone remain?", lambda: stages3(7, 8, 42, 5, 2), "days"),
        (1241, "A shed would take A and B 7 days as a pair, B and C 9 days, and C and A 18 days. Everyone works for the first 3 "
               "days; for the next 3 days only B and C work; after that C is on his own. How many days does C spend finishing "
               "the shed?", lambda: stages3(7, 9, 18, 3, 3), "days"),
        (1240, "Clearing a plot in pairs, A and B need 21 days, B and C need 28 days and C and A need 60 days. Suppose all three "
               "turn up together; how long will the clearing take?", lambda: together3(21, 28, 60), "days"),
        (1243, "Three gardeners keep a long hedge trimmed. When A and B share it they need 30 days; B and C need 45 days; C and "
               "A need 54 days. How long would the hedge take with all three trimming?", lambda: together3(30, 45, 54), "days")],
    4: [(188, "Working alone, A would need 10 days to repaint the benches in a park, while B would need 15. How long will the job "
              "take if they repaint them side by side?", lambda: two(10, 15), "days"),
        (1246, "A garden wall is a 14-day job for A and a 35-day job for B. Sharing it, how soon can they finish?",
         lambda: two(14, 35), "days"),
        (1248, "On his own, A can print a batch of posters in 20 days, and on her own B can print them in 30 days. How long will the "
               "batch take if both print at the same time?", lambda: two(20, 30), "days"),
        (1665, "A can type a thesis in 21 days and B in 42 days. If they split the typing and work at the same time, in how many "
               "days is the thesis done?", lambda: two(21, 42), "days"),
        (1247, "Paving a road would occupy 12 men for 18 days; alternatively, 16 women could pave it in 9 days. Working side by "
               "side, the 12 men and 16 women will finish in how many days?",
         lambda: two(18, 9, "the 12 men", "the 16 women",
                     lead=r"The 12 men finish the work in \(18\) days and the 16 women in \(9\) days. In one day:<br>"), "days"),
        (189, "Single-handed, A would take 20 days to paint a hall and B 10 days. A third painter, C, is as fast as A and B put "
              "together. If B teams up with C, how long will the painting take?", lambda: c_as_ab(20, 10), "days"),
        (1249, "A finishes a mural in 14 days and B in 28 days. C, on his own, works at the same speed as A and B working together. "
               "How long will B and C take as a team?", lambda: c_as_ab(14, 28), "days"),
        (190, r"Surveying alone, A covers \(\frac{5}{8}\) of the area in 20 days. Once B joins him, the remaining area is covered "
              "in 9 days. Had they started together, how many days would the full survey have taken?",
         lambda: frac_then_help("5/8", 20, 9), "days"),
        (1250, r"Working alone, A does \(\frac{4}{9}\) of a wiring job in 14 days. A and B then finish the remaining part together "
               "in 10 days. If they had worked together from the start, how long would the job have taken?",
         lambda: frac_then_help("4/9", 14, 10), "days"),
        (191, "Laying a pipeline would take A 24 days or B 40 days. The two work side by side for 9 days; C then lays the rest in "
              "8 days. Working alone from the start, how long would C have needed?", lambda: then_c(24, 40, 9, 8), "days"),
        (1663, "Painting a mural, A on his own would need 28 days and B on his own 21 days. After the two have painted side by side "
               "for 9 days, C takes over and needs 5 more days to complete it. How long would C have needed to paint the mural "
               "from scratch?", lambda: then_c(28, 21, 9, 5), "days"),
        (192, "Cleaning a fleet of buses takes A 6 hours alone, B and C as a pair 21 hours, and A and C as a pair 5 hours. On his "
              "own, how many hours would B spend on it?", lambda: b_from_pairs(6, 21, 5), "hours"),
        (1664, "Sorting a day's mail takes A 7 hours. B and C sorting together also take 7 hours, but A and C together need only 4 "
               "hours. How long would B need with nobody's help?", lambda: b_from_pairs(7, 7, 4), "hours"),
        (193, r"Painting a fence, A gets \(\frac{3}{4}\) of it done in 9 days, while B gets \(\frac{7}{8}\) of it done in 21 days. "
              "How many days will the fence take if they paint it together from the start?",
         lambda: from_fractions("3/4", 9, "7/8", 21), "days"),
        (1666, r"A gets through \(\frac{3}{8}\) of a project in 6 days, and B gets through \(\frac{11}{16}\) of it in 33 days. "
               "Sharing the project from day one, when will they finish?", lambda: from_fractions("3/8", 6, "11/16", 33), "days")],
    5: [(194, "Three painters A, B and C can each paint a hall alone in 8, 36 and 72 days. How long will the hall take if all "
              "three paint it at once?", lambda: three5(8, 36, 72), "days"),
        (1251, "A field could be harvested by A alone in 9 days, by B alone in 18 days or by C alone in 30 days. If the three "
               "harvest it together, how many days will it take?", lambda: three5(9, 18, 30), "days"),
        (1256, "Binding an order of books would take A 7 days, B 12 days and C 42 days if each worked alone. Working all at once, "
               "how long do they take?", lambda: three5(7, 12, 42), "days"),
        (1257, "A quilt would take A 8 days, B 33 days or C 88 days if each sewed it alone. If they sew it together, how long will "
               "it take?", lambda: three5(8, 33, 88), "days"),
        (195, "A could build a boat by himself in 9 days and B in 30 days. With C's help the three build it in 6 days. Alone, how "
              "long would C take?", lambda: c_missing5(9, 30, 6), "days"),
        (1252, "Alone, A needs 12 days to plaster a house and B needs 42 days. When C joins them, the house is plastered in 4 days. "
               "How long would C take by himself?", lambda: c_missing5(12, 42, 4), "days"),
        (196, "A works twice as fast as B, so A needs only half B's time for a job; C works as fast as A and B combined. Together "
              "the three finish the job in 5 days. How long would each of them take alone?", lambda: half5(5), "days"),
        (1253, "A takes half the time B takes to paint a wall. C is as quick as A and B put together. If the three paint the wall "
               "together in 9 days, find the number of days each needs alone.", lambda: half5(9), "days"),
        (197, "A job takes 2 hours if 15 men do it, 3 hours if 24 women do it, and 3 hours if 40 children do it. Working as a "
              "trio, 1 man, 1 woman and 1 child would need how many hours?", lambda: groups5(15, 2, 24, 3, 40, 3), "hours"),
        (1254, "Repairing a stretch of road is a 3-hour task for 10 men, a 3-hour task for 20 women and a 5-hour task for 36 "
               "children. If 1 man, 1 woman and 1 child repair it together, how long will they take?",
         lambda: groups5(10, 3, 20, 3, 36, 5), "hours"),
        (198, "Doing a job alone, A takes twice as long as B and three times as long as C. Working together, the three finish it "
              "in 5 days. How long would each need on his own?", lambda: twice_thrice5(5), "days")],
}


def main():
    write_batch(HERE, PLAN)


if __name__ == "__main__":
    main()
