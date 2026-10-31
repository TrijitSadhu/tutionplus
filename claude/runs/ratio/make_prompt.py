# Builds the Ratio and Proportion prompt from prompt #9 ("time and distance_detail method + theorem"): the shared rules stay word
# for word; every Time and Distance-specific block is swapped for a Ratio and Proportion one. Reads prompt9_original.txt (copied
# from claude/runs/average/), writes prompt_ratio.txt next to this file (no DB access). Same swaps as claude/runs/average/make_prompt.py.
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
         "merely because they belong to the Ratio and Proportion chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR RATIO AND PROPORTION

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Parts table (each share's ratio part, the value of one part, and the share itself)
- Before / after table (the two numbers, or the milk and water, before and after something is added or taken away)
- Linked-ratios table (A : B and B : C written over a common middle term to give A : B : C)
- Proportion layout (\(a : b :: c : d\), extremes and means)
- Mixture table (milk and water in each vessel and in the mixture)
- Income / expenditure / saving table for two persons

For example (parts table for sharing an amount in the ratio \(a : b : c\)):

<table border="1" cellpadding="4">
<tr><th></th><th>Parts</th><th>Share</th></tr>
<tr><td>A</td><td>\(a\)</td><td>\(\frac{a}{a+b+c}\times x\)</td></tr>
<tr><td>B</td><td>\(b\)</td><td>\(\frac{b}{a+b+c}\times x\)</td></tr>
<tr><td>C</td><td>\(c\)</td><td>\(\frac{c}{a+b+c}\times x\)</td></tr>
<tr><td>All</td><td>\(a+b+c\)</td><td>\(x\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ RATIO-SPECIFIC CHECKS (MANDATORY)

- A ratio compares quantities of the same kind in the same unit; change units first (paise and rupees, months and years).
- Work with the value of ONE PART: total \(\div\) sum of the parts (or difference \(\div\) difference of the parts).
- Keep the order asked for: A : B is not B : A, and "new to old" is not "old to new". Write the final ratio in lowest terms.
- To join A : B and B : C, make the two B terms equal first (multiply each ratio), then read A : B : C.
- When something is added to (or taken from) both numbers, the difference of the two numbers does not change.
- Mixtures: track each liquid separately; when part of a mixture is taken out, each liquid goes out in the mixture's ratio.
- Areas go as the square and volumes as the cube of the ratio of the sides.
- Quantities in inverse proportion (speed and time for the same distance, men and days for the same work) take the reciprocals of the ratio.
- A count of people, coins or articles must come out as a whole number; check the answer against the question.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "share an amount in a given ratio" problem:

Add the parts of the ratio:

\[
\text{Total parts}=a+b
\]

Find the value of one part:

\[
\text{One part}=\frac{\text{Amount}}{\text{Total parts}}
\]

Each share is its number of parts times one part:

\[
\text{Share of A}=a\times\text{One part}
\]

For other Ratio and Proportion problems, use the natural mathematical relationship required by the question (write every quantity as a number of parts, or set up the equation for the unknown and solve it).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
a : b=\text{the given ratio},\qquad k=\text{value of one part},\qquad \text{the quantities}=ak \text{ and } bk
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> If two numbers are in the ratio \(a : b\) and their sum is \(x\), the numbers are

\[
\frac{ax}{a+b}\quad\text{and}\quad\frac{bx}{a+b}
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Write the numbers as parts.</b><br>

A rope of 84 m is cut into two pieces in the ratio 5 : 7. Let the pieces be \(5k\) and \(7k\) metres.

\[
5k+7k=84\quad\Rightarrow\quad 12k=84\quad\Rightarrow\quad k=7
\]

<br><br>

<b>Step 2: Find each piece.</b><br>

\[
5k=35,\qquad 7k=49
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
a=5,\qquad b=7,\qquad x=84
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\frac{ax}{a+b},\qquad \frac{bx}{a+b}
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{5\times 84}{12}=35,\qquad \frac{7\times 84}{12}=49
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(35\) m and \(49\) m</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
84\div 12=7;\qquad 5\times 7=35,\quad 7\times 7=49
\]

<br>

∴ <b>Final Answer: \(35\) m and \(49\) m</b>.

</div>

""")

p = swap(p, "Do not alter the underlying mathematical concept merely to change wording.\n",
         "Do not alter the underlying mathematical concept merely to change wording.\n\n"
         "Keep the question sentence simple, like an ordinary textbook question: change the object or setting (marbles instead of "
         "coins, a village fund instead of a school fund) and use ALL-new numbers - no number of the source question may be kept "
         "except 1, 2 and 3. A hard, unusual sentence is not wanted; a copied sentence with only the numbers changed is not allowed.\n")
p = swap(p, '"chapter":"time_and_distance"', '"chapter":"ratio_n_proportion"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Ratio and Proportion rule.\n"
         "- Follow every RATIO-SPECIFIC CHECK (same units, value of one part, order of the ratio, join ratios over a common term, "
         "lowest terms, whole-number counts).")

assert "Time and Distance" not in p and "TIME AND DISTANCE" not in p, "left-over Time and Distance text"
open(os.path.join(HERE, "prompt_ratio.txt"), "w", encoding="utf-8").write(p)
print("prompt_ratio.txt:", len(p), "chars | prompt #9:", len(src), "chars")
