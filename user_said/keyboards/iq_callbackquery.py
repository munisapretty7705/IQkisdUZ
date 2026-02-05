from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types


async def handle_answer_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    current = data.get("current_question", 0)
    score = data.get("score", 0)

    parts = callback.data.split("_")  # Masalan: answer_0_2
    q_index = int(parts[1])
    chosen = int(parts[2])

    # Allaqachon o‘tgan savolni bosib yuborsa
    if q_index != current:
        await callback.answer("Bu savolga allaqachon javob berilgan!", show_alert=True)
        return

    correct_answer = questions[q_index]["answer"] - 1  # ❗ sizning JSON 1-dan boshlangan
    if chosen == correct_answer:
        score += 1

    current += 1
    await state.update_data(current_question=current, score=score)

    if current < len(questions):
        from user_said.functions.iq_test import send_question  # Import qiling yoki tepaga olib chiqing
        await send_question(callback.message, state, questions, current)
    else:
        # Test yakunlangan
        total = len(questions)
        percent = round(score / total * 100)

        result_text = (
            f"📊 Test yakunlandi!\n\n"
            f"✅ To‘g‘ri javoblar soni: {score} / {total}\n"
            f"📈 Foiz: {percent}%\n\n"
            f"Yana test topshirish uchun /start buyrug‘ini bosing."
        )

        await callback.message.answer(result_text)
        await state.clear()

    await callback.answer()
