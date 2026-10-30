# Rule cards pasted into the admin as JSON text (\" quotes, \\( backslashes, literal \n) -> decode back to HTML.
# Backs the card up first. DO_UPDATE=False = dry run.
import json, os
from django.core import serializers
from bank.models import rule_math

CARD_IDS, DO_UPDATE = globals()["CARD_IDS"], globals().get("DO_UPDATE", False)
for cid in CARD_IDS:
    card = rule_math.objects.get(pk=cid, chapter="alligation_n_mixture")
    old = card.rule_html
    new = json.loads('"' + old + '"').replace("\n", "")      # JSON string escapes -> real characters
    assert '\\"' not in new and "\\\\" not in new and "\\(" in new or "\\[" in new, "decode did not give clean HTML"
    print(f"card {cid} {card.rule_name}: {len(old)} -> {len(new)} chars | sample: {new[:120]!r}")
    if DO_UPDATE:
        backup = rf"C:\Users\newwe\Desktop\tution\tutionplus\claude\backups\rule_math_{cid}_before_unescape.json"
        assert not os.path.exists(backup)
        open(backup, "w", encoding="utf-8").write(serializers.serialize("json", [card], indent=2))
        card.rule_html = new
        card.save(update_fields=["rule_html"])
        card.refresh_from_db()
        print("   saved, re-read equal:", card.rule_html == new, "| backup:", backup)
