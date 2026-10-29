"""Rewording pilot (2026-10-29): 10 Time & Work rows that copied the book word for word get a fresh sentence and all-new
numbers (copyright - the owner's rule), new options, and an explanation regenerated with the same rule generator for the new
numbers. Row ids, rule links, days and times stay. Writes reword/pilot/ruleNN/2_new_rows.json; check with
`python reword_check.py pilot`."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))          # reword/pilot
TW = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, TW)
from common import regen_entry  # noqa: E402
from gen_1_4 import men_for_days, opts  # noqa: E402
from gen_5_10 import other_alone, twice_thrice5  # noqa: E402
from gen_11_20 import absent18, faster11, good14, hours12, times15  # noqa: E402
from gen_36_40 import r37  # noqa: E402

NOTE = "question reworded (fresh wording + all-new numbers, checked against the book) by Claude Opus 5.5 (2026-10-29)"
D = "days"

# rule -> {row id: (question, generator, options)}; the numbers keep the order each rule's solver reads them in
PLAN = {
    1: {1232: ("Resurfacing a stretch of road keeps 14 men busy for 9 days. If the same stretch has to be resurfaced over 21 days "
               "instead, how many men should be put on the job?",
               lambda: men_for_days(14, 9, 21), opts("men", 4, 6, 9, 7))},
    5: {1255: ("To paint a hall alone, A needs twice as much time as B and three times as much time as C. When all three paint "
               "together, the hall is finished in 4 days. How many days would A, B and C each need on their own?",
               lambda: twice_thrice5(4),
               {"a": r"\(18\) days, \(9\) days, \(6\) days", "b": r"\(30\) days, \(15\) days, \(10\) days",
                "c": r"\(24\) days, \(12\) days, \(8\) days", "d": r"\(12\) days, \(6\) days, \(4\) days"})},
    6: {1258: ("Working side by side, A and B can weed a large garden in 10 days. On his own, A would need 15 days. How long would "
               "B take to weed the garden by himself?",
               lambda: other_alone(10, 15), opts(D, 30, 25, 20, 35)),
        1268: ("A and B, sharing the job, paint a fence in 14 days, while B on his own takes 21 days. In how many days can A paint "
               "the fence alone?",
               lambda: other_alone(14, 21, "B", "A"), opts(D, 35, 28, 49, 42))},
    11: {1292: ("A works 3 times as fast as B and so finishes a job 24 days sooner than B does. How many days do the two need to "
                "finish the job together?",
                lambda: faster11(3, 24), opts(D, 12, 9, 8, 18))},
    12: {1296: ("Working 8 hours a day, I can type a manuscript in 9 days; you, working 3 hours a day, can type it in 8 days. If we "
                "type it together for 3 hours a day, in how many days will it be done?",
                lambda: hours12(9, 8, 8, 3, 3), opts(D, 4, 9, 6, 8))},
    14: {1306: ("A is twice as efficient a worker as B. Between them they can build a wall in 12 days. How many days would A need "
                "to build it alone?",
                lambda: good14(2, 12), opts(D, 24, 36, 15, 18))},
    15: {1311: ("Per hour, a gang of 10 men and 3 boys finishes 8 times the work that a single man paired with a single boy "
                "finishes. What is the ratio of one man's work to one boy's work?",
                lambda: times15(10, 3, 8), {"a": "5 : 2", "b": "2 : 5", "c": "5 : 3", "d": "3 : 2"})},
    18: {1323: ("A contractor planned to finish a job in 21 days with a team of men, but 9 of the men never turned up. The men who "
                "did come finished the job in 28 days. How many men were in the team as planned?",
                lambda: absent18(21, 9, 28), opts("men", 27, 32, 36, 42))},
    37: {1397: ("Laying a floor takes A 12 days by himself and B 24 days by himself. Both begin on the first day, but A quits 3 "
                "days before the floor is complete. How many days does the floor take from start to finish?",
                lambda: r37(12, 24, 3), opts(D, 10, 9, 12, 8))},
}


def main():
    for n, plan in PLAN.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(plan), (n, sorted(set(rows) ^ set(plan)))
        out = []
        for rid, (question, fn, options) in plan.items():
            r = rows[rid]
            assert r["rule_id"] == dump["rule_card"]["id"]
            llm = r["llm_used"] or ""
            extra = {"question": question, **options, "e": "",
                     "llm_used": llm if NOTE in llm else (llm + "; " if llm else "") + NOTE}
            extra = {k: v for k, v in extra.items() if v != r[k]}
            out.append(regen_entry(r, fn(), r["rule_id"], extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows reworded")


if __name__ == "__main__":
    main()
