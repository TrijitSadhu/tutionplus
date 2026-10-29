# Read-only: runs dump_rows.py for every rule of a batch. BATCH = {rule number: [row ids]}.
import os
ROOT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\permutation"
code = open(os.path.join(ROOT, "dump_rows.py"), encoding="utf-8").read()
for n, ids in globals()["BATCH"].items():
    exec(code, {"IDS": ids, "RULE": f"Rule {n}", "OUT_DIR": os.path.join(ROOT, f"rule{n:02d}")})
