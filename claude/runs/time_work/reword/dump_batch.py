# Read-only: dumps the rows to be reworded into reword/<SUB>/ruleNN (one folder per rule). BATCH = {rule: [row ids]}, SUB = batch folder.
import os
TW = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\time_work"
code = open(os.path.join(TW, "dump_rows.py"), encoding="utf-8").read()
for n, ids in globals()["BATCH"].items():
    exec(code, {"IDS": ids, "RULE": f"Rule {n}", "OUT_DIR": os.path.join(TW, "reword", globals()["SUB"], f"rule{n:02d}")})
