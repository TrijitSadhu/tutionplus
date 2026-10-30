"""Average Miscellaneous (2026-10-30): the book's 20 Miscellaneous problems (pdf pages 19-21) had no copy in the DB, so all 20 are
new questions, written in the simple style with all-new numbers (sentences in sentences.py) and filed on the stored card of the
rule each one uses (R2 sum = average x number, R4 weighted average, R5 average of the rest, R8 a newcomer, R11 a replacement,
R20 distances at speeds, R39 geometric mean, R40 harmonic mean). Misc 12 and 19 are the same book problem - different numbers here.
Misc 6 asks the average yearly growth: the book divides the 3-year total by 3 (38.67%); here it is the compound (geometric) rate.
Usage: python misc/gen_misc.py (writes misc/ruleNN/3_json_import_payload.json + 3_answers.json; ruleNN/0_current_rows.json is
the dump of the stored card)."""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import new_question, steps, tex  # noqa: E402
from gen_1_3 import T2  # noqa: E402
from gen_4_5 import T4, T5  # noqa: E402
from gen_6_11 import T8, T11, UU, answer_json, nf  # noqa: E402
from gen_18_30 import TH as TH18, ops  # noqa: E402
from gen_31_43 import TH as TH31  # noqa: E402
from helpers import place, result  # noqa: E402
from sentences import SENT  # noqa: E402

TH = {2: T2, 4: T4, 5: T5, 8: T8, 11: T11, 20: TH18[20], 39: TH31[39], 40: TH31[40]}


def make(rule, ans, trad, ident, sub, fin, rb):
    rs = steps(("Identify the values.", ident), ("Apply the specified rule.", TH[rule].split("<br>")[1]), ("Substitute the values.", sub))
    return result(ans, TH[rule], steps(*trad), rs, fin, rb, sub)


def num(rule, v, trad, ident, sub, unit=""):
    v = F(v)
    return make(rule, ("number", v), trad, ident, sub, UU(v, unit), [ident, rf"Answer \(= {nf(v)}\)."])


def pc(v):
    return rf"\({nf(v)}\%\)"


def m01():
    return num(8, 272, [("Totals.", r"First 5 days: \(5\times 248 = 1240\). First 6 days: \(6\times 252 = 1512\)."),
                        ("The 6th day.", r"\[ 1512 - 1240 = 272 \]")],
               r"\(n = 5\), \(x = 248\), \(y = 252\).", r"\[ 5(252-248)+252 = 20+252 = 272 \]", "items")


def m02():
    trad = [("Distance.", r"In \(x\) hours at \(40\): \(40x\) km; in \(y\) hours at \(65\): \(65y\) km."),
            ("Average speed.", r"\[ \frac{\text{distance}}{\text{time}} = \frac{40x+65y}{x+y} \]")]
    return make(4, ("expr", F(475, 10)), trad, r"\(m = x\) hours at \(40\), \(n = y\) hours at \(65\).", r"\[ \frac{x\times 40 + y\times 65}{x+y} = \frac{40x+65y}{x+y} \]",
                r"\(\frac{40x+65y}{x+y}\) km/hr", [r"Speeds weighted by the hours.", r"Average \(= \frac{40x+65y}{x+y}\)."])


def m03():
    trad = [("Time.", r"\(\frac{x}{30} + \frac{y}{45} = \frac{3x+2y}{90}\) hours."),
            ("Average speed.", r"\[ \frac{x+y}{\frac{3x+2y}{90}} = \frac{90(x+y)}{3x+2y} \]")]
    return make(20, ("expr", F(100, 3)), trad, r"\(A = x\) km at \(30\), \(B = y\) km at \(45\).", r"\[ \frac{x+y}{\frac{x}{30}+\frac{y}{45}} = \frac{90(x+y)}{3x+2y} \]",
                r"\(\frac{90(x+y)}{3x+2y}\) km/hr", [r"Distance \(x+y\), time \(\frac{x}{30}+\frac{y}{45}\).", r"Average \(= \frac{90(x+y)}{3x+2y}\)."])


def m04():
    return num(40, 480, [("Take a side.", r"Let each side be \(1800\) m. Times: \(\frac{1800}{300}=6\), \(\frac{1800}{450}=4\), \(\frac{1800}{600}=3\), \(\frac{1800}{900}=2\) minutes."),
                         ("Average speed.", r"\[ \frac{4\times 1800}{6+4+3+2} = \frac{7200}{15} = 480 \]")],
               r"\(n = 4\) equal sides at \(300, 450, 600, 900\).", r"\[ \frac{4}{\frac{1}{300}+\frac{1}{450}+\frac{1}{600}+\frac{1}{900}} = \frac{4\times 1800}{15} = 480 \]",
               "metres a minute")


def m05():
    return num(2, 24, [("Total age.", r"\(3\times 18 = 54\) years."), ("Share by the ratio.", r"\(2+3+4 = 9\) parts, so one part \(= 54\div 9 = 6\); the eldest \(= 4\times 6 = 24\).")],
               r"Average \(18\), number \(3\).", r"Sum \(= 18\times 3 = 54\); eldest \(= \frac{4}{9}\times 54 = 24\).", "years")


def m06():
    trad = [("Growth factors.", r"\(1.08\times 1.25\times 1.28 = 1.728\) over the three years."),
            ("One yearly rate.", r"The rate \(r\) with \((1+r)^{3} = 1.728\): \(1.2\times 1.2\times 1.2 = 1.728\), so \(1+r = 1.2\), \(r = 20\%\).")]
    sub = r"\[ \sqrt[3]{1.08\times 1.25\times 1.28} = \sqrt[3]{1.728} = 1.2 \]so the rate is \(20\%\)."
    return make(39, ("number", F(20)), trad, r"Growth factors \(1.08\), \(1.25\), \(1.28\).", sub, pc(20), [r"Geometric mean of the factors \(= 1.2\).", r"Rate \(= 20\%\)."])


def m07():
    trad = [("Take an amount.", r"Let the money be Rs \(600\): Rs \(200\) at \(9\%\), Rs \(300\) at \(15\%\), Rs \(100\) at \(18\%\)."),
            ("Returns.", r"\(18 + 45 + 18 = 81\) rupees on Rs \(600\): \[ \frac{81}{600}\times 100 = 13.5\% \]")]
    sub = r"\[ \frac{\frac{1}{3}\times 9 + \frac{1}{2}\times 15 + \frac{1}{6}\times 18}{1} = 3 + 7.5 + 3 = 13.5 \]"
    return make(4, ("number", F("13.5")), trad, r"Shares \(\frac{1}{3}, \frac{1}{2}, \frac{1}{6}\) at \(9\%, 15\%, 18\%\).", sub, pc(F("13.5")),
                [r"Rates weighted by the shares.", r"Average \(= 13.5\%\)."])


def m08():
    return num(2, 90, [("Write them with one letter.", r"First \(= x\), second \(= \frac{x}{2}\), third \(= \frac{x}{4}\)."),
                       ("Use the sum.", r"\(x + \frac{x}{2} + \frac{x}{4} = 3\times 70 = 210\), so \(\frac{7x}{4} = 210\), \(x = 120\); third \(= 30\); difference \(= 90\).")],
               r"Average \(70\), number \(3\).", r"Sum \(= 70\times 3 = 210 = \frac{7x}{4}\Rightarrow x = 120\); \(120 - 30 = 90\).")


def m09():
    return num(5, F("24.6"), [("Totals.", r"All \(8\): \(8\times 21.5 = 172\); first two \(33\); next three \(3\times 19.4 = 58.2\)."),
                              ("The last three.", r"\(172 - 33 - 58.2 = 80.8 = x + (x+2) + (x+5)\), so \(3x = 73.8\), \(x = 24.6\).")],
               r"\(m = 8\) at \(21.5\); known groups \(2\) at \(16.5\), \(3\) at \(19.4\).", r"Rest \(= 8\times 21.5 - (2\times 16.5 + 3\times 19.4) = 80.8\) for \(3\) readings: \(3x+7 = 80.8\), \(x = 24.6\).")


def m10():
    return num(2, 20, [("Total now.", r"\(5\times 24 = 120\) years."),
                       ("Eight years ago.", r"The other four were \(8\) years younger each and the youngest was not born: \(120 - 8 - 4\times 8 = 80\) for \(4\) people: \(80\div 4 = 20\).")],
               r"Average \(24\), number \(5\).", r"Sum \(= 24\times 5 = 120\); then \(\frac{120 - 8 - 32}{4} = 20\).", "years")


def m11():
    return num(8, 4, [("The couple now.", r"At marriage \(2\times 25 = 50\); now \(50 + 2\times 6 = 62\)."), ("With the child.", r"\(3\times 22 = 66\), so the child \(= 66 - 62 = 4\).")],
               r"\(n = 2\), \(x = 31\) (the couple's average now), \(y = 22\).", r"\[ 2(22-31)+22 = -18+22 = 4 \]", "years")


def m12():
    return num(8, 32, [("P, Q, R now.", r"Six years ago \(3\times 34 = 102\); now \(102 + 3\times 6 = 120\)."), ("With S.", r"\(4\times 38 = 152\), so S \(= 152 - 120 = 32\).")],
               r"\(n = 3\), \(x = 40\) (their average now), \(y = 38\).", r"\[ 3(38-40)+38 = -6+38 = 32 \]", "years")


def m13():
    return num(8, 38, [("Anil and Sunil now.", r"Three years ago \(2\times 24 = 48\); now \(48 + 6 = 54\)."),
                       ("Kiran.", r"\(3\times 29 = 87\), so Kiran \(= 87 - 54 = 33\) now and \(33 + 5 = 38\) in \(5\) years.")],
               r"\(n = 2\), \(x = 27\) (their average now), \(y = 29\).", r"Kiran now \(= 2(29-27)+29 = 33\); in \(5\) years \(= 38\).", "years")


def m14():
    return num(5, 28, [("Weight of the three taken out.", r"\(30\times 21 - 27\times 20 = 630 - 540 = 90\) kg."), ("Share it.", r"\(x + x + (x+6) = 90\), so \(3x = 84\), \(x = 28\).")],
               r"\(m = 30\) at \(21\), \(n = 27\) at \(20\), so \(m - n = 3\).", r"\[ \frac{30\times 21 - 27\times 20}{30-27} = 30 \]is their average, so \(3x+6 = 90\), \(x = 28\).", "kg")


def m15():
    trad = [("Write them with one letter.", r"Second \(= x\), first \(= 3x\), third \(= 6x\)."), ("Use the sum.", r"\(3x + x + 6x = 3\times 50 = 150\), so \(x = 15\): \(45, 15, 90\).")]
    return make(2, ("triple", (F(45), F(15), F(90))), trad, r"Average \(50\), number \(3\).", r"Sum \(= 50\times 3 = 150 = 10x\Rightarrow x = 15\).",
                r"\(45, 15, 90\)", [r"Sum \(= 150\).", r"Numbers \(45, 15, 90\)."])


def m16():
    return num(2, 54, [("Write them with one letter.", r"First \(= x\), second \(= 3x\), third \(= \frac{3x}{2}\)."),
                       ("Use the sum.", r"\(x + 3x + \frac{3x}{2} = 3\times 33 = 99\), so \(\frac{11x}{2} = 99\), \(x = 18\); the largest is \(3x = 54\).")],
               r"Average \(33\), number \(3\).", r"Sum \(= 33\times 3 = 99 = \frac{11x}{2}\Rightarrow x = 18\); largest \(= 54\).")


def m17():
    return num(2, 28, [("Join the ratios.", r"\(3 : 4\) and \(2 : 5 = 4 : 10\), so the three are \(3 : 4 : 10\)."),
                       ("Share the sum.", r"\(3+4+10 = 17\) parts; one part \(= 119\div 17 = 7\); second \(= 4\times 7 = 28\).")],
               r"Sum \(119\) (average \(\frac{119}{3}\) of \(3\) numbers).", r"Sum \(= 119 = 17k\Rightarrow k = 7\); second \(= 28\).")


def m18():
    return num(11, 62, [("S and T.", r"S \(= 4\times 60 - 3\times 62 = 240 - 186 = 54\); T \(= 58\)."),
                        ("Q and R, then P.", r"\(Q+R = 4\times 59 - 54 - 58 = 124\), so P \(= 186 - 124 = 62\).")],
               r"\(n = 4\) (P, Q, R, S), the average falls by \(x = 1\) when P is replaced by T \(= 58\).", r"\[ T = P - 4\times 1 \;\Rightarrow\; P = 58 + 4 = 62 \]", "kg")


def m19():
    return num(8, 29, [("The four now.", r"Three years ago \(4\times 31 = 124\); now \(124 + 4\times 3 = 136\)."), ("With the fifth.", r"\(5\times 33 = 165\), so the fifth \(= 165 - 136 = 29\).")],
               r"\(n = 4\), \(x = 34\) (their average now), \(y = 33\).", r"\[ 4(33-34)+33 = -4+33 = 29 \]", "years")


def m20():
    trad = [("Pair sums.", r"\(K+L = 68\), \(L+M = 62\), \(K+M = 72\)."), ("Add and take away.", r"\(2(K+L+M) = 202\), so \(K+L+M = 101\): \(M = 33\), \(K = 39\), \(L = 29\).")]
    return make(2, ("triple", (F(39), F(29), F(33))), trad, r"Each average is of \(2\) people.", r"Sums \(= 2\times 34, 2\times 31, 2\times 36 = 68, 62, 72\); all three \(= 101\).",
                r"\(K = 39\), \(L = 29\), \(M = 33\)", [r"Sums \(68, 62, 72\).", r"\(K = 39, L = 29, M = 33\)."])


BUILD = {f"m{i:02d}": f for i, f in enumerate([m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20], 1)}
E = lambda s: "\\(" + s + "\\)"
WRONG = {   # options that are not plain numbers
    "m02": [E(r"\frac{65x+40y}{x+y}"), E(r"\frac{40x+65y}{2}"), E(r"\frac{105}{x+y}")],
    "m03": [E(r"\frac{90(x+y)}{2x+3y}"), E(r"\frac{30x+45y}{x+y}"), E(r"\frac{x+y}{75}")],
    "m06": [pc(F(61, 3)), pc(19), pc(22)],
    "m07": [pc(13), pc(14), pc(F("12.5"))],
    "m15": [E("15, 45, 90"), E("45, 90, 15"), E("90, 15, 45")],
    "m20": [E("K = 29, L = 39, M = 33"), E("K = 39, L = 33, M = 29"), E("K = 33, L = 29, M = 39")],
}
RIGHT = {"m02": E(r"\frac{40x+65y}{x+y}"), "m03": E(r"\frac{90(x+y)}{3x+2y}"), "m06": pc(20), "m07": pc(F("13.5")), "m15": E("45, 15, 90"),
         "m20": E("K = 39, L = 29, M = 33")}
UNIT = {"m01": "items", "m04": "metres a minute", "m05": "years", "m09": "", "m10": "years", "m11": "years", "m12": "years", "m13": "years", "m14": "kg",
        "m18": "kg", "m19": "years"}


def main():
    by_rule = {}
    for key, (rule, q) in SENT.items():
        by_rule.setdefault(rule, []).append((key, q))
    for rule, items in sorted(by_rule.items()):
        folder = os.path.join(HERE, f"rule{rule:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] and not dump["rows"]
        qs, answers = [], []
        for key, q in items:
            g = BUILD[key]()
            if key in RIGHT:
                op, pos = place(RIGHT[key], WRONG[key])
            else:
                op, pos = ops(g["answer"][1], UNIT.get(key, ""))
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, answer_json(g["answer"])])
        json.dump({"rules_html": [{"chapter": "average", "rule_name": f"Rule {rule}", "rule_html": dump["rule_card"]["rule_html"]}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(qs)} new questions ({', '.join(k for k, _ in items)})")


if __name__ == "__main__":
    main()
