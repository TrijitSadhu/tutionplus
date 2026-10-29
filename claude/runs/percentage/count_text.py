# Text-layer count per rule: highest exercise number seen, answer letters parsed, number of "Ex" worked examples. Read-only.
import re
t = open("pdf_text.txt", encoding="utf-8").read()
mi = t.find("\nMiscellaneous")
heads = [(m.start(), int(m.group(1))) for m in re.finditer(r"\nRule (\d+)\b", t[:mi])]
for i, (s, n) in enumerate(heads):
    e = heads[i + 1][0] if i + 1 < len(heads) else mi
    body = t[s:e]
    ex_part = body.split("Exercise", 1)[1] if "Exercise" in body else ""
    q_part, _, a_part = ex_part.partition("Answers")
    nums = [int(x) for x in re.findall(r"(?m)^\s*(\d{1,2})\s*[\.\^,]", q_part)]
    seq = 0
    for x in nums:
        if x == seq + 1:
            seq = x
    ans = re.findall(r"(\d{1,2}|[lLI:•i])\s*[\.,]?\s*(?:\(i\))?\s*([a-d])\b", a_part)
    exs = len(re.findall(r"(?m)^\s*Ex\.?\s*\d*\s*[:;.]", body))
    pg = t[:s].count("=== PAGE")
    print(f"Rule {n:2} p{pg:2} examples {exs} | exercises {seq:2} | answers {len(ans):2}: {' '.join(a for _, a in ans)}")
