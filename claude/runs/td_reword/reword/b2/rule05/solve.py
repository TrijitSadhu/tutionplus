import importlib.util
_p = "C:/Users/newwe/Desktop/tution/tutionplus/claude/runs/td_reword/reword/b2/solve_b2.py"
_s = importlib.util.spec_from_file_location("solve_b2", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
solve = _m.solve
