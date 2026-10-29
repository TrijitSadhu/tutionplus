# Step 1 (EXPORT=True): writes prompt #9 from the DB to prompt9_original.txt (\r\n -> \n) for make_prompt.py.
# Step 2 (SAVE=True): saves prompt_permutation.txt as a new MathPromptTemplate (not default, \r\n line endings
# like the others). Refuses to overwrite an existing template of the same name.
import os
from genai.models import MathPromptTemplate

HERE = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\permutation"
NAME = "permutation combination_detail method + theorem"
EXPORT = globals().get("EXPORT", False)
SAVE = globals().get("SAVE", False)

p9 = MathPromptTemplate.objects.get(id=9)
assert p9.name == "time and distance_detail method + theorem", p9.name
if EXPORT:
    open(os.path.join(HERE, "prompt9_original.txt"), "w", encoding="utf-8", newline="\n").write(p9.prompt_text.replace("\r\n", "\n"))
    print("exported prompt #9:", len(p9.prompt_text), "chars, CRLF:", p9.prompt_text.count("\r\n"))
if SAVE:
    assert not MathPromptTemplate.objects.filter(name=NAME).exists(), "template already exists"
    text = open(os.path.join(HERE, "prompt_permutation.txt"), encoding="utf-8").read()
    assert "\r" not in text
    t = MathPromptTemplate.objects.create(name=NAME, prompt_text=text.replace("\n", "\r\n"), is_default=False,
                                          created_by=p9.created_by)
    print("saved template", t.id, repr(t.name), "| default:", t.is_default, "| chars:", len(t.prompt_text))
    print("default is still:", [(x.id, x.name) for x in MathPromptTemplate.objects.filter(is_default=True)])
