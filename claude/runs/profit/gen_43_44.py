"""Profit and Loss Rules 43 and 44 (2026-10-30) = the loss versions of Rules 39 and 40, built with the same builders (gen_39.r39,
gen_40.r40) and their own theorem. Rule 43: three parts all sold at a loss, total loss Rs P. Rule 44: part x at m% loss, the rest
at n% profit, overall loss Rs P. Their book examples are old rows 338 and 339, which were first linked to Rules 39 / 40 and are
moved here; their sentences (already reworded and gated against the original copies kept in 0_original_rows.json) stay as they
are. Adds the book exercises (3 for Rule 43, 5 for Rule 44) with new settings and all-new numbers. Usage: python gen_43_44.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry  # noqa: E402
from gen_18_21 import ropts  # noqa: E402
import gen_39  # noqa: E402
import gen_40  # noqa: E402

T43 = (r"If parts \(x\), \(y\) and \(z\) of a stock (\(x+y+z=1\)) are sold at \(m\%\), \(n\%\) and \(p\%\) loss and the total loss is "
       r"Rs \(P\), then<br>\[ \text{Value of the stock}=\frac{P\times 100}{mx+ny+pz} \]")
T44 = (r"If part \(x\) of a stock is sold at \(m\%\) loss and the rest \(y = 1 - x\) at \(n\%\) profit, and the overall loss is "
       r"Rs \(P\), then<br>\[ \text{Value of the stock}=\frac{P\times 100}{mx-ny} \]")

CARDS = {
    43: card(43, "Three Parts of a Stock at Three Losses: Find the Value",
             r"When parts \(x\), \(y\) and \(z\) of a stock lose \(m\%\), \(n\%\) and \(p\%\), the whole stock loses the weighted rate "
             r"\(mx+ny+pz\) per cent, and the total loss Rs \(P\) is that rate of the value.",
             T43.split("<br>")[1],
             [("Rest", r"z=1-x-y"), ("Overall loss rate", r"mx+ny+pz\ \text{per cent}"), ("Value", r"\frac{P\times 100}{mx+ny+pz}")],
             r"It is Rule 39 with every profit turned into a loss.",
             "'x of a commodity is sold at m% loss, y at n% loss and the rest at p% loss; the total loss is Rs P. Find the value of the commodity.'",
             r"\(\frac{1}{2}\) at \(4\%\), \(\frac{1}{4}\) at \(8\%\), rest at \(12\%\) loss, loss Rs \(70\): \(2+2+3=7\), value \(=\frac{7000}{7}=\text{Rs }1000\).",
             r"Forgetting to work out the rest \(z=1-x-y\) before using it."),
    44: card(44, "Part at a Loss, the Rest at a Profit, Overall Loss: Find the Value",
             r"When part \(x\) of a stock loses \(m\%\) and the rest \(y\) gains \(n\%\), the whole stock loses \(mx-ny\) per cent, and the "
             r"overall loss Rs \(P\) is that rate of the value.",
             T44.split("<br>")[1],
             [("Rest", r"y=1-x"), ("Overall loss rate", r"mx-ny\ \text{per cent}"), ("Value", r"\frac{P\times 100}{mx-ny}")],
             r"It is Rule 40 with profit and loss swapped: the gain on the rest lowers the overall loss.",
             "'x of a consignment was sold at m% loss and the rest at n% profit; the overall loss was Rs P. Find the value of the consignment.'",
             r"\(\frac{1}{2}\) at \(20\%\) loss, rest at \(10\%\) profit, loss Rs \(50\): \(10-5=5\), value \(=\frac{5000}{5}=\text{Rs }1000\).",
             r"Adding \(ny\) instead of taking it away."),
}
BUILD = {43: lambda c, w="loss": gen_39.r39(*c, word=w, theorem=T43),
         44: lambda c, w="loss": gen_40.r40(*c, word=w, theorem=T44)}
QTXT = {43: lambda item, c: gen_39.q_of(item, c, "loss"), 44: lambda item, c: gen_40.q_of(item, c, "loss")}
OLD = {43: {338: ("lot of cloth", (F(1, 6), F(1, 2), (12, 18, 9), 140))}, 44: {339: ("bags", (F(3, 5), 10, 5, 240))}}
NEW = {43: [("r43_e1", "stock of soap", (F(1, 4), F(1, 2), (6, 10, 22), 96)),
            ("r43_e2", "stock of oil", (F(1, 7), F(2, 7), (14, 21, 7), 78)),
            ("r43_e3", "stock of jam", (F(1, 3), F(1, 6), (9, 30, 14), 105))],
       44: [("r44_e1", "kettles", (F(2, 3), 9, 6, 180)),
            ("r44_e2", "rugs", (F(5, 6), 12, 18, 280)),
            ("r44_e3", "belts", (F(3, 7), 35, 21, 75)),
            ("r44_e4", "caps", (F(3, 8), 40, 16, 65)),
            ("r44_e5", "watches", (F(4, 5), 25, 30, 49))]}


def main(n):
    folder = os.path.join(HERE, f"rule{n}")
    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    rows = {r["id"]: r for r in dump["rows"]}
    assert sorted(rows) == sorted(OLD[n])
    out = []
    for rid, (item, c) in OLD[n].items():
        g = BUILD[n](c)
        assert rows[rid]["question"] == QTXT[n](item, c), rid      # the stored sentence is the one these numbers came from
        op, _ = ropts(g["answer"][1])
        extra = {**dict(zip("abcd", op)), "e": ""}
        extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
        out.append(regen_entry(rows[rid], g, f"NEW_RULE_{n}", extra))
    json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cc = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, item, c in NEW[n]:
        g = BUILD[n](c)
        op, pos = ropts(g["answer"][1])
        qs.append(new_question(n, QTXT[n](item, c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    for n in (43, 44):
        main(n)
