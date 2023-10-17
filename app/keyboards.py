from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

set_status_kb = [
    [KeyboardButton(text='Преподователь'),
     KeyboardButton(text='Ученик')]
]

set_status = ReplyKeyboardMarkup(
    keyboard=set_status_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете кто вы'
)