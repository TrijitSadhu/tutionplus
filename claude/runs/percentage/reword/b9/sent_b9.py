"""Sentence templates of Percentage rewording batch 9 (Rules 65-76), shared by gen_b9.py and the number search. They keep
what solve_65_72.py / solve_73_77.py read: the total as the first plain number and the per cent first (65-67), three per
cents in order (68-69), x then y (72), the Rs difference last and "incomes of X and Y?" only when both are asked (73),
"ratio a : b" and "becomes W kg" in plain digits (74), the savings as the last Rs amount (75), "If W kg" (76)."""

SPLIT = {
    650: lambda N, p: rf"Divide {N} sweets between Ravi and Mohan so that Mohan gets \({p}\%\) of what Ravi gets. How many does each get?",
    2003: lambda N, p: rf"A farmer puts {N} mangoes in two baskets so that the small basket holds \({p}\%\) of what the big one holds. How many mangoes go in each basket?",
    2004: lambda N, p: rf"Split {N} marbles between two boys so that the younger one gets \({p}\%\) of the elder one's share. Find the two shares.",
    2005: lambda N, p: rf"A club has {N} members in two groups, and the smaller group is \({p}\%\) of the larger one. How many members are in each group?",
    2006: lambda N, p: rf"Break {N} into two parts so that the smaller part is \({p}\%\) of the larger part.",
    2007: lambda N, p: rf"A shop packs {N} eggs into two trays so that one tray has \({p}\%\) of what the other has. How many eggs are in each tray?",
}
MORE = {
    651: lambda X, x: rf"After {X} litres of oil are poured into a drum, it is still \({x}\%\) empty. How much more oil is needed to fill it?",
    2008: lambda X, x: rf"A tank gets {X} litres of oil and is still \({x}\%\) empty. How many more litres will fill it to the top?",
    2009: lambda X, x: rf"A man pours {X} litres of oil into a barrel, and the barrel is still \({x}\%\) empty. How much more oil does it need?",
    2010: lambda X, x: rf"With {X} litres of oil in it, a can is still \({x}\%\) empty. Find the oil needed to fill the can.",
    2011: lambda X, x: rf"A storage tank holds {X} litres of oil and is still \({x}\%\) empty. How many more litres can it take?",
    2012: lambda X, x: rf"{X} litres of oil fill a vat so that it is still \({x}\%\) empty. How much oil must be added to fill it?",
}
CAP = {
    652: lambda X, x: rf"After {X} litres of oil are poured into a drum, it is still \({x}\%\) empty. How much oil can the drum hold?",
    2013: lambda X, x: rf"A tank gets {X} litres of oil and is still \({x}\%\) empty. Find how many litres the tank holds when full.",
    2014: lambda X, x: rf"A man pours {X} litres of oil into a barrel, and the barrel is still \({x}\%\) empty. What is the barrel's capacity?",
    2015: lambda X, x: rf"With {X} litres of oil in it, a can is still \({x}\%\) empty. How much oil does the can hold when full?",
    2016: lambda X, x: rf"A storage tank holds {X} litres of oil and is still \({x}\%\) empty. Find its capacity.",
    2017: lambda X, x: rf"{X} litres of oil fill a vat so that it is still \({x}\%\) empty. What is the capacity of the vat?",
}
UP3 = {
    653: lambda x, y, z: rf"The price of a house goes up by \({x}\%\) in one year, \({y}\%\) in the next and \({z}\%\) in the year after. What single per cent rise is the same as these three?",
    2018: lambda x, y, z: rf"A worker's pay is raised by \({x}\%\), then by \({y}\%\) and then by \({z}\%\). What one rise per cent would give the same pay?",
    2019: lambda x, y, z: rf"The rent of a shop rises by \({x}\%\), \({y}\%\) and \({z}\%\) in three years in a row. Find the single equal rise per cent.",
    2020: lambda x, y, z: rf"A plant's height grows by \({x}\%\) in the first week, \({y}\%\) in the second and \({z}\%\) in the third. By what single per cent has it grown?",
    2021: lambda x, y, z: rf"The fees of a school go up by \({x}\%\), then \({y}\%\) and then \({z}\%\). What one increase per cent equals these three?",
}
DISC3 = {
    654: lambda x, y, z: rf"A shop gives three discounts one after another on a TV: \({x}\%\), \({y}\%\) and \({z}\%\). What single discount is the same as these three?",
    2022: lambda x, y, z: rf"On a bicycle a dealer allows discounts of \({x}\%\), \({y}\%\) and \({z}\%\) in turn. Find the one discount per cent that gives the same price.",
    2023: lambda x, y, z: rf"A sale takes \({x}\%\) off a coat, then \({y}\%\) off the new price and then \({z}\%\) more. What single discount per cent is this?",
    2024: lambda x, y, z: rf"Three discounts of \({x}\%\), \({y}\%\) and \({z}\%\) are given one after the other on a fridge. What one discount equals them?",
    2025: lambda x, y, z: rf"A trader cuts the price of a watch by \({x}\%\), then by \({y}\%\) and then by \({z}\%\). Find the single discount per cent that has the same effect.",
}
HOUSE = {
    656: lambda x, y: rf"A survey of a town found that \({x}\%\) of the houses had two or more people living in them. Of the houses with just one person, \({y}\%\) had only a male. What per cent of all the houses had one female and no male?",
    2034: lambda x, y: rf"In a village, \({x}\%\) of the houses have two or more people. Among the houses with a single person, \({y}\%\) have only a male. What per cent of all houses have exactly one female and no male?",
    2035: lambda x, y: rf"A count of the houses in a colony shows that \({x}\%\) have two or more people, and of the one-person houses \({y}\%\) have only a male. Find the per cent of all houses with one female and no male.",
    2036: lambda x, y: rf"In a city ward \({x}\%\) of the houses hold two or more people. Of the houses holding one person, \({y}\%\) hold only a male. What per cent of the houses hold just one female?",
    2037: lambda x, y: rf"A study of a street found that \({x}\%\) of its houses have two or more people. Of those with one person, \({y}\%\) have only a male. What per cent of the houses have one female and no male?",
}
INC = {
    657: (lambda x, y, M: rf"Asha's monthly pay is \({x}\%\) more than Neha's, and Neha's is \({y}\%\) less than Rina's. If Asha and Rina earn Rs {M} apart, what are the monthly incomes of Neha and Rina?", ("Asha", "Neha", "Rina"), True),
    2038: (lambda x, y, M: rf"Kamal earns \({x}\%\) more a month than Vinod, and Vinod earns \({y}\%\) less than Sunil. The monthly pay of Kamal and Sunil differs by Rs {M}. What is Vinod's monthly pay?", ("Kamal", "Vinod", "Sunil"), False),
    2039: (lambda x, y, M: rf"Ritu's salary is \({x}\%\) more than Pooja's, and Pooja's salary is \({y}\%\) less than Anu's. If Ritu and Anu earn Rs {M} apart each month, find Pooja's monthly salary.", ("Ritu", "Pooja", "Anu"), False),
    2040: (lambda x, y, M: rf"Ajay gets \({x}\%\) more each month than Vijay, who gets \({y}\%\) less than Sanjay. The gap between Ajay's and Sanjay's monthly pay is Rs {M}. What does Vijay get each month?", ("Ajay", "Vijay", "Sanjay"), False),
    2041: (lambda x, y, M: rf"Meera's monthly income is \({x}\%\) more than Lata's, and Lata's is \({y}\%\) less than Usha's. If Meera's and Usha's incomes differ by Rs {M}, find Lata's monthly income.", ("Meera", "Lata", "Usha"), False),
}
WT = {
    658: lambda a, b, x, y, W: rf"The weights of two brothers, Raj and Dev, are in the ratio {a} : {b}. Raj's weight goes up by \({x}\%\), and the total weight of the two becomes {W} kg, which is \({y}\%\) more than before. By what per cent did Dev's weight go up?",
    2043: lambda a, b, x, y, W: rf"Two sisters, Uma and Rani, have weights in the ratio {a} : {b}. Uma's weight rises by \({x}\%\) and their total weight becomes {W} kg, a rise of \({y}\%\). By what per cent did Rani's weight rise?",
}
SAVE = {
    659: lambda x, y, S: rf"A clerk spends \({x}\%\) of his monthly income on food and \({y}\%\) of the rest on rent, and saves the remaining Rs {S}. Find his monthly income, his spending on food and his spending on rent.",
}
USE = {
    660: lambda x, y, W: rf"The price of sugar rises by \({x}\%\), so a family cuts down its use and spends only \({y}\%\) more on sugar than before. If {W} kg was used each month before, how much is used now?",
    2050: lambda x, y, W: rf"When the price of dal went up by \({x}\%\), a hostel used less dal and spent just \({y}\%\) more on it. If {W} kg was used each month before, what is the new monthly use?",
    2051: lambda x, y, W: rf"After a \({x}\%\) rise in the price of oil, a family's spending on oil rose by only \({y}\%\) because it used less. If {W} kg was used a month before, find the new monthly use.",
    2052: lambda x, y, W: rf"The price of flour rose by \({x}\%\), but a bakery kept its extra spending on flour to \({y}\%\) by using less. If {W} kg was used each month before, how much is used now?",
    2053: lambda x, y, W: rf"A canteen saw the price of milk powder rise by \({x}\%\) and cut its use so that it spends only \({y}\%\) more. If {W} kg was used each month before, find the new use.",
}
