"""Profit and Loss Rules 13-17 (2026-10-30): mark-up needed for a profit after a discount (13), goods passing through successive
hands at profits (14), at losses (15), at a profit and a loss (16), and two successive profits (17). Writes the five cards,
regenerates the 11 old rows (301-308 copy the book; 355-357 are discount / mark-up questions that use Rule 13; 306 had no option
holding the answer, 308's key was on option e, 355 had four empty options) with a simple-style sentence, a new setting and
all-new numbers, and adds the 20 book exercises that had no copy. Same file layout as gen_1_3.py."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from gen_1_3 import P, Rs, m, result  # noqa: E402

POS = [3, 1, 4, 2, 2, 4, 1, 3, 4, 2, 3, 1]
_k = [0]


def place(right, wrong):
    pos = POS[_k[0] % len(POS)]
    _k[0] += 1
    o = list(wrong)[:3]
    o.insert(pos - 1, right)
    return o, pos


def popts(v):
    v = F(v)
    return place(P(v), [P(w) for w in (v + 5, v - 3 if v > 3 else v + 8, v * 2)])


def ropts(v):
    v = F(v)
    return place(Rs(v), [Rs(w) for w in (v * F(11, 10), v * F(9, 10), v * F(6, 5))])


# ---------------------------------------------------------------- Rule 13
T13 = (r"If a dealer wants a profit of \(x\%\) after allowing a discount of \(y\%\), the marked price must be above the cost price by<br>"
       r"\[ \frac{x+y}{100-y}\times 100\% \]")


def r13(x, y):
    x, y = F(x), F(y)
    v = (x + y) / (100 - y) * 100
    sp = 100 + x
    mp = sp * 100 / (100 - y)
    trad = steps(
        ("Take the cost price as Rs 100.", rf"For a \({tex(x)}\%\) profit the selling price must be Rs \({tex(sp)}\)."),
        ("This is the marked price less the discount.", rf"The selling price is \({tex(100 - y)}\%\) of the marked price, so<br>"
                                                        rf"\[ \text{{MP}} = {tex(sp)}\times\frac{{100}}{{{tex(100 - y)}}} = {tex(mp)} \]"),
        ("Compare with the cost price.", rf"The marked price is \({tex(mp)} - 100 = {tex(v)}\%\) above the cost price."))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", r"\[ \frac{x+y}{100-y}\times 100\% \]"),
        ("Substitute the values.", rf"\[ \frac{{{tex(x)} + {tex(y)}}}{{100 - {tex(y)}}}\times 100 = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", r"Mark-up \(= \frac{x+y}{100-y}\times 100\%\).", rf"\(\frac{{{tex(x + y)}}}{{{tex(100 - y)}}}\times 100 = {tex(v)}\%\)."]
    return result(("number", v), T13, trad, rule, P(v), rb, rf"\[ \frac{{{tex(x + y)}}}{{{tex(100 - y)}}}\times 100 = {tex(v)}\% \]")


# ---------------------------------------------------------------- Rules 14-16: successive hands
TH = {
    14: (r"If A sells an article to B at a profit of \(x\%\) and B sells it to C at a profit of \(y\%\), and C pays Rs \(X\), then A's cost price is<br>"
         r"\[ \frac{100^2 X}{(100+x)(100+y)} \](one more factor \(\frac{100}{100+z}\) for each further seller)"),
    15: (r"If A sells an article to B at a loss of \(x\%\) and B sells it to C at a loss of \(y\%\), and C pays Rs \(X\), then A paid<br>"
         r"\[ \frac{100^2 X}{(100-x)(100-y)} \](one more factor \(\frac{100}{100-z}\) for each further seller)"),
    16: (r"If A sells an article to B at a profit of \(x\%\) and B sells it to C at a loss of \(y\%\) (or a loss first and then a profit), "
         r"and C pays Rs \(X\), then A paid<br>\[ \frac{100^2 X}{(100+x)(100-y)}\qquad\text{or}\qquad \frac{100^2 X}{(100-x)(100+y)} \]"),
}


def chain(n, changes, X):
    """changes = [(+1 / -1, per cent), ...] in the order the article travels; X = the last selling price."""
    X = F(X)
    prices = [X]
    for s, p in reversed(changes):
        prices.append(prices[-1] * 100 / (100 + s * F(p)))
    prices = prices[::-1]                                   # cost of the first seller ... last price
    cp = prices[0]
    lines = []
    for i in range(len(changes) - 1, -1, -1):
        s, p = changes[i]
        k = 100 + s * F(p)
        lines.append(rf"Seller {i + 1} sold at a {'profit' if s > 0 else 'loss'} of \({tex(F(p))}\%\), so he had paid \({m(prices[i + 1])}\times\frac{{100}}{{{tex(k)}}} = {m(prices[i])}\)")
    trad = steps(("Work back from the last price.", "<br>".join(lines) + "."),
                 ("The first seller's cost.", rf"\[ \text{{CP}} = \text{{Rs }}{m(cp)} \]"))
    factors = r"\times".join(rf"\frac{{100}}{{{tex(100 + s * F(p))}}}" for s, p in changes)
    rule = steps(
        ("Identify the values.", rf"\(X = {m(X)}\); the per cents are " + ", ".join(rf"\({'+' if s > 0 else '-'}{tex(F(p))}\%\)" for s, p in changes) + "."),
        ("Apply the specified rule.", r"\[ \text{CP} = X\times\frac{100}{100\pm x}\times\frac{100}{100\pm y}\times\cdots \]"),
        ("Substitute the values.", rf"\[ {m(X)}\times {factors} = {m(cp)} \]"))
    rb = [rf"\(X = {m(X)}\).", r"Divide by each \(\frac{100\pm p}{100}\) in turn.", rf"\({m(X)}\times {factors} = {m(cp)}\)."]
    return result(("number", cp), TH[n], trad, rule, Rs(cp), rb, rf"\[ {m(X)}\times {factors} = {m(cp)} \]")


# ---------------------------------------------------------------- Rule 17
T17 = r"When there are two successive profits of \(x\%\) and \(y\%\), the resultant profit is<br>\[ \left(x+y+\frac{xy}{100}\right)\% \]"


def r17(x, y):
    x, y = F(x), F(y)
    v = x + y + x * y / 100
    a = 100 + x
    b = a * (100 + y) / 100
    trad = steps(
        ("Take the first cost as Rs 100.", rf"After a \({tex(x)}\%\) profit the price is Rs \({tex(a)}\)."),
        ("Second profit on the new price.", rf"\[ {tex(a)} + \frac{{{tex(y)}}}{{100}}\times {tex(a)} = {tex(b)} \]"),
        ("Overall.", rf"From Rs \(100\) to Rs \({tex(b)}\) is a profit of \({tex(v)}\%\)."))
    rule = steps(
        ("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\)."),
        ("Apply the specified rule.", r"\[ x+y+\frac{xy}{100} \]"),
        ("Substitute the values.", rf"\[ {tex(x)} + {tex(y)} + \frac{{{tex(x)}\times {tex(y)}}}{{100}} = {tex(v)}\% \]"))
    rb = [rf"\(x = {tex(x)}\), \(y = {tex(y)}\).", r"\(x+y+\frac{xy}{100}\).", rf"\({tex(x)} + {tex(y)} + {tex(x * y / 100)} = {tex(v)}\%\)."]
    return result(("number", v), T17, trad, rule, P(v), rb, rf"\[ {tex(x)} + {tex(y)} + \frac{{{tex(x * y)}}}{{100}} = {tex(v)}\% \]")


CARDS = {
    13: card(13, "Mark-up Needed for a Profit after a Discount",
             r"To make a profit of \(x\%\) after giving a discount of \(y\%\), the dealer must mark his goods above the cost price by a "
             r"larger per cent than \(x\).",
             r"\[ \text{Mark-up}=\frac{x+y}{100-y}\times 100\% \]",
             [("SP needed (CP = 100)", r"100+x"), ("SP is (100 - y)% of MP", r"\text{MP}=\frac{(100+x)\times 100}{100-y}"), ("Mark-up", r"\text{MP}-100=\frac{x+y}{100-y}\times 100")],
             r"The discount is taken off the marked price, so the marked price has to carry both the profit and the discount.",
             "'By what per cent above the cost price must a trader mark his goods to gain x% after allowing a discount of y%?'",
             r"Profit \(12\%\), discount \(20\%\): \(\frac{32}{80}\times 100=40\%\).",
             r"Adding the two per cents (\(32\%\)) - the discount is on the larger marked price."),
    14: card(14, "Goods Passing Through Hands at Profits",
             r"When an article passes from seller to seller, each making a profit on what he paid, the first cost is found by removing the "
             r"profits one at a time from the last price.",
             r"\[ \text{CP of A}=\frac{100^2 X}{(100+x)(100+y)} \]",
             [("Last price", r"X"), ("Remove the last profit", r"X\times\frac{100}{100+y}"), ("Remove the first profit", r"X\times\frac{100}{100+y}\times\frac{100}{100+x}")],
             r"Each profit is on that seller's own cost, so the factors multiply; they are never added.",
             "'A sells to B at x% profit, B sells to C at y% profit; C pays Rs X. Find A's cost' (or three dealers, each gaining z%).",
             r"\(10\%\) and \(20\%\), C pays Rs \(330\): \(330\times\frac{100}{110}\times\frac{100}{120}=\text{Rs }250\).",
             r"Taking \(x+y=30\%\) off Rs \(X\), or subtracting the per cents of the selling prices."),
    15: card(15, "Goods Passing Through Hands at Losses",
             r"When each seller in turn sells at a loss, the first price is found by dividing the last price by each loss factor.",
             r"\[ \text{A's price}=\frac{100^2 X}{(100-x)(100-y)} \]",
             [("Last price", r"X"), ("Undo the last loss", r"X\times\frac{100}{100-y}"), ("Undo the first loss", r"X\times\frac{100}{100-y}\times\frac{100}{100-x}")],
             r"A loss of \(y\%\) means the seller got \((100-y)\%\) of what he paid, so to go back divide by that fraction.",
             "'A sells to B at a loss of x%, B sells to C at a loss of y%; C pays Rs X. At what price did A buy?'",
             r"Losses \(15\%\) and \(20\%\), C pays Rs \(1360\): \(1360\times\frac{100}{85}\times\frac{100}{80}=\text{Rs }2000\).",
             r"Adding the losses back on the last price (\(1360 + 35\%\)) instead of dividing."),
    16: card(16, "Goods Passing Through Hands at a Profit and a Loss",
             r"If one seller gains and the next one loses (or the other way round), undo each change with its own factor.",
             r"\[ \text{A's price}=\frac{100^2 X}{(100+x)(100-y)}\qquad\text{or}\qquad\frac{100^2 X}{(100-x)(100+y)} \]",
             [("Last price", r"X"), ("Undo the second change", r"X\times\frac{100}{100\mp y}"), ("Undo the first change", r"\times\frac{100}{100\pm x}")],
             r"The order does not change the product of the factors, but each factor must have the right sign.",
             "'A sells to B at a profit of x%, B sells to C at a loss of y%; C pays Rs X. At what price did A buy?'",
             r"Profit \(25\%\), loss \(16\%\), C pays Rs \(630\): \(630\times\frac{100}{125}\times\frac{100}{84}=\text{Rs }600\).",
             r"Using \(100+y\) for the loss, or treating the profit and the loss as cancelling out."),
    17: card(17, "Two Successive Profits",
             r"If an article is sold at a profit of \(x\%\) and the buyer sells it again at a profit of \(y\%\), the overall profit is more than \(x+y\).",
             r"\[ \left(x+y+\frac{xy}{100}\right)\% \]",
             [("Start", r"100"), ("After x%", r"100+x"), ("After y% on that", r"(100+x)\frac{100+y}{100}")],
             r"The second profit is earned on the already increased price, which adds the extra \(\frac{xy}{100}\).",
             "'A sells to B at x% profit and B sells to C at y% profit; find the resultant profit per cent.'",
             r"\(10\%\) and \(30\%\): \(10+30+\frac{300}{100}=43\%\).",
             r"Writing just \(x+y\)."),
}

UP, DN = 1, -1
OLD = {
    13: {301: (lambda: r13(12, 16), r"A shopkeeper wants a profit of 12% after giving a discount of 16%. By what per cent above the cost price should he mark his goods?"),
         355: (lambda: r13(16, 20), r"A trader gives a cash discount of 20% and still wants a profit of 16%. How much per cent above the cost price must he mark his goods?"),
         356: (lambda: r13(16, 4), r"A dealer allows 4% discount for cash. By what per cent above the cost price should he mark his goods to gain 16%?"),
         357: (lambda: r13(44, 4), r"How much per cent above the cost price must a seller mark a fan so that he gains 44% even after a discount of 4%?")},
    14: {302: (lambda: chain(14, [(UP, 5), (UP, 40)], 588), r"A maker sells a lamp to a dealer at a profit of 5%, and the dealer sells it to a shop at a profit of 40%. "
                                                             r"If the shop pays Rs 588, what did the lamp cost the maker?"),
         306: (lambda: chain(14, [(UP, 12), (UP, 15)], 644), r"Ravi sells a bicycle to Mohan at a gain of 12%, and Mohan sells it to Sita at a gain of 15%. Sita pays "
                                                             r"Rs 644. What did the bicycle cost Ravi?"),
         303: (lambda: chain(14, [(UP, 10), (UP, 10), (UP, 10)], 1331), r"A clock passes through three shops, and each shop makes a profit of 10%. If the last shop "
                                                                        r"sells it for Rs 1331, what did the first shop pay?")},
    15: {304: (lambda: chain(15, [(DN, 15), (DN, 40)], 1020), r"A farmer sells a cow to a trader at a loss of 15%, and the trader sells it to a dairy at a loss of 40%. "
                                                              r"If the dairy pays Rs 1020, what did the farmer pay for the cow?"),
         305: (lambda: chain(15, [(DN, 10), (DN, 10), (DN, 10)], 5832), r"A scooter is sold by three owners in turn, each losing 10%. If the third owner sells it "
                                                                        r"for Rs 5832, what did the first owner pay?")},
    16: {307: (lambda: chain(16, [(DN, 15), (UP, 25)], 63750), r"A woman sells her car to a friend at a loss of 15%. The friend sells it for Rs 63750 and gains "
                                                               r"25%. What did the car cost the woman?")},
    17: {308: (lambda: r17(10, 30), r"A sells a cooler to B at a profit of 10%, and B sells it to C at a profit of 30%. Find the overall profit per cent.")},
}

NEW = {
    13: [("r13_e1", r"A shop wants an 8% profit after a 4% discount. By what per cent above the cost price should it mark its goods?", lambda: r13(8, 4)),
         ("r13_e2", r"To gain 19% after allowing a discount of 15%, by what per cent should a trader raise the marked price above the cost?", lambda: r13(19, 15)),
         ("r13_e3", r"A seller wants to earn 24% after giving 20% off the marked price. How much per cent above the cost should he mark the goods?", lambda: r13(24, 20)),
         ("r13_e4", r"After a 25% discount a dealer still wants a 14% profit. By what per cent above the cost price should he mark his goods?", lambda: r13(14, 25)),
         ("r13_e5", r"A store gives 25% off and wants a profit of 35%. By what per cent above the cost price must it mark a shirt?", lambda: r13(35, 25))],
    14: [("r14_e1", r"A potter sells a pot to a trader at a profit of 15%, and the trader sells it to a shop at a profit of 20%. The shop pays Rs 1380. What "
                    r"did the pot cost the potter?", lambda: chain(14, [(UP, 15), (UP, 20)], 1380)),
         ("r14_e3", r"A maker sells a cooker to a wholesaler at 25% profit, the wholesaler sells it to a shopkeeper at 8% profit, and the shopkeeper sells "
                    r"it for Rs 297 at a profit of 10%. What did the cooker cost the maker?", lambda: chain(14, [(UP, 25), (UP, 8), (UP, 10)], 297)),
         ("r14_e4", r"A sells a bat to B at a profit of 40%, and B sells it to C at a profit of 5%. If C pays Rs 2940, what was A's cost price?",
          lambda: chain(14, [(UP, 40), (UP, 5)], 2940)),
         ("r14_e5", r"A tailor sells a coat to a shop at 30% profit, and the shop sells it to a buyer at 10% profit. The buyer pays Rs 715. Find the "
                    r"tailor's cost.", lambda: chain(14, [(UP, 30), (UP, 10)], 715))],
    15: [("r15_e1", r"A man sells a goat to his neighbour at a loss of 8%, and the neighbour sells it at a loss of 25% for Rs 1380. What did the man pay "
                    r"for the goat?", lambda: chain(15, [(DN, 8), (DN, 25)], 1380)),
         ("r15_e2", r"A horse is sold twice: first at a loss of 30%, then by its new owner at a loss of 5%. The last buyer pays Rs 3990. What did the first owner pay?",
          lambda: chain(15, [(DN, 30), (DN, 5)], 3990))],
    16: [("r16_x1", r"A sells a fridge to B at a profit of 25%, and B sells it to C at a loss of 16%. If C pays Rs 630, what did A pay for it?",
          lambda: chain(16, [(UP, 25), (DN, 16)], 630)),
         ("r16_e1", r"A boy sells a toy to his friend at a profit of 10%, and the friend sells it at a loss of 10% for Rs 39.60. What did the toy cost the boy?",
          lambda: chain(16, [(UP, 10), (DN, 10)], F(198, 5))),
         ("r16_e2", r"A shopkeeper sells a pen to a friend at a gain of 25%, and the friend sells it at a loss of 12% for Rs 33. What did the pen cost the shopkeeper?",
          lambda: chain(16, [(UP, 25), (DN, 12)], 33)),
         ("r16_e3", r"A trader sells a mat to a shop at a gain of 20%, and the shop sells it at a loss of 15% for Rs 306. Find the trader's cost price.",
          lambda: chain(16, [(UP, 20), (DN, 15)], 306))],
    17: [("r17_e1", r"A sells a fan to B at a profit of 6%, and B sells it to C at a profit of 15%. Find the overall profit per cent.", lambda: r17(6, 15)),
         ("r17_e2", r"A farmer sells rice to a miller at 12% profit, and the miller sells it to a shop at 25% profit. What is the overall profit per cent?",
          lambda: r17(12, 25)),
         ("r17_e3", r"A sells a radio to B at a gain of 16%, and B sells it to C at a gain of 25%. Find the resultant profit per cent.", lambda: r17(16, 25)),
         ("r17_e4", r"A sells a desk to B at a profit of 12.5%, and B sells it to C at a profit of 20%. What is the overall profit per cent?",
          lambda: r17(F(25, 2), 20)),
         ("r17_e5", r"A bike is sold at a profit of 40%, and its buyer sells it again at a profit of 50%. What is the profit per cent over the two sales?", lambda: r17(40, 50))],
}


def main():
    for n in (13, 14, 15, 16, 17):
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question) in OLD[n].items():
            g = fn()
            op, _ = (popts if n in (13, 17) else ropts)(g["answer"][1])
            extra = {"question": question, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn in NEW[n]:
            g = fn()
            op, pos = (popts if n in (13, 17) else ropts)(g["answer"][1])
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "profit_n_loss", **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
