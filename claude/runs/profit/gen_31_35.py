"""Profit and Loss Rules 31-35 (2026-10-30): cost and price both Rs A lower (31); a price cut that turns a profit into a loss (32)
or into a smaller profit (33); cost and price lowered (34) or raised (35) by different amounts. Writes the five cards, regenerates
the 6 old rows (324-328 copy the book; 962 is a copy of 324) and adds the 20 book exercises that had no copy (Rule 35's
exercises 3-5 are on the next book page and go with the next batch). Sentences: sent_31_35.py; numbers: PICKS (searched against
the book). Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402
import sent_31_35 as S  # noqa: E402

PICKS = {324: (6, 52, 13), 962: (15, 51, 9), "r31_e1": (17, 96, 12), "r31_e2": (6, 225, 10), "r31_e3": (15, 152, 4), "r31_e4": (5, 192, 20),
         "r31_e5": (33, 168, 6),
         325: (12, 7, 13), "r32_e1": (8, 23, 15), "r32_e2": (11, 4, 9), "r32_e3": (9, 27, 6), "r32_e4": (8, 6, 17), "r32_e5": (23, 35, 27),
         326: (36, 15, 26), "r33_e1": (42, 35, 28), "r33_e2": (24, 40, 4), "r33_e3": (19, 20, 14),
         327: (13, 50, 40, 3), "r34_e1": (16, 41, 13, 4), "r34_e2": (10, 39, 18, 5), "r34_e3": (35, 16, 13, 2), "r34_e4": (13, 56, 9, 2),
         "r34_e5": (16, 49, 35, 4),
         328: (33, 44, 14, 7), "r35_e1": (28, 33, 9, 2), "r35_e2": (20, 30, 12, 10)}

TH = {
    31: (r"If an article is sold at \(x\%\) profit and, with both the cost price and the selling price Rs \(A\) less, the profit per cent "
         r"would be \(y\) more, then<br>\[ \text{CP}=\frac{(x+y)A}{y} \]"),
    32: (r"If a dealer sells at a profit of \(x\%\) and cutting the price by \(X\) gives a loss of \(y\%\), then<br>"
         r"\[ \text{CP}=\frac{100X}{x+y},\qquad \text{first SP}=\frac{(100+x)X}{x+y} \]"),
    33: (r"If a dealer sells at a profit of \(x\%\) and cutting the price by \(X\) still gives a profit of \(y\%\), then<br>"
         r"\[ \text{CP}=\frac{100X}{x-y},\qquad \text{first SP}=\frac{(100+x)X}{x-y} \]"),
    34: (r"If an article is sold at \(P\%\) profit and lowering its cost by Rs \(c\) and its price by Rs \(s\) raises the profit per cent by "
         r"\(p\), then<br>\[ \text{CP}=\frac{c(P+p)-100(s-c)}{p} \]"),
    35: (r"If an article is sold at \(P\%\) profit and raising its cost by Rs \(c\) and its price by Rs \(s\) lowers the profit per cent by "
         r"\(p\), then<br>\[ \text{CP}=\frac{c(P-p)-100(s-c)}{p} \]"),
}


def M_(unit):
    return (lambda v: rf"\({m(v)}\) paise") if unit == "paise" else (lambda v: rf"Rs \({m(v)}\)")


def r31(x, A, y):
    x, A, y = map(F, (x, A, y))
    cp = A * (x + y) / y
    trad = steps(
        ("Let the cost price be Rs \\(c\\).", rf"Selling price \(= \frac{{{tex(100 + x)}}}{{100}}c\). New cost \(= c - {m(A)}\), new price \(= \frac{{{tex(100 + x)}}}{{100}}c - {m(A)}\)."),
        ("The new profit is " + tex(x + y) + "% of the new cost.", rf"The profit stays \(\frac{{{tex(x)}}}{{100}}c\) rupees, so"
                                                                  rf"\[ \frac{{{tex(x)}}}{{100}}c = \frac{{{tex(x + y)}}}{{100}}(c - {m(A)}) \;\Rightarrow\; {tex(y)}c = {tex(x + y)}\times {m(A)} \;\Rightarrow\; c = {m(cp)} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(A = {m(A)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", TH[31].split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{({tex(x)} + {tex(y)})\times {m(A)}}}{{{tex(y)}}} = {m(cp)} \]"))
    rb = [rf"\(x = {tex(x)}\), \(A = {m(A)}\), \(y = {tex(y)}\).", r"\(\text{CP} = \frac{(x+y)A}{y}\).", rf"\(\frac{{{tex(x + y)}\times {m(A)}}}{{{tex(y)}}} = {m(cp)}\)."]
    return result(("number", cp), TH[31], trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{{tex(x + y)}\times {m(A)}}}{{{tex(y)}}} = {m(cp)} \]")


def cut(n, x, X, y, ask, unit):
    x, X, y = map(F, (x, X, y))
    second = 100 - y if n == 32 else 100 + y
    d = (100 + x) - second
    cp = 100 * X / d
    sp = cp * (100 + x) / 100
    M = M_(unit)
    trad = steps(
        ("Take the cost price as 100.", rf"The first price is \({tex(100 + x)}\); after the cut it is \({tex(second)}\) (a {'loss' if n == 32 else 'profit'} of \({tex(y)}\%\))."),
        ("The cut is the gap.", rf"The cut, \({m(X)}\), is \({tex(d)}\) on every \(100\) of cost, so \[ \text{{CP}} = \frac{{{m(X)}}}{{{tex(d)}}}\times 100 = {m(cp)} \]"),
        ("The first selling price.", rf"\[ {m(cp)}\times\frac{{{tex(100 + x)}}}{{100}} = {m(sp)} \]"))
    den = "x+y" if n == 32 else "x-y"
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(X = {m(X)}\), \(y = {tex(y)}\)."), ("Apply the specified rule.", TH[n].split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \text{{CP}} = \frac{{100\times {m(X)}}}{{{tex(d)}}} = {m(cp)},\qquad \text{{first SP}} = \frac{{{tex(100 + x)}\times {m(X)}}}{{{tex(d)}}} = {m(sp)} \]"))
    if ask == "cpsp":
        fin, ans = rf"cost price {M(cp)}, first selling price {M(sp)}", ("pair", (cp, sp))
    else:
        fin, ans = M(sp), ("number", sp)
    rb = [rf"\(x = {tex(x)}\), \(X = {m(X)}\), \(y = {tex(y)}\).", rf"\({den} = {tex(d)}\), CP \(= {m(cp)}\).", rf"First SP \(= {m(sp)}\)."]
    return result(ans, TH[n], trad, rule, fin, rb, rf"\[ \frac{{100\times {m(X)}}}{{{tex(d)}}} = {m(cp)},\quad \frac{{{tex(100 + x)}\times {m(X)}}}{{{tex(d)}}} = {m(sp)} \]")


def shift2(n, P, c, s, p):
    P, c, s, p = map(F, (P, c, s, p))
    sign = -1 if n == 34 else 1                     # 34: both lowered, 35: both raised
    newP = P + p if n == 34 else P - p
    num = c * (P + p) - 100 * (s - c) if n == 34 else c * (P - p) - 100 * (s - c)
    cp = num / p
    trad = steps(
        ("Let the cost price be Rs \\(x\\).", rf"The selling price is \(\frac{{{tex(100 + P)}}}{{100}}x\). After the change the cost is \(x {'-' if n == 34 else '+'} {m(c)}\) and the price "
                                              rf"\(\frac{{{tex(100 + P)}}}{{100}}x {'-' if n == 34 else '+'} {m(s)}\)."),
        ("The new profit per cent is " + tex(newP) + ".", rf"\[ \frac{{{tex(100 + P)}}}{{100}}x {'-' if n == 34 else '+'} {m(s)} = \frac{{{tex(100 + newP)}}}{{100}}(x {'-' if n == 34 else '+'} {m(c)}) \]"),
        ("Solve.", rf"\[ x = {m(cp)} \]"))
    rule = steps(("Identify the values.", rf"\(P = {tex(P)}\), \(c = {m(c)}\), \(s = {m(s)}\), \(p = {tex(p)}\)."), ("Apply the specified rule.", TH[n].split("<br>")[1]),
                 ("Substitute the values.", rf"\[ \frac{{{m(c)}\times {tex(P + p if n == 34 else P - p)} - 100\times ({m(s)} - {m(c)})}}{{{tex(p)}}} = \frac{{{m(num)}}}{{{tex(p)}}} = {m(cp)} \]"))
    rb = [rf"\(P = {tex(P)}\), \(c = {m(c)}\), \(s = {m(s)}\), \(p = {tex(p)}\).", rf"Numerator \(= {m(num)}\).", rf"\(\frac{{{m(num)}}}{{{tex(p)}}} = {m(cp)}\)."]
    return result(("number", cp), TH[n], trad, rule, rf"Rs \({m(cp)}\)", rb, rf"\[ \frac{{{m(num)}}}{{{tex(p)}}} = {m(cp)} \]")


def build(key):
    n, tpl, ask = S.S[key]
    c = PICKS[key]
    q = tpl(*c)
    unit = "paise" if "paise" in q else "Rs"
    if n == 31:
        fn = lambda: r31(*c)
    elif n in (32, 33):
        fn = lambda: cut(n, *c, ask, unit)
    else:
        fn = lambda: shift2(n, *c)
    return n, q, fn, unit


def opts(g, unit):
    M = M_(unit)
    kind, v = g["answer"]
    if kind == "number":
        v = F(v)
        return place(M(v), [M(w) for w in (v * F(11, 10), v * F(9, 10), v * F(6, 5))])
    a, b = (F(t) for t in v)
    PP = lambda t: f"{M(t[0])}, {M(t[1])}"
    return place(PP((a, b)), [PP((b, a)), PP((a * F(11, 10), b)), PP((a, b * F(11, 10)))])


def card_(n, title, statement, visual, intuition, pattern, example, mistake):
    return card(n, title, statement, TH[n].split("<br>")[1], visual, intuition, pattern, example, mistake)


CARDS = {
    31: card_(31, "Cost and Price Both Rs A Lower",
              r"Lowering the cost price and the selling price by the same Rs \(A\) leaves the profit in rupees unchanged but raises the profit per cent.",
              [("Profit in rupees", r"\frac{x}{100}\text{CP}"), ("Same profit on the lower cost", r"\frac{x+y}{100}(\text{CP}-A)"), ("Solve", r"\text{CP}=\frac{(x+y)A}{y}")],
              r"The same rupee profit is a larger share of a smaller cost.",
              "'An article is sold at x% profit. If both the cost price and the selling price are Rs A less, the profit would be y% more. Find the cost price.'",
              r"\(6\%\), Rs \(52\), \(13\) more: \(\frac{19\times 52}{13}=\text{Rs }76\).",
              r"Using \(y\) as the new profit per cent - the new per cent is \(x+y\)."),
    32: card_(32, "A Price Cut Turns a Profit into a Loss",
              r"If a dealer selling at \(x\%\) profit cuts his price by \(X\) and then loses \(y\%\), the cut covers the profit and the loss together.",
              [("First SP (CP = 100)", r"100+x"), ("SP after the cut", r"100-y"), ("Gap = X", r"(x+y)\%\text{ of CP}")],
              r"The cut takes the price from \(x\%\) above the cost to \(y\%\) below it.",
              "'A man sells rice at a profit of x%. If he reduces the price by Rs X per kg, he would make a loss of y%. Find the initial selling price.'",
              r"\(12\%\) profit, Rs \(7\) cut, \(13\%\) loss: CP \(=\frac{700}{25}=\text{Rs }28\), first SP \(=\text{Rs }31.36\).",
              r"Using \(x-y\) - that is for a cut that still leaves a profit (Rule 33)."),
    33: card_(33, "A Price Cut Leaves a Smaller Profit",
              r"If a dealer selling at \(x\%\) profit cuts his price by \(X\) and still gains \(y\%\), the cut equals \((x-y)\%\) of the cost.",
              [("First SP (CP = 100)", r"100+x"), ("SP after the cut", r"100+y"), ("Gap = X", r"(x-y)\%\text{ of CP}")],
              r"Both prices are above the cost; their gap is the difference of the two profit per cents.",
              "'A hawker sells at a profit of x%. If he reduces the price of each by X paise, he earns a profit of y%. Find the initial selling price.'",
              r"\(30\%\) to \(20\%\) with \(20\) paise: CP \(=\frac{2000}{10}=200\) paise, first SP \(=260\) paise.",
              r"Adding the two per cents, or answering with the cost price when the first selling price is asked."),
    34: card_(34, "Cost and Price Lowered by Different Amounts",
              r"If the cost falls by Rs \(c\) and the price by Rs \(s\), and the profit per cent rises by \(p\), the cost price is fixed by one linear equation.",
              [("Old", r"\text{SP}=\frac{100+P}{100}\text{CP}"), ("New", r"\text{SP}-s=\frac{100+P+p}{100}(\text{CP}-c)"), ("Solve", r"\text{CP}=\frac{c(P+p)-100(s-c)}{p}")],
              r"Write the new selling price as the new profit per cent of the new cost and solve for the cost.",
              "'An article is sold at P% profit. If its cost price and selling price are less by Rs c and Rs s and the profit per cent increases by p, find the cost price.'",
              r"\(13\%\), Rs \(50\), Rs \(40\), \(3\): \(\frac{50\times 16+1000}{3}=\text{Rs }600\).",
              r"Mixing up \(s-c\) with \(c-s\) (the sign matters)."),
    35: card_(35, "Cost and Price Raised by Different Amounts",
              r"If the cost rises by Rs \(c\) and the price by Rs \(s\), and the profit per cent falls by \(p\), the cost price follows from one equation.",
              [("Old", r"\text{SP}=\frac{100+P}{100}\text{CP}"), ("New", r"\text{SP}+s=\frac{100+P-p}{100}(\text{CP}+c)"), ("Solve", r"\text{CP}=\frac{c(P-p)-100(s-c)}{p}")],
              r"A cost that rises faster than the price eats into the profit per cent.",
              "'An article is sold at P% profit. If its CP and SP are increased by Rs c and Rs s and the profit per cent decreases by p, find the cost price.'",
              r"\(20\%\), Rs \(30\), Rs \(12\), \(10\): \(\frac{30\times 10+1800}{10}=\text{Rs }210\).",
              r"Using \(P+p\) - the profit per cent has gone DOWN."),
}

OLD_IDS = {31: [324, 962], 32: [325], 33: [326], 34: [327], 35: [328]}


def main():
    for n in range(31, 36):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD_IDS[n]), n
        out = []
        for rid in OLD_IDS[n]:
            _, q, fn, unit = build(rid)
            g = fn()
            op, _ = opts(g, unit)
            extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key in [k for k in S.S if isinstance(k, str) and S.S[k][0] == n]:
            _, q, fn, unit = build(key)
            g = fn()
            op, pos = opts(g, unit)
            qs.append(new_question(n, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
