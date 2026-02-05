# ===================== user_said/functions/func.py =====================
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from user_said.states.statess import Form
from aiogram import Bot
from user_said.keyboards.key_language import (
    get_languages_keyboard, registration_keyboard, confirm_keyboard,
    get_location_type_keyboard, get_bogcha_type_keyboard
)

from user_said.keyboards.iq_test_button import main_menu
from datetime import datetime
from user_said.keyboards.key_regions import region_keyboard, district_keyboard
from user_said.utils.i18n import t ,TRANSLATIONS, add_ariza_line, send_ariza_to_admin

#---------------R.Mehriniso
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

# async def set_language(message: Message, state: FSMContext):
#     lang_code = LANG_MAP.get(message.text, "uz")
#     await state.update_data(language=lang_code)
#     await message.answer(
#         text=t(lang_code, "welcome"),
#         reply_markup=ReplyKeyboardRemove()
#     )
#     data = await state.get_data()
#     await message.answer(
#         text="Menu",
#         reply_markup=registration_keyboard(data)
#     )
#     await state.set_state(Form.chose_menu)

# 

async def set_language(message: Message, state: FSMContext):
    # 1. Tilni aniqlash va saqlash (bu juda muhim, keyingi t(lang, ...) funksiyalari uchun)
    lang = LANG_MAP.get(message.text, "uz")
    await state.update_data(language=lang)
    data = await state.get_data()
    text = t(lang, "welcome")

    # 3. Klaviaturani o'chirish va matnni yuborish
    await message.answer(text, reply_markup=registration_keyboard(data))
    
    await state.set_state(Form.chose_menu)

# ================= MENYU TANLOVINI BOSHQARISH =================
async def handle_menu_choice(message: Message, state: FSMContext):
    text = message.text
    
    # 1. Registratsiya tugmasi bosilganda
    # (Tugma matnida 'Registratsiya' yoki 'Registration' so'zi bo'lsa)
    if "Registratsiya" in text or "Registration" in text or "Регистрация" in text:
        await start_registration(message, state)
        
    # 2. Oddiy IQ Test (Tasodifiy) tugmasi bosilganda
    # (Tugma matnida 'IQ Test' yoki 'Тест' so'zi bo'lsa)
    elif "IQ Test" in text or "Тест" in text:
        await start_random_iq_test(message, state)
        
    else:
        # Agar foydalanuvchi boshqa narsa yozsa
        await message.answer("Iltimos, pastdagi tugmalardan birini tanlang.")
        
    
 # =========Bu tilni qaytadan o'zgartirish=============

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
    await message.answer(t(lang, "ask_name"),)
    await state.set_state(Form.name)
    
# ==================ISM kiritish===================
async def answer_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")

    text = message.text.strip()
    parts = text.split()

    if len(parts) == 2:
        if not any(char.isdigit() for char in text):  # raqam bor-yo‘qligini yaxshiroq tekshirish
            await state.update_data(full_name=text)          # ← yaxshi nom: full_name
            await message.answer(t(lang, "ans_name").format(name=text))
            await message.answer(t(lang, "ask_birth"))
            await state.set_state(Form.birth_date)
        else:
            await message.answer(t(lang, "name_try1"))
    else:
        await message.answer(t(lang, "true_name"))

# ================= Yosh kiritish ========================


async def handle_birth_date(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
 
    try:
        # Sana formatini tekshirish
        birth_date = datetime.strptime(message.text.strip(), "%d.%m.%Y")
        current_date = datetime.now()

        # Yoshni hisoblash (yil va oylar)
        years = current_date.year - birth_date.year
        months = current_date.month - birth_date.month

        if current_date.day < birth_date.day:
            months -= 1
        if months < 0:
            years -= 1
            months += 12
# BU YERNI HAM TO'G'IRLASH KERAK==================================================


        # Faqat 3–7 yosh oralig‘idagilar
        if 3 <= years <= 7:
#      =================================================================================
# ... yosh hisoblangandan keyin
            await state.update_data(
                birth_date=message.text,
                age_years=years,
                age_months=months,
                full_name=data.get("full_name")
            )

            await message.answer(
                t(lang, "ans_age").format(
                name=data.get("full_name"),
                years=years,
                months=months
                )
            )
            await message.answer(t(lang, "ask_region"), reply_markup=region_keyboard())
            await state.set_state(Form.viloyat)
            
        else:
            await message.answer(
                t(lang, "age_try"), reply_markup=ReplyKeyboardRemove()
            )
            # await state.clear()

    except ValueError:
        await message.answer(t(lang , "date_try"),
            parse_mode="Markdown"
        )



# ================= Viloyat QABUL QILISH =================

async def process_region(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    await state.update_data(viloyat=message.text)
    await message.answer(t(lang, "ans_region").format(region=message.text))
    await message.answer(
        t(lang, "ask_district"),
        reply_markup=district_keyboard(message.text)
    )
    await state.set_state(Form.tuman)


# Tuman qabul qilish
async def process_district(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    await state.update_data(tuman=message.text)
    await message.answer(t(lang, "ans_district").format(district=message.text))
    await message.answer(
        t(lang, "ask_location_type"),
        reply_markup=get_location_type_keyboard(lang)
    )
    await state.set_state(Form.location_type)







# ========================= Alohida arizalarni yig'adi===================

ADMIN_ID = 6793352820
# ================= UY / BOG‘CHA =================
async def process_location_type(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    choice = message.text.strip()  # bo'shliqlar bo'lsa ham tozalab olamiz

    # Har bir til uchun mumkin bo'lgan tugma matnlari (emoji bilan va emojisiz)
    home_options = {
        "uz": ["🏡 Uy", "Uy"],
        "en": ["🏡 Home", "Home"],
        "ru": ["🏡 Дом", "Дом"]
    }

    kindergarten_options = {
        "uz": ["🏫 Bog‘cha", "Bog‘cha"],
        "en": ["🏫 Kindergarten", "Kindergarten"],
        "ru": ["🏫 Детский сад", "Детский сад"]
    }

    # Uy tanlanganmi?
    if choice in home_options.get(lang, []):
        await state.update_data(location_type="home")
        await message.answer(t(lang, "ans_home"))  # .format kerak emas, chunki shablon yo'q

        home_translation = TRANSLATIONS[lang]
        home_translations = t(lang, 'location')
        
        # Ariza matni (foydalanuvchi tilida)
        ariza = (
            f"{TRANSLATIONS[lang].get('applicant','Ariza beruvchi')}: {data.get('name', data.get('full_name', '—'))}\n"
            f"{TRANSLATIONS[lang].get('age','Yoshi')}: {data.get('age_years', '?')} , {TRANSLATIONS[lang].get('year','yil')} , {data.get('age_months', '?')} {TRANSLATIONS[lang].get('month','oy')}:\n"
            f"{TRANSLATIONS[lang].get('region','Viloyat')}: {data.get('viloyat', '—')}\n"
            f"{TRANSLATIONS[lang].get('district','Tuman')}: {data.get('tuman', '—')}\n"    
            f"{TRANSLATIONS[lang].get('homea','Ta\'lim olish joyi')}: {home_translations['home']}"
        )
        
        await message.answer(
            t(lang, "ariza_qabuli") + "\n\n" + ariza + "\n\n" + t(lang, "ariza_qabuli1"),
            reply_markup=confirm_keyboard(lang)
        )
        # await send_ariza_to_admin(message.bot, state, lang, ADMIN_ID)
        await state.set_state(Form.confirm)

    # Bog'cha tanlanganmi?
    elif choice in kindergarten_options.get(lang, []):
        await state.update_data(location_type="kindergarten")
        await message.answer(t(lang, "ans_kin"))
        kinder_trans = t(lang, 'location')

        await message.answer(
            t(lang, "ask_bogcha_type"),
            reply_markup=get_bogcha_type_keyboard(lang)
        )
        await state.set_state(Form.bogcha_type)


    else:
        await message.answer(t(lang, "errors.choose_button") or "Iltimos, tugmalardan birini tanlang.")

# ================= DAVLAT / XUSUSIY =================
async def process_bogcha_type(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    choice = message.text.strip()

    public_options = {
        "uz": ["🏛 Davlat", "Davlat"],
        "en": ["🏛 Public", "Public"],
        "ru": ["🏛 Государственный", "Государственный"]
    }
    private_options = {
        "uz": ["🏠 Xususiy", "Xususiy"],
        "en": ["🏠 Private", "Private"],
        "ru": ["🏠 Частный", "Частный"]
    }

 

    if choice in public_options.get(lang, []):
        await state.update_data(bogcha_type="public")
        await message.answer(t(lang, "loc_pub"))
        await message.answer(t(lang, "ask_bogcha_number"))
        await state.set_state(Form.bogcha_number)

    elif choice in private_options.get(lang, []):
        await state.update_data(bogcha_type="private")
        await message.answer(t(lang, "loc_pri"))

        # Ariza tayyorlash (xususiy uchun)
        kinder_trans = t(lang, 'location')
        ta_lim_joyi = t(lang, 'kindergarten')

        ariza_1 = (
            f"{TRANSLATIONS[lang].get('applicant','Ariza beruvchi')}: "
            f"{data.get('name', data.get('full_name', '—'))}\n"

            f"{TRANSLATIONS[lang].get('age','Yoshi')}: "
            f"{data.get('age_years','?')} {TRANSLATIONS[lang].get('year','yil')} "
            f"{data.get('age_months','?')} {TRANSLATIONS[lang].get('month','oy')}\n"

            f"{TRANSLATIONS[lang].get('region','Viloyat')}: "
            f"{data.get('viloyat','—')}\n"

            f"{TRANSLATIONS[lang].get('district','Tuman')}: "
            f"{data.get('tuman','—')}\n"

            f"{TRANSLATIONS[lang].get('homea','Ta\'lim olish joyi')}:" 
            f"{kinder_trans['kindergarten']}\n"

            f"{TRANSLATIONS[lang].get('kindergarten_type',"Bog\'cha turi")}: "
            f"{ta_lim_joyi['private']}"
)


        await message.answer(
            t(lang, "ariza_qabuli") + "\n\n" + ariza_1 + "\n\n" + t(lang, "ariza_qabuli1"),
            reply_markup=confirm_keyboard(lang)
        )
        # await send_ariza_to_admin(message.bot, state, lang, ADMIN_ID)
        await state.set_state(Form.confirm)

    else:
        await message.answer(t(lang, "errors.choose_button") or "Iltimos, tugmalardan birini tanlang.")
# ================= BOG‘CHA RAQAMI =================
async def process_bogcha_number(message: Message, state: FSMContext):  
    data = await state.get_data()
    lang = data.get("language","uz")
    number = message.text.strip()
    await state.update_data(bogcha_number=number)
    await message.answer(t(lang, "b_num"))  

    # To'g'ri ariza yig'ish
    kinder_trans = t(lang, 'location')
    ta_lim_joyi = t(lang, 'kindergarten')

    ariza_2 = (
            f"{TRANSLATIONS[lang].get('applicant','Ariza beruvchi')}: "
            f"{data.get('name', data.get('full_name', '—'))}\n"

            f"{TRANSLATIONS[lang].get('age','Yoshi')}: "
            f"{data.get('age_years','?')} {TRANSLATIONS[lang].get('year','yil')} "
            f"{data.get('age_months','?')} {TRANSLATIONS[lang].get('month','oy')}\n"

            f"{TRANSLATIONS[lang].get('region','Viloyat')}: "
            f"{data.get('viloyat','—')}\n"

            f"{TRANSLATIONS[lang].get('district','Tuman')}: "
            f"{data.get('tuman','—')}\n"

            f"{TRANSLATIONS[lang].get('homea','Ta\'lim olish joyi')}:" 
            f"{kinder_trans['kindergarten']}\n"

            f"{TRANSLATIONS[lang].get('kindergarten_type',"Bog\'cha turi")}: "
            f"{ta_lim_joyi['private']}\n"
            f"{TRANSLATIONS[lang].get('kindergarten_number','Bog\'cha raqami')}: "
            f"{number}"
    )
    await message.answer(
        t(lang, "ariza_qabuli") + "\n\n" + ariza_2 + "\n\n" + t(lang, "ariza_qabuli1"),
        reply_markup=confirm_keyboard(lang)
    )
    # await send_ariza_to_admin(message.bot, state, lang, ADMIN_ID)
    await state.set_state(Form.confirm)
   

# ================= TASDIQLASH =================
async def confirm_registration(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    # Matnni tozalaymiz va kichik harfga o'tkazamiz
    text = message.text.strip().lower()
    
    # "ha" ni aniqlash uchun kalit so'zlar (ko'p variant)
    ha_keywords = ["ha", "yes", "да", "ҳа", "хоп", "ok"]
    
    # "yo'q" ni aniqlash uchun kalit so'zlar (lotin + kirill + turli apostrof)
    yoq_keywords = ["yo'q", "yo‘q", "yoq", "йўқ", "нет", "no", "y", "yo"]

    # Agar matnda yuqoridagi so'zlardan birortasi bo'lsa → HA deb hisoblaymiz
    if any(keyword in text for keyword in ha_keywords):
        # ----------------- Ariza qabul qilindi bloki -----------------
        kinder_trans = t(lang, 'location')
        ta_lim_joyi = t(lang, 'kindergarten')

        ariza_3 = (
            f"{TRANSLATIONS[lang].get('applicant','Ariza beruvchi')}: "
            f"{data.get('name', data.get('full_name', '—'))}\n"

            f"{TRANSLATIONS[lang].get('age','Yoshi')}: "
            f"{data.get('age_years','?')} {TRANSLATIONS[lang].get('year','yil')} "
            f"{data.get('age_months','?')} {TRANSLATIONS[lang].get('month','oy')}\n"

            f"{TRANSLATIONS[lang].get('region','Viloyat')}: "
            f"{data.get('viloyat','—')}\n"

            f"{TRANSLATIONS[lang].get('district','Tuman')}: "
            f"{data.get('tuman','—')}\n"

            f"{TRANSLATIONS[lang].get('homea','Ta\'lim olish joyi')}:" 
            f"{kinder_trans['kindergarten']}\n"

            f"{TRANSLATIONS[lang].get('kindergarten_type',"Bog\'cha turi")}: "
            f"{ta_lim_joyi['private']}\n"
            f"{TRANSLATIONS[lang].get('kindergarten_number','Bog\'cha raqami')}: "
            f"{data.get('bogcha_number')}"
    )
        
        await bot.send_message(ADMIN_ID, t(lang, "new_ariza") + "\n\n" + ariza_3)
        await send_ariza_to_admin(message.bot, state, lang, ADMIN_ID)
        await message.answer(t(lang, "ariza_q"), reply_markup=main_menu, parse_mode="Markdown")
          # "Ariza qabul qilindi" degan xabar
        

    # Agar matnda yo'q kalit so'zlaridan biri bo'lsa → BEKOR
    elif any(keyword in text for keyword in yoq_keywords):
        await message.answer(t(lang, "ariza_cancel"))  # "Ariza bekor qilindi"
        await state.clear()

    else:
        # Foydalanuvchiga yana ha/yo'q so'rash
        await message.answer(t(lang, "ariza_qabuli1"))
        # state ni tozalamaymiz → qayta yozsin

    await state.set_state(Form.user_test)







import os
import random
import json
from pathlib import Path
from user_said.functions.iq_test import send_question, BASE_DIR

# ================= ODDIY (TASODIFIY) TEST BOSHLASH =================
async def start_random_iq_test(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    # JSON fayllar turgan papka manzili
    json_folder = BASE_DIR / "IQ_JSON"
    
    try:
        # Papka ichidagi hamma .json fayllarni qidiramiz
        all_jsons = [f for f in os.listdir(json_folder) if f.endswith('.json')]
        
        if not all_jsons:
            await message.answer("Xatolik: IQ_JSON papkasida fayllar topilmadi.")
            return

        # Tasodifiy bitta fayl nomini tanlaymiz (masalan: 'besh_bir.json')
        chosen_file = random.choice(all_jsons)
        
        # Faylni ochib ichidagi savollarni yuklaymiz
        with open(json_folder / chosen_file, encoding="utf-8") as f:
            questions = json.load(f)

        # Bot xotirasiga (state) savollarni saqlaymiz
        await state.update_data(
            current_question=0,
            questions=questions,
            score=0
        )

        await message.answer("Test boshlanmoqda... Omad!")
        
        # IQ_test.py ichidagi send_question funksiyasini chaqiramiz
        await send_question(message, state, questions, 0)
        
        # Holatni test rejimiga o'tkazamiz
        await state.set_state(Form.user_test)

    except Exception as e:
        await message.answer(f"Tizimda xatolik: {str(e)}")