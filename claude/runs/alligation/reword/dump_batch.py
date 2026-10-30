# Read-only: dumps the Alligation rows to be reworded into reword/<SUB>/ruleNN (one folder per rule). BATCH = {rule: [row ids]},
# SUB = batch folder. Same as claude/runs/time_work/reword/dump_batch.py, with the Alligation dump_rows.py.
import os
AL = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\alligation"
code = open(os.path.join(AL, "dump_rows.py"), encoding="utf-8").read()
for n, ids in globals()["BATCH"].items():
    exec(code, {"IDS": ids, "RULE": f"Rule {n}", "OUT_DIR": os.path.join(AL, "reword", globals()["SUB"], f"rule{n:02d}")})
