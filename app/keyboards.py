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
cancel_for_create_test = ReplyKeyboardMarkup(
    keyboard=cancel_kb,
    resize_keyboard=True,
    input_field_placeholder='Нажмите для отмены создание теста'
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

set_question_for_test_kb = [
    [KeyboardButton(text='Отмена'),
     KeyboardButton(text='Предпросмотр')]
]
set_question_for_test = ReplyKeyboardMarkup(
    keyboard=set_question_for_test_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт'
)
text_for_choice_for_test_preview = ['Отмена', 'Удалить вопрос', 'Добавить вопрос', 'Опубликовать тест']
choice_for_test_preview_kb = [
    [KeyboardButton(text='Опубликовать тест'),
     KeyboardButton(text='Удалить вопрос'),
     KeyboardButton(text='Добавить вопрос'),
     KeyboardButton(text='Отмена')]
]
choice_for_test_preview = ReplyKeyboardMarkup(
    keyboard=choice_for_test_preview_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт'
)

text_for_choosing_visible_result = ['Да', 'Нет', 'Отмена']
choosing_visible_result_kb = [
    [KeyboardButton(text='Да'),
     KeyboardButton(text='Нет'),
     KeyboardButton(text='Отмена')]
]
choosing_visible_result = ReplyKeyboardMarkup(
    keyboard=choosing_visible_result_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт'
)

text_for_start_solve_test = ['Начать решать', 'Отмена']
start_solve_test_kb = [
    [KeyboardButton(text='Начать решать'),
     KeyboardButton(text='Отмена')]
]
start_solve_test = ReplyKeyboardMarkup(
    keyboard=start_solve_test_kb,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт'
)