"""Shared building blocks for the Time and Work generators (copied from td_new; same layout as prompt #11 asks for)."""
from fractions import Fraction as F

LLM = "Claude Opus 5.5 (2026-10-28)"
S = "<br><br>"


def tex(v):
    """Fraction -> LaTeX mixed number, the book's style for days: 12, 9\\frac{3}{5}, 12\\frac{6}{7}."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    if v < 0:                                       # divmod floors negatives: -21/2 would print as -11 1/2
        return "-" + tex(-v)
    whole, rem = divmod(v.numerator, v.denominator)
    return (f"{whole}" if whole else "") + rf"\frac{{{rem}}}{{{v.denominator}}}"


def frac(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def timephrase(h):
    """Hours (Fraction) -> '\\(3.5\\) hours' / '\\(40\\) minutes' / '\\(1\\) hour \\(15\\) minutes'."""
    h = F(h)
    mins = h * 60
    assert mins.denominator == 1, h
    whole, rest = divmod(int(mins), 60)
    if whole == 0:
        return rf"\({rest}\) minutes"
    if rest == 0:
        return rf"\({whole}\) hour" + ("" if whole == 1 else "s")
    if rest == 30 and whole > 1:
        return rf"\({tex(h)}\) hours"
    return rf"\({whole}\) hour" + ("" if whole == 1 else "s") + rf" \({rest}\) minutes"


def solution(theorem, trad, rule, final):
    return ('<div style="display:block;text-align:justify;border:1px solid;padding:12px">'
            f"<b>Theorem :</b> {theorem}<hr><b>Traditional Method :</b><br><br>{trad}<hr>"
            f"<b>Using the Specified Rule :</b><br><br>{rule}<br><br>"
            "<b>Verification:</b> Both methods give the same result.<br><br>"
            f"∴ <b>Final Answer: {final}</b></div>")


def rbe(steps_, final):
    body = "".join(f"<b>Step {i}:</b> {s}<br>" for i, s in enumerate(steps_, 1))
    return f"Using the specified Rule:<br>{body}<b>Final Answer:</b> {final}"


def shortcut(body, final):
    return ('<div style="display:block;text-align:justify;border:0px solid;padding:10px">'
            f'<span style="display:table">Applying the specified Rule:</span>{body}<br>∴ <b>Final Answer: {final}</b></div>')


def steps(*items):
    return S.join(f"<b>Step {i}: {title}</b><br>{body}" for i, (title, body) in enumerate(items, 1))


def pick(ans, candidates, n=3):
    """First n candidates that differ from the answer and from each other (and are positive)."""
    out = []
    for c in candidates:
        if c > 0 and c != ans and c not in out:
            out.append(c)
        if len(out) == n:
            return out
    raise ValueError(f"not enough distinct distractors for {ans}: {candidates}")


def place(correct, wrong, pos):
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (correct, wrong)
    opts = list(wrong)
    opts.insert(pos - 1, correct)
    return opts


def q(question, opts, pos, sol, rb, sc, exam=""):
    return {"chapter": "time_n_distance", "question": question,
            "a": opts[0], "b": opts[1], "c": opts[2], "d": opts[3], "correct_answer": pos,
            "solution": sol, "rule_based_explanation": rb, "shortcut": sc,
            "validation_status": "validated", "llm_used": LLM, "exam_and_year": exam, "from_json": True}


def card(n, title, statement, formula, visual, intuition, pattern, example, mistake):
    lis = "".join(f"<li>{a} → <span>\\( {b} \\)</span></li>" for a, b in visual)
    return (f"<section class='rule-card'><h2>Rule {n}: {title}</h2>"
            f"<div class='rule-statement'><p>{statement}</p></div>"
            f"<div class='rule-formula'><p><strong>Formula:</strong></p><p>{formula}</p></div>"
            f"<div class='rule-visual'><p><strong>Visual Breakdown:</strong></p><ul>{lis}</ul></div>"
            f"<div class='rule-intuition'><p><strong>Concept (Why it works):</strong> {intuition}</p></div>"
            f"<div class='rule-pattern'><p><strong>Pattern Recognition:</strong></p><p>{pattern}</p></div>"
            f"<div class='rule-example'><p><strong>Worked Example:</strong></p><p>{example}</p></div>"
            f"<div class='rule-mistake'><p><strong>Common Mistake:</strong></p><p>{mistake}</p></div></section>")


def kmh(v):
    return rf"\({tex(v)}\) km/hr"


def km(v):
    return rf"\({tex(v)}\) km"
