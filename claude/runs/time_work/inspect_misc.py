# Read-only: page counter, option e on the ans=5 rows, a sample solution, prompt templates and JsonImports for the chapter.
import re
from bank.models import math, total_math
from genai.models import MathPromptTemplate, JsonImport

t = total_math.objects.get(id=2)
print("total_time_n_work_page =", getattr(t, "total_time_n_work_page", "(no field)"))
for i in (261, 262):
    m = math.objects.get(id=i)
    print(i, "ans", m.ans, "| e =", repr(m.e)[:80])
m = math.objects.get(id=1229)
print("--- sample solution 1229 ---")
print(m.solution[:1500])
print("--- shortcut ---")
print((m.shortcut or "")[:400])
print("--- rbe ---")
print((m.rule_based_explanation or "")[:400])
print("--- old 181 solution ---")
print(math.objects.get(id=181).solution[:600])
print("--- prompts ---")
for p in MathPromptTemplate.objects.order_by("id"):
    print(p.id, repr(p.name)[:70], "default" if p.is_default else "", len(p.template or "") if hasattr(p, "template") else "")
print("--- JsonImports for time_n_work ---")
for j in JsonImport.objects.filter(to_table="math").order_by("id"):
    s = str(j.json_data)[:20000]
    if "time_n_work" in s:
        print(j.id, getattr(j, "created_at", ""), len(s))
