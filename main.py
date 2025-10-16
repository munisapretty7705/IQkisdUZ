import asyncio
from aiogram.filters import Command
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from config import API_TOKEN
from user_said.functions.func import ask_region,ask_district,confirm_registration,start_registration,finish_registration,start_commond,set_language,lang_command_answer,ask_location_type,process_bogcha_number,process_bogcha_type,process_location_type
from user_said.states.statess import Form

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
    dp.message.register(ask_region, Form.name)
    dp.message.register(ask_district, Form.viloyat)
    dp.message.register(ask_location_type, Form.tuman)
    dp.message.register(process_location_type, Form.location_type)
    dp.message.register(process_bogcha_type, Form.bogcha_type)
    dp.message.register(process_bogcha_number, Form.bogcha_number)
    
    

# menu qismlari
    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/lang", description="Tilni o'zgartirish")
        ])

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())



