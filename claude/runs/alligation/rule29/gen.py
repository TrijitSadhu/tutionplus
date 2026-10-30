"""Rule 29 (capacity of a cask from repeated draw-and-refill): new rule card + the book's worked example and its
4 exercises, rewritten with new numbers in the prompt #10 layout. Writes 3_json_import_payload.json, 3_answers.json,
3_rule_card.json and an empty 0_current_rows.json (no existing rows)."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import card, frac, new_question, rbe, shortcut, solution, steps, tex  # noqa: E402

THEOREM = (r"If \(L\) litres are drawn from a cask full of one liquid and the cask is refilled with another, and after \(n\) such operations "
           r"the first liquid and the second are in the ratio \(a : b\), then the capacity of the cask is<br>"
           r"\[ C = \frac{L}{1 - \left(\frac{a}{a+b}\right)^{1/n}} \]")


def capacity(L, a, b, first, second, n=2):
    L, a, b = F(L), F(a), F(b)
    share = a / (a + b)
    k = {F(25, 36): F(5, 6), F(1, 9): F(1, 3), F(49, 64): F(7, 8), F(16, 25): F(4, 5), F(169, 225): F(13, 15)}[share]
    C = L / (1 - k)
    assert k ** n == share
    trad = steps(
        ("Follow the " + first + " through two draws.", rf"Let the cask hold \(C\) litres of {first}. The first draw leaves \((C - {tex(L)})\) litres of it."
         rf" The second draw removes \(\frac{{{tex(L)}}}{{C}}\) of what is there:<br>"
         rf"\[ (C - {tex(L)}) - (C - {tex(L)})\times\frac{{{tex(L)}}}{{C}} = \frac{{(C - {tex(L)})^2}}{{C}} \]"),
        ("Use the final ratio.", rf"The {first} is \(\frac{{{tex(a)}}}{{{tex(a)} + {tex(b)}}} = {frac(share)}\) of the full cask:<br>"
         rf"\[ \frac{{(C - {tex(L)})^2}}{{C}} = {frac(share)}\,C \;\Rightarrow\; \left(\frac{{C - {tex(L)}}}{{C}}\right)^2 = {frac(share)} \]"),
        ("Solve for \\(C\\).", rf"\[ \frac{{C - {tex(L)}}}{{C}} = {frac(k)} \;\Rightarrow\; {frac(1 - k)}\,C = {tex(L)} \;\Rightarrow\; C = {tex(C)} \]")
    )
    rule = steps(("Identify the values.", rf"\(L = {tex(L)}\), \(n = {n}\), {first} : {second} \(= {tex(a)} : {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ C = \frac{L}{1 - \left(\frac{a}{a+b}\right)^{1/n}} \]"),
                 ("Substitute the values.", rf"\[ C = \frac{{{tex(L)}}}{{1 - \left({frac(share)}\right)^{{1/{n}}}}} = \frac{{{tex(L)}}}{{1 - {frac(k)}}} = \frac{{{tex(L)}}}{{{frac(1 - k)}}} = {tex(C)}\text{{ litres}} \]"))
    fin = rf"\({tex(C)}\) litres"
    rb = rbe([rf"\(L = {tex(L)}\), \(n = {n}\), \(\frac{{a}}{{a+b}} = {frac(share)}\).", rf"\(\left({frac(share)}\right)^{{1/{n}}} = {frac(k)}\).",
              rf"\(C = \frac{{{tex(L)}}}{{1 - {frac(k)}}} = {tex(C)}\) litres."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(L)}}}{{1 - \sqrt{{{frac(share)}}}}} = \frac{{{tex(L)}}}{{{frac(1 - k)}}} = {tex(C)} \]", fin)
    return dict(answer=("number", C), solution=solution(THEOREM, trad, rule, fin), rbe=rb, shortcut=sc)


CARD = card(
    29, "Capacity of a Cask from Repeated Replacement",
    r"A cask is full of one liquid. \(L\) litres are drawn off and the cask is topped up with a second liquid, and this is repeated \(n\) times. "
    r"If the final ratio of the first liquid to the second is known, the size of the cask can be found.",
    r"\[ C = \frac{L}{1 - \left(\frac{a}{a+b}\right)^{1/n}} \]",
    [("Share of the first liquid left", r"\frac{a}{a+b}"), ("Undo the n draws", r"\left(\frac{a}{a+b}\right)^{1/n} = 1 - \frac{L}{C}"),
     ("Fraction removed per draw", r"\frac{L}{C} = 1 - \left(\frac{a}{a+b}\right)^{1/n}"), ("Capacity", r"C = \frac{L}{1 - \left(\frac{a}{a+b}\right)^{1/n}}")],
    r"Each draw keeps the same share \(1 - \frac{L}{C}\) of the first liquid, so after \(n\) draws its share is \(\left(1 - \frac{L}{C}\right)^n\). "
    r"Setting this equal to \(\frac{a}{a+b}\) and solving for \(C\) gives the rule. It is Rule 28 worked backwards.",
    r"The number of litres drawn each time, the number of operations and the final ratio are given; the question asks how much the cask holds.",
    r"\(5\) litres are drawn from a cask of water and replaced with milk, twice; water : milk becomes \(9 : 16\)."
    r"\[ C = \frac{5}{1 - \sqrt{\frac{9}{25}}} = \frac{5}{1 - \frac{3}{5}} = \frac{5}{\frac{2}{5}} = 12.5\text{ litres} \]",
    r"Using \(\frac{a}{b}\) instead of \(\frac{a}{a+b}\) under the root. The rule needs the share of the first liquid in the whole cask, not the ratio of the two liquids.",
)

NEW = [
    ("N1", "\\(6\\) litres are drawn from a cask full of water and the cask is filled up with milk. Once again \\(6\\) litres of the mixture are drawn and the cask is filled up with milk. "
           "Water and milk in the cask are now in the ratio \\(25:11\\). How many litres does the cask hold?",
     ["36 litres", "30 litres", "42 litres", "48 litres"], 1, lambda: capacity(6, 25, 11, "water", "milk")),
    ("N2", "\\(6\\) litres of water are drawn from a vessel full of water and replaced with pure milk. Then \\(6\\) litres of the mixture are drawn and again replaced with pure milk. "
           "If the vessel now holds water and milk in the ratio \\(1:8\\), what is its capacity?",
     ["8 litres", "10 litres", "9 litres", "12 litres"], 3, lambda: capacity(6, 1, 8, "water", "milk")),
    ("N3", "\\(12\\) litres of wine are taken out of a vessel full of wine and the vessel is filled up with water. Then \\(12\\) litres of the mixture are taken out and the vessel is filled with water again. "
           "Wine and water in the vessel are now in the ratio \\(49:15\\). What is the capacity of the vessel?",
     ["90 litres", "96 litres", "84 litres", "None of these"], 2, lambda: capacity(12, 49, 15, "wine", "water")),
    ("N4", "\\(15\\) litres are drawn from a vessel full of spirit and it is filled up with water. \\(15\\) litres of the mixture are then drawn and the vessel is filled with water once more. "
           "Spirit and water are now in the ratio \\(16:9\\). What is the full capacity of the vessel?",
     ["60 litres", "70 litres", "75 litres", "80 litres"], 3, lambda: capacity(15, 16, 9, "spirit", "water")),
    ("N5", "\\(4\\) litres are drawn from a cask full of wine and it is filled up with water. \\(4\\) litres of the mixture are drawn and the cask is filled with water again. "
           "The wine left in the cask is now to the water in it as \\(169:56\\). How much does the cask hold?",
     ["24 litres", "26 litres", "28 litres", "30 litres"], 4, lambda: capacity(4, 169, 56, "wine", "water")),
]

if __name__ == "__main__":
    qs, answers = [], []
    for key, text, opts, pos, fn in NEW:
        g = fn()
        qs.append(new_question(29, text, opts, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    payload = {"rules_html": [{"chapter": "alligation_n_mixture", "rule_name": "Rule 29", "rule_html": CARD}], "questions": qs}
    json.dump(payload, open(os.path.join(HERE, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(HERE, "3_answers.json"), "w", encoding="utf-8"), indent=2)
    json.dump({"rule_name": "Rule 29", "rule_html": CARD}, open(os.path.join(HERE, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump({"rule_card": None, "rows": []}, open(os.path.join(HERE, "0_current_rows.json"), "w", encoding="utf-8"), indent=2)
    print("Rule 29: card +", len(qs), "questions")
