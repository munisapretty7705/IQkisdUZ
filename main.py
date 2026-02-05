import asyncio
from aiogram.filters import Command
from aiogram import Dispatcher, Bot, F
from aiogram.types import BotCommand
from config import API_TOKEN
from user_said.functions.func import (
    process_region, process_district, confirm_registration, start_registration,
    start_commond, set_language, lang_command_answer,
    process_bogcha_number, process_bogcha_type,
    process_location_type, handle_birth_date, answer_name, handle_menu_choice
)
from user_said.states.statess import Form

from user_said.functions.iq_test import handle_test_command, handle_main_menu
from user_said.keyboards.iq_callbackquery import handle_answer_callback

# S.Marjona
dp = Dispatcher()
async def startup_answer(bot : Bot):
    await bot.send_message(6793352820, "bot ishga tushdi🙌")
async  def shutdown_answer(bot : Bot):
    await bot.send_message(6793352820, "bot ishdan toxtadi")


# R.Mehriniso
# funksiyalarni registerlash
async def main():
    bot = Bot(token=API_TOKEN)
 # startup va shutdown eventlar
    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)

    # 🔸 COMMAND HANDLERLAR
    dp.message.register(start_commond, Command("start"))
    dp.message.register(lang_command_answer, Command("lang"))

    dp.message.register(set_language, Form.language)
    dp.message.register(start_registration, Form.chose_menu)
    # Munisa Akbarovna 
    # Munisa Akbarovna: Ro'yxatdan o'tish bosqichlari

    dp.message(Form.chose_menu)(handle_menu_choice)
    dp.message.register(answer_name, Form.name)
    dp.message.register(handle_birth_date, Form.birth_date)
    dp.message.register(process_region,    Form.viloyat)
    dp.message.register(process_district,  Form.tuman)
    dp.message.register(process_location_type, Form.location_type)
    dp.message.register(process_bogcha_type,   Form.bogcha_type)
    dp.message.register(process_bogcha_number, Form.bogcha_number)
    dp.message.register(confirm_registration,  Form.confirm)

    # Marjona Sultonova  Test yechish qismi
    dp.message.register(handle_test_command, F.text.lower() == "test")
    dp.message.register(handle_main_menu, F.text.lower() == "bosh menu")

    # --- Callback tugmalar uchun ro‘yxatdan o‘tkazish
    dp.callback_query.register(handle_answer_callback, F.data.startswith("answer_"))
   
        
    

# menu qismlari
    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/lang", description="Tilni o'zgartirish")
        ])

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())



