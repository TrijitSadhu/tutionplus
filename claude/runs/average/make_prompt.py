# Builds the Average prompt from prompt #9 ("time and distance_detail method + theorem"): the shared rules stay word for word;
# every Time and Distance-specific block is swapped for an Average one. Reads prompt9_original.txt (copied from
# claude/runs/profit/), writes prompt_average.txt next to this file (no DB access). Same swaps as claude/runs/profit/make_prompt.py.
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
         "merely because they belong to the Average chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR AVERAGE

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Sum table (number of items, their average, their sum - for each group and for all of them together)
- Before / after table (the group before a member joins, leaves or is replaced, and after)
- Pass / fail table (candidates, average marks and total marks of each part)
- Overlapping-groups table (first part, middle item, last part - for "the average of the first six and of the last six")
- Distance-time table for average speed (each part's distance, speed and time, and the whole journey)
- A short list of the numbers in a series (consecutive, odd, even, squares, cubes) with their sum

For example (sum table for two groups put together):

<table border="1" cellpadding="4">
<tr><th></th><th>Number</th><th>Average</th><th>Sum</th></tr>
<tr><td>Group A</td><td>\(m\)</td><td>\(x\)</td><td>\(mx\)</td></tr>
<tr><td>Group B</td><td>\(n\)</td><td>\(y\)</td><td>\(ny\)</td></tr>
<tr><td>All</td><td>\(m+n\)</td><td>\(\frac{mx+ny}{m+n}\)</td><td>\(mx+ny\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ AVERAGE-SPECIFIC CHECKS (MANDATORY)

- \(\text{Average}=\frac{\text{Sum of the quantities}}{\text{Number of quantities}}\); work with SUMS (average \(\times\) number), never by adding or averaging averages of groups of different sizes.
- When a member joins, leaves or is replaced, compare the total before and after; the change in the average times the number of members is the change in the total.
- Average speed for a whole journey is total distance \(\div\) total time - never the plain average of the speeds (for two equal distances it is \(\frac{2xy}{x+y}\)).
- Count the items carefully ("from the 9th to the 16th, both days inclusive" is 8 days; "first n natural numbers" starts at 1, "first n even numbers" at 2).
- For overlapping groups (first six and last six of eleven numbers) the shared middle item is counted twice: subtract the whole sum once.
- In pass / fail and men / women questions the totals of the two parts must add up to the whole (number of people and total marks).
- An average answer keeps its unit (years, kg, runs, Rs, km/hr) and may be a fraction; write repeating values as exact fractions or mixed numbers (\(16\frac{2}{3}\)), never as rounded decimals, unless the options themselves are decimals.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "a new member joins and the average changes" problem:

Find the total before the change:

\[
\text{Old total}=\text{old average}\times\text{old number}
\]

Find the total after the change:

\[
\text{New total}=\text{new average}\times\text{new number}
\]

The new member is the difference:

\[
\text{New member}=\text{New total}-\text{Old total}
\]

For other Average problems, use the natural mathematical relationship required by the question (turn every average into a sum, compare the sums, and divide by the number of items only at the end).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
n=\text{number of quantities},\qquad S=\text{their sum},\qquad A=\frac{S}{n}=\text{their average}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> The average of a set of quantities is their sum divided by their number:

\[
\text{Average}=\frac{\text{Sum of the quantities}}{\text{Number of quantities}}
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Add the scores.</b><br>

A player scores 42, 57 and 63 runs in three matches.

\[
42+57+63=162
\]

<br><br>

<b>Step 2: Share the total equally among the matches.</b><br>

\[
162\div 3=54
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
\text{Sum}=162,\qquad \text{Number}=3
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\text{Average}=\frac{\text{Sum}}{\text{Number}}
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{162}{3}=54
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(54\) runs</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
\frac{42+57+63}{3}=54
\]

<br>

∴ <b>Final Answer: \(54\) runs</b>.

</div>

""")

p = swap(p, "Do not alter the underlying mathematical concept merely to change wording.\n",
         "Do not alter the underlying mathematical concept merely to change wording.\n\n"
         "Keep the question sentence simple, like an ordinary textbook question: change the object or setting (marks of pupils instead "
         "of runs of a batsman, a village instead of a town) and use ALL-new numbers - no number of the source question may be kept "
         "except 1, 2 and 3. A hard, unusual sentence is not wanted; a copied sentence with only the numbers changed is not allowed.\n")
p = swap(p, '"chapter":"time_and_distance"', '"chapter":"average"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Average rule.\n"
         "- Follow every AVERAGE-SPECIFIC CHECK (work with sums, compare totals before and after, average speed = total distance / "
         "total time, count items carefully, exact fractions).")

assert "Time and Distance" not in p and "TIME AND DISTANCE" not in p, "left-over Time and Distance text"
open(os.path.join(HERE, "prompt_average.txt"), "w", encoding="utf-8").write(p)
print("prompt_average.txt:", len(p), "chars | prompt #9:", len(src), "chars")
