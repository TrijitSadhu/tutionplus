# Writes book_map.json: per rule the PDF page, the text-layer count of exercises and answer letters (first pass, confirmed
# from the page images batch by batch), and the DB rows that copy the rule's worked example (fuzzy match, map_text.py).
import json, re, subprocess, sys
out = subprocess.run([sys.executable, "-X", "utf8", "count_text.py"], capture_output=True, text=True, check=True).stdout
db = {583: 1, 584: 2, 585: 3, 586: 3, 587: 3, 588: 4, 589: 4, 590: 5, 591: 5, 592: 5, 593: 5, 594: 6, 595: 7, 596: 8}
db.update({597 + i: 9 + i for i in range(33)})          # 597-629 -> Rules 9-41, one worked example each
db.update({630: 42, 631: 43, 632: 44, 633: 45, 634: 46, 635: 47, 636: 48, 637: 49, 638: 53})
db.update({639 + i: 54 + i for i in range(16)})          # 639-654 -> Rules 54-69
db.update({655 + i: 71 + i for i in range(7)})           # 655-661 -> Rules 71-77 (Rule 70 has no copy)
rules = {}
for line in out.splitlines():
    m = re.match(r"Rule\s+(\d+) p\s*(\d+) examples (\d) \| exercises\s+(\d+) \| answers\s+(\d+): ?(.*)", line)
    n = int(m.group(1))
    rules[str(n)] = {"pdf_page": int(m.group(2)), "answers_text_layer": m.group(6).split(), "db_examples": []}
rules.setdefault("8", {"pdf_page": 5, "answers_text_layer": [], "db_examples": []})
for i, n in db.items():
    rules[str(n)]["db_examples"].append(i)
misc_db = {662: 3, 663: 4, 664: 5, 665: 6, 666: 7, 667: 8, 668: 14, 669: 15, 670: 16, 671: 17, 672: 18, 673: 19, 674: 20, 675: 21,
           676: 23, 677: 24, 678: 29, 679: 25}
data = {"_note": "Percentage.pdf = Chapter 'Percentage', book pages 135-176 (pdf page N = book page 134+N). 77 rules + 31 Miscellaneous "
                 "problems (pdf pages 38-42, answers with hints on pages 40-42). Rows 583-661 copy the worked examples word for word "
                 "(2019 rows, no rule linked); 662-679 copy Miscellaneous problems; 47 and 56 are 2018 rows from another book. "
                 "answers_text_layer comes from the garbled text layer - confirm from the page images per batch. None of the "
                 "rule exercises has a copy in the DB.",
        "rules": dict(sorted(rules.items(), key=lambda kv: int(kv[0]))),
        "misc": {"count": 31, "db_rows": {str(k): f"Misc {v}" for k, v in misc_db.items()},
                 "missing": [1, 2, 9, 10, 11, 12, 13, 22, 26, 27, 28, 30, 31], "note": "9-13 share one passage (a set)"},
        "other_rows": {"47": "2018, '1/2 is what percent of 1/3' (Rule 5 type)", "56": "2018, Shobha's test (Rule 3/5 type)"}}
json.dump(data, open("book_map.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rules", len(rules), "| rules with no DB row:", [n for n, r in data["rules"].items() if not r["db_examples"]])
print("text-layer answers total:", sum(len(r["answers_text_layer"]) for r in rules.values()))
