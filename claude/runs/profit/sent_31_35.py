"""Sentences of Profit and Loss Rules 31-35 (shared by gen_31_35.py and the number search); numbers in the order the solvers read
them. ask: 'cp' (cost price), 'sp' (first selling price) or 'cpsp' (both)."""

S = {
    # Rule 31: profit x; cost and price both Rs A lower -> profit up by y points; find CP  (x, A, y)
    324: (31, lambda x, A, y: f"A lamp is sold at a profit of {x}%. If its cost and its selling price were both Rs {A} lower, the profit per cent would be {y} more. Find the cost price of the lamp.", "cp"),
    962: (31, lambda x, A, y: f"A shop sells a kettle at a profit of {x}%. Were the cost price and the selling price each Rs {A} less, the profit per cent would go up by {y}. What is the cost price?", "cp"),
    "r31_e1": (31, lambda x, A, y: f"A pen is sold at a profit of {x}%. If both its cost price and its selling price were Rs {A} less, the profit per cent would be {y} higher. Find the cost price.", "cp"),
    "r31_e2": (31, lambda x, A, y: f"A bag sells at a profit of {x}%. With its cost and its price both cut by Rs {A}, the profit per cent would rise by {y}. Find what the bag cost.", "cp"),
    "r31_e3": (31, lambda x, A, y: f"A clock is sold at a profit of {x}%. Lowering both its cost price and its selling price by Rs {A} would make the profit per cent {y} more. Find the cost price.", "cp"),
    "r31_e4": (31, lambda x, A, y: f"A toy brings a profit of {x}%. Had it cost Rs {A} less and sold for Rs {A} less, the profit per cent would have been {y} more. Find its cost price.".replace(f"Rs {A} less and sold for Rs {A} less", f"Rs {A} less and been sold for that much less"), "cp"),
    "r31_e5": (31, lambda x, A, y: f"A mat is sold at a profit of {x}%. If the cost price and the selling price both came down by Rs {A}, the profit per cent would rise by {y}. Find the cost price of the mat.", "cp"),
    # Rule 32: profit x; price cut by Rs X a kg -> loss y  (x, X, y)
    325: (32, lambda x, X, y: f"A grocer sells sugar at a profit of {x}%. If he cuts the price by Rs {X} a kg, he makes a loss of {y}%. Find the cost price and the first selling price per kg.", "cpsp"),
    "r32_e1": (32, lambda x, X, y: f"A man sells dal at a profit of {x}%. A cut of Rs {X} a kg in the price would give him a loss of {y}%. Find the first selling price per kg.", "sp"),
    "r32_e2": (32, lambda x, X, y: f"Ravi sells flour at a profit of {x}%. Cutting the price by Rs {X} a kg would leave him with a loss of {y}%. Find the first selling price per kg of flour.", "sp"),
    "r32_e3": (32, lambda x, X, y: f"A shop sells coffee at a profit of {x}%. If it brings the price down by Rs {X} a kg, it makes a loss of {y}%. Find the first selling price per kg.", "sp"),
    "r32_e4": (32, lambda x, X, y: f"Meena sells honey at a profit of {x}%. A price cut of Rs {X} a kg would turn it into a loss of {y}%. Find the first selling price per kg.", "sp"),
    "r32_e5": (32, lambda x, X, y: f"A trader sells salt at a profit of {x}%. Lowering the price by Rs {X} a kg would give a loss of {y}%. Find the first selling price per kg of salt.", "sp"),
    # Rule 33: profit x; price cut by X paise -> profit y  (x, X, y)
    326: (33, lambda x, X, y: f"A fruit seller sells guavas at a profit of {x}%. If he cuts the price of each guava by {X} paise, his profit is {y}%. Find the cost price and the first selling price of a guava.", "cpsp"),
    "r33_e1": (33, lambda x, X, y: f"A vendor sells lemons at a profit of {x}%. Cutting the price of each lemon by {X} paise leaves a profit of {y}%. Find the first selling price of a lemon.", "sp"),
    "r33_e2": (33, lambda x, X, y: f"A hawker sells pears at a profit of {x}%. If each pear costs the buyer {X} paise less, the hawker's profit is {y}%. Find the first selling price of a pear.", "sp"),
    "r33_e3": (33, lambda x, X, y: f"A girl sells eggs at a profit of {x}%. If she lowers the price of each egg by {X} paise, she makes {y}%. Find the first selling price of an egg.", "sp"),
    # Rule 34: profit P; cost Rs c less, price Rs s less -> profit per cent up by p  (P, c, s, p)
    327: (34, lambda P, c, s, p: f"A chair is sold at a profit of {P}%. If its cost price were Rs {c} less and its selling price Rs {s} less, the profit per cent would rise by {p}. Find the cost price.", "cp"),
    "r34_e1": (34, lambda P, c, s, p: f"A cap is sold at a profit of {P}%. Were its cost Rs {c} lower and its price Rs {s} lower, the profit per cent would go up by {p}. Find the cost price.", "cp"),
    "r34_e2": (34, lambda P, c, s, p: f"A book sells at a profit of {P}%. If it had cost Rs {c} less and been sold for Rs {s} less, the profit per cent would have been {p} more. Find the cost price.", "cp"),
    "r34_e3": (34, lambda P, c, s, p: f"A shirt is sold at a profit of {P}%. With its cost cut by Rs {c} and its price by Rs {s}, the profit per cent rises by {p}. What did the shirt cost?", "cp"),
    "r34_e4": (34, lambda P, c, s, p: f"A box is sold at a profit of {P}%. If the cost price fell by Rs {c} and the selling price by Rs {s}, the profit per cent would increase by {p}. Find the cost price.", "cp"),
    "r34_e5": (34, lambda P, c, s, p: f"A vase is sold at a profit of {P}%. A fall of Rs {c} in its cost and of Rs {s} in its price would raise the profit per cent by {p}. Find the cost price.", "cp"),
    # Rule 35: profit P; cost Rs c more, price Rs s more -> profit per cent down by p  (P, c, s, p)
    328: (35, lambda P, c, s, p: f"A fan is sold at a profit of {P}%. If its cost price went up by Rs {c} and its selling price by Rs {s}, the profit per cent would fall by {p}. Find the cost price.", "cp"),
    "r35_e1": (35, lambda P, c, s, p: f"A lamp is sold at a profit of {P}%. If the cost rose by Rs {c} and the price by Rs {s}, the profit per cent would drop by {p}. Find the cost price.", "cp"),
    "r35_e2": (35, lambda P, c, s, p: f"A stool sells at a profit of {P}%. Raising its cost by Rs {c} and its price by Rs {s} would bring the profit per cent down by {p}. What did the stool cost?", "cp"),
}
