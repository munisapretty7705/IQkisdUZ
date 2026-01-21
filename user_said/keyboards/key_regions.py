from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_said.data.region import REGIONS


def region_keyboard():
    buttons = [
        [KeyboardButton(text=region)]
        for region in REGIONS.keys()
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def district_keyboard(region_name: str):
    districts = REGIONS.get(region_name, [])
    buttons = [
        [KeyboardButton(text=district)]
        for district in districts
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
