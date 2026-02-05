from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(keyboard=[
    [
            KeyboardButton(text="Test"),
            KeyboardButton(text="Bosh menu")
    ],
],
        resize_keyboard=True
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_option_buttons(question_index: int, options: list[str]):
    buttons = [
        [InlineKeyboardButton(text=f"{i+1}- {option}", callback_data=f"answer_{question_index}_{i}")]
        for i, option in enumerate(options)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

