"""Rewording batch 3 (2026-10-29): the 51 regular rows of Time & Work Rules 11-20 that copied the book get a fresh sentence
and all-new numbers (copyright - the owner's rule), new options, and an explanation regenerated with the same rule generator
for the new numbers. Row ids, rule links, days and times stay. The Miscellaneous rows of these rules (271, 274) are left for
the Miscellaneous batch; 1292, 1296, 1306, 1311 and 1323 were done in the pilot. Number sets were picked so that no book
sentence holds the same set (originality.Book.numbers_together). Writes reword/b3/ruleNN/2_new_rows.json; check:
`python reword_check.py b3`."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # reword/b3
sys.path.insert(0, os.path.dirname(HERE))
from rw_common import write_batch  # noqa: E402
from gen_11_20 import (a_alone16, absent18, builder20, c_ab13, extra19, faster11, good14, hours12,  # noqa: E402
                       left16, mwb17, times15)

PLAN = {
    11: [(219, "B needs 30 days more than A to finish a job, because A works 4 times as fast as B. Working together, in how many "
               "days will they finish it?", lambda: faster11(4, 30), "days"),
         (1290, "A works 3 times as quickly as B, and so, working alone, B ends up 40 days behind A in completing an order. If they "
                "share the order, how many days will it take?", lambda: faster11(3, 40), "days"),
         (1291, "Since A is 2 times as quick as B, A completes a survey 27 days ahead of B when each works alone. How many days "
                "will the survey take if A and B do it together?", lambda: faster11(2, 27), "days"),
         (1293, "A finishes a task 48 days sooner than B, as A works at 5 times B's speed. Find the number of days the two need "
                "for the task when working as a team.", lambda: faster11(5, 48), "days"),
         (1294, "A gets 3 times as much work done per day as B, so A finishes a repair job 32 days before B would. In how many "
                "days can they finish it jointly?", lambda: faster11(3, 32), "days")],
    12: [(220, "I can paint a house in 16 days if I work 3 hours a day; you can paint it in 20 days working 4 hours a day. If the "
               "two of us paint together for 5 hours a day, how many days will the house take?",
               lambda: hours12(16, 3, 20, 4, 5), "days"),
         (1295, "Putting in 7 hours a day, I would knit a set of shawls in 12 days, while you would need 21 days at 3 hours a "
                "day. Working side by side for 6 hours a day, in how many days do we finish the set?",
                lambda: hours12(12, 7, 21, 3, 6), "days"),
         (1297, "At 9 hours a day I would finish binding an order of books in 10 days, and at 6 hours a day you would finish it "
                "in 12 days. If we bind together for 5 hours a day, how many days will the order take?",
                lambda: hours12(10, 9, 12, 6, 5), "days"),
         (1298, "I need 12 days to plaster a hall when I work 3 hours a day, and you need 21 days when you work 4 hours a day. "
                "How many days will the plastering take if we work together 9 hours a day?",
                lambda: hours12(12, 3, 21, 4, 9), "days")],
    13: [(221, "A takes 12 days and B takes 24 days to print a batch of posters. C alone takes as long as A and B together "
               "would. If A, B and C all work on the batch, how many days will it take?", lambda: c_ab13(12, 24, "abc"), "days"),
         (1299, "A would take 30 days to plant a vineyard and B would take 15 days. C needs exactly as long as A and B need when "
                "they work as a pair. In how many days will B and C plant the vineyard together?",
                lambda: c_ab13(30, 15, "bc"), "days"),
         (1300, "To service a fleet of buses, A needs 14 days and B needs 28 days. Working alone, C would take the same time "
                "that A and B take together. How long will the pair B and C take?", lambda: c_ab13(14, 28, "bc"), "days"),
         (1301, "A alone can catalogue a library in 15 days, B alone in 6 days. C, working by himself, matches the time of A "
                "and B working jointly. How many days will A and C take if they catalogue it together?",
                lambda: c_ab13(15, 6, "ac"), "days"),
         (1302, "Tiling a courtyard is a 14-day job for A and a 21-day job for B. Left to himself, C needs the same number of days "
                "that A and B would need as a team. If A and C tile the courtyard as a pair, how many days will it take?",
                lambda: c_ab13(14, 21, "ac"), "days"),
         (1303, "A could dig a section of canal in 21 days and B in 28 days, while C alone needs the time that A and B need "
                "jointly. How long will A, B and C take working together?", lambda: c_ab13(21, 28, "abc"), "days"),
         (1304, "A can repaint a ship's hull in 15 days and B in 20 days. Working alone, C would match the combined time of A "
                "and B. How many days will A, B and C need with all three working?", lambda: c_ab13(15, 20, "abc"), "days")],
    14: [(222, "A does 3 times as much work in a day as B. Working together they can lay a pipeline in 9 days. How many days "
               "would each of them need to lay it alone?", lambda: good14(3, 9, both=True), "days"),
         (1305, "A is twice as productive as B, and together the two finish packing an order in 16 days. How many days would A "
                "take to pack it by himself?", lambda: good14(2, 16), "days"),
         (1307, "Varnishing a set of doors keeps A and B busy for 15 days when they share it. Hour for hour, A's output is 3 times "
                "B's output. How many days would A need to varnish the doors with no help?", lambda: good14(3, 15), "days"),
         (1308, "A and B finish weaving a rug together in 8 days. In any given time A weaves 4 times as much as B. Find the "
                "number of days A would need to weave the rug without help.", lambda: good14(4, 8), "days"),
         (1309, "Working together, A and B can repair a bridge in 18 days. A does twice the work B does in an hour. In how many "
                "days could A repair it alone?", lambda: good14(2, 18), "days"),
         (1310, "A, who works 5 times as fast as B, teams up with B and they finish a mural in 10 days. How many days would A "
                "need to paint the mural on his own?", lambda: good14(5, 10), "days")],
    15: [(223, "A gang of 9 men and 3 boys completes, in one hour, 7 times the work that 1 man and 1 boy finish as a pair in that "
               "hour. What is the ratio of the work of one man to the work of one boy?", lambda: times15(9, 3, 7), ""),
         (1312, "Hour for hour, a squad of 13 men and 3 boys produces 11 times the output of a pair made up of 1 man and 1 boy. "
                "Express the output of one man and the output of one boy as a ratio.", lambda: times15(13, 3, 11), "")],
    16: [(224, "A can build a garden wall in 28 days and B in 20 days. They start together, A walks off the job partway "
               "through, and B finishes the wall alone in a further 8 days. How many days after the start did A leave?",
               lambda: left16(28, 20, 8), "days"),
         (225, "A and B together could restore an old house in 60 days. After 15 days of joint work B leaves, and A takes "
               "another 27 days to finish. How many days would A need to restore the whole house alone?",
               lambda: a_alone16(60, 15, 27), "days"),
         (1313, "Working alone, A would plough a field in 22 days, B in 44 days. Both plough from the first day until A is "
                "called away; B then needs 14 more days to finish. For how many days did A plough?",
                lambda: left16(22, 44, 14), "days"),
         (1314, "Translating a novel would take A 36 days and B 45 days. Both translate side by side at first; once A withdraws, B "
                "needs a further 27 days to complete the novel. For how many days were the two working together?",
                lambda: left16(36, 45, 27), "days"),
         (1315, "A alone needs 32 days and B alone needs 56 days to wire a factory. The two start together; when A is "
                "transferred, B spends 12 more days finishing. How long did A work?", lambda: left16(32, 56, 12), "days"),
         (1316, "A takes 18 days and B takes 42 days to pave a road on their own. They pave together until A quits, and B "
                "completes the remaining part in 17 days. How many days did A work?", lambda: left16(18, 42, 17), "days"),
         (1317, "Working as a pair, A and B could print a book in 70 days. They print for 49 days together; then B stops and A "
                "finishes the printing in 9 more days. How long would A take to print the book alone?",
                lambda: a_alone16(70, 49, 9), "days")],
    17: [(226, "Building a boundary fence would occupy 1 man for 28 days, and it would occupy 2 women, or 4 boys, for exactly as "
               "long. How many days do they need if a trio of 1 man, 1 woman and 1 boy builds it?", lambda: mwb17(1, 2, 4, 28), "days"),
         (1318, "Clearing a plot of scrubland is a 26-day task whether it is given to 1 man, to a group of 3 women or to a group of 9 "
                "boys. Find the number of days the plot takes when 1 man, 1 woman and 1 boy clear it side by side.",
                lambda: mwb17(1, 3, 9, 26), "days"),
         (1319, "Repairing all the seats of a stadium takes 55 days for 1 man working alone; 4 women or 8 boys would need the "
                "same time. How many days does a team of 1 man, 1 woman and 1 boy need?", lambda: mwb17(1, 4, 8, 55), "days"),
         (1320, "Stitching a large tent keeps 1 man busy for 31 days; a team of 3 women would also take 31 days, and so would a team "
                "of 7 boys. If the tent is stitched by 1 man, 1 woman and 1 boy sharing the work, how many days are needed?",
                lambda: mwb17(1, 3, 7, 31), "days"),
         (1321, "Painting a long fence takes 35 days for 1 man, and the same time for 3 women or for 8 boys. In how many days "
                "can 1 man, 1 woman and 1 boy paint it working together?", lambda: mwb17(1, 3, 8, 35), "days")],
    18: [(227, "A foreman planned to complete a job in 18 days with a certain gang of men. 9 of the men fell ill, and the rest "
               "took 45 days to complete it. How many men were in the gang at first?", lambda: absent18(18, 9, 45), "men"),
         (1322, "A road crew was meant to finish a stretch of road in 24 days, but 5 of its men left on the first day. The "
                "remaining men finished the stretch in 30 days. How many men were in the crew originally?",
                lambda: absent18(24, 5, 30), "men"),
         (1324, "Some men agreed to finish a job in 13 days. Since 19 of them did not report for work, the others needed 26 "
                "days. What was the original number of men?", lambda: absent18(13, 19, 26), "men"),
         (1325, "A team of men was hired to complete a project in 35 days. 5 men dropped out before it began, so the project "
                "took 42 days. How many men were hired at first?", lambda: absent18(35, 5, 42), "men")],
    19: [(228, "Working at a steady pace, a gang finishes a drainage job in 35 days. Had the foreman added 6 men, the same job "
               "would have ended 5 days earlier. How large is the gang?", lambda: extra19(35, 6, 5), "men"),
         (1326, "Some men can complete a building in 72 days. Adding 9 men would cut the time by 18 days. Find the original "
                "number of men.", lambda: extra19(72, 9, 18), "men"),
         (1327, "A certain crew finishes laying a railway line in 80 days. If 8 men joined the crew, the line would be laid 20 "
                "days sooner. How many men are in the crew?", lambda: extra19(80, 8, 20), "men"),
         (1328, "A group of men can dig a reservoir in 35 days. If the group had 10 more men, the digging would finish 14 days "
                "earlier. How many men are in the group?", lambda: extra19(35, 10, 14), "men"),
         (1329, "A team takes 63 days to finish a contract. 4 extra men would let it finish 7 days ahead of that. How many men "
                "does the team have?", lambda: extra19(63, 4, 7), "men")],
    20: [(229, "A bridge was due in 90 days. Its contractor kept 120 men on the site from the start, took on 60 more after 70 "
               "days, and met the deadline exactly. By how many days would the bridge have been late if those 60 had never "
               "joined?", lambda: builder20(90, 120, 60, 70), "days"),
         (1330, "A school building had to be ready in 27 days. The builder put 100 men to work, added 150 more after 21 days, "
                "and handed it over on the due date. Had the extra men never been hired, by how many days would the work have "
                "been late?", lambda: builder20(27, 100, 150, 21), "days"),
         (1331, "A hospital wing was to be built in 46 days. Work began with 150 men, a further 250 joined after 40 days, and "
                "the wing was finished on schedule. How many days behind schedule would it have been with only the first "
                "men?", lambda: builder20(46, 150, 250, 40), "days"),
         (1332, "A firm agreed to lay a highway in 41 days. It began with 120 men and sent in 40 more after 17 days, finishing "
                "exactly on the agreed day. Had the first men worked alone, how many days would the whole highway have "
                "taken?", lambda: builder20(41, 120, 40, 17, delay=False), "days"),
         (1333, "A stadium was to be completed in 45 days. The contractor used 130 men at first and brought in 260 more after "
                "39 days, so the stadium was ready on time. If no extra men had come, how many days late would it have "
                "been?", lambda: builder20(45, 130, 260, 39), "days"),
         (1334, "A dam had to be raised in 54 days. Work started with 120 men, 60 more were added after 22 days, and the job "
                "ended on the planned day. How many days in all would the first men have needed on their own?",
                lambda: builder20(54, 120, 60, 22, delay=False), "days")],
}

if __name__ == "__main__":
    write_batch(HERE, PLAN)
