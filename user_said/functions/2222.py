import json
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from user_said.states.statess import Form
# from user_said.keyboards.key_language import get_languages_keyboard, registration_keyboard
from user_said.keyboards.key_language import (
    get_languages_keyboard,
    registration_keyboard,
    get_district_keyboard,
    get_region_keyboard,
    get_location_type_keyboard,get_location_type_keyboard, get_bogcha_type_keyboard,
    confirm_keyboard)
# S.Marjona
# JSON yuklab olamiz
with open("user_said/translations/keyboard_translation.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
# tugmalarning nomlari
LANG_MAP = {
    "🇺🇿 Uz": "uz",
    "🇺🇸 En": "en",
    "🇷🇺 Ru": "ru"
}

# R.Mehriniso 
# start ni ishga tushirish yani botni
async def start_commond(message: Message, state: FSMContext):
    await message.answer(text="Tilni tanlang / Выберите язык / Choose a language:", reply_markup=get_languages_keyboard())
    await state.set_state(Form.language)

# Til tanlangandan keyin welcome text ni chiqarish
async def set_language(message: Message, state: FSMContext):
    lang_code = LANG_MAP.get(message.text, "uz")  # agar boshqa narsa yozilsa default uz
    await state.update_data(language=lang_code)

    await message.answer(
        text=translations[lang_code]["welcome"],
        reply_markup=ReplyKeyboardRemove()
    )

        # 🔥 Til tanlangach darhol menyuni chiqaramiz
    data = await state.get_data()
    await message.answer(
        text="Menu",
        reply_markup=registration_keyboard(data)
    )
    await state.set_state(Form.chose_menu)

async def lang_command_answer(message: Message, state: FSMContext):
    await message.answer(
        text="Tilni tanlang / Выберите язык / Choose a language:",
        reply_markup=get_languages_keyboard()
    )
    await state.set_state(Form.language)


# ---------------- RO‘YXATNI BOSHLASH ----------------
async def start_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(translations[lang]["ask_name"])

    await state.set_state(Form.name)


# ---------------- ISM QABUL QILISH ----------------
async def ask_region(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Endi viloyatingizni tanlang:", reply_markup=get_region_keyboard())
    await state.set_state(Form.viloyat)


# ---------------- VILOYAT QABUL QILISH ----------------
async def ask_district(message: Message, state: FSMContext):
    await state.update_data(viloyat=message.text)
    await message.answer("Endi tumaningizni tanlang:", reply_markup=get_district_keyboard())
    await state.set_state(Form.tuman)


# ---------------- TUMAN QABUL QILISH ----------------
async def ask_location_type(message: Message, state: FSMContext):
    await state.update_data(tuman=message.text)
    await message.answer("Farzandingiz qayerda ta’lim oladi?", reply_markup=get_location_type_keyboard())
    await state.set_state(Form.location_type)


# ---------------- UY / BOG‘CHA TANLASH ----------------
async def process_location_type(message: Message, state: FSMContext):
    location = message.text.strip().lower()
    await state.update_data(location_type=location)

    if "bog‘cha" in location or "bogcha" in location:
        await message.answer("Bog‘changiz turi qanday?", reply_markup=get_bogcha_type_keyboard())
        await state.set_state(Form.bogcha_type)
    else:
        # Agar "Uy" tanlasa — to‘g‘ridan-to‘g‘ri tasdiqlashga o‘tamiz
        await confirm_registration(message, state)


# ---------------- DAVLAT / XUSUSIY ----------------
async def process_bogcha_type(message: Message, state: FSMContext):
    bogcha_type = message.text.strip().lower()
    await state.update_data(bogcha_type=bogcha_type)

    if "davlat" in bogcha_type:
        await message.answer("Iltimos, bog‘changiz raqamini kiriting (masalan: 154):")
        await state.set_state(Form.bogcha_number)
    elif "xususiy" in bogcha_type:
        await confirm_registration(message, state)
    else:
        await message.answer("Iltimos, pastdagi tugmalardan birini tanlang.")


# ---------------- BOG‘CHA RAQAMI ----------------
async def process_bogcha_number(message: Message, state: FSMContext):
    number = message.text.strip()
    await state.update_data(bogcha_number=number)
    await confirm_registration(message, state)


# ---------------- TASDIQLASH EKRANI ----------------
async def confirm_registration(message: Message, state: FSMContext):
    data = await state.get_data()

    summary = (
        f"👤 Ism: {data.get('name')}\n"
        f"📍 Viloyat: {data.get('viloyat')}\n"
        f"🏠 Tuman: {data.get('tuman')}\n"
        f"🏡 Joylashuv: {data.get('location_type')}\n"
    )

    # Agar bog‘cha tanlangan bo‘lsa — qo‘shimcha ma’lumotlarni qo‘shamiz
    if "bog‘cha" in data.get("location_type", ""):
        summary += f"🏫 Bog‘cha turi: {data.get('bogcha_type', '—')}\n"
        if data.get("bogcha_number"):
            summary += f"🔢 Bog‘cha raqami: {data.get('bogcha_number')}\n"

    summary += "\nHammasi to‘g‘rimi?"

    await message.answer(summary, reply_markup=confirm_keyboard())
    await state.set_state(Form.confirm)


# ---------------- YAKUNIY TASDIQLASH ----------------
async def finish_registration(message: Message, state: FSMContext):
    text = (message.text or "").lower()
    if "ha" in text or "tasdiq" in text or "✅" in text:
        data = await state.get_data()
        await message.answer(
            f"✅ Rahmat, {data.get('name')}!\nSiz muvaffaqiyatli ro‘yxatdan o‘tdingiz 🎉",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer("❌ Bekor qilindi. Qayta /start bosing.", reply_markup=ReplyKeyboardRemove())
        await state.clear() 