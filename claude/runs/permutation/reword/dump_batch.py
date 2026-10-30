# Read-only: dumps the P&C rows to be reworded into reword/<SUB>/ruleNN (one folder per rule). BATCH = {rule: [row ids]},
# SUB = batch folder. Same as claude/runs/alligation/reword/dump_batch.py, with the P&C dump_rows.py.
import os
PC = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\permutation"
code = open(os.path.join(PC, "dump_rows.py"), encoding="utf-8").read()
for n, ids in globals()["BATCH"].items():
    exec(code, {"IDS": ids, "RULE": f"Rule {n}", "OUT_DIR": os.path.join(PC, "reword", globals()["SUB"], f"rule{n:02d}")})
