"""Alligation rewording batch 2 (2026-10-30): the 36 rows of Rules 6-16 that fail the originality gate get all-new numbers and
a sentence in the book's simple style with the setting changed (the owner's style), new options, and an explanation
regenerated with the same rule generator (gen_5_10.py, gen_11_18.py) for the new numbers. Row ids, rule links, days and times
stay; rows that already pass the gate are left as they are. Numbers keep the order the rule solvers read them in, and each
sentence keeps the phrase its solver uses ("kilolitre", "water to milk", "each litre", "by bus?", "by train?", "ratio",
"respectively", "chickens and goats", "How many rabbits", "How many pigeons"); Rule 13 pair rows avoid the word "ratio".
Writes reword/b2/ruleNN/2_new_rows.json; check: `python reword_check.py b2`."""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # alligation/reword/b2
AL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, AL)
import rw_common  # noqa: E402
from gen_5_10 import journey, liquid, profit_loss, students, two_profits  # noqa: E402
from gen_11_18 import add_b, heads_legs, overall_loss, replace, savings, vessel  # noqa: E402

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
PL = ("Profit part", "loss part")

PLAN = {
    6: [(840, "There are 44 pupils in a class. Rs 28 is shared among them so that each boy gets 75 P and each girl gets 25 P. "
              "Find the number of boys and girls in the class.",
         lambda: students(44, 2800, 75, 25, "bg", r"Rs \(28 = 2800\) paise; each boy gets \(75\) paise and each girl \(25\) paise."),
         plain("Boys = 30, Girls = 14", "Boys = 34, Girls = 10", "Boys = 10, Girls = 34", "Boys = 32, Girls = 12"))],
    7: [(841, "A dealer has a cleaning liquid that costs Rs 72 per litre. In what ratio should he mix the liquid with water so "
              "that by selling the mixture at Rs 64 per litre he makes a profit of 60%?",
         lambda: liquid(72, 64, 60, "liquid", "lw", ""), ""),
        (1120, "A man buys milk at Rs 12 a litre, adds water and sells the mixture at Rs 12 a litre, making a profit of 20%. "
               "Find the ratio of milk to water in the mixture.", lambda: liquid(12, 12, 20, "milk", "lw", ""), ""),
        (1121, "A dairy buys milk at Rs 28 a litre and mixes it with water. By selling the mixture at Rs 18 a litre it gains "
               "50% on its cost. How much water is there in each litre of the mixture?",
         lambda: liquid(28, 18, 50, "milk", "per_litre", ""),
         plain(r"\(\frac{3}{7}\) litre", r"\(\frac{2}{7}\) litre", r"\(\frac{4}{7}\) litre", r"\(\frac{5}{7}\) litre")),
        (1122, "A milkman pays Rs 500 per kilolitre for his milk. He adds water and sells the mixture at 60 paise a litre, "
               "making a profit of 50% in all. Find the ratio of water to milk in what his customers get.",
         lambda: liquid(50, 60, 50, "milk", "wl", r"Rs \(500\) per kilolitre \(= \frac{50000}{1000} = 50\) paise per litre.", "paise"), ""),
        (1123, "A shop has a liquid soap that costs Rs 70 per litre. It is mixed with water and the mixture is sold at Rs 63 "
               "per litre for a profit of 40%. Find the ratio of soap to water.", lambda: liquid(70, 63, 40, "liquid soap", "lw", ""), "")],
    8: [(842, "A family travels 275 km in 7 hours in two parts. First they go by bus at 25 km per hour, and then by train at "
              "50 km per hour. How far did they travel by train?", lambda: journey(275, 7, 25, 50, "train"), "km"),
        (1125, "A salesman covers 210 km in 4 hours in two parts. He first goes by bus at 45 km/hr and then by train at 75 "
               "km/hr. How far did he travel by bus?", lambda: journey(210, 4, 45, 75, "bus"), "km"),
        (1126, "A student travels 250 km in 6 hours in two parts, first by bus at 40 km/hr and then by train at 45 km/hr. How "
               "far did she travel by train?", lambda: journey(250, 6, 40, 45, "train"), "km"),
        (1127, "A tourist covers 170 km in 5 hours in two parts, first by bus at 30 km/hr and then by train at 45 km/hr. What "
               "is the ratio of the distance by bus to the distance by train?", lambda: journey(170, 5, 30, 45, "ratio"), ""),
        (1128, "Travelling 340 km in 8 hours, a woman goes part of the way by bus at 30 km/hr and the rest by train at 60 "
               "km/hr. Find the distances she covered by bus and by train, respectively.", lambda: journey(340, 8, 30, 60, "both"),
         "km", ("Bus", "train"))],
    9: [(843, "A grocer has 45 kg of sugar. He sells part of it at 13% profit and the rest at 43% profit, and gains 25% on the "
              "whole. How much sugar did he sell at 43% profit?", lambda: two_profits(45, 13, 43, 25, "sugar"), "kg"),
        (1129, "A shopkeeper has 35 kg of lentils. He sells part of it at 12% profit and the rest at 27% profit, and gains 18% "
               "on the whole. How many kg did he sell at 27% profit?", lambda: two_profits(35, 12, 27, 18, "lentils"), "kg"),
        (1130, "A dealer has 80 kg of flour. Part of it is sold at 13% profit and the rest at 37% profit, giving a gain of 19% "
               "on the whole. What quantity is sold at 37% profit?", lambda: two_profits(80, 13, 37, 19, "flour"), "kg"),
        (1131, "A merchant has 65 kg of maize. He sells part of it at 20% profit and the rest at 35% profit, and gains 32% on "
               "the whole. How much maize did he sell at 35% profit?", lambda: two_profits(65, 20, 35, 32, "maize"), "kg"),
        (1132, "A trader has 50 kg of peas. He sells part of them at 17% profit and the rest at 32% profit, and gains 23% on "
               "the whole. How many kg did he sell at 32% profit?", lambda: two_profits(50, 17, 32, 23, "peas"), "kg")],
    10: [(844, "A grocer has 70 kg of sugar. He sells part of it at 25% profit and the rest at 3% loss, and gains 9% on the "
               "whole. How much did he sell at 25% profit and how much at 3% loss?",
          lambda: profit_loss(70, 25, 3, 9, "sugar"), "kg", PL),
         (1133, "A shopkeeper has 45 kg of flour. He sells part of it at 32% profit and the rest at 13% loss, and gains 21% on "
                "the whole. How much did he sell at a profit and how much at a loss?",
          lambda: profit_loss(45, 32, 13, 21, "flour"), "kg", PL),
         (1134, "A dealer has 20 kg of tea. Part of it is sold at 29% profit and the rest at 11% loss, giving a gain of 17% on "
                "the whole. How much tea is sold at a profit and how much at a loss?",
          lambda: profit_loss(20, 29, 11, 17, "tea"), "kg", PL),
         (1135, "A merchant has 85 kg of lentils. He sells part of it at 24% profit and the rest at 10% loss, and gains 14% on "
                "the whole. How much did he sell at a profit and how much at a loss?",
          lambda: profit_loss(85, 24, 10, 14, "lentils"), "kg", PL),
         (1136, "A trader has 80 kg of maize. He sells part of it at 31% profit and the rest at 9% loss, and gains 7% on the "
                "whole. How much did he sell at a profit and how much at a loss?",
          lambda: profit_loss(80, 31, 9, 7, "maize"), "kg", PL)],
    11: [(1138, r"A grocer has 55 kg of sugar. He sells part of it at \(13\%\) profit and the rest at \(20\%\) loss, and on the "
                r"whole he loses \(14\%\). How much did he sell at a profit and how much at a loss?",
          lambda: overall_loss(55, 13, 20, 14), "kg", PL)],
    12: [(1141, r"Anil's spending and saving are in the ratio \(5:2\). His income goes up by \(27\%\) and his spending goes up "
                r"by \(29\%\). By what percent does his saving go up?", lambda: savings(5, 2, 27, 29, "Anil"),
          plain("20%", "22%", "24%", "18%"))],
    13: [(1145, "A tank of 160 litres is full of milk and water. 64% of the milk and 32% of the water are drawn out, and the "
                "tank is then 52% empty. What is the ratio of milk to water in the tank?",
          lambda: vessel(160, 64, 32, 52, "ratio"), ""),
         (1146, "A tank of 130 litres is full of milk and water. 79% of the milk and 44% of the water are drawn out, and the "
                "tank is then 65% empty. How much milk and how much water did the tank hold at first?",
          lambda: vessel(130, 79, 44, 65, "pair"), "litres", ("Milk", "water")),
         (1147, "A drum of 170 litres is full of milk and water. 85% of the milk and 51% of the water are drawn out, and the "
                "drum is then 65% empty. How much milk and how much water did the drum hold at first?",
          lambda: vessel(170, 85, 51, 65, "pair"), "litres", ("Milk", "water"))],
    14: [(1148, r"On a farm there are chickens and goats. Counting heads gives \(148\) and counting legs gives \(364\). How "
                r"many chickens and goats are there on the farm?",
          lambda: heads_legs(148, 364, "goats", "chickens", "pair"),
          plain("34 chickens, 114 goats", "114 chickens, 34 goats", "104 chickens, 44 goats", "118 chickens, 30 goats")),
         (1149, r"A pet shop has rabbits and pigeons. There are \(135\) heads and \(440\) legs. How many rabbits are there?",
          lambda: heads_legs(135, 440, "rabbits", "pigeons", "four"), "rabbits"),
         (1150, r"A pet shop has rabbits and pigeons. There are \(113\) heads and \(310\) legs. How many pigeons are there?",
          lambda: heads_legs(113, 310, "rabbits", "pigeons", "two"), "pigeons")],
    15: [(1152, r"A tank holds liquids A and B in the ratio \(3:2\). When \(15\) litres of the mixture are taken out and \(18\) "
                r"litres of liquid B are poured in, the ratio becomes \(15:28\). How many litres of liquid A were in the tank "
                r"at first?", lambda: replace(3, 2, 15, 18, 15, 28), "litres"),
         (1153, r"A drum holds liquids A and B in the ratio \(7:3\). When \(20\) litres of the mixture are taken out and "
                r"replaced by \(20\) litres of liquid B, the ratio changes to \(21:29\). How many litres of liquid A were in "
                r"the drum at first?", lambda: replace(7, 3, 20, 20, 21, 29), "litres"),
         (1154, r"A jar holds liquids A and B in the ratio \(8:1\). When \(9\) litres of the mixture are drawn off and the jar "
                r"is filled up with liquid B, the ratio of A to B becomes \(2:1\). How many litres of liquid A were in the "
                r"jar at first?", lambda: replace(8, 1, 9, 9, 2, 1), "litres")],
    16: [(1155, r"In a can there are 56 litres of milk and water mixed in the ratio \(5:2\). How many litres of water should be "
                r"poured in so that milk and water are in the ratio \(2:3\)?", lambda: add_b(56, 5, 2, 2, 3), "litres"),
         (1156, r"In a jug there are 80 litres of juice and water mixed in the ratio \(7:1\). How many litres of water should be "
                r"poured in so that juice and water are in the ratio \(7:3\)?", lambda: add_b(80, 7, 1, 7, 3), "litres"),
         (1157, r"In a pot there are 54 litres of milk and water mixed in the ratio \(8:1\). How many litres of water should be "
                r"poured in so that milk and water are in the ratio \(8:3\)?", lambda: add_b(54, 8, 1, 8, 3), "litres"),
         (1158, r"In a barrel there are 150 litres of syrup and water mixed in the ratio \(9:1\). How many litres of water should "
                r"be poured in so that syrup and water are in the ratio \(9:2\)?", lambda: add_b(150, 9, 1, 9, 2), "litres")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
