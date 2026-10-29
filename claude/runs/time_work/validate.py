"""Independent check of a rule folder (no DB access). Usage: python validate.py 1 2 3
- 2_new_rows.json (regenerated existing rows): re-solves each question from its own text with ruleNN/solve.py
  (a different method from gen.py), checks the generator agrees, finds the single option holding the answer
  and stores it as new["ans"] (fixing a wrong key).
- 3_json_import_payload.json (new questions, optional): same checks, but the stated correct_answer must
  already be right, the rule card must be present, and the question must not repeat an existing one.
Also checks the solution layout, HTML, LaTeX and that no draft text slipped in. Writes ruleNN/4_validation_report.txt."""
import importlib.util, json, os, re, sys
from fractions import Fraction as F
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
GATE = None            # set to originality.Book(...) by reword_check.py: every row must then be reworded and pass the gate
GATE_SIMPLE = False    # True for the simple (book-like) rewording runs: looser wording limits, same number rules
sys.path.insert(0, os.path.join(ROOT, "..", "..", "tools"))
import originality  # noqa: E402
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
    if s.count(r"\(") != s.count(r"\)") or s.count(r"\[") != s.count(r"\]"):
        return False
    for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S):
        depth = 0
        for ch in (a or b):
            depth += (ch == "{") - (ch == "}")
            if depth < 0: return False
        if depth: return False
    return True


def raw_lt(s):
    """A '<' inside math that a browser would read as the start of a tag."""
    return any(re.search(r"<(?=[A-Za-z!/])", m) for pair in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S) for m in pair if m)


def numbers(text):
    """Numbers in reading order, with 12\frac{3}{7} and \frac{4}{9} read as one number each."""
    out = []
    pat = r"(\d+)?\\frac\{(\d+)\}\{(\d+)\}|(\d+(?:\.\d+)?)"
    for whole, a, b, plain in re.findall(pat, text):
        out.append(F(plain) if plain else F(int(whole or 0)) + F(int(a), int(b)))
    return out


X_VAL, Y_VAL = F(7), F(3)                          # algebraic answers are compared at x = 7, y = 3


def expr_value(t):
    """Value of a small algebraic expression such as \\frac{x-2}{x} or 4(2x+y) at x = 7, y = 3 (None if it is not one)."""
    t = t.strip()
    if not re.fullmatch(r"[\dxy+\-()\\{}frac ]+", t) or not re.search(r"[xy]", t.replace("frac", "")):
        return None
    s = t
    while r"\frac" in s:                            # innermost \frac{A}{B} -> ((A)/(B))
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = s.replace(" ", "")
    s = re.sub(r"(?<=[\dxy)])(?=[xy(])", "*", s)    # 2x -> 2*x, )( -> )*(, 4(2x+y) -> 4*(2*x+y)
    if not re.fullmatch(r"[\dxy+\-*/()]+", s):
        return None
    return F(eval(s, {"__builtins__": {}}, {"x": X_VAL, "y": Y_VAL}))


def option_value(text):
    t = re.sub(r"\\[()]", "", text or "").strip()
    if not t or "none" in t.lower():
        return None
    ev = expr_value(t)
    if ev is not None:
        return ("expr", ev)
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)", t)
    if m:
        return ("ratio", F(m[1]) / F(m[2]))
    if "=" in t:                                    # "Boys = 39, Girls = 26" -> the numbers after each "="
        t = ", ".join(part.split("=", 1)[1] for part in t.split(",") if "=" in part)
    nums = numbers(t)
    if len(nums) == 3:                              # "A 30 days, B 20 days, C 60 days"
        return ("triple", tuple(nums))
    if len(nums) == 2:
        return ("pair", (nums[0], nums[1]))
    if len(nums) == 1:
        return ("number", nums[0])
    return None


def as_value(kind, val):
    if kind == "ratio":
        return ("ratio", F(int(val[0]), int(val[1])))
    if kind in ("pair", "triple"):
        return (kind, tuple(F(x) for x in val))
    return (kind if kind == "expr" else "number", F(val))


def shown(indep, raw):
    """Values the Final Answer must show: 7 and 3 for 7 : 3; 15.2 (written 15.20); 3/5 (written \\frac{3}{5} or 0.6)."""
    if indep[0] == "ratio":
        return [F(int(t)) for t in raw[1]]
    return list(indep[1] if indep[0] in ("pair", "triple") else (indep[1],))


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
        fails += check(not any(b in v.lower() for b in BAD_TEXT), f"{tag} {field} has no draft/garbage text")
        fin = v[v.rfind("Final Answer"):]
        want = shown(indep, raw)
        if indep[0] == "ratio":                      # order matters: 7 : 3 is not 3 : 7
            ok = re.search(rf"(?<![\d.]){want[0]}\s*:\s*{want[1]}(?![\d.])", fin) is not None
        elif indep[0] == "expr":                     # some \( ... \) in the Final Answer must have the same value
            ok = any(expr_value(m) == indep[1] for m in re.findall(r"\\\((.*?)\\\)", fin))
        else:
            ok = all(w in numbers(fin) for w in want)
        fails += check(ok, f"{tag} {field} Final Answer shows {' : '.join(str(w) for w in want) if indep[0] == 'ratio' else [str(w) for w in want]}")
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
        seen = {re.sub(r"\s+", " ", r["question"]) for r in rows.values()}
        for i, (qq, (key_name, decl)) in enumerate(zip(payload["questions"], answers), 1):
            tag = f"new {key_name}:"
            fails += check(qq["rule_name"] == f"Rule {n}" and qq["chapter"] == "time_n_work", f"{tag} chapter and rule_name set")
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
