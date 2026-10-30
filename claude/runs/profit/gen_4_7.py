"""Profit and Loss Rules 4-7 (2026-10-30): price cut -> more for the same money (4), price rise -> less for the same money (5),
"buys x for Rs y, sells y for Rs x" (6) and "buys a for Rs b, sells c for Rs d" (7). Writes the four cards and regenerates the
32 old rows (every one a copy of a book example or exercise) in the prompt #14 layout with a simple-style sentence, a new setting
and all-new numbers (checked with gate_check.py). Every book exercise of these rules already has a copy, so there are no new
questions. Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, Rs, m, result  # noqa: E402


def pair_opts(a, b, wrong):
    fmt = lambda t: rf"Rs \({m(t[0])}\), Rs \({m(t[1])}\)"
    vals = [(a, b)] + wrong
    return [fmt(t) for t in vals]


def place(right, others, pos):
    o = list(others)
    o.insert(pos - 1, right)
    return dict(zip("abcd", o))


# ---------------------------------------------------------------- Rule 4: price cut
T4 = (r"If a reduction of \(x\%\) in the price of an article lets a person buy \(n\) units more for Rs \(A\), then the reduced and the "
      r"original prices per unit are<br>\[ \frac{Ax}{100n}\qquad\text{and}\qquad \frac{Ax}{(100-x)n} \]")


def r4(x, n, A, ask="both", unit="kg"):
    x, n, A = F(x), F(n), F(A)
    saved = A * x / 100
    red = saved / n
    orig = red * 100 / (100 - x)
    trad = steps(
        ("Money saved by the cut.", rf"Each rupee of the old bill now costs only \({tex(100 - x)}\) paise, so on Rs \({m(A)}\) the buyer saves \(\frac{{{tex(x)}}}{{100}}\times {m(A)} = "
                                    rf"{m(saved)}\) rupees."),
        ("The saving buys the extra units.", rf"That Rs \({m(saved)}\) pays for the \({tex(n)}\) extra {unit} at the new price, so the new price is "
                                             rf"\[ \frac{{{m(saved)}}}{{{tex(n)}}} = {m(red)} \]"),
        ("Go back to the old price.", rf"The new price is \({tex(100 - x)}\%\) of the old one: \[ {m(red)}\times\frac{{100}}{{{tex(100 - x)}}} = {m(orig)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(n = {tex(n)}\), \(A = {m(A)}\)."),
        ("Apply the specified rule.", r"\[ \text{Reduced price}=\frac{Ax}{100n},\qquad \text{Original price}=\frac{Ax}{(100-x)n} \]"),
        ("Substitute the values.", rf"\[ \frac{{{m(A)}\times {tex(x)}}}{{100\times {tex(n)}}} = {m(red)},\qquad \frac{{{m(A)}\times {tex(x)}}}{{{tex(100 - x)}\times {tex(n)}}} = {m(orig)} \]"))
    if ask == "both":
        fin, ans = rf"reduced price Rs \({m(red)}\), original price Rs \({m(orig)}\) per {unit}", ("pair", (red, orig))
    elif ask == "orig":
        fin, ans = rf"Rs \({m(orig)}\) per {unit}", ("number", orig)
    else:
        fin, ans = rf"Rs \({m(red)}\) per {unit}", ("number", red)
    rb = [rf"\(x = {tex(x)}\), \(n = {tex(n)}\), \(A = {m(A)}\).", rf"Reduced \(= \frac{{Ax}}{{100n}} = {m(red)}\).", rf"Original \(= \frac{{Ax}}{{(100-x)n}} = {m(orig)}\)."]
    sc = rf"\[ \frac{{{m(A)}\times {tex(x)}}}{{100\times {tex(n)}}} = {m(red)},\quad \frac{{{m(A)}\times {tex(x)}}}{{{tex(100 - x)}\times {tex(n)}}} = {m(orig)} \]"
    return result(ans, T4, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 5: price rise
T5 = (r"If a rise of \(x\%\) in the price of an article makes a person buy \(n\) units less for Rs \(A\), then the new and the original "
      r"prices per unit are<br>\[ \frac{Ax}{100n}\qquad\text{and}\qquad \frac{Ax}{(100+x)n} \]")


def r5(x, n, A, ask="both", unit="kg"):
    x, n, A = F(x), F(n), F(A)
    new = A * x / (100 * n)
    orig = new * 100 / (100 + x)
    lost = A * x / (100 + x)
    trad = steps(
        ("Let the old price be Rs \\(p\\) per " + unit + ".", rf"Rs \({m(A)}\) bought \(\frac{{{m(A)}}}{{p}}\) {unit}; at the new price \({tex(100 + x)}\%\) of \(p\) it buys "
                                                           rf"\(\frac{{{m(A)}\times 100}}{{{tex(100 + x)}p}}\) {unit}."),
        ("The difference is the units lost.", rf"\[ \frac{{{m(A)}}}{{p}} - \frac{{{m(A * 100)}}}{{{tex(100 + x)}p}} = {tex(n)} \;\Rightarrow\; \frac{{{m(lost)}}}{{p}} = {tex(n)} "
                                              rf"\;\Rightarrow\; p = {m(orig)} \]"),
        ("Find the new price.", rf"\[ {m(orig)}\times\frac{{{tex(100 + x)}}}{{100}} = {m(new)} \]"))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(n = {tex(n)}\), \(A = {m(A)}\)."),
        ("Apply the specified rule.", r"\[ \text{New price}=\frac{Ax}{100n},\qquad \text{Original price}=\frac{Ax}{(100+x)n} \]"),
        ("Substitute the values.", rf"\[ \frac{{{m(A)}\times {tex(x)}}}{{100\times {tex(n)}}} = {m(new)},\qquad \frac{{{m(A)}\times {tex(x)}}}{{{tex(100 + x)}\times {tex(n)}}} = {m(orig)} \]"))
    if ask == "both":
        fin, ans = rf"new price Rs \({m(new)}\), original price Rs \({m(orig)}\) per {unit}", ("pair", (new, orig))
    else:
        fin, ans = rf"Rs \({m(orig)}\) per {unit}", ("number", orig)
    rb = [rf"\(x = {tex(x)}\), \(n = {tex(n)}\), \(A = {m(A)}\).", rf"New \(= \frac{{Ax}}{{100n}} = {m(new)}\).", rf"Original \(= \frac{{Ax}}{{(100+x)n}} = {m(orig)}\)."]
    sc = rf"\[ \frac{{{m(A)}\times {tex(x)}}}{{100\times {tex(n)}}} = {m(new)},\quad \frac{{{m(A)}\times {tex(x)}}}{{{tex(100 + x)}\times {tex(n)}}} = {m(orig)} \]"
    return result(ans, T5, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rules 6-7: bought at one rate, sold at another
T6 = (r"If a man buys \(x\) articles for Rs \(y\) and sells \(y\) articles for Rs \(x\), his profit or loss is<br>"
      r"\[ \frac{x^2-y^2}{y^2}\times 100\% \]a profit if the sign is positive and a loss if it is negative.")
T7 = (r"If a man buys \(a\) articles for Rs \(b\) and sells \(c\) articles for Rs \(d\), his gain or loss is<br>"
      r"\[ \frac{ad-bc}{bc}\times 100\% \]a gain if the sign is positive and a loss if it is negative.")


def rates(a, b, c, d, n, item):
    """Buys a for Rs b, sells c for Rs d (Rule 6 when a = d and b = c)."""
    a, b, c, d = F(a), F(b), F(c), F(d)
    cp, sp = b / a, d / c
    v = (a * d - b * c) / (b * c) * 100
    word = "gain" if v > 0 else "loss"
    trad = steps(
        ("Cost of one article.", rf"\({tex(a)}\) for Rs \({m(b)}\): one costs Rs \(\frac{{{m(b)}}}{{{tex(a)}}}\)."),
        ("Selling price of one article.", rf"\({tex(c)}\) for Rs \({m(d)}\): one sells for Rs \(\frac{{{m(d)}}}{{{tex(c)}}}\)."),
        (f"Find the {word} per cent.", rf"\[ \frac{{\frac{{{m(d)}}}{{{tex(c)}}} - \frac{{{m(b)}}}{{{tex(a)}}}}}{{\frac{{{m(b)}}}{{{tex(a)}}}}}\times 100 = {tex(v)}\% \]"))
    if n == 6:
        rule = steps(
            ("Identify the values.", rf"\(x = {tex(a)}\), \(y = {tex(b)}\)."),
            ("Apply the specified rule.", r"\[ \frac{x^2-y^2}{y^2}\times 100\% \]"),
            ("Substitute the values.", rf"\[ \frac{{{tex(a)}^2 - {tex(b)}^2}}{{{tex(b)}^2}}\times 100 = \frac{{{tex(a * a - b * b)}}}{{{tex(b * b)}}}\times 100 = {tex(v)}\% \]"))
        sc = rf"\[ \frac{{{tex(a)}^2 - {tex(b)}^2}}{{{tex(b)}^2}}\times 100 = {tex(v)}\% \]"
        rb = [rf"\(x = {tex(a)}\), \(y = {tex(b)}\).", r"\(\frac{x^2-y^2}{y^2}\times 100\%\).", rf"\(\frac{{{tex(a * a - b * b)}}}{{{tex(b * b)}}}\times 100 = {tex(v)}\%\)."]
    else:
        rule = steps(
            ("Identify the values.", rf"\(a = {tex(a)}\), \(b = {tex(b)}\), \(c = {tex(c)}\), \(d = {tex(d)}\)."),
            ("Apply the specified rule.", r"\[ \frac{ad-bc}{bc}\times 100\% \]"),
            ("Substitute the values.", rf"\[ \frac{{{tex(a)}\times {tex(d)} - {tex(b)}\times {tex(c)}}}{{{tex(b)}\times {tex(c)}}}\times 100 = \frac{{{tex(a * d - b * c)}}}{{{tex(b * c)}}}\times 100 = {tex(v)}\% \]"))
        sc = rf"\[ \frac{{{tex(a * d)} - {tex(b * c)}}}{{{tex(b * c)}}}\times 100 = {tex(v)}\% \]"
        rb = [rf"\(a = {tex(a)}\), \(b = {tex(b)}\), \(c = {tex(c)}\), \(d = {tex(d)}\).", r"\(\frac{ad-bc}{bc}\times 100\%\).",
              rf"\(\frac{{{tex(a * d - b * c)}}}{{{tex(b * c)}}}\times 100 = {tex(v)}\%\)."]
    fin = rf"a {word} of \({tex(abs(v))}\%\)"
    return result(("signed", v), T6 if n == 6 else T7, trad, rule, fin, rb, sc)


def gl(v):
    """Signed options: right one, other direction, two wrong sizes."""
    v = F(v)
    w, o = ("Gain", "Loss") if v > 0 else ("Loss", "Gain")
    s = abs(v)
    return [rf"{w} of \({tex(s)}\%\)", rf"{o} of \({tex(s)}\%\)", rf"{w} of \({tex(s + 4)}\%\)", rf"{w} of \({tex(s * 2)}\%\)"]


# ---------------------------------------------------------------- cards
CARDS = {
    4: card(4, "A Price Cut Buys More for the Same Money",
            r"When the price falls by \(x\%\), the money saved on a fixed bill of Rs \(A\) buys the extra \(n\) units. That gives the new price, "
            r"and the old price follows from it.",
            r"\[ \text{Reduced price}=\frac{Ax}{100n},\qquad \text{Original price}=\frac{Ax}{(100-x)n} \]",
            [("Money saved on the bill", r"\frac{Ax}{100}"), ("It buys n units at the new price", r"\frac{Ax}{100n}"),
             ("New price is (100 - x)% of the old", r"\frac{Ax}{(100-x)n}")],
            r"The buyer spends the same Rs \(A\). The part of it freed by the cut, \(x\%\) of \(A\), is exactly what the extra units cost at the new price.",
            "'A reduction of x% in the price enables a person to buy n kg more for Rs A; find the reduced (and the original) price.'",
            r"\(25\%\) cut, \(5\) kg more for Rs \(60\): reduced \(=\frac{60\times 25}{100\times 5}=\text{Rs }3\), original \(=\frac{60\times 25}{75\times 5}=\text{Rs }4\).",
            r"Dividing the saving by \(n\) and calling it the ORIGINAL price - the saving buys the extra units at the REDUCED price."),
    5: card(5, "A Price Rise Buys Less for the Same Money",
            r"When the price rises by \(x\%\), a fixed bill of Rs \(A\) buys \(n\) units less. The new price and the old price both follow.",
            r"\[ \text{New price}=\frac{Ax}{100n},\qquad \text{Original price}=\frac{Ax}{(100+x)n} \]",
            [("Extra money needed for the old quantity", r"\frac{Ax}{100}"), ("Equal to n units at the new price", r"\frac{Ax}{100n}"),
             ("Old price is the new one divided by (100 + x)%", r"\frac{Ax}{(100+x)n}")],
            r"To buy the old quantity at the new price would need \(x\%\) more money, \(\frac{Ax}{100}\); that missing money is the cost of the \(n\) units given up.",
            "'A hike of x% in the price forces a person to buy n kg less for Rs A; find the new (and the original) price.'",
            r"\(20\%\) rise, \(3\) kg less for Rs \(72\): new \(=\frac{72\times 20}{100\times 3}=\text{Rs }4.80\), original \(=\frac{72\times 20}{120\times 3}=\text{Rs }4\).",
            r"Using \(100-x\) in place of \(100+x\) (that belongs to a price cut, Rule 4)."),
    6: card(6, "Buys x for Rs y, Sells y for Rs x",
            r"If \(x\) articles are bought for Rs \(y\) and \(y\) articles are sold for Rs \(x\), the gain or loss per cent depends only on \(x\) and \(y\).",
            r"\[ \frac{x^2-y^2}{y^2}\times 100\%\quad(\text{gain if positive, loss if negative}) \]",
            [("Cost of one", r"\frac{y}{x}"), ("Selling price of one", r"\frac{x}{y}"), ("Compare", r"\frac{x/y - y/x}{y/x}=\frac{x^2-y^2}{y^2}")],
            r"One article costs \(\frac{y}{x}\) and sells for \(\frac{x}{y}\); the ratio of the two prices is \(\frac{x^2}{y^2}\).",
            "'A man purchases x items for Rs y and sells y items for Rs x; find his profit or loss per cent.'",
            r"Buys \(9\) for Rs \(8\), sells \(8\) for Rs \(9\): \(\frac{81-64}{64}\times 100 = 26\frac{9}{16}\%\) gain.",
            r"Swapping \(x\) and \(y\) in the denominator - it is the square of the rupees paid, \(y^2\)."),
    7: card(7, "Buys a for Rs b, Sells c for Rs d",
            r"If \(a\) articles are bought for Rs \(b\) and \(c\) articles are sold for Rs \(d\), compare the cost and the selling price of one article.",
            r"\[ \frac{ad-bc}{bc}\times 100\%\quad(\text{gain if positive, loss if negative}) \]",
            [("Cost of one", r"\frac{b}{a}"), ("Selling price of one", r"\frac{d}{c}"), ("Per cent change", r"\frac{d/c-b/a}{b/a}\times 100=\frac{ad-bc}{bc}\times 100")],
            r"Rule 6 is the special case \(a = d\), \(b = c\). The per cent is always on the cost of one article, \(\frac{b}{a}\).",
            "'A person buys a items for Rs b and sells them at c for Rs d; what does he gain or lose per cent?'",
            r"Buys \(5\) for Rs \(6\), sells \(4\) for Rs \(6\): \(\frac{5\times 6-6\times 4}{6\times 4}\times 100=25\%\) gain.",
            r"Comparing the totals (Rs \(b\) with Rs \(d\)) although the two counts \(a\) and \(c\) are different."),
}

PA = lambda a, b, wrong, pos: place(pair_opts(a, b, [])[0], pair_opts(a, b, wrong)[1:], pos)

OLD = {
    4: {290: (lambda: r4(40, 15, 216), r"A cut of 40% in the price of dal lets a cook buy 15 kg more for Rs 216. Find the reduced price and the original price per kg.",
              PA(F(144, 25), F(48, 5), [(F(48, 5), F(144, 25)), (F(144, 25), 12), (F(24, 5), F(48, 5))], 2)),
        932: (lambda: r4(25, 5, 246, "orig"), r"When the price of tea falls by 25%, a family can buy 5 kg more for Rs 246. What was the price per kg before the fall?",
              place(Rs(F(82, 5)), [Rs(F(123, 10)), Rs(18), Rs(F(41, 2))], 4)),
        933: (lambda: r4(10, 3, 81, "orig"), r"Because the price of salt goes down by 10%, a hotel buys 3 kg more for Rs 81. Find the old price of salt per kg.",
              place(Rs(3), [Rs(F(27, 10)), Rs(F(33, 10)), Rs(4)], 1)),
        934: (lambda: r4(20, 6, 90), r"A 20% fall in the price of sugar allows a shop to buy 6 kg more for Rs 90. Find the reduced price and the original price per kg.",
              PA(3, F(15, 4), [(F(15, 4), 3), (3, 4), (F(5, 2), F(15, 4))], 3)),
        935: (lambda: r4(50, 6, 153), r"With a 50% drop in the price of flour, a baker gets 6 kg more for Rs 153. What are the reduced price and the original price per kg?",
              PA(F(51, 4), F(51, 2), [(F(51, 2), F(51, 4)), (F(51, 4), 30), (10, F(51, 2))], 4)),
        936: (lambda: r4(40, 12, 180), r"When the price of rice is cut by 40%, a mess buys 12 kg more for Rs 180. Find the reduced price and the original price per kg.",
              PA(6, 10, [(10, 6), (6, 9), (5, 10)], 1)),
        937: (lambda: r4(15, 6, 136), r"A fall of 15% in the price of wheat lets a farmer buy 6 kg more for Rs 136. Find the reduced price and the original price per kg.",
              PA(F(17, 5), 4, [(4, F(17, 5)), (F(17, 5), 5), (3, 4)], 2)),
        938: (lambda: r4(40, 4, 222), r"A potter finds that a 40% cut in the price of clay lets him get 4 kg more for Rs 222. What are the reduced price and the original price per kg?",
              PA(F(111, 5), 37, [(37, F(111, 5)), (F(111, 5), 40), (20, 37)], 3)),
        941: (lambda: r4(30, 16, 168, unit="orange"), r"A 30% cut in the price of oranges lets a buyer get 16 more oranges for Rs 168. Find the reduced price and the original price of one orange.",
              PA(F(63, 20), F(9, 2), [(F(9, 2), F(63, 20)), (F(63, 20), 5), (3, F(9, 2))], 4)),
        942: (lambda: r4(12, 3, 44, unit="sweet"), r"If the price of sweets came down by 12%, a child could get 3 more sweets for Rs 44. Find the reduced price and the original price of one sweet.",
              PA(F(44, 25), 2, [(2, F(44, 25)), (F(44, 25), F(5, 2)), (F(3, 2), 2)], 1)),
        943: (lambda: r4(5, 5, 323, "red", unit="banana"), r"A 5% fall in the price of bananas would let a buyer get 5 more bananas for Rs 323. What is the reduced price of one banana?",
              place(Rs(F(323, 100)), [Rs(F(17, 5)), Rs(3), Rs(F(323, 50))], 2))},
    5: {291: (lambda: r5(20, 3, 72), r"After a 20% rise in the price of sugar, a family gets 3 kg less for Rs 72. Find the new price and the old price per kg.",
              PA(F(24, 5), 4, [(4, F(24, 5)), (F(24, 5), 5), (6, 4)], 3)),
        939: (lambda: r5(10, 2, 198, "orig"), r"Because the price of rice went up by 10%, a man gets 2 kg less for Rs 198. What was the price per kg before the rise?",
              place(Rs(9), [Rs(F(99, 10)), Rs(8), Rs(11)], 4)),
        940: (lambda: r5(10, 5, 66, "orig"), r"A 10% increase in the price of onions means a cook buys 5 kg less for Rs 66. Find the original price of onions per kg.",
              place(Rs(F(6, 5)), [Rs(F(33, 25)), Rs(1), Rs(F(3, 2))], 1)),
        944: (lambda: r5(50, 3, 54, "orig"), r"When the price of dal goes up by 50%, a hostel gets 3 kg less for Rs 54. What was the old price of dal per kg?",
              place(Rs(6), [Rs(9), Rs(5), Rs(F(9, 2))], 2)),
        945: (lambda: r5(40, 4, 98, "orig"), r"After the price of coffee rises by 40%, a shop buys 4 kg less for Rs 98. Find the original price of coffee per kg.",
              place(Rs(7), [Rs(F(49, 5)), Rs(6), Rs(8)], 3))},
    6: {292: (lambda: rates(21, 28, 28, 21, 6, "pencil"), r"For every 21 pencils a man pays Rs 28, and he sells 28 pencils for Rs 21. What per cent does he gain or lose?",
              place(*(lambda o: (o[0], o[1:]))(gl(F(-175, 4))), 2)),
        946: (lambda: rates(20, 16, 16, 20, 6, "lemon"), r"A vendor buys 20 lemons for Rs 16 and sells 16 lemons for Rs 20. Find his gain or loss per cent.",
              place(*(lambda o: (o[0], o[1:]))(gl(F(225, 4))), 4)),
        947: (lambda: rates(30, 25, 25, 30, 6, "egg"), r"A shop buys 30 eggs for Rs 25 and sells 25 eggs for Rs 30. What is its gain or loss per cent?",
              place(*(lambda o: (o[0], o[1:]))(gl(44)), 1)),
        948: (lambda: rates(8, 10, 10, 8, 6, "pen"), r"A boy buys 8 pens for Rs 10 and sells 10 pens for Rs 8. What is his gain or loss per cent?",
              place(*(lambda o: (o[0], o[1:]))(gl(-36)), 3)),
        949: (lambda: rates(9, 12, 12, 9, 6, "notebook"), r"A girl buys 9 notebooks for Rs 12 and sells 12 notebooks for Rs 9. Find her gain or loss per cent.",
              place(*(lambda o: (o[0], o[1:]))(gl(F(-175, 4))), 2)),
        950: (lambda: rates(6, 4, 4, 6, 6, "cake"), r"A baker buys 6 cakes for Rs 4 and sells 4 cakes for Rs 6. What is his gain or loss per cent?",
              place(*(lambda o: (o[0], o[1:]))(gl(125)), 4))},
    7: {293: (lambda: rates(3, 3, 10, 14, 7, "ribbon"), r"A girl buys 3 ribbons for Rs 3 and sells 10 ribbons for Rs 14. What is her gain or loss per cent?",
              place(*(lambda o: (o[0], o[1:]))(gl(40)), 1)),
        951: (lambda: rates(26, 14, 16, 7, 7, "apple"), r"Apples are bought at 26 for Rs 14 and sold at 16 for Rs 7. Is there a gain or a loss, and what per cent is it?",
              place(*(lambda o: (o[0], o[1:]))(gl(F(-75, 4))), 3)),
        952: (lambda: rates(27, 18, 16, 7, 7, "toffee"), r"A shop buys 27 toffees for Rs 18 and sells them at 16 for Rs 7. Find its gain or loss per cent.",
              place(*(lambda o: (o[0], o[1:]))(gl(F(-275, 8))), 2)),
        953: (lambda: rates(9, 25, 6, 18, 7, "chocolate"), r"Chocolates bought at 9 for Rs 25 are sold at 6 for Rs 18. What is the gain or loss per cent on them?",
              place(*(lambda o: (o[0], o[1:]))(gl(8)), 4)),
        954: (lambda: rates(5, 13, 8, 26, 7, "candle"), r"For every 5 candles a trader pays Rs 13, and he sells 8 candles for Rs 26. What per cent does he gain or lose?",
              place(*(lambda o: (o[0], o[1:]))(gl(25)), 1))},
}


def main():
    for n in (4, 5, 6, 7):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, op) in OLD[n].items():
            extra = {"question": question, **(op or {})}
            if rows[rid]["e"] is None or rows[rid]["e"].strip():
                extra["e"] = ""
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump({"rule_name": f"Rule {n}", "rule_html": CARDS[n]}, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written")


if __name__ == "__main__":
    main()
