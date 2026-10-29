# Builds sync_time_work_reword.sql from the three-way result (claude/tools/threeway.json) for the Time & Work rewording push
# (2026-10-30): every "push" row must be a bank_math row of the time_n_work chapter that already exists on live, and is updated
# column by column from the full local row (jsonb_populate_record). Refuses to build on any conflict, delete or insert, on a push
# in any other table, or on a row outside time_n_work. Same SQL shape as claude/runs/permutation/build_sync.py.
import json, subprocess
from django.db import connection

SCR = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools"
OUT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\time_work\reword\sync_time_work_reword.sql"
T = "bank_math"
TAG = "$SYNC7q$"
three = json.load(open(SCR + r"\threeway.json"))
assert not any(k.startswith(("CONFLICT", "push delete")) for kinds in three.values() for k in kinds), "conflict or delete - stop"
pushed = {t for t, kinds in three.items() if any(k.startswith("push") for k in kinds)}
assert pushed == {T}, f"pushes outside {T}: {pushed}"


def remote(sql):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "tutionplus-vps", f"cd /tmp; sudo -u postgres psql -d tutionplus -At -c \"{sql}\""],
                          capture_output=True, text=True, check=True).stdout.split()


ids = sorted(int(i) for i in three[T]["push (changed or added locally only)"])
live_ids = set(map(int, remote(f"SELECT id FROM {T} WHERE id IN ({','.join(map(str, ids))})")))
assert live_ids == set(ids), f"rows missing on live (would be inserts): {sorted(set(ids) - live_ids)}"
live_cols = remote(f"SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='{T}' ORDER BY 1")
cur = connection.cursor()
cur.execute("SET timezone = 'UTC'")
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY 1", [T])
assert [r[0] for r in cur.fetchall()] == live_cols, "columns differ between local and live"
cur.execute(f"SELECT id, chapter FROM {T} WHERE id = ANY(%s) AND chapter <> 'time_n_work'", [ids])
outside = cur.fetchall()
assert not outside, f"rows outside time_n_work in the push list: {outside[:10]}"
cur.execute(f"SELECT count(*) FROM {T} WHERE chapter = 'time_n_work'")
n_ch = cur.fetchone()[0]

sets = ", ".join(f'"{c}" = r."{c}"' for c in live_cols if c != "id")
out = ["SET timezone = 'UTC';"]
for i in ids:
    cur.execute(f"SELECT to_jsonb(x)::text FROM {T} x WHERE id = %s", [i])
    js = cur.fetchone()[0]
    assert TAG not in js
    out.append(f"UPDATE {T} SET {sets} FROM jsonb_populate_record(NULL::{T}, {TAG}{js}{TAG}::jsonb) r WHERE {T}.id = {i};")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"{T}: {len(ids)} updates, 0 inserts (ids {ids[0]}-{ids[-1]}); time_n_work rows locally: {n_ch}")
print("statements:", len(out), "|", OUT)
