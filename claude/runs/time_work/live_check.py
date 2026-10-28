# Read-only: crawls the LIVE chapter pages (same checks as claude/tools/check_order.py, against the live site) for the chapters
# in CHAPTERS: every question exactly once, rule numbers never go back, rule-less last, no "None" option, no display math in options.
import re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from bank.models import math

BASE = globals()["BASE"]                     # the live site URL (claude/LIVE_SERVER.local.md)
for chapter in globals().get("CHAPTERS", ["time_n_work", "profit_n_loss"]):
    rows = {m.id: m for m in math.objects.filter(chapter=chapter).select_related("rule")}
    pages = (len(rows) + 4) // 5

    def fetch(p):
        return p, urllib.request.urlopen(f"{BASE}/math/{chapter}/{p}/", timeout=60).read().decode("utf-8")

    with ThreadPoolExecutor(6) as ex:
        htmls = dict(ex.map(fetch, range(1, pages + 1)))
    seen, none_opts, disp = [], 0, 0
    for p in range(1, pages + 1):
        h = htmls[p]
        seen += [int(i) for i in re.findall(r'data-math-id="(\d+)"', h)]
        none_opts += len(re.findall(r">None</span>", h))
        disp += len(re.findall(r'id="matho[a-e]-\d+">[^<]*\\\[', h))
    nums = [int(rows[i].rule.rule_name.split()[-1]) if i in rows and rows[i].rule else None for i in seen]
    ruled = [n for n in nums if n is not None]
    first_none = nums.index(None) if None in nums else len(nums)
    print(f"LIVE {chapter}: {pages} pages | shown {len(seen)} of {len(rows)} | duplicates {len(seen) - len(set(seen))} | missing {len(set(rows) - set(seen))} "
          f"| rule order never goes back: {ruled == sorted(ruled)} | rule-less all at the end: {all(n is None for n in nums[first_none:])} "
          f"| 'None' options: {none_opts} | display math in options: {disp}")
