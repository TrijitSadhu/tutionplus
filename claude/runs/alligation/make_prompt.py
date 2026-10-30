# Builds the Alligation and Mixture prompt from prompt #9 ("time and distance_detail method + theorem"):
# the shared rules stay word for word; every Time and Distance-specific block is swapped for an
# Alligation one. Writes prompt_alligation.txt next to this file (no DB access).
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
         "merely because they belong to the Alligation and Mixture chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR ALLIGATION AND MIXTURE

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Alligation cross diagram written as a table (cheaper price, dearer price, mean price, the two differences)
- Mixture composition table (quantity, price per unit, total cost of each component)
- Cost price / selling price / profit table
- Concentration table (amount of each substance before and after adding or removing)
- Replacement table (amount of the original liquid left after each draw)
- Ratio-to-quantity split table

For example (alligation cross written as a table):

<table border="1" cellpadding="4">
<tr><th>Cheaper (per unit)</th><th>Mean price</th><th>Dearer (per unit)</th></tr>
<tr><td>\(c\)</td><td>\(m\)</td><td>\(d\)</td></tr>
<tr><td>Parts of cheaper \(= d-m\)</td><td></td><td>Parts of dearer \(= m-c\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚖️ ALLIGATION-SPECIFIC CHECKS (MANDATORY)

- Water (or any free ingredient) costs Rs 0 per unit unless the question says otherwise.
- The mean price must lie strictly between the two component prices; otherwise the mixture is impossible.
- When the mixture is SOLD at a price with a profit or loss, first convert that selling price back into the cost price of the mixture: \( \text{CP} = \text{SP}\times\frac{100}{100+\text{gain}\%} \) (or \( \frac{100}{100-\text{loss}\%} \)). Alligation always works on cost prices.
- "Gain a fraction of the outlay" means the profit is that fraction of the cost price.
- Give the ratio in the SAME order the question asks for (e.g. water : spirit, cheaper : dearer). Check that the option order matches.
- When a total quantity is given, split it in the ratio and check that the parts add up to the total.
- Percentages of a substance (sugar, alcohol, milk) are treated like prices: pure substance = 100%, pure water = 0%.
- For repeated replacement, the amount of the original liquid left after \(n\) operations is \( Q\left(1-\frac{r}{Q}\right)^n \).
- Keep money units consistent (paise vs rupees) and state the unit in the final answer.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt z \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a basic alligation problem:

Let the quantities mixed be \(x\) kg of the cheaper item and \(y\) kg of the dearer item.

Write the total cost of the mixture in two ways:

\[
c\,x + d\,y = m\,(x+y)
\]

Collect the \(x\) terms and the \(y\) terms:

\[
(m-c)\,x = (d-m)\,y
\]

Then find the ratio \(x:y\).

For other Alligation and Mixture problems, use the natural mathematical relationship required by the question (total cost, total amount of a substance, profit on cost price, quantity left after replacement, and so on).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
c=\text{price of the cheaper item}
\]

\[
d=\text{price of the dearer item}
\]

\[
m=\text{mean price of the mixture}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> When an item costing \(c\) per kg is mixed with an item costing \(d\) per kg to get a mixture worth \(m\) per kg (\(c \lt m \lt d\)), they must be mixed in the ratio

\[
\text{cheaper} : \text{dearer} = (d-m) : (m-c)
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

Let \(x\) kg of rice at Rs 12 per kg be mixed with \(y\) kg of rice at Rs 20 per kg.

Mixture price:

\[
\text{Rs } 15 \text{ per kg}
\]

<br><br>

<b>Step 2: Write the total cost in two ways.</b><br>

\[
12x + 20y = 15(x+y)
\]

<br><br>

<b>Step 3: Solve for the ratio.</b><br>

\[
12x + 20y = 15x + 15y
\]

\[
5y = 3x
\]

\[
\frac{x}{y}=\frac{5}{3}
\]

Therefore, the rice must be mixed in the ratio:

\[
5 : 3
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
c=12,\qquad d=20,\qquad m=15
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\text{cheaper} : \text{dearer} = (d-m) : (m-c)
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
(20-15) : (15-12) = 5 : 3
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(5 : 3\)</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
(d-m) : (m-c) = (20-15) : (15-12) = 5 : 3
\]

<br>

∴ <b>Final Answer: \(5 : 3\)</b>.

</div>

""")

p = swap(p, '"chapter":"time_and_distance"', '"chapter":"alligation_n_mixture"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Alligation and Mixture rule.\n"
         "- Follow every ALLIGATION-SPECIFIC CHECK (water = Rs 0, convert selling price to cost price first, ratio in the order asked).")

for word in ("Distance", "distance", "speed", "km/hr", "Speed"):
    assert word not in p, f"left-over Time and Distance text: {word}"
open(os.path.join(HERE, "prompt_alligation.txt"), "w", encoding="utf-8").write(p)
print("prompt_alligation.txt:", len(p), "chars | prompt #9:", len(src), "chars")
