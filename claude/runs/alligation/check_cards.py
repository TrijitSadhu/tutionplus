"""Read-only: checks the rule cards stored in ruleNN/0_current_rows.json. Usage: python check_cards.py 5 6 7"""
import json, os, re, sys
from validate import html_ok, latex_ok, raw_lt

ROOT = os.path.dirname(os.path.abspath(__file__))
MATH = re.compile(r"\\\(.*?\\\)|\\\[.*?\\\]", re.S)
STRAY = re.compile(r"[\\](?:frac|text|times|left|right|div)\b[^<]{0,30}")
for n in map(int, sys.argv[1:]):
    h = json.load(open(os.path.join(ROOT, f"rule{n:02d}", "0_current_rows.json"), encoding="utf-8"))["rule_card"]["rule_html"]
    stray = STRAY.findall(MATH.sub("", h))
    print(f"Rule {n}: html_ok={html_ok(h)} latex_ok={latex_ok(h)} raw_lt={raw_lt(h)} | LaTeX outside math: {stray}")
