"""Rules 8-13 (book I. Permutations, Rules 8-13): writes the six rule cards, regenerates the old rows in the prompt #13
layout and links them (all keys were right; options written as LaTeX, '50 ways.' style options cleaned, e = ''), and adds
the book's worked examples and exercises that had no copy (numbers / words changed). Rule 10's Exr 1 and 3 are rewritten
with 'three' / 'four particular delegates' (the book says 'two' but answers for 3 and 5). Same outputs as gen_1_7.py."""
import json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from pc_common import D, I, factorial, falling_tex, fin, nP, num, perm, result, times  # noqa: E402
import gen_1_7  # noqa: E402

VOW = set("AEIOU")


def pair(a, b):
    return ("pair", (a, b))


# ---------------------------------------------------------------- multiset helpers
def mset(items):
    """(tex, value) for the number of arrangements of a list with repeats: \\frac{7!}{2!\\,2!}."""
    c = Counter(items)
    n = len(items)
    reps = [k for k in c.values() if k > 1]
    v = factorial(n)
    for k in reps:
        v //= factorial(k)
    if not reps:
        return f"{n}!", v
    den = THIN.join(f"{k}!" for k in reps)
    return rf"\frac{{{n}!}}{{{den}}}", v


THIN = chr(92) + ","


def rep_note(items, what="letters", names=None):
    c = Counter(items)
    nm = names or {}
    if nm:                                            # 'the bag has 12 balls: 5 yellow balls, 4 green balls, 3 black balls.'
        return f"{len(items)} {what}: " + ", ".join(f"{k} {nm[x]}" for x, k in c.items()) + "."
    reps = [f"{x} occurs {k} times" if k > 2 else f"{x} occurs twice" for x, k in c.items() if k > 1]
    return (f"{len(items)} {what}; " + ", ".join(reps) + "." if reps else f"{len(items)} {what}, all different.")


# ---------------------------------------------------------------- Rule 8: m boys and (m-1) girls alternate
T8 = (r"The number of ways in which \(m\) boys and \((m-1)\) girls can be seated in a row so that they are alternate is"
      r"<br>\[ m!\times (m-1)! \]")


def r8(m):
    v = factorial(m) * factorial(m - 1)
    pat = " ".join(["B G"] * (m - 1)) + " B"
    expr = rf"{m}!\times {m - 1}!"
    trad = steps(
        ("Find the only possible pattern.", rf"With \({m}\) boys and \({m - 1}\) girls the row must start and end with a boy: {pat}. "
                                            r"(Starting with a girl would need as many girls as boys.)"),
        ("Fill the seats.", rf"The \({m}\) boys take the \({m}\) boy seats in \({m}!\) ways and the \({m - 1}\) girls take the girl seats in \({m - 1}!\) ways."),
        ("Multiply.", D(rf"{m}!\times {m - 1}! = {factorial(m)}\times {factorial(m - 1)} = {v}")))
    rule = steps(
        ("Identify the value.", rf"\(m = {m}\) boys, \(m - 1 = {m - 1}\) girls."),
        ("Apply the specified rule.", D(r"m!\times (m-1)!")),
        ("Substitute the value.", D(rf"{m}!\times {m - 1}! = {v}")))
    rb = [rf"\(m = {m}\).", r"Ways \(= m!\times (m-1)!\).", rf"\({expr} = {v}\)."]
    return result(num(v), T8, trad, rule, fin(expr, v), rb, D(rf"{expr} = {v}"))


# ---------------------------------------------------------------- Rule 9: two groups alternate round a circle
T9 = (r"The number of ways in which \(m\) persons of one group and \(m\) persons of another group can be seated along a circle "
      r"so that they are alternate is<br>\[ m!\times (m-1)! \]")


def r9(m, A, B):
    v = factorial(m) * factorial(m - 1)
    expr = rf"{m - 1}!\times {m}!"
    trad = steps(
        (f"Seat the {A} round the circle.", rf"In a circle only the order relative to one person matters, so \({m}\) {A} can sit in \(({m} - 1)! = {m - 1}!\) ways."),
        ("Mark the seats between them.", rf"There are \({m}\) places between the {A} (one between each pair of neighbours)."),
        (f"Seat the {B} in those places.", rf"The \({m}\) {B} fill these \({m}\) distinct places in \({m}!\) ways; now the groups alternate."),
        ("Multiply.", D(rf"{m - 1}!\times {m}! = {factorial(m - 1)}\times {factorial(m)} = {v}")))
    rule = steps(
        ("Identify the value.", rf"\(m = {m}\) in each group."),
        ("Apply the specified rule.", D(r"m!\times (m-1)!")),
        ("Substitute the value.", D(rf"{m}!\times ({m}-1)! = {m}!\times {m - 1}! = {v}")))
    rb = [rf"\(m = {m}\).", r"Ways \(= m!\times (m-1)!\).", rf"\({m}!\times {m - 1}! = {v}\)."]
    return result(num(v), T9, trad, rule, fin(expr, v), rb, D(rf"{m}!\times {m - 1}! = {v}"))


# ---------------------------------------------------------------- Rule 10: round table, m particular delegates together
T10 = (r"A round table conference is held between \(n\) delegates. The number of ways in which they can be seated so that "
       r"\(m\) particular delegates always sit together is<br>\[ (n-m)!\times m! \]"
       r"(With no restriction, \(n\) people sit round a table in \((n-1)!\) ways.)")


def r10(n, m):
    v = factorial(n - m) * factorial(m)
    expr = rf"{n - m}!\times {m}!"
    units = n - m + 1
    trad = steps(
        ("Tie the particular delegates together.", rf"Treat the \({m}\) delegates who must sit together as one unit: \({n} - {m} + 1 = {units}\) units round the table."),
        ("Seat the units round the table.", rf"Round a table only the order relative to one unit matters: \(({units} - 1)! = {units - 1}!\) ways."),
        ("Arrange inside the unit.", rf"The \({m}\) delegates can change places among themselves in \({m}!\) ways."),
        ("Multiply.", D(rf"{units - 1}!\times {m}! = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) delegates, \(m = {m}\) always together."),
        ("Apply the specified rule.", D(r"(n-m)!\times m!")),
        ("Substitute the values.", D(rf"({n} - {m})!\times {m}! = {expr} = {v}")))
    rb = [rf"\(n = {n}\), \(m = {m}\).", r"Ways \(= (n-m)!\times m!\).", rf"\(({n}-{m})!\times {m}! = {expr}\)."]
    return result(num(v), T10, trad, rule, fin(expr, v), rb, D(rf"({n}-{m})!\times {m}! = {expr}"))


def r10_circle(n, who):
    """n people round a table with no restriction (the circular-permutation note of Rule 10)."""
    v = factorial(n - 1)
    trad = steps(
        ("Fix one person.", rf"Turning the whole circle does not give a new seating, so seat one of the \({n}\) {who} anywhere; every other seat is now fixed relative to him."),
        ("Fill the other seats.", rf"The remaining \({n - 1}\) {who} fill the remaining \({n - 1}\) seats in \({falling_tex(n - 1, n - 1)} = {v}\) ways."))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) {who}, \(m = 1\) (no group has to sit together, so take each person alone)."),
        ("Apply the specified rule.", D(r"(n-m)!\times m! = (n-1)!\times 1!")),
        ("Substitute the values.", D(rf"({n} - 1)!\times 1! = {n - 1}! = {v}")))
    rb = [rf"\(n = {n}\), \(m = 1\).", r"Ways \(= (n-1)!\times 1! = (n-1)!\).", rf"\({n - 1}! = {v}\)."]
    return result(num(v), T10, trad, rule, I(v), rb, D(rf"({n}-1)! = {v}"))


# ---------------------------------------------------------------- Rule 11: necklace
T11 = r"The number of ways in which \(n\) different beads can be arranged to form a necklace is<br>\[ \frac{(n-1)!}{2} \]"


def r11(n, show_expr=True):
    v = factorial(n - 1) // 2
    expr = rf"\frac{{{n - 1}!}}{{2}}"
    trad = steps(
        ("Arrange the beads in a circle.", rf"Round a circle only the order relative to one bead matters: \(({n} - 1)! = {factorial(n - 1)}\) ways."),
        ("Allow for turning the necklace over.", r"A necklace can be turned over, so each clockwise arrangement is the same necklace as its anticlockwise one: every necklace is counted twice."),
        ("Halve the count.", D(rf"\frac{{{factorial(n - 1)}}}{{2}} = {v}")))
    rule = steps(
        ("Identify the value.", rf"\(n = {n}\) different beads."),
        ("Apply the specified rule.", D(r"\frac{(n-1)!}{2}")),
        ("Substitute the value.", D(rf"\frac{{({n}-1)!}}{{2}} = {expr} = {v}")))
    rb = [rf"\(n = {n}\).", r"Ways \(= \frac{(n-1)!}{2}\).", rf"\({expr} = {v}\)."]
    return result(num(v), T11, trad, rule, fin(expr, v) if show_expr else I(v), rb, D(rf"{expr} = {v}"))


# ---------------------------------------------------------------- Rule 12: things not all different
T12 = (r"The number of permutations of \(n\) things taken all at a time, when \(p\) of them are alike of one kind, \(q\) alike of a "
       r"second kind, \(r\) alike of a third kind and the rest are all different, is<br>\[ \frac{n!}{p!\,q!\,r!} \]"
       r"And if one work can be done in \(m\) ways and another in \(n\) ways, both together can be done in \(m\times n\) ways.")


def r12_word(word, what="letters", minus1=False, label=None, names=None):
    items = list(word)
    tex, v = mset(items)
    c = Counter(items)
    nm = names or {}
    reps = [(nm.get(x, x + "'s" if what == "letters" else x), k) for x, k in c.items() if k > 1]
    ans = v - 1 if minus1 else v
    lab = label or f"the word '{word}'"
    trad = steps(
        ("Count the things.", f"{lab[0].upper() + lab[1:]} has " + rep_note(items, what, names)),
        ("Pretend the alike things are different.", rf"If every one of the \({len(items)}\) {what} were different there would be \({len(items)}! = {factorial(len(items))}\) arrangements."),
        ("Remove the repeats.", "In each arrangement, swapping alike " + what + " among themselves gives the same arrangement: "
         + ", ".join(rf"the {k} {x} can be swapped in \({k}!\) ways" for x, k in reps) + ". So every arrangement was counted "
         + rf"\({times(*[f'{k}!' for _, k in reps])}\) times:" + D(rf"{tex} = {v}"))
        if reps else ("No repeats.", "All are different, so nothing is divided out."),
        *((("A rearrangement must differ from the word itself.", D(f"{v} - 1 = {ans}")),) if minus1 else ()))
    rule = steps(
        ("Identify the values.", rf"\(n = {len(items)}\)" + "".join(rf", {x}: \({k}\)" for x, k in reps) + "."),
        ("Apply the specified rule.", D(r"\frac{n!}{p!\,q!\,r!}") + (" and subtract the original order." if minus1 else "")),
        ("Substitute the values.", D(f"{tex} = {v}" + (f",\\qquad {v} - 1 = {ans}" if minus1 else ""))))
    rb = [rf"\(n = {len(items)}\)" + "".join(rf", {x} \(\times {k}\)" for x, k in reps) + ".", r"Ways \(= \frac{n!}{p!\,q!\,r!}\)" + (" \\(- 1\\)." if minus1 else "."),
          rf"\({tex} = {v}\)" + (rf", \({v} - 1 = {ans}\)." if minus1 else ".")]
    return result(num(ans), T12, trad, rule, I(ans), rb, D(f"{tex}" + (" - 1" if minus1 else "") + f" = {ans}"))


def r12_rearr_end(word, last):
    items = list(word)
    tex, v = mset(items)
    rest = list(word)
    rest.remove(last)
    tex2, v2 = mset(rest)
    trad = steps(
        ("Count all the arrangements.", f"'{word}' has " + rep_note(items) + rf" With the alike letters swapped among themselves giving nothing new:" + D(f"{tex} = {v}")),
        ("Rearrangements.", rf"One of these is the word itself:" + D(f"{v} - 1 = {v - 1}")),
        (f"Words ending in {last}.", rf"Put {last} in the last place; the other \({len(rest)}\) letters ({rep_note(rest)[:-1].split('; ', 1)[-1]}) fill the rest:" + D(f"{tex2} = {v2}")))
    rule = steps(
        ("Identify the values.", rf"All letters: \(n = {len(items)}\); with {last} fixed at the end: \(n = {len(rest)}\)."),
        ("Apply the specified rule.", D(r"\frac{n!}{p!\,q!\,r!}") + " for each part (and subtract the word itself for the rearrangements)."),
        ("Substitute the values.", D(f"{tex} - 1 = {v - 1},\\qquad {tex2} = {v2}")))
    rb = [rf"All letters: \(n = {len(items)}\); ending in {last}: \(n = {len(rest)}\).", r"Each part \(= \frac{n!}{p!\,q!\,r!}\); rearrangements subtract 1.",
          rf"\({tex} - 1 = {v - 1}\) and \({tex2} = {v2}\)."]
    return result(pair(v - 1, v2), T12, trad, rule, I(f"{v - 1}") + " and " + I(f"{v2}"), rb, D(f"{tex} - 1 = {v - 1},\\quad {tex2} = {v2}"))


def split(word):
    v = [ch for ch in word if ch in VOW]
    c = [ch for ch in word if ch not in VOW]
    return v, c


def word_together(word, T, rule_name):
    vs, cs = split(word)
    units = cs + ["(vowels)"]
    t_units, v_units = mset(units)
    t_in, v_in = mset(vs)
    v = v_units * v_in
    trad = steps(
        ("Tie the vowels together.", rf"'{word}' has the vowels {', '.join(vs)} and the consonants {', '.join(cs)}. Treat the \({len(vs)}\) vowels as one letter: "
                                     rf"\({len(cs)} + 1 = {len(units)}\) letters to arrange."),
        ("Arrange the letters.", rep_note(units).replace("(vowels)", "the vowel block") + D(f"{t_units} = {v_units}")),
        ("Arrange the vowels inside their block.", rep_note(vs, "vowels") + D(f"{t_in} = {v_in}")),
        ("Multiply.", D(f"{v_units}\\times {v_in} = {v}")))
    rule = steps(
        ("Identify the values.", rf"Units: \({len(units)}\) (the vowel block and \({len(cs)}\) consonants); vowels in the block: \({len(vs)}\)."),
        ("Apply the specified rule.", rule_name),
        ("Substitute the values.", D(f"{t_units}\\times {t_in} = {v_units}\\times {v_in} = {v}")))
    rb = [rf"\({len(units)}\) units (vowel block + consonants), \({len(vs)}\) vowels inside.", rule_name, rf"\({t_units}\times {t_in} = {v}\)."]
    return result(num(v), T, trad, rule, I(v), rb, D(f"{t_units}\\times {t_in} = {v}"))


R12_PRODUCT = r"Arrange the units with \(\frac{n!}{p!\,q!\,r!}\), then the things inside the tied group the same way, and multiply (\(m\times n\))."


def r12_not_all_together(word):
    vs, cs = split(word)
    t_all, v_all = mset(list(word))
    t_units, v_units = mset(cs + ["(v)"])
    t_in, v_in = mset(vs)
    tog = v_units * v_in
    v = v_all - tog
    trad = steps(
        ("Count all the arrangements.", f"'{word}' has " + rep_note(list(word)) + D(f"{t_all} = {v_all}")),
        ("Count those with the vowels together.", rf"Tie the vowels {', '.join(vs)} into one letter: \({len(cs) + 1}\) letters, then arrange the vowels inside:"
         + D(f"{t_units}\\times {t_in} = {v_units}\\times {v_in} = {tog}")),
        ("Subtract.", D(f"{v_all} - {tog} = {v}")))
    rule = steps(
        ("Identify the values.", rf"All \({len(word)}\) letters; the \({len(vs)}\) vowels as one block with \({len(cs)}\) consonants."),
        ("Apply the specified rule.", r"Count all arrangements and the 'together' arrangements with \(\frac{n!}{p!\,q!\,r!}\) (times the inside order), then subtract."),
        ("Substitute the values.", D(f"{t_all} - {t_units}\\times {t_in} = {v_all} - {tog} = {v}")))
    rb = [rf"All: \({t_all} = {v_all}\).", rf"Vowels together: \({t_units}\times {t_in} = {tog}\).", rf"\({v_all} - {tog} = {v}\)."]
    return result(num(v), T12, trad, rule, I(v), rb, D(f"{t_all} - {t_units}\\times {t_in} = {v}"))


def r12_relative(word):
    vs, cs = split(word)
    tv, vv = mset(vs)
    tc, vc = mset(cs)
    v = vv * vc
    trad = steps(
        ("Keep the places of the vowels and of the consonants.", rf"'{word}' has \({len(vs)}\) vowels ({', '.join(vs)}) and \({len(cs)}\) consonants ({', '.join(cs)}). "
                                                              "Keeping the relative order means vowels may move only into vowel places and consonants only into consonant places."),
        ("Arrange the vowels in the vowel places.", rep_note(vs, "vowels") + D(f"{tv} = {vv}")),
        ("Arrange the consonants in the consonant places.", rep_note(cs, "consonants") + D(f"{tc} = {vc}")),
        ("Multiply.", D(f"{vv}\\times {vc} = {v}")))
    rule = steps(
        ("Identify the values.", rf"Vowels: \({len(vs)}\); consonants: \({len(cs)}\)."),
        ("Apply the specified rule.", r"Each group is arranged with \(\frac{n!}{p!\,q!\,r!}\) and the two jobs multiply (\(m\times n\))."),
        ("Substitute the values.", D(f"{tv}\\times {tc} = {vv}\\times {vc} = {v}")))
    rb = [rf"Vowels \({len(vs)}\), consonants \({len(cs)}\).", r"Arrange each group in its own places; multiply.", rf"\({tv}\times {tc} = {v}\)."]
    return result(num(v), T12, trad, rule, I(v), rb, D(f"{tv}\\times {tc} = {v}"))


def r12_places(word, parity):
    """Vowels only in the even (parity 0) / odd (parity 1) places; letters all different."""
    vs, cs = split(word)
    n = len(word)
    places = [i for i in range(1, n + 1) if i % 2 == (1 if parity else 0)]
    k = len(places)
    v = perm(k, len(vs)) * factorial(n - len(vs))
    name = "odd" if parity else "even"
    trad = steps(
        (f"List the {name} places.", rf"'{word}' has \({n}\) letters; the {name} places are {', '.join(map(str, places))}: \({k}\) places for the \({len(vs)}\) vowels ({', '.join(vs)})."),
        ("Seat the vowels.", rf"The 1st vowel has \({k}\) choices, the 2nd \({k - 1}\), and so on:" + D(f"{falling_tex(k, len(vs))} = {perm(k, len(vs))}")),
        ("Seat the consonants.", rf"The \({len(cs)}\) consonants fill the \({n - len(vs)}\) places left in \({n - len(vs)}! = {factorial(n - len(vs))}\) ways."),
        ("Multiply.", D(f"{perm(k, len(vs))}\\times {factorial(n - len(vs))} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\({k}\) {name} places, \({len(vs)}\) vowels; \({len(cs)}\) consonants."),
        ("Apply the specified rule.", r"Vowels in the allowed places in \({}^{k}P_{v}\) ways, the consonants in the rest; multiply (\(m\times n\))."),
        ("Substitute the values.", D(f"{nP(k, len(vs))}\\times {len(cs)}! = {perm(k, len(vs))}\\times {factorial(len(cs))} = {v}")))
    rb = [rf"\({k}\) {name} places, \({len(vs)}\) vowels, \({len(cs)}\) consonants.", r"Vowels \({}^{k}P_{v}\) ways, consonants in the rest; multiply.",
          rf"\({nP(k, len(vs))}\times {len(cs)}! = {v}\)."]
    return result(num(v), T12, trad, rule, I(v), rb, D(f"{nP(k, len(vs))}\\times {len(cs)}! = {v}"))


def r12_no_two(nv, nc):
    v = factorial(nc) * perm(nc + 1, nv)
    trad = steps(
        ("Place the consonants first.", rf"The \({nc}\) consonants can be arranged in \({nc}! = {factorial(nc)}\) ways."),
        ("Use the gaps.", rf"They leave \({nc + 1}\) gaps (between them and at both ends); putting each of the \({nv}\) vowels in a different gap keeps every two vowels apart:"
         + D(f"{falling_tex(nc + 1, nv)} = {perm(nc + 1, nv)}")),
        ("Multiply.", D(f"{factorial(nc)}\\times {perm(nc + 1, nv)} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\({nc}\) consonants, \({nv}\) vowels, all different."),
        ("Apply the specified rule.", r"Consonants in \(c!\) ways and vowels in the \(c+1\) gaps in \({}^{c+1}P_{v}\) ways; multiply (\(m\times n\))."),
        ("Substitute the values.", D(f"{nc}!\\times {nP(nc + 1, nv)} = {factorial(nc)}\\times {perm(nc + 1, nv)} = {v}")))
    rb = [rf"\({nc}\) consonants, \({nv}\) vowels.", r"\(c!\times {}^{c+1}P_{v}\).", rf"\({nc}!\times {nP(nc + 1, nv)} = {v}\)."]
    return result(num(v), T12, trad, rule, I(v), rb, D(f"{nc}!\\times {nP(nc + 1, nv)} = {v}"))


def r12_periods(subjects, periods):
    """periods = subjects + 1: one subject gets two periods."""
    assert periods == subjects + 1
    each = factorial(periods) // 2
    v = subjects * each
    trad = steps(
        ("See how the periods are shared.", rf"\({periods}\) periods and \({subjects}\) subjects, each at least once: exactly one subject gets two periods, the others one each."),
        ("Choose the doubled subject.", rf"\({subjects}\) ways."),
        ("Arrange the timetable.", rf"The \({periods}\) periods now hold \({periods}\) entries in which one subject appears twice: \(\frac{{{periods}!}}{{2!}} = {each}\) orders."),
        ("Multiply.", D(f"{subjects}\\times {each} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\(n = {periods}\) entries, one subject repeated (\(p = 2\)); \({subjects}\) choices for that subject."),
        ("Apply the specified rule.", r"Orders \(= \frac{n!}{p!}\) for each choice; the choice and the order multiply (\(m\times n\))."),
        ("Substitute the values.", D(rf"{subjects}\times \frac{{{periods}!}}{{2!}} = {subjects}\times {each} = {v}")))
    rb = [rf"\({periods}\) periods, one of the \({subjects}\) subjects twice.", r"\(\text{subjects}\times \frac{n!}{2!}\).", rf"\({subjects}\times \frac{{{periods}!}}{{2!}} = {v}\)."]
    return result(num(v), T12, trad, rule, I(v), rb, D(rf"{subjects}\times \frac{{{periods}!}}{{2!}} = {v}"))


# ---------------------------------------------------------------- Rule 13: certain things together
T13 = (r"When certain things must occur together, tie each such group into one unit, arrange the units, then arrange the things "
       r"inside each unit, and multiply:<br>\[ \text{Ways} = (\text{arrangements of the units})\times (\text{arrangements inside each group}) \]")
R13_RULE = r"Ways \(=\) (arrangements of the units) \(\times\) (arrangements inside each group)."


def r13_groups(groups, singles=0, identical=False, what="persons"):
    """groups: list of (name, size). identical: the things inside a group are alike (one order only)."""
    units = len(groups) + singles
    inside = 1 if identical else 1
    parts = []
    for _, s in groups:
        if not identical:
            inside *= factorial(s)
            parts.append(f"{s}!")
    v = factorial(units) * inside
    expr = times(f"{units}!", *parts) if parts else f"{units}!"
    trad = steps(
        ("Tie each group into one unit.", "Groups: " + ", ".join(f"{name} ({s})" for name, s in groups)
         + (rf", plus \({singles}\) single {what}" if singles else "") + rf". That gives \({units}\) units."),
        ("Arrange the units.", rf"\({units}! = {factorial(units)}\) ways."),
        ("Arrange inside the groups.", ("The copies inside a group are identical, so each group can be arranged in only \\(1\\) way." if identical else
                                        "Inside each group: " + ", ".join(rf"\({s}!\)" for _, s in groups) + rf" ways, that is \({inside}\) ways in all.")),
        ("Multiply.", D(f"{expr} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\({units}\) units; group sizes " + ", ".join(rf"\({s}\)" for _, s in groups) + ("" if not identical else " (identical copies)") + "."),
        ("Apply the specified rule.", R13_RULE),
        ("Substitute the values.", D(f"{expr} = {v}")))
    rb = [rf"\({units}\) units, groups of " + ", ".join(str(s) for _, s in groups) + ".", R13_RULE, rf"\({expr} = {v}\)."]
    return result(num(v), T13, trad, rule, fin(expr, v), rb, D(f"{expr} = {v}"))


# ---------------------------------------------------------------- cards
CARDS = {
    8: card(8, "m Boys and (m - 1) Girls Alternate in a Row",
            r"The number of ways in which \(m\) boys and \((m-1)\) girls can be seated in a row so that they are alternate is \(m!\times (m-1)!\).",
            r"\[ m!\times (m-1)! \]",
            [("Boys", "m"), ("Girls", "m-1"), ("Only pattern", r"BGBG\cdots GB"), ("Ways", r"m!\times (m-1)!")],
            r"With one boy more than girls, the row must begin and end with a boy, so there is only ONE pattern; boys and girls then fill their own seats.",
            r"'Alternate' in a row with the two numbers differing by one (10 boys and 9 girls, 5 boys and 4 girls).",
            r"4 boys and 3 girls: \(4!\times 3! = 24\times 6 = 144\).",
            r"Multiplying by \(2\) as in Rule 7 - with unequal numbers the row can not start with a girl."),
    9: card(9, "Two Groups Alternate round a Circle",
            r"The number of ways in which \(m\) persons of one group and \(m\) persons of another group can sit along a circle so that "
            r"they are alternate is \(m!\times (m-1)!\).",
            r"\[ m!\times (m-1)! \]",
            [("First group round the circle", "(m-1)!"), ("Places between them", "m"), ("Second group", "m!"), ("Ways", r"m!\times (m-1)!")],
            r"Seat one group first: round a circle that is \((m-1)!\) ways. The \(m\) places between them are now all different, so the other group fills them in \(m!\) ways.",
            r"'Seated along a circle (round table) so that they are alternate', equal numbers of two kinds.",
            r"5 Indians and 5 Englishmen: \(4!\times 5! = 24\times 120 = 2880\).",
            r"Using \(2(m!)^{2}\) from the row rule, or \(((m-1)!)^{2}\): only the first group is circular, the second sits in fixed places."),
    10: card(10, "Round Table: Particular Persons Together",
             r"A round table conference is held between \(n\) delegates. The number of ways they can be seated so that \(m\) particular "
             r"delegates always sit together is \((n-m)!\times m!\). With no restriction, \(n\) people sit round a table in \((n-1)!\) ways.",
             r"\[ (n-m)!\times m! \]",
             [("Delegates", "n"), ("Must sit together", "m"), ("Units round the table", "n-m+1"), ("Ways", r"(n-m)!\times m!")],
             r"Tie the \(m\) delegates into one unit: \(n-m+1\) units round a table in \((n-m)!\) ways (circular: one less than the number of units), "
             r"and the \(m\) can change places inside the unit in \(m!\) ways.",
             r"'Round table', 'circular order', 'two (three) particular delegates always sit together'.",
             r"20 delegates, 2 particular ones together: \((20-2)!\times 2! = 18!\times 2!\).",
             r"Using \((n-m+1)!\) as for a row - round a table one unit is fixed, so it is \((n-m)!\)."),
    11: card(11, "Necklace of Different Beads",
             r"The number of ways in which \(n\) different beads can be arranged to form a necklace (or garland) is \(\frac{(n-1)!}{2}\).",
             r"\[ \frac{(n-1)!}{2} \]",
             [("Beads", "n"), ("Round a circle", "(n-1)!"), ("Turned over is the same", r"\div 2"), ("Ways", r"\frac{(n-1)!}{2}")],
             r"Round a circle there are \((n-1)!\) arrangements; a necklace can be turned over, so a clockwise arrangement and its anticlockwise mirror are one necklace.",
             r"'Necklace', 'garland', 'beads', 'flowers on a ring' - anything that can be flipped over.",
             r"6 beads: \(\frac{5!}{2} = 60\).",
             r"Forgetting to halve (that is the count for people at a round table, who can not be flipped)."),
    12: card(12, "Permutations of Things Not All Different",
             r"The number of permutations of \(n\) things taken all at a time, when \(p\) are alike of one kind, \(q\) alike of a second kind, "
             r"\(r\) alike of a third kind and the rest different, is \(\frac{n!}{p!\,q!\,r!}\). Combine with the multiplication rule: "
             r"if one job can be done in \(m\) ways and another in \(n\) ways, both can be done in \(m\times n\) ways.",
             r"\[ \frac{n!}{p!\,q!\,r!} \]",
             [("All things", "n"), ("Alike of one kind", "p"), ("Alike of another kind", "q"), ("Arrangements", r"\frac{n!}{p!\,q!\,r!}")],
             r"If the alike things were labelled, there would be \(n!\) arrangements; removing the labels makes \(p!\,q!\,r!\) of them look the same.",
             r"Words from the letters of a word with repeated letters, balls of the same colour in a row, 'rearrangements' (subtract the word itself), "
             r"'vowels together', 'vowels in the even places', 'relative order of vowels and consonants unchanged'.",
             r"'CIVILIZATION' has 12 letters with 4 I's: \(\frac{12!}{4!}\) arrangements, so \(\frac{12!}{4!} - 1\) rearrangements.",
             r"Dividing only by the repeats of one letter, or forgetting to subtract 1 when the question asks for REarrangements."),
    13: card(13, "Arrangements with Certain Things Together",
             r"There is no single formula when certain things must be together. Tie each such group into one unit, arrange the units, "
             r"arrange the things inside each unit, and multiply.",
             r"\[ \text{Ways} = (\text{arrangements of the units})\times (\text{arrangements inside each group}) \]",
             [("Each group", r"\text{one unit}"), ("Units", r"(\text{groups} + \text{singles})!"), ("Inside a group of k things", "k!"), ("Identical copies inside", "1")],
             r"Things that must be together behave like one block in the row; the block can still be reordered inside.",
             r"'Persons of the same nationality sit together', 'volumes of the same book are not separated', 'the vowels always come together'.",
             r"8 Indians, 4 Americans and 4 Englishmen, each nationality together: \(3!\times 8!\times 4!\times 4!\).",
             r"Forgetting the arrangements inside the groups, or multiplying by them when the things inside are identical copies."),
}

OLD = {
    8: {},
    9: {852: (lambda: r9(5, "Indians", "Englishmen"), None,
              {"a": r"\(5!\times 5!\)", "b": r"\(5!\times 6!\)", "c": r"\(5!\times 4!\)", "d": r"\(4!\times 4!\)"}),
        901: (lambda: r9(5, "girls", "boys"), None, None)},
    10: {853: (lambda: r10(20, 2), "A round table conference is to be held between 20 delegates of 20 countries. In how many ways can they be seated "
                                   "if two particular delegates are always to sit together?",
               {"a": r"\(15!\times 18!\)", "b": r"\(18!\times 12!\)", "c": r"\(5!\times 2!\)", "d": r"\(18!\times 2!\)"}),
         908: (lambda: r10_circle(7, "boys"), None, None)},
    11: {854: (lambda: r11(6, False), None, {"a": "50 ways", "c": "60 ways"}),
         909: (lambda: r11(7, False), "In how many ways can 7 different beads be arranged to form a necklace?", None)},
    12: {888: (lambda: r12_places("DETAIL", 1), None, None),
         890: (lambda: r12_word("LEADER"), None, None),
         892: (lambda: r12_word("ENGINEERING"), "How many arrangements can be made out of the letters of the word 'ENGINEERING'?", None),
         895: (lambda: r12_word("RUMOUR"), None, None),
         896: (lambda: r12_periods(5, 6), None, None),
         907: (lambda: r12_word("YYYYYGGGGBBB", "balls", label="the bag", names={"Y": "yellow balls", "G": "green balls", "B": "black balls"}), None, None)},
    13: {881: (lambda: word_together("OPTICAL", T13, R13_RULE), None, None),
         882: (lambda: word_together("CORPORATION", T13, R13_RULE), None, None),
         886: (lambda: word_together("LEADING", T13, R13_RULE), None, None),
         889: (lambda: word_together("JUDGE", T13, R13_RULE), None, None)},
}

NEW = {
    8: [("r8_x1", "In how many ways can 6 boys and 5 girls be seated in a row so that they are alternate?", lambda: r8(6),
         [r"\(2(6!\times 5!)\)", r"\(6!\times 5!\)", r"\(6!\times 6!\)", r"\(11!\)"], 2),
        ("r8_e1", "In how many ways can 9 boys and 8 girls be seated in a row so that they are alternate?", lambda: r8(9),
         [r"\(9!\times 8!\)", r"\(9!\times 9!\)", r"\(2(9!\times 8!)\)", r"\(8!\times 8!\)"], 1),
        ("r8_e2", "In how many ways can 7 boys and 6 girls be seated in a row so that they are alternate?", lambda: r8(7),
         [r"\(7!\times 7!\)", r"\(2(7!\times 6!)\)", r"\(6!\times 6!\)", r"\(7!\times 6!\)"], 4),
        ("r8_e3", "In how many ways can 3 boys and 2 girls be seated in a row so that they are alternate?", lambda: r8(3),
         ["24", "6", "12", "120"], 3)],
    9: [("r9_e1", "In how many ways can 6 Indians and 6 Englishmen be seated along a circle so that they are alternate?", lambda: r9(6, "Indians", "Englishmen"),
         [r"\(6!\times 6!\)", r"\(5!\times 6!\)", r"\(2(5!\times 6!)\)", r"\(5!\times 5!\)"], 2),
        ("r9_e2", "In how many ways can 7 Indians and 7 Englishmen be seated along a circle so that they are alternate?", lambda: r9(7, "Indians", "Englishmen"),
         [r"\(7!\times 7!\)", r"\(6!\times 6!\)", r"\(2\times 6!\times 7!\)", r"\(6!\times 7!\)"], 4),
        ("r9_e3", "In how many ways can 3 Indians and 3 Englishmen be seated along a circle so that they are alternate?", lambda: r9(3, "Indians", "Englishmen"),
         ["12", "36", "72", "4"], 1)],
    10: [("r10_e1", "A round table conference is to be held between 16 delegates. In how many ways can they be seated if three particular delegates are always to sit together?",
          lambda: r10(16, 3), [r"\(13!\times 2!\)", r"\(14!\times 3!\)", r"\(13!\times 3!\)", r"\(15!\times 3!\)"], 3),
         ("r10_e2", "A round table conference is to be held between 14 delegates. In how many ways can they be seated if two particular delegates are always to sit together?",
          lambda: r10(14, 2), [r"\(12!\times 2!\)", r"\(13!\times 2!\)", r"\(12!\)", r"\(11!\times 2!\)"], 1),
         ("r10_e3", "A round table conference is to be held between 19 delegates. In how many ways can they be seated if four particular delegates are always to sit together?",
          lambda: r10(19, 4), [r"\(16!\times 4!\)", r"\(15!\times 4!\)", r"\(15!\times 3!\)", r"\(14!\times 4!\)"], 2)],
    11: [("r11_e1", "Find the number of ways in which 5 different beads can be arranged to form a necklace.", lambda: r11(5),
          [r"\(\frac{5!}{2}\)", r"\(4!\)", r"\(\frac{3!}{2}\)", r"\(\frac{4!}{2}\)"], 4),
         ("r11_e2", "Find the number of ways in which 9 different beads can be arranged to form a necklace.", lambda: r11(9),
          [r"\(\frac{9!}{2}\)", r"\(\frac{8!}{2}\)", r"\(8!\)", r"\(\frac{7!}{2}\)"], 2),
         ("r11_e3", "Find the number of ways in which 10 different beads can be arranged to form a necklace.", lambda: r11(10),
          [r"\(\frac{9!}{2}\)", r"\(9!\)", r"\(\frac{10!}{2}\)", r"\(\frac{8!}{2}\)"], 1)],
    12: [("r12_x1", "Find the number of permutations of the letters of the word 'STATISTICS'.", lambda: r12_word("STATISTICS"),
          ["50400", "25200", "100800", "151200"], 1),
         ("r12_x2", "How many different words can be formed with the letters of the word 'EXAMINATION' so that all the vowels come together?",
          lambda: word_together("EXAMINATION", T12, R12_PRODUCT), ["129600", "32400", "64800", "43200"], 3),
         ("r12_e1", "In how many ways can the letters of the word 'ASSISTANT' be rearranged?", lambda: r12_word("ASSISTANT", minus1=True),
          ["15120", "15119", "30239", "7559"], 2),
         ("r12_e2", "In how many ways can the letters of the word 'ARTICLE' be arranged so that the three vowels are not all together?",
          lambda: r12_not_all_together("ARTICLE"), ["720", "5040", "4320", "3600"], 3),
         ("r12_e3", "Find the number of rearrangements of the letters of the word 'EXCELLENT'. How many of them end in T?",
          lambda: r12_rearr_end("EXCELLENT", "T"), [r"\(30240\), \(3360\)", r"\(30239\), \(3359\)", r"\(15119\), \(3360\)", r"\(30239\), \(3360\)"], 4),
         ("r12_e4", "How many words can be formed with the letters of the word 'CALCUTTA' without changing the relative order of the vowels and consonants?",
          lambda: r12_relative("CALCUTTA"), ["180", "90", "60", "360"], 2),
         ("r12_e5", "How many different words can be formed with the letters of the word 'CHAMPION' when the vowels occupy only the even places?",
          lambda: r12_places("CHAMPION", 0), ["2880", "720", "1440", "4320"], 1),
         ("r12_e6", "How many different words can be formed with seven different letters, of which three are vowels and four are consonants, "
                    "so that no two vowels are together in any word?", lambda: r12_no_two(3, 4), ["720", "2880", "1440", "1200"], 3),
         ("r12_e7", "The letters of the word TOMORROW are arranged so that all the vowels come together. Find the number of such arrangements.",
          lambda: word_together("TOMORROW", T12, R12_PRODUCT), ["720", "120", "180", "360"], 4),
         ("r12_e8", "How many different letter arrangements can be made from the letters of the word PEPPER?", lambda: r12_word("PEPPER"),
          ["60", "120", "720", "30"], 1)],
    13: [("r13_x1", "In how many ways can 5 Indians, 3 Americans and 2 Englishmen be seated in a row so that all persons of the same nationality sit together?",
          lambda: r13_groups([("Indians", 5), ("Americans", 3), ("Englishmen", 2)]),
          [r"\(5!\times 3!\times 2!\)", r"\(3!\times 5!\times 3!\times 2!\)", r"\(10!\)", r"\(2!\times 5!\times 3!\times 2!\)"], 2),
         ("r13_e1", "There are 15 books, of which 3 are single volumes and the others are books of 6, 4 and 2 volumes. In how many ways can all these books "
                    "be arranged on a shelf so that volumes of the same book are not separated?",
          lambda: r13_groups([("the 6-volume book", 6), ("the 4-volume book", 4), ("the 2-volume book", 2)], singles=3, what="volumes"),
          [r"\(6!\times 6!\times 4!\times 2!\)", r"\(6!\times 4!\times 2!\)", r"\(3!\times 6!\times 4!\times 2!\)", r"\(15!\)"], 1),
         ("r13_e2", "A library has two books with three copies each and four other books with two copies each. In how many ways can all these books "
                    "be arranged on a shelf so that copies of the same book are not separated?",
          lambda: r13_groups([("book 1", 3), ("book 2", 3), ("book 3", 2), ("book 4", 2), ("book 5", 2), ("book 6", 2)], identical=True, what="books"),
          ["120", "720", "5040", "1440"], 2),
         ("r13_e3", "5 boys and 3 girls are to be seated in a row so that the three girls are always together. In how many different ways can they be seated?",
          lambda: r13_groups([("the girls", 3)], singles=5, what="boys"), ["720", "4320", "40320", "2880"], 2),
         ("r13_e4", "In how many different ways can the letters of the word PATTERN be arranged so that the vowels always come together?",
          lambda: word_together("PATTERN", T13, R13_RULE), ["1440", "360", "2520", "720"], 4)],
}


def main():
    gen_1_7.OLD, gen_1_7.NEW, gen_1_7.CARDS = OLD, NEW, CARDS
    gen_1_7.main(range(8, 14))


if __name__ == "__main__":
    main()
