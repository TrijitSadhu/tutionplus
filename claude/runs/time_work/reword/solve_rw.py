"""Independent solvers for the reworded Time & Work rows (reword/<batch>/ruleNN). The new sentences are free-form, so
each row is mapped to its problem type by row id (KIND); the numbers are read from the question in the order the type
lists them, and the answer is worked out from first principles - one-day / one-hour rates, man-hours, a linear solve or a
day-by-day count - never through the rule formula the generator uses."""
import re
from fractions import Fraction as F
from solve_1_4 import finish_time, lin_solve
from validate import numbers


def pair_rates(x, y, z):
    """A + B = 1/x, B + C = 1/y, C + A = 1/z -> one-day rates of A, B, C."""
    return lin_solve([[1, 1, 0], [0, 1, 1], [1, 0, 1]], [1 / x, 1 / y, 1 / z])


def k_men_days(n):                         # M1 men, D1 days; how many men for D2 days
    M1, D1, D2 = n[:3]
    M = next(M for M in range(1, 100000) if M * D2 >= M1 * D1)
    assert M * D2 == M1 * D1
    return ("number", F(M))


def k_trees(q):                            # read by label: "<M1> men" ... "<leave> men / of them", "<W1> trees", hours (first, last)
    men = [F(x) for x in re.findall(r"(\d+) (?:men\b|of (?:them|the men)\b)", q)]
    W1 = F(re.search(r"(\d+) trees", q)[1])
    hours = [F(x) for x in re.findall(r"(\d+)(?:-| )hours?\b", q)]
    M1, leave, D1, D2 = men[0], men[1], hours[0], hours[-1]
    per_man_hour = W1 / (M1 * D1)
    return ("number", sum((M1 - leave) * per_man_hour for _ in range(int(D2))))


def k_k_works(n):                          # one job in D1 days; k jobs
    D1, k = n[:2]
    return ("number", finish_time(1 / D1, F(k)))


def k_toys(q):                             # read by label (any word order): men, toys, days, hours - first and second group
    lab = lambda unit: [F(x) for x in re.findall(rf"(\d+)(?:-| ){unit}", q)]
    (M1, M2), (W1, W2), (D1,), (T1, T2) = lab("men"), lab("toys"), lab("days")[:1], lab("hours?")
    per_man_hour = W1 / (M1 * D1 * T1)
    return ("number", finish_time(M2 * T2 * per_man_hour, W2))


def k_wmb(n):                              # woman hw h = man hm h = boy hb h; T1 h/day, M1 men, D1 days; k men, k women, k boys, T2 h/day
    hw, hm, hb, T1, M1, D1, men, women, boys, T2 = n[:10]
    job = M1 * T1 * D1 / hm                # parts (one part = what a man does in hm hours)
    return ("number", finish_time((men / hm + women / hw + boys / hb) * T2, job))


def k_r3_each(n):
    a, b, c = pair_rates(*n[:3])
    return ("triple", (1 / a, 1 / b, 1 / c))


def k_r3_stages(n):                        # all three d_all days, then B and C d_bc days, then C alone
    a, b, c = pair_rates(*n[:3])
    d_all, d_bc = n[3:5]
    return ("number", finish_time(c, 1 - d_all * (a + b + c) - d_bc * (b + c)))


def k_r3_together(n):
    a, b, c = pair_rates(*n[:3])
    return ("number", finish_time(a + b + c))


def k_two(n):                              # A x days, B y days, together
    x, y = n[:2]
    return ("number", finish_time(1 / x + 1 / y))


def k_two_groups(n):                       # g1 men in x days, g2 women in y days, all together
    g1, x, g2, y = n[:4]
    return ("number", finish_time(1 / x + 1 / y))


def k_c_as_ab(n):                          # A x, B y, C as fast as A and B together; B and C together
    x, y = n[:2]
    return ("number", finish_time(1 / y + (1 / x + 1 / y)))


def k_frac_help(n):                        # A does p in d days, A and B do the rest in e days; A and B on the whole
    p, d, e = n[:3]
    return ("number", finish_time((1 - p) / e))


def k_then_c(n):                           # A x, B y together k days, C finishes in m days; C alone
    x, y, k, m = n[:4]
    left = 1 - k * (1 / x + 1 / y)
    return ("number", 1 / (left / m))


def k_b_pairs(n):                          # A ta, B + C tbc, A + C tac; B alone
    ta, tbc, tac = n[:3]
    a, b, c = lin_solve([[1, 0, 0], [0, 1, 1], [1, 0, 1]], [1 / ta, 1 / tbc, 1 / tac])
    return ("number", 1 / b)


def k_fractions(n):                        # A does p in d days, B does q in e days; together
    p, d, q, e = n[:4]
    return ("number", finish_time(p / d + q / e))


def k_three(n):
    x, y, z = n[:3]
    return ("number", finish_time(1 / x + 1 / y + 1 / z))


def k_c_missing(n):                        # A x, B y, all three T; C alone
    x, y, T = n[:3]
    return ("number", 1 / (1 / T - 1 / x - 1 / y))


def k_half(n):                             # A takes half B's time, C as fast as A and B together, all three T days
    T = n[0]
    u = 1 / T / (2 + 1 + 3)                # rates: B u, A 2u, C 3u
    return ("triple", (1 / (2 * u), 1 / u, 1 / (3 * u)))


def k_groups(n):                           # m men in tm h, w women in tw h, c children in tc h; one of each
    m, tm, w, tw, c, tc = n[:6]
    return ("number", 1 / (1 / (m * tm) + 1 / (w * tw) + 1 / (c * tc)))


def k_twice_thrice(n):                     # A twice B's time and three times C's; all three T days (T is the last number)
    u = 1 / n[-1] / 6                      # rates: A u, B 2u, C 3u
    return ("triple", (1 / u, 1 / (2 * u), 1 / (3 * u)))


# ---------------------------------------------------------------- batch 2 types (Rules 6-10)
def k_other_alone(n):                      # A + B together ab days, A alone a days; B alone
    ab, a = n[:2]
    return ("number", 1 / (1 / ab - 1 / a))


def k_c_from_groups(n):                    # A + B ab days, A + B + C abc days; C alone
    ab, abc = n[:2]
    return ("number", 1 / (1 / abc - 1 / ab))


def k_ab_chain(n):                         # B b, B + C bc, A + B + C abc; A + B together
    b, bc, abc = n[:3]
    a = 1 / abc - 1 / bc
    return ("number", finish_time(a + 1 / b))


def k_ac_b(n):                             # A + B ab, B + C bc, A + B + C abc -> (A + C, B)
    ab, bc, abc = n[:3]
    a, b, c = lin_solve([[1, 1, 0], [0, 1, 1], [1, 1, 1]], [1 / ab, 1 / bc, 1 / abc])
    return ("pair", (1 / (a + c), 1 / b))


def k_frac_b(n):                           # A does p (the number below 1) in d days, then A + B finish the rest in e days; B alone
    p = next(v for v in n[:3] if v < 1)
    d, e = [v for v in n[:3] if v is not p][:2]
    return ("number", 1 / ((1 - p) / e - p / d))


def k_finish_both(n):                      # A + B ab, B b; both work k days, then A alone finishes
    ab, b, k = n[:3]
    return ("number", (1 - k / ab) / (1 / ab - 1 / b))


def k_finish_b_first(n):                   # A + B ab, B b; B alone works k days, then A alone finishes
    ab, b, k = n[:3]
    return ("number", (1 - k / b) / (1 / ab - 1 / b))


def k_called_off(n):                       # A + B ab; together k days, A alone the rest in m days -> (A, B)
    ab, k, m = n[:3]
    a = (1 - k / ab) / m
    return ("pair", (1 / a, 1 / (1 / ab - a)))


def k_ab_from_abc(n):                      # A + B + C abc, B b, B + C bc; A + B together
    abc, b, bc = n[:3]
    return ("number", finish_time(1 / abc - 1 / bc + 1 / b))


def r7_rates(n):                           # B takes p times as long as A + C, C takes q times as long as A + B, all three T
    p, q, T = n[:3]
    return lin_solve([[1, -p, 1], [1, 1, -q], [1, 1, 1]], [0, 0, 1 / T])


def k_r7_each(n):
    a, b, c = r7_rates(n)
    return ("triple", (1 / a, 1 / b, 1 / c))


def k_r7_bc(n):
    a, b, c = r7_rates(n)
    return ("number", 1 / (b + c))


def lab(q, unit):
    """Numbers written as '<n> <unit>' (or '<n>-<unit>'), in reading order."""
    return [F(x) for x in re.findall(rf"(\d+)(?:-| ){unit}\b", q)]


def k_mw(q):                               # by label: x1 men or y1 women/boys in D days; x2 men and y2 women/boys; 'half'
    men, other, days = lab(q, "men"), lab(q, "(?:women|boys)"), lab(q, "days?")
    x1, x2, y1, y2, D = men[0], men[1], other[0], other[1], days[0]
    part = F(1, 2) if "half" in q else F(1)
    return ("number", part / (x2 / (x1 * D) + y2 / (y1 * D)))


def mb_label(q):                           # by label: groups in reading order - (men, boys, days) twice, then men, boys
    men, boys, days = lab(q, "men"), lab(q, "boys"), lab(q, "days")
    return men, boys, days


def k_mw_whereas(n):                       # x1 men in D1 days, y1 women in D2 days; x2 men and y2 women
    x1, D1, y1, D2, x2, y2 = n[:6]
    return ("number", 1 / (x2 / (x1 * D1) + y2 / (y1 * D2)))


def mb_rates(q):                           # a1 men + b1 boys in x days, a2 men + b2 boys in y days (by label)
    men, boys, days = mb_label(q)
    return lin_solve([[men[0] * days[0], boys[0] * days[0]], [men[1] * days[1], boys[1] * days[1]]], [1, 1])


def k_mb_time(q):                          # ... then the third group of men and boys
    man, boy = mb_rates(q)
    men, boys, _ = mb_label(q)
    return ("number", finish_time(men[2] * man + boys[2] * boy))


def k_mb_ratio(q):
    man, boy = mb_rates(q)
    return ("ratio", man / boy)


def k_mb_ratio_boy(q):
    man, boy = mb_rates(q)
    return ("ratio", boy / man)


EQUIV = re.compile(r"(\d+) men [^.?,;]*?(?:as much|as productive|as fast|equal)[^.?,;]*?(\d+) boys")


def k_equiv(q):                            # m1 men + b1 boys in D days; m2 men + b2 boys; "em men ... as much as eb boys" anywhere
    m = EQUIV.search(q)
    em, eb = F(m[1]), F(m[2])
    men, boys, days = mb_label(q[:m.start()] + " " + q[m.end():])
    (m1, m2), (b1, b2), D = men[:2], boys[:2], days[0]
    boy = 1 / ((m1 * eb / em + b1) * D)
    return ("number", 1 / ((m2 * eb / em + b2) * boy))


def k_times(q):                            # a1 M + b1 B = k (a2 M + b2 B) per hour, B = 1 -> man : boy (by label)
    men, boys = lab(q, "m[ae]n"), lab(q, "boys?")
    k = F(re.search(r"(\d+) times", q)[1])
    (a1, a2), (b1, b2) = men[:2], boys[:2]
    return ("ratio", (k * b2 - b1) / (a1 - k * a2))


def k_children(q):                         # c children + m men in D days, a child takes twice a man's time; m2 men alone
    c, (m, m2), D = lab(q, "children")[0], lab(q, "men")[:2], lab(q, "days")[0]
    man = 1 / ((c / 2 + m) * D)
    return ("number", 1 / (m2 * man))


def k_orig_men(n):                         # M men in D days, (M - x) men in D + d days: find M by search
    D, x, d = n[:3]
    return ("number", F(next(M for M in range(int(x) + 1, 100000) if M * D == (M - x) * (D + d))))


KIND = {}                                  # row id -> solver; filled per batch below
KIND.update({181: k_men_days, 1229: k_men_days, 1233: k_men_days, 182: k_trees, 1230: k_trees, 1234: k_trees, 1235: k_trees,
             183: k_k_works, 1231: k_k_works, 1236: k_k_works,
             184: k_toys, 1238: k_toys, 1239: k_toys, 185: k_wmb, 1237: k_wmb,
             186: k_r3_each, 1242: k_r3_each, 187: k_r3_stages, 1241: k_r3_stages, 1240: k_r3_together, 1243: k_r3_together,
             188: k_two, 1246: k_two, 1248: k_two, 1665: k_two, 1247: k_two_groups, 189: k_c_as_ab, 1249: k_c_as_ab,
             190: k_frac_help, 1250: k_frac_help, 191: k_then_c, 1663: k_then_c, 192: k_b_pairs, 1664: k_b_pairs,
             193: k_fractions, 1666: k_fractions,
             194: k_three, 1251: k_three, 1256: k_three, 1257: k_three, 195: k_c_missing, 1252: k_c_missing,
             196: k_half, 1253: k_half, 197: k_groups, 1254: k_groups, 198: k_twice_thrice})


KIND.update({199: k_other_alone, 200: k_c_from_groups, 1260: k_c_from_groups, 1269: k_c_from_groups, 201: k_ab_chain, 1261: k_ab_chain,
             202: k_ac_b, 1262: k_ac_b, 203: k_frac_b, 1263: k_frac_b, 204: k_finish_both, 1264: k_finish_both,
             207: k_finish_b_first, 1267: k_finish_b_first, 205: k_called_off, 1265: k_called_off, 206: k_ab_from_abc, 1266: k_ab_from_abc,
             1259: k_three,
             208: k_r7_each, 1270: k_r7_each, 209: k_r7_each, 1271: k_r7_each, 210: k_r7_bc, 1272: k_r7_bc, 1273: k_r7_bc,
             211: k_mw, 1274: k_mw, 1275: k_mw, 1276: k_mw, 1277: k_mw, 1278: k_mw, 1279: k_mw,
             212: k_mb_time, 1280: k_mb_time, 213: k_mb_ratio, 1281: k_mb_ratio, 1284: k_mb_ratio_boy, 216: k_mb_ratio_boy,
             214: k_equiv, 1282: k_equiv, 215: k_times, 1283: k_times, 217: k_children, 1285: k_children,
             218: k_orig_men, 1286: k_orig_men, 1287: k_orig_men, 1288: k_orig_men, 1289: k_orig_men})

# ---------------------------------------------------------------- batch 3 types (Rules 11-20)
def labf(q, unit):
    """Like lab, but also reads '\\(7\\frac{1}{2}\\) <unit>' as one number."""
    pat = rf"(?:\\\((\d+)?\\frac\{{(\d+)\}}\{{(\d+)\}}\\\)|(\d+))(?:-| ){unit}\b"
    return [F(p) if p else F(int(w or 0)) + F(int(a), int(b)) for w, a, b, p in re.findall(pat, q)]


def times_word(q):                         # "4 times as fast" / "twice as productive"
    m = re.search(r"(\d+) times", q)
    return F(m[1]) if m else F(2) if "twice" in q else None


def k_faster(q):                           # A n times as fast as B, B takes D days more; together (A's time found by search)
    n, D = times_word(q), labf(q, "days")[0]
    t = next(F(k, 100) for k in range(1, 10 ** 6) if F(k, 100) * n - F(k, 100) == D)
    return ("number", finish_time(1 / t + 1 / (n * t)))


def k_hours(q):                            # by label: I d1 days, you d2 days; hours a day h1, h2, then h together
    (d1, d2), (h1, h2, h) = labf(q, "days")[:2], labf(q, "hours?")[:3]
    per_day = (1 / (d1 * h1) + 1 / (d2 * h2)) * h      # each person's one-hour work, times the hours worked a day
    return ("number", finish_time(per_day))


def last_sentence(q):
    return re.split(r"[.]\s", q)[-1]


def k_c13q(q):                             # A x days, B y days, C as long as A and B together; the pair/trio asked in the last sentence
    x, y = numbers(q)[:2]
    a, b = 1 / x, 1 / y
    c = 1 / finish_time(a + b)             # C's one-day work from his time
    who = set(re.findall(r"\b([ABC])\b", last_sentence(q)))
    return ("number", finish_time(sum({"A": a, "B": b, "C": c}[w] for w in who)))


def k_good(q):                             # A does n times B's work; together x days; A alone (or each, as a pair)
    n, x = times_word(q), labf(q, "days")[0]
    b = lin_solve([[n * x + x]], [1])[0]   # (n b + b) x = 1
    if "each" in last_sentence(q):
        return ("pair", (1 / (n * b), 1 / b))
    return ("number", 1 / (n * b))


def k_left(n):                             # A x, B y; together until A leaves, B alone z more days -> days A worked (half-day search)
    x, y, z = n[:3]
    return ("number", next(F(k, 2) for k in range(1, 10 ** 5) if F(k, 2) * (1 / x + 1 / y) + z / y == 1))


def k_a_alone(n):                          # A + B T days; together k days, A alone m more days -> A alone
    T, k, m = n[:3]
    a = (1 - k / T) / m
    return ("number", 1 / a)


def k_mwb(q):                              # by label: x1 men or x2 women or x3 boys in D days; 1 man + 1 woman + 1 boy
    (x1,), (x2,), (x3,), (D,) = lab(q, "m[ae]n")[:1], lab(q, "wom[ae]n")[:1], lab(q, "boys?")[:1], lab(q, "days?")[:1]
    return ("number", finish_time(1 / (x1 * D) + 1 / (x2 * D) + 1 / (x3 * D)))


def k_absent(n):                           # planned x days, n absent, the rest y days -> search M
    x, a, y = n[:3]
    return ("number", F(next(M for M in range(int(a) + 1, 100000) if M * x == (M - a) * y)))


def k_extra(n):                            # M men D days; M + x men D - d days -> search M
    D, x, d = n[:3]
    return ("number", F(next(M for M in range(1, 100000) if M * D == (M + x) * (D - d))))


def k_builder(q):                          # D days planned, x men, y more after d days; without them: days late / total (day-by-day count)
    D, x, y, d = numbers(q)[:4]
    work = x * d + (x + y) * (D - d)
    days, done = 0, F(0)
    while done + x <= work:
        done += x
        days += 1
    days += (work - done) / x
    return ("number", days - D if re.search(r"\b(late|behind)\b", q) else days)


KIND.update({219: k_faster, 1290: k_faster, 1291: k_faster, 1293: k_faster, 1294: k_faster,
             220: k_hours, 1295: k_hours, 1297: k_hours, 1298: k_hours,
             221: k_c13q, 1299: k_c13q, 1300: k_c13q, 1301: k_c13q, 1302: k_c13q, 1303: k_c13q, 1304: k_c13q,
             222: k_good, 1305: k_good, 1307: k_good, 1308: k_good, 1309: k_good, 1310: k_good,
             223: k_times, 1312: k_times,
             224: k_left, 1313: k_left, 1314: k_left, 1315: k_left, 1316: k_left, 225: k_a_alone, 1317: k_a_alone,
             226: k_mwb, 1318: k_mwb, 1319: k_mwb, 1320: k_mwb, 1321: k_mwb,
             227: k_absent, 1322: k_absent, 1324: k_absent, 1325: k_absent,
             228: k_extra, 1326: k_extra, 1327: k_extra, 1328: k_extra, 1329: k_extra,
             229: k_builder, 1330: k_builder, 1331: k_builder, 1332: k_builder, 1333: k_builder, 1334: k_builder})

BY_LABEL = {k_toys, k_trees, k_mw, k_mb_time, k_mb_ratio, k_mb_ratio_boy, k_equiv, k_times, k_children,
            k_faster, k_hours, k_c13q, k_good, k_mwb, k_builder}                    # these read the question text itself, not the ordered numbers


def solve(rid, q):
    f = KIND[rid]
    try:
        return f(q) if f in BY_LABEL else f(numbers(q))
    except (ValueError, IndexError, TypeError, ZeroDivisionError, StopIteration):
        return ("unsolved", q[:40])        # a question this type can not read -> the validator's answer check fails
