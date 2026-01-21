# ===================== user_said/functions/func.py =====================
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from user_said.states.statess import Form
from user_said.keyboards.key_language import (
    get_languages_keyboard, registration_keyboard, confirm_keyboard,
    get_location_type_keyboard, get_bogcha_type_keyboard
)
from user_said.keyboards.key_regions import region_keyboard, district_keyboard
from user_said.utils.i18n import t  # ==== CHATGPT QO'SHGAN ====

# Tugmalar va til kodi map
LANG_MAP = {
    "🇺🇿 Uz": "uz",
    "🇺🇸 En": "en",
    "🇷🇺 Ru": "ru"
}

# ================= START / TIL TANLASH =================
async def start_commond(message: Message, state: FSMContext):
    await message.answer(
        text="Tilni tanlang / Выберите язык / Choose a language:",
        reply_markup=get_languages_keyboard()
    )
    await state.set_state(Form.language)

async def set_language(message: Message, state: FSMContext):
    lang_code = LANG_MAP.get(message.text, "uz")
    await state.update_data(language=lang_code)
    await message.answer(
        text=t(lang_code, "welcome"),
        reply_markup=ReplyKeyboardRemove()
    )
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

# ================= RO‘YXAT BOSHLASH =================
async def start_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(t(lang, "ask_name"))
    await state.set_state(Form.name)

# ================= ISM QABUL QILISH =================
async def ask_region(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====
    await message.answer(t(lang,"ask_region"), reply_markup=region_keyboard())
    await state.set_state(Form.viloyat)

async def ask_district(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====
    await state.update_data(viloyat=message.text)
    await message.answer(t(lang,"ask_district"), reply_markup=district_keyboard(data.get("viloyat")))
    await state.set_state(Form.tuman)

async def ask_location_type(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====
    await state.update_data(tuman=message.text)
    await message.answer(
        t(lang,"ask_location_type"),
        reply_markup=get_location_type_keyboard(lang)
    )
    await state.set_state(Form.location_type)

# ================= UY / BOG‘CHA =================
async def process_location_type(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====

    text = message.text

    if text == t(lang, "location", "kindergarten"):
        await state.update_data(location_type="kindergarten")
        await message.answer(
            t(lang,"ask_bogcha_type"),
            reply_markup=get_bogcha_type_keyboard(lang)
        )
        await state.set_state(Form.bogcha_type)

    elif text == t(lang, "location", "home"):
        await state.update_data(location_type="home")
        await confirm_registration(message, state)

    else:
        await message.answer(t(lang, "errors", "choose_button"))

# ================= DAVLAT / XUSUSIY =================
async def process_bogcha_type(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====

    text = message.text

    if text == t(lang, "kindergarten", "public"):
        await state.update_data(bogcha_type="public")
        await message.answer(t(lang,"ask_bogcha_number"))
        await state.set_state(Form.bogcha_number)

    elif text == t(lang, "kindergarten", "private"):
        await state.update_data(bogcha_type="private")
        await confirm_registration(message, state)

    else:
        await message.answer(t(lang, "errors", "choose_button"))

# ================= BOG‘CHA RAQAMI =================
async def process_bogcha_number(message: Message, state: FSMContext):  # ==== CHATGPT QO'SHGAN ====
    data = await state.get_data()
    lang = data.get("language","uz")
    number = message.text.strip()
    await state.update_data(bogcha_number=number)
    await confirm_registration(message, state)

# ================= TASDIQLASH =================
async def confirm_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====

    location_key = data.get("location_type")
    location_label = t(lang, "location", location_key) if location_key else "—"

    summary = (
        f"👤 {t(lang,'ask_name')} {data.get('name')}\n"
        f"📍 {t(lang,'ask_region')} {data.get('viloyat')}\n"
        f"🏠 {t(lang,'ask_district')} {data.get('tuman')}\n"
        f"🏡 {location_label}\n"
    )

    if location_key == "kindergarten":
        bogcha_key = data.get("bogcha_type")
        bogcha_label = t(lang, "kindergarten", bogcha_key) if bogcha_key else "—"
        summary += f"🏫 {bogcha_label}\n"

        if data.get("bogcha_number"):
            summary += f"🔢 {t(lang,'ask_bogcha_number')}: {data.get('bogcha_number')}\n"

    summary += f"\n{t(lang,'confirm_question')}"

    await message.answer(summary, reply_markup=confirm_keyboard(lang))
    await state.set_state(Form.confirm)

# ================= YAKUNIY TASDIQLASH =================
async def finish_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language","uz")  # ==== CHATGPT QO'SHGAN ====

    text = (message.text or "").lower()

    if "ha" in text or "yes" in text or "да" in text or "✅" in text:
        await message.answer(
            t(lang,"responses","registered"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(
            t(lang,"responses","cancelled"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
