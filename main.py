import asyncio
from aiogram.filters import Command
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from config import API_TOKEN
from user_said.functions.func import start_commond, set_language, lang_command_answer
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
    dp.startup.register(startup_answer)
    dp.message.register(start_commond, Command("start"))
    dp.message.register(lang_command_answer, Command("lang"))
    dp.message.register(set_language, Form.language)
    dp.shutdown.register(shutdown_answer)

# menu qismlari
    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/lang", description="Tilni o'zgartirish")
        ])

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
