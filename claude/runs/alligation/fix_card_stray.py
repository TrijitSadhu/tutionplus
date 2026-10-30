# Wraps \frac{..}{..} that sit outside any \( \) / \[ \] in a rule card with \( \), so MathJax typesets them.
# Only text outside existing math is touched. Backs the card up first. DO_UPDATE=False = dry run.
import os, re
from django.core import serializers
from bank.models import rule_math

CARD_IDS, DO_UPDATE = globals()["CARD_IDS"], globals().get("DO_UPDATE", False)
MATH = re.compile(r"(\\\(.*?\\\)|\\\[.*?\\\])", re.S)
FRAC = re.compile(r"\\frac\{[^{}]*\}\{[^{}]*\}")
for cid in CARD_IDS:
    card = rule_math.objects.get(pk=cid, chapter="alligation_n_mixture")
    parts = MATH.split(card.rule_html)
    fixed = [p if i % 2 else FRAC.sub(lambda m: r"\(" + m[0] + r"\)", p) for i, p in enumerate(parts)]
    new = "".join(fixed)
    wrapped = sum(len(FRAC.findall(p)) for i, p in enumerate(parts) if not i % 2)
    print(f"card {cid} {card.rule_name}: {wrapped} stray fractions wrapped")
    if DO_UPDATE and wrapped:
        backup = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\rule_math_{cid}_before_stray_fix.json"
        assert not os.path.exists(backup)
        open(backup, "w", encoding="utf-8").write(serializers.serialize("json", [card], indent=2))
        card.rule_html = new
        card.save(update_fields=["rule_html"])
        card.refresh_from_db()
        print("   saved, re-read equal:", card.rule_html == new, "| backup:", backup)
