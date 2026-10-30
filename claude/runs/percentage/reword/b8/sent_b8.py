"""Sentence templates of Percentage rewording batch 8 (Rules 57-64), shared by gen_b8.py and the number search. They keep what
solve_57_64.py reads: the selling price as the last Rs amount (57), the first plain "N litres" (58-59), "N kg mixture" (60),
the per cents in the order p, a, q (61), "reduction of Rs N", "N kg more" and the money as the last Rs amount (63), and
"N kg more" / "for a rupee" / "reduced price and the original price" (64)."""

MAKER = {
    642: lambda x, y, z, A: rf"A toy maker earns \({x}\%\) profit on a toy, a wholesaler then earns \({y}\%\) and a shopkeeper \({z}\%\). The shopkeeper sells the toy for Rs {A}. What did it cost the maker?",
    1972: lambda x, y, z, A: rf"A chair passes from its maker, who gains \({x}\%\), to a dealer, who gains \({y}\%\), and then to a shop, which gains \({z}\%\) and sells it for Rs {A}. What did the chair cost the maker?",
    1973: lambda x, y, z, A: rf"On a school bag the maker gains \({x}\%\), the wholesaler \({y}\%\) and the seller \({z}\%\). If the seller's price is Rs {A}, find the maker's cost.",
    1974: lambda x, y, z, A: rf"A clock is sold by its maker at a profit of \({x}\%\), then by a dealer at a profit of \({y}\%\), and then by a shopkeeper at a profit of \({z}\%\) for Rs {A}. What did it cost to make?",
}
ADD = {
    643: lambda A, x, y: rf"A jar holds {A} litres of a liquid that is \({x}\%\) acid. How much water must be added to make it \({y}\%\) acid?",
    1975: lambda A, x, y: rf"A can has {A} litres of liquid with \({x}\%\) acid in it. How many litres of water should be poured in so that it is \({y}\%\) acid?",
    1976: lambda A, x, y: rf"To weaken {A} litres of a \({x}\%\) acid liquid into a \({y}\%\) acid liquid, how much water must be mixed in?",
    1977: lambda A, x, y: rf"A drum contains {A} litres of a liquid which is \({x}\%\) acid. Find the water to be added to bring the acid down to \({y}\%\).",
    1978: lambda A, x, y: rf"A tank holds {A} litres of liquid that is \({x}\%\) acid. How much water should be added so that the acid is only \({y}\%\)?",
    1979: lambda A, x, y: rf"A bottle has {A} litres of a \({x}\%\) acid liquid. How many litres of water must be added to make it a \({y}\%\) acid liquid?",
}
OUT = {
    644: lambda A, x, y: rf"A pan has {A} litres of a liquid that is \({x}\%\) acid. How much water must be boiled off to make it \({y}\%\) acid?",
    1980: lambda A, x, y: rf"A tub holds {A} litres of liquid with \({x}\%\) acid. How many litres of water should be dried off so that it becomes \({y}\%\) acid?",
    1981: lambda A, x, y: rf"To make {A} litres of a \({x}\%\) acid liquid stronger, at \({y}\%\) acid, how much water must be taken out?",
    1982: lambda A, x, y: rf"A vat contains {A} litres of a liquid which is \({x}\%\) acid. Find the water to be removed to raise the acid to \({y}\%\).",
    1983: lambda A, x, y: rf"A pot has {A} litres of a \({x}\%\) acid liquid. How many litres of water must be boiled away to make it \({y}\%\) acid?",
}
MIX = {
    645: (lambda M, p, n: rf"A {M} kg mixture of sand and gravel is \({p}\%\) gravel. How much sand must be mixed in so that gravel makes up only \({n}\%\)?", "gravel", "sand"),
    1984: (lambda M, p, n: rf"A {M} kg mixture of nuts and raisins is \({p}\%\) raisins. How many kg of nuts should be added so that raisins are only \({n}\%\) of it?", "raisins", "nuts"),
    1985: (lambda M, p, n: rf"In a {M} kg mixture of sugar and salt, \({p}\%\) is salt. How much sugar must be added to bring the salt down to \({n}\%\)?", "salt", "sugar"),
    1986: (lambda M, p, n: rf"A {M} kg mixture of clay and chalk has \({p}\%\) chalk. Find how much clay must be added so that the chalk is \({n}\%\) of the mixture.", "chalk", "clay"),
}
SCHOOL = {
    1987: (lambda p, a, q: rf"In a test, \({p}\%\) of the pupils sent by school P passed. School Q sent \({a}\%\) more pupils than school P, and \({q}\%\) more of its pupils passed than school P's. What per cent of school Q's pupils passed?", "P", "Q"),
    1988: (lambda p, a, q: rf"At a sports trial \({p}\%\) of the players from club X were picked. Club Y sent \({a}\%\) more players than club X, and \({q}\%\) more of them were picked than from club X. What per cent of club Y's players were picked?", "X", "Y"),
    1989: (lambda p, a, q: rf"In an exam, \({p}\%\) of the candidates from centre M passed. Centre N had \({a}\%\) more candidates than centre M, and \({q}\%\) more of its candidates passed than centre M's. Find the pass per cent of centre N.", "M", "N"),
}
CUT = {
    648: (lambda d, q, E: rf"After a reduction of Rs {d} per kg in the price of dal, a cook gets {q} kg more for Rs {E}. What was the first price per kg?", "dal"),
    1997: (lambda d, q, E: rf"With a reduction of Rs {d} per kg in the price of onions, a woman can buy {q} kg more for Rs {E}. Find the price per kg before the cut.", "onions"),
    1998: (lambda d, q, E: rf"A reduction of Rs {d} per kg in the price of flour lets a baker get {q} kg more for Rs {E}. What did the flour cost per kg at first?", "flour"),
}
PCUT = {
    649: lambda p, q, E: rf"When the price of coffee is cut by \({p}\%\), a buyer can get {q} kg more for Rs {E}. What was the price per kg before the cut?",
    1999: lambda p, q: rf"A \({p}\%\) cut in the price of oranges lets a buyer get {q} more for a rupee. What are the reduced price and the original price of one orange?",
    2000: lambda p, q, E: rf"After a \({p}\%\) cut in the price of wheat, a buyer gets {q} kg more for Rs {E}. What are the reduced price and the original price per kg?",
}
