"""Independent check of a rule folder (no DB access). Usage: python validate.py 1 2 3
Same checks as claude/runs/percentage/validate.py, for Permutation and Combination:
- 2_new_rows.json (regenerated existing rows): re-solves each question from its own text with ruleNN/solve.py
  (brute force / enumeration, a different method from the generator), checks the generator agrees, finds the single
  option holding the answer and stores it as new["ans"] (fixing a wrong key).
- 3_json_import_payload.json (new questions, optional): same checks, but the stated correct_answer must already be
  right, the rule card must be present, and the question must not repeat an existing one.
Options and Final Answers may be counting expressions (5!, \\frac{9!\\times 8!}{3!}, {}^{15}C_{3}, 2^{5}-1, 13\\times 14!):
they are evaluated exactly (pc_value) and compared by value. Writes ruleNN/4_validation_report.txt."""
import importlib.util, json, os, re, sys
from fractions import Fraction as F
from html.parser import HTMLParser
from math import comb, factorial, perm

ROOT = os.path.dirname(os.path.abspath(__file__))
GATE = None            # set to originality.Book(...) by reword/reword_check.py: every row must then be reworded and pass the gate
GATE_SIMPLE = False    # True for the simple (book-like) rewording runs: looser wording limits, same number rules
sys.path.insert(0, os.path.join(ROOT, "..", "..", "tools"))
import originality  # noqa: E402
CHAPTER = "permutation_combination"
BAD_TEXT = ("wait", "mistakenly", "let me", "i'll", "i will", "recalc", "approach:", "<b>answer:</b>", "<b>ans :</b>", "display=table")


class TagBalance(HTMLParser):
    VOID = {"br", "hr"}
    def __init__(self):
        super().__init__(); self.stack, self.errors = [], []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag: self.errors.append(tag)


def html_ok(s):
    p = TagBalance(); p.feed(s); p.close()
    return not p.errors and not p.stack


def latex_ok(s):
    if s.count(r"\(") != s.count(r"\)") or s.count(r"\[") != s.count(r"\]") or "$$" in s:
        return False
    for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S):
        depth = 0
        for ch in (a or b):
            depth += (ch == "{") - (ch == "}")
            if depth < 0: return False
        if depth: return False
    return True


def stray_tex(s):
    """LaTeX written outside \\( \\) / \\[ \\] (the page would show it raw): \\frac, \\times, ^{..}, _{..}, \\cdots ..."""
    outside = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", " ", s, flags=re.S)
    outside = re.sub(r"<[^>]+>", " ", outside)
    return re.search(r"\\(frac|times|cdots|qquad|quad|text|Rightarrow|left|right)\b|\^\{|_\{|\{\}\^", outside) is not None


def raw_lt(s):
    """A '<' inside math that a browser would read as the start of a tag."""
    return any(re.search(r"<(?=[A-Za-z!/])", m) for pair in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S) for m in pair if m)


def numbers(text):
    """Plain numbers in reading order (digits only; counting expressions are read by pc_value)."""
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))]


def _fact(x):
    assert x.denominator == 1 and 0 <= x <= 200
    return F(factorial(int(x)))


def _P(n, r):
    return F(perm(int(n), int(r)))


def _C(n, r):
    return F(comb(int(n), int(r)))


def pc_value(t):
    """Exact value of a counting expression written in LaTeX or plain text, or None.
    '\\frac{9!\\times 8!}{3!}', '{}^{15}C_{3}', '2(4!\\times 4!)', '2^{5}-1', '5! 4!', '120 ways', 'n = 6' -> Fraction."""
    s = re.sub(r"\\[()\[\]]", " ", t or "")
    if "=" in s:                                   # 'n = 6' / '8\times 9! = 2903040' -> every side must agree
        vals = [pc_value(part) for part in s.split("=")]
        vals = [v for v in vals if v is not None]
        return vals[0] if vals and all(v == vals[0] for v in vals) else None
    s = re.sub(r"\\text\{[^{}]*\}", " ", s)
    s = re.sub(r"\b(ways?|numbers?|words?|signals?|attempts?|persons?|people|students|lines|triangles|diagonals|rectangles|handshakes|cards)\b\.?", " ", s)
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", " ").replace(r"\ ", " ").replace("~", " ")
    s = s.replace(r"\times", "*").replace(r"\cdot", "*").replace("×", "*").strip().rstrip(".")
    if not s or re.search(r"[A-Za-oq-z]", re.sub(r"\{\}\^\{?\d+\}?\s*[PC]_\{?\d+\}?|\\frac", "", s)):
        return None                                # words such as 'None of these', 'Data inadequate'
    s = re.sub(r"(?:\{\})?\^\{?(\d+)\}?\s*([PC])_\{?(\d+)\}?", r"\2[\1,\3]", s)      # {}^{n}P_{r} -> P[n,r]
    s = re.sub(r"\^\s*\{(\d+)\}", r"^[\1]", s)    # powers first, so \frac{...}{(4!)^{3}} has no inner braces
    for _ in range(10):                            # innermost \frac{A}{B} -> ((A)/(B))
        s2 = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        if s2 == s:
            break
        s = s2
    if "\\" in s:
        return None
    s = s.replace("{", "(").replace("}", ")").replace("[", "(").replace("]", ")")
    s = re.sub(r"\^\s*(\(|\d+)", r"**\1", s)
    s = re.sub(r"(\d+)\s*!", r"f(\1)", s)
    for _ in range(10):                            # (expr)! -> f(expr)
        s2 = re.sub(r"\(([^()]*)\)\s*!", r"f(\1)", s)
        if s2 == s:
            break
        s = s2
    if "!" in s or "%" in s:
        return None
    s = re.sub(r"(?<=[\d)])\s*(?=[fPC(])", "*", s)     # implicit products: 5! 4! (f(5)f(4)), 2(..), )(
    s = re.sub(r"(?<=[\d)])\s+(?=\d)", "*", s)          # '5 6' only when separated by a space (never inside 120)
    s = s.replace(" ", "")
    if not re.fullmatch(r"[\d+\-*/().,fPC]+", s) or re.search(r"\d\.\d", s):
        return None
    s = re.sub(r"\d+", lambda m: f"F({m.group(0)})", s)
    try:
        v = eval(s, {"__builtins__": {}}, {"F": F, "f": _fact, "P": _P, "C": _C})
    except Exception:
        return None
    return v if isinstance(v, F) else None


def option_value(text, signed=False):
    """('number', v) or ('pair', (v1, v2)) for '35, 35' / '\\(126\\) and \\(126\\)'; None for words."""
    t = (text or "").strip()
    if not t or "none" in t.lower():
        return None
    parts = [p for p in re.split(r",(?![^{]*\})|\band\b|;", t) if p.strip()]
    if len(parts) == 2:
        a, b = pc_value(parts[0]), pc_value(parts[1])
        return ("pair", (a, b)) if a is not None and b is not None else None
    v = pc_value(t)
    return ("number", v) if v is not None else None


def as_value(kind, val):
    if kind == "pair":
        return ("pair", tuple(F(x) for x in val))
    return ("number", F(val))


def final_shows(fin, indep):
    """The Final Answer shows the value: some math segment (or side of an '=') evaluates to it, or a plain number equals it."""
    want = list(indep[1]) if indep[0] == "pair" else [indep[1]]
    segs = re.findall(r"\\\((.*?)\\\)", fin)
    vals = set()
    for sgm in segs:
        for part in sgm.split("="):
            v = pc_value(part)
            if v is not None:
                vals.add(v)
    vals |= set(numbers(re.sub(r"\\\(.*?\\\)", " ", fin)))
    return all(w in vals for w in want)


def check_layout(tag, fields, indep, raw, check):
    fails = 0
    s = fields["solution"]
    i = [s.find(t) for t in ("<b>Theorem :</b>", "<hr>", "<b>Traditional Method :</b>", "<b>Using the Specified Rule :</b>", "<b>Verification:</b>", "Final Answer")]
    fails += check(min(i) >= 0 and i == sorted(i) and s.count("<hr>") == 2 and s.count("Final Answer") == 1,
                   f"{tag} order Theorem -> Traditional -> Specified Rule -> Verification -> one Final Answer")
    trad = s[s.find("<b>Traditional Method :</b>"):s.find("<b>Using the Specified Rule :</b>")]
    fails += check("specified" not in trad.lower(), f"{tag} Traditional Method does not use the rule")
    for field in ("solution", "rule_based_explanation", "shortcut"):
        v = fields[field]
        fails += check(html_ok(v) and latex_ok(v) and not raw_lt(v), f"{tag} {field} HTML and LaTeX balanced, no raw < in math")
        fails += check(not stray_tex(v), f"{tag} {field} has no LaTeX outside math delimiters")
        fails += check(not any(b in v.lower() for b in BAD_TEXT), f"{tag} {field} has no draft/garbage text")
        fin = v[v.rfind("Final Answer"):]
        fails += check(final_shows(fin, indep), f"{tag} {field} Final Answer shows {[str(w) for w in (indep[1] if indep[0] == 'pair' else (indep[1],))]}")
    return fails


def run(n):
    folder = os.path.join(ROOT, f"rule{n:02d}")
    spec = importlib.util.spec_from_file_location("solve", os.path.join(folder, "solve.py"))
    solver = importlib.util.module_from_spec(spec); spec.loader.exec_module(solver)
    report, fails, fixes = [], 0, 0

    def check(ok, msg):
        report.append(("PASS " if ok else "FAIL ") + msg)
        return not ok

    dump = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))
    rows = {r["id"]: r for r in dump["rows"]}
    new_path = os.path.join(folder, "2_new_rows.json")
    new_rows = json.load(open(new_path, encoding="utf-8")) if os.path.exists(new_path) else []
    fails += check(sorted(rows) == sorted(x["id"] for x in new_rows), f"Rule {n}: every dumped row was regenerated")
    for x in new_rows:
        rid, r, new = x["id"], rows[x["id"]], x["new"]
        tag = f"row {rid}:"
        q = new.get("question", r["question"])
        opts = {k: new.get(k, r[k]) for k in "abcd"}
        indep = solver.solve(rid, q)
        declared = as_value(*x["answer"])
        fails += check(indep == declared, f"{tag} independent answer {indep[1]} = generator answer {declared[1]}")
        vals = [option_value(opts[k]) for k in "abcd"]
        hits = [v == indep for v in vals]
        fails += check(sum(hits) == 1, f"{tag} exactly one option holds the answer (found {sum(hits)})")
        vv = [v for v in vals if v is not None]
        fails += check(len(set(vv)) == len(vv), f"{tag} options distinct")
        fails += check(new.get("e", r["e"]) == "", f"{tag} option e is empty (NULL prints 'None')")
        if sum(hits) == 1:
            key = hits.index(True) + 1
            new["ans"] = key
            if key != r["ans"]:
                fixes += 1
                old = "abcde"[r["ans"] - 1] if 1 <= r["ans"] <= 5 else str(r["ans"])          # old rows may hold ans = 5
                report.append(f"FIX  {tag} answer key {old} ({opts.get(old, r.get(old))}) -> {'abcd'[key - 1]} ({opts['abcd'[key - 1]]})")
            else:
                report.append(f"PASS {tag} stored key {'abcd'[key - 1]} ({opts['abcd'[key - 1]]}) is correct")
        for f in ("question", "a", "b", "c", "d"):
            if f in new and new[f] != r[f]:
                report.append(f"FIX  {tag} {f}: {r[f]!r} -> {new[f]!r}")
        fails += check(latex_ok(q) and not raw_lt(q), f"{tag} question LaTeX balanced")
        fails += check(all(latex_ok(opts[k]) and "\\[" not in opts[k] for k in "abcd"), f"{tag} options use inline math only")
        fails += check_layout(tag, new, indep, x["answer"], check)
        dbl = [f for f in ("question", "a", "b", "c", "d", "solution", "rule_based_explanation", "shortcut")
               if chr(92) * 2 in (new.get(f, r.get(f)) or "")]
        fails += check(not dbl, f"{tag} no doubled backslash (would show raw LaTeX) in {dbl or 'any field'}")
        if GATE:                                     # rewording run: a fresh sentence and all-new numbers (claude/tools/originality.py)
            fails += check("question" in new and new["question"] != r["question"], f"{tag} question was reworded")
            problems = originality.check_question(q, GATE, r["question"], simple=GATE_SIMPLE)
            fails += check(not problems, f"{tag} originality gate {originality.measures(q, GATE, r['question'])}" + (f" - {problems}" if problems else ""))
    if new_rows:
        json.dump(new_rows, open(new_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    card_path = os.path.join(folder, "3_rule_card.json")
    if os.path.exists(card_path):
        c = json.load(open(card_path, encoding="utf-8"))
        h = c["rule_html"]
        fails += check(c["rule_name"] == f"Rule {n}" and f"<h2>Rule {n}:" in h and html_ok(h) and latex_ok(h) and not raw_lt(h),
                       f"Rule {n}: rule card has the right title, balanced HTML/LaTeX, no raw < in math")

    pay_path = os.path.join(folder, "3_json_import_payload.json")
    if os.path.exists(pay_path):
        payload = json.load(open(pay_path, encoding="utf-8"))
        answers = json.load(open(os.path.join(folder, "3_answers.json"), encoding="utf-8"))
        cards = payload["rules_html"]
        fails += check(len(cards) == 1 and cards[0]["rule_name"] == f"Rule {n}" and html_ok(cards[0]["rule_html"])
                       and latex_ok(cards[0]["rule_html"]) and not raw_lt(cards[0]["rule_html"]), f"Rule {n}: one clean rule card in the payload")
        if os.path.exists(card_path):
            fails += check(cards[0]["rule_html"] == json.load(open(card_path, encoding="utf-8"))["rule_html"], f"Rule {n}: payload card = 3_rule_card.json")
        seen = {re.sub(r"\s+", " ", r["question"]) for r in rows.values()}
        for i, (qq, (key_name, decl)) in enumerate(zip(payload["questions"], answers), 1):
            tag = f"new {key_name}:"
            fails += check(qq["rule_name"] == f"Rule {n}" and qq["chapter"] == CHAPTER, f"{tag} chapter and rule_name set")
            indep = solver.solve(key_name, qq["question"])
            declared = as_value(*decl)
            fails += check(indep == declared, f"{tag} independent answer {indep[1]} = generator answer {declared[1]}")
            vals = [option_value(qq[k]) for k in "abcd"]
            hits = [v == indep for v in vals]
            fails += check(sum(hits) == 1 and hits.index(True) + 1 == qq["correct_answer"],
                           f"{tag} correct_answer {qq['correct_answer']} is the only option holding the answer")
            vv = [v for v in vals if v is not None]
            fails += check(len(set(vv)) == len(vv), f"{tag} options distinct")
            norm = re.sub(r"\s+", " ", qq["question"])
            fails += check(norm not in seen, f"{tag} question is not a repeat")
            seen.add(norm)
            fails += check(latex_ok(qq["question"]) and not raw_lt(qq["question"]), f"{tag} question LaTeX balanced")
            fails += check(all(latex_ok(qq[k]) and "\\[" not in qq[k] for k in "abcd"), f"{tag} options use inline math only")
            fails += check_layout(tag, qq, indep, decl, check)
        positions = [qq["correct_answer"] for qq in payload["questions"]]
        report.append(f"INFO new questions' answer positions: {''.join('abcd'[p - 1] for p in positions)}")

    passed = sum(t.startswith("PASS") for t in report)
    head = f"Rule {n}: {passed}/{passed + fails} checks passed, {fails} failed, {fixes} answer keys fixed"
    open(os.path.join(folder, "4_validation_report.txt"), "w", encoding="utf-8").write(head + "\n\n" + "\n".join(report) + "\n")
    for t in report:
        if not t.startswith("PASS"):
            print("   ", t)
    print(head)
    return fails


if __name__ == "__main__":
    sys.exit(1 if sum(run(n) for n in map(int, sys.argv[1:])) else 0)
