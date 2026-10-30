"""Alligation rewording batch 4 (2026-10-30): the 31 rows of Rules 23-29 that fail the originality gate get all-new numbers and
a sentence in the book's simple style with the setting changed (the owner's style), new options, and an explanation
regenerated with the same rule generator (gen_19_28.py, rule29/gen.py) for the new numbers. Row ids, rule links, days and times
stay; rows that already pass the gate are left as they are. Numbers keep the order the solvers read them in (Rule 24 rows 1192,
1194, 1195 have their own orders); Rule 23 keeps "<n> parts <liquid>" and "replaced with <liquid>", Rule 27 "lotion".
`released` / `capacity` look the square root up in a small table, so their new ratios come from that table. Rule 28 uses a new
solver (b4/solve28_rw.py, loaded by b4/rule28/solve.py) that reads "<n> times in all" and the fraction words, so the numbers there can change too.
Writes reword/b4/ruleNN/2_new_rows.json; check: `python reword_check.py b4`."""
import importlib.util, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # alligation/reword/b4
AL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, AL)
import rw_common  # noqa: E402
from gen_19_28 import blend_pct, half_half, left_after, lotion, lower_price, released, weights  # noqa: E402

_s = importlib.util.spec_from_file_location("gen_rule29", os.path.join(AL, "rule29", "gen.py"))
g29 = importlib.util.module_from_spec(_s); _s.loader.exec_module(g29)

rw_common.NOTE = ("question rewritten in the book's simple style (setting changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
fr = lambda a, b: rf"\(\frac{{{a}}}{{{b}}}\)"

PLAN = {
    23: [(1187, "A jug holds 9 parts juice and 7 parts water. What part of the mixture should be taken out and replaced with "
                "water so that the jug holds half juice and half water?", lambda: half_half(9, 7, "juice", "water"),
          plain(fr(1, 9), fr(1, 7), fr(2, 9), fr(1, 8))),
         (1188, "A tank holds 11 parts milk and 9 parts water. What part of the mixture should be taken out and replaced with "
                "water so that the tank holds half milk and half water?", lambda: half_half(11, 9, "milk", "water"),
          plain(fr(1, 9), fr(1, 11), fr(2, 11), fr(1, 10))),
         (1189, "A can holds 8 parts milk and 1 part water. What part of the mixture should be taken out and replaced with "
                "water so that the can holds half milk and half water?", lambda: half_half(8, 1, "milk", "water"),
          plain(fr(3, 8), fr(9, 16), fr(7, 16), fr(5, 16)))],
    24: [(1190, "How much water must be added to a can holding 40 litres of milk that costs Rs 7.50 a litre so that the cost "
                "comes down to Rs 6.00 a litre?", lambda: lower_price(40, "7.50", "6.00", "litres", "milk", "water"), "litres"),
         (1191, "A dairy has 24 kilolitres of milk worth Rs 9.60 a litre. How much water should it add so that the mixture is "
                "worth Rs 7.20 a litre?", lambda: lower_price(24, "9.60", "7.20", "kilolitres", "milk", "water"), "kilolitres"),
         (1192, r"How much water should be added to 54 litres of milk bought at \(1\frac{1}{4}\) litres for Rs 15 so that the "
                r"mixture is worth Rs 9 per litre?",
          lambda: lower_price(54, 12, 9, "litres", "milk", "water",
                              price_note=r"\(1\frac{1}{4}\) litres for Rs \(15\) means Rs \(15\div 1\frac{1}{4} = 12\) per litre."), "litres"),
         (1193, "How much water must be added to a drum holding 45 litres of spirit worth Rs 14.40 a litre to bring the price "
                "down to Rs 12 a litre?", lambda: lower_price(45, "14.40", 12, "litres", "spirit", "water"), "litres"),
         (1194, "Chicory costs Rs 20 a kg. If it is mixed with 12 kg of coffee costing Rs 90 a kg, how much chicory will make "
                "the mixture worth Rs 60 a kg?", lambda: lower_price(12, 90, 60, "kg", "coffee", "chicory", 20), "kg"),
         (1195, "How many oranges at 4 for Rs 2 should be mixed with 240 oranges at 6 for Rs 4.50 so that all of them are worth "
                "Rs 7.20 a dozen?",
          lambda: lower_price(240, "0.75", "0.60", "oranges", "oranges", "the cheaper oranges", "0.50",
                              r"Price per orange: \(4.50\div 6 = 0.75\), \(2\div 4 = 0.50\), and Rs \(7.20\) a dozen \(= 0.60\).", count=True),
          "oranges")],
    25: [(1197, r"One liquid has \(18\%\) water and another has \(30\%\) water. A jar is filled with \(1\) part of the first "
                r"liquid and \(2\) parts of the second. What is the percentage of water in the jar?",
          lambda: blend_pct(18, 30, 1, 2, "water"), plain("24%", "26%", "28%", "25%")),
         (1198, r"One liquid has \(15\%\) milk and another has \(25\%\) milk. A can is filled with \(3\) parts of the first and "
                r"\(2\) parts of the second. Find the percentage of milk in the can.",
          lambda: blend_pct(15, 25, 3, 2, "milk"), plain("20%", "19%", "21%", "18%")),
         (1199, r"One liquid has \(11\%\) milk and another has \(29\%\) milk. A bottle is filled with \(4\) parts of the first and "
                r"\(2\) parts of the second. Find the percentage of milk in the bottle.",
          lambda: blend_pct(11, 29, 4, 2, "milk"), plain("18%", "16%", "20%", "17%")),
         (1200, r"One liquid has \(6\%\) milk and another has \(15\%\) milk. A cup is filled with \(1\) part of the first and \(2\) "
                r"parts of the second. Find the percentage of milk in the cup.",
          lambda: blend_pct(6, 15, 1, 2, "milk"), plain("11%", "13%", "10%", "12%")),
         (1654, r"One liquid has \(35\%\) milk and another has \(50\%\) milk. A jug is filled with \(2\) parts of the first and \(1\) "
                r"part of the second. What percentage of the jug is milk?",
          lambda: blend_pct(35, 50, 2, 1, "milk"), plain("40%", "42%", "38%", "45%"))],
    26: [(1201, r"The weights of two brothers, Ravi and Kiran, are in the ratio \(1:4\). Ravi's weight goes up by \(20\%\), and "
                r"their total weight becomes \(87\) kg, a rise of \(16\%\). By what percent did Kiran's weight go up?",
          lambda: weights(1, 4, 20, 87, 16, "Ravi", "Kiran"), plain("12%", "18%", "15%", "16%")),
         (1202, r"The weights of two sisters, Asha and Usha, are in the ratio \(3:2\). Asha's weight goes up by \(20\%\), and their "
                r"total weight becomes \(174\) kg, a rise of \(16\%\). By what percent did Usha's weight go up?",
          lambda: weights(3, 2, 20, 174, 16, "Asha", "Usha"), plain("12%", "10%", "8%", "14%")),
         (1203, r"The weights of two friends, Mohan and Sohan, are in the ratio \(7:3\). Mohan's weight goes up by \(10\%\), and "
                r"their total weight becomes \(116\) kg, a rise of \(16\%\). By what percent did Sohan's weight go up?",
          lambda: weights(7, 3, 10, 116, 16, "Mohan", "Sohan"), plain("25%", "30%", "35%", "20%"))],
    27: [(1204, "A 36-litre tank holds a mixture of oxygen and nitrogen, with oxygen making up 32% of it. Some litres of the "
                "mixture are let out and the same amount of nitrogen is put in. This is done once more with the same amount, "
                "and now oxygen makes up 18% of the tank. How many litres were let out each time?",
          lambda: released(36, 32, 18), "litres"),
         (1205, "A barber uses a mixture of 5 parts pure lotion and 3 parts water. He takes out some of the mixture and puts in "
                "the same amount of water, so that the lotion becomes half of the mixture. What part of the mixture did he take "
                "out?", lambda: lotion(5, 3), plain(fr(1, 4), fr(1, 3), fr(1, 5), fr(2, 5))),
         (1206, "A 40-litre tank holds a mixture of oxygen and nitrogen, with oxygen making up 60% of it. Some litres of the "
                "mixture are let out and the same amount of nitrogen is put in. This is done once more with the same amount, "
                "and now oxygen makes up 15% of the tank. How many litres were let out each time?",
          lambda: released(40, 60, 15), "litres"),
         (1207, "A 45-litre tank holds a mixture of oxygen and nitrogen, with oxygen making up 75% of it. Some litres of the "
                "mixture are let out and the same amount of nitrogen is put in. This is done once more with the same amount, "
                "and now oxygen makes up 48% of the tank. How many litres were let out each time?",
          lambda: released(45, 75, 48), "litres"),
         (1208, "A 56-litre tank holds a mixture of oxygen and nitrogen, with oxygen making up 48% of it. Some litres of the "
                "mixture are let out and the same amount of nitrogen is put in. This is done once more with the same amount, "
                "and now oxygen makes up 27% of the tank. How many litres were let out each time?",
          lambda: released(56, 48, 27), "litres")],
    28: [(1209, "A barrel holds 216 litres of wine. 36 litres are taken out and the barrel is filled up with water. This is done "
                "three times in all. How many litres of wine are left in the barrel?",
          lambda: left_after(216, 36, 3, "amount", "wine"), "litres"),
         (1210, "From a can full of oil, one-third is taken out and the can is filled up with water. This is done four times in "
                "all. What part of the oil that was in the can has been removed?",
          lambda: left_after(1, F(1, 3), 4, "removed", "oil"), plain(fr(16, 81), fr(65, 81), fr(2, 3), fr(55, 81))),
         (1211, "From a jar full of syrup, one-tenth is taken out and the jar is filled up with water. This is done three times "
                "in all. Find the ratio of the syrup left to the syrup there was at first.",
          lambda: left_after(1, F(1, 10), 3, "left_ratio", "syrup"), plain("729 : 1000", "271 : 1000", "81 : 100", "9 : 10")),
         (1212, "A drum holds 72 litres of juice. 12 litres are drawn out and the drum is filled up with water. This is done "
                "three times in all. Find the ratio of juice to water in the drum.",
          lambda: left_after(72, 12, 3, "lw", "juice"), ""),
         (1213, "A tank holds 256 litres of milk. 64 litres are taken out and replaced by water, and this is done three times in "
                "all. How much milk is left in the tank?", lambda: left_after(256, 64, 3, "amount", "milk"), "litres"),
         (1214, "From a cask of 90 litres of wine, 30 litres are drawn out and the cask is filled up with water. This is done "
                "three times in all. What is the ratio of wine to water now?", lambda: left_after(90, 30, 3, "lw", "wine"), ""),
         (1215, "A can holds 49 litres of milk. 7 litres are taken out and replaced with water. This is done two times in all. "
                "Find the ratio of milk to water in the can.", lambda: left_after(49, 7, 2, "lw", "milk"), "")],
    29: [(1661, r"\(7\) litres are drawn from a drum full of spirit and it is filled up with water. \(7\) litres of the mixture "
                r"are drawn again and the drum is filled up with water once more. Spirit and water are now in the ratio \(25:11\). "
                r"How much does the drum hold?", lambda: g29.capacity(7, 25, 11, "spirit", "water"), "litres"),
         (1662, r"\(10\) litres are drawn from a cask full of wine and it is filled up with water. \(10\) litres of the mixture "
                r"are drawn again and the cask is filled up with water once more. Wine and water are now in the ratio \(49:15\). "
                r"How much does the cask hold?", lambda: g29.capacity(10, 49, 15, "wine", "water"), "litres")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
