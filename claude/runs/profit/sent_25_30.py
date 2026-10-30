"""Sentences of Profit and Loss Rules 25-30 (shared by gen_25_30.py and the number search). Numbers always come in the order
x, X, y[, z]: the first per cent, the rupees (or paise), the second per cent, and the wished gain."""

# rule -> (first sale is a profit?, second sale is a profit?, X is 'more' or 'less')
KIND = {25: (False, True, "more"), 26: (True, True, "more"), 27: (False, True, "more"),
        28: (True, True, "less"), 29: (True, True, "more"), 30: (False, False, "more")}

S = {
    # Rule 25: loss x, Rs X more -> gain y; price for gain z
    318: (25, lambda x, X, y, z: f"A shop sold a heater at a loss of {x}%. With Rs {X} more it would have made a gain of {y}%. At what price should it sell the heater to gain {z}%, and what did the heater cost?", "both"),
    961: (25, lambda x, X, y, z: f"A trader sold a fridge at a loss of {x}%. Had he got Rs {X} more, his gain would have been {y}%. For how much must he sell it to gain {z}%? Also find its cost.", "both"),
    "r25_e1": (25, lambda x, X, y, z: f"A dealer let a desk go at a loss of {x}%. Rs {X} more would have given him a gain of {y}%. Find the price for a gain of {z}% and the cost of the desk.", "both"),
    "r25_e2": (25, lambda x, X, y, z: f"A table is sold at a loss of {x}%. For Rs {X} more it would have brought a gain of {y}%. At what price will it bring a gain of {z}%?", "sp"),
    "r25_e3": (25, lambda x, X, y, z: f"A pen is sold at a loss of {x}%. If the price had been Rs {X} higher, the gain would have been {y}%. What price gives a gain of {z}%?", "sp"),
    "r25_e4": (25, lambda x, X, y, z: f"A TV set is sold at a loss of {x}%. Rs {X} more would have turned this into a gain of {y}%. For what price should it be sold to gain {z}%?", "sp"),
    "r25_e5": (25, lambda x, X, y, z: f"A camera is sold at a loss of {x}%. With Rs {X} more the seller would have gained {y}%. At what price should it be sold for a gain of {z}%?", "sp"),
    # Rule 26: profit x, X more -> profit y; cost and first selling price
    319: (26, lambda x, X, y: f"A fruit seller makes a profit of {x}% on each mango. If he asks {X} paise more for each mango, his profit becomes {y}%. Find the cost price and the first selling price of a mango.", "cpsp"),
    "r26_e1": (26, lambda x, X, y: f"A dealer makes a profit of {x}% on a scooter. If he raises its price by Rs {X}, his profit becomes {y}%. Find the cost price and the first selling price.", "cpsp"),
    "r26_e2": (26, lambda x, X, y: f"A shop sells a fan at a profit of {x}%. By asking Rs {X} more it would make a profit of {y}%. Find the cost price and the first selling price of the fan.", "cpsp"),
    "r26_e3": (26, lambda x, X, y: f"A man sells a cupboard at a gain of {x}%. If he puts up the price by Rs {X}, he gains {y}%. Find the cost price and the first selling price.", "cpsp"),
    "r26_e4": (26, lambda x, X, y: f"A vendor sells guavas at a profit of {x}%. If he charges {X} paise more for each guava, he makes {y}%. Find the cost price and the first selling price of one guava.", "cpsp"),
    "r26_e5": (26, lambda x, X, y: f"A seller makes {x}% on each lemon. If each lemon costs the buyer {X} paise more, the seller makes {y}%. Find the cost price and the first selling price of a lemon.", "cpsp"),
    # Rule 27: loss x, X more per kg -> profit y; cost and first selling price per kg
    320: (27, lambda x, X, y: f"A grocer had to sell sugar at a loss of {x}%. If he raises the price by Rs {X} a kg, he makes a profit of {y}%. Find the cost price and the first selling price per kg.", "cpsp"),
    "r27_e1": (27, lambda x, X, y: f"A man had to sell dal at a loss of {x}%. Charging Rs {X} more a kg would give him a profit of {y}%. Find the cost price and the first selling price per kg.", "cpsp"),
    "r27_e2": (27, lambda x, X, y: f"Tea was sold at a loss of {x}%. Had it been sold for Rs {X} more a kg, the profit would have been {y}%. Find the cost price and the first selling price per kg.", "cpsp"),
    "r27_e3": (27, lambda x, X, y: f"A shop sold flour at a loss of {x}%. With Rs {X} more a kg it would make {y}%. Find the cost price and the first selling price of flour per kg.", "cpsp"),
    "r27_e4": (27, lambda x, X, y: f"A woman sold rice at a loss of {x}%. Asking Rs {X} more a kg would give her a profit of {y}%. Find the cost price and the first selling price per kg.", "cpsp"),
    # Rule 28: profit x, Rs X less -> still profit y; price for gain z
    321: (28, lambda x, X, y, z: f"A dealer sold a cooler at a profit of {x}%. Even for Rs {X} less he would still have gained {y}%. At what price should he sell it to gain {z}%, and what did it cost?", "both"),
    "r28_e1": (28, lambda x, X, y, z: f"A TV was sold at a profit of {x}%. Sold for Rs {X} less, it would still have given a profit of {y}%. For what price should it be sold to gain {z}%?", "sp"),
    "r28_e2": (28, lambda x, X, y, z: f"A camera brought a profit of {x}%. For Rs {X} less the profit would have been {y}%. What price would give a profit of {z}%?", "sp"),
    "r28_e3": (28, lambda x, X, y, z: f"A sofa was sold at a gain of {x}%. Had it been sold for Rs {X} less, the gain would have been {y}%. At what price will the gain be {z}%?", "sp"),
    # Rule 29: profit x, Rs X more -> profit y; price for gain z
    322: (29, lambda x, X, y, z: f"A shop sold a radio at a profit of {x}%. For Rs {X} more it would have made {y}%. At what price should it sell the radio to gain {z}%, and what did the radio cost?", "both"),
    "r29_e1": (29, lambda x, X, y, z: f"A camera was sold at a profit of {x}%. If it had fetched Rs {X} more, the profit would have been {y}%. What price would give a profit of {z}%?", "sp"),
    "r29_e2": (29, lambda x, X, y, z: f"A TV was sold at a gain of {x}%. With Rs {X} more the gain would have been {y}%. For what price should it be sold to gain {z}%?", "sp"),
    "r29_e3": (29, lambda x, X, y, z: f"A pen was sold at a profit of {x}%. Rs {X} more would have made the profit {y}%. At what price will the profit be {z}%?", "sp"),
    # Rule 30: loss x, Rs X more -> still loss y; price for gain z
    323: (30, lambda x, X, y, z: f"A shop sold a radio at a loss of {x}%. For Rs {X} more it would still have lost {y}%. At what price should it sell the radio to gain {z}%, and what did the radio cost?", "both"),
    "r30_e1": (30, lambda x, X, y, z: f"A CD player was sold at a loss of {x}%. With Rs {X} more the loss would have been only {y}%. For what price should it be sold to gain {z}%?", "sp"),
    "r30_e2": (30, lambda x, X, y, z: f"A TV was sold at a loss of {x}%. Had it fetched Rs {X} more, the loss would have been {y}%. At what price will it give a gain of {z}%?", "sp"),
    "r30_e3": (30, lambda x, X, y, z: f"A chair was sold at a loss of {x}%. For Rs {X} more the loss would have been {y}%. What price gives a gain of {z}%?", "sp"),
}
