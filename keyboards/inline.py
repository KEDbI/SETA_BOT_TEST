from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button1 = InlineKeyboardButton(text='Выбор 1', callback_data='button1')
button2 = InlineKeyboardButton(text='Выбор 2', callback_data='button2')
inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])