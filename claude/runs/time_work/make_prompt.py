# Builds the Time and Work prompt from prompt #9 ("time and distance_detail method + theorem"):
# the shared rules stay word for word; every Time and Distance-specific block is swapped for a
# Time and Work one. Reads prompt9_original.txt (exported from the DB by save_prompt.py), writes
# prompt_time_work.txt next to this file (no DB access).
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "prompt9_original.txt"), encoding="utf-8").read()


def swap(text, old, new):
    assert text.count(old) == 1, f"expected exactly one {old[:60]!r}"
    return text.replace(old, new)


def swap_block(text, start, end, new):
    i = text.index(start)
    j = text.index(end, i)
    assert text.count(start) == 1
    return text[:i] + new + text[j:]


p = src
p = swap(p, "merely because they belong to the Time and Distance chapter.",
         "merely because they belong to the Time and Work chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR TIME AND WORK

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- One-day work table (each worker, days alone, work done in 1 day)
- Efficiency / units table (total work taken as the LCM of the days, units per day for each worker)
- Man-days (or man-hours) table for groups of men, women and boys
- Work-done-in-stages table (who works, for how many days, work done, work left)
- Timeline for workers who join or leave part-way
- Alternate-day (or alternate-hour) work cycle table
- Food / provisions table (men, days, man-days of food used and left)

For example (one-day work table):

<table border="1" cellpadding="4">
<tr><th>Worker</th><th>Days alone</th><th>Work in 1 day</th></tr>
<tr><td>A</td><td>\(x\)</td><td>\(\frac{1}{x}\)</td></tr>
<tr><td>B</td><td>\(y\)</td><td>\(\frac{1}{y}\)</td></tr>
<tr><td>A + B</td><td>\(\frac{xy}{x+y}\)</td><td>\(\frac{1}{x}+\frac{1}{y}\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ TIME AND WORK-SPECIFIC CHECKS (MANDATORY)

- Work done = rate \(\times\) time. A worker who finishes the whole work in \(x\) days does \(\frac{1}{x}\) of it in one day; rates of people working together ADD, times never add.
- "A is \(n\) times as fast (as efficient, as good a workman)" means A's one-day work is \(n\) times B's, so A takes \(\frac{1}{n}\) of B's time.
- "A takes half as long as B" means A's time is \(\frac{1}{2}\) of B's, so A's rate is twice B's.
- "B would take \(n\) times as long as A and C together" means \(\text{B's rate} = \frac{1}{n}\times\) (A + C)'s rate.
- When men, women and boys (or children) appear together, convert everyone to one unit (e.g. boys) using the given equivalence before using \(M_1D_1 = M_2D_2\).
- Include hours per day and the amount of work in the group formula: \(M_1D_1T_1W_2 = M_2D_2T_2W_1\). When the efficiency of the two groups differs, include it as well: \(M_1D_1T_1E_1W_2 = M_2D_2T_2E_2W_1\).
- When someone leaves or joins part-way, split the work into stages and make the stages add up to 1 (the whole work). Read carefully whether a worker leaves "after \(a\) days" (from the start) or "\(a\) days before the work is completed" (counted back from the end).
- In alternate-day (or alternate-hour) work, the last day may be a part-day: finish the remainder at that worker's rate and do not round up to a whole day unless the question asks for it.
- A negative or zero time means the data are inconsistent; re-read the question instead of forcing an answer.
- Give the answer in the unit the question asks (days, hours, number of men, clock time, fraction of the work) and in the order asked (e.g. A, B, C or man : boy).
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a two-worker problem:

Let the whole work be 1 unit.

Write the work each person does in one day:

\[
\text{A's 1-day work}=\frac{1}{x},\qquad \text{B's 1-day work}=\frac{1}{y}
\]

Add the rates of the people who work together:

\[
\text{(A + B)'s 1-day work}=\frac{1}{x}+\frac{1}{y}
\]

Then the time to finish the whole work is

\[
\text{Time}=\frac{1}{\text{(A + B)'s 1-day work}}
\]

For other Time and Work problems, use the natural mathematical relationship required by the question (work done in each stage adding up to 1, man-days of work or food, units of work per day, and so on).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
x=\text{days A takes alone}
\]

\[
y=\text{days B takes alone}
\]

\[
W=\text{the whole work (taken as 1)}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> If A can do a piece of work in \(x\) days and B can do it in \(y\) days, then A and B working together will do the same work in

\[
\frac{xy}{x+y} \text{ days}
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

A alone takes 10 days and B alone takes 15 days. Let the whole work be 1.

<br><br>

<b>Step 2: Find the work done in one day.</b><br>

\[
\text{A's 1-day work}=\frac{1}{10},\qquad \text{B's 1-day work}=\frac{1}{15}
\]

\[
\text{(A + B)'s 1-day work}=\frac{1}{10}+\frac{1}{15}=\frac{3+2}{30}=\frac{1}{6}
\]

<br><br>

<b>Step 3: Find the time for the whole work.</b><br>

\[
\text{Time}=\frac{1}{\frac{1}{6}}=6 \text{ days}
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
x=10,\qquad y=15
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\text{Time}=\frac{xy}{x+y}
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{10\times 15}{10+15}=\frac{150}{25}=6 \text{ days}
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(6\) days</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
\frac{xy}{x+y}=\frac{10\times 15}{10+15}=6
\]

<br>

∴ <b>Final Answer: \(6\) days</b>.

</div>

""")

p = swap(p, '"chapter":"time_and_distance"', '"chapter":"time_n_work"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Time and Work rule.\n"
         "- Follow every TIME AND WORK-SPECIFIC CHECK (rates add, convert men/women/boys to one unit, stages add up to the whole work, answer in the unit and order asked).")

for word in ("Distance", "distance", "speed", "km/hr", "Speed", "journey"):
    assert word not in p, f"left-over Time and Distance text: {word}"
open(os.path.join(HERE, "prompt_time_work.txt"), "w", encoding="utf-8").write(p)
print("prompt_time_work.txt:", len(p), "chars | prompt #9:", len(src), "chars")
