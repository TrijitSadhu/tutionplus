"""Ratio and Proportion Miscellaneous (book pdf pages 24-29, problems M1-M35): one simple-style sentence per problem, all-new numbers.
Key -> (rule card it is filed on, sentence). Old rows keep their id as key (746-758)."""
B = chr(92)
fr = lambda a, b: B + "(" + B + "frac{" + str(a) + "}{" + str(b) + "}" + B + ")"
SENT = {
    746: (11, "Three numbers are in the ratio 4 : 7 : 8 and the sum of their squares is 1161. What is their sum?"),
    747: (16, "If P : Q = 7 : 12, Q : R = 6 : 11 and R : S = 22 : 13, find P : S."),
    "m02b": (16, "If P : Q = 12 : 13, Q : R = 13 : 15 and R : S = 10 : 11, find P : Q : R : S."),
    748: (5, f"Split 147 into two parts so that one-third of the first part and one-fifth of the second part are in the ratio 2 : 3. Find the two parts."),
    749: (32, "Divide 1450 into three parts so that 6 times the first, 8 times the second and 9 times the third are all equal. What is the largest part?"),
    "m05": (15, f"Rs 1020 is shared among A, B and C so that A gets {fr(3, 4)} of what B gets and B gets {fr(2, 5)} of what C gets. What is C's share?"),
    750: (2, "If 15% of p is equal to 25% of q, what is p : q?"),
    751: (15, "If A : B = 11 : 6 and B : C = 9 : 14, find C : A."),
    "m08": (11, f"Rs 830 is divided among A, B and C so that Rs 30 more than {fr(1, 2)} of A's share, Rs 20 more than {fr(1, 3)} of B's share and "
                f"Rs 10 more than {fr(1, 4)} of C's share are all equal. What is A's share?"),
    752: (19, "450 ml of a drink has juice and water in the ratio 8 : 1. How much more water must be added to make the ratio 4 : 1?"),
    753: (12, "Silver is 13 times as heavy as water and tin is 6 times as heavy as water. In what ratio must they be mixed to get an alloy 10 times as heavy as water?"),
    754: (15, f"If P is {fr(1, 4)} of Q and Q is {fr(2, 5)} of R, find P : Q : R."),
    755: (5, "A sum of money is shared between Ali and Babu in the ratio 5 : 8. If Babu's share is Rs 3200, what is the whole sum?"),
    756: (5, "A box of 15 eggs is dropped. Which of these cannot be the ratio of broken eggs to unbroken eggs?"),
    757: (5, "A man spends Rs 9500 on desks at Rs 1500 each and stools at Rs 250 each. If he buys as many desks as he can, what is the ratio of stools to desks?"),
    "m15": (15, "Rs 51600 is divided among A, B and C so that for every rupee A gets, B gets 80 paise, and for every rupee B gets, C gets 75 paise. What is B's share?"),
    "m16": (11, f"Rs 7200 is shared among A, B and C so that A gets {fr(1, 3)} as much as B and C together, and B gets {fr(1, 5)} of what A and C together get. "
                "By how much is C's share more than A's?"),
    "m17": (4, "If a 15 m long pipe weighs 40.5 kg, what does 8 m of the same pipe weigh?"),
    "m18": (15, "The money with Asha and Bina is in the ratio 5 : 9, and the money with Bina and Chitra is also in the ratio 5 : 9. If Asha has Rs 750, how much does Chitra have?"),
    "m19": (25, "The pupils in three classes are in the ratio 3 : 4 : 6. If 15 pupils are added to each class, the ratio becomes 4 : 5 : 7. How many pupils were there in all before?"),
    "m20": (11, "A year ago the pay of Hari and Ravi was in the ratio 3 : 4. Hari's pay last year to his pay now is 2 : 3, and Ravi's is 5 : 6. "
                "Their total pay now is Rs 4650. What is Hari's pay now?"),
    "m21": (15, "The first of three numbers is to the second as 1 : 2, and the second is to the third as 3 : 4. The sum of the squares of the numbers is 436. What is the second number?"),
    "m22": (1, f"If bc : ca : ab = 1 : 3 : 4, find {B}({B}frac{{a}}{{bc}} : {B}frac{{b}}{{ca}}{B})."),
    "m23": (5, f"The sum of two numbers is {B}(x{B}) and the first divided by the second is {B}(y{B}). What is the first number?"),
    "m24": (6, "A bag has Re 1, 50 paise, 25 paise and 10 paise coins numbering in the ratio 2 : 3 : 4 : 5. The total is Rs 45. How many 25 paise coins are there?"),
    "m25": (1, "The boys and girls in a club are in the ratio 7 : 8. If the boys increase by 10% and the girls by 65%, what is the new ratio of boys to girls?"),
    758: (11, "Money is shared among X, Y and Z in the ratio 5 : 11 : 8. If Z gives Rs 300 of his share to Y, the ratio becomes 5 : 14 : 5. What was the total amount?"),
    "m27": (2, "When 25% of a number is added to another number, the second number increases by 15%. What is the ratio of the second number to the first?"),
    "m28": (5, "Two numbers are in the ratio 7 : 6. If 30% of the first number is 21, what is 40% of the second number?"),
    "m29": (11, "Rs 6250 is to be shared among P, Q and R in the ratio 3 : 7 : 15. What is P's share?"),
    "m30": (2, "When 40% of a number is added to another number, the second number becomes 160% of itself. What is the ratio of the first number to the second?"),
    "m31": (2, f"When 45% of a number is taken from a second number, the second number becomes {fr(3, 4)} of itself. What is the ratio of the first number to the second?"),
    "m32": (2, f"When 30% of one number is added to a second number, the second number becomes {fr(11, 10)} of itself. What is the ratio of the first number to the second?"),
    "m33": (11, "A prize fund of Rs 5600 is split three ways between P, Q and R in the ratio 3 : 5 : 6. How much does Q receive?"),
    "m34": (2, "Given that a : b = 3 : 4, what is the ratio of 2a + 3b to 3a + 2b?"),
    "m35": (6, "A bag has Re 1, 50 paise and 25 paise coins numbering in the ratio 3 : 4 : 8. The total is Rs 252. How many 25 paise coins are there?"),
}

if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools")
    from originality import Book, check_question, measures
    book = Book(r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\ratio\pdf_text.txt")
    old = {r["id"]: r["q"] for r in json.load(open(r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\ratio\norule_questions.json", encoding="utf-8"))}
    for k, (r, q) in SENT.items():
        p = check_question(q, book, old.get(k) if isinstance(k, int) else None, simple=True)
        if p:
            print(k, "FAIL", measures(q, book, old.get(k) if isinstance(k, int) else None), p)
    print("checked", len(SENT))
