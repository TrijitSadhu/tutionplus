"""Profit and Loss Rules 57-60 (2026-10-30). Rule 57: selling X a rupee loses x% - how many a rupee to gain y%. Rule 58: an article sold
for Rs A at x% profit - the price for y% profit, the rise needed, or the gain / loss at another price. Rule 59: the same from a loss of
x% (and the book's "part of the stock spoiled" example). Rule 60: bought x% below the list price, sold y% above it - profit per cent.
Writes the four cards, regenerates old rows 360 (R57), 361-363 (R58), 364-367 (R59), 368-369 (R60) with simple-style sentences, new
settings and all-new numbers, and adds the book exercises that have no copy. Usage: python gen_57_60.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import _k, place, popts  # noqa: E402
from gen_18_21 import ropts, sopts  # noqa: E402
from gen_51_52 import pct_txt  # noqa: E402

# ---------------------------------------------------------------- Rule 57
T57 = (r"If selling \(X\) articles a rupee gives a loss of \(x\%\), then to gain \(y\%\) the number to sell for a rupee is"
       r"<br>\[ X\times\frac{100-x}{100+y} \]")


def r57(X, x, y, item):
    X, x, y = map(F, (X, x, y))
    v = X * (100 - x) / (100 + y)
    trad = steps(
        ("Price of one article now and its cost.", rf"One sells for Re \(\frac{{1}}{{{tex(X)}}}\), which is \({tex(100 - x)}\%\) of its cost, so cost \(= \frac{{1}}{{{tex(X)}}}\times\frac{{100}}{{{tex(100 - x)}}} = {tex(100 / (X * (100 - x)))}\)."),
        ("Price of one for the gain.", rf"\[ {tex(100 / (X * (100 - x)))}\times\frac{{{tex(100 + y)}}}{{100}} = {tex((100 + y) / (X * (100 - x)))} \]"),
        ("Number for Re 1.", rf"\[ 1 \div {tex((100 + y) / (X * (100 - x)))} = {tex(v)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(X = {tex(X)}\), \(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T57.split("<br>")[1]),
        ("Substitute the values.", rf"\[ {tex(X)}\times\frac{{{tex(100 - x)}}}{{{tex(100 + y)}}} = {tex(v)} \]"))
    rb = [rf"\(X = {tex(X)}\), \(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\({tex(X)}\times\frac{{{tex(100 - x)}}}{{{tex(100 + y)}}}\).", rf"\(= {tex(v)}\) a rupee."]
    return result(("number", v), T57, trad, rule, rf"\({tex(v)}\) {item} a rupee", rb, rf"\[ {tex(X)}\times\frac{{{tex(100 - x)}}}{{{tex(100 + y)}}} = {tex(v)} \]")


def copts(g, item):
    v = F(g["answer"][1])
    Q = lambda t: rf"\({tex(t)}\) {item}"
    return place(Q(v), [Q(v + 2), Q(v - 2), Q(v + 4)])


# ---------------------------------------------------------------- Rules 58 and 59
TH = {58: (r"If an article sold for Rs \(A\) gives a profit of \(x\%\), then for a profit of \(y\%\) the price must rise by "
           r"\(\frac{y-x}{100+x}\times A\), and the new price is<br>\[ \frac{100+y}{100+x}\times A \]"),
      59: (r"If an article sold for Rs \(A\) gives a loss of \(x\%\), then for a profit of \(y\%\) the price must rise by "
           r"\(\frac{x+y}{100-x}\times A\), and the new price is<br>\[ \frac{100+y}{100-x}\times A \]")}


def r5859(rule, A, x, ask, y=None, B=None, note="", unit="", per=None):
    """ask: 'newsp' (price for y% profit), 'incr' (rise and new price), 'other' (gain / loss per cent at the price B)."""
    A, x = F(A), F(x)
    base = 100 + x if rule == 58 else 100 - x
    cp = A * 100 / base
    T = TH[rule]
    sgn = "+" if rule == 58 else "-"
    trad = [("Find the cost price.", (note + " " if note else "") + rf"Rs \({m(A)}\) is \({tex(base)}\%\) of the cost, so \[ \text{{CP}} = {m(A)}\times\frac{{100}}{{{tex(base)}}} = {m(cp)} \]")]
    rule_s = [("Identify the values.", rf"\(A = {m(A)}\), \(x = {tex(x)}\)" + (rf", \(y = {tex(y)}\)." if y is not None else rf", other price \(B = {m(B)}\)."))]
    if ask in ("newsp", "incr"):
        y = F(y)
        new = A * (100 + y) / base
        trad.append(("Price for the profit wanted.", rf"\[ {m(cp)}\times\frac{{{tex(100 + y)}}}{{100}} = {m(new)} \]"))
        rule_s += [("Apply the specified rule.", T.split("<br>")[1]),
                   ("Substitute the values.", rf"\[ \frac{{100 + {tex(y)}}}{{100 {sgn} {tex(x)}}}\times {m(A)} = {m(new)} \]")]
        if ask == "incr":
            rise = new - A
            trad.append(("The rise in price.", rf"\[ {m(new)} - {m(A)} = {m(rise)} \]"))
            top = rf"{tex(y)} - {tex(x)}" if rule == 58 else rf"{tex(x)} + {tex(y)}"
            rule_s.append(("The rise.", rf"\[ \frac{{{top}}}{{100 {sgn} {tex(x)}}}\times {m(A)} = {m(rise)} \]"))
            fin = rf"a rise of Rs \({m(rise)}\); new selling price Rs \({m(new)}\)"
            rb = [rf"CP \(= {m(cp)}\).", rf"New SP \(= {m(new)}\).", rf"Rise \(= {m(rise)}\)."]
            return result(("pair", (rise, new)), T, steps(*trad), steps(*rule_s), fin, rb, rf"\[ {m(new)} - {m(A)} = {m(rise)} \]")
        fin = rf"Rs \({m(new)}\)" + (f" {per}" if per else "")
        rb = [rf"CP \(= {m(cp)}\).", rf"\(\frac{{100 + {tex(y)}}}{{100 {sgn} {tex(x)}}}\times {m(A)}\).", rf"\(= {m(new)}\)."]
        return result(("number", new), T, steps(*trad), steps(*rule_s), fin, rb, rf"\[ \frac{{{tex(100 + y)}}}{{{tex(base)}}}\times {m(A)} = {m(new)} \]")
    B = F(B)
    v = B * base / A - 100
    trad.append(("Gain or loss at the other price.", rf"\[ \frac{{{m(B)} - {m(cp)}}}{{{m(cp)}}}\times 100 = {tex(v)}\% \]"
                                                     + (" It is negative, so a loss." if v < 0 else "")))
    rule_s += [("Apply the specified rule.", T.split("<br>")[1] + r"with the new price \(B\) known: \(B = \frac{100+y}{" + rf"100 {sgn} x" + r"}\times A\)."),
               ("Solve for y.", rf"\[ y = \frac{{{m(B)}\times {tex(base)}}}{{{m(A)}}} - 100 = {tex(v)} \]")]
    rb = [rf"CP \(= {m(cp)}\).", rf"\(y = \frac{{{m(B)}\times {tex(base)}}}{{{m(A)}}} - 100\).", rf"\(= {tex(v)}\%\)."]
    fin = rf"a {'loss' if v < 0 else 'gain'} of \({tex(abs(v))}\%\)"
    return result(("signed", v), T, steps(*trad), steps(*rule_s), fin, rb, rf"\[ \frac{{{m(B)}\times {tex(base)}}}{{{m(A)}}} - 100 = {tex(v)}\% \]")


def iopts(g):
    a, b = (F(t) for t in g["answer"][1])
    step = 1 if b < 100 else 10
    Q = lambda t: rf"Rs \({m(t[0])}\), Rs \({m(t[1])}\)"
    return place(Q((a, b)), [Q((a + step, b + step)), Q((a, b + step)), Q((a + step, b))])


def gopts(v):                                    # signed gain / loss options in the words the questions use
    o, pos = sopts(v)
    return [s.replace("Profit of", "Gain of") for s in o], pos


# ---------------------------------------------------------------- Rule 60
T60 = (r"If an article is bought at \(x\%\) below its list price and sold at \(y\%\) above the list price, the profit is"
       r"<br>\[ \frac{y+x}{100-x}\times 100\% \]")


def r60(x, y):
    x, y = F(x), F(y)
    v = (y + x) / (100 - x) * 100
    trad = steps(
        ("Take the list price as 100.", rf"Cost \(= 100 - {tex(x)} = {tex(100 - x)}\); selling price \(= 100 + {tex(y)} = {tex(100 + y)}\)."),
        ("Profit.", rf"\[ {tex(100 + y)} - {tex(100 - x)} = {tex(x + y)} \]"),
        ("Profit per cent on the cost.", rf"\[ \frac{{{tex(x + y)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", T60.split("<br>")[1]),
        ("Substitute the values.", rf"\[ \frac{{{tex(y)} + {tex(x)}}}{{100 - {tex(x)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", rf"\(\frac{{{tex(x + y)}}}{{{tex(100 - x)}}}\times 100\).", rf"\(= {tex(v)}\%\)."]
    return result(("number", v), T60, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(x + y)}}}{{{tex(100 - x)}}}\times 100 = {tex(v)}\% \]")


def r60_list(x, y):                              # sold y% above the price PAID; profit per cent on the LIST price
    x, y = F(x), F(y)
    paid = 100 - x
    sp = paid * (100 + y) / 100
    v = sp - 100
    trad = steps(
        ("Take the list price as 100.", rf"He pays \(100 - {tex(x)} = {tex(paid)}\)."),
        ("He sells at " + tex(y) + "% above what he paid.", rf"\[ {tex(paid)}\times\frac{{{tex(100 + y)}}}{{100}} = {tex(sp)} \]"),
        ("Profit measured on the list price.", rf"\[ {tex(sp)} - 100 = {tex(v)}\% \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\); the selling price is \({tex(y)}\%\) above the cost, not above the list price."),
        ("Apply the specified rule.", T60.split("<br>")[1] + r"here the sale is \(y\%\) above the cost, so on the list price the result is "
                                                             r"\(\left(\frac{(100-x)(100+y)}{100}-100\right)\%\)"),
        ("Substitute the values.", rf"\[ \frac{{{tex(paid)}\times {tex(100 + y)}}}{{100}} - 100 = {tex(v)}\% \]"))
    rb = [rf"Paid \(= {tex(paid)}\).", rf"Sold for \({tex(sp)}\).", rf"Profit on the list price \(= {tex(v)}\%\)."]
    return result(("number", v), T60, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(paid)}\times {tex(100 + y)}}}{{100}} - 100 = {tex(v)}\% \]")


CARDS = {
    57: card(57, "Selling So Many a Rupee at a Loss: How Many for a Gain",
             r"Selling \(X\) a rupee brings in only \((100-x)\%\) of the cost. For a gain of \(y\%\) each article must bring in \((100+y)\%\) of it, "
             r"so fewer must be sold for a rupee.",
             r"\[ \text{Number a rupee}=X\times\frac{100-x}{100+y} \]",
             [("Price now", r"(100-x)\%\ \text{of cost}"), ("Price wanted", r"(100+y)\%\ \text{of cost}"), ("Number a rupee", r"X\times\frac{100-x}{100+y}")],
             r"The number a rupee goes down as the price of each article goes up.",
             "'By selling oranges at X a rupee a man loses x%. How many a rupee should he sell to gain y%?'",
             r"\(30\) a rupee, loss \(10\%\), gain \(8\%\): \(30\times\frac{90}{108}=25\).",
             r"Multiplying by \(\frac{100+y}{100-x}\) - that would give more articles a rupee."),
    58: card(58, "Sold at a Profit: the Price for Another Profit",
             r"The price Rs \(A\) is \((100+x)\%\) of the cost. Any other price is found from the same cost: Rs \(A\) scaled by \(\frac{100+y}{100+x}\).",
             r"\[ \text{New price}=\frac{100+y}{100+x}\times A,\qquad \text{rise}=\frac{y-x}{100+x}\times A \]",
             [("Cost", r"\frac{100A}{100+x}"), ("Price for y%", r"\frac{100+y}{100+x}A"), ("Other price B", r"y=\frac{B(100+x)}{A}-100")],
             r"For a price that gives a loss, \(y\) comes out negative.",
             "'By selling an article for Rs A a dealer makes x% profit. By how much should he raise the price to make y%?' / 'What would he gain or lose by selling it for Rs B?'",
             r"Rs \(44\) at \(10\%\) profit, wanted \(25\%\): \(\frac{125}{110}\times 44=\text{Rs }50\), a rise of Rs \(6\).",
             r"Taking \(y\%\) of the selling price instead of the cost."),
    59: card(59, "Sold at a Loss: the Price for a Profit",
             r"The price Rs \(A\) is \((100-x)\%\) of the cost. For a profit of \(y\%\) the price must be \((100+y)\%\) of the cost.",
             r"\[ \text{New price}=\frac{100+y}{100-x}\times A,\qquad \text{rise}=\frac{x+y}{100-x}\times A \]",
             [("Cost", r"\frac{100A}{100-x}"), ("Price for y%", r"\frac{100+y}{100-x}A"), ("Other price B", r"y=\frac{B(100-x)}{A}-100")],
             r"Spoiled stock works like a loss: if \(s\%\) is spoiled, selling the rest at cost loses \(s\%\).",
             "'By selling an article for Rs A a dealer loses x%. At what price should he sell it to gain y%?'",
             r"Rs \(90\) at \(10\%\) loss, wanted \(20\%\) profit: \(\frac{120}{90}\times 90=\text{Rs }120\).",
             r"Adding \(x+y\) per cent of the selling price instead of the cost."),
    60: card(60, "Bought Below the List Price, Sold Above It",
             r"Bought at \(x\%\) below the list price and sold at \(y\%\) above it, the profit is \(x+y\) per cent of the list price, on a cost of "
             r"\(100-x\).",
             r"\[ \text{Profit}=\frac{y+x}{100-x}\times 100\% \]",
             [("Cost (list = 100)", r"100-x"), ("Selling price", r"100+y"), ("Profit %", r"\frac{x+y}{100-x}\times 100")],
             r"Profit per cent is on the cost, not on the list price.",
             "'A dealer bought a horse at x% discount on its original price and sold it at y% increase on the original price. What profit per cent did he get?'",
             r"\(10\%\) below, \(8\%\) above: \(\frac{18}{90}\times 100=20\%\).",
             r"Answering \(x+y\) - that is the profit on the list price."),
}

Q57 = {"a": "A hawker sells {item} at {X} a rupee and loses {x}%. How many should he sell for a rupee to gain {y}%?",
       "b": "By selling {X} {item} for one rupee, a woman loses {x}%. How many must she sell for a rupee to make a gain of {y}%?"}
OLD = {57: {360: (("a", "pears", 36, 25, 35))},
       58: {361: ("incr", "A dealer sells a kettle for Rs {A} and makes a profit of {x}%. By how much should he raise the price to make a profit of {y}%, and what will the new price be?", dict(A="27.60", x=15, y=25)),
            362: ("other", "A pump is sold for Rs {A} at a gain of {x}%. What would the gain or loss per cent be if it were sold for Rs {B}?", dict(A=6480, x=8, B=5820)),
            363: ("per", "By selling {qa} kg of rice for Rs {A}, a grocer gains {x}%. What does he gain or lose per cent by selling {qb} kg of the same rice for Rs {B}?",
                  dict(qa=20, A=648, x=8, qb=40, B=1236))},
       59: {364: ("incr", "By selling a heater for Rs {A}, a dealer loses {x}%. By how much should he raise the price to make a profit of {y}%, and what will the new price be?", dict(A=255, x=15, y=24)),
            365: ("spoil", "A trader buys wheat at Rs {A} a quintal and {s}% of it gets spoiled. At what price per quintal should he sell the rest to gain {y}% on his outlay?", dict(A=360, s=4, y=8)),
            366: ("other", "A cow is sold for Rs {A} at a loss of {x}%. What would the gain or loss per cent be if it were sold for Rs {B}?", dict(A=1520, x=5, B=1720)),
            367: ("frac", r"By selling a stool for Rs {A}, a man loses \(\frac{{1}}{{{k}}}\) of his outlay. What would he gain or lose per cent by selling it for Rs {B}?", dict(A=70, k=8, B=92))},
       60: {368: ("std", (30, 26))}}
NEW = {57: [("r57_e1", ("a", "figs", 40, 16, 12)), ("r57_e2", ("a", "limes", 50, 28, 20)), ("r57_e3", ("a", "eggs", 42, 4, 12)),
            ("r57_e4", ("a", "plums", 27, 30, 5)), ("r57_e5", ("b", "lemons", 14, 10, 26))],
       58: [("r58_e1", ("newsp", "A grocer sells sugar at Rs {A} a kg and gains {x}%. At what price per kg should he sell it to gain {y}%?", dict(A="4.68", x=4, y=12))),
            ("r58_e3", ("other", "A clock is sold for Rs {A} at a gain of {x}%. What would the gain or loss per cent be if it were sold for Rs {B}?", dict(A=150, x=25, B=114))),
            ("r58_e5", ("fracg", r"By selling a toy for Rs {A}, a man gains \(\frac{{1}}{{{k}}}\) of his outlay. What would he gain or lose per cent by selling it for Rs {B}?", dict(A=132, k=5, B=121)))],
       59: [("r59_e1", ("newsp", "A dealer sells salt at Rs {A} a quintal and loses {x}%. At what price per quintal should he sell it to gain {y}%?", dict(A="42.50", x=15, y=15))),
            ("r59_e2", ("newsp", "By selling a cart for Rs {A}, a man loses {x}%. At what price must he sell it to gain {y}%?", dict(A=1176, x=2, y=8))),
            ("r59_e3", ("newsp", "By selling a lamp for Rs {A}, a shop loses {x}%. At what price should it sell the lamp to gain {y}%?", dict(A=21, x="12.5", y=25))),
            ("r59_e4", ("newsp", "By selling cloth at Rs {A} a metre, a draper loses {x}%. At what price per metre should he sell it to gain {y}%?", dict(A=57, x=5, y=35))),
            ("r59_e5", ("newsp", "A shop loses {x}% when it sells a bag for Rs {A}. What price should it charge to make a gain of {y}%?", dict(A="15.60", x="2.5", y=15))),
            ("r59_e7", ("other", "A trader loses {x}% when he sells a batch of goods for Rs {A}. Would he gain or lose, and by what per cent, if he sold them for Rs {B}?", dict(A=356, x=11, B=412))),
            ("r59_e9", ("newsp", "On selling a fan for Rs {A}, a trader loses {x}%. For what price must he sell it to gain {y}%?", dict(A=1152, x=4, y=15)))],
       60: [("r60_e1", ("std", (12, 10))), ("r60_e2", ("std", (4, 8))), ("r60_e3", ("std", (35, 30)))]}
Q60 = {"std": "A dealer buys a {item} at {x}% below its list price and sells it at {y}% above the list price. Find his profit per cent.",
       "list": "A trader buys a {item} at {x}% off its list price and sells it at {y}% above the price he paid. What per cent profit does he make on the list price?"}
ITEM60 = {368: "scooter", 369: "car", "r60_e1": "camera", "r60_e2": "printer", "r60_e3": "sofa"}


def build(rule, key, spec):
    if rule == 57:
        form, item, X, x, y = spec
        g = r57(X, x, y, item)
        return g, Q57[form].format(item=item, X=X, x=x, y=y), copts(g, item)
    if rule == 60:
        kind, (x, y) = spec
        g = r60(x, y) if kind == "std" else r60_list(x, y)
        return g, Q60[kind].format(item=ITEM60[key], x=x, y=y), popts(g["answer"][1])
    kind, tpl, d = spec
    q = tpl.format(**d)
    A, x = F(d["A"]), F(d.get("x", 0))
    if kind == "per":                                       # per-kg prices from the two lots
        g = r5859(rule, A / d["qa"], x, "other", B=F(d["B"]) / d["qb"],
                  note=rf"Price per kg: \(\frac{{{m(A)}}}{{{d['qa']}}} = {m(A / d['qa'])}\); at the new sale \(\frac{{{m(F(d['B']))}}}{{{d['qb']}}} = {m(F(d['B']) / d['qb'])}\).")
        return g, q, gopts(g["answer"][1])
    if kind == "spoil":                                     # spoiled part = selling everything at cost with an s% loss
        g = r5859(rule, A, d["s"], "newsp", y=d["y"], per="a quintal",
                  note=rf"Take the wheat bought as 100 parts costing Rs \({m(A)}\) each; only \({100 - d['s']}\) parts are left, so selling them at Rs \({m(A)}\) "
                       rf"a quintal would bring in \({100 - d['s']}\%\) of the outlay, a loss of \({d['s']}\%\).")
        return g, q, ropts(g["answer"][1])
    if kind in ("frac", "fracg"):
        g = r5859(rule, A, F(100, d["k"]), "other", B=d["B"],
                  note=rf"\(\frac{{1}}{{{d['k']}}}\) of the outlay is \({tex(F(100, d['k']))}\%\).")
        return g, q, gopts(g["answer"][1])
    if kind == "other":
        g = r5859(rule, A, x, "other", B=d["B"])
        return g, q, gopts(g["answer"][1])
    g = r5859(rule, A, x, kind, y=F(d["y"]))
    return g, q, (iopts(g) if kind == "incr" else ropts(g["answer"][1]))


MOVED = {60: 1}


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None
    rows = {r["id"]: r for r in dump["rows"]}
    assert set(OLD[rule]) <= set(rows)  # row 369 moved to Rule 61 on 2026-10-30 (it is that rule's book example)
    out = []
    for rid, spec in OLD[rule].items():
        g, q, (op, _) = build(rule, rid, spec)
        extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
    _k[0] += MOVED.get(rule, 0)  # row 369 used an answer position here before it moved; keeps the applied files reproducible
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, key, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        kind, v = g["answer"]
        answers.append([key, [kind, [str(t) for t in v] if kind == "pair" else str(v)]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (57, 58, 59, 60):
        main(r)
