# ===================== user_said/keyboards/key_language.py =====================
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_said.utils.i18n import t # ==== CHATGPT QO'SHGAN ====

def get_languages_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Uz"), KeyboardButton(text="🇺🇸 En"), KeyboardButton(text="🇷🇺 Ru")]
        ],
        resize_keyboard=True
    )

def registration_keyboard(data):
    lang = data.get("language", "uz")
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang,"menu","register")), KeyboardButton(text=t(lang,"menu","test"))]
        ],
        resize_keyboard=True
    )

def confirm_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang,"responses","registered")), KeyboardButton(text=t(lang,"responses","cancelled"))]
        ],
        resize_keyboard=True
    )

def get_location_type_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "location", "home")),
                KeyboardButton(text=t(lang, "location", "kindergarten"))
            ]
        ],
        resize_keyboard=True
    )


def get_bogcha_type_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "kindergarten", "public")),
                KeyboardButton(text=t(lang, "kindergarten", "private"))
            ]
        ],
        resize_keyboard=True
    )

# ===================== user_said/keyboards/key_language.py =====================
