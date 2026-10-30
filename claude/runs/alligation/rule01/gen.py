"""Rule 1 (basic alligation): regenerates solution / rule_based_explanation / shortcut for the 18 Rule 1 rows
in the prompt #10 layout, fixes answer keys, links every row to the Rule 1 card. Writes 2_new_rows.json."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import (LLM_NOTE, S, cross_table, money, ratio, ratio_steps, rbe, rtex, shortcut,  # noqa: E402
                    solution, steps, tex, tidy)

THEOREM = (r"If an item costing \(x\) per unit is mixed with a dearer item costing \(y\) per unit so that the "
           r"mixture is worth \(z\) per unit \((x \lt z \lt y)\), the two must be mixed in the ratio"
           r"\[ \frac{\text{Quantity of cheaper}}{\text{Quantity of dearer}} = \frac{y-z}{z-x} \]")
RULE = r"\[ \frac{\text{Quantity of cheaper}}{\text{Quantity of dearer}} = \frac{y-z}{z-x} \]"


def price(v, cur):
    return rf"\({money(v)}\) paise" if cur == "paise" else rf"Rs \({money(v)}\)"


def collect(c, d, m, a="p", b="q"):
    c, d, m = F(c), F(d), F(m)
    return (rf"\[ {money(c)}{a} + {money(d)}{b} = {money(m)}{a} + {money(m)}{b} \]"
            rf"\[ {money(d)}{b} - {money(m)}{b} = {money(m)}{a} - {money(c)}{a} \]"
            rf"\[ {tex(d - m)}{b} = {tex(m - c)}{a} \]")


def rule_part(c, d, m, unit, cur, left="Cheaper", right="Dearer", order=""):
    r = ratio(F(d) - F(m), F(m) - F(c))
    return steps(
        ("Identify the values.", rf"Cheaper price \(x = {money(c)}\), dearer price \(y = {money(d)}\), mean price \(z = {money(m)}\)."),
        ("Draw the alligation cross.", cross_table(c, m, d, f"per {unit}" if cur == "Rs" else f"paise per {unit}", left, right).replace("Rs ", "" if cur == "paise" else "Rs ")),
        ("Apply the specified rule.", RULE + rf"\[ = \frac{{{money(d)} - {money(m)}}}{{{money(m)} - {money(c)}}} = {ratio_steps(F(d) - F(m), F(m) - F(c))} \]"
         + rf"So {order or 'cheaper : dearer'} \(= {rtex(r)}\)."),
    ), r


def basic(row, item, unit, c, d, m, cur="Rs", qty="kg"):
    """Ratio of the cheaper (named first) to the dearer item."""
    c, d, m = F(c), F(d), F(m)
    r = ratio(d - m, m - c)
    trad = steps(
        ("Let the quantities be unknowns.",
         rf"Let \(p\) {qty} of the {item} at {price(c, cur)} per {unit} be mixed with \(q\) {qty} of the {item} at {price(d, cur)} per {unit}.<br>"
         rf"The mixture is worth {price(m, cur)} per {unit}."),
        ("Write the total cost of the mixture in two ways.",
         rf"Cost of the two parts = cost of the whole mixture:<br>\[ {money(c)}p + {money(d)}q = {money(m)}(p+q) \]"),
        ("Collect the \\(p\\) terms and the \\(q\\) terms.", collect(c, d, m)),
        ("Find the ratio.", rf"\[ \frac{{p}}{{q}} = {ratio_steps(d - m, m - c)} \]So the two must be mixed in the ratio \({rtex(r)}\).")
    )
    rule, r2 = rule_part(c, d, m, unit, cur)
    assert r == r2
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"Cheaper \(x = {money(c)}\), dearer \(y = {money(d)}\), mean \(z = {money(m)}\).",
              rf"\(y - z = {tex(d - m)}\) and \(z - x = {tex(m - c)}\).",
              rf"Cheaper : dearer \(= {tex(d - m)} : {tex(m - c)} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{y-z}}{{z-x}} = \frac{{{money(d)} - {money(m)}}}{{{money(m)} - {money(c)}}} = {ratio_steps(d - m, m - c)} \]", fin)
    return dict(answer=("ratio", r), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def gain(row, cheap_name, dear_name, unit, c, d, sp, g, cur):
    """Mixture sold at sp with a gain of g (fraction) of the outlay: CP = sp / (1 + g), then alligation."""
    c, d, sp, g = F(c), F(d), F(sp), F(g)
    cp = sp / (1 + g)
    r = ratio(d - cp, cp - c)
    cp_step = (rf"Gain \(= {tex(g)}\) of the outlay, so<br>\[ \text{{SP}} = \text{{CP}} + {tex(g)}\,\text{{CP}} = {frac_(1 + g)}\,\text{{CP}} \]"
               rf"\[ {money(sp)} = {frac_(1 + g)}\,\text{{CP}} \;\Rightarrow\; \text{{CP}} = {money(sp)} \times {frac_(1 / (1 + g))} = {money(cp)} \]"
               rf"So the mixture must cost {price(cp, cur)} per {unit}.")
    trad = steps(
        ("Find the cost price of the mixture.", cp_step),
        ("Let the quantities be unknowns.",
         rf"Let \(p\) kg of {cheap_name} at {price(c, cur)} per {unit} be mixed with \(q\) kg of {dear_name} at {price(d, cur)} per {unit}."),
        ("Write the total cost of the mixture in two ways.", rf"\[ {money(c)}p + {money(d)}q = {money(cp)}(p+q) \]"),
        ("Collect the \\(p\\) terms and the \\(q\\) terms.", collect(c, d, cp)),
        ("Find the ratio.", rf"\[ \frac{{p}}{{q}} = {ratio_steps(d - cp, cp - c)} \]So {cheap_name} : {dear_name} \(= {rtex(r)}\).")
    )
    rule_steps, _ = rule_part(c, d, cp, unit, cur, order=f"{cheap_name} : {dear_name}")
    rule = (rf"<b>Step 0: Turn the selling price into the cost price.</b><br>\[ \text{{CP}} = {money(sp)} \times {frac_(1 / (1 + g))} = {money(cp)} \]"
            r"Alligation always works on cost prices, so the mean price is \(z = " + money(cp) + r"\)." + S + rule_steps)
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"Cost price of the mixture \(= {money(sp)} \times {frac_(1 / (1 + g))} = {money(cp)}\).",
              rf"Cheaper \(x = {money(c)}\), dearer \(y = {money(d)}\), mean \(z = {money(cp)}\).",
              rf"Ratio \(= ({money(d)} - {money(cp)}) : ({money(cp)} - {money(c)}) = {tex(d - cp)} : {tex(cp - c)} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \text{{CP}} = {money(sp)} \times {frac_(1 / (1 + g))} = {money(cp)} \]\[ \frac{{{money(d)} - {money(cp)}}}{{{money(cp)} - {money(c)}}} = {ratio_steps(d - cp, cp - c)} \]", fin)
    return dict(answer=("ratio", r), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def frac_(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def mean_from_ratio(row, c, d, a, b):
    c, d = F(c), F(d)
    z = (c * a + d * b) / (a + b)
    trad = steps(
        ("Take quantities in the given ratio.", rf"Take \({a}\) kg at Rs \({money(c)}\) and \({b}\) kg at Rs \({money(d)}\)."),
        ("Find the total cost.", rf"\[ {a}\times{money(c)} + {b}\times{money(d)} = {tex(a * c)} + {tex(b * d)} = {tex(a * c + b * d)} \]"),
        ("Divide by the total quantity.", rf"\[ \text{{Price per kg}} = \frac{{{tex(a * c + b * d)}}}{{{a + b}}} = {tex(z)} \]So the mixture is worth Rs \({money(z)}\) per kg.")
    )
    rule = steps(
        ("Identify the values.", rf"Cheaper \(x = {money(c)}\), dearer \(y = {money(d)}\), ratio cheaper : dearer \(= {a} : {b}\), mean price \(z\) unknown."),
        ("Apply the specified rule.", RULE + rf"\[ \frac{{{money(d)} - z}}{{z - {money(c)}}} = \frac{{{a}}}{{{b}}} \]"),
        ("Solve for \\(z\\).", rf"\[ {b}({money(d)} - z) = {a}(z - {money(c)}) \]\[ {tex(b * d)} - {b}z = {a}z - {tex(a * c)} \]"
         rf"\[ {tex(b * d + a * c)} = {a + b}z \;\Rightarrow\; z = {tex(z)} \]")
    )
    fin = rf"Rs \({money(z)}\) per kg"
    rb = rbe([rf"Cheaper \(x = {money(c)}\), dearer \(y = {money(d)}\), ratio \({a} : {b}\).",
              rf"\(\frac{{{money(d)} - z}}{{z - {money(c)}}} = \frac{{{a}}}{{{b}}}\), so \({b}({money(d)} - z) = {a}(z - {money(c)})\).",
              rf"\({tex(b * d + a * c)} = {a + b}z\), so \(z = {tex(z)}\)."], fin)
    sc = shortcut(rf"\[ z = \frac{{{a}\times{money(c)} + {b}\times{money(d)}}}{{{a}+{b}}} = \frac{{{tex(a * c + b * d)}}}{{{a + b}}} = {tex(z)} \]", fin)
    return dict(answer=("money", z), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def water(row, wine, m):
    wine, m = F(wine), F(m)
    r = ratio(wine - m, m)
    trad = steps(
        ("Let the quantities be unknowns.", r"Let \(p\) litres of water (cost Rs \(0\)) be mixed with \(q\) litres of wine at Rs \(" + money(wine) + r"\) per litre."),
        ("Write the total cost of the mixture in two ways.", rf"\[ 0\cdot p + {money(wine)}q = {money(m)}(p+q) \]"),
        ("Collect the terms.", rf"\[ {money(wine)}q - {money(m)}q = {money(m)}p \]\[ {tex(wine - m)}q = {money(m)}p \]"),
        ("Find the ratio.", rf"\[ \frac{{p}}{{q}} = {ratio_steps(wine - m, m)} \]So water : wine \(= {rtex(r)}\).")
    )
    rule_steps, _ = rule_part(0, wine, m, "litre", "Rs", "Water", "Wine", "water : wine")
    rule = "Water is free, so its price is Rs \\(0\\) per litre." + S + rule_steps
    fin = rf"\({rtex(r)}\)"
    rb = rbe([rf"Water \(x = 0\), wine \(y = {money(wine)}\), mean \(z = {money(m)}\).",
              rf"\(y - z = {tex(wine - m)}\) and \(z - x = {money(m)}\).",
              rf"Water : wine \(= {tex(wine - m)} : {money(m)} = {rtex(r)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{money(wine)} - {money(m)}}}{{{money(m)} - 0}} = {ratio_steps(wine - m, m)} \]", fin)
    return dict(answer=("ratio", r), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def split_total(row, item, c, d, m, total):
    c, d, m = F(c), F(d), F(m)
    r = ratio(d - m, m - c)
    q = total * (m - c) / (d - c)
    p = total - q
    trad = steps(
        ("Let the quantities be unknowns.", rf"Let \(p\) kg of {item} at Rs \({money(c)}\) and \(q\) kg at Rs \({money(d)}\) be taken.<br>\[ p + q = {total} \]"),
        ("Use the total cost.", rf"\[ {money(c)}p + {money(d)}q = {money(m)}\times{total} = {tex(m * total)} \]"),
        ("Substitute \\(p = " + str(total) + " - q\\).",
         rf"\[ {money(c)}({total} - q) + {money(d)}q = {tex(m * total)} \]\[ {tex(c * total)} + {tex(d - c)}q = {tex(m * total)} \]"
         rf"\[ {tex(d - c)}q = {tex(m * total - c * total)} \;\Rightarrow\; q = {tex(q)} \]"),
        ("Find the other quantity.", rf"\[ p = {total} - {tex(q)} = {tex(p)} \]")
    )
    rule_steps, _ = rule_part(c, d, m, "kg", "Rs")
    rule = rule_steps + S + (rf"<b>Step 4: Split the total in this ratio.</b><br>Total parts \(= {r[0]} + {r[1]} = {r[0] + r[1]}\).<br>"
                             rf"\[ \text{{At Rs }}{money(c)} = \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total} = {tex(p)}\text{{ kg}},\qquad \text{{At Rs }}{money(d)} = \frac{{{r[1]}}}{{{r[0] + r[1]}}}\times{total} = {tex(q)}\text{{ kg}} \]")
    fin = rf"\({tex(p)}\) kg at Rs \({money(c)}\) and \({tex(q)}\) kg at Rs \({money(d)}\)"
    rb = rbe([rf"Ratio \(= ({money(d)} - {money(m)}) : ({money(m)} - {money(c)}) = {tex(d - m)} : {tex(m - c)} = {rtex(r)}\).",
              rf"Total parts \(= {r[0] + r[1]}\) for \({total}\) kg.",
              rf"Quantities \(= \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total} = {tex(p)}\) kg and \(\frac{{{r[1]}}}{{{r[0] + r[1]}}}\times{total} = {tex(q)}\) kg."], fin)
    sc = shortcut(rf"\[ {rtex(r)} \text{{ of }} {total} \text{{ kg}} \Rightarrow {tex(p)}\text{{ kg and }}{tex(q)}\text{{ kg}} \]", fin)
    return dict(answer=("pair", (p, q)), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def split_cost(row, worse, better, total_qty, total_cost):
    worse, better, total_cost = F(worse), F(better), F(total_cost)
    b = (total_cost - worse * total_qty) / (better - worse)
    w = total_qty - b
    m = total_cost / total_qty
    r = ratio(better - m, m - worse)
    trad = steps(
        ("Let the quantities be unknowns.", rf"Let \(b\) quintals of the better sort and \(w\) quintals of the worse sort be bought.<br>\[ b + w = {total_qty} \]"),
        ("Use the total cost.", rf"\[ {money(better)}b + {money(worse)}w = {money(total_cost)} \]"),
        ("Substitute \\(w = " + str(total_qty) + " - b\\).",
         rf"\[ {money(better)}b + {money(worse)}({total_qty} - b) = {money(total_cost)} \]\[ {tex(better - worse)}b + {tex(worse * total_qty)} = {money(total_cost)} \]"
         rf"\[ {tex(better - worse)}b = {tex(total_cost - worse * total_qty)} \;\Rightarrow\; b = {tex(b)} \]"),
        ("Find the other quantity.", rf"\[ w = {total_qty} - {tex(b)} = {tex(w)} \]")
    )
    rule = (rf"<b>Step 0: Find the mean price.</b><br>\[ z = \frac{{{money(total_cost)}}}{{{total_qty}}} = {tex(m)} \text{{ per quintal}} \]" + S +
            rule_part(worse, better, m, "quintal", "Rs", "Worse", "Better", "worse : better")[0] + S +
            rf"<b>Step 4: Split the {total_qty} quintals.</b><br>"
            rf"\[ \text{{Worse}} = \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total_qty} = {tex(w)},\qquad \text{{Better}} = \frac{{{r[1]}}}{{{r[0] + r[1]}}}\times{total_qty} = {tex(b)} \]")
    fin = rf"\({tex(b)}\) quintals of the better sort and \({tex(w)}\) quintals of the worse sort"
    rb = rbe([rf"Mean price \(= {money(total_cost)} \div {total_qty} = {tex(m)}\).",
              rf"Worse : better \(= ({money(better)} - {tex(m)}) : ({tex(m)} - {money(worse)}) = {tex(better - m)} : {tex(m - worse)} = {rtex(r)}\).",
              rf"Better \(= \frac{{{r[1]}}}{{{r[0] + r[1]}}}\times{total_qty} = {tex(b)}\), worse \(= {tex(w)}\)."], fin)
    sc = shortcut(rf"\[ z = {tex(m)},\quad \text{{worse}} : \text{{better}} = {tex(better - m)} : {tex(m - worse)} = {rtex(r)} \Rightarrow {tex(w)}\text{{ and }}{tex(b)} \]", fin)
    return dict(answer=("pair", (b, w)), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


def whisky(row, w1, w2, total, m):
    w1, w2, m = F(w1), F(w2), F(m)
    k = m * total / (w1 + w2)
    water_q = total - 2 * k
    blend = (w1 + w2) / 2
    r = ratio(blend - m, m)
    trad = steps(
        ("Let the quantities be unknowns.", rf"Let each whisky lot be \(k\) litres (equal quantities) and the water be \(r\) litres.<br>\[ 2k + r = {total} \]"),
        ("Use the total cost (water costs nothing).", rf"\[ {money(w1)}k + {money(w2)}k + 0\cdot r = {money(m)}\times{total} \]\[ {tex(w1 + w2)}k = {tex(m * total)} \;\Rightarrow\; k = {tex(k)} \]"),
        ("Find the water.", rf"\[ r = {total} - 2\times{tex(k)} = {tex(water_q)} \]")
    )
    rule = steps(
        ("Price of the whisky blend.", rf"Equal quantities give the ratio \(1 : 1\), so by the rule \(\frac{{{money(w1)} - z}}{{z - {money(w2)}}} = 1\), i.e. \(z = \frac{{{money(w1)} + {money(w2)}}}{{2}} = {tex(blend)}\)."),
        ("Mix the blend with water.", rf"Water \(x = 0\), blend \(y = {tex(blend)}\), mean \(z = {money(m)}\).<br>" + RULE +
         rf"\[ \frac{{\text{{Water}}}}{{\text{{Blend}}}} = \frac{{{tex(blend)} - {money(m)}}}{{{money(m)} - 0}} = {ratio_steps(blend - m, m)} \]"),
        ("Find the water in the mixture.", rf"\[ \text{{Water}} = \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total} = {tex(water_q)}\text{{ litres}} \]")
    )
    fin = rf"\({tex(water_q)}\) litres"
    rb = rbe([rf"Equal lots: blend price \(= \frac{{{money(w1)} + {money(w2)}}}{{2}} = {tex(blend)}\).",
              rf"Water : blend \(= ({tex(blend)} - {money(m)}) : ({money(m)} - 0) = {rtex(r)}\).",
              rf"Water \(= \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total} = {tex(water_q)}\) litres."], fin)
    sc = shortcut(rf"\[ \text{{Blend}} = {tex(blend)},\quad \frac{{{tex(blend)} - {money(m)}}}{{{money(m)}}} = {rtex(r).replace(' : ', ':')} \Rightarrow \text{{water}} = \frac{{{r[0]}}}{{{r[0] + r[1]}}}\times{total} = {tex(water_q)} \]", fin)
    return dict(answer=("number", water_q), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


PLAN = {
    680: (basic, ("rice", "kg", "3.10", "3.60", "3.25")),
    1058: (basic, ("wheat", "kg", "4.20", "5.00", "4.50")),
    1059: (basic, ("tea", "kg", 10, 18, 16)),
    1060: (basic, ("coffee", "kg", 10, 20, 16)),
    1061: (basic, ("cotton", "kg", 20, 28, 22)),
    1062: (basic, ("sugar", "kg", "15.00", "15.50", "15.30")),
    1063: (basic, ("tea", "kg", 24, 30, 26)),
    1064: (basic, ("beer", "litre", 4, 9, 7, "Rs", "litres")),
    1065: (basic, ("tea", "kg", 4, 5, "4.40")),
    1066: (basic, ("gold", "gm", 15, 20, 18, "Rs", "gm")),
    1067: (gain, ("the cheaper sugar", "the dearer sugar", "kg", 50, 80, 70, F(1, 6), "paise")),
    1068: (mean_from_ratio, (10, 15, 2, 3)),
    1069: (gain, ("black tea", "green tea", "kg", 4, 10, 7, F(1, 6), "Rs")),
    1070: (water, (25, 15)),
    1071: (split_total, ("currants", 40, 100, 76, 25)),
    1072: (split_cost, (70, 85, 60, 4740)),
    1073: (whisky, (30, 20, 50, 20)),
    1074: (split_total, ("currants", 40, 100, 76, 25)),
}

if __name__ == "__main__":
    cur = json.load(open(os.path.join(HERE, "0_current_rows.json"), encoding="utf-8"))
    card_id = cur["rule_card"]["id"]
    out = []
    for row in cur["rows"]:
        fn, args = PLAN[row["id"]]
        g = fn(row, *args)
        llm = row["llm_used"] or ""
        out.append({"id": row["id"], "answer": [g["answer"][0], [str(x) for x in g["answer"][1]] if isinstance(g["answer"][1], tuple) else str(g["answer"][1])],
                    "old": {k: row[k] for k in ("solution", "rule_based_explanation", "shortcut", "ans", "rule_id", "llm_used")},
                    "new": {"solution": tidy(g["solution"]), "rule_based_explanation": tidy(g["rbe"]), "shortcut": tidy(g["shortcut"]),
                            "rule_id": card_id, "llm_used": llm if LLM_NOTE in llm else (llm + "; " if llm else "") + LLM_NOTE}})
    json.dump(out, open(os.path.join(HERE, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("generated", len(out), "rows")
