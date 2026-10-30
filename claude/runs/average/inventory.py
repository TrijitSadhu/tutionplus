# Read-only inventory of the Average chapter: questions per rule, Traditional Method / Theorem coverage,
# key distribution, card health, duplicates, missing fields. Writes norule_questions.json + inventory.json next to it.
import re, json, os
from collections import Counter, defaultdict
from bank.models import math, rule_math

CH = "average"
OUT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\average"


def rnum(s):
    d = re.sub(r"\D", "", s or "")
    return int(d) if d else 10 ** 6


def plain(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()


qs = list(math.objects.filter(chapter=CH).select_related("rule"))
qs.sort(key=lambda m: (rnum(m.rule.rule_name) if m.rule else 10 ** 7, str(m.day), m.id))
cards = list(rule_math.objects.filter(chapter=CH).order_by("id"))
print("questions:", len(qs), "| with rule:", sum(1 for m in qs if m.rule_id), "| pages needed:", (len(qs) + 4) // 5)
print("cards:", len(cards))
names = Counter(c.rule_name for c in cards)
print("duplicate card names:", {k: v for k, v in names.items() if v > 1})
print("card names:", ", ".join(c.rule_name for c in sorted(cards, key=lambda c: rnum(c.rule_name))))
odd = [c.rule_name for c in cards if not re.fullmatch(r"Rule \d+", c.rule_name)]
print("card names not 'Rule N':", odd)

# card health
for c in sorted(cards, key=lambda c: rnum(c.rule_name)):
    h = c.rule_html or ""
    issues = []
    if '\\"' in h or "\\\\(" in h:
        issues.append("escaped-json")
    if h.count("\\(") != h.count("\\)"):
        issues.append("unbalanced \\( \\)")
    if h.count("\\[") != h.count("\\]"):
        issues.append("unbalanced \\[ \\]")
    if "$" in h:
        issues.append("$-math")
    outside = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", "", h, flags=re.S)
    if re.search(r"\\(frac|times|div|cdot|sqrt)", outside):
        issues.append("latex outside math")
    if len(plain(h)) < 40:
        issues.append("very short")
    used = sum(1 for m in qs if m.rule_id == c.id)
    print(f"  {c.rule_name:8} id={c.id:5} len={len(h):5} used_by={used:3} {'; '.join(issues)} | {plain(h)[:90]}")

per = defaultdict(list)
for m in qs:
    per[m.rule.rule_name if m.rule else "(no rule)"].append(m)


def has_trad(m):
    return "traditional method" in (m.solution or "").lower()


def has_thm(m):
    return "theorem" in (m.solution or "").lower()


print("\nper rule:")
page = 0
for r in sorted(per, key=rnum):
    ms = per[r]
    a = page // 5 + 1
    page += len(ms)
    b = (page - 1) // 5 + 1
    keys = Counter(str(m.ans) for m in ms)
    print(f"{r:10} n={len(ms):3} pages {a:2}-{b:2} | trad {sum(map(has_trad, ms)):3} | thm {sum(map(has_thm, ms)):3} "
          f"| shortcut {sum(bool((m.shortcut or '').strip()) for m in ms):3} | rbe {sum(bool((m.rule_based_explanation or '').strip()) for m in ms):3} "
          f"| keys {dict(sorted(keys.items()))} | days {sorted(set(str(m.day) for m in ms))[:2]}{'...' if len(set(str(m.day) for m in ms)) > 2 else ''}")

print("\nglobal:")
print("  keys:", Counter(str(m.ans) for m in qs))
print("  times:", Counter(m.time for m in qs))
print("  llm_used:", Counter(m.llm_used for m in qs))
print("  from_json:", Counter(bool(m.from_json) for m in qs))
print("  difficult_level:", Counter(m.difficult_level for m in qs))
bad_opts = [m.id for m in qs if not all((getattr(m, k) or "").strip() for k in "abcd")]
print("  questions with an empty option:", bad_opts)
bad_ans = [m.id for m in qs if str(m.ans) not in ("1", "2", "3", "4")]
print("  bad ans values:", bad_ans)
dup_opt = [m.id for m in qs if len({plain(getattr(m, k)) for k in "abcd"}) < 4]
print("  questions with duplicate options:", dup_opt)
draft = [m.id for m in qs if re.search(r"\b(Wait|mistakenly|Let me re|Hmm|Actually,)\b", plain(m.solution) + plain(m.shortcut) + plain(m.rule_based_explanation))]
print("  LLM draft text:", draft)
rawlt = [m.id for m in qs if re.search(r"\\\([^)]*<[^)]*\\\)", (m.solution or "") + (m.question or ""))]
print("  raw < inside math:", rawlt[:30])
empty_sol = [m.id for m in qs if len(plain(m.solution)) < 20]
print("  empty/short solution:", empty_sol)

# duplicates by normalised question text
norm = defaultdict(list)
for m in qs:
    norm[re.sub(r"[^a-z0-9]", "", plain(m.question).lower())].append(m.id)
dups = [v for v in norm.values() if len(v) > 1]
print("  duplicate questions:", dups)

nr = per.get("(no rule)", [])
json.dump([{"id": m.id, "day": str(m.day), "q": plain(m.question), "opts": [plain(getattr(m, k)) for k in "abcd"], "ans": m.ans,
            "trad": has_trad(m)} for m in nr], open(os.path.join(OUT, "norule_questions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({r: [{"id": m.id, "day": str(m.day), "q": plain(m.question)[:300], "ans": m.ans, "trad": has_trad(m)} for m in ms]
           for r, ms in per.items()}, open(os.path.join(OUT, "inventory.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("no-rule questions:", len(nr))
