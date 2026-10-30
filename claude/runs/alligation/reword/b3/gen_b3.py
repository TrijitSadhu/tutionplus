"""Alligation rewording batch 3 (2026-10-30): the 22 rows of Rules 17-22 that fail the originality gate get all-new numbers and
a sentence in the book's simple style with the setting changed (the owner's style), new options, and an explanation
regenerated with the same rule generator (gen_11_18.py, gen_19_28.py) for the new numbers. Row ids, rule links, days and times
stay; rows that already pass the gate are left as they are. What the solvers read: Rule 17 only the mixture ratios (a:b) or the
percentages written \(p\%\); Rule 19 every "<n> litres" as a vessel size, the ratios, plain "p%" percentages and
"<n> litres of water is added"; Rule 21 the first three ratios, or "whisky" + three numbers; Rules 18, 20, 22 the numbers in order.
Writes reword/b3/ruleNN/2_new_rows.json; check: `python reword_check.py b3`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # alligation/reword/b3
AL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, AL)
import rw_common  # noqa: E402
from gen_11_18 import alloys, equal_glasses  # noqa: E402
from gen_19_28 import P, PCT, remaining_rate, sizes_mix, two_alloys, water_avg, whisky_replaced  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))

PLAN = {
    17: [(1159, r"Three jugs, each holding 16 litres, are filled with milk and water. The ratios of milk to water in them are "
                r"\(3:2\), \(9:1\) and \(11:9\). If all three jugs are poured into one large pot, what is the ratio of milk to "
                r"water in the pot?", lambda: equal_glasses([(3, 2), (9, 1), (11, 9)], "milk", "water", r"The jugs hold \(16\) litres each."), ""),
         (1160, r"Three equal cups are filled with spirit and water. The ratio of spirit to water is \(2:3\) in the first cup, "
                r"\(3:7\) in the second and \(1:9\) in the third. If the three cups are emptied into one bowl, find the ratio "
                r"of spirit to water in the bowl.", lambda: equal_glasses([(2, 3), (3, 7), (1, 9)], "spirit", "water"), ""),
         (1161, r"Three equal bottles hold juice and water. The ratio of juice to water is \(5:1\) in the first bottle, \(7:1\) "
                r"in the second and \(2:1\) in the third. If all three are mixed in one jar, what is the ratio of juice to water "
                r"in the jar?", lambda: equal_glasses([(5, 1), (7, 1), (2, 1)], "juice", "water"), ""),
         (1162, r"Four tanks of the same size hold spirit and water. The strength of spirit in the tanks is \(55\%\), \(70\%\), "
                r"\(90\%\) and \(45\%\). If all four are mixed together, find the ratio of spirit to water in the mixture.",
          lambda: equal_glasses([(55, 45), (70, 30), (90, 10), (45, 55)], "spirit", "water",
                                r"A strength of \(55\%\) means spirit : water \(= 55 : 45\), and so on."), ""),
         (1163, r"Two equal cups hold syrup and water in the ratios \(5:3\) and \(7:1\). Both are poured into a third cup. What "
                r"is the ratio of syrup to water in the third cup?", lambda: equal_glasses([(5, 3), (7, 1)], "syrup", "water"), "")],
    18: [(1164, r"If \(9\) kg of an alloy, of which \(\frac{1}{6}\) is tin and the rest lead, is melted with \(6\) kg of another "
                r"alloy, of which \(\frac{1}{2}\) is tin and the rest lead, what is the ratio of tin to lead in the new alloy?",
          lambda: alloys(9, F(1, 6), 6, F(1, 2)), "")],
    19: [(1168, r"Three jars of 12 litres, 18 litres and 24 litres hold spirit and water in the ratios \(1:2\), \(2:1\) and "
                r"\(1:3\). All three jars are emptied into one tank. Find the ratio of spirit to water in the tank.",
          lambda: sizes_mix([12, 18, 24], [(1, 2), (2, 1), (1, 3)], "spirit", "water"), ""),
         (1169, r"Two barrels of 40 litres and 90 litres hold juice and water in the ratios \(3:1\) and \(4:5\). The two are "
                r"mixed, and then 20 litres of water is added. What is the ratio of juice to water now?",
          lambda: sizes_mix([40, 90], [(3, 1), (4, 5)], "juice", "water", 20), ""),
         (1170, "Three cans of 5 litres, 8 litres and 12 litres hold milk and water, with milk making up 60%, 75% and 50% of "
                "them. All three are emptied into a big drum. Find the ratio of milk to water in the drum.",
          lambda: sizes_mix([5, 8, 12], P(60, 75, 50), "milk", "water", pct_text=PCT), ""),
         (1171, r"Four bottles of 12 litres, 20 litres, 33 litres and 16 litres hold milk and water in the ratios \(1:2\), \(3:1\), "
                r"\(2:1\) and \(1:3\). Find the ratio of milk to water when all four bottles are poured into one vessel.",
          lambda: sizes_mix([12, 20, 33, 16], [(1, 2), (3, 1), (2, 1), (1, 3)], "milk", "water"), ""),
         (1172, "Three pots of 12 litres, 24 litres and 32 litres hold milk and water, with milk making up 45%, 70% and 40% of "
                "them. If all three are mixed, what is the ratio of milk to water?",
          lambda: sizes_mix([12, 24, 32], P(45, 70, 40), "milk", "water", pct_text=PCT), "")],
    20: [(1173, r"A dairy mixes 9 kilolitres of milk at Rs \(8000\) per kilolitre with 8 kilolitres at Rs \(9000\) per kilolitre, "
                r"and adds enough water to bring the average value to Rs \(4500\) per kilolitre. How many kilolitres of water "
                r"does it add?", lambda: water_avg(9, 8000, 8, 9000, 4500), "kilolitres"),
         (1174, r"A dairy mixes 10 kilolitres of milk at Rs \(700\) per kilolitre with 4 kilolitres at Rs \(500\) per kilolitre, "
                r"and adds enough water to bring the average value to Rs \(450\) per kilolitre. How many kilolitres of water "
                r"does it add?", lambda: water_avg(10, 700, 4, 500, 450), "kilolitres"),
         (1175, r"A dairy mixes 9 kilolitres of milk at Rs \(640\) per kilolitre with 3 kilolitres at Rs \(800\) per kilolitre, "
                r"and adds enough water to bring the average value to Rs \(600\) per kilolitre. How many kilolitres of water "
                r"does it add?", lambda: water_avg(9, 640, 3, 800, 600), "kilolitres")],
    21: [(1176, r"In one alloy, tin and lead are in the ratio \(1:2\). In another alloy they are in the ratio \(3:1\). In what "
                r"ratio should the two alloys be melted together to get an alloy with tin and lead in the ratio \(3:2\)?",
          lambda: two_alloys((1, 2), (3, 1), (3, 2)), ""),
         (1177, r"In one alloy, tin and lead are in the ratio \(1:10\). In another alloy they are in the ratio \(8:3\). In what "
                r"ratio should the two alloys be melted together to get an alloy with tin and lead in the ratio \(1:3\)?",
          lambda: two_alloys((1, 10), (8, 3), (1, 3)), ""),
         (1178, r"In one alloy, tin and lead are in the ratio \(1:2\). In another alloy they are in the ratio \(1:9\). In what "
                r"ratio should the two alloys be melted together to get an alloy with tin and lead in the ratio \(2:11\)?",
          lambda: two_alloys((1, 2), (1, 9), (2, 11)), ""),
         (1179, r"In one alloy, tin and lead are in the ratio \(2:3\). In another alloy they are in the ratio \(7:3\). In what "
                r"ratio should the two alloys be melted together to get an alloy with equal amounts of tin and lead, \(1:1\)?",
          lambda: two_alloys((2, 3), (7, 3), (1, 1)), ""),
         (1180, r"A bottle full of whisky has \(50\%\) alcohol. Some of this whisky is replaced by another whisky with \(26\%\) "
                r"alcohol, and now the alcohol is \(35\%\). What part of the whisky was replaced?",
          lambda: whisky_replaced(50, 26, 35), plain(r"\(\frac{3}{8}\)", r"\(\frac{1}{2}\)", r"\(\frac{3}{5}\)", r"\(\frac{5}{8}\)"))],
    22: [(1181, "Sunita bought 150 kg of lentils at Rs 16 per kg. She sold 50 kg at a profit of 10%. At what price per kg "
                "should she sell the rest to make a profit of 30% on the whole?",
          lambda: remaining_rate(150, 16, 50, 10, 30, "Sunita", "lentils"), plain("Rs 22.40", "Rs 20.80", "Rs 21.60", "Rs 23.20")),
         (1182, "Asha bought 90 kg of sugar at Rs 24 per kg and first sold 30 kg of it at a profit of 15%. At what price per kg "
                "must she sell the rest to make a profit of 25% on the whole deal?",
          lambda: remaining_rate(90, 24, 30, 15, 25, "Asha", "sugar"), plain("Rs 30.00", "Rs 31.20", "Rs 32.40", "Rs 29.60")),
         (1183, "Nisha bought 80 kg of flour at Rs 15 per kg. She sold 30 kg at a profit of 12%. At what price per kg should she "
                "sell the rest to make a profit of 24% on the whole?",
          lambda: remaining_rate(80, 15, 30, 12, 24, "Nisha", "flour"), plain("Rs 19.68", "Rs 18.60", "Rs 20.40", "Rs 19.20"))],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
