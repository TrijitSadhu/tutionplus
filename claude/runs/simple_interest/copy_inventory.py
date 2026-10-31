"""One-off: copies claude/runs/ratio/inventory.py here with the chapter and output folder switched to Simple Interest."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "ratio", "inventory.py"), encoding="utf-8").read()
B = chr(92)
swaps = [('CH = "ratio_n_proportion"', 'CH = "simple_interest"'),
         ("claude" + B + "runs" + B + "ratio" + '"', "claude" + B + "runs" + B + "simple_interest" + '"'),
         ("Ratio and Proportion chapter", "Simple Interest chapter")]
for a, b in swaps:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
dst = os.path.join(HERE, "inventory.py")
assert not os.path.exists(dst)
open(dst, "w", encoding="utf-8").write(src)
print("written", dst)
