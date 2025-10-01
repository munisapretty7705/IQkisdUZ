import json
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from user_said.states.statess import Form
from user_said.keyboards.key_language import get_languages_keyboard, registration_keyboard

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

async def lang_command_answer(message:Message, state: FSMContext):
    await message.answer(text="Tilni tanlang / Выберите язык / Choose a language:",reply_markup=get_languages_keyboard())
    await state.set_state(Form.language)





