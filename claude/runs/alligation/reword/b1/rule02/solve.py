# Rule 2 rows 1641-1649 were inserted from the payload keys E1-E9; the book solver knows them by those keys.
import importlib.util
_p = "C:/Users/newwe/Desktop/tution/tutionplus/claude/runs/alligation/rule02/solve.py"
_s = importlib.util.spec_from_file_location("base_solve_02", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
KEY = {1640 + i: f"E{i}" for i in range(1, 10)}


def solve(rid, q):
    try:
        return _m.solve(KEY.get(rid, rid), q)
    except Exception:                      # a question this solver can not read -> the answer check fails
        return ("unsolved", q[:40])
