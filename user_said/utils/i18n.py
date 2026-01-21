# ===================== utils/i18n.py =====================
import json

with open("user_said/translations/keyboard_translation.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

def t(lang: str, *keys, default=""):
    # ==== CHATGPT QO'SHGAN ====
    if lang not in TRANSLATIONS:
        lang = "uz"

    data = TRANSLATIONS.get(lang, {})
    for key in keys:
        data = data.get(key)
        if data is None:
            return default or "TEXT_NOT_FOUND"
    return data
# ===================== utils/i18n.py =====================
