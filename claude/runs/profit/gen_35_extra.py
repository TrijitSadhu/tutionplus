"""Profit and Loss Rule 35, exercises 3-5 (2026-10-30; book pdf page 19, left out of the Rules 31-35 batch). Card #286 is already
stored, so these go in their own folder extra35/rule35/ with the stored card unchanged in the payload (the importer links new
questions to an existing card only when the payload's card is identical). Built with gen_31_35.shift2 and gen_31_35.opts.
Checks: PROFIT_RULE_ROOT=extra35 validate.py / gate_check.py / mutation_test.py 35; insert: save_and_insert.py with ROOT = extra35."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import new_question  # noqa: E402
import gen_31_35 as G  # noqa: E402

# (P, c, s, p): sold at P% profit; cost Rs c more and price Rs s more -> profit per cent down by p (the order solve_31_35 reads)
NEW = [("r35_e3", lambda P, c, s, p: f"A kettle is sold at a profit of {P}%. If its cost price went up by Rs {c} and its selling price by Rs {s}, the profit per cent would fall by {p}. Find the cost price.", (8, 5, 2, 2)),
       ("r35_e4", lambda P, c, s, p: f"A tray is sold at a profit of {P}%. If the cost went up by Rs {c} and the price by Rs {s}, the profit per cent would drop by {p}. Find the cost price.", (30, 14, 4, 20)),
       ("r35_e5", lambda P, c, s, p: f"A basket sells at a profit of {P}%. Raising its cost by Rs {c} and its price by Rs {s} would bring the profit per cent down by {p}. What did the basket cost?", (40, 27, 9, 30))]


def main():
    folder = os.path.join(HERE, "extra35", "rule35")
    stored = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))["rule_card"]
    assert G.CARDS[35] == json.load(open(os.path.join(HERE, "rule35", "3_rule_card.json"), encoding="utf-8"))["rule_html"]
    assert stored and stored["rule_html"] == G.CARDS[35], "card #286 in the DB is not the generated Rule 35 card"
    json.dump([], open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"))
    cc = {"rule_name": "Rule 35", "rule_html": G.CARDS[35]}
    json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    qs, answers = [], []
    for key, tpl, c in NEW:
        g = G.shift2(35, *c)
        op, pos = G.opts(g, "Rs")
        qs.append(new_question(35, tpl(*c), op, pos, g["solution"], g["rbe"], g["shortcut"]))
        answers.append([key, [g["answer"][0], str(g["answer"][1])]])
    json.dump({"rules_html": [{"chapter": "profit_n_loss", **cc}], "questions": qs},
              open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Rule 35 extra: {len(qs)} new questions for the stored card")


if __name__ == "__main__":
    main()
