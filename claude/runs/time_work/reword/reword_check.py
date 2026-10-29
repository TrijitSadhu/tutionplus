"""Validates the reword/ruleNN folders with the originality gate on (every row must be reworded: fresh sentence, all-new
numbers, checked against the book text and the question it replaces), then mutation-tests the validator on scratch copies,
including m_copy (the old book question put back) and m_old_number (one old number kept).
Usage: python reword_check.py <batch folder>   (pilot, b1, b2, ...; simple/pilot, simple/b1, ... use the simple gate mode)"""
import contextlib, io, json, os, shutil, sys, tempfile

TW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
sys.path.insert(0, TW)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))          # solve_rw.py
import validate  # noqa: E402
import mutation_test as mt  # noqa: E402

validate.GATE = validate.originality.Book(os.path.join(TW, "pdf_text.txt"))
validate.GATE_SIMPLE = (sys.argv[1].replace("\\", "/").startswith("simple/")            # simple-style pass of an old batch
                       or os.path.exists(os.path.join(HERE, "SIMPLE_STYLE")))            # batch written in the simple style
RULES = sorted(int(d[4:]) for d in os.listdir(HERE) if d.startswith("rule"))


def m_copy(folder):        # the old (book) question put back -> not reworded, gate fails
    p = os.path.join(folder, "2_new_rows.json"); d = mt.load(p)
    d[0]["new"].pop("question", None); mt.save(p, d)


def m_old_number(folder):  # one number of the old question kept in the new one
    old = json.load(open(os.path.join(folder, "0_current_rows.json"), encoding="utf-8"))["rows"][0]["question"]
    kept = sorted(validate.originality.big_numbers(old), key=float)
    if not kept:                                       # the old question has no number above 3 to keep
        return False
    p = os.path.join(folder, "2_new_rows.json"); d = mt.load(p)
    d[0]["new"]["question"] += f" (Use {kept[-1]} as a check.)"; mt.save(p, d)


def m_double_backslash(folder):   # LaTeX written with doubled backslashes (the slip once made in rows 203 and 1263)
    p = os.path.join(folder, "2_new_rows.json"); d = mt.load(p)
    d[0]["new"]["question"] = d[0]["new"].get("question", "") + " " + chr(92) * 2 + "(x" + chr(92) * 2 + ")"; mt.save(p, d)


validate.ROOT = HERE
fails = sum(validate.run(n) for n in RULES)
bad = 0
for n in RULES:
    for mut in list(mt.MUTATIONS) + [m_copy, m_old_number, m_double_backslash]:
        tmp = tempfile.mkdtemp()
        dst = os.path.join(tmp, f"rule{n:02d}")
        shutil.copytree(os.path.join(HERE, f"rule{n:02d}"), dst)
        if mut(dst) is False:
            shutil.rmtree(tmp); continue
        validate.ROOT = tmp
        with contextlib.redirect_stdout(io.StringIO()):
            f = validate.run(n)
        bad += not f
        if not f:
            print(f"reword Rule {n} {mut.__name__} NOT CAUGHT")
        shutil.rmtree(tmp)
validate.ROOT = HERE
with contextlib.redirect_stdout(io.StringIO()):
    validate.run(RULES[0])
print(f"reword: {fails} failed checks | mutations: {'all caught' if not bad else f'{bad} NOT caught'}")
sys.exit(1 if fails or bad else 0)
