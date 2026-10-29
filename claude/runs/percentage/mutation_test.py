"""Breaks a scratch copy of rule folders in one way at a time and checks validate.py fails each time.
Usage: python mutation_test.py 1 2 3 4   (folders are copied to a temp dir; the real ones are not touched)"""
import json, os, shutil, sys, tempfile
import validate

HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    return json.load(open(p, encoding="utf-8"))


def save(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def m_option(folder):      # the correct option's value changed -> no option holds the answer
    p = os.path.join(folder, "2_new_rows.json"); d = load(p); x = d[-1]
    k = "abcd"[x["new"].get("ans", x["old"]["ans"]) - 1]
    x["new"][k] = r"\(999\) days"; save(p, d)


def m_answer(folder):      # generator answer wrong -> independent solver disagrees
    p = os.path.join(folder, "2_new_rows.json"); d = load(p); x = d[0]
    a = x["answer"]
    x["answer"] = [a[0], [str(int(float(eval(v))) + 1) for v in a[1]] if isinstance(a[1], list) else str(eval(a[1]) + 1)]
    save(p, d)


def m_final(folder):       # Final Answer in the shortcut shows another number
    p = os.path.join(folder, "2_new_rows.json"); d = load(p); x = d[min(1, len(d) - 1)]
    s = x["new"]["shortcut"]; i = s.rfind("Final Answer")
    x["new"]["shortcut"] = s[:i] + "Final Answer: \\(12345\\) days</b></div>"; save(p, d)


def m_draft(folder):       # LLM draft text slipped in
    p = os.path.join(folder, "2_new_rows.json"); d = load(p)
    d[0]["new"]["solution"] = d[0]["new"]["solution"].replace("<b>Traditional Method :</b>", "<b>Traditional Method :</b> Wait, let me recheck."); save(p, d)


def m_order(folder):       # Traditional Method moved after the Specified Rule
    p = os.path.join(folder, "2_new_rows.json"); d = load(p); s = d[0]["new"]["solution"]
    d[0]["new"]["solution"] = s.replace("<b>Traditional Method :</b>", "@@T@@").replace("<b>Using the Specified Rule :</b>", "<b>Traditional Method :</b>").replace("@@T@@", "<b>Using the Specified Rule :</b>")
    save(p, d)


def m_rawlt(folder):       # raw < inside math
    p = os.path.join(folder, "2_new_rows.json"); d = load(p)
    d[0]["new"]["rule_based_explanation"] = d[0]["new"]["rule_based_explanation"].replace(r"\(", r"\(x<y,\ ", 1); save(p, d)


def m_card(folder):        # card title wrong
    p = os.path.join(folder, "3_rule_card.json")
    if not os.path.exists(p):
        return False
    c = load(p); c["rule_html"] = c["rule_html"].replace("<h2>Rule", "<h2>Rul", 1); save(p, c)


def m_newkey(folder):      # new question's stated key wrong
    p = os.path.join(folder, "3_json_import_payload.json")
    if not os.path.exists(p):
        return False
    d = load(p); q = d["questions"][0]; q["correct_answer"] = q["correct_answer"] % 4 + 1; save(p, d)


def m_trad_rule(folder):   # Traditional Method quotes the rule
    p = os.path.join(folder, "2_new_rows.json"); d = load(p)
    d[0]["new"]["solution"] = d[0]["new"]["solution"].replace("<b>Step 1:", "By the specified rule, <b>Step 1:", 1); save(p, d)


def m_direction(folder):   # a signed answer's Final Answer says increase instead of decrease (or the other way)
    p = os.path.join(folder, "2_new_rows.json"); d = load(p); x = d[0]
    if x["answer"][0] != "signed":
        return False
    s = x["new"]["shortcut"]
    swap = {"a decrease": "an increase", "an increase": "a decrease", "a loss": "a profit", "a profit": "a loss"}
    i = s.rfind("Final Answer")
    word = next(w for w in swap if w in s[i:])
    x["new"]["shortcut"] = s[:i] + s[i:].replace(word, swap[word], 1); save(p, d)


def m_new_answer(folder):  # a new question's generator answer wrong -> the independent solver disagrees
    p = os.path.join(folder, "3_answers.json")
    if not os.path.exists(p):
        return False
    d = load(p); a = d[0][1]
    a[1] = [str(eval(v) + 1) for v in a[1]] if isinstance(a[1], list) else str(eval(a[1]) + 1); save(p, d)


def m_new_option(folder):  # a new question's correct option changed -> no option holds the answer
    p = os.path.join(folder, "3_json_import_payload.json")
    if not os.path.exists(p):
        return False
    d = load(p); q = d["questions"][-1]; q["abcd"[q["correct_answer"] - 1]] = r"\(999\%\) excess"; save(p, d)


ROW_MUTATIONS = (m_option, m_answer, m_final, m_draft, m_order, m_rawlt, m_trad_rule, m_direction)
MUTATIONS = [m_option, m_answer, m_final, m_draft, m_order, m_rawlt, m_card, m_newkey, m_trad_rule, m_direction, m_new_answer, m_new_option]

if __name__ == "__main__":
    bad = 0
    for n in map(int, sys.argv[1:]):
        for mut in MUTATIONS:
            tmp = tempfile.mkdtemp()
            src = os.path.join(HERE, f"rule{n:02d}")
            dst = os.path.join(tmp, f"rule{n:02d}")
            shutil.copytree(src, dst)
            if not load(os.path.join(dst, "2_new_rows.json")) and mut in ROW_MUTATIONS:   # rule with no old rows
                shutil.rmtree(tmp); continue
            if mut(dst) is False:
                shutil.rmtree(tmp); continue
            validate.ROOT = tmp
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                fails = validate.run(n)
            print(f"Rule {n} {mut.__name__:12} -> {'caught (' + str(fails) + ' failed)' if fails else 'NOT CAUGHT'}")
            bad += not fails
            shutil.rmtree(tmp)
    print("all mutations caught" if not bad else f"{bad} mutations NOT caught")
    sys.exit(1 if bad else 0)
