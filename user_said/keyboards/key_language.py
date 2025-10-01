import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# R.Mehriniso
# Til tugmalarini yaratish
def get_languages_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 Uz"),
                KeyboardButton(text="🇺🇸 En"),
                KeyboardButton(text="🇷🇺 Ru")
            ]
        ],
        resize_keyboard=True
    )

# S.Marjona
# Menu tugmalarini yaratish yani Ro'yxatdan o'tish va oddiy test qism tugmalari
def translate_into(path: str, data: dict):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
# tarjimasini olish uchun qo'llangan
def registration_keyboard(data):
    path = "user_said/translations/keyboard_translation.json"
    translations = translate_into(path, data)

    lang = data.get("language", "uz")  # 🔑 nomini `language` qildik

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations[lang]["menu"]["start_test"]),
                KeyboardButton(text=translations[lang]["menu"]["history"])
            ]
        ],
        resize_keyboard=True
    )

