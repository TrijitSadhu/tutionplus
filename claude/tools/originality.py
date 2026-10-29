"""Originality gate for reworded / new questions (copyright: the owner wants a fresh sentence AND all-new numbers vs the book).
No DB access. Usage from a validator:

    from originality import Book, check_question
    book = Book(r"...\\pdf_text.txt")
    problems = check_question(new_q, book, old_q)        # [] = passes

Measures (the PDF text layer is a little garbled, so these are approximate - thresholds are set with that in mind):
- book wording : share of the question's 4-word phrases (digits masked as #) that occur anywhere in the book;
- book numbers : the question's numbers (1, 2, 3 ignored) all occur together inside one sentence-sized passage of the book
                 (WINDOW words) - the full number set of a book problem. Only tested with at least MIN_SET such numbers:
                 pairs of common numbers (10 and 15, 12 and 24) sit near each other all over a maths book, so a pair says nothing;
                 the numbers of the specific book problem a question replaces are checked through `old` instead;
- old wording  : word-sequence similarity (difflib ratio, digits masked) to the question it replaces;
- old numbers  : numbers kept from the question it replaces (1, 2 and 3 are ignored: 'twice', 'three times', 1 man ...)."""
import difflib, re

MAX_BOOK_WORDING = 0.35
MAX_OLD_WORDING = 0.55
# "simple" mode (owner, 2026-10-29): keep the book's easy sentence pattern but change the job/object, all-new numbers. Copying the
# book sentence with only the numbers changed scores about 0.86 / 0.97, a changed job about 0.35-0.65 / 0.60-0.88.
MAX_SIMPLE_BOOK = 0.70
MAX_SIMPLE_OLD = 0.90
SMALL = {"1", "2", "3"}
WINDOW = 25
MIN_SET = 3


def tokens(s, mask):
    s = re.sub(r"\\[a-zA-Z]+|[{}^_\\()\[\]$]", " ", s or "")
    s = re.sub(r"<[^>]+>", " ", s).lower()
    t = re.findall(r"[a-z]+|\d+(?:\.\d+)?", s)
    return ["#" if mask and re.match(r"\d", x) else x for x in t]


def grams(t, n):
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def big_numbers(s):
    return {x for x in tokens(s, False) if re.match(r"\d", x)} - SMALL


class Book:
    def __init__(self, path):
        text = open(path, encoding="utf-8").read()
        self.words = grams(tokens(text, True), 4)
        t = tokens(text, False)
        self.where = {}                                   # number -> word positions
        for i, w in enumerate(t):
            if re.match(r"\d", w):
                self.where.setdefault(w, []).append(i)

    def numbers_together(self, nums):
        """True if every number in `nums` occurs within one WINDOW-word passage of the book."""
        nums = sorted(nums, key=lambda v: len(self.where.get(v, [])))
        if len(nums) < MIN_SET or any(v not in self.where for v in nums):
            return False
        for start in self.where[nums[0]]:
            if all(any(abs(p - start) <= WINDOW for p in self.where[v]) for v in nums[1:]):
                return True
        return False


def measures(q, book, old=None):
    qw = grams(tokens(q, True), 4)
    wording = len(qw & book.words) / len(qw) if qw else 0.0
    out = {"book_wording": round(wording, 2), "book_numbers": book.numbers_together(big_numbers(q))}
    if old is not None:
        out["old_wording"] = round(difflib.SequenceMatcher(None, tokens(q, True), tokens(old, True)).ratio(), 2)
        out["old_numbers_kept"] = sorted(big_numbers(q) & big_numbers(old), key=lambda v: float(v))
    return out


def check_question(q, book, old=None, simple=False):
    """List of reasons the question is not original enough ([] = it passes). simple=True: the looser wording limits of the
    simple (book-like) style; the number rules are the same."""
    m = measures(q, book, old)
    max_book, max_old = (MAX_SIMPLE_BOOK, MAX_SIMPLE_OLD) if simple else (MAX_BOOK_WORDING, MAX_OLD_WORDING)
    bad = []
    if m["book_wording"] > max_book:
        bad.append(f"book wording {m['book_wording']} > {max_book}")
    if m["book_numbers"]:
        bad.append(f"all its numbers {sorted(big_numbers(q), key=float)} occur together in one book passage")
    if old is not None:
        if m["old_wording"] > max_old:
            bad.append(f"sentence too close to the old question ({m['old_wording']} > {max_old})")
        if m["old_numbers_kept"]:
            bad.append(f"numbers kept from the old question: {m['old_numbers_kept']}")
    return bad
