# Builds the Simple Interest prompt from prompt #9 ("time and distance_detail method + theorem"): the shared rules stay word for word;
# every Time and Distance-specific block is swapped for a Simple Interest one. Reads prompt9_original.txt, writes prompt_si.txt next
# to this file (no DB access). Same swaps as claude/runs/ratio/make_prompt.py.
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
         "merely because they belong to the Simple Interest chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR SIMPLE INTEREST

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Year-by-year table (principal, interest of each year, amount at the end of each year)
- Principal / rate / time / interest table for two loans or two parts of a sum
- Before / after table when the rate, the time or the principal changes
- Amount table for "amounts to Rs A1 in t1 years and Rs A2 in t2 years"

For example (one sum lent in two parts):

<table border="1" cellpadding="4">
<tr><th></th><th>Principal</th><th>Rate</th><th>Interest a year</th></tr>
<tr><td>Part 1</td><td>\(x\)</td><td>\(r_1\%\)</td><td>\(\frac{x r_1}{100}\)</td></tr>
<tr><td>Part 2</td><td>\(P-x\)</td><td>\(r_2\%\)</td><td>\(\frac{(P-x) r_2}{100}\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ SIMPLE-INTEREST CHECKS (MANDATORY)

- \(SI = \frac{P\times R\times T}{100}\) with \(R\) a per cent per year and \(T\) in YEARS - change months and days to years first.
- Amount \(=\) Principal \(+\) Simple Interest; do not mix up the amount with the interest.
- Simple interest is the same every year and is always worked on the original principal (unless the question changes the principal).
- "Doubles itself" means the interest equals the principal; "becomes n times" means the interest is \((n-1)\) times the principal.
- When a rate or a time changes, only the change in the interest depends on the change in the rate or time.
- Check the answer against the question: rates are per cent per annum, sums are in rupees, times in years (and months).
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "find the interest" problem:

Find the interest for one year:

\[
\text{Interest for 1 year}=\frac{\text{Rate}}{100}\times\text{Principal}
\]

Multiply by the number of years:

\[
\text{Interest}=\text{Interest for 1 year}\times\text{Time}
\]

For other Simple Interest problems, use the natural mathematical relationship required by the question (work out the interest of one year, compare the amounts, or set up the equation for the unknown and solve it).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
P=\text{Principal},\qquad R=\text{Rate per cent per annum},\qquad T=\text{Time in years},\qquad SI=\frac{PRT}{100}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> The simple interest on a principal \(P\) at \(R\%\) per annum for \(T\) years is

\[
SI=\frac{P\times R\times T}{100}
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Interest for one year.</b><br>

A farmer borrows Rs 2400 at 7% per annum for 3 years.

\[
\frac{7}{100}\times 2400 = 168
\]

<br><br>

<b>Step 2: Interest for 3 years.</b><br>

\[
168\times 3 = 504
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
P=2400,\qquad R=7,\qquad T=3
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
SI=\frac{P\times R\times T}{100}
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{2400\times 7\times 3}{100}=504
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: Rs \(504\)</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
\frac{2400\times 7\times 3}{100}=504
\]

<br>

∴ <b>Final Answer: Rs \(504\)</b>.

</div>

""")

p = swap(p, "Do not alter the underlying mathematical concept merely to change wording.\n",
         "Do not alter the underlying mathematical concept merely to change wording.\n\n"
         "Keep the question sentence simple, like an ordinary textbook question: change the object or setting (a loan for a shop "
         "instead of a bank deposit, a farmer instead of a clerk) and use ALL-new numbers - no number of the source question may be "
         "kept except 1, 2 and 3. A hard, unusual sentence is not wanted; a copied sentence with only the numbers changed is not allowed.\n")
p = swap(p, '"chapter":"time_and_distance"', '"chapter":"simple_interest"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Simple Interest rule.\n"
         "- Follow every SIMPLE-INTEREST CHECK (time in years, amount = principal + interest, interest on the original principal, "
         "'doubles' / 'n times' read correctly).")

assert "Time and Distance" not in p and "TIME AND DISTANCE" not in p, "left-over Time and Distance text"
open(os.path.join(HERE, "prompt_si.txt"), "w", encoding="utf-8").write(p)
print("prompt_si.txt:", len(p), "chars | prompt #9:", len(src), "chars")
