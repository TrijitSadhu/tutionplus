"""Extracts the text layer of the Ratio and Proportion book chapter to pdf_text.txt and renders every page to pages/pNNN.png
(110 dpi). Both outputs are book content - never commit them. Usage: python extract_book.py"""
import os
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\newwe\Desktop\prompt for tutionplus\math\14\m tyra"
os.makedirs(os.path.join(HERE, "pages"), exist_ok=True)
out, k = [], 0
for name in ("Ratio and Proportion.1.pdf", "Ratio and Proportion.2.pdf"):
    doc = fitz.open(os.path.join(SRC, name))
    for i, page in enumerate(doc):
        k += 1
        out.append(f"=== PAGE {k} ({name} p{i + 1}) ===")
        out.append(page.get_text())
        page.get_pixmap(dpi=110).save(os.path.join(HERE, "pages", f"p{k:03d}.png"))
open(os.path.join(HERE, "pdf_text.txt"), "w", encoding="utf-8").write("\n".join(out))
print("pages", k)
