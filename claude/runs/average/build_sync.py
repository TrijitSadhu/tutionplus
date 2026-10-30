# Builds sync_average.sql from the three-way result (claude/tools/threeway.json) for the 2026-10-30 Average push: the 60 rewritten
# old rows 467-526 and the 238 new questions, the 43 cards #341-#383, total_math row 2, JsonImports #384-#434 and prompt #15. For
# every "push" row, the full local row as JSON, inserted (new on live) or updated column by column (exists on live), then the id
# sequences are moved past the new ids. Refuses to build on any conflict or delete, on a pushed row of any other table, or on a
# math row / card outside average. Same SQL shape as claude/runs/percentage/build_sync_misc.py.
import json, subprocess
from django.db import connection

SCR = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools"
OUT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\average\sync_average.sql"
TABLES = ["bank_rule_math", "bank_math", "bank_total_math", "genai_jsonimport", "genai_mathprompttemplate"]
TAG = "$SYNC7q$"
three = json.load(open(SCR + r"\threeway.json"))
assert not any(k.startswith(("CONFLICT", "push delete")) for t in three.values() for k in t), "conflict or delete - stop"
assert set(t for t, kinds in three.items() if any(k.startswith("push") for k in kinds)) == set(TABLES), "a pushed row outside the expected tables"


def remote(sql):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "tutionplus-vps", f"cd /tmp; sudo -u postgres psql -d tutionplus -At -c \"{sql}\""],
                          capture_output=True, text=True, check=True).stdout.split()


cur = connection.cursor()
cur.execute("SET timezone = 'UTC'")
out = ["SET timezone = 'UTC';"]
summary = []
for t in TABLES:
    ids = sorted(int(i) for i in three[t]["push (changed or added locally only)"])
    live_ids = set(map(int, remote(f"SELECT id FROM {t} WHERE id IN ({','.join(map(str, ids))})")))
    live_cols = remote(f"SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='{t}' ORDER BY 1")
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY 1", [t])
    assert [r[0] for r in cur.fetchall()] == live_cols, f"{t}: columns differ between local and live"
    if t in ("bank_math", "bank_rule_math"):
        cur.execute(f"SELECT count(*) FROM {t} WHERE id = ANY(%s) AND chapter <> 'average'", [ids])
        assert cur.fetchone()[0] == 0, f"{t}: a row outside average is in the push list"
    sets = ", ".join(f'"{c}" = r."{c}"' for c in live_cols if c != "id")
    n_ins = n_upd = 0
    for i in ids:
        cur.execute(f"SELECT to_jsonb(x)::text FROM {t} x WHERE id = %s", [i])
        js = cur.fetchone()[0]
        assert TAG not in js
        if i in live_ids:
            out.append(f"UPDATE {t} SET {sets} FROM jsonb_populate_record(NULL::{t}, {TAG}{js}{TAG}::jsonb) r WHERE {t}.id = {i};")
            n_upd += 1
        else:
            out.append(f"INSERT INTO {t} SELECT * FROM jsonb_populate_record(NULL::{t}, {TAG}{js}{TAG}::jsonb);")
            n_ins += 1
    out.append(f"SELECT setval(pg_get_serial_sequence('{t}', 'id'), (SELECT max(id) FROM {t}));")
    summary.append(f"{t}: {n_upd} updates, {n_ins} inserts (ids {ids[0]}-{ids[-1]})")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(summary))
print("statements:", len(out), "|", OUT)
