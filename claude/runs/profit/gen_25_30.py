"""Profit and Loss Rules 25-30 (2026-10-30): one change of price (Rs X more or less) moves a sale from x% to y% (profit or loss);
from that the cost price follows, and with it the first selling price (26, 27) or the price for a wished gain z% (25, 28, 29, 30).
Writes the six cards, regenerates the 7 old rows (318-323 copy the book's examples, 961 is a copy of 318; 319's key was on
option e) and adds the 23 book exercises that had no copy. Sentences: sent_25_30.py; numbers: PICKS (searched so that no number
set occurs in the book and no old number is kept). Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import m, result  # noqa: E402
from gen_13_17 import place  # noqa: E402
import sent_25_30 as S  # noqa: E402

PICKS = {318: (17, 88, 23, 15), 961: (21, 112, 7, 30), "r25_e1": (6, 63, 9, 30), "r25_e2": (15, 500, 5, 30), "r25_e3": (10, 210, 5, 30),
         "r25_e4": (5, 780, 7, 15), "r25_e5": (16, 820, 24, 30),
         319: (6, 65, 16), "r26_e1": (12, 400, 22), "r26_e2": (12, 65, 17), "r26_e3": (10, 117, 16), "r26_e4": (17, 20, 22), "r26_e5": (8, 50, 28),
         320: (8, 41, 33), "r27_e1": (19, 86, 24), "r27_e2": (30, 168, 10), "r27_e3": (21, 76, 17), "r27_e4": (6, 90, 24),
         321: (22, 92, 17, 5), "r28_e1": (12, 110, 10, 15), "r28_e2": (17, 260, 12, 30), "r28_e3": (22, 140, 12, 15),
         322: (4, 36, 6, 5), "r29_e1": (9, 700, 16, 5), "r29_e2": (11, 164, 15, 30), "r29_e3": (15, 33, 21, 30),
         323: (16, 21, 9, 5), "r30_e1": (21, 43, 16, 5), "r30_e2": (20, 126, 13, 5), "r30_e3": (22, 210, 7, 30)}

TH = {
    25: (r"If a dealer sells at a loss of \(x\%\) and Rs \(X\) more would have given a gain of \(y\%\), then for a gain of \(z\%\)<br>"
         r"\[ \text{SP}=\frac{X(100+z)}{x+y},\qquad \text{CP}=\frac{100X}{x+y} \]"),
    26: (r"If a dealer sells at a profit of \(x\%\) and raising the price by \(X\) gives a profit of \(y\%\), then<br>"
         r"\[ \text{CP}=\frac{100X}{y-x},\qquad \text{first SP}=\frac{(100+x)X}{y-x} \]"),
    27: (r"If a dealer sells at a loss of \(x\%\) and selling for \(X\) more gives a profit of \(y\%\), then<br>"
         r"\[ \text{CP}=\frac{100X}{x+y},\qquad \text{first SP}=\frac{(100-x)X}{x+y} \]"),
    28: (r"If a dealer sells at a profit of \(x\%\) and Rs \(X\) less would still have given \(y\%\), then for a gain of \(z\%\)<br>"
         r"\[ \text{SP}=\frac{X(100+z)}{x-y},\qquad \text{CP}=\frac{100X}{x-y} \]"),
    29: (r"If a dealer sells at a profit of \(x\%\) and Rs \(X\) more would have given \(y\%\), then for a gain of \(z\%\)<br>"
         r"\[ \text{SP}=\frac{X(100+z)}{y-x},\qquad \text{CP}=\frac{100X}{y-x} \]"),
    30: (r"If a dealer sells at a loss of \(x\%\) and Rs \(X\) more would still have meant a loss of \(y\%\), then for a gain of \(z\%\)<br>"
         r"\[ \text{SP}=\frac{X(100+z)}{x-y},\qquad \text{CP}=\frac{100X}{x-y} \]"),
}
DEN = {25: "x+y", 26: "y-x", 27: "x+y", 28: "x-y", 29: "y-x", 30: "x-y"}


def money_of(unit):
    return (lambda v: rf"\({m(v)}\) paise") if unit == "paise" else (lambda v: rf"Rs \({m(v)}\)")


def shift(n, c, ask, unit="Rs"):
    p1, p2, more = S.KIND[n]
    x, X, y = map(F, c[:3])
    z = F(c[3]) if len(c) > 3 else None
    first = 100 + x if p1 else 100 - x
    second = 100 + y if p2 else 100 - y
    d = abs(second - first)
    cp = 100 * X / d
    sp1 = cp * first / 100
    spz = cp * (100 + z) / 100 if z is not None else None
    M = money_of(unit)
    w1 = f"{'profit' if p1 else 'loss'} of \\({tex(x)}\\%\\)"
    w2 = f"{'profit' if p2 else 'loss'} of \\({tex(y)}\\%\\)"
    trad_steps = [
        ("Take the cost price as 100.", rf"The real sale (a {w1}) brings \({tex(first)}\); the other sale (a {w2}) brings \({tex(second)}\)."),
        ("The gap is the extra money.", rf"\({tex(second)}\) and \({tex(first)}\) differ by \({tex(d)}\) on every \(100\) of cost, and that gap is \({m(X)}\), so"
                                        rf"\[ \text{{CP}} = \frac{{{m(X)}}}{{{tex(d)}}}\times 100 = {m(cp)} \]")]
    if ask == "cpsp":
        trad_steps.append(("The first selling price.", rf"\[ {m(cp)}\times\frac{{{tex(first)}}}{{100}} = {m(sp1)} \]"))
    else:
        trad_steps.append((f"Price for a {tex(z)}% gain.", rf"\[ {m(cp)}\times\frac{{{tex(100 + z)}}}{{100}} = {m(spz)} \]"))
    trad = steps(*trad_steps)
    vals = rf"\(x = {tex(x)}\), \(X = {m(X)}\), \(y = {tex(y)}\)" + (rf", \(z = {tex(z)}\)" if z is not None else "") + "."
    sub = rf"\[ \text{{CP}} = \frac{{100\times {m(X)}}}{{{tex(d)}}} = {m(cp)}"
    if ask == "cpsp":
        sub += rf",\qquad \text{{first SP}} = \frac{{{tex(first)}\times {m(X)}}}{{{tex(d)}}} = {m(sp1)} \]"
    else:
        sub += rf",\qquad \text{{SP}} = \frac{{{m(X)}\times {tex(100 + z)}}}{{{tex(d)}}} = {m(spz)} \]"
    rule = steps(("Identify the values.", vals), ("Apply the specified rule.", TH[n].split("<br>")[1]),
                 ("Substitute the values.", rf"\({DEN[n]} = {tex(d)}\)." + sub))
    if ask == "cpsp":
        fin, ans = rf"cost price {M(cp)}, first selling price {M(sp1)}", ("pair", (cp, sp1))
    elif ask == "both":
        fin, ans = rf"sell for {M(spz)}; cost price {M(cp)}", ("pair", (spz, cp))
    else:
        fin, ans = M(spz), ("number", spz)
    rb = [vals, rf"\({DEN[n]} = {tex(d)}\), CP \(= {m(cp)}\).", (rf"First SP \(= {m(sp1)}\)." if ask == "cpsp" else rf"SP for \({tex(z)}\%\) \(= {m(spz)}\).")]
    sc = sub
    return result(ans, TH[n], trad, rule, fin, rb, sc)


def opts(g, ask, unit):
    M = money_of(unit)
    kind, v = g["answer"]
    if kind == "number":
        v = F(v)
        return place(M(v), [M(w) for w in (v * F(11, 10), v * F(9, 10), v * F(6, 5))])
    a, b = (F(t) for t in v)
    P = lambda t: f"{M(t[0])}, {M(t[1])}"
    return place(P((a, b)), [P((b, a)), P((a * F(11, 10), b)), P((a, b * F(11, 10)))])


def card_(n, title, pattern, example, mistake):
    p1, p2, more = S.KIND[n]
    statement = (rf"A sale at a {'profit' if p1 else 'loss'} of \(x\%\) becomes a sale at a {'profit' if p2 else 'loss'} of \(y\%\) when the "
                 rf"price is {'raised' if more == 'more' else 'lowered'} by \(X\). Both are per cents of the same cost price, so their gap "
                 rf"\({DEN[n]}\) per cent of the cost is exactly \(X\).")
    visual = [("Real sale (CP = 100)", r"100+x" if p1 else r"100-x"), ("Other sale", r"100+y" if p2 else r"100-y"),
              ("Gap = X", rf"{DEN[n]}\%\text{{ of CP}}=X"), ("Cost price", rf"\text{{CP}}=\frac{{100X}}{{{DEN[n]}}}")]
    return card(n, title, statement, TH[n].split("<br>")[1], visual,
                r"Once the cost price is known, any other selling price is that cost times \(\frac{100\pm\text{per cent}}{100}\).",
                pattern, example, mistake)


CARDS = {
    25: card_(25, "From a Loss to a Gain with Rs X More, Then the Price for z%",
              "'A dealer sold an article at a loss of x%. Had he sold it for Rs X more, he would have gained y%. For what value should he sell it to gain z%?'",
              r"Loss \(17\%\), gain \(23\%\), Rs \(88\): CP \(=\frac{8800}{40}=220\); for \(15\%\): \(\text{Rs }253\).",
              r"Using \(y-x\) as the gap - from a loss to a gain the gap is \(x+y\)."),
    26: card_(26, "Raising the Price Raises the Profit: Cost and First Price",
              "'A dealer sells at a profit of x%. If he increases the price by Rs X, he earns a profit of y%. Find the cost price and the initial selling price.'",
              r"\(12\%\) to \(22\%\) with Rs \(400\): CP \(=\frac{40000}{10}=\text{Rs }4000\), first SP \(=\text{Rs }4480\).",
              r"Dividing by \(y\) instead of by \(y-x\)."),
    27: card_(27, "From a Loss to a Profit: Cost and First Price",
              "'A man had to sell at a loss of x%. If he increases the price by Rs X per kg, he would make a profit of y%. Find the cost price and the initial selling price.'",
              r"Loss \(8\%\), profit \(33\%\), Rs \(41\): CP \(=\frac{4100}{41}=\text{Rs }100\), first SP \(=\text{Rs }92\).",
              r"Using \(y-x\); a loss and a profit lie on opposite sides of the cost, so the gap is \(x+y\)."),
    28: card_(28, "Rs X Less Still Gives y%: the Price for z%",
              "'A dealer sold at x% profit. Had he sold it for Rs X less, he would still have gained y%. For what value should he sell it to gain z%?'",
              r"\(22\%\) and \(17\%\) with Rs \(92\): CP \(=\frac{9200}{5}=1840\); for \(5\%\): \(\text{Rs }1932\).",
              r"Adding the two per cents - both sales are profits, so the gap is \(x-y\)."),
    29: card_(29, "Rs X More Would Give y%: the Price for z%",
              "'A dealer sold at x% profit. Had he sold it for Rs X more, he would have gained y%. For what value should he sell it to gain z%?'",
              r"\(4\%\) and \(6\%\) with Rs \(36\): CP \(=\frac{3600}{2}=1800\); for \(5\%\): \(\text{Rs }1890\).",
              r"Taking \(z\%\) of the old selling price instead of the cost price."),
    30: card_(30, "Rs X More Still Means a Loss: the Price for z%",
              "'A dealer sold at a loss of x%. Had he sold it for Rs X more, he would still have lost y%. For what value should he sell it to gain z%?'",
              r"Loss \(16\%\) and \(9\%\) with Rs \(21\): CP \(=\frac{2100}{7}=300\); for \(5\%\): \(\text{Rs }315\).",
              r"Using \(x+y\); both sales are losses, so the gap is \(x-y\)."),
}

OLD_IDS = {25: [318, 961], 26: [319], 27: [320], 28: [321], 29: [322], 30: [323]}


def make_entry(key):
    n, tpl, ask = S.S[key]
    c = PICKS[key]
    q = tpl(*c)
    unit = "paise" if "paise" in q else "Rs"
    return q, (lambda: shift(n, c, ask, unit)), ask, unit


def main():
    for n in range(25, 31):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        # Rule 29 already "has" card #114 - a Time & Distance card filed under profit_n_loss by mistake, used by no row;
        # apply_cards.py replaces its HTML (with a backup) by the real Profit and Loss Rule 29 card
        assert dump["rule_card"] is None or (n == 29 and dump["rule_card"]["id"] == 114), f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD_IDS[n]), n
        out = []
        for rid in OLD_IDS[n]:
            q, fn, ask, unit = make_entry(rid)
            g = fn()
            op, _ = opts(g, ask, unit)
            extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key in [k for k in S.S if isinstance(k, str) and S.S[k][0] == n]:
            q, fn, ask, unit = make_entry(key)
            g = fn()
            op, pos = opts(g, ask, unit)
            qs.append(new_question(n, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
