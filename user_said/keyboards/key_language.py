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

#   Munisa Akbarovna 
#  ro'yxatdan utish uchun kerak bo'ladigan tugmalar

# 🔹 Viloyat tanlash uchun klaviatura
def get_region_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Toshkent"), KeyboardButton(text="Samarqand")],
            [KeyboardButton(text="Farg‘ona"), KeyboardButton(text="Andijon")],
            [KeyboardButton(text="Buxoro"), KeyboardButton(text="Xorazm")],
            [KeyboardButton(text="Jizzax"), KeyboardButton(text="Qashqadaryo")],
            [KeyboardButton(text="Sirdaryo"), KeyboardButton(text="Surxondaryo")],
            [KeyboardButton(text="Navoiy"), KeyboardButton(text="Namangan")],
            [KeyboardButton(text="Orqaga")]
        ],
        resize_keyboard=True
    )


# 🔹 Tumanni tanlash uchun klaviatura (keyinroq viloyatga qarab dinamik qilamiz)
def get_district_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tuman 1"), KeyboardButton(text="Tuman 2")],
            [KeyboardButton(text="Tuman 3"), KeyboardButton(text="Tuman 4")],
            [KeyboardButton(text="Orqaga")]
        ],
        resize_keyboard=True
    )


# 🔹 Yakuniy tasdiqlash tugmalari
def confirm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tasdiqlash ✅"), KeyboardButton(text="Bekor qilish ❌")]
        ],
        resize_keyboard=True
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_location_type_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Uy"), KeyboardButton(text="Bog'cha")]
        ],
        resize_keyboard=True
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_location_type_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏡 Uy"), KeyboardButton(text="🏫 Bog‘cha")]
        ],
        resize_keyboard=True
    )

def get_bogcha_type_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏛 Davlat"), KeyboardButton(text="🏠 Xususiy")]
        ],
        resize_keyboard=True
    )


