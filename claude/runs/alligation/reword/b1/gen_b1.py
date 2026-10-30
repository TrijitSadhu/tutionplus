"""Alligation rewording batch 1 (2026-10-30): the 45 rows of Rules 1-5 that fail the originality gate (book wording or the
book's numbers) get all-new numbers and a sentence in the book's simple style with the item changed (the owner's style),
new options, and an explanation regenerated with the same rule generator for the new numbers. Row ids, rule links, days and
times stay. Rows that already pass the gate (1074, 1641, 1643-1646, 1648) are left as they are. Numbers keep the order the
rule solvers read them in (rule01/solve.py etc.), and the Rule 1 "basic" rows keep exactly three numbers.
Writes reword/b1/ruleNN/2_new_rows.json; check: `python reword_check.py b1`."""
import importlib.util, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))                      # alligation/reword/b1
AL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, AL)
import rw_common  # noqa: E402
from gen_5_10 import add_pure, alcohol_after_water, water_for_ratio  # noqa: E402


def load(rule):
    spec = importlib.util.spec_from_file_location(f"gen_rule{rule:02d}", os.path.join(AL, f"rule{rule:02d}", "gen.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g1, g2, g3, g4 = load(1), load(2), load(3), load(4)
rw_common.NOTE = ("question rewritten in the book's simple style (item changed, all-new numbers, checked against the book) "
                  "by Claude Opus 5.5 (2026-10-30)")
plain = lambda *v: dict(zip("abcd", v))
LEADED = r"Leaded petrol is the part being added. It is now \(100 - {u1} = {l1}\%\) of the mixture and must become \(100 - {u2} = {l2}\%\)."
BARLEY = r"Barley is the part being added. It is now \(100 - 80 = 20\%\) of the mixture and must become \(100 - 64 = 36\%\)."
CD = ("Cheaper", "dearer")

PLAN = {
    1: [(680, "In what ratio must lentils at Rs 6.20 per kg be mixed with lentils at Rs 7.70 per kg, so that the mixture is "
              "worth Rs 6.80 per kg?", lambda: g1.basic(None, "lentils", "kg", "6.20", "7.70", "6.80"), ""),
        (1058, "In what ratio must flour at Rs 8.40 per kg be mixed with flour at Rs 9.60 per kg, so that the mixture is worth "
               "Rs 9.10 per kg?", lambda: g1.basic(None, "flour", "kg", "8.40", "9.60", "9.10"), ""),
        (1059, "In what ratio must peanuts at Rs 12 per kg be mixed with peanuts at Rs 21 per kg, so that the mixture is worth "
               "Rs 15 per kg?", lambda: g1.basic(None, "peanuts", "kg", 12, 21, 15), ""),
        (1060, "In what ratio must cashews at Rs 14 per kg be mixed with cashews at Rs 26 per kg, so that the mixture is worth "
               "Rs 22 per kg?", lambda: g1.basic(None, "cashews", "kg", 14, 26, 22), ""),
        (1061, "In what ratio must wool at Rs 32 per kg be mixed with wool at Rs 44 per kg, so that the mixture is worth Rs 35 "
               "per kg?", lambda: g1.basic(None, "wool", "kg", 32, 44, 35), ""),
        (1062, "In what ratio must salt at Rs 22.40 per kg be mixed with salt at Rs 23.20 per kg, so that the mixture is worth "
               "Rs 22.70 per kg?", lambda: g1.basic(None, "salt", "kg", "22.40", "23.20", "22.70"), ""),
        (1063, "A shop owner mixes two kinds of coffee costing Rs 28 and Rs 37 per kg. In what ratio should he mix them so that "
               "the mixture costs Rs 32 per kg?", lambda: g1.basic(None, "coffee", "kg", 28, 37, 32), ""),
        (1064, "In what ratio must a shopkeeper mix oil at Rs 13 per litre with oil at Rs 21 per litre, so that the mixture is "
               "worth Rs 16 per litre?", lambda: g1.basic(None, "oil", "litre", 13, 21, 16, "Rs", "litres"), ""),
        (1065, "How must a trader mix pulses at Rs 6 per kg and Rs 8 per kg so that the mixture is worth Rs 7.20 per kg?",
         lambda: g1.basic(None, "pulses", "kg", 6, 8, "7.20"), ""),
        (1066, "Silver costing Rs 25 per gm is to be mixed with silver costing Rs 36 per gm. In what ratio must they be mixed "
               "so that the mixture costs Rs 33 per gm?", lambda: g1.basic(None, "silver", "gm", 25, 36, 33, "Rs", "gm"), ""),
        (1067, r"In what ratio must a trader mix rice at 40 paise per kg with rice at 75 paise per kg so that by selling the "
               r"mixture at 72 paise per kg he gains \(\frac{1}{5}\) of his outlay?",
         lambda: g1.gain(None, "the cheaper rice", "the dearer rice", "kg", 40, 75, 72, F(1, 5), "paise"), ""),
        (1068, "Two kinds of almonds, costing Rs 14 and Rs 22 per kg, are mixed in the ratio 3 : 5. What does the mixture cost "
               "per kg?", lambda: g1.mean_from_ratio(None, 14, 22, 3, 5), plain("Rs 18", "Rs 20", "Rs 19", "Rs 17")),
        (1069, r"A shopkeeper buys red lentils at Rs 8 per kg and green lentils at Rs 17 per kg. He sells the mixture at Rs 16 "
               r"per kg and gains \(\frac{1}{3}\) of his outlay. In what ratio must he mix them?",
         lambda: g1.gain(None, "red lentils", "green lentils", "kg", 8, 17, 16, F(1, 3), "Rs"), ""),
        (1070, "In what ratio should water be mixed with juice at Rs 36 per litre to bring the price down to Rs 27 per litre? "
               "(Water is free)", lambda: g1.water(None, 36, 27), ""),
        (1071, "Two kinds of almonds cost Rs 300 and Rs 500 per kg. They are mixed to make 45 kg of a mixture worth Rs 380 per "
               "kg. How many kg of each kind are used?", lambda: g1.split_total(None, "almonds", 300, 500, 380, 45), "kg", CD),
        (1072, "A trader bought 80 quintals of wheat of two kinds for Rs 4450. The better kind costs Rs 65 per quintal and the "
               "worse Rs 50 per quintal. How many quintals of each kind did he buy?",
         lambda: g1.split_cost(None, 50, 65, 80, 4450), "quintals", ("Better kind", "worse kind")),
        (1073, "A man has juice worth Rs 40 a litre and another lot worth Rs 24 a litre. Equal amounts of the two are mixed with "
               "water to get 60 litres of a mixture worth Rs 24 a litre. How much water is in the mixture?",
         lambda: g1.whisky(None, 40, 24, 60, 24), "litres")],
    2: [(836, "How many kg of rice at 50 P per kg must a man mix with 30 kg of rice at 26 P per kg, so that on selling the "
              "mixture at 44 P per kg he gains 10% on his cost?", lambda: g2.quantity(50, 30, 26, 44, 10, "paise", "rice"), "kg"),
        (1642, r"A trader buys \(40\) kg of lentils at Rs \(14.50\) per kg and \(10\) kg of lentils at Rs \(17\) per kg and mixes "
               r"them. At what price per kg should he sell the mixture to make a profit of \(24\%\)?",
         lambda: g2.selling_price(40, "14.50", 10, 17, 24, "lentils"), plain("Rs 18.20", "Rs 17.40", "Rs 18.60", "Rs 19.20")),
        (1647, r"Sugar at \(36\) P per kg is to be mixed with \(8\) kg of sugar at \(54\) P per kg. If the mixture is sold at "
               r"\(44\) P per kg for a profit of \(10\%\), how many kg of the cheaper sugar are needed?",
         lambda: g2.quantity(36, 8, 54, 44, 10, "paise", "sugar"), "kg"),
        (1649, r"Rohan has \(80\) kg of flour bought at Rs \(6.25\) per kg and \(120\) kg bought at Rs \(7.50\) per kg. He "
               r"mixes them. At what price per kg must he sell the mixture to gain \(30\%\)?",
         lambda: g2.selling_price(80, "6.25", 120, "7.50", 30, "flour"), plain("Rs 9.10", "Rs 8.75", "Rs 9.45", "Rs 8.40"))],
    3: [(837, "Some milk is mixed with 12 litres of water and the mixture is worth 75 P per litre. If pure milk costs 100 P "
              "per litre, how much milk is in the mixture?", lambda: g3.milk(None, 12, 75, 100, "paise"), "litres"),
        (1079, "Some milk is mixed with 14 litres of water and the mixture is worth 60 P per litre. If pure milk costs 81 P per "
               "litre, how much milk is in the mixture?", lambda: g3.milk(None, 14, 60, 81, "paise"), "litres"),
        (1080, "Some milk is mixed with 21 litres of water and the mixture is worth Rs 10 per litre. If pure milk costs Rs 16 "
               "per litre, how much milk is in the mixture?", lambda: g3.milk(None, 21, 10, 16, "Rs"), "litres"),
        (1081, "Some milk is mixed with 30 litres of water and the mixture is worth Rs 8 per litre. If pure milk costs Rs 23 "
               "per litre, how much milk is in the mixture?", lambda: g3.milk(None, 30, 8, 23, "Rs"), "litres"),
        (1082, "Some milk is mixed with 8 litres of water and the mixture is worth Rs 4.50 per litre. If pure milk costs Rs 6 "
               "per litre, how much milk is in the mixture?", lambda: g3.milk(None, 8, "4.50", 6, "Rs"), "litres")],
    4: [(838, "A shopkeeper mixes water with spirit and sells the mixture at the cost price of spirit. In what ratio must he "
              "mix water and spirit to gain 25%?", lambda: g4.spirit(None, 25), ""),
        (1095, "A shopkeeper mixes water with spirit and sells the mixture at the cost price of spirit. In what ratio must he "
               "mix water and spirit to gain 10%?", lambda: g4.spirit(None, 10), ""),
        (1096, "A trader adds water to spirit and sells the mixture at the cost price of spirit. In what ratio must water and "
               "spirit be mixed for him to gain 30%?", lambda: g4.spirit(None, 30), ""),
        (1097, "A trader adds water to spirit and sells the mixture at the cost price of spirit. In what ratio must water and "
               "spirit be mixed for him to gain 15%?", lambda: g4.spirit(None, 15), ""),
        (1098, "Water is mixed with spirit and the mixture is sold at the cost price of spirit. In what ratio must they be "
               "mixed to gain 8%?", lambda: g4.spirit(None, 8), ""),
        (1099, "Water is mixed with spirit and the mixture is sold at the cost price of spirit. In what ratio must they be "
               "mixed to gain 50%?", lambda: g4.spirit(None, 50), "")],
    5: [(839, "400 gm of salt solution has 20% salt in it. How much salt should be added to make it 36% salt?",
         lambda: add_pure(400, 20, 36, "gm", "salt", "rest of the solution"), "gm"),
        (1104, r"A sugar syrup weighs 360 gm and \(25\%\) of it is sugar. How much sugar must be added so that sugar becomes "
               r"\(46\%\) of the syrup?", lambda: add_pure(360, 25, 46, "gm", "sugar", "rest of the syrup"), "gm"),
        (1105, r"180 litres of juice mixed with water has \(10\%\) water. How much water should be added so that water becomes "
               r"\(28\%\) of the mixture?", lambda: add_pure(180, 10, 28, "litres", "water", "juice"), "litres"),
        (1106, r"A petrol pump owner mixed leaded and unleaded petrol so that the mixture has \(20\%\) unleaded petrol. How much "
               r"leaded petrol should be added to 2 litres of this mixture so that the unleaded petrol becomes \(8\%\)?",
         lambda: add_pure(2, 80, 92, "litres", "leaded petrol", "unleaded petrol", LEADED.format(u1=20, l1=80, u2=8, l2=92), 1000, "ml"),
         "ml"),
        (1107, r"110 gm of a salt solution has \(25\%\) salt in it. How much salt should be added to make it \(34\%\) salt?",
         lambda: add_pure(110, 25, 34, "gm", "salt", "rest of the solution"), "gm"),
        (1108, r"A petrol pump owner mixed leaded and unleaded petrol so that the mixture has \(35\%\) unleaded petrol. How much "
               r"leaded petrol should be added to 6 litres of this mixture so that the unleaded petrol becomes \(14\%\)?",
         lambda: add_pure(6, 65, 86, "litres", "leaded petrol", "unleaded petrol", LEADED.format(u1=35, l1=65, u2=14, l2=86), 1000, "ml"),
         "ml"),
        (1109, r"A 50 litre mixture of juice and water contains \(16\%\) water. How much water must be added to make the water "
               r"\(30\%\) of the new mixture?", lambda: add_pure(50, 16, 30, "litres", "water", "juice"), "litres"),
        (1110, r"In a mixture of wheat and barley, wheat is \(80\%\). To 500 quintals of this mixture some barley is added, and "
               r"then wheat is \(64\%\) of the new mixture. How many quintals of barley are added?",
         lambda: add_pure(500, 20, 36, "quintals", "barley", "wheat", BARLEY), "quintals"),
        (1111, r"100 gm of an alloy of gold and copper contains \(55\%\) gold. How much gold must be added to this alloy so "
               r"that it contains \(70\%\) gold?", lambda: add_pure(100, 55, 70, "gm", "gold", "copper"), "gm"),
        (1112, r"A 27 litre mixture of alcohol and water has \(65\%\) alcohol. If 18 litres of water are poured in, what percent "
               r"of the new mixture is alcohol?", lambda: alcohol_after_water(27, 65, 18),
         plain("36%", "42%", "39%", "45%")),
        (1113, r"360 ml of a mixture has juice and water in the ratio \(5:1\). How much more water must be added to make the "
               r"ratio of juice and water \(5:2\)?", lambda: water_for_ratio(360, 5, 1, 5, 2, "ml"), "ml"),
        (1114, r"A mixture of 120 litres has milk and water in the ratio \(3:1\). How many litres of water should be poured in so "
               r"that the ratio of milk to water becomes \(1:1\)?", lambda: water_for_ratio(120, 3, 1, 1, 1, "litres"), "litres"),
        (1115, r"An 84 litre mixture has juice and water in the ratio \(6:1\). How much water should be added to change the "
               r"ratio to \(3:2\)?", lambda: water_for_ratio(84, 6, 1, 3, 2, "litres"), "litres")],
}

if __name__ == "__main__":
    rw_common.write_batch(HERE, PLAN)
