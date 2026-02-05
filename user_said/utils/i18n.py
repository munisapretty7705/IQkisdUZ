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

# from utils.i18n import t

async def add_ariza_line(state, lang, key, value):
    """State ichida ariza satrlarini yig‘ish"""
    data = await state.get_data()
    lines = data.get("ariza_lines", [])
    lines.append(f"{t(lang, key)}: {value}")
    await state.update_data(ariza_lines=lines)

async def send_ariza_to_admin(bot, state, lang, admin_id):
    """Adminga arizani yuborish"""
    data = await state.get_data()
    ariza_lines = data.get("ariza_lines", [])
    ariza_text = "\n".join(ariza_lines)
    await bot.send_message(admin_id, t(lang, "new_ariza") + "\n\n" + ariza_text)



