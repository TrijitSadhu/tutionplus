"""Profit and Loss Rules 65-68 (2026-10-30). Rule 65: charging Rs M more on each article raises the profit from x% to y% - the cost and
the first price. Rule 66: the 'rule of chain' (a of A cost as much as b of B, ...) - the cost of one item from another. Rule 67: saving
x% of income, then saving z% of an income y% larger - the rise in savings. Rule 68: two articles sold at the same price, at x% and y%
profit or loss - the result on the whole. Writes the four cards, regenerates old rows 373 (R65), 374-378 (R66), 379 (R67), 380, 381,
405 (R68) with simple-style sentences, new settings and all-new numbers, and adds the book exercises that have no copy.
Usage: python gen_65_68.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import place, popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
from gen_57_60 import gopts  # noqa: E402

# ---------------------------------------------------------------- Rule 65
T65 = (r"If charging Rs \(M\) more on each article raises the profit from \(x\%\) to \(y\%\), then"
       r"<br>\[ \text{CP}=\frac{100M}{y-x},\qquad \text{first SP}=\frac{M(100+x)}{y-x} \]")


def r65(x, M, y):
    x, M, y = map(F, (x, M, y))
    cp, sp = 100 * M / (y - x), M * (100 + x) / (y - x)
    trad = steps(
        ("Let the cost of one be Rs \\(c\\).", rf"First price \(= \frac{{{tex(100 + x)}}}{{100}}c\); with Rs \({m(M)}\) more it is \(\frac{{{tex(100 + y)}}}{{100}}c\)."),
        ("The extra charge is the gap between the two prices.", rf"\[ \frac{{{tex(100 + y)} - {tex(100 + x)}}}{{100}}c = {m(M)} \;\Rightarrow\; c = {m(cp)} \]"),
        ("First selling price.", rf"\[ {m(cp)}\times\frac{{{tex(100 + x)}}}{{100}} = {m(sp)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(M = {m(M)}\)."),
        ("Apply the specified rule.", T65.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{100\times {m(M)}}}{{{tex(y - x)}}} = {m(cp)},\qquad \frac{{{m(M)}\times {tex(100 + x)}}}{{{tex(y - x)}}} = {m(sp)} \]"))
    rb = [rf"\(y - x = {tex(y - x)}\).", rf"CP \(= \frac{{100\times {m(M)}}}{{{tex(y - x)}}} = {m(cp)}\).", rf"First SP \(= {m(sp)}\)."]
    return result(("pair", (cp, sp)), T65, trad, rule, rf"cost price Rs \({m(cp)}\), first selling price Rs \({m(sp)}\)", rb,
                  rf"\[ \frac{{100\times {m(M)}}}{{{tex(y - x)}}} = {m(cp)},\quad \frac{{{m(M)}\times {tex(100 + x)}}}{{{tex(y - x)}}} = {m(sp)} \]")


def opts65(g):
    a, b = (F(t) for t in g["answer"][1])
    Q = lambda t: rf"CP Rs \({m(t[0])}\), first price Rs \({m(t[1])}\)"
    return place(Q((a, b)), [Q((b, a)), Q((a + 1, b + 1)), Q((a, b + 2))])


# ---------------------------------------------------------------- Rule 66
T66 = (r"If \(a_1\) of A cost as much as \(b_1\) of B, \(a_2\) of B as much as \(b_2\) of C, \(a_3\) of C as much as \(b_3\) of D, and \(n\) of A "
       r"cost Rs \(R\), then \(m\) of D cost<br>\[ \text{Rs }\frac{R\times a_1\times a_2\times a_3\times m}{n\times b_1\times b_2\times b_3} \]")


def r66(names, links, known, ask, unit=""):
    """names: item names in chain order; links: [(a_i, b_i)] meaning a_i of names[i] cost as much as b_i of names[i+1];
    known: (index, qty, Rs); ask: (index, qty). Prices are worked out along the chain."""
    links = [(F(a), F(b)) for a, b in links]
    ki, kq, kR = known[0], F(known[1]), F(known[2])
    ai, aq = ask[0], F(ask[1])
    price = {ki: kR / kq}
    nm = lambda i, qty: unit + names[i] if unit or qty == 1 else names[i] + "s"
    lines = [rf"One {nm(ki, 1)} costs \({m(kR)} \div {tex(kq)} = {m(price[ki])}\)."]
    step = 1 if ai > ki else -1
    i = ki
    while i != ai:
        j = i + step
        a, b = links[min(i, j)]
        if step == 1:                                    # a of names[i] = b of names[j]
            price[j] = price[i] * a / b
            lines.append(rf"\({tex(a)}\) {nm(i, a)} cost \({tex(a)}\times {m(price[i])} = {m(a * price[i])}\), the same as \({tex(b)}\) {nm(j, b)}, "
                         rf"so one {nm(j, 1)} costs \({m(price[j])}\).")
        else:                                            # a of names[j] = b of names[i]
            price[j] = price[i] * b / a
            lines.append(rf"\({tex(b)}\) {nm(i, b)} cost \({tex(b)}\times {m(price[i])} = {m(b * price[i])}\), the same as \({tex(a)}\) {nm(j, a)}, "
                         rf"so one {nm(j, 1)} costs \({m(price[j])}\).")
        i = j
    v = price[ai] * aq
    trad = steps(("Work out the price of one, step by step.", "<br>".join(lines)),
                 ("Cost asked for.", rf"\[ {tex(aq)}\times {m(price[ai])} = {m(v)} \]"))
    num = [kR] + ([links[k][0] for k in range(ki, ai)] if step == 1 else [links[k][1] for k in range(ai, ki)]) + [aq]
    den = [kq] + ([links[k][1] for k in range(ki, ai)] if step == 1 else [links[k][0] for k in range(ai, ki)])
    TIMES = chr(92) + "times "
    rule = steps(
        ("Identify the values.", r"Write the chain from the item whose price is known to the item asked for."),
        ("Apply the specified rule.", T66.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{TIMES.join(m(t) if k == 0 else tex(t) for k, t in enumerate(num))}}}{{{TIMES.join(tex(t) for t in den)}}} = {m(v)} \]"))
    rb = [rf"Known: \({tex(kq)}\) cost \({m(kR)}\).", rf"Price of one {nm(ai, 1)} \(= {m(price[ai])}\).", rf"Cost of \({tex(aq)}\) \(= {m(v)}\)."]
    return result(("number", v), T66, trad, rule, rf"Rs \({m(v)}\)", rb, rf"\[ {tex(aq)}\times {m(price[ai])} = {m(v)} \]")


def r66_gets(pairs, A0):
    """'A gets Rs a as often as B gets Rs b' for each step; A's amount A0 is known, D's is asked."""
    pairs = [(F(a), F(b)) for a, b in pairs]
    A0 = F(A0)
    amt, lines, who = [A0], [], "ABCD"
    for k, (a, b) in enumerate(pairs):
        amt.append(amt[-1] * b / a)
        lines.append(rf"When {who[k]} gets Rs \({m(a)}\), {who[k + 1]} gets Rs \({m(b)}\): {who[k + 1]} gets "
                     rf"\({m(amt[-2])}\times\frac{{{tex(b)}}}{{{tex(a)}}} = {m(amt[-1])}\).")
    v = amt[-1]
    TIMES = chr(92) + "times "
    fracs = TIMES.join(r"\frac{" + tex(b) + "}{" + tex(a) + "}" for a, b in pairs)
    trad = steps(("Follow the shares from A to D.", "<br>".join(lines)), ("D's share.", rf"\[ \text{{D}} = {m(v)} \]"))
    rule = steps(
        ("Identify the values.", r"Each step 'X gets Rs a as often as Y gets Rs b' says Y's share is \(\frac{b}{a}\) of X's."),
        ("Apply the specified rule.", T66.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{m(A0)}\times {TIMES.join(tex(b) for a, b in pairs)}}}{{{TIMES.join(tex(a) for a, b in pairs)}}} = {m(v)} \]"))
    rb = [rf"A gets \({m(A0)}\).", rf"Multiply by \({fracs}\).", rf"D gets \({m(v)}\)."]
    return result(("number", v), T66, trad, rule, rf"Rs \({m(v)}\)", rb, rf"\[ {m(A0)}\times {fracs} = {m(v)} \]")


# ---------------------------------------------------------------- Rule 67
T67 = (r"If a person saves \(x\%\) of his income, and his income rises by \(y\%\) while he now saves \(z\%\) of it, his savings rise by"
       r"<br>\[ \frac{(100+y)z-100x}{x}\% \]")


def r67(x, y, z):
    x, y, z = map(F, (x, y, z))
    old, new = x, (100 + y) * z / 100
    v = (new - old) / old * 100
    trad = steps(
        ("Take the income as 100.", rf"Savings \(= {tex(old)}\)."),
        ("The new income and savings.", rf"Income \(= {tex(100 + y)}\); savings \(= {tex(z)}\%\) of \({tex(100 + y)} = {tex(new)}\)."),
        ("Rise in savings.", rf"\[ \frac{{{tex(new)} - {tex(old)}}}{{{tex(old)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(z = {tex(z)}\)."),
        ("Apply the specified rule.", T67.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{tex(100 + y)}\times {tex(z)} - 100\times {tex(x)}}}{{{tex(x)}}} = {tex(v)}\% \]"))
    rb = [rf"\((100+y)z = {tex((100 + y) * z)}\).", rf"\(100x = {tex(100 * x)}\).", rf"Rise \(= {tex(v)}\%\)."]
    return result(("number", v), T67, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex((100 + y) * z)} - {tex(100 * x)}}}{{{tex(x)}}} = {tex(v)}\% \]")


# ---------------------------------------------------------------- Rule 68
T68 = (r"If two articles are sold at the same price, one at \(P\%\) profit and the other at \(L\%\) loss, the result on the whole is"
       r"<br>\[ \frac{100(P-L)-2PL}{(100+P)+(100-L)}\% \]a gain if positive, a loss if negative (for two profits use \(+L\) for \(-L\)).")


def r68(A, p, q):
    """p, q: signed per cents (profit +, loss -)."""
    A, p, q = map(F, (A, p, q))
    c1, c2 = A * 100 / (100 + p), A * 100 / (100 + q)
    v = (2 * A - c1 - c2) / (c1 + c2) * 100
    w = lambda t: f"a {'profit' if t > 0 else 'loss'} of"
    trad = steps(
        ("Cost of each article.", rf"\[ {m(A)}\times\frac{{100}}{{{tex(100 + p)}}} = {m(c1)},\qquad {m(A)}\times\frac{{100}}{{{tex(100 + q)}}} = {m(c2)} \]"),
        ("Whole cost and whole selling price.", rf"Cost \(= {m(c1 + c2)}\), selling price \(= 2\times {m(A)} = {m(2 * A)}\)."),
        ("Gain or loss per cent.", rf"\[ \frac{{{m(2 * A)} - {m(c1 + c2)}}}{{{m(c1 + c2)}}}\times 100 = {tex(v)}\% \]" + (" It is negative, so a loss." if v < 0 else "")))
    rule = steps(
        ("Identify the values.", rf"First: {w(p)} \({tex(abs(p))}\%\); second: {w(q)} \({tex(abs(q))}\%\). With signs, \(p = {tex(p)}\), \(q = {tex(q)}\)."),
        ("Apply the specified rule.", T68.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{100\times ({tex(p)} + {tex(q)}) + 2\times ({tex(p)})\times ({tex(q)})}}{{(100 + {tex(p)}) + (100 + {tex(q)})}} = "
                                   rf"\frac{{{tex(100 * (p + q) + 2 * p * q)}}}{{{tex(200 + p + q)}}} = {tex(v)}\% \]"))
    rb = [rf"\(100(p+q) + 2pq = {tex(100 * (p + q) + 2 * p * q)}\).", rf"\((100+p) + (100+q) = {tex(200 + p + q)}\).",
          rf"Result \(= {tex(v)}\%\)."]
    fin = "no gain and no loss" if v == 0 else rf"a {'gain' if v > 0 else 'loss'} of \({tex(abs(v))}\%\)"
    return result(("signed", v), T68, trad, rule, fin, rb, rf"\[ \frac{{{tex(100 * (p + q) + 2 * p * q)}}}{{{tex(200 + p + q)}}} = {tex(v)}\% \]")


CARDS = {
    65: card(65, "Rs M More on Each Article Raises the Profit",
             r"Charging Rs \(M\) more on each article moves the profit from \(x\%\) to \(y\%\) of the same cost, so Rs \(M\) is \((y-x)\%\) of the cost.",
             r"\[ \text{CP}=\frac{100M}{y-x},\qquad \text{first SP}=\frac{M(100+x)}{y-x} \]",
             [("Extra charge", r"M=\frac{y-x}{100}\text{CP}"), ("Cost", r"\frac{100M}{y-x}"), ("First price", r"\text{CP}\times\frac{100+x}{100}")],
             r"Both profit per cents are on the cost, so only their difference matters.",
             "'A fruit merchant makes x% profit; if he charges Rs M more on each, he would gain y%. Find the cost and the first selling price.'",
             r"\(10\%\) to \(30\%\) with Rs \(3\) more: CP \(=\frac{300}{20}=\text{Rs }15\), first price Rs \(16.50\).",
             r"Dividing by \(y\) instead of \(y-x\)."),
    66: card(66, "The Rule of Chain",
             r"'a of A cost as much as b of B' fixes the price of B from the price of A. Going along the chain, each step multiplies the price by "
             r"\(\frac{a}{b}\).",
             r"\[ \text{Cost of } m \text{ of D}=\frac{R\times a_1 a_2 a_3\times m}{n\times b_1 b_2 b_3} \]",
             [("One A", r"\frac{R}{n}"), ("One B", r"\frac{R}{n}\cdot\frac{a_1}{b_1}"), ("One D", r"\frac{R}{n}\cdot\frac{a_1a_2a_3}{b_1b_2b_3}")],
             r"Going the other way along the chain, the \(a\)'s and \(b\)'s change places.",
             "'x kg of rice costs as much as y kg of sugar, z kg of sugar as much as p kg of tea, ...; if n kg of rice cost Rs A, find the cost of m kg of tea.'",
             r"\(2\) A \(=\) \(3\) B, \(4\) B \(=\) \(1\) C, one A Rs \(6\): one B \(=\text{Rs }4\), one C \(=\text{Rs }16\).",
             r"Putting a step's numbers upside down - check that a dearer item gets a higher price."),
    67: card(67, "Savings When the Income and the Saving Rate Change",
             r"On an income of 100, the savings go from \(x\) to \(z\%\) of \(100+y\).",
             r"\[ \text{Rise in savings}=\frac{(100+y)z-100x}{x}\% \]",
             [("Old savings", r"x"), ("New savings", r"\frac{(100+y)z}{100}"), ("Rise", r"\frac{(100+y)z-100x}{x}\%")],
             r"If the saving rate stays at \(x\%\), the savings rise by \(y\%\), the same as the income.",
             "'A person saves x% of his income. If his income increases by y% and he saves z% of it, by what per cent has his saving increased?'",
             r"\(10\%\), income \(+30\%\), now \(20\%\): \(\frac{2600-1000}{10}=160\%\).",
             r"Adding \(y\) and \(z-x\)."),
    68: card(68, "Two Articles Sold at the Same Price",
             r"With equal selling prices the dearer article is the one sold at a loss, so the costs are not equal and the profit and loss do "
             r"not cancel.",
             r"\[ \frac{100(P-L)-2PL}{(100+P)+(100-L)}\% \]",
             [("Costs", r"\frac{100A}{100+P},\ \frac{100A}{100-L}"), ("Sale", r"2A"), ("Same per cent P = L", r"\text{a loss of }\frac{P^2}{100}\%")],
             r"For two profits use \(+L\) in place of \(-L\); for the same profit on both the answer is that profit.",
             "'Each of two cars is sold at the same price; a profit of P% is made on one and a loss of L% on the other. What is the gain or loss per cent?'",
             r"\(20\%\) profit and \(20\%\) loss: a loss of \(\frac{400}{100}=4\%\).",
             r"Thinking equal per cents of profit and loss cancel."),
}
Q65 = ("A shop makes a profit of {x}% by selling {items} at a certain price. If it charges Rs {M} more for each, it would make a profit of {y}%. "
       "Find the cost price of one {one} and the price it charged at first.")
Q67 = "A woman saves {x}% of her income. Her income rises by {y}% and she now saves {z}% of it. By what per cent have her savings gone up?"
Q68 = "A trader sells two {items} at Rs {A} apiece, making a {w1} of {p}% on the first and a {w2} of {q}% on the second. What is his gain or loss per cent on the whole?"
Q68S = "A trader sells two {items} for Rs {A} each and makes a profit of {p}% on each. Find his gain or loss per cent on the whole."

# Rule 66 questions are written out; the numbers in the sentence are the ones in the spec
CH = {374: ("30 kg of flour costs as much as 2 kg of ghee, 2 kg of ghee costs as much as 6 kg of jam, and 8 kg of jam costs as much as 2 kg of nuts. "
            "If 7 kg of nuts cost Rs 4200, find the cost of 6.5 kg of flour.",
            (["flour", "ghee", "jam", "nuts"], [(30, 2), (2, 6), (8, 2)], (3, 7, 4200), (0, F(13, 2)), "kg of ")),
      376: ("15 kg of salt costs as much as 2 kg of oil, 12 kg of oil costs as much as 3 kg of tea, and 3 kg of tea costs as much as 2 kg of coffee. "
            "If 3.5 kg of salt cost Rs 56, find the cost of 13 kg of coffee.",
            (["salt", "oil", "tea", "coffee"], [(15, 2), (12, 3), (3, 2)], (0, F(7, 2), 56), (3, 13), "kg of ")),
      375: ("2 desks cost as much as 3 racks, 3 racks cost as much as 4 stools, and 6 stools cost as much as one cupboard. "
            "If 4 cupboards cost Rs 10800, find the cost of one desk.",
            (["desk", "rack", "stool", "cupboard"], [(2, 3), (3, 4), (6, 1)], (3, 4, 10800), (0, 1), "")),
      377: ("5 goats are worth 2 cows, 6 cows are worth one tractor, and 15 tractors are worth 3 trucks. If one truck costs Rs 450000, "
            "what is the price of one goat?",
            (["goat", "cow", "tractor", "truck"], [(5, 2), (6, 1), (15, 3)], (3, 1, 450000), (0, 1), "")),
      378: ("3 kg of maize costs as much as 2 kg of millet, 48 kg of millet costs as much as 3 kg of cocoa, and 2 kg of cocoa costs as much as "
            "12 kg of jaggery. If 7 kg of maize cost Rs 98, find the cost of 9 kg of jaggery.",
            (["maize", "millet", "cocoa", "jaggery"], [(3, 2), (48, 3), (2, 12)], (0, 7, 98), (3, 9), "kg of ")),
      "r66_e3": ("2 spoons cost as much as 3 forks, 12 forks cost as much as one pan, and 3 pans cost as much as 2 pots. If one pot costs Rs 180, "
                 "find the price of one spoon.",
                 (["spoon", "fork", "pan", "pot"], [(2, 3), (12, 1), (3, 2)], (3, 1, 180), (0, 1), "")),
      "r66_e4": ("A gets Rs 2 as often as B gets Rs 3, B gets Rs 4 as often as C gets Rs 5, and C gets Rs 6 as often as D gets Rs 7. "
                 "If A gets Rs 3.20, how much does D get?",
                 ("gets", [(2, 3), (4, 5), (6, 7)], F(16, 5))),
      "r66_e6": ("3 kg of beans cost as much as 2 kg of peas, one kg of peas costs as much as 2 kg of carrots, and 4 kg of carrots cost as much as "
                 "6 kg of radish. If 7 kg of radish cost Rs 140, find the cost of 9 kg of beans.",
                 (["beans", "peas", "carrots", "radish"], [(3, 2), (1, 2), (4, 6)], (3, 7, 140), (0, 9), "kg of "))}

OLD = {65: {373: ("bananas", "banana", (20, 3, 35))},
       66: {k: k for k in (374, 375, 376, 377, 378)},
       67: {379: (12, 25, 18)},
       68: {380: ("cycles", 1530, 12, -8), 381: ("cupboards", 960, 20, -20), 405: ("lamps", 600, 20, 50)}}
NEW = {65: [("r65_e1", ("pears", "pear", (12, 2, 28))), ("r65_e2", ("melons", "melon", (6, 7, 34))), ("r65_e3", ("coconuts", "coconut", (18, 9, 48))),
            ("r65_e4", ("pineapples", "pineapple", (16, 3, 36)))],
       66: [(k, k) for k in ("r66_e3", "r66_e4", "r66_e6")],
       67: [("r67_e1", (16, 50, 24)), ("r67_e2", (25, 60, 18)), ("r67_e3", (14, 40, 12))],
       68: [("r68_n3", ("chairs", 472, 18, 18)), ("r68_e1", ("sheep", 310, 24, -24)), ("r68_e2", ("ponies", 270, 35, -35)),
            ("r68_e3", ("tables", 585, 30, -10)), ("r68_e4", ("mirrors", 750, 50, 25)), ("r68_e5", ("sofas", 770, 40, 10)),
            ("r68_e6", ("flats", 270000, 8, -8))]}


def build(rule, spec):
    if rule == 65:
        items, one, (x, M, y) = spec
        g = r65(x, M, y)
        return g, Q65.format(items=items, one=one, x=x, M=M, y=y), opts65(g)
    if rule == 66:
        q, c = CH[spec]
        g = r66_gets(c[1], c[2]) if c[0] == "gets" else r66(*c)
        return g, q, ropts(g["answer"][1])
    if rule == 67:
        x, y, z = spec
        g = r67(x, y, z)
        return g, Q67.format(x=x, y=y, z=z), popts(g["answer"][1])
    items, A, p, q = spec
    g = r68(A, p, q)
    if p == q:
        text = Q68S.format(items=items, A=A, p=p)
    else:
        w = lambda t: "profit" if t > 0 else "loss"
        text = Q68.format(items=items, A=A, w1=w(p), p=abs(p), w2=w(q), q=abs(q))
    return g, text, gopts(g["answer"][1])


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[rule])
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, spec)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        kind, v = g["answer"]
        answers.append([key, [kind, [str(t) for t in v] if kind == "pair" else str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (65, 66, 67, 68):
        main(r)
