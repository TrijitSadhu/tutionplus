"""Rules 36-40: regenerates every row in the prompt #11 layout (Theorem -> Traditional Method -> Specified Rule ->
Verification -> Final Answer), links the 2018 book copies and cleans their text. Answer keys come from validate.py
(255's key was wrong). Also writes the Rule 37 card fix and the two missing exercises (Rule 36 Exercise 5, Rule 40
Exercise 6, numbers changed) as JsonImport payloads."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import new_question, rbe, regen_entry, shortcut, steps, tex  # noqa: E402
from gen_1_4 import R, clean, fr, opts, result  # noqa: E402
from gen_5_10 import fin_of  # noqa: E402


def leaves_early(x, y, a, who):
    """A (x days) and B (y days) start together; `who` leaves a days before the end. Rules 36 (B leaves) and 37 (A leaves)."""
    x, y, a = R(x, y, a)
    s = 1 / x + 1 / y
    if who == "B":
        rhs = 1 + a / y
        T, num, form = x * (y + a) / (x + y), x * (y + a), r"\frac{x(y+a)}{x+y}"
        eq = rf"\[ \frac{{T}}{{{tex(x)}}} + \frac{{T - {tex(a)}}}{{{tex(y)}}} = 1 \]"
        line = rf"\[ T = \frac{{{tex(x)}({tex(y)} + {tex(a)})}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex(num)}}}{{{tex(x + y)}}} = {tex(T)}\text{{ days}} \]"
        extra = fr(a / y)
    else:
        rhs = 1 + a / x
        T, num, form = (x + a) * y / (x + y), (x + a) * y, r"\frac{(x+a)y}{x+y}"
        eq = rf"\[ \frac{{T - {tex(a)}}}{{{tex(x)}}} + \frac{{T}}{{{tex(y)}}} = 1 \]"
        line = rf"\[ T = \frac{{({tex(x)} + {tex(a)})\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex(num)}}}{{{tex(x + y)}}} = {tex(T)}\text{{ days}} \]"
        extra = fr(a / x)
    assert T == rhs / s
    other = "A" if who == "B" else "B"
    trad = steps(
        ("Write each person's working days.", rf"Let the work take \(T\) days. {other} works all \(T\) days and {who} works \(T - {tex(a)}\) days:" + eq),
        ("Collect the \\(T\\) terms.", rf"\[ T\left({fr(1 / x)} + {fr(1 / y)}\right) = 1 + {extra} \;\Rightarrow\; {fr(s)}\,T = {fr(rhs)} \]"),
        ("Solve for \\(T\\).", rf"\[ T = {fr(rhs)}\div {fr(s)} = {tex(T)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) (A), \(y = {tex(y)}\) (B), \(a = {tex(a)}\) (days {who} leaves before the end)."),
                 ("Apply the specified rule.", rf"\[ T = {form} \]"), ("Substitute the values.", line))
    fin = fin_of(T, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, a = {tex(a)}\).", rf"\(T = {form}\).", rf"\(T = \frac{{{tex(num)}}}{{{tex(x + y)}}} = {tex(T)}\)."], fin)
    sc = shortcut(line, fin)
    return T, trad, rule, fin, rb, sc


T36 = (r"If A and B can do a piece of work in \(x\) and \(y\) days respectively, both start together and B leaves the work \(a\) days before "
       r"its completion, then the whole work is completed in<br>\[ \frac{x(y+a)}{x+y}\text{ days} \]")
T37 = (r"If A and B can do a piece of work in \(x\) and \(y\) days respectively, both start together and A leaves the work \(a\) days before "
       r"its completion, then the whole work is completed in<br>\[ \frac{(x+a)y}{x+y}\text{ days} \]")


def r36(x, y, a):
    T, trad, rule, fin, rb, sc = leaves_early(x, y, a, "B")
    return result(("number", T), T36, trad, rule, fin, rb, sc)


def r37(x, y, a):
    T, trad, rule, fin, rb, sc = leaves_early(x, y, a, "A")
    return result(("number", T), T37, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 38: A works a days, B finishes in b days
T38 = (r"If A can do a piece of work in \(x\) days, A works only \(a\) days and B does the remaining work in \(b\) days, then B alone can do "
       r"the whole work in<br>\[ \frac{xb}{x-a}\text{ days} \]")


def r38(x, a, b, together=False):
    x, a, b = R(x, a, b)
    left = 1 - a / x
    B = x * b / (x - a)
    trad = steps(("Find A's share.", rf"\[ {tex(a)}\times {fr(1 / x)} = {fr(a / x)} \]So \(1 - {fr(a / x)} = {fr(left)}\) is left for B."),
                 ("Find B's time for the whole work.", rf"B does \({fr(left)}\) in \({tex(b)}\) days:<br>\[ {tex(b)}\div {fr(left)} = {tex(B)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(a = {tex(a)}\), \(b = {tex(b)}\)."),
                 ("Apply the specified rule.", r"\[ \text{B alone} = \frac{xb}{x-a} \]"),
                 ("Substitute the values.", rf"\[ \frac{{{tex(x)}\times {tex(b)}}}{{{tex(x)} - {tex(a)}}} = \frac{{{tex(x * b)}}}{{{tex(x - a)}}} = {tex(B)}\text{{ days}} \]"))
    v = B
    if together:
        v = x * B / (x + B)
        trad += "<br><br>" + rf"<b>Step 3: Work together.</b><br>\[ {fr(1 / x)} + {fr(1 / B)} = {fr(1 / x + 1 / B)} \;\Rightarrow\; 1\div {fr(1 / x + 1 / B)} = {tex(v)}\text{{ days}} \]"
        rule += "<br><br>" + rf"<b>Step 4: Put A and B together.</b><br>\[ \frac{{{tex(x)}\times {tex(B)}}}{{{tex(x)} + {tex(B)}}} = {tex(v)}\text{{ days}} \]"
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, a = {tex(a)}, b = {tex(b)}\).", rf"B alone \(= \frac{{xb}}{{x-a}} = {tex(B)}\) days.",
              rf"Together \(= \frac{{{tex(x)}\times {tex(B)}}}{{{tex(x)} + {tex(B)}}} = {tex(v)}\)." if together else rf"B alone \(= {tex(B)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{{tex(x)}\times {tex(b)}}}{{{tex(x)} - {tex(a)}}} = {tex(B)}" + (rf";\quad \frac{{{tex(x)}\times {tex(B)}}}{{{tex(x)} + {tex(B)}}} = {tex(v)}" if together else "") + r" \]", fin)
    return result(("number", v), T38, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 39: A leaves, B finishes in a days
T39 = (r"If A and B can do a piece of work in \(x\) and \(y\) days respectively, they start together, A leaves after some time and B does the "
       r"remaining work in \(a\) days, then A leaves after<br>\[ \frac{(y-a)x}{x+y}\text{ days} \]")


def r39(x, y, a):
    x, y, a = R(x, y, a)
    s = 1 / x + 1 / y
    t = (y - a) * x / (x + y)
    trad = steps(("Find B's share at the end.", rf"B works alone \({tex(a)}\) days: \({tex(a)}\times {fr(1 / y)} = {fr(a / y)}\)."),
                 ("Find the share done together.", rf"\[ 1 - {fr(a / y)} = {fr(1 - a / y)} \]Together they do \({fr(1 / x)} + {fr(1 / y)} = {fr(s)}\) a day."),
                 ("Find the days together.", rf"\[ {fr(1 - a / y)}\div {fr(s)} = {tex(t)}\text{{ days}} \]"))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\), \(y = {tex(y)}\), \(a = {tex(a)}\)."),
                 ("Apply the specified rule.", r"\[ t = \frac{(y-a)x}{x+y} \]"),
                 ("Substitute the values.", rf"\[ \frac{{({tex(y)} - {tex(a)})\times {tex(x)}}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex((y - a) * x)}}}{{{tex(x + y)}}} = {tex(t)}\text{{ days}} \]"))
    fin = fin_of(t, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, a = {tex(a)}\).", r"\(t = \frac{(y-a)x}{x+y}\).", rf"\(t = \frac{{{tex((y - a) * x)}}}{{{tex(x + y)}}} = {tex(t)}\)."], fin)
    sc = shortcut(rf"\[ \frac{{({tex(y)} - {tex(a)})\times {tex(x)}}}{{{tex(x)} + {tex(y)}}} = {tex(t)} \]", fin)
    return result(("number", t), T39, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- Rule 40: A alone a days, then B joins
T40 = (r"If A completes a work in \(x\) days and B in \(y\) days, A starts working alone and after \(a\) days B joins him, then they finish the "
       r"remaining work together in<br>\[ \frac{(x-a)y}{x+y}\text{ days} \]")


def r40(x, y, a, starter="A", joiner="B", total=False):
    x, y, a = R(x, y, a)
    left = 1 - a / x
    s = 1 / x + 1 / y
    t = (x - a) * y / (x + y)
    trad = steps(("Find the starter's share.", rf"{starter} works alone \({tex(a)}\) days: \({tex(a)}\times {fr(1 / x)} = {fr(a / x)}\), leaving \({fr(left)}\)."),
                 ("Find the work they do together in a day.", rf"\[ {fr(1 / x)} + {fr(1 / y)} = {fr(s)} \]"),
                 ("Find the days together.", rf"\[ {fr(left)}\div {fr(s)} = {tex(t)}\text{{ days}} \]" + (rf"In all: \({tex(a)} + {tex(t)} = {tex(a + t)}\) days." if total else "")))
    rule = steps(("Identify the values.", rf"\(x = {tex(x)}\) ({starter}, who starts), \(y = {tex(y)}\) ({joiner}), \(a = {tex(a)}\)."),
                 ("Apply the specified rule.", r"\[ t = \frac{(x-a)y}{x+y} \]"),
                 ("Substitute the values.", rf"\[ \frac{{({tex(x)} - {tex(a)})\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = \frac{{{tex((x - a) * y)}}}{{{tex(x + y)}}} = {tex(t)}\text{{ days}} \]"
                                            + (rf"The whole work takes \({tex(a)} + {tex(t)} = {tex(a + t)}\) days." if total else "")))
    v = a + t if total else t
    fin = fin_of(v, "days")
    rb = rbe([rf"\(x = {tex(x)}, y = {tex(y)}, a = {tex(a)}\).", r"\(t = \frac{(x-a)y}{x+y}\).",
              rf"\(t = {tex(t)}\)" + (rf", in all \({tex(a)} + {tex(t)} = {tex(v)}\)." if total else ".")], fin)
    sc = shortcut(rf"\[ \frac{{({tex(x)} - {tex(a)})\times {tex(y)}}}{{{tex(x)} + {tex(y)}}} = {tex(t)}" + (rf";\quad {tex(a)} + {tex(t)} = {tex(v)}" if total else "") + r" \]", fin)
    return result(("number", v), T40, trad, rule, fin, rb, sc)


# ---------------------------------------------------------------- text fixes, card fix, plan, new questions
BOOK_Q = {
    254: lambda q: q.replace("Both starts the work together for some time but B leaves", "Both start the work together, but B leaves"),
    255: lambda q: q.replace("Both starts the work together but A leaves the work 5 days before its completion time.",
                             "Both start the work together, but A leaves the work 5 days before its completion."),
    257: lambda q: q.replace("could complete the work in...", "could complete the work in:"),
    259: lambda q: q.replace("after 5 days B joins him", "after 5 days Shyam joins him"),
    260: lambda q: q.replace("would be completed in...", "would be completed in:"),
}
BOOK_OPTS = {
    254: opts("days", 10, 8, 12, 9), 255: opts("days", 12, 10, 9, 11), 256: opts("days", 6, 8, 7, 5), 257: opts("days", 24, 25, 30, 35),
    258: opts("days", 9, 10, 8, 11), 259: opts("days", 6, 2, 5, 3), 260: opts("days", 9, 7, 11, 10),
}
CARD_FIX = {37: [(
    "Do not subtract \\(a\\) from the final total incorrectly. A's absence affects only A's working days, so use \\(x+a\\) in the numerator after "
    "solving the work equation; avoid writing \\(T = \\frac{xy}{x+y} + a\\) unless algebra supports it.",
    "Do not simply add \\(a\\) to the time together, \\(\\frac{xy}{x+y}+a\\). A is absent only for the last \\(a\\) days, so A works \\(T-a\\) days "
    "while B works all \\(T\\) days; solving \\(\\frac{T-a}{x}+\\frac{T}{y}=1\\) gives \\(T=\\frac{(x+a)y}{x+y}\\).")]}

PLAN = {
    36: (81, {254: lambda: r36(15, 25, 7), 1391: lambda: r36(24, 40, 8), 1392: lambda: r36(30, 50, 10), 1393: lambda: r36(40, 60, 15), 1394: lambda: r36(18, 30, 6)}),
    37: (82, {255: lambda: r37(10, 20, 5), 1395: lambda: r37(12, 24, 6), 1396: lambda: r37(18, 30, 6), 1397: lambda: r37(10, 25, 5),
              1398: lambda: r37(24, 48, 12), 1399: lambda: r37(8, 16, 4)}),
    38: (83, {256: lambda: r38(12, 2, 5), 257: lambda: r38(80, 10, 42, together=True), 1400: lambda: r38(18, 3, 10), 1401: lambda: r38(20, 4, 12),
              1402: lambda: r38(30, 6, 8), 1403: lambda: r38(26, 8, 9), 1404: lambda: r38(24, 8, 10), 1405: lambda: r38(60, 12, 32, together=True)}),
    39: (84, {258: lambda: r39(45, 40, 23), 1406: lambda: r39(30, 20, 5), 1407: lambda: r39(24, 30, 6), 1408: lambda: r39(24, 36, 11),
              1409: lambda: r39(18, 30, 14), 1410: lambda: r39(24, 30, 15)}),
    40: (85, {259: lambda: r40(10, 15, 5, "Ram", "Shyam"), 260: lambda: r40(15, 10, 5, "Umesh", "Mahesh", total=True), 1411: lambda: r40(18, 24, 4),
              1412: lambda: r40(24, 30, 6), 1413: lambda: r40(16, 20, 4), 1414: lambda: r40(36, 45, 9), 1415: lambda: r40(30, 45, 10)}),
}
NEW = {
    36: [("ex5", "A and B can do a piece of work in 19 days and 31 days respectively. Both start the work together, but B leaves the job 9 days "
                 "before the work is completed. Find the time in which the work is finished.", lambda: r36(19, 31, 9),
          opts("days", r"16\frac{1}{5}", r"5\frac{1}{15}", r"15\frac{1}{5}", r"14\frac{4}{5}"), 3)],
    40: [("ex6", "Nikhil and Rohan can complete a work in 12 and 18 days respectively. Rohan starts the work and after 6 days Nikhil also joins "
                 "him. In all, the work would be completed in:", lambda: r40(18, 12, 6, "Rohan", "Nikhil", total=True),
          opts("days", r"4\frac{4}{5}", 12, r"10\frac{4}{5}", 11), 3)],
}


def main():
    cards = {}
    for n, (card_id, plan) in PLAN.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"]["id"] == card_id
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(plan), (n, sorted(set(rows) ^ set(plan)))
        out = []
        for rid, fn in plan.items():
            extra = {}
            if rows[rid]["rule_id"] is None:
                q = clean(rows[rid]["question"])
                extra["question"] = BOOK_Q[rid](q) if rid in BOOK_Q else q
                assert "\\[" not in extra["question"], rid
            if rid in BOOK_OPTS:
                extra.update(BOOK_OPTS[rid])
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], fn(), card_id, extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated")
        h = dump["rule_card"]["rule_html"]
        if n in CARD_FIX:
            for a, b in CARD_FIX[n]:
                assert h.count(a) == 1, (n, a[:60])
                h = h.replace(a, b)
            json.dump({"rule_name": f"Rule {n}", "rule_html": h}, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            print(f"Rule {n}: card fixed")
        cards[n] = h
    for n, items in NEW.items():
        folder = os.path.join(HERE, f"rule{n:02d}")
        qs, answers = [], []
        for key, text, fn, op, pos in items:
            g = fn()
            qs.append(new_question(n, text, [op[k] for k in "abcd"], pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "time_n_work", "rule_name": f"Rule {n}", "rule_html": cards[n]}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(qs)} new question")


if __name__ == "__main__":
    main()
