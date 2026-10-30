# Builds sync_five_chapters.sql from the three-way result (claude/tools/threeway.json) for the 2026-10-30 push: the rewording of
# Alligation, Time & Distance, Percentage and P&C, and the whole Profit and Loss audit. For every "push" row of the five content
# tables, the full local row as JSON, inserted (new on live) or updated column by column (exists on live), then the id sequences are
# moved past the new ids. Refuses to build on any conflict or delete in a content table, on a pushed row of any other table, on a
# math row outside the five chapters, or on a card outside profit_n_loss. Same SQL shape as claude/runs/percentage/build_sync.py.
import json, subprocess
from django.db import connection

SCR = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools"
OUT = r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\profit\sync_five_chapters.sql"
TABLES = ["bank_rule_math", "bank_math", "bank_total_math", "genai_jsonimport", "genai_mathprompttemplate"]   # FK order
CHAPTERS = ("alligation_n_mixture", "time_n_distance", "percentage", "permutation_combination", "profit_n_loss")
TAG = "$SYNC7q$"
three = json.load(open(SCR + r"\threeway.json"))
assert not any(k.startswith(("CONFLICT", "push delete")) for t in TABLES for k in three.get(t, {})), "conflict or delete - stop"
assert set(t for t, kinds in three.items() if any(k.startswith("push") for k in kinds)) == set(TABLES), "a pushed row outside the content tables"


def remote(sql):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "tutionplus-vps", f"cd /tmp; sudo -u postgres psql -d tutionplus -At -c \"{sql}\""],
                          capture_output=True, text=True, check=True).stdout.split()


cur = connection.cursor()
cur.execute("SET timezone = 'UTC'")
out = ["SET timezone = 'UTC';"]
summary = []
for t in TABLES:
    ids = sorted(int(i) for i in three[t]["push (changed or added locally only)"])
    live_ids = set()
    for k in range(0, len(ids), 400):                        # keep each ssh command short
        live_ids |= set(map(int, remote(f"SELECT id FROM {t} WHERE id IN ({','.join(map(str, ids[k:k + 400]))})")))
    live_cols = remote(f"SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='{t}' ORDER BY 1")
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY 1", [t])
    assert [r[0] for r in cur.fetchall()] == live_cols, f"{t}: columns differ between local and live"
    if t == "bank_math":
        cur.execute("SELECT count(*) FROM bank_math WHERE id = ANY(%s) AND chapter <> ALL(%s)", [ids, list(CHAPTERS)])
        assert cur.fetchone()[0] == 0, "bank_math: a row outside the five chapters is in the push list"
    if t == "bank_rule_math":
        cur.execute("SELECT count(*) FROM bank_rule_math WHERE id = ANY(%s) AND chapter <> 'profit_n_loss'", [ids])
        assert cur.fetchone()[0] == 0, "bank_rule_math: a card outside profit_n_loss is in the push list"
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
