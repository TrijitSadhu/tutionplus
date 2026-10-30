"""Average Miscellaneous (book pdf pages 19-21): one simple-style sentence per problem, all-new numbers. Key -> (rule card, sentence)."""
B = chr(92)
SENT = {
    "m01": (8, "A shop sold an average of 248 items a day for the first 5 days of a week, and an average of 252 items a day for the first 6 days. "
               "How many items were sold on the 6th day?"),
    "m02": (4, "A car runs for " + B + "(x" + B + ") hours at 40 km/hr and then for " + B + "(y" + B + ") hours at 65 km/hr. "
               "What is its average speed for the whole journey?"),
    "m03": (20, "A van goes " + B + "(x" + B + ") km at 30 km/hr and then " + B + "(y" + B + ") km at 45 km/hr. Find its average speed for the whole journey."),
    "m04": (40, "A drone flies once round the four sides of a square plot at 300, 450, 600 and 900 metres a minute. What is its average speed for the whole round?"),
    "m05": (2, "The average age of three sisters is 18 years and their ages are in the ratio 2 : 3 : 4. How old is the eldest?"),
    "m06": (39, "The members of a club grew by 8% in the first year, by 25% in the second year and by 28% in the third year. "
                "What is the average yearly rate of growth, that is, the one rate that gives the same result when applied each year?"),
    "m07": (4, "A trader earns 9% on " + B + "(" + B + "frac{1}{3}" + B + ") of his money, 15% on " + B + "(" + B + "frac{1}{2}" + B + ") of it and 18% on the rest. "
               "What is his average rate of return on all his money?"),
    "m08": (2, "Of three numbers, the first is twice the second and four times the third. Their average is 70. What is the first number minus the third?"),
    "m09": (5, "The average of 8 readings is 21.5. The first two average 16.5 and the next three average 19.4. The 6th reading is 2 less than the 7th "
               "and 5 less than the 8th. What is the 6th reading?"),
    "m10": (2, "The average age of a family of 5 is 24 years. The youngest member is 8 years old. What was the average age of the family just before "
               "the youngest was born?"),
    "m11": (8, "A couple's average age was 25 years when they married 6 years ago. Now the average age of the couple and their child, born since "
               "then, is 22 years. How old is the child?"),
    "m12": (8, "Six years ago the average age of P, Q and R was 34 years. Now S has joined them and the average age of all four is 38 years. How old is S?"),
    "m13": (8, "Three years ago the average age of Anil and Sunil was 24 years. Now the average age of Anil, Sunil and Kiran is 29 years. "
               "How old will Kiran be 5 years from now?"),
    "m14": (5, "The average weight of 30 parcels is 21 kg. When parcels X, Y and Z are taken out, the other 27 average 20 kg. X and Y weigh the same, "
               "and Z weighs 6 kg more than X. Find the weight of X."),
    "m15": (2, "Of three numbers, the first is three times the second and half the third. Their average is 50. Find the three numbers in order."),
    "m16": (2, "Of three numbers, the second is three times the first and also twice the third. Their average is 33. What is the largest of them?"),
    "m17": (2, "Three numbers add up to 119. The first and second are in the ratio 3 : 4, and the second and third in the ratio 2 : 5. "
               "What is the second number?"),
    "m18": (11, "The average weight of P, Q and R is 62 kg. When S joins them, the average becomes 60 kg. Then T, who weighs 4 kg more than S, "
                "takes the place of P, and the average of Q, R, S and T becomes 59 kg. What does P weigh?"),
    "m19": (8, "Three years ago the average age of four friends was 31 years. A fifth friend has now joined them, and the average age of all five "
               "is 33 years. How old is the fifth friend?"),
    "m20": (2, "The average age of K and L is 34 years. If M took the place of K, the average would be 31 years, and if M took the place of L, "
               "it would be 36 years. Find the ages of K, L and M."),
}

if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"C:\Users\newwe\Desktop\tution\tutionplus\claude\tools")
    from originality import Book, check_question, measures
    book = Book(r"C:\Users\newwe\Desktop\tution\tutionplus\claude\runs\average\pdf_text.txt")
    for k, (r, q) in SENT.items():
        p = check_question(q, book, None, simple=True)
        print(k, "PASS" if not p else "FAIL", measures(q, book, None), p)
