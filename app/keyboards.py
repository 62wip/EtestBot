from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

set_status_kb = [
    [KeyboardButton(text='Преподаватель'),
     KeyboardButton(text='Ученик')]
]
set_status = ReplyKeyboardMarkup(
    keyboard=set_status_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете кто вы'
)

cancel_kb = [
    [KeyboardButton(text='Отмена')]
]
cancel_for_feedback = ReplyKeyboardMarkup(
    keyboard=cancel_kb,
    resize_keyboard=True,
    input_field_placeholder='Нажмите для отмены или напишите сообщение'
)