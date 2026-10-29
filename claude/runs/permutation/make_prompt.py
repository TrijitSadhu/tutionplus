# Builds the Permutation and Combination prompt from prompt #9 ("time and distance_detail method + theorem"):
# the shared rules stay word for word; every Time and Distance-specific block is swapped for a
# Permutation and Combination one. Reads prompt9_original.txt (exported from the DB), writes
# prompt_permutation.txt next to this file (no DB access). Same swaps as claude/runs/percentage/make_prompt.py.
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
         "merely because they belong to the Permutation and Combination chapter.")

p = swap_block(p, "## 📊 VISUAL BREAKDOWN FOR TIME AND DISTANCE", "## 🧠 TRADITIONAL METHOD", r"""## 📊 VISUAL BREAKDOWN FOR PERMUTATION AND COMBINATION

Use an appropriate visual breakdown when it helps explain the specified rule.

Depending on the specified rule, this may include:

- Place-filling boxes (one box per place, with the number of ways each place can be filled written under it)
- Seating patterns (B G B G ..., or × B × B × to show the gaps where the restricted group can sit)
- A circle sketch for round-table and necklace problems
- A case table (No. of officers | No. of jawans | No. of ways) for "at least" / "exactly" selections
- A grid sketch for rectangles and parallelograms formed by two sets of parallel lines

For example (place-filling boxes for a 3-digit number greater than 400 from 2, 3, 4, 5, 6, 0):

<table border="1" cellpadding="4">
<tr><th>Hundreds</th><th>Tens</th><th>Units</th></tr>
<tr><td>4, 5 or 6: \(3\) ways</td><td>any of the remaining \(5\)</td><td>any of the remaining \(4\)</td></tr>
</table>

Use a visual only when it genuinely improves understanding.

Do not force a visual into every question.

---

## ⚙️ PERMUTATION-AND-COMBINATION-SPECIFIC CHECKS (MANDATORY)

- Decide first whether ORDER matters: arrangements (seating, words, numbers, signals, prizes to different people) are permutations; groups, committees, teams, selections and handshakes are combinations.
- Decide whether REPETITION is allowed (digits "may be repeated", a servant can carry many cards, a boy can win many prizes): then each place has the same number of choices and the count is \(n^r\), not \({}^{n}P_{r}\).
- In repetition problems, start from the things that cannot repeat (prizes, friends, rings, arms): each of them chooses one of the others, so the count is (choices)^(number of non-repeating things).
- Number problems: the first digit cannot be 0; handle the restricted places (first digit, even last digit, "greater than") first, then fill the rest; split into cases when the restriction depends on another place.
- "Together": tie the group into one unit, arrange the units, then multiply by the arrangements inside the group. "No two together": arrange the others first, then place the group in the gaps (including both ends). "Not all together" = total minus all together - it is NOT the same as "no two together".
- Circular arrangements of \(n\) different things: \((n-1)!\); a necklace or garland (can be turned over): \(\frac{(n-1)!}{2}\).
- Repeated letters or identical objects: divide by the factorial of each repetition count; remember to subtract 1 when the question asks for REarrangements of a given word.
- Selections with "at least" or "at most": either add the cases or use the complement (total minus the forbidden cases) - never count a selection twice.
- Points and polygons: collinear points give only ONE line and NO triangle; diagonals = lines joining vertices minus the sides.
- Write factorials and \({}^{n}P_{r}\), \({}^{n}C_{r}\) in LaTeX (\(5!\), \({}^{10}C_{3}\)); when an option is a factorial expression, give the Final Answer in the same form and also its value when it is reasonably small.
- Inside any HTML field never write a raw `<` or `>` in math (a browser reads `<z` as a tag). Use `\lt` and `\gt`, e.g. \(r \lt n\).

---

""")

p = swap_block(p, "For example, for a round-trip problem:", "IMPORTANT:\n\nThe Traditional Method must genuinely", r"""For example, for a "no two girls sit together" problem:

Seat the boys first and mark the gaps between them (including both ends):

\[
\times\ B\ \times\ B\ \times\ B\ \times
\]

\(m\) boys leave \(m+1\) gaps, so the girls can be placed in the gaps in \({}^{m+1}P_{n}\) ways and the boys among themselves in \(m!\) ways.

For other Permutation and Combination problems, use counting from first principles (fill the places one by one and multiply, list the cases and add, or count the total and subtract the unwanted cases) without quoting the specified rule.

""")

p = swap_block(p, "For example:\n\n\\[\nD=\\text{Distance}", "Use only the variables relevant", r"""For example:

\[
n=\text{the number of different things}
\]

\[
r=\text{the number of places to fill (or things to choose)}
\]

\[
m=\text{the size of the second group}
\]

""")

p = swap_block(p, "## EXAMPLE OF A WELL-FORMATTED SOLUTION", "---\n\n## RULE EXTRACTION", r"""## EXAMPLE OF A WELL-FORMATTED SOLUTION

<div style="display:block;text-align:justify;border:1px solid;padding:12px">

<b>Theorem :</b> The number of ways in which \(m\) boys and \(m\) girls can be seated in a row so that boys and girls are alternate is

\[
2\,(m!\times m!)
\]

<hr>

<b>Traditional Method :</b>

<br><br>

<b>Step 1: List the possible patterns.</b><br>

With 4 boys and 4 girls in 8 seats, the row is either B G B G B G B G or G B G B G B G B.

<br><br>

<b>Step 2: Count each pattern.</b><br>

In each pattern the 4 boys fill their 4 seats in \(4!\) ways and the 4 girls fill theirs in \(4!\) ways:

\[
4!\times 4!=24\times 24=576
\]

<br><br>

<b>Step 3: Add the two patterns.</b><br>

\[
576+576=1152
\]

<hr>

<b>Using the Specified Rule :</b>

<br><br>

<b>Step 1: Identify the values.</b><br>

\[
m=4
\]

<br><br>

<b>Step 2: Apply the specified rule.</b><br>

\[
2\,(m!\times m!)
\]

<br><br>

<b>Step 3: Substitute the values.</b><br>

\[
2\,(4!\times 4!)=2\times 576=1152
\]

<br><br>

<b>Verification:</b> Both methods give the same result.

<br><br>

∴ <b>Final Answer: \(1152\)</b>.

</div>

<div style="display:block;text-align:justify;border:1px solid;padding:10px">

<span style="color:#4955e0;display:table">Quicker Method:</span>

\[
2\,(4!\times 4!)=1152
\]

<br>

∴ <b>Final Answer: \(1152\)</b>.

</div>

""")

p = swap(p, '"chapter":"time_and_distance"', '"chapter":"permutation_combination"')
p = swap(p, "- Do not introduce an unrelated Time and Distance rule.",
         "- Do not introduce an unrelated Permutation and Combination rule.\n"
         "- Follow every PERMUTATION-AND-COMBINATION-SPECIFIC CHECK (does order matter, is repetition allowed, first digit "
         "not 0, together / no two together / not all together, circular (n-1)!, identical things, collinear points).")

for word in ("Distance", "distance", "speed", "km/hr", "Speed", "journey"):
    assert word not in p, f"left-over Time and Distance text: {word}"
open(os.path.join(HERE, "prompt_permutation.txt"), "w", encoding="utf-8").write(p)
print("prompt_permutation.txt:", len(p), "chars | prompt #9:", len(src), "chars")
