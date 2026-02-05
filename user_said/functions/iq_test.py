import json
from aiogram import  types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from user_said.states.statess import Form

from pathlib import Path

# Fayl joylashgan joydan 3 daraja tepaga chiqamiz (agar IQ_test.py functions ichida bo'lsa)
# Yoki logingizga qarab, aniq loyiha ildizini topamiz:
BASE_DIR = Path(__file__).resolve().parents[2] 

# Agarda yuqoridagi kod baribir 'functions'ni ko'rsatsa, buni ishlating:
# BASE_DIR = Path(__file__).resolve().parent.parent.parent







def age_range(years: int, months: int):
    if years == 3:
        if 0 <= months <= 3:
            return "uchu_bir.json"
        elif 4 <= months <= 6:
            return "uchu_ikki.json"
        elif 7 <= months <= 9:
            return "uchu_uch.json"
        elif 10 <= months <= 11:
            return "uchu_tort.json"

    elif years == 4:
        if 0 <= months <= 3:
            return "tort_bir.json"
        elif 4 <= months <= 6:
            return "tort_ikki.json"
        elif 7 <= months <= 9:
            return "tort_uch.json"
        elif 10 <= months <= 11:
            return "tort_tort.json"

    elif years == 5:
        if 0 <= months <= 3:
            return "besh_bir.json"
        elif 4 <= months <= 6:
            return "besh_ikki.json"
        elif 7 <= months <= 9:
            return "besh_uch.json"
        elif 10 <= months <= 11:
            return "besh_tort.json"

    elif years == 6:
        if 0 <= months <= 3:
            return "olti_bir.json"
        elif 4 <= months <= 6:
            return "olti_ikki.json"
        elif 7 <= months <= 9:
            return "olti_uch.json"
        elif 10 <= months <= 11:
            return "olti_tort.json"

    elif years == 7:
        if 0 <= months <= 3:
            return "yetti_bir.json"
        elif 4 <= months <= 6:
            return "yetti_ikki.json"
        elif 7 <= months <= 9:
            return "yetti_uch.json"
        elif 10 <= months <= 11:
            return "yetti_tort.json"

    return None

from aiogram.types import FSInputFile, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from user_said.keyboards.iq_test_button import generate_option_buttons


async def send_question(message_or_callback: Message | CallbackQuery, state: FSMContext, questions, current: int):
    question = questions[current]
    image_path = question.get("image")
    text = question.get("question_audio", "Savol:")
    options = question.get("options", [])

    # Rasm yuborish (agar bor bo‘lsa)
from aiogram.types import FSInputFile
from pathlib import Path

async def send_question(message_or_callback: Message | CallbackQuery, state: FSMContext, questions, current: int):
    question = questions[current]
    image_path = question.get("image")
    text = question.get("question_audio", "Savol:")
    options = question.get("options", [])

    # Fayl yo‘lini Path sifatida tuzamiz
    if image_path:
        image_file = Path(image_path)
        if image_file.exists():
            photo = FSInputFile(image_file)
            await message_or_callback.answer_photo(photo, caption=text)
        else:
            await message_or_callback.answer(f"⚠️ Rasm topilmadi: {image_path}")
    else:
        await message_or_callback.answer(text)

    # Variant tugmalari
    markup = generate_option_buttons(current, options)
    await message_or_callback.answer("Variantlardan birini tanlang:", reply_markup=markup)


# XATO CHIQAYOTGAN JOY===========================================

async def handle_test_command(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print("STATE:", await state.get_data())



    years = user_data.get("age_years")
    months = user_data.get("age_months")

    if years is None or months is None:
        await message.answer(
            "Iltimos, avval farzandingiz tug‘ilgan sanasini kiriting. /start ni bosing.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    json_file = age_range(years, months)

    if not json_file:
        await message.answer(
            "Xatolik: Yosh oralig‘i aniqlanmadi. /start buyrug‘i bilan qaytadan boshlang.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    try:
        # ASOSIY TUZATISH SHU YERDA:
        # Loyiha ildizidagi IQ_JSON papkasiga kiramiz
        json_path = BASE_DIR / "IQ_JSON" / json_file

        print(f"Tekshirilayotgan to'liq yo'l: {json_path}")

        if not json_path.exists():
            # Agar fayl topilmasa, qayerdan qidirganini foydalanuvchiga ko'rsatamiz
            await message.answer(f"Xatolik: Fayl topilmadi.\nManzil: {json_path}")
            return

        with open(json_path, encoding="utf-8") as f:
            questions = json.load(f)

   
        if not questions:
            await message.answer("Test savollari topilmadi.")
            return

        await state.update_data(
            current_question=0,
            questions=questions,
            score=0
        )

        await send_question(message, state, questions, 0)
        await state.set_state(Form.user_test)

    except FileNotFoundError:
        await message.answer(f"Xatolik: {json_file} fayli topilmadi.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")






# async def handle_test_command(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     age = user_data.get("age")
#     name_surname = user_data.get("name_surname", "Noma'lum")

#     if not age:
#         await message.answer(
#             "Iltimos, avval farzandingiz ma'lumotlarini kiriting. /start buyrug'ini bosing.",
#             reply_markup=types.ReplyKeyboardRemove()
#         )
#         return
# #================================================================================
#     json_file = await age_range(age)
#     if not json_file:
#         await message.answer(
#             "Xatolik: Yosh oralig'i aniqlanmadi. Iltimos, /start buyrug'i bilan qaytadan boshlang.",
#             reply_markup=types.ReplyKeyboardRemove()
#         )
#         return

#     try:
#         with open(f"IQ_JSON/{json_file}", 'r', encoding='utf-8') as f:
#             questions = json.load(f)

#         if not questions:
#             await message.answer("Testlar topilmadi. Iltimos, keyinroq qayta urinib ko'ring.")
#             return

#         # Testni boshlaymiz — birinchi savolni yuboramiz
#         await state.update_data(current_question=0, questions=questions, score=0)
#         await send_question(message, state, questions, 0)

#         await state.set_state(Form.user_test)

#     except FileNotFoundError:
#         await message.answer(f"Xatolik: {json_file} fayli topilmadi.")
#     except Exception as e:
#         await message.answer(f"Xatolik yuz berdi: {str(e)}")



async def handle_main_menu(message: types.Message, state: FSMContext):
    await message.answer(
        "Bosh menyuga qaytdingiz. Yangi test boshlash uchun ma'lumotlarni qaytadan kiriting: /start",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()

    




