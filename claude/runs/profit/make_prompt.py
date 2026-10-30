# Builds the Profit and Loss prompt from prompt #9 ("time and distance_detail method + theorem"):
# the shared rules stay word for word; every Time and Distance-specific block is swapped for a
# Profit and Loss one. Reads prompt9_original.txt (exported from the DB by save_prompt.py), writes
# prompt_profit.txt next to this file (no DB access). Same swaps as claude/runs/percentage/make_prompt.py.
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
         "merely because they belong to the Profit and Loss chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR PROFIT AND LOSS

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- CP → SP table (cost price, profit or loss, selling price)
- Base-100 table (take the cost price as 100 and follow it through the mark-up, the discount and the profit)
- Marked price → discount → selling price chain (one discount after another)
- Chain of sellers (maker → wholesaler → retailer → customer, each with his own profit)
- Two-article table (cost, selling price and profit or loss of each article and of both together)
- Weights table for a dishonest dealer (what he gives, what he charges for)
- Units table for "bought x for a rupee, sold y for a rupee" problems

For example (base-100 table for a mark-up followed by a discount):

<table border="1" cellpadding="4">
<tr><th></th><th>Cost price</th><th>Marked price</th><th>Selling price</th></tr>
<tr><td>Value</td><td>\(100\)</td><td>\(100+m\)</td><td>\((100+m)\times\frac{100-d}{100}\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ PROFIT AND LOSS-SPECIFIC CHECKS (MANDATORY)

- Profit and loss per cent are ALWAYS on the cost price, unless the question clearly says "on the selling price"; a discount per cent is ALWAYS on the marked price.
- \(\text{Profit}=\text{SP}-\text{CP}\) when \(\text{SP}\gt\text{CP}\); \(\text{Loss}=\text{CP}-\text{SP}\) when \(\text{CP}\gt\text{SP}\).
- \(\text{SP}=\text{CP}\times\frac{100+\text{gain}\%}{100}\) and \(\text{SP}=\text{CP}\times\frac{100-\text{loss}\%}{100}\); go back from SP to CP by dividing, never by subtracting the per cent of the SP.
- Successive discounts MULTIPLY (\(20\%\) and \(10\%\) is \(28\%\), not \(30\%\)); a mark-up followed by a discount is a successive change too.
- In a chain of sellers every profit is on that seller's own cost price (the price he paid).
- When two articles are sold at the same selling price, one at \(x\%\) gain and one at \(x\%\) loss, there is always a LOSS, of \(\frac{x^2}{100}\%\) on the whole outlay.
- False weights: the gain is on what the dealer really gives, \(\frac{\text{true weight}-\text{false weight}}{\text{false weight}}\times 100\%\).
- "Bought \(a\) for a rupee and sold \(b\) for a rupee": compare the cost and the selling price of ONE article (or of the LCM of the counts).
- Say clearly whether the result is a profit or a loss (gain or loss), give a per cent answer with the % sign and money in Rs.
- Write repeating values as exact fractions or mixed numbers (\(33\frac{1}{3}\%\), \(16\frac{2}{3}\%\), \(9\frac{1}{11}\%\)), never as rounded decimals, unless the options themselves are decimals.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(x \lt y\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "sold at a profit, find the cost price" problem:

Take the cost price as Rs 100 (or as Rs \(x\)).

Follow it to the selling price:

\[
\text{SP}=100+\text{gain}=100\times\frac{100+g}{100}
\]

Then scale to the real selling price:

\[
\text{CP}=\text{real SP}\times\frac{100}{100+g}
\]

For other Profit and Loss problems, use the natural mathematical relationship required by the question (take the unknown cost price as 100 or as \(x\), follow it through every mark-up, discount and sale, and form an equation with the given figure).

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
\text{CP}=\text{cost price},\qquad \text{SP}=\text{selling price},\qquad \text{MP}=\text{marked price}
\]

\[
g,\ l,\ d=\text{the gain, loss and discount per cents}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> The profit or loss per cent is always reckoned on the cost price:

\[
\text{Gain or Loss per cent}=\frac{\text{Gain or Loss}}{\text{CP}}\times 100
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: Find the profit.</b><br>

A cycle bought for Rs 1600 is sold for Rs 2000.

\[
\text{Profit}=2000-1600=\text{Rs }400
\]

<br><br>

<b>Step 2: Find the profit on Rs 100 of cost.</b><br>

On Rs 1600 the profit is Rs 400, so on Rs 1 it is \(\frac{400}{1600}\) and on Rs 100 it is

\[
\frac{400}{1600}\times 100=25
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
\text{Gain}=\text{Rs }400,\qquad \text{CP}=\text{Rs }1600
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
\text{Gain per cent}=\frac{\text{Gain}}{\text{CP}}\times 100
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
\frac{400}{1600}\times 100=25\%
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: a gain of \(25\%\)</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
\frac{2000-1600}{1600}\times 100=25
\]

<br>

∴ <b>Final Answer: a gain of \(25\%\)</b>.

</div>

""")

p = swap(p, "Do not alter the underlying mathematical concept merely to change wording.\n",
         "Do not alter the underlying mathematical concept merely to change wording.\n\n"
         "Keep the question sentence simple, like an ordinary textbook question: change the object or setting (a cycle instead of a "
         "radio, a shopkeeper instead of a dealer) and use ALL-new numbers - no number of the source question may be kept except 1, 2 "
         "and 3. A hard, unusual sentence is not wanted; a copied sentence with only the numbers changed is not allowed.\n")
p = swap(p, '"chapter":"time_and_distance"', '"chapter":"profit_n_loss"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Profit and Loss rule.\n"
         "- Follow every PROFIT AND LOSS-SPECIFIC CHECK (profit and loss on the cost price, discount on the marked price, successive "
         "discounts multiply, say profit or loss, exact fractions such as 33 1/3%).")

for word in ("Distance", "distance", "speed", "km/hr", "Speed", "journey"):
    assert word not in p, f"left-over Time and Distance text: {word}"
open(os.path.join(HERE, "prompt_profit.txt"), "w", encoding="utf-8").write(p)
print("prompt_profit.txt:", len(p), "chars | prompt #9:", len(src), "chars")
