from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

text_for_set_status = ['Преподаватель', 'Ученик']
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
    input_field_placeholder='Нажмите для отмены'
)

text_for_edit_my_profile_for_student = ['ФИО', 'Статус', 'Группа']
edit_my_profile_for_student_kb = [
    [KeyboardButton(text='ФИО'),
    KeyboardButton(text='Статус'),
    KeyboardButton(text='Группа')]
]
edit_my_profile_for_student = ReplyKeyboardMarkup(
    keyboard=edit_my_profile_for_student_kb,
    resize_keyboard=True,
    input_field_placeholder='Что вы хотите изменить'
)

text_for_edit_my_profile_for_teacher = ['ФИО', 'Статус']
edit_my_profile_for_teacher_kb = [
    [KeyboardButton(text='ФИО'),
    KeyboardButton(text='Статус')]
]
edit_my_profile_for_teacher = ReplyKeyboardMarkup(
    keyboard=edit_my_profile_for_teacher_kb,
    resize_keyboard=True,
    input_field_placeholder='Что вы хотите изменить'
)