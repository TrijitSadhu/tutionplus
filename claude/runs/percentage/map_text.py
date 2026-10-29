# Text-layer first pass of the book map: per rule, the PDF page, number of answer entries, and which DB rows match
# which part of the rule (example or exercise) by fuzzy word overlap. Read-only; refine from the page images.
import re, json
from difflib import SequenceMatcher
t = open("pdf_text.txt", encoding="utf-8").read()
pages = {}
for m in re.finditer(r"=== PAGE (\d+) ===", t):
    pages[m.start()] = int(m.group(1))
def page_at(pos):
    return max((p for s, p in pages.items() if s <= pos), default=1)
heads = [(m.start(), int(m.group(1))) for m in re.finditer(r"\nRule (\d+)\b", t)]
heads.insert(7, (t.find("Rule 7 7") + 300, 8)) if False else None
spans = []
for i, (s, n) in enumerate(heads):
    e = heads[i + 1][0] if i + 1 < len(heads) else len(t)
    spans.append((n, s, e))
def words(s):
    s = re.sub(r"\bo f\b", "of", s.lower())
    return re.findall(r"[a-z]{3,}", s)
rows = json.load(open("norule_questions.json", encoding="utf-8"))
out = {}
for r in rows:
    qw = words(r["q"])[:25]
    best = (0, None)
    for n, s, e in spans:
        body = words(t[s:e])
        joined = " ".join(body)
        q = " ".join(qw)
        sm = SequenceMatcher(None, q, joined, autojunk=False)
        blk = sum(b.size for b in sm.get_matching_blocks() if b.size >= 6)
        sc = blk / max(1, len(q))
        if sc > best[0]:
            best = (sc, n)
    out[r["id"]] = best
    print(r["id"], "rule", best[1], f"{best[0]:.2f}", "|", r["q"][:80])
