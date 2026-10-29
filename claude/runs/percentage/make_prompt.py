# Builds the Percentage prompt from prompt #9 ("time and distance_detail method + theorem"):
# the shared rules stay word for word; every Time and Distance-specific block is swapped for a
# Percentage one. Reads prompt9_original.txt (exported from the DB by save_prompt.py), writes
# prompt_percentage.txt next to this file (no DB access). Same swaps as claude/runs/time_work/make_prompt.py.
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
         "merely because they belong to the Percentage chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR PERCENTAGE

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Base-100 table (take the original value as 100 and follow it through each change)
- Successive-change chain (100 → after the 1st change → after the 2nd change → ...)
- Before / after table (price, consumption and expenditure; or the two factors of a product and the product)
- Share table (what each person takes and what is left after each step)
- Population year-by-year table
- Venn-style counts for "failed in A, failed in B, failed in both" problems
- Mixture table (quantity of each part before and after adding or removing)

For example (base-100 table for price and consumption):

<table border="1" cellpadding="4">
<tr><th></th><th>Price</th><th>Consumption</th><th>Expenditure</th></tr>
<tr><td>Before</td><td>\(100\)</td><td>\(100\)</td><td>\(100\times 100=10000\)</td></tr>
<tr><td>After</td><td>\(100+r\)</td><td>\(c\)</td><td>\((100+r)\times c=10000\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ PERCENTAGE-SPECIFIC CHECKS (MANDATORY)

- Always identify the BASE of every percentage: "\(x\%\) of A" uses A as the base; "A is \(x\%\) more than B" and "B is \(x\%\) less than A" use B and A respectively as the base. Changing the base changes the answer (25% more is NOT undone by 25% less).
- "\(x\%\) more than \(N\)" is \(N\times\frac{100+x}{100}\); "\(x\%\) less than \(N\)" is \(N\times\frac{100-x}{100}\); "\(x\%\) of \(N\)" is \(N\times\frac{x}{100}\).
- Successive percentage changes MULTIPLY (each one acts on the value left by the previous one); they never simply add.
- In "of the remaining" problems, every later percentage is taken on what is left after the earlier steps, not on the original amount.
- Population and depreciation: the change each year is on the population at the start of that year, so use powers / products, not \(n\times r\%\).
- Price × Consumption = Expenditure (and Rate × Quantity = Revenue, Length × Breadth = Area): when one factor changes, find the other from the product.
- Distinguish a percentage CHANGE from the NEW value as a percentage of the old one (an increase of 20% means the new value is 120% of the old one).
- Give the sign: say clearly whether the result is an increase or a decrease (gain or loss), and give a percentage answer with the % sign and other answers in the unit asked (Rs, kg, litres, votes, marks, people).
- Write repeating values as exact fractions or mixed numbers (\(33\frac{1}{3}\%\), \(16\frac{2}{3}\%\), \(9\frac{1}{11}\%\)), never as rounded decimals, unless the options themselves are decimals.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "two values are more than a third value" problem:

Take the third value as 100 (or as \(N\)).

Write each value in terms of it:

\[
\text{First}=100\times\frac{100+x}{100}=100+x,\qquad \text{Second}=100+y
\]

Then compare them directly:

\[
\text{First as a percentage of Second}=\frac{100+x}{100+y}\times 100\%
\]

For other Percentage problems, use the natural mathematical relationship required by the question (take the unknown original value as 100 or as \(N\), follow it through every change, and form an equation with the given figure).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
N=\text{the original value (taken as 100 when only percentages are given)}
\]

\[
x,\ y=\text{the given percentages}
\]

\[
R=\text{the result (the value after the change)}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> If two values are respectively \(x\%\) and \(y\%\) more than a third value, then the first is

\[
\frac{100+x}{100+y}\times 100\% \text{ of the second}
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Take the third value as 100.</b><br>

The two numbers are 20% and 50% more than the third number.

<br><br>

<b>Step 2: Write both numbers.</b><br>

\[
\text{First}=100+20=120,\qquad \text{Second}=100+50=150
\]

<br><br>

<b>Step 3: Express the first as a percentage of the second.</b><br>

\[
\frac{120}{150}\times 100\%=80\%
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
x=20,\qquad y=50
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\frac{100+x}{100+y}\times 100\%
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{100+20}{100+50}\times 100\%=\frac{120}{150}\times 100\%=80\%
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(80\%\)</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
\frac{100+x}{100+y}\times 100=\frac{120}{150}\times 100=80
\]

<br>

∴ <b>Final Answer: \(80\%\)</b>.

</div>

""")

p = swap(p, '"chapter":"time_and_distance"', '"chapter":"percentage"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Percentage rule.\n"
         "- Follow every PERCENTAGE-SPECIFIC CHECK (identify the base of every percentage, successive changes multiply, "
         "\"of the remaining\" uses what is left, say increase or decrease, exact fractions such as 33 1/3%).")

for word in ("Distance", "distance", "speed", "km/hr", "Speed", "journey"):
    assert word not in p, f"left-over Time and Distance text: {word}"
open(os.path.join(HERE, "prompt_percentage.txt"), "w", encoding="utf-8").write(p)
print("prompt_percentage.txt:", len(p), "chars | prompt #9:", len(src), "chars")
