"""Percentage helpers: the prompt #12 solution layout (same as the Alligation runs) plus formatting."""
import os, re, sys
from fractions import Fraction as F
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import S, card, frac, rbe, shortcut, solution, steps, tex  # noqa: E402,F401

CHAPTER = "percentage"
LLM = "Claude Opus 5.5 (2026-10-28)"


def pct(v):
    """Percentage as a mixed number: 20, 12\\frac{1}{2}, 33\\frac{1}{3}."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    whole, rem = divmod(v.numerator, v.denominator)
    return (str(whole) if whole else "") + rf"\frac{{{rem}}}{{{v.denominator}}}"


def new_question(rule_n, question, opts, pos, sol, rb, sc, exam=""):
    """One question in the JsonImport payload shape (same keys the generation page produces)."""
    assert len(opts) == 4 and len(set(opts)) == 4
    return {"chapter": CHAPTER, "rule_name": f"Rule {rule_n}", "question": question,
            "a": opts[0], "b": opts[1], "c": opts[2], "d": opts[3], "correct_answer": pos,
            "solution": tidy(sol), "rule_based_explanation": tidy(rb), "shortcut": tidy(sc),
            "validation_status": "validated", "llm_used": LLM, "exam_and_year": exam, "from_json": True}


def regen_entry(row, g, card_id, extra_new=None):
    """2_new_rows.json entry for an existing row: old values (for the stale check) + regenerated fields."""
    llm = row["llm_used"] or ""
    new = {"solution": tidy(g["solution"]), "rule_based_explanation": tidy(g["rbe"]), "shortcut": tidy(g["shortcut"]),
           "rule_id": card_id, "llm_used": llm if LLM_NOTE in llm else (llm + "; " if llm else "") + LLM_NOTE}
    new.update(extra_new or {})
    ans = g["answer"]
    return {"id": row["id"], "answer": [ans[0], [str(x) for x in ans[1]] if isinstance(ans[1], tuple) else str(ans[1])],
            "old": {k: row[k] for k in list(new) + ["ans"]}, "new": new}

LLM_NOTE = "solution regenerated (Theorem + Traditional Method + Specified Rule) by Claude Opus 5.5 (2026-10-28)"


def tidy(s):
    """The site draws back-to-back display equations on one line, so end every \\[ ... \\] with a <br>."""
    return re.sub(r"\\\](?!<br>|<hr>|</)", r"\\]<br>", s)


def money(v):
    """Price as written in questions: 12, 4.50, 3.10."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):.2f}"


def ratio(a, b):
    """Two Fractions -> the same ratio in lowest whole numbers."""
    a, b = F(a), F(b)
    scale = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    x, y = int(a * scale), int(b * scale)
    g = gcd(x, y)
    return x // g, y // g


def rtex(r):
    return f"{r[0]} : {r[1]}"


def ratio_steps(top, bottom):
    """LaTeX chain \\frac{0.35}{0.15} = \\frac{35}{15} = \\frac{7}{3} for two differences."""
    top, bottom = F(top), F(bottom)
    chain = [rf"\frac{{{tex(top)}}}{{{tex(bottom)}}}"]
    if top.denominator != 1 or bottom.denominator != 1:
        for k in (10, 100, 1000):
            if (top * k).denominator == 1 and (bottom * k).denominator == 1:
                chain.append(rf"\frac{{{int(top * k)}}}{{{int(bottom * k)}}}")
                break
    x, y = ratio(top, bottom)
    if chain[-1] != rf"\frac{{{x}}}{{{y}}}":
        chain.append(rf"\frac{{{x}}}{{{y}}}")
    return " = ".join(chain)


def cross_table(c, m, d, unit, left="Cheaper", right="Dearer"):
    """The alligation cross written as a table (prompt #10 visual)."""
    return ('<table border="1" cellpadding="4">'
            f"<tr><th>{left} (Rs {money(c)} {unit})</th><th>Mean (Rs {money(m)} {unit})</th><th>{right} (Rs {money(d)} {unit})</th></tr>"
            rf"<tr><td>\({money(d)} - {money(m)} = {tex(F(d) - F(m))}\)</td><td></td><td>\({money(m)} - {money(c)} = {tex(F(m) - F(c))}\)</td></tr>"
            "</table>")
