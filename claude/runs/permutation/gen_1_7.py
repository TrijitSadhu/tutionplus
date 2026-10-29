"""Rules 1-7 (book I. Permutations, Rules 1-7): writes the seven rule cards (the chapter had none), regenerates every
old row in the prompt #13 layout (Theorem -> Traditional Method -> Specified Rule -> Verification -> Final Answer),
links it to its card and cleans it ($$..$$ math the site does not render, display math in options, empty fifth option,
'319.' style options); fixes 894 (no option held 9900, key on the empty option e) and 903 (720 printed twice). Adds the
book exercises that had no copy (numbers changed, wording rewritten) as one JsonImport payload per rule.
Writes ruleNN/2_new_rows.json, ruleNN/3_rule_card.json, ruleNN/3_json_import_payload.json + 3_answers.json."""
import json, os, sys
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import card, new_question, regen_entry, steps  # noqa: E402
from pc_common import D, F, I, factorial, factorise, falling, falling_tex, fin, nP, num, perm, result, times  # noqa: E402

CH = "permutation_combination"


# ---------------------------------------------------------------- Rule 1: nPr directly
T1 = (r"The number of permutations (arrangements) of \(n\) different things taken \(r\) at a time is<br>"
      r"\[ {}^{n}P_{r} = \frac{n!}{(n-r)!} = n(n-1)(n-2)\cdots \text{ (} r \text{ factors)} \]")


def r1_find_n(r, V):
    n = next(k for k in range(r, 200) if perm(k, r) == V)
    fs = falling(n, r)
    trad = steps(
        ("Count the arrangements place by place.",
         rf"To arrange \(r = {r}\) of \(n\) different things, the 1st place can be filled in \(n\) ways, the 2nd in \(n-1\) ways, and so on. "
         rf"So the number of arrangements is a product of \({r}\) consecutive whole numbers, the largest being \(n\)."),
        ("Factorise the given number.", D(f"{V} = {factorise(V)}")),
        ("Regroup the factors into consecutive numbers.", D(f"{V} = {times(*fs)}") + rf"The largest of these \({r}\) consecutive numbers is \({n}\)."))
    rule = steps(
        ("Identify the values.", rf"\(r = {r}\), \({nP('n', r)} = {V}\)."),
        ("Apply the specified rule.", D(rf"{nP('n', r)} = \frac{{n!}}{{(n-{r})!}} = " + times(*[("n" if i == 0 else f"(n-{i})") for i in range(r)]))),
        ("Substitute and solve.", D(times(*[("n" if i == 0 else f"(n-{i})") for i in range(r)]) + f" = {V} = {times(*fs)}") + rf"\(\therefore n = {n}\)."))
    rb = [rf"\(r = {r}\), \({nP('n', r)} = {V}\).", rf"\({nP('n', r)} = n(n-1)\cdots\) (\({r}\) factors).",
          rf"\({V} = {times(*fs)}\), so \(n = {n}\)."]
    sc = D(f"{V} = {times(*fs)} \\Rightarrow n = {n}")
    return result(num(n), T1, trad, rule, I(f"n = {n}"), rb, sc)


def r1_find_r(n, V):
    r = next(k for k in range(0, n + 1) if perm(n, k) == V)
    fs = falling(n, r)
    trad = steps(
        ("Count the arrangements place by place.",
         rf"Arranging \(r\) of \({n}\) different things: the 1st place in \({n}\) ways, the 2nd in \({n - 1}\) ways, the 3rd in \({n - 2}\) ways, and so on, "
         rf"one factor for every place."),
        ("Divide the given number by these factors in turn.",
         "<br>".join(I(rf"{V // perm(n, i)} \div {n - i} = {V // perm(n, i + 1)}") for i in range(r))),
        ("Count the factors used.", rf"We reached \(1\) after \({r}\) factors \(({times(*fs)} = {V})\), so \({r}\) places were filled."))
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\), \({nP(n, 'r')} = {V}\)."),
        ("Apply the specified rule.", D(rf"{nP(n, 'r')} = \frac{{{n}!}}{{({n}-r)!}} = {n}\times {n - 1}\times {n - 2}\cdots \text{{ (r factors)}}")),
        ("Substitute and solve.", D(f"{V} = {times(*fs)}") + rf"This is a product of \({r}\) factors, so \(r = {r}\)."))
    rb = [rf"\(n = {n}\), \({nP(n, 'r')} = {V}\).", rf"\({nP(n, 'r')} = {n}\times {n - 1}\times\cdots\) (\(r\) factors).",
          rf"\({V} = {times(*fs)}\), so \(r = {r}\)."]
    sc = D(f"{V} = {times(*fs)} \\Rightarrow r = {r}")
    return result(num(r), T1, trad, rule, I(f"r = {r}"), rb, sc)


def r1_value(n, r, places, things, thing):
    """places: names of the r places in order; things / thing: what fills them (e.g. 'letters' / 'letter')."""
    v = perm(n, r)
    lines = "<br>".join(rf"{p}: \({n - i}\) ways" for i, p in enumerate(places))
    trad = steps(
        ("Fill the places one by one.", lines + (rf"<br>(a {thing} used once can not be used again)" if r > 1 else "")),
        ("Multiply the ways.", D(f"{falling_tex(n, r)} = {v}")))
    expr = nP(n, r)
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) different {things}, \(r = {r}\) places to fill."),
        ("Apply the specified rule.", D(rf"{nP('n', 'r')} = \frac{{n!}}{{(n-r)!}}")),
        ("Substitute the values.", D(rf"{expr} = \frac{{{n}!}}{{{n - r}!}} = {falling_tex(n, r)} = {v}")))
    rb = [rf"\(n = {n}\), \(r = {r}\).", rf"\({nP('n', 'r')} = \frac{{n!}}{{(n-r)!}}\).", rf"\({expr} = {falling_tex(n, r)} = {v}\)."]
    sc = D(rf"{expr} = {falling_tex(n, r)} = {v}")
    return result(num(v), T1, trad, rule, I(v), rb, sc)


# ---------------------------------------------------------------- Rule 2: numbers from digits, no repetition
T2 = (r"To form numbers with given digits when repetition is not allowed: decide how many digits the number has, fill the places "
      r"that carry a restriction first (the first digit can not be \(0\); the last digit decides 'even'; the first digits decide "
      r"'greater than'), then fill the remaining \(r\) places with the remaining \(n\) digits in \({}^{n}P_{r}\) ways. "
      r"Multiply within a case and add the cases:<br>\[ \text{Ways} = (\text{ways for the restricted places})\times {}^{n}P_{r} \]")


def boxes(heads, cells):
    return ('<table border="1" cellpadding="4"><tr>' + "".join(f"<th>{h}</th>" for h in heads) + "</tr><tr>"
            + "".join(f"<td>{c}</td>" for c in cells) + "</tr></table>")


def r2_cases(cases, total_note=""):
    """cases: list of (title, restricted_ways, n_left, r_left, heads, cells); restricted_ways may be a list of the
    restricted places' factors ([2, 4]: units 2 ways, thousands 4 ways). Returns (total, trad, rule, rb, sc)."""
    cases = [(t, w if isinstance(w, list) else [w], n, r, h, c) for t, w, n, r, h, c in cases]
    wv = lambda w: prod(w)
    total = sum(wv(w) * perm(n, r) for _, w, n, r, _, _ in cases)
    trad_items, rule_items, rb, sc_parts = [], [], [], []
    for title, w, n, r, heads, cells in cases:
        v = wv(w) * perm(n, r)
        wt = times(*w)
        trad_items.append((title, boxes(heads, cells) + D(f"{times(wt, falling_tex(n, r)) if r else wt} = {v}")))
        rule_items.append(rf"<b>{title}</b> \({times(wt, nP(n, r))} = {times(wt, perm(n, r))} = {v}\)")
        rb.append(rf"{title.rstrip('.')}: \({times(wt, nP(n, r))} = {v}\).")
        sc_parts.append(times(wt, nP(n, r)))
    cases = [(t, wv(w), n, r, h, c) for t, w, n, r, h, c in cases]
    if len(cases) > 1:
        trad_items.append(("Add the cases.", D(" + ".join(str(w * perm(n, r)) for _, w, n, r, _, _ in cases) + f" = {total}")))
        rb.append(rf"Total \(= {' + '.join(str(w * perm(n, r)) for _, w, n, r, _, _ in cases)} = {total}\).")
    rule = steps(
        ("Identify the restricted places and the digits left.", "Fill the restricted places first; the other places take the remaining digits." + total_note),
        ("Apply the specified rule.", r"Ways \(=\) (ways for the restricted places) \(\times {}^{n}P_{r}\) in each case."),
        ("Substitute the values.", "<br>".join(rule_items) + (D(" + ".join(str(w * perm(n, r)) for _, w, n, r, _, _ in cases) + f" = {total}") if len(cases) > 1 else "")))
    sc = D(" + ".join(sc_parts) + f" = {total}")
    return total, steps(*trad_items), rule, rb, sc


def r2_result(cases, note=""):
    total, trad, rule, rb, sc = r2_cases(cases, note)
    return result(num(total), T2, trad, rule, I(total), rb, sc)


def r2_product(a, b, what_a, what_b, verb):
    """Multiplication principle: a ways for the first job, b ways for the second."""
    v = a * b
    trad = steps(
        ("List the choices in order.", rf"For each of the \({a}\) {what_a} there are \({b}\) {what_b}, so the possibilities can be listed as \({a}\) rows of \({b}\) each."),
        ("Count them.", D(f"{b} + {b} + \\cdots \\text{{ ({a} times)}} = {v}")))
    rule = steps(
        ("Identify the two places to fill.", rf"Place 1 ({what_a}): \({a}\) ways; place 2 ({what_b}): \({b}\) ways."),
        ("Apply the specified rule.", r"Fill the places one by one and multiply the ways (here no digit is reused, each place has its own list)."),
        ("Substitute the values.", D(f"{times(a, b)} = {v}")))
    rb = [rf"{what_a.capitalize()}: \({a}\) ways, {what_b}: \({b}\) ways.", f"{verb}: multiply the ways.", rf"\({times(a, b)} = {v}\)."]
    return result(num(v), T2, trad, rule, I(v), rb, D(f"{times(a, b)} = {v}"))


def r2_sum(digits):
    k = len(digits)
    each = factorial(k - 1)
    s = sum(digits)
    ones = int("1" * k)
    v = each * s * ones
    trad = steps(
        ("Count how often each digit stands in a place.",
         rf"There are \({k}! = {factorial(k)}\) numbers. Fix a digit in the units place: the other \({k - 1}\) digits fill the other places in "
         rf"\({k - 1}! = {each}\) ways. So every digit stands in the units place \({each}\) times, and the same holds for the tens, hundreds and thousands places."),
        ("Add one place.", D(rf"\text{{Sum of the units digits}} = {each}\times ({' + '.join(map(str, digits))}) = {each}\times {s} = {each * s}")),
        ("Add all the places.", D(rf"{each * s}\times (1000 + 100 + 10 + 1) = {each * s}\times {ones} = {v}")))
    rule = steps(
        ("Identify the values.", rf"\({k}\) digits \({', '.join(map(str, digits))}\), each used once; sum of the digits \(= {s}\)."),
        ("Apply the specified rule.", rf"With one digit fixed in a place, the remaining \({k - 1}\) places are filled in \({nP(k - 1, k - 1)} = {k - 1}!\) ways, "
                                      r"so each digit appears that many times in every place:"
                                      + D(rf"\text{{Sum}} = {nP(k - 1, k - 1)}\times (\text{{sum of digits}})\times {ones}")),
        ("Substitute the values.", D(rf"{nP(k - 1, k - 1)}\times {s}\times {ones} = {each}\times {s}\times {ones} = {v}")))
    rb = [rf"Digits \({', '.join(map(str, digits))}\), sum \(= {s}\).", rf"Each digit appears \({nP(k - 1, k - 1)} = {each}\) times in every place.",
          rf"Sum \(= {each}\times {s}\times {ones} = {v}\)."]
    return result(num(v), T2, trad, rule, I(v), rb, D(rf"{each}\times {s}\times {ones} = {v}"))


# ---------------------------------------------------------------- Rule 3: repetition allowed
T3 = (r"The number of permutations of \(n\) different things taken \(r\) at a time, when each thing may be repeated any number "
      r"of times, is<br>\[ n\times n\times n\cdots (r \text{ times}) = n^{r} \]")


def r3(n, r, who, choice, minus=0, minus_why=""):
    """who: the r things that can not repeat (each picks one of the n); choice: the n options."""
    v = n ** r - minus
    lines = rf"Each of the \({r}\) {who} can independently take any one of the \({n}\) {choice}, because the same one may be used again."
    trad = steps(
        ("Start with the things that can not repeat.", lines),
        ("Multiply the ways.", D(f"{times(*([n] * r))} = {n ** r}")),
        *((("Remove the cases that do not count.", minus_why + D(f"{n ** r} - {minus} = {v}")),) if minus else ()))
    expr = f"{n}^{{{r}}}" + (f" - {minus}" if minus else "")
    rule = steps(
        ("Identify the values.", rf"\(n = {n}\) {choice} (each may be repeated), \(r = {r}\) {who}."),
        ("Apply the specified rule.", D(r"n^{r}") + (minus_why if minus else "")),
        ("Substitute the values.", D(f"{expr} = {v}")))
    rb = [rf"\(n = {n}\), \(r = {r}\).", r"With repetition the number is \(n^{r}\)" + (rf", minus the \({minus}\) case{'s' if minus > 1 else ''} that do not count." if minus else "."),
          rf"\({expr} = {v}\)."]
    return result(num(v), T3, trad, rule, I(v), rb, D(f"{expr} = {v}"))


def r3_numbers(digits, lo, hi):
    """Numbers greater than lo and not greater than hi (both 4-digit, hi a round thousand) with digits repeated freely."""
    n = len(digits)
    firsts = [d for d in digits if lo // 1000 <= d < hi // 1000]
    base = len(firsts) * n ** 3
    v = base - 1 + 1                                  # lo itself is excluded, hi itself is included
    trad = steps(
        ("Count the 4-digit numbers from the first digit.",
         rf"A number from \({lo}\) to \({hi - 1}\) has its thousands digit in \(\{{{', '.join(map(str, firsts))}\}}\): \({len(firsts)}\) ways; "
         rf"each of the other three places can take any of the \({n}\) digits: \({n}\times {n}\times {n}\) ways."
         + D(rf"{len(firsts)}\times {n}\times {n}\times {n} = {base}")),
        ("Adjust the ends.", rf"\({lo}\) itself is counted but is not greater than \({lo}\): subtract \(1\). \({hi}\) is not counted but is allowed: add \(1\)."
         + D(f"{base} - 1 + 1 = {v}")))
    rule = steps(
        ("Identify the values.", rf"First digit: \({len(firsts)}\) ways; the other \(r = 3\) places from \(n = {n}\) digits with repetition."),
        ("Apply the specified rule.", D(r"\text{Ways} = (\text{first-digit ways})\times n^{r}")),
        ("Substitute the values.", D(rf"{len(firsts)}\times {n}^{{3}} - 1 + 1 = {base} - 1 + 1 = {v}")))
    rb = [rf"First digit \({len(firsts)}\) ways, then \(n = {n}\), \(r = 3\).", r"Ways \(= (\text{first-digit ways})\times n^{r}\), then fix the two ends.",
          rf"\({len(firsts)}\times {n}^{{3}} - 1 + 1 = {v}\)."]
    return result(num(v), T3, trad, rule, I(v), rb, D(rf"{len(firsts)}\times {n}^{{3}} - 1 + 1 = {v}"))


# ---------------------------------------------------------------- Rule 4: no two of group B together
T4 = (r"If there are two groups A and B of \(m\) and \(n\) things respectively (\(n \le m+1\)), the number of ways in which they "
      r"can be arranged in a row so that no two of group B are together is<br>\[ {}^{m+1}P_{n}\times m! \]")


def r4(m, n, A, B, sym):
    v = perm(m + 1, n) * factorial(m)
    expr = rf"\frac{{{m + 1}!\times {m}!}}{{{m + 1 - n}!}}" if m + 1 - n > 1 else rf"{m + 1}!\times {m}!"
    gaps = r"\ ".join(["\\times"] + [rf"\text{{{sym}}}\ \times"] * m)
    trad = steps(
        (f"Seat the {A} first.", rf"There is no restriction on the \({m}\) {A}: they sit in a row in \({m}!\) ways."),
        ("Mark the gaps.", rf"Between them and at both ends there are \({m + 1}\) gaps:" + D(gaps)
         + rf"If every {B[:-1] if B.endswith('s') else B} sits in a different gap, no two {B} are together."),
        (f"Seat the {B} in the gaps.", rf"The 1st of the \({n}\) {B} has \({m + 1}\) gaps to choose, the 2nd \({m}\), and so on:"
         + D(rf"{falling_tex(m + 1, n)} = \frac{{{m + 1}!}}{{{m + 1 - n}!}}")),
        ("Multiply.", D(rf"{m}!\times \frac{{{m + 1}!}}{{{m + 1 - n}!}} = {expr} = {v}")))
    rule = steps(
        ("Identify the values.", rf"Group A ({A}): \(m = {m}\); group B ({B}): \(n = {n}\) (\({n} \le {m + 1}\))."),
        ("Apply the specified rule.", D(r"{}^{m+1}P_{n}\times m!")),
        ("Substitute the values.", D(rf"{nP(m + 1, n)}\times {m}! = \frac{{{m + 1}!}}{{{m + 1 - n}!}}\times {m}! = {v}")))
    rb = [rf"\(m = {m}\) {A}, \(n = {n}\) {B}.", r"Ways \(= {}^{m+1}P_{n}\times m!\).", rf"\({nP(m + 1, n)}\times {m}! = {expr} = {v}\)."]
    return result(num(v), T4, trad, rule, fin(expr, v), rb, D(rf"{nP(m + 1, n)}\times {m}! = {expr}"))


# ---------------------------------------------------------------- Rule 5: best and worst never together
T5 = (r"The number of ways in which \(n\) examination papers can be arranged so that the best and the worst papers never come "
      r"together (or \(n\) books so that two particular books are never together) is<br>\[ (n-2)\times (n-1)! \]")


def r5(n, things, pair):
    v = (n - 2) * factorial(n - 1)
    expr = rf"{n - 2}\times {n - 1}!"
    trad = steps(
        ("Count all the arrangements.", rf"With no restriction the \({n}\) {things} can be arranged in \({n}!\) ways."),
        (f"Count the arrangements with the {pair} together.", rf"Tie the {pair} into one unit: \({n - 1}\) units, arranged in \({n - 1}!\) ways, "
                                                            rf"and the two can change places in \(2!\) ways: \(2\times {n - 1}!\) arrangements."),
        ("Subtract.", D(rf"{n}! - 2\times {n - 1}! = {n - 1}!\,({n} - 2) = {expr}")))
    rule = steps(
        ("Identify the value.", rf"\(n = {n}\) {things}."),
        ("Apply the specified rule.", D(r"(n-2)\times (n-1)!")),
        ("Substitute the value.", D(rf"({n} - 2)\times ({n} - 1)! = {expr}")))
    rb = [rf"\(n = {n}\).", r"Ways \(= (n-2)\times (n-1)!\).", rf"\(({n}-2)\times ({n}-1)! = {expr}\)."]
    return result(num(v), T5, trad, rule, I(expr), rb, D(rf"({n}-2)\times ({n}-1)! = {expr}"))


# ---------------------------------------------------------------- Rule 6: all of one group not together
T6 = (r"There are \(m\) boys and \(n\) girls. The number of ways in which they can be seated in a row so that all the girls do "
      r"not sit together is<br>\[ (m+n)! - (m+1)!\times n! \]"
      r"(If all the boys must not sit together, the roles change: \((m+n)! - (n+1)!\times m!\).)")


def r6(g, o, G, O, as_multiple=None):
    """g people of group G must not ALL sit together; o others (group O)."""
    total = factorial(g + o)
    together = factorial(o + 1) * factorial(g)
    v = total - together
    if as_multiple:                                   # answer written as k x a! like the book's options
        k = v // factorial(as_multiple)
        expr = rf"{k}\times {as_multiple}!"
        tail = rf" = {as_multiple}!\,\left(\frac{{{g + o}!}}{{{as_multiple}!}} - \frac{{{o + 1}!\times {g}!}}{{{as_multiple}!}}\right) = {expr}"
    else:
        expr, tail = str(v), ""
    trad = steps(
        ("Count all the arrangements.", rf"\({g}\) {G} and \({o}\) {O} are \({g + o}\) people: \({g + o}!\) ways in a row."),
        (f"Count the arrangements with all the {G} together.",
         rf"Tie the \({g}\) {G} into one unit: \({o} + 1 = {o + 1}\) units in \({o + 1}!\) ways, and the {G} change places inside the unit in \({g}!\) ways:"
         + D(rf"{o + 1}!\times {g}! = {together}")),
        ("Subtract.", D(rf"{g + o}! - {o + 1}!\times {g}! = {total} - {together} = {v}" + tail)))
    rule = steps(
        ("Identify the values.", rf"The group that must not be all together has \({g}\) ({G}); the others: \({o}\) ({O})."),
        ("Apply the specified rule.", D(r"(m+n)! - (m+1)!\times n!") + rf"with \(n = {g}\) for the {G} and \(m = {o}\) for the {O}."),
        ("Substitute the values.", D(rf"({o}+{g})! - ({o}+1)!\times {g}! = {total} - {together} = {v}")))
    rb = [rf"\(n = {g}\) {G} (not all together), \(m = {o}\) {O}.", r"Ways \(= (m+n)! - (m+1)!\times n!\).",
          rf"\({g + o}! - {o + 1}!\times {g}! = {v}\)" + (rf" \(= {expr}\)." if as_multiple else ".")]
    return result(num(v), T6, trad, rule, fin(expr, v) if as_multiple else I(v), rb, D(rf"{g + o}! - {o + 1}!\times {g}! = {expr}"))


# ---------------------------------------------------------------- Rule 7: m boys and m girls alternate in a row
T7 = r"The number of ways in which \(m\) boys and \(m\) girls can be seated in a row so that boys and girls are alternate is<br>\[ 2\,(m!\times m!) \]"


def r7(m):
    v = 2 * factorial(m) ** 2
    pat1 = " ".join(["B G"] * m)
    pat2 = " ".join(["G B"] * m)
    expr = rf"2({m}!\times {m}!)"
    trad = steps(
        ("List the possible patterns.", rf"With \({m}\) boys and \({m}\) girls in \({2 * m}\) seats the row is either {pat1} or {pat2}."),
        ("Count each pattern.", rf"In each pattern the boys fill their \({m}\) seats in \({m}!\) ways and the girls fill theirs in \({m}!\) ways:"
         + D(rf"{m}!\times {m}! = {factorial(m)}\times {factorial(m)} = {factorial(m) ** 2}")),
        ("Add the two patterns.", D(f"{factorial(m) ** 2} + {factorial(m) ** 2} = {v}")))
    rule = steps(
        ("Identify the value.", rf"\(m = {m}\)."),
        ("Apply the specified rule.", D(r"2\,(m!\times m!)")),
        ("Substitute the value.", D(rf"2\,({m}!\times {m}!) = 2\times {factorial(m) ** 2} = {v}")))
    rb = [rf"\(m = {m}\).", r"Ways \(= 2(m!\times m!)\).", rf"\(2({m}!\times {m}!) = {v}\)."]
    return result(num(v), T7, trad, rule, fin(expr, v), rb, D(rf"2({m}!\times {m}!) = {v}"))


# ---------------------------------------------------------------- rule cards
CARDS = {
    1: card(1, "Permutations: Direct Use of nPr",
            r"The number of arrangements of \(n\) different things taken \(r\) at a time (\(r \le n\)) is \({}^{n}P_{r}\). "
            r"It is the product of \(r\) consecutive whole numbers that starts at \(n\) and goes down.",
            r"\[ {}^{n}P_{r} = \frac{n!}{(n-r)!} = n(n-1)(n-2)\cdots(n-r+1) \]",
            [("Number of different things", "n"), ("Places to fill", "r"), ("Arrangements", r"{}^{n}P_{r}"), ("All the things", r"{}^{n}P_{n} = n!")],
            r"The 1st place can take any of the \(n\) things, the 2nd any of the \(n-1\) left, and so on for \(r\) places; multiplying the choices gives the count.",
            r"'Arrange', 'words from the letters of', 'in how many ways can \(r\) of them sit', or an equation such as \({}^{n}P_{4} = 360\). "
            r"To find \(n\) or \(r\), write the given number as a product of consecutive integers (factorise it and try the largest prime factor first).",
            r"If \({}^{n}P_{4} = 360\): \(360 = 6\times 5\times 4\times 3\), so \(n = 6\).",
            r"Writing \(\frac{n!}{r!}\) instead of \(\frac{n!}{(n-r)!}\) (they agree only when \(r = n - r\)): \({}^{10}P_{3} = \frac{10!}{7!} = 720\), "
            r"not \(\frac{10!}{3!}\). Also \(\frac{n!}{r!} \ne \left(\frac{n}{r}\right)!\): \(\frac{8!}{4!} = 1680\) but \(2! = 2\)."),
    2: card(2, "Forming Numbers with Digits (No Repetition)",
            r"To count numbers formed from given digits when no digit is repeated: fix the number of digits, fill the restricted places "
            r"first, then fill the remaining \(r\) places from the remaining \(n\) digits in \({}^{n}P_{r}\) ways; add the cases.",
            r"\[ \text{Ways} = (\text{ways for the restricted places})\times {}^{n}P_{r} \]",
            [("Digits still unused", "n"), ("Places still empty", "r"), ("First digit", r"\ne 0"), ("Even number", r"\text{units digit } 0, 2, 4, 6, 8")],
            r"Every number is a row of places. The multiplication principle says the choices for the places multiply; a restriction only "
            r"changes how many choices one place has, so it is filled first.",
            r"'How many numbers between ... and ...', 'even numbers of four digits', 'greater than 2300', 'no digit repeated', "
            r"also any task done in stages (a chair and a table, P to Q and then Q to R): multiply the ways of the stages.",
            r"Numbers between 400 and 1000 from 2, 3, 4, 5, 6, 0: hundreds digit 4, 5 or 6 (3 ways), then \({}^{5}P_{2} = 20\): \(3\times 20 = 60\).",
            r"Forgetting that \(0\) can not be the first digit, or filling the unrestricted places first so that the restricted place "
            r"loses a digit you can no longer count. Split into cases when one restriction depends on another (for example \(0\) in the units place)."),
    3: card(3, "Permutations with Repetition",
            r"The number of permutations of \(n\) different things taken \(r\) at a time, when each thing may be used any number of "
            r"times, is \(n^{r}\).",
            r"\[ n\times n\times n\cdots (r\text{ times}) = n^{r} \]",
            [("Choices for each place", "n"), ("Number of places", "r"), ("Arrangements", "n^{r}")],
            r"When repetition is allowed, using a thing once does not remove it, so every one of the \(r\) places still has all \(n\) choices.",
            r"'Each boy is eligible for any of the prizes', 'servants carry the cards', 'rings on fingers', 'each arm in any position', "
            r"'repetition allowed'. Start with what can NOT repeat (prizes, friends, rings, arms): each of them picks one of the things that can.",
            r"6 friends, 3 servants: each friend's card goes through any of the 3 servants, so \(3^{6} = 729\) ways.",
            r"Raising the wrong number to the power: 3 prizes to 7 boys is \(7^{3}\), not \(3^{7}\) (a prize can not be split between two boys, "
            r"but a boy can win two prizes). Remember to remove cases that do not count, such as the all-rest signal or the one correct code."),
    4: card(4, "No Two of One Group Together",
            r"If there are two groups A and B of \(m\) and \(n\) things (\(n \le m+1\)), the number of ways to arrange all of them in a row "
            r"so that no two things of group B are together is \({}^{m+1}P_{n}\times m!\).",
            r"\[ {}^{m+1}P_{n}\times m! = \frac{(m+1)!}{(m+1-n)!}\times m! \]",
            [("Group A (no restriction)", "m"), ("Group B (no two together)", "n"), ("Gaps around group A", "m+1"), ("Ways", r"{}^{m+1}P_{n}\times m!")],
            r"Seat group A first; the \(m+1\) gaps between them (including both ends) keep any two B's apart if each B takes its own gap.",
            r"'No two of the girls sit together', 'no two vowels together', 'no two of the three girls are consecutive'.",
            r"7 I.A. and 5 I.Sc. students: \({}^{8}P_{5}\times 7! = \frac{8!}{3!}\times 7!\).",
            r"Confusing 'no two together' with 'not all together' (Rule 6), or using \(m\) gaps instead of \(m+1\)."),
    5: card(5, "Two Particular Things Never Together",
            r"The number of ways in which \(n\) examination papers can be arranged so that the best and the worst papers never come "
            r"together is \((n-2)\times (n-1)!\). The same holds for any two particular things (two books, two people) in a row.",
            r"\[ (n-2)\times (n-1)! \]",
            [("Number of things", "n"), ("All arrangements", "n!"), ("The two together", r"2\times (n-1)!"), ("Never together", r"(n-2)\times (n-1)!")],
            r"Subtract the arrangements in which the two are together (tie them into one unit, which can be flipped) from all arrangements: "
            r"\(n! - 2(n-1)! = (n-1)!(n-2)\).",
            r"'The best and the worst papers never come together', 'two particular books are never together', 'the oldest and the newest books'.",
            r"10 papers: \((10-2)\times 9! = 8\times 9!\).",
            r"Forgetting the factor \(2\) for the two orders inside the tied unit, which gives \((n-1)!\,(n-1)\) instead."),
    6: card(6, "All of One Group Not Together",
            r"There are \(m\) boys and \(n\) girls. The number of ways to seat them in a row so that all the girls do NOT sit together "
            r"is \((m+n)! - (m+1)!\times n!\). For 'all the boys not together' swap the roles: \((m+n)! - (n+1)!\times m!\).",
            r"\[ (m+n)! - (m+1)!\times n! \]",
            [("Total people", "m+n"), ("All arrangements", "(m+n)!"), ("All girls together", r"(m+1)!\times n!"), ("Not all together", r"(m+n)! - (m+1)!\times n!")],
            r"'Not all together' is everything except the arrangements where the whole group forms one block; the block plus the \(m\) "
            r"others give \(m+1\) units, and the group can be ordered inside the block in \(n!\) ways.",
            r"'All the three girls do not sit together', 'all the boys do not sit together'. Check WHICH group must not be together.",
            r"5 boys, 3 girls: \(8! - 6!\times 3! = 40320 - 4320 = 36000\).",
            r"Mixing it up with 'no two together' (Rule 4), or putting the wrong group in the factorial: for 'all the boys not together' "
            r"the block is the boys, so it is \((n+1)!\times m!\) that is subtracted."),
    7: card(7, "m Boys and m Girls Alternate in a Row",
            r"The number of ways in which \(m\) boys and \(m\) girls can be seated in a row so that boys and girls are alternate is "
            r"\(2\,(m!\times m!)\).",
            r"\[ 2\,(m!\times m!) \]",
            [("Boys", "m"), ("Girls", "m"), ("Patterns", r"BGBG\cdots \text{ or } GBGB\cdots"), ("Ways", r"2(m!\times m!)")],
            r"With equal numbers the row can start with a boy or with a girl (2 patterns); in each pattern the boys and the girls fill "
            r"their own seats in \(m!\) ways each.",
            r"'Boys and girls are alternate' with EQUAL numbers of each in a row. (Unequal numbers: Rule 8; round a circle: Rule 9.)",
            r"4 boys and 4 girls: \(2(4!\times 4!) = 2\times 576 = 1152\).",
            r"Forgetting the factor \(2\) (only one starting pattern), or using it when the numbers are unequal - then only one pattern is possible."),
}

# ---------------------------------------------------------------- old rows (id -> generator, cleaned question, options or None)
OLD = {
    1: {845: (lambda: r1_find_n(4, 360), r"If \({}^{n}P_{4} = 360\), find \(n\).",
              {"a": r"\(n = 16\)", "b": r"\(n = 6\)", "c": r"\(n = 4\)", "d": r"\(n = 8\)"}),
        885: (lambda: r1_value(10, 3, ["1st letter", "2nd letter", "3rd letter"], "letters", "letter"), None, None),
        891: (lambda: r1_value(5, 5, ["1st place", "2nd place", "3rd place", "4th place", "5th place"], "letters", "letter"), None, None),
        893: (lambda: r1_value(5, 5, ["1st place", "2nd place", "3rd place", "4th place", "5th place"], "letters", "letter"), None, None),
        894: (lambda: r1_value(100, 2, ["1st place", "2nd place"], "things", "thing"), r"What is the value of \({}^{100}P_{2}\)?",
              {"c": "9900"}),
        899: (lambda: r1_value(25, 2, ["Going from P to Q (any bus)", "Returning from Q to P (any bus except the one used)"], "buses", "bus"), None, None),
        903: (lambda: r1_value(5, 5, ["1st man", "2nd man", "3rd man", "4th man", "5th man"], "taps", "tap"),
              "In how many ways can 5 men draw water from 5 taps if no tap can be used more than once?", {"a": "25"})},
    2: {846: (lambda: r2_result([("Fill the four places.", 1, 5, 4, ["Thousands", "Hundreds", "Tens", "Units"], ["5 ways", "4 ways", "3 ways", "2 ways"])]),
              "How many numbers of four digits can be formed with the digits 1, 2, 3, 4 and 5 if repetition of digits is not allowed?", None),
        897: (lambda: r2_result([("The first two places are fixed as 3 and 5.", 1, 8, 4, ["1st", "2nd", "3rd", "4th", "5th", "6th"],
                                  ["3 (fixed)", "5 (fixed)", "8 ways", "7 ways", "6 ways", "5 ways"])],
                                r" Here the first two digits are fixed (1 way); the other 4 places take 4 of the remaining 8 digits."),
              "How many 6-digit telephone numbers can be formed if each number starts with 35 and no digit appears more than once?", None),
        898: (lambda: r2_product(10, 8, "patterns of chairs", "patterns of tables", "Choosing a chair and then a table"),
              "An event manager has ten patterns of chairs and eight patterns of tables. In how many ways can he make a pair of a table and a chair?", None),
        904: (lambda: r2_product(3, 4, "roads from P to Q", "roads from Q to R", "Travelling P to Q and then Q to R"),
              "There are three places P, Q and R such that 3 roads connect P and Q and 4 roads connect Q and R. In how many ways can one travel from P to R through Q?", None),
        914: (lambda: r2_sum([2, 3, 4, 5]), None, None)},
    3: {847: (lambda: r3(3, 6, "friends", "servants"),
              "A gentleman has 6 friends to invite. In how many ways can he send invitation cards to them if he has three servants to carry the cards?",
              {"c": "319"}),
        887: (lambda: r3(2, 3, "tosses", "outcomes (head or tail)"), None, None),
        902: (lambda: r3(3, 6, "rings", "fingers"), "Find the number of ways in which 6 rings of different types can be worn on 3 fingers.", None)},
    4: {848: (lambda: r4(7, 5, "I.A. students", "I.Sc. students", "A"),
              "In how many ways can 7 I.A. and 5 I.Sc. students be seated in a row so that no two of the I.Sc. students sit together?",
              {"a": r"\(\frac{8!}{3!}\times 7!\)", "b": r"\(\frac{8!}{7!}\times 3!\)", "c": r"\(\frac{8!}{5!}\times 7!\)", "d": r"\(8!\times 7!\)"})},
    5: {849: (lambda: r5(10, "papers", "best and the worst papers"),
              "In how many ways can 10 examination papers be arranged so that the best and the worst papers never come together?",
              {"a": r"\(7\times 3!\)", "b": r"\(9\times 8!\)", "c": r"\(6\times 12!\)", "d": r"\(8\times 9!\)"})},
    6: {850: (lambda: r6(3, 5, "girls", "boys"),
              "There are 5 boys and 3 girls. In how many ways can they be seated in a row so that all the three girls do not sit together?",
              {"a": "33000", "d": "63000"})},
    7: {851: (lambda: r7(4), "In how many ways can 4 boys and 4 girls be seated in a row so that boys and girls are alternate?", None)},
}

FR = r"\frac"
NEW = {
    1: [("r1_e1", r"If \({}^{n}P_{3} = 4896\), find \(n\).", lambda: r1_find_n(3, 4896),
         [r"\(n = 16\)", r"\(n = 17\)", r"\(n = 18\)", r"\(n = 19\)"], 3),
        ("r1_e2", r"If \({}^{12}P_{r} = 1320\), find \(r\).", lambda: r1_find_r(12, 1320),
         [r"\(r = 3\)", r"\(r = 2\)", r"\(r = 4\)", r"\(r = 10\)"], 1)],
    2: [("r2_e1", "How many numbers between 600 and 1000 can be made with the digits 0, 1, 4, 6, 7, 8 and 9 if no digit is repeated?",
         lambda: r2_result([("Hundreds digit 6, 7, 8 or 9.", 4, 6, 2, ["Hundreds", "Tens", "Units"], ["6, 7, 8 or 9: 4 ways", "6 ways", "5 ways"])]),
         ["150", "120", "90", "180"], 2),
        ("r2_e2", "Find how many numbers between 400 and 4000 can be formed with the digits 0, 1, 2, 3, 4, 5 and 6, no digit being repeated in any number.",
         lambda: r2_result([("Case I: 3-digit numbers (hundreds digit 4, 5 or 6).", 3, 6, 2, ["Hundreds", "Tens", "Units"], ["4, 5 or 6: 3 ways", "6 ways", "5 ways"]),
                            ("Case II: 4-digit numbers (thousands digit 1, 2 or 3).", 3, 6, 3, ["Thousands", "Hundreds", "Tens", "Units"],
                             ["1, 2 or 3: 3 ways", "6 ways", "5 ways", "4 ways"])]),
         ["360", "540", "450", "390"], 3),
        ("r2_e3", "How many even numbers of four digits can be formed with the digits 0, 1, 2, 3, 4 and 5 if no digit is used more than once?",
         lambda: r2_result([("Case I: 0 in the units place.", 1, 5, 3, ["Thousands", "Hundreds", "Tens", "Units"], ["5 ways", "4 ways", "3 ways", "0: 1 way"]),
                            ("Case II: 2 or 4 in the units place (thousands digit not 0).", [2, 4], 4, 2, ["Thousands", "Hundreds", "Tens", "Units"],
                             ["4 ways (not 0)", "4 ways", "3 ways", "2 or 4: 2 ways"])]),
         ["180", "120", "144", "156"], 4),
        ("r2_e4", "How many numbers of four digits greater than 3400 can be formed with the digits 0, 1, 2, 3, 4, 5 and 6, no digit being repeated?",
         lambda: r2_result([("Case I: thousands digit 3 (hundreds digit 4, 5 or 6).", [1, 3], 5, 2, ["Thousands", "Hundreds", "Tens", "Units"],
                             ["3: 1 way", "4, 5 or 6: 3 ways", "5 ways", "4 ways"]),
                            ("Case II: thousands digit 4, 5 or 6.", 3, 6, 3, ["Thousands", "Hundreds", "Tens", "Units"], ["4, 5 or 6: 3 ways", "6 ways", "5 ways", "4 ways"])]),
         ["420", "480", "360", "400"], 1),
        ("r2_e5", "How many positive numbers can be formed by using any number of the digits 0, 1, 2, 3, 4 and 5, no digit being repeated in any number?",
         lambda: r2_result([(f"{k}-digit numbers.", 5, 5, k - 1, [f"Place {i}" for i in range(1, k + 1)],
                             ["5 ways (not 0)"] + [f"{5 - i} ways" for i in range(k - 1)]) for k in range(1, 7)]),
         ["1500", "1630", "1625", "1720"], 2)],
    3: [("r3_e1", "In how many ways can 4 prizes be given away to 6 boys when each boy is eligible for any of the prizes?",
         lambda: r3(6, 4, "prizes", "boys"), ["360", "4096", "1296", "24"], 3),
        ("r3_e2", "A signal post has 4 arms and each arm can be put in any of 5 distinct positions, including the position of rest. "
                  "What is the total number of signals that can be made?",
         lambda: r3(5, 4, "arms", "positions", 1, "When all the arms are in the rest position no signal is made, so that \\(1\\) case is removed."),
         ["625", "1023", "1024", "624"], 4),
        ("r3_e3", "A letter lock has 4 rings, each marked with 6 different letters. In how many ways is it possible to make an unsuccessful attempt to open the lock?",
         lambda: r3(6, 4, "rings", "letters", 1, "Only one of these settings opens the lock, so \\(1\\) is subtracted."),
         ["1295", "1296", "4095", "360"], 1),
        ("r3_e4", "How many numbers greater than 2000 but not greater than 5000 can be formed with the digits 0, 1, 2, 3, 4 and 5 if repetition of digits is allowed?",
         lambda: r3_numbers([0, 1, 2, 3, 4, 5], 2000, 5000), ["647", "648", "864", "540"], 2)],
    4: [("r4_x2", "In a class of 11 students there are 4 girls. In how many different ways can they be arranged in a row so that no two of the four girls are consecutive?",
         lambda: r4(7, 4, "boys", "girls", "B"),
         [rf"\({FR}{{8!\times 7!}}{{3!}}\)", rf"\({FR}{{7!\times 7!}}{{4!}}\)", rf"\({FR}{{8!\times 7!}}{{4!}}\)", rf"\({FR}{{8!\times 4!}}{{3!}}\)"], 3),
        ("r4_e1", "In how many ways can 9 I.A. and 5 I.Sc. students be seated in a row so that no two of the I.Sc. students sit together?",
         lambda: r4(9, 5, "I.A. students", "I.Sc. students", "A"),
         [rf"\({FR}{{10!\times 9!}}{{5!}}\)", rf"\({FR}{{10!\times 9!}}{{4!}}\)", rf"\({FR}{{9!\times 9!}}{{5!}}\)", r"\(10!\times 5!\)"], 1),
        ("r4_e2", "In how many ways can 5 I.A. and 3 I.Sc. students be seated in a row so that no two of the I.Sc. students sit together?",
         lambda: r4(5, 3, "I.A. students", "I.Sc. students", "A"),
         [rf"\({FR}{{6!\times 5!}}{{2!}}\)", rf"\({FR}{{5!\times 5!}}{{3!}}\)", rf"\({FR}{{6!\times 3!}}{{2!}}\)", rf"\({FR}{{6!\times 5!}}{{3!}}\)"], 4),
        ("r4_e3", "In a class of 13 students there are 5 girls. In how many different ways can they be arranged in a row so that no two of the five girls are consecutive?",
         lambda: r4(8, 5, "boys", "girls", "B"),
         [rf"\({FR}{{9!\times 8!}}{{5!}}\)", rf"\({FR}{{9!\times 8!}}{{4!}}\)", rf"\({FR}{{8!\times 8!}}{{3!}}\)", rf"\({FR}{{9!\times 5!}}{{4!}}\)"], 2),
        ("r4_e4", "In a class of 14 students there are 4 girls. In how many different ways can they be arranged in a row so that no two of the four girls are consecutive?",
         lambda: r4(10, 4, "boys", "girls", "B"),
         [rf"\({FR}{{11!\times 10!}}{{6!}}\)", rf"\({FR}{{10!\times 10!}}{{7!}}\)", rf"\({FR}{{11!\times 10!}}{{7!}}\)", rf"\({FR}{{11!\times 4!}}{{7!}}\)"], 3)],
    5: [("r5_e1", "In how many ways can 11 examination papers be arranged so that the best and the worst papers never come together?",
         lambda: r5(11, "papers", "best and the worst papers"),
         [r"\(10\times 9!\)", r"\(9\times 10!\)", r"\(11\times 9!\)", r"\(9\times 11!\)"], 2),
        ("r5_e2", "In how many ways can 13 examination papers be arranged so that the best and the worst papers never come together?",
         lambda: r5(13, "papers", "best and the worst papers"),
         [r"\(12\times 11!\)", r"\(11\times 13!\)", r"\(11\times 12!\)", r"\(13\times 11!\)"], 3),
        ("r5_e3", "Find the number of ways in which 17 books can be arranged on a shelf so that the oldest and the newest books are never together.",
         lambda: r5(17, "books", "oldest and the newest books"),
         [r"\(15\times 16!\)", r"\(16\times 15!\)", r"\(15\times 17!\)", r"\(17\times 15!\)"], 1)],
    6: [("r6_e1", "There are 4 boys and 2 girls. In how many ways can they be seated in a row so that all the four boys do not sit together?",
         lambda: r6(4, 2, "boys", "girls"), ["144", "600", "480", "576"], 4),
        ("r6_e2", "There are 7 boys and 3 girls. In how many ways can they be seated in a row so that all the girls do not sit together?",
         lambda: r6(3, 7, "girls", "boys", as_multiple=8),
         [r"\(90\times 8!\)", r"\(84\times 8!\)", r"\(84\times 7!\)", r"\(78\times 8!\)"], 2),
        ("r6_e3", "There are 6 boys and 4 girls. Find the number of ways in which they can be seated in a row so that all the boys do not sit together.",
         lambda: r6(6, 4, "boys", "girls", as_multiple=6),
         [r"\(5040\times 6!\)", r"\(4920\times 5!\)", r"\(4920\times 6!\)", r"\(4800\times 6!\)"], 3)],
    7: [("r7_e1", "In how many ways can 6 boys and 6 girls be seated in a row so that boys and girls are alternate?",
         lambda: r7(6), [r"\(2(6!\times 6!)\)", r"\(6!\times 6!\)", r"\(12!\)", r"\(2(6!\times 5!)\)"], 1),
        ("r7_e2", "In how many ways can 7 boys and 7 girls be seated in a row so that boys and girls are alternate?",
         lambda: r7(7), [r"\(7!\times 7!\)", r"\(2(7!\times 6!)\)", r"\(14!\)", r"\(2(7!\times 7!)\)"], 4),
        ("r7_e3", "In how many ways can 8 boys and 8 girls be seated in a row so that boys and girls are alternate?",
         lambda: r7(8), [r"\(8!\times 8!\)", r"\(2(8!\times 8!)\)", r"\(2(8!\times 7!)\)", r"\(16!\)"], 2)],
}


def main(rules=range(1, 8)):
    for n in rules:
        folder = os.path.join(HERE, f"rule{n:02d}")
        dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
        assert dump["rule_card"] is None, f"Rule {n} already has a card"
        rows = {r["id"]: r for r in dump["rows"]}
        assert sorted(rows) == sorted(OLD[n]), (n, sorted(set(rows) ^ set(OLD[n])))
        out = []
        for rid, (fn, question, opts) in OLD[n].items():
            r = rows[rid]
            extra = {"question": question or r["question"].replace("\r\n", " "), **(opts or {})}
            for k in "abcd":                          # '319.' / '63000.' -> no trailing dot
                v = extra.get(k, r[k])
                if v != v.strip().rstrip("."):
                    extra[k] = v.strip().rstrip(".")
            if r["e"] is None or r["e"].strip():
                extra["e"] = ""                       # the page draws option e; NULL prints "None"
            extra = {k: v for k, v in extra.items() if v != r[k]}
            out.append(regen_entry(r, fn(), f"NEW_RULE_{n}", extra))
        json.dump(out, open(os.path.join(folder, "2_new_rows.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        c = {"rule_name": f"Rule {n}", "rule_html": CARDS[n]}
        json.dump(c, open(os.path.join(folder, "3_rule_card.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        qs, answers = [], []
        for key, text, fn, op, pos in NEW[n]:
            g = fn()
            qs.append(new_question(n, text, op, pos, g["solution"], g["rbe"], g["shortcut"]))
            a = g["answer"]
            answers.append([key, [a[0], [str(v) for v in a[1]] if isinstance(a[1], tuple) else str(a[1])]])
        json.dump({"rules_html": [{"chapter": CH, **c}], "questions": qs},
                  open(os.path.join(folder, "3_json_import_payload.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        json.dump(answers, open(os.path.join(folder, "3_answers.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Rule {n}: {len(out)} rows regenerated, card written, {len(qs)} new questions")


if __name__ == "__main__":
    main()
