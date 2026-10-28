"""Validates the misc/ruleNN folders (gen_misc.py output) and mutation-tests the validator on scratch copies of them.
Usage: python misc_check.py"""
import contextlib, io, os, shutil, sys, tempfile
import validate
import mutation_test as mt

MISC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "misc")
RULES = sorted(int(d[4:]) for d in os.listdir(MISC) if d.startswith("rule"))

validate.ROOT = MISC
fails = sum(validate.run(n) for n in RULES)

bad = 0
for n in RULES:
    for mut in mt.MUTATIONS:
        tmp = tempfile.mkdtemp()
        dst = os.path.join(tmp, f"rule{n:02d}")
        shutil.copytree(os.path.join(MISC, f"rule{n:02d}"), dst)
        if mut(dst) is False:
            shutil.rmtree(tmp)
            continue
        validate.ROOT = tmp
        with contextlib.redirect_stdout(io.StringIO()):
            f = validate.run(n)
        bad += not f
        if not f:
            print(f"misc Rule {n} {mut.__name__} NOT CAUGHT")
        shutil.rmtree(tmp)
validate.ROOT = MISC
with contextlib.redirect_stdout(io.StringIO()):
    sum(validate.run(n) for n in RULES)             # rewrite the real reports last
print("validation failures:", fails, "| mutations not caught:", bad)
sys.exit(1 if fails or bad else 0)
