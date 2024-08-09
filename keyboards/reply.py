from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard(buttons_text: list[str], width: int = 4) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in buttons_text:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(width)
    kb = builder.as_markup(one_time_keyboard=True, resize_keyboard=True)
    return kb
