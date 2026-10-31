#!/bin/bash
# Example apply script (Simple Interest Rules 34-39): backup, cards, old rows, new questions, page counter, compare, crawl. Copy it
# for a new batch, change the rule lists / file names, run it in the background with set -e -o pipefail (a pipe hides errors otherwise).
set -e -o pipefail
cd /c/Users/newwe/Desktop/tution/tutionplus/django/django_project
PY="../../env/Scripts/python.exe -X utf8 manage.py shell -c"
D='C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\simple_interest'
T='C:\Users\newwe\Desktop\tution\tutionplus\claude\tools'
run() { $PY "$1" 2>&1 | { grep -vE "^\[(CONFIG|OK)\]" || true; }; }
echo "== backup"; run "exec(open(r'$T\backup_db.py').read(), {})"
echo "== cards"; run "exec(open(r'$D\apply_cards.py').read(), {'RULES': [34, 35, 36, 37, 38, 39], 'DO_UPDATE': True})"
for n in 34 35 37 38 39; do
  echo "== rows rule$n"; run "exec(open(r'$D\apply_rows.py').read(), {'RUN_DIR': r'$D\rule$n', 'LABEL': 'audit_rule$n', 'DO_UPDATE': True})"
done
for n in 34 35 36 37 38 39; do
  echo "== insert Rule $n"; run "from datetime import date; exec(open(r'$D\save_and_insert.py').read(), {'N': $n, 'DAY': date(2026, 10, 31), 'DO_INSERT': True})"
done
echo "== page counter"; run "exec(open(r'$D\save_page_counters.py').read(), {'DO_UPDATE': True, 'BACKUP': r'C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\total_math_before_si_rule_34_39.json'})"
echo "== compare"; run "exec(open(r'$D\compare_applied.py').read(), {'RULES': [34, 35, 36, 37, 38, 39]})"
echo "== crawl"; run "exec(open(r'$T\check_order.py').read(), {'CHAPTERS': ['simple_interest']})"
echo "== done"
