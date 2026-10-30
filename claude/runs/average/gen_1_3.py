"""Average Rules 1-3 (2026-10-30). Rule 1: average = sum / number. Rule 2: sum = average x number (and the many problems the book
solves by comparing totals: a missing member, an overlapping window, a member joining or leaving, a group joining, income from
spending and saving). Rule 3: number = sum / average. Writes the three cards, regenerates the old rows 467-489 (the book's examples
and exercises) with simple-style sentences, new settings and all-new numbers, and adds the book exercises that had no copy.
Usage: python gen_1_3.py"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps, tex  # noqa: E402
from helpers import U, m, nopts, result  # noqa: E402

T1 = r"The average of a set of quantities is their sum divided by their number:<br>\[ \text{Average}=\frac{\text{Sum of the quantities}}{\text{Number of quantities}} \]"
T2 = r"When the number of quantities and their average are known, their sum is<br>\[ \text{Sum of the quantities}=\text{Average}\times\text{Number of quantities} \]"
T3 = r"When the sum of the quantities and their average are known, their number is<br>\[ \text{Number of quantities}=\frac{\text{Sum of the quantities}}{\text{Average}} \]"
TH = {1: T1, 2: T2, 3: T3}


def apply(r):
    return ("Apply the specified rule.", TH[r].split("<br>")[1])


def add(vals):
    return " + ".join(tex(F(v)) for v in vals)


# ---------------------------------------------------------------- Rule 1
def r1_list(vals, unit, what="the quantities"):
    vals = [F(v) for v in vals]
    S, n = sum(vals), len(vals)
    v = S / n
    trad = steps((f"Add {what}.", rf"\[ {add(vals)} = {tex(S)} \]"), ("Share the total equally.", rf"\[ {tex(S)} \div {n} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Sum \(= {tex(S)}\), number \(= {n}\)."), apply(1), ("Substitute the values.", rf"\[ \frac{{{tex(S)}}}{{{n}}} = {tex(v)} \]"))
    return result(("number", v), T1, trad, rule, U(v, unit), [rf"Sum \(= {tex(S)}\).", rf"Number \(= {n}\).", rf"Average \(= {tex(v)}\)."], rf"\[ \frac{{{tex(S)}}}{{{n}}} = {tex(v)} \]")


def primes(n):
    out, k = [], 2
    while len(out) < n:
        if all(k % p for p in out):
            out.append(k)
        k += 1
    return out


def r1_consec_even(n):
    """n consecutive even numbers p, p+2, ...: how much is the average more than p."""
    v = F(2 * (n - 1), 2)
    terms = " + ".join(["p"] + [f"(p+{2 * i})" for i in range(1, n)])
    trad = steps(("Write the numbers.", rf"They are \(p, p+2, \dots, p+{2 * (n - 1)}\)."),
                 ("Add and divide.", rf"\[ \frac{{{terms}}}{{{n}}} = \frac{{{n}p + {n * (n - 1)}}}{{{n}}} = p + {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Sum \(= {n}p + {n * (n - 1)}\), number \(= {n}\)."), apply(1),
                 ("Substitute the values.", rf"\[ \frac{{{n}p + {n * (n - 1)}}}{{{n}}} = p + {tex(v)} \]So the average is \({tex(v)}\) more than \(p\)."))
    return result(("number", v), T1, trad, rule, rf"\({tex(v)}\)", [rf"Sum \(= {n}p + {n * (n - 1)}\).", rf"\(\div {n}\).", rf"Average \(= p + {tex(v)}\)."],
                  rf"\[ \frac{{{n}p + {n * (n - 1)}}}{{{n}}} - p = {tex(v)} \]")


def r1_daily(a, b, days):
    a, b, days = map(F, (a, b, days))
    S = a + b
    v = S / days
    trad = steps(("Spending in the whole year.", rf"\[ {m(a)} + {m(b)} = {m(S)} \]"), ("Per day.", rf"\[ {m(S)} \div {tex(days)} = {m(v)} \]"))
    rule = steps(("Identify the values.", rf"Sum \(= {m(S)}\), number of days \(= {tex(days)}\)."), apply(1), ("Substitute the values.", rf"\[ \frac{{{m(S)}}}{{{tex(days)}}} = {m(v)} \]"))
    return result(("number", v), T1, trad, rule, U(v, "Rs"), [rf"Sum \(= {m(S)}\).", rf"Days \(= {tex(days)}\).", rf"Average \(= {m(v)}\)."], rf"\[ \frac{{{m(S)}}}{{{tex(days)}}} = {m(v)} \]")


# ---------------------------------------------------------------- Rule 2
def r2_total(avg, n, unit):
    avg, n = F(avg), F(n)
    v = avg * n
    trad = steps(("Each of the " + tex(n) + " has the average on the whole.", rf"So together they have \({tex(n)}\) times the average."), ("Multiply.", rf"\[ {tex(n)}\times {tex(avg)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Average \(= {tex(avg)}\), number \(= {tex(n)}\)."), apply(2), ("Substitute the values.", rf"\[ {tex(avg)}\times {tex(n)} = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Average \(= {tex(avg)}\).", rf"Number \(= {tex(n)}\).", rf"Sum \(= {tex(v)}\)."], rf"\[ {tex(avg)}\times {tex(n)} = {tex(v)} \]")


def r2_missing(known, target, unit):
    """known values, and the average all of them plus one more must have."""
    known = [F(v) for v in known]
    target = F(target)
    n = len(known) + 1
    need, have = target * n, sum(known)
    v = need - have
    trad = steps(("Total needed.", rf"\[ {n}\times {tex(target)} = {tex(need)} \]"), ("Total already there.", rf"\[ {add(known)} = {tex(have)} \]"),
                 ("The missing one.", rf"\[ {tex(need)} - {tex(have)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Average \(= {tex(target)}\) for \({n}\) items."), apply(2),
                 ("Substitute the values.", rf"\[ {tex(target)}\times {n} - {tex(have)} = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Needed sum \(= {tex(need)}\).", rf"Known sum \(= {tex(have)}\).", rf"Missing \(= {tex(v)}\)."], rf"\[ {tex(need)} - {tex(have)} = {tex(v)} \]")


def r2_window(days, a1, a2, first, unit):
    days, a1, a2, first = map(F, (days, a1, a2, first))
    s1, s2 = days * a1, days * a2
    v = first + s2 - s1
    trad = steps(("Totals of the two windows.", rf"First window: \({tex(days)}\times {tex(a1)} = {tex(s1)}\); second window: \({tex(days)}\times {tex(a2)} = {tex(s2)}\)."),
                 ("They share all days but the first and the last.", rf"Last day \(-\) first day \(= {tex(s2)} - {tex(s1)} = {tex(s2 - s1)}\)."),
                 ("The last day.", rf"\[ {tex(first)} + {tex(s2 - s1)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Each window has \({tex(days)}\) days."), apply(2),
                 ("Substitute the values.", rf"\[ {tex(first)} + {tex(days)}\times({tex(a2)} - {tex(a1)}) = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Sums \({tex(s1)}\) and \({tex(s2)}\).", rf"Difference \(= {tex(s2 - s1)}\).", rf"Last day \(= {tex(v)}\)."],
                  rf"\[ {tex(first)} + {tex(s2 - s1)} = {tex(v)} \]")


def r2_new_member(n, old, new, unit):
    n, old, new = map(F, (n, old, new))
    v = (n + 1) * new - n * old
    trad = steps(("Total before.", rf"\[ {tex(n)}\times {tex(old)} = {tex(n * old)} \]"), ("Total after.", rf"\[ {tex(n + 1)}\times {tex(new)} = {tex((n + 1) * new)} \]"),
                 ("The new member.", rf"\[ {tex((n + 1) * new)} - {tex(n * old)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"\({tex(n)}\) at \({tex(old)}\), then \({tex(n + 1)}\) at \({tex(new)}\)."), apply(2),
                 ("Substitute the values.", rf"\[ {tex(n + 1)}\times {tex(new)} - {tex(n)}\times {tex(old)} = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Before \(= {tex(n * old)}\).", rf"After \(= {tex((n + 1) * new)}\).", rf"New member \(= {tex(v)}\)."],
                  rf"\[ {tex((n + 1) * new)} - {tex(n * old)} = {tex(v)} \]")


def r2_remove(n, avg, removed, unit=""):
    n, avg = F(n), F(avg)
    removed = [F(r) for r in removed]
    S = n * avg - sum(removed)
    k = n - len(removed)
    v = S / k
    trad = steps(("Total of all.", rf"\[ {tex(n)}\times {tex(avg)} = {tex(n * avg)} \]"), ("Take the removed ones away.", rf"\[ {tex(n * avg)} - ({add(removed)}) = {tex(S)} \]"),
                 ("Average of the rest.", rf"\[ {tex(S)} \div {tex(k)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Average \(= {tex(avg)}\), number \(= {tex(n)}\)."), apply(2),
                 ("Substitute the values.", rf"\[ \frac{{{tex(avg)}\times {tex(n)} - {tex(sum(removed))}}}{{{tex(k)}}} = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Total \(= {tex(n * avg)}\).", rf"Rest \(= {tex(S)}\) for \({tex(k)}\).", rf"Average \(= {tex(v)}\)."],
                  rf"\[ \frac{{{tex(S)}}}{{{tex(k)}}} = {tex(v)} \]")


def r2_group_join(avg, k, kavg, drop, unit):
    avg, k, kavg, drop = map(F, (avg, k, kavg, drop))
    newavg = avg - drop
    x = k * (newavg - kavg) / (avg - newavg)
    trad = steps(("Let there be x at first.", rf"Total before \(= {tex(avg)}x\); the newcomers add \({tex(k)}\times {tex(kavg)} = {tex(k * kavg)}\)."),
                 ("Total after.", rf"\[ {tex(avg)}x + {tex(k * kavg)} = {tex(newavg)}(x + {tex(k)}) \]"),
                 ("Solve.", rf"\[ {tex(avg - newavg)}x = {tex(k * newavg - k * kavg)} \;\Rightarrow\; x = {tex(x)} \]"))
    rule = steps(("Identify the values.", rf"Old average \({tex(avg)}\), new average \({tex(newavg)}\), \({tex(k)}\) join at \({tex(kavg)}\)."), apply(2),
                 ("Substitute the values.", rf"Sums: \({tex(avg)}x + {tex(k)}\times {tex(kavg)} = {tex(newavg)}\times(x + {tex(k)})\), so \(x = {tex(x)}\)."))
    return result(("number", x), T2, trad, rule, U(x, unit), [rf"New average \(= {tex(newavg)}\).", rf"\({tex(avg - newavg)}x = {tex(k * newavg - k * kavg)}\).", rf"\(x = {tex(x)}\)."],
                  rf"\[ \frac{{{tex(k)}\times({tex(newavg)} - {tex(kavg)})}}{{{tex(drop)}}} = {tex(x)} \]")


def r2_income(m1, a1, m2, a2, save):
    m1, a1, m2, a2, save = map(F, (m1, a1, m2, a2, save))
    spend = m1 * a1 + m2 * a2
    inc = spend + save
    v = inc / (m1 + m2)
    trad = steps(("Spending in the year.", rf"\[ {tex(m1)}\times {m(a1)} + {tex(m2)}\times {m(a2)} = {m(spend)} \]"), ("Income in the year.", rf"\[ {m(spend)} + {m(save)} = {m(inc)} \]"),
                 ("Per month.", rf"\[ {m(inc)} \div {tex(m1 + m2)} = {m(v)} \]"))
    rule = steps(("Identify the values.", rf"Two groups of months with their averages."), apply(2),
                 ("Substitute the values.", rf"\[ \frac{{{tex(m1)}\times {m(a1)} + {tex(m2)}\times {m(a2)} + {m(save)}}}{{{tex(m1 + m2)}}} = {m(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, "Rs"), [rf"Spent \(= {m(spend)}\).", rf"Income \(= {m(inc)}\).", rf"Per month \(= {m(v)}\)."], rf"\[ \frac{{{m(inc)}}}{{{tex(m1 + m2)}}} = {m(v)} \]")


def r2_last(groups, total_n, avg, unit):
    """groups: [(days, average)]; the remaining day(s) make up total_n days at the overall average (one day left)."""
    groups = [(F(d), F(a)) for d, a in groups]
    avg, total_n = F(avg), F(total_n)
    S = total_n * avg
    have = sum(d * a for d, a in groups)
    v = S - have
    parts = " + ".join(tex(d) + r"\times " + tex(a) for d, a in groups)
    trad = steps(("Total for all the days.", rf"\[ {tex(total_n)}\times {tex(avg)} = {tex(S)} \]"),
                 ("Total of the known days.", rf"\[ {parts} = {tex(have)} \]"), ("The last day.", rf"\[ {tex(S)} - {tex(have)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Average \(= {tex(avg)}\) for \({tex(total_n)}\) days."), apply(2), ("Substitute the values.", rf"\[ {tex(avg)}\times {tex(total_n)} - {tex(have)} = {tex(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, unit), [rf"Whole sum \(= {tex(S)}\).", rf"Known \(= {tex(have)}\).", rf"Last day \(= {tex(v)}\)."], rf"\[ {tex(S)} - {tex(have)} = {tex(v)} \]")


def r2_annual(n, old, new):
    n, old, new = map(F, (n, old, new))
    month = (n + 1) * new - n * old
    v = 12 * month
    trad = steps(("Monthly pay of the newcomer.", rf"\[ {tex(n + 1)}\times {m(new)} - {tex(n)}\times {m(old)} = {m(month)} \]"), ("For a year.", rf"\[ 12\times {m(month)} = {m(v)} \]"))
    rule = steps(("Identify the values.", rf"\({tex(n)}\) at \({m(old)}\), then \({tex(n + 1)}\) at \({m(new)}\)."), apply(2),
                 ("Substitute the values.", rf"\[ 12\times({tex(n + 1)}\times {m(new)} - {tex(n)}\times {m(old)}) = {m(v)} \]"))
    return result(("number", v), T2, trad, rule, U(v, "Rs"), [rf"Monthly \(= {m(month)}\).", r"Times 12.", rf"Annual \(= {m(v)}\)."], rf"\[ 12\times {m(month)} = {m(v)} \]")


# ---------------------------------------------------------------- Rule 3
def r3_count(S, avg, unit):
    S, avg = F(S), F(avg)
    v = S / avg
    trad = steps(("Each item is worth the average on the whole.", rf"So the number is how many times the average goes into the sum."), ("Divide.", rf"\[ {tex(S)} \div {tex(avg)} = {tex(v)} \]"))
    rule = steps(("Identify the values.", rf"Sum \(= {tex(S)}\), average \(= {tex(avg)}\)."), apply(3), ("Substitute the values.", rf"\[ \frac{{{tex(S)}}}{{{tex(avg)}}} = {tex(v)} \]"))
    return result(("number", v), T3, trad, rule, U(v, unit), [rf"Sum \(= {tex(S)}\).", rf"Average \(= {tex(avg)}\).", rf"Number \(= {tex(v)}\)."], rf"\[ \frac{{{tex(S)}}}{{{tex(avg)}}} = {tex(v)} \]")


def r3_orchard(k, y1, y2, y3, avg):
    k, y1, y2, y3, avg = map(F, (k, y1, y2, y3, avg))
    # y1 (x+k) + y2 x + y3 (x-k) = avg * 3x
    x = k * (y3 - y1) / (y1 + y2 + y3 - 3 * avg)
    trad = steps(("Total fruit.", rf"\({tex(y1)}(x + {tex(k)}) + {tex(y2)}x + {tex(y3)}(x - {tex(k)}) = {tex(y1 + y2 + y3)}x - {tex(k * (y3 - y1))}\)."),
                 ("Number of trees.", rf"\((x + {tex(k)}) + x + (x - {tex(k)}) = 3x\)."),
                 ("Average per tree.", rf"\[ \frac{{{tex(y1 + y2 + y3)}x - {tex(k * (y3 - y1))}}}{{3x}} = {tex(avg)} \;\Rightarrow\; x = {tex(x)} \]"))
    rule = steps(("Identify the values.", rf"Sum \(= {tex(y1 + y2 + y3)}x - {tex(k * (y3 - y1))}\), average \(= {tex(avg)}\)."), apply(3),
                 ("Substitute the values.", rf"\[ 3x = \frac{{{tex(y1 + y2 + y3)}x - {tex(k * (y3 - y1))}}}{{{tex(avg)}}} \;\Rightarrow\; x = {tex(x)} \]"))
    return result(("number", x), T3, trad, rule, rf"\(x = {tex(x)}\)", [rf"Sum in terms of \(x\).", r"Number of trees \(3x\).", rf"\(x = {tex(x)}\)."], rf"\[ x = {tex(x)} \]")


CARDS = {
    1: card(1, "Average from the Sum and the Number", r"The average shares the total equally among all the quantities.", T1.split("<br>")[1],
            [("Sum", r"S"), ("Number", r"n"), ("Average", r"\frac{S}{n}")], r"The average lies between the smallest and the largest quantity.",
            "'Find the average of ...' / 'A batsman scores a, b and c runs; find his average.'",
            r"\(12, 15, 18\): \(\frac{45}{3}=15\).", r"Dividing by the wrong count (count every quantity once)."),
    2: card(2, "Sum from the Average and the Number", r"If every quantity were equal to the average, they would still add up to the same total.", T2.split("<br>")[1],
            [("Average", r"A"), ("Number", r"n"), ("Sum", r"A\times n")],
            r"Most average problems are solved this way: turn each average into a sum, compare the sums (before and after, part and whole).",
            "'The average of n quantities is A; find their total' / 'what must the next one be' / 'a member joins and the average changes'.",
            r"Average \(20\) of \(6\) numbers: sum \(=120\); for an average of \(21\) with a seventh number it must be \(7\times 21-120=27\).",
            r"Adding or averaging averages of groups of different sizes."),
    3: card(3, "Number from the Sum and the Average", r"The number of quantities is how many times the average goes into the sum.", T3.split("<br>")[1],
            [("Sum", r"S"), ("Average", r"A"), ("Number", r"\frac{S}{A}")], r"The answer must be a whole number when it counts things.",
            "'The sum of some quantities is S and their average is A; how many are there?'",
            r"Sum \(84\), average \(7\): \(\frac{84}{7}=12\).", r"Multiplying instead of dividing."),
}
OLD = {
    467: (1, "A girl scores 46, 58 and 61 marks in three tests. Find her average mark.", lambda: r1_list([46, 58, 61], "marks"), "marks"),
    468: (1, "What is the mean of the 7 smallest prime numbers?", lambda: r1_list(primes(7), "", "the first 7 prime numbers"), ""),
    469: (1, "A list holds the first 20 multiples of 7. What is the mean of the list?", lambda: r1_list([7 * i for i in range(1, 21)], "", "the first 20 multiples of 7"), ""),
    470: (1, "If p, q, r, s, t and u are six consecutive even numbers, by how much is their average more than p?", lambda: r1_consec_even(6), ""),
    471: (1, "A family spent Rs 54750 in the first half of a year and Rs 63875 in the second half. If the year had 365 days, what was its average daily spending?",
          lambda: r1_daily(54750, 63875, 365), "Rs"),
    472: (1, "The average of the first seven multiples of 4 is", lambda: r1_list([4 * i for i in range(1, 8)], "", "the first seven multiples of 4"), ""),
    473: (2, "The average mark of 85 pupils in a test is 42. Find their total marks.", lambda: r2_total(42, 85, "marks"), "marks"),
    474: (2, "The average weight of 45 boxes is 18 kg. Find their total weight.", lambda: r2_total(18, 45, "kg"), "kg"),
    475: (2, "The heights of 5 trees are 410 cm, 455 cm, 390 cm, 470 cm and 425 cm. How tall must a sixth tree be so that the average height of the six trees is 440 cm?",
          lambda: r2_missing([410, 455, 390, 470, 425], 440, "cm"), "cm"),
    476: (2, "The average rainfall from the 12th to the 18th of July, both days included, was 14.2 mm, and from the 13th to the 19th it was 15 mm. The rainfall on the 12th was 11.4 mm. What was it on the 19th?",
          lambda: r2_window(7, F("14.2"), 15, F("11.4"), "mm"), "mm"),
    477: (2, "The weights of five players of a team are 61 kg, 66 kg, 64 kg, 68 kg and 63 kg, and the average weight of the six people in the team, including the coach, is 65 kg. Find the coach's weight.",
          lambda: r2_missing([61, 66, 64, 68, 63], 65, "kg"), "kg"),
    478: (2, "The average age of 24 members of a club was 36 years. When a new member joined, the average fell to 35.6 years. How old is the new member?",
          lambda: r2_new_member(24, 36, F("35.6"), "years"), "years"),
    479: (2, "The average of 11 numbers is 26. What should a twelfth number be so that the average becomes 27?", lambda: r2_new_member(11, 26, 27, ""), ""),
    480: (2, "The average of 22 numbers is 40. If two of them, 52 and 68, are removed, what is the average of the rest?", lambda: r2_remove(22, 40, [52, 68]), ""),
    481: (2, "The average age of a choir is 30 years. 8 new singers with an average age of 21 years join it, and the average age falls by 3 years. How many singers were there at first?",
          lambda: r2_group_join(30, 8, 21, 3, "singers"), "singers"),
    482: (2, "A man spends an average of Rs 2300 a month for the first 4 months of a year and Rs 2500 a month for the next 8 months. If he saves Rs 4400 in the year, what is his average monthly income?",
          lambda: r2_income(4, 2300, 8, 2500, 4400), "Rs"),
    483: (2, "The average sale of a shop for the first 4 days of a week is Rs 520 and for the next 2 days Rs 610. If the average for all 7 days is Rs 560, what was the sale on the last day?",
          lambda: r2_last([(4, 520), (2, 610)], 7, 560, "Rs"), "Rs"),
    484: (2, "A runner covers 16 km on Monday and 23 km on Tuesday. How far must she run on Wednesday so that her average for the three days is 21 km?",
          lambda: r2_missing([16, 23], 21, "km"), "km"),
    485: (2, "The average monthly pay of 15 clerks is Rs 8400. When the manager's pay is added, the average becomes Rs 9000. What is the manager's annual pay?",
          lambda: r2_annual(15, 8400, 9000), "Rs"),
    486: (3, "The sum of some numbers is 96 and their average is 8. How many numbers are there?", lambda: r3_count(96, 8, ""), ""),
    487: (3, "The total weight of some parcels is 238 kg and their average weight is 14 kg. How many parcels are there?", lambda: r3_count(238, 14, "parcels"), "parcels"),
    488: (3, "A tailor earns Rs 380 a day on average. In how many days will he earn Rs 4560?", lambda: r3_count(4560, 380, "days"), "days"),
    489: (3, "In an orchard, (x + 3) trees give 50 fruits a year each, x trees give 90 fruits each and (x - 3) trees give 130 fruits each. If the average yield per tree is 80 fruits, find x.",
          lambda: r3_orchard(3, 50, 90, 130, 80), "x"),
}
NEW = {1: [("r1_e3", "Find the average of the first 8 prime numbers.", lambda: r1_list(primes(8), "", "the first 8 prime numbers"), ""),
           ("r1_e4", "A list holds the first 15 multiples of 4. What is the mean of the list?", lambda: r1_list([4 * i for i in range(1, 16)], "", "the first 15 multiples of 4"), "")],
       2: [("r2_e2", "A bowler has taken an average of 2.4 wickets a match in 65 matches. How many wickets has he taken?", lambda: r2_total(F("2.4"), 65, "wickets"), "wickets"),
           ("r2_e3", "The average score of 160 players is 47. What is their total score?", lambda: r2_total(47, 160, ""), "")],
       3: [("r3_e3", "The total rainfall in a month was 168 mm and the average daily rainfall was 5.6 mm. How many days were there in the month?", lambda: r3_count(168, F("5.6"), "days"), "days")]}


def opts(g, unit):
    v = F(g["answer"][1])
    if unit == "x":
        from helpers import place
        return place(rf"\(x = {tex(v)}\)", [rf"\(x = {tex(w)}\)" for w in (v + 2, v - 2, v + 4)])
    return nopts(v, unit)


def main():
    for rule in (1, 2, 3):
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
            op, _ = opts(g, unit)
            extra = {"question": q, **dict(zip("abcd", op)), "e": ""}
            extra = {k: v for k, v in extra.items() if v != rows[rid][k]}
            out.append(regen_entry(rows[rid], g, f"NEW_RULE_{rule}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cc = {"rule_name": f"Rule {rule}", "rule_html": CARDS[rule]}
        json.dump(cc, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, q, fn, unit in NEW[rule]:
            g = fn()
            op, pos = opts(g, unit)
            qs.append(new_question(rule, q, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            answers.append([key, [g["answer"][0], str(g["answer"][1])]])
        json.dump({"rules_html": [{"chapter": "average", **cc}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {rule}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
