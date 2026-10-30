"""Average Rules 4-5 (2026-10-30). Rule 4: groups put together - the average of all of them is (mx + ny + ...)/(m + n + ...) (a
discrete series: values times their frequencies over the total frequency); also the average of a group that joined, worked
backwards. Rule 5: the average of the rest - (mx - ny)/(m - n). Writes the two cards, regenerates the old rows 490-502 (the book's
examples and exercises) with simple-style sentences, new settings and all-new numbers, and adds the book exercises with no copy.
Usage: python gen_4_5.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from helpers import U, m, nopts, result  # noqa: E402

T4 = (r"If the average of \(m\) items is \(x\) and the average of \(n\) other items is \(y\), the average of all of them put together is"
      r"<br>\[ \frac{mx+ny}{m+n} \](for more groups add more products \(m_i x_i\) above and more counts \(m_i\) below).")
T5 = (r"If the average of \(m\) items is \(x\) and the average of \(n\) of them is \(y\), the average of the rest is"
      r"<br>\[ \frac{mx-ny}{m-n} \](take away every group whose average is known).")
TH = {4: T4, 5: T5}


def apply(r):
    return ("Apply the specified rule.", TH[r].split("<br>")[1])


def money_or_tex(v, unit):
    return m(v) if unit == "Rs" else tex(F(v))


def r4_groups(groups, unit):
    groups = [(F(c), F(a)) for c, a in groups]
    S, n = sum(c * a for c, a in groups), sum(c for c, _ in groups)
    v = S / n
    f = lambda t: money_or_tex(t, unit)
    rows = "<br>".join(rf"\({tex(c)}\times {f(a)} = {f(c * a)}\)" for c, a in groups)
    trad = steps(("Total of each group.", rows), ("Total of all and the number of all.", rf"Sum \(= {f(S)}\), number \(= {tex(n)}\)."),
                 ("Average of all.", rf"\[ {f(S)} \div {tex(n)} = {f(v)} \]"))
    top = " + ".join(tex(c) + r"\times " + f(a) for c, a in groups)
    bottom = " + ".join(tex(c) for c, _ in groups)
    rule = steps(("Identify the values.", ", ".join(rf"\({tex(c)}\) at \({f(a)}\)" for c, a in groups) + "."), apply(4),
                 ("Substitute the values.", rf"\[ \frac{{{top}}}{{{bottom}}} = \frac{{{f(S)}}}{{{tex(n)}}} = {f(v)} \]"))
    return result(("number", v), T4, trad, rule, U(v, unit), [rf"Sum \(= {f(S)}\).", rf"Number \(= {tex(n)}\).", rf"Average \(= {f(v)}\)."], rf"\[ \frac{{{f(S)}}}{{{tex(n)}}} = {f(v)} \]")


def r4_price(groups, unit="Rs"):
    """groups of (count, total paid): the average price per article."""
    groups = [(F(c), F(t)) for c, t in groups]
    S, n = sum(t for _, t in groups), sum(c for c, _ in groups)
    v = S / n
    trad = steps(("Money paid in all.", rf"\[ {' + '.join(m(t) for _, t in groups)} = {m(S)} \]"), ("Articles in all.", rf"\[ {' + '.join(tex(c) for c, _ in groups)} = {tex(n)} \]"),
                 ("Price per article.", rf"\[ {m(S)} \div {tex(n)} = {m(v)} \]"))
    rule = steps(("Identify the values.", ", ".join(rf"\({tex(c)}\) at an average of \({m(t / c)}\)" for c, t in groups) + "."), apply(4),
                 ("Substitute the values.", rf"\[ \frac{{{' + '.join(tex(c) + chr(92) + 'times ' + m(t / c) for c, t in groups)}}}{{{' + '.join(tex(c) for c, _ in groups)}}} = {m(v)} \]"))
    return result(("number", v), T4, trad, rule, U(v, unit), [rf"Paid \(= {m(S)}\).", rf"Articles \(= {tex(n)}\).", rf"Average \(= {m(v)}\)."], rf"\[ \frac{{{m(S)}}}{{{tex(n)}}} = {m(v)} \]")


def r4_income(m1, a1, m2, a2, save):
    m1, a1, m2, a2, save = map(F, (m1, a1, m2, a2, save))
    spend = m1 * a1 + m2 * a2
    v = (spend + save) / (m1 + m2)
    trad = steps(("Spending in the year.", rf"\[ {tex(m1)}\times {m(a1)} + {tex(m2)}\times {m(a2)} = {m(spend)} \]"), ("Income in the year.", rf"\[ {m(spend)} + {m(save)} = {m(spend + save)} \]"),
                 ("Per month.", rf"\[ {m(spend + save)} \div {tex(m1 + m2)} = {m(v)} \]"))
    rule = steps(("Identify the values.", rf"\({tex(m1)}\) months at \({m(a1)}\), \({tex(m2)}\) months at \({m(a2)}\), saving \({m(save)}\)."), apply(4),
                 ("Substitute the values.", rf"Average spending \(= \frac{{{tex(m1)}\times {m(a1)} + {tex(m2)}\times {m(a2)}}}{{{tex(m1 + m2)}}} = {m(spend / (m1 + m2))}\); add the saving per month \({m(save / (m1 + m2))}\): \({m(v)}\)."))
    return result(("number", v), T4, trad, rule, U(v, "Rs"), [rf"Spent \(= {m(spend)}\).", rf"Income \(= {m(spend + save)}\).", rf"Per month \(= {m(v)}\)."],
                  rf"\[ \frac{{{m(spend + save)}}}{{{tex(m1 + m2)}}} = {m(v)} \]")


def r4_back(n, avg, k, newavg, unit):
    n, avg, k, newavg = map(F, (n, avg, k, newavg))
    v = ((n + k) * newavg - n * avg) / k
    trad = steps(("Total before.", rf"\[ {tex(n)}\times {tex(avg)} = {tex(n * avg)} \]"), ("Total after.", rf"\[ {tex(n + k)}\times {tex(newavg)} = {tex((n + k) * newavg)} \]"),
                 ("The newcomers.", rf"They add \({tex((n + k) * newavg - n * avg)}\) between them: \[ {tex((n + k) * newavg - n * avg)} \div {tex(k)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"\(m = {tex(n)}\), \(x = {tex(avg)}\), \(n = {tex(k)}\), average of all \(= {tex(newavg)}\); \(y\) is unknown."), apply(4),
                 ("Substitute the values.", rf"\[ \frac{{{tex(n)}\times {tex(avg)} + {tex(k)}y}}{{{tex(n + k)}}} = {tex(newavg)} \;\Rightarrow\; y = {tex(v)} \]"))
    return result(("number", v), T4, trad, rule, U(v, unit), [rf"Before \(= {tex(n * avg)}\).", rf"After \(= {tex((n + k) * newavg)}\).", rf"Newcomers' average \(= {tex(v)}\)."],
                  rf"\[ \frac{{{tex((n + k) * newavg)} - {tex(n * avg)}}}{{{tex(k)}}} = {tex(v)} \]")


def r5_rest(n, avg, parts, unit):
    n, avg = F(n), F(avg)
    parts = [(F(c), F(a)) for c, a in parts]
    f = lambda t: money_or_tex(t, unit)
    S = n * avg - sum(c * a for c, a in parts)
    k = n - sum(c for c, _ in parts)
    v = S / k
    trad = steps(("Total of all.", rf"\[ {tex(n)}\times {f(avg)} = {f(n * avg)} \]"),
                 ("Totals of the known groups.", "<br>".join(rf"\({tex(c)}\times {f(a)} = {f(c * a)}\)" for c, a in parts)),
                 ("The rest.", rf"\({f(n * avg)} - {f(sum(c * a for c, a in parts))} = {f(S)}\) for \({tex(k)}\): \[ {f(S)} \div {tex(k)} = {f(v)} \]"))
    sub = " - ".join(tex(c) + r"\times " + f(a) for c, a in parts)
    rule = steps(("Identify the values.", rf"\(m = {tex(n)}\), \(x = {f(avg)}\); known groups: " + ", ".join(rf"\({tex(c)}\) at \({f(a)}\)" for c, a in parts) + "."), apply(5),
                 ("Substitute the values.", rf"\[ \frac{{{tex(n)}\times {f(avg)} - {sub}}}{{{tex(n)} - {tex(n - k)}}} = \frac{{{f(S)}}}{{{tex(k)}}} = {f(v)} \]"))
    return result(("number", v), T5, trad, rule, U(v, unit), [rf"All \(= {f(n * avg)}\).", rf"Rest \(= {f(S)}\) for \({tex(k)}\).", rf"Average \(= {f(v)}\)."],
                  rf"\[ \frac{{{f(S)}}}{{{tex(k)}}} = {f(v)} \]")


CARDS = {
    4: card(4, "Average of Groups Put Together", r"Each group's average times its size gives its total; the totals and the sizes add up.", r"\[ \frac{mx+ny}{m+n} \]",
            [("Group 1", r"m\ \text{at}\ x\Rightarrow mx"), ("Group 2", r"n\ \text{at}\ y\Rightarrow ny"), ("All", r"\frac{mx+ny}{m+n}")],
            r"The combined average lies between \(x\) and \(y\), nearer the larger group. With prices or ages of several kinds it is a discrete series: "
            r"\(\frac{\sum f_ix_i}{\sum f_i}\).",
            "'The average of m boys is x and of n boys is y; find the average of all' / 'bought a articles at p and b at q; average price'.",
            r"\(10\) at \(20\) and \(30\) at \(40\): \(\frac{200+1200}{40}=35\).", r"Taking \(\frac{x+y}{2}\) when the groups are not the same size."),
    5: card(5, "Average of the Rest", r"Take the known groups' totals away from the total of all, and share what is left among the rest.", r"\[ \frac{mx-ny}{m-n} \]",
            [("All", r"m\ \text{at}\ x\Rightarrow mx"), ("Known part", r"n\ \text{at}\ y\Rightarrow ny"), ("Rest", r"\frac{mx-ny}{m-n}")],
            r"When only one item is left (\(m-n=1\)) the answer is that item itself.",
            "'The average of m quantities is x and the average of n of them is y; find the average of the rest.'",
            r"\(12\) numbers average \(30\), \(8\) of them average \(25\): \(\frac{360-200}{4}=40\).", r"Subtracting the averages instead of the totals."),
}
OLD = {   # row: (rule, question, builder, unit)
    490: (4, "Class P has 45 pupils with an average age of 13 years and class Q has 35 pupils with an average age of 9 years. Find the average age of all the pupils together.",
          lambda: r4_groups([(45, 13), (35, 9)], "years"), "years"),
    491: (4, "A girl buys 5 pens for Rs 135 at one shop and 7 pens for Rs 165 at another. What is the average price she paid per pen?",
          lambda: r4_price([(5, 135), (7, 165)]), "Rs"),
    492: (4, "In one school 120 pupils have an average mark of 45, and in another 80 pupils have an average mark of 70. Find the average mark of all 200 pupils.",
          lambda: r4_groups([(120, 45), (80, 70)], "marks"), "marks"),
    493: (4, "A woman spends an average of Rs 1800 a month for the first 3 months of a year and Rs 2100 a month for the other 9 months. If she saves Rs 4500 in the year, what is her average monthly income?",
          lambda: r4_income(3, 1800, 9, 2100, 4500), "Rs"),
    494: (4, "A shop buys 14 bags at Rs 80 each, 16 bags at Rs 95 each and 10 bags at Rs 110 each. What is the average price of a bag?",
          lambda: r4_groups([(14, 80), (16, 95), (10, 110)], "Rs"), "Rs"),
    495: (4, "In a club there are 11 children aged 8, 19 aged 10 and 10 aged 13. Find their average age.", lambda: r4_groups([(11, 8), (19, 10), (10, 13)], "years"), "years"),
    496: (4, "Out of 30 boys, 9 are 142 cm tall, 12 are 136 cm tall and the rest are 130 cm tall. What is their average height?",
          lambda: r4_groups([(9, 142), (12, 136), (9, 130)], "cm"), "cm"),
    497: (4, "A bus carried an average of 1450 passengers a day from Monday to Friday and 1100 a day on Saturday and Sunday. What was its daily average for the whole week?",
          lambda: r4_groups([(5, 1450), (2, 1100)], "passengers"), "passengers"),
    498: (4, "The average weight of 18 parcels is 12.5 kg. If 6 more parcels with an average weight of 14.5 kg are added, what is the new average weight?",
          lambda: r4_groups([(18, F("12.5")), (6, F("14.5"))], "kg"), "kg"),
    499: (4, "The average age of 400 members of a club is 32 years. After 50 new members join, the average age becomes 30 years. What is the average age of the new members?",
          lambda: r4_back(400, 32, 50, 30, "years"), "years"),
    500: (5, "The average of 21 numbers is 24. The average of 7 of them is 21. What is the average of the other 14?", lambda: r5_rest(21, 24, [(7, 21)], ""), ""),
    501: (5, "The average age of 45 members of a club is 25 years. One group of 9 members has an average of 21 years and another group of 16 has an average of 29 years. What is the average age of the other members?",
          lambda: r5_rest(45, 25, [(9, 21), (16, 29)], "years"), "years"),
    502: (5, "A dealer buys 25 cows for Rs 900000. The average price of 15 of them is Rs 32000. What is the average price of the others?",
          lambda: r5_rest(25, 36000, [(15, 32000)], "Rs"), "Rs"),
}
NEW = {4: [("r4_ex1", "A man buys 9 caps at Rs 120 each, 12 belts at Rs 150 each and 9 wallets at Rs 210 each. What is the average price of an article?",
            lambda: r4_groups([(9, 120), (12, 150), (9, 210)], "Rs"), "Rs"),
           ("r4_ex2", "A player's average score in 4 matches is 36 and in 6 other matches is 41. What is his average in all 10 matches?", lambda: r4_groups([(4, 36), (6, 41)], "runs"), "runs"),
           ("r4_e3", "A class has 24 boys with an average age of 14 years and 16 girls with an average age of 13 years. What is the average age of the class?",
            lambda: r4_groups([(24, 14), (16, 13)], "years"), "years"),
           ("r4_e4", "Of 25 workers, 15 earn Rs 640 a day and 10 earn Rs 515 a day. What is the average daily earning of a worker?", lambda: r4_groups([(15, 640), (10, 515)], "Rs"), "Rs"),
           ("r4_e5", "A school buys 18 desks at Rs 900 each, 12 at Rs 750 each and 10 at Rs 1020 each. What is the average price of a desk?",
            lambda: r4_groups([(18, 900), (12, 750), (10, 1020)], "Rs"), "Rs"),
           ("r4_e6", "In a class of 36 pupils, the average height of 24 is 148 cm and that of the rest is 154 cm. What is the average height of the class?",
            lambda: r4_groups([(24, 148), (12, 154)], "cm"), "cm"),
           ("r4_e14", "In a sports camp there are 45 children aged 10, 35 aged 11, 40 aged 12 and 30 aged 13. What is their average age?",
            lambda: r4_groups([(45, 10), (35, 11), (40, 12), (30, 13)], "years"), "years"),
           ("r4_e15", "Out of 50 runners, the average time of 35 is 42 minutes and that of the rest is 48 minutes. What is the average time of all the runners?",
            lambda: r4_groups([(35, 42), (15, 48)], "minutes"), "minutes"),
           ("r4_e16", "The average weight of 28 of the 40 boys in a hostel is 52 kg and that of the other boys is 57 kg. What is the average weight of all the boys?",
            lambda: r4_groups([(28, 52), (12, 57)], "kg"), "kg")],
       5: [("r5_e1", "A team of 24 players has an average age of 21 years. The average age of 16 of them is 22 years. What is the average age of the other 8?",
            lambda: r5_rest(24, 21, [(16, 22)], "years"), "years"),
           ("r5_e2", "A group of 35 children has an average age of 9 years. The average age of 21 of them is 10 years. What is the average age of the others?",
            lambda: r5_rest(35, 9, [(21, 10)], "years"), "years"),
           ("r5_e5", "The average of 16 results is 24, and the average of the first 4 is 21. What is the average of the rest?", lambda: r5_rest(16, 24, [(4, 21)], ""), ""),
           ("r5_e6", "The average of 13 numbers is 42, and the average of the first 12 is 40. Find the last number.", lambda: r5_rest(13, 42, [(12, 40)], ""), ""),
           ("r5_e7", "A batsman's average for 15 matches is 46.4 runs. If his average for the first 9 matches is 52, what is his average for the last 6?",
            lambda: r5_rest(15, F("46.4"), [(9, 52)], "runs"), "runs")]}


def main():
    for rule in (4, 5):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None
        rows = {r["id"]: r for r in dump["rows"]}
        ids = [rid for rid, v in OLD.items() if v[0] == rule]
        assert sorted(rows) == sorted(ids)
        out = []
        for rid in ids:
            _, q, fn, unit = OLD[rid]
            g = fn()
            op, _ = nopts(g["answer"][1], unit)
            extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
        json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, unit in NEW[rule]:
            g = fn()
            op, pos = nopts(g["answer"][1], unit)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "average", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
