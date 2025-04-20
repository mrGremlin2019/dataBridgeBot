from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Получить данные", callback_data="get_data"),
            InlineKeyboardButton(text="Сохранить", callback_data="save_data")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
