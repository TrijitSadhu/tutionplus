"""Profit and Loss Rules 81-84 (2026-10-30). Rule 81: selling N articles gains the selling price of n - gain per cent. Rule 82: selling
N loses the selling price of n - loss per cent. Rule 83: selling N gains the cost of n - gain per cent. Rule 84: marked price A, x%
discount, y% gain on cost B, A(100 - x) = B(100 + y) - the price paid (from the rupee discount), the mark-up needed, the profit, or the
discount rate. None of the four has an old row; this writes the four cards and the book's examples and exercises as new questions
with new settings and all-new numbers. Usage: python gen_81_84.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, steps, tex  # noqa: E402
from gen_1_3 import P as PCT, m, result  # noqa: E402
from gen_13_17 import popts  # noqa: E402
from gen_18_21 import ropts  # noqa: E402

T81 = r"If selling \(N\) articles gains the selling price of \(n\) articles, the gain is<br>\[ \frac{n}{N-n}\times 100\% \]"
T82 = r"If selling \(N\) articles loses the selling price of \(n\) articles, the loss is<br>\[ \frac{n}{N+n}\times 100\% \]"
T83 = r"If selling \(N\) articles gains the cost price of \(n\) articles, the gain is<br>\[ \frac{n}{N}\times 100\% \]"
T84 = (r"If an article marked at Rs \(A\) is sold at a discount of \(x\%\) for a gain of \(y\%\) on its cost Rs \(B\), then"
       r"<br>\[ \frac{A(100-x)}{100}=\frac{B(100+y)}{100}=\text{selling price} \]")


def r_sp_gain(rule, N, n, unit):
    N, n = F(N), F(n)
    T = T81 if rule == 81 else T82
    if rule == 81:
        v = n / (N - n) * 100
        mid = (rf"Selling \({tex(N)}\) {unit} brings in their cost plus the price of \({tex(n)}\), so their cost is the price of \({tex(N)} - {tex(n)} = {tex(N - n)}\) {unit}.",
               rf"\[ \frac{{{tex(n)}}}{{{tex(N - n)}}}\times 100 = {tex(v)}\% \]")
        sub, word = rf"\[ \frac{{{tex(n)}}}{{{tex(N)} - {tex(n)}}}\times 100 = {tex(v)}\% \]", "gain"
    else:
        v = n / (N + n) * 100
        mid = (rf"Selling \({tex(N)}\) {unit} brings in their cost less the price of \({tex(n)}\), so their cost is the price of \({tex(N)} + {tex(n)} = {tex(N + n)}\) {unit}.",
               rf"\[ \frac{{{tex(n)}}}{{{tex(N + n)}}}\times 100 = {tex(v)}\% \]")
        sub, word = rf"\[ \frac{{{tex(n)}}}{{{tex(N)} + {tex(n)}}}\times 100 = {tex(v)}\% \]", "loss"
    trad = steps(("Take the price of one as Re 1.", mid[0]), (f"The {word} is the price of {tex(n)} on that cost.", mid[1]))
    rule_s = steps(("Identify the values.", rf"\(N = {tex(N)}\), \(n = {tex(n)}\)."), ("Apply the specified rule.", T.split("<br>")[1]),
                   ("Substitute the values.", sub))
    rb = [rf"\(N = {tex(N)}\), \(n = {tex(n)}\).", rf"{word.capitalize()} \(= {tex(v)}\%\).", rf"So the {word} is \({tex(v)}\%\)."]
    return result(("number", v), T, trad, rule_s, PCT(v), rb, sub)


def r83(N, n, unit):
    N, n = F(N), F(n)
    v = n / N * 100
    trad = steps(("Take the cost of one as Re 1.", rf"\({tex(N)}\) {unit} cost Rs \({tex(N)}\); the gain is the cost of \({tex(n)}\), i.e. Rs \({tex(n)}\)."),
                 ("Gain per cent.", rf"\[ \frac{{{tex(n)}}}{{{tex(N)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(N = {tex(N)}\), \(n = {tex(n)}\)."), ("Apply the specified rule.", T83.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(n)}}}{{{tex(N)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(N = {tex(N)}\), \(n = {tex(n)}\).", rf"\(\frac{{n}}{{N}}\times 100\).", rf"Gain \(= {tex(v)}\%\)."]
    return result(("number", v), T83, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(n)}}}{{{tex(N)}}}\times 100 = {tex(v)}\% \]")


def r84(kind, a, b):
    """kind 'paid': a = discount %, b = rupee saving; 'markup': a = discount %, b = gain %; 'profit': a = mark-up %, b = discount %;
    'discount': a = mark-up %, b = gain %."""
    a, b = F(a), F(b)
    if kind == "paid":
        x, D = a, b
        A = D * 100 / x
        sp = A - D
        trad = steps(("The saving is the discount.", rf"\({tex(x)}\%\) of the marked price \(= {m(D)}\), so the marked price \(= {m(D)}\times\frac{{100}}{{{tex(x)}}} = {m(A)}\)."),
                     ("Price paid.", rf"\[ {m(A)} - {m(D)} = {m(sp)} \]"))
        rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), the discount in rupees \(A - \frac{{A(100-x)}}{{100}} = {m(D)}\)."),
                     ("Apply the specified rule.", T84.split("<br>")[1]),
                     ("Substitute the values.", rf"\[ \frac{{{tex(x)}}}{{100}}A = {m(D)} \;\Rightarrow\; A = {m(A)},\qquad \frac{{{m(A)}\times {tex(100 - x)}}}{{100}} = {m(sp)} \]"))
        rb = [rf"\(\frac{{{tex(x)}}}{{100}}A = {m(D)}\).", rf"\(A = {m(A)}\).", rf"Paid \(= {m(sp)}\)."]
        return result(("number", sp), T84, trad, rule, rf"Rs \({m(sp)}\)", rb, rf"\[ {m(A)} - {m(D)} = {m(sp)} \]")
    if kind == "markup":
        x, y = a, b
        v = (100 + y) / (100 - x) * 100 - 100
        trad = steps(("Take the cost price as 100.", rf"The selling price must be \({tex(100 + y)}\), which is \({tex(100 - x)}\%\) of the marked price."),
                     ("Marked price.", rf"\[ {tex(100 + y)}\times\frac{{100}}{{{tex(100 - x)}}} = {tex(100 + v)} \]"),
                     ("Mark-up.", rf"\[ {tex(100 + v)} - 100 = {tex(v)}\% \]"))
        rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), cost \(B = 100\)."), ("Apply the specified rule.", T84.split("<br>")[1]),
                     ("Substitute the values.", rf"\[ A\times {tex(100 - x)} = 100\times {tex(100 + y)} \;\Rightarrow\; A = {tex(100 + v)},\ \text{{i.e. }}{tex(v)}\%\text{{ above the cost}} \]"))
        rb = [rf"\(A({tex(100 - x)}) = 100({tex(100 + y)})\).", rf"\(A = {tex(100 + v)}\).", rf"Mark-up \(= {tex(v)}\%\)."]
        return result(("number", v), T84, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(100 + y)}}}{{{tex(100 - x)}}}\times 100 - 100 = {tex(v)}\% \]")
    if kind == "profit":
        up, x = a, b
        v = (100 + up) * (100 - x) / 100 - 100
        trad = steps(("Take the cost price as 100.", rf"Marked price \(= {tex(100 + up)}\); after \({tex(x)}\%\) off: \({tex((100 + up) * (100 - x) / 100)}\)."),
                     ("Profit per cent.", rf"\[ {tex((100 + up) * (100 - x) / 100)} - 100 = {tex(v)}\% \]"))
        rule = steps(("Identify the values.", rf"\(A = {tex(100 + up)}\) on a cost \(B = 100\), \(x = {tex(x)}\)."), ("Apply the specified rule.", T84.split("<br>")[1]),
                     ("Substitute the values.", rf"\[ \frac{{{tex(100 + up)}\times {tex(100 - x)}}}{{100}} = 100 + y \;\Rightarrow\; y = {tex(v)} \]"))
        rb = [rf"\(A = {tex(100 + up)}\), \(B = 100\).", rf"Selling price \(= {tex(100 + v)}\).", rf"Profit \(= {tex(v)}\%\)."]
        return result(("number", v), T84, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(100 + up)}\times {tex(100 - x)}}}{{100}} - 100 = {tex(v)}\% \]")
    up, y = a, b
    v = 100 - (100 + y) / (100 + up) * 100
    trad = steps(("Take the cost price as 100.", rf"Marked price \(= {tex(100 + up)}\); selling price \(= {tex(100 + y)}\)."),
                 ("Discount on the marked price.", rf"\[ \frac{{{tex(100 + up)} - {tex(100 + y)}}}{{{tex(100 + up)}}}\times 100 = {tex(v)}\% \]"))
    rule = steps(("Identify the values.", rf"\(A = {tex(100 + up)}\) on a cost \(B = 100\), \(y = {tex(y)}\)."), ("Apply the specified rule.", T84.split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{tex(100 + up)}(100 - x)}}{{100}} = {tex(100 + y)} \;\Rightarrow\; x = {tex(v)} \]"))
    rb = [rf"\(A = {tex(100 + up)}\), SP \(= {tex(100 + y)}\).", rf"Discount \(= {tex(100 + up - 100 - y)}\) on \({tex(100 + up)}\).", rf"Rate \(= {tex(v)}\%\)."]
    return result(("number", v), T84, trad, rule, PCT(v), rb, rf"\[ \frac{{{tex(up - y)}}}{{{tex(100 + up)}}}\times 100 = {tex(v)}\% \]")


CARDS = {
    81: card(81, "Selling N Gains the Selling Price of n",
             r"If the gain on \(N\) articles equals the price of \(n\) of them, the cost of the \(N\) is the price of \(N-n\).",
             r"\[ \text{Gain}=\frac{n}{N-n}\times 100\% \]",
             [("Takings", r"N"), ("Cost", r"N-n"), ("Gain", r"\frac{n}{N-n}\times 100")],
             r"The gain per cent is on the cost, which is the price of \(N-n\) articles.",
             "'By selling N metres of cloth I gain the selling price of n metres. Find the gain per cent.'",
             r"\(40\) sold, gain \(=\) price of \(10\): \(\frac{10}{30}\times 100=33\frac{1}{3}\%\).",
             r"Dividing by \(N\) instead of \(N-n\)."),
    82: card(82, "Selling N Loses the Selling Price of n",
             r"If the loss on \(N\) articles equals the price of \(n\) of them, the cost of the \(N\) is the price of \(N+n\).",
             r"\[ \text{Loss}=\frac{n}{N+n}\times 100\% \]",
             [("Takings", r"N"), ("Cost", r"N+n"), ("Loss", r"\frac{n}{N+n}\times 100")],
             r"The loss per cent is on the cost, which is the price of \(N+n\) articles.",
             "'By selling N metres of cloth I lose the selling price of n metres. Find the loss per cent.'",
             r"\(30\) sold, loss \(=\) price of \(10\): \(\frac{10}{40}\times 100=25\%\).",
             r"Dividing by \(N\) or by \(N-n\)."),
    83: card(83, "Selling N Gains the Cost of n",
             r"If the gain on \(N\) articles equals the cost of \(n\) of them, the gain is \(n\) parts of a cost of \(N\) parts.",
             r"\[ \text{Gain}=\frac{n}{N}\times 100\% \]",
             [("Cost", r"N"), ("Gain", r"n"), ("Gain %", r"\frac{n}{N}\times 100")],
             r"Compare Rule 81: there the gain is the selling price of \(n\), here it is the cost of \(n\).",
             "'By selling N metres of cloth a person gains the cost price of n metres. Find the gain per cent.'",
             r"\(50\) sold, gain \(=\) cost of \(10\): \(\frac{10}{50}\times 100=20\%\).",
             r"Dividing by \(N-n\)."),
    84: card(84, "Marked Price, Discount and Gain Together",
             r"The selling price is \((100-x)\%\) of the marked price \(A\) and also \((100+y)\%\) of the cost \(B\); either side gives the other.",
             r"\[ A(100-x)=B(100+y) \]",
             [("From the mark", r"\frac{A(100-x)}{100}"), ("From the cost", r"\frac{B(100+y)}{100}"), ("Equal", r"\text{selling price}")],
             r"Discount is on the marked price; gain is on the cost.",
             "'How much above the cost should goods be marked to gain y% after x% discount?' / 'A discount of x% saves Rs D; what was paid?'",
             r"\(10\%\) off, \(17\%\) gain: \(A\times 90=B\times 117\), \(A=1.3B\), i.e. \(30\%\) above the cost.",
             r"Taking the discount on the cost price."),
}
QSP = {81: "A draper sells {N} metres of {item}, and his profit equals what he gets for {n} metres. What is his profit per cent?",
       82: "A draper sells {N} metres of {item}, and his loss equals what he gets for {n} metres. What is his loss per cent?"}
Q83 = "A draper sells {N} metres of {item}; his profit is equal to the cost of {n} metres. What is his profit per cent?"
Q84 = {"paid": "A {x}% discount on the marked price of a {item} saves a woman Rs {D}, just the price of a {other}. How much did she pay for the {item}?",
       "markup": "By what per cent above the cost price should a shop mark its goods to make a profit of {y}% after giving a discount of {x}%?",
       "profit": "A shop marks its goods {up}% above the cost price and gives a discount of {x}%. What is its profit per cent?",
       "discount": "A shop marks its goods {up}% above the cost price and still makes a profit of {y}% after a discount. What is the rate of discount?"}
NEW = {81: [("r81_ex", ("silk", 40, 8)), ("r81_e1", ("cotton", 27, 9)), ("r81_e2", ("lace", 33, 3)), ("r81_e3", ("ribbon", 52, 12))],
       82: [("r82_ex", ("wool", 36, 4)), ("r82_e1", ("linen", 70, 30)), ("r82_e2", ("satin", 42, 14)), ("r82_e3", ("muslin", 56, 8)),
            ("r82_e4", ("denim", 88, 12))],
       83: [("r83_ex", ("velvet", 45, 9)), ("r83_e1", ("chiffon", 64, 16)), ("r83_e2", ("khadi", 80, 12)), ("r83_e3", ("tweed", 72, 12)),
            ("r83_e4", ("canvas", 120, 27))],
       84: [("r84_ex", ("paid", 15, 54, "jacket", "cap")), ("r84_e1", ("markup", 8, 15)), ("r84_e2", ("profit", 40, 20)),
            ("r84_e3", ("discount", 25, 10)), ("r84_e4", ("markup", 12, 32))]}


def build(rule, spec):
    if rule in (81, 82):
        item, N, n = spec
        g = r_sp_gain(rule, N, n, "metres")
        return g, QSP[rule].format(N=N, n=n, item=item), popts(g["answer"][1])
    if rule == 83:
        item, N, n = spec
        g = r83(N, n, "metres")
        return g, Q83.format(N=N, n=n, item=item), popts(g["answer"][1])
    kind, a, b, *rest = spec
    g = r84(kind, a, b)
    if kind == "paid":
        q = Q84[kind].format(x=a, D=b, item=rest[0], other=rest[1])
        return g, q, ropts(g["answer"][1])
    q = Q84[kind].format(x=a if kind == "markup" else b, y=b, up=a)
    return g, q, popts(g["answer"][1])


def main(rule):
    folder = os.path.join(HERE, f"rule{rule}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    assert dump["rule_card"] is None and dump["rows"] == []
    json.dump([], open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"))
    cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, spec in NEW[rule]:
        g, q, (op, pos) = build(rule, spec)
        qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {rule}: card written, {len(qs)} new questions")


if __name__ == "__main__":
    for r in (81, 82, 83, 84):
        main(r)
