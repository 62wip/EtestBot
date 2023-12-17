from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

text_for_set_status = ['Преподаватель', 'Ученик']
set_status_kb = [
    [KeyboardButton(text='Преподаватель'),
     KeyboardButton(text='Ученик')]
]
set_status = ReplyKeyboardMarkup(
    keyboard=set_status_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Кто вы? 🧐'
)

cancel_kb = [
    [KeyboardButton(text='Отмена')]
]
cancel_for_feedback = ReplyKeyboardMarkup(
    keyboard=cancel_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Нажмите для отмены ❌'
)
cancel_for_create_test = ReplyKeyboardMarkup(
    keyboard=cancel_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Нажмите для отмены создание теста ❌' 
)

text_for_edit_my_profile_for_student = ['ФИО', 'Статус', 'Группа']
edit_my_profile_for_student_kb = [
    [KeyboardButton(text='ФИО')],
    [KeyboardButton(text='Статус')],
    [KeyboardButton(text='Группа')]
]
edit_my_profile_for_student = ReplyKeyboardMarkup(
    keyboard=edit_my_profile_for_student_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Что вы хотите изменить? 🧐'
)

text_for_edit_my_profile_for_teacher = ['ФИО', 'Статус']
edit_my_profile_for_teacher_kb = [
    [KeyboardButton(text='ФИО')],
    [KeyboardButton(text='Статус')]
]
edit_my_profile_for_teacher = ReplyKeyboardMarkup(
    keyboard=edit_my_profile_for_teacher_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Что вы хотите изменить? 🧐'
)

set_question_for_test_kb = [
    [KeyboardButton(text='Предпросмотр')],
    [KeyboardButton(text='Отмена')],
]
set_question_for_test = ReplyKeyboardMarkup(
    keyboard=set_question_for_test_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете пункт из списка 📜'
)
text_for_choice_for_test_preview = ['Отмена', 'Удалить вопрос', 'Добавить вопрос', 'Опубликовать тест']
choice_for_test_preview_kb = [
    [KeyboardButton(text='Опубликовать тест')],
    [KeyboardButton(text='Удалить вопрос'),
     KeyboardButton(text='Добавить вопрос')],
    [KeyboardButton(text='Отмена')]
]
choice_for_test_preview = ReplyKeyboardMarkup(
    keyboard=choice_for_test_preview_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете пункт из списка 📜'
)

text_for_choosing_visible_result = ['Да', 'Нет', 'Отмена']
choosing_visible_result_kb = [
    [KeyboardButton(text='Да'),
     KeyboardButton(text='Нет')],
    [KeyboardButton(text='Отмена')]
]
choosing_visible_result = ReplyKeyboardMarkup(
    keyboard=choosing_visible_result_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете пункт из списка 📜'
)

text_for_start_solve_test = ['Начать решать', 'Отмена']
start_solve_test_kb = [
    [KeyboardButton(text='Начать решать')],
    [KeyboardButton(text='Отмена')]
]
start_solve_test = ReplyKeyboardMarkup(
    keyboard=start_solve_test_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете пункт из списка 📜'
)

async def markup_for_answers(answers: list) -> ReplyKeyboardMarkup:
    answers_kb = []
    for i in range(len(answers)):
        answers_kb.append([KeyboardButton(text=f'{i + 1}) {answers[i]}')])
    result_answers = ReplyKeyboardMarkup(
    keyboard=answers_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете ответ 💥'
    )
    return result_answers

text_for_choice_for_result_preview = ['Отмена', 'Изменить ответ', 'Завершить тест']
choice_for_result_preview_kb = [
    [KeyboardButton(text='Изменить ответ'),
     KeyboardButton(text='Завершить тест')],
    [KeyboardButton(text='Отмена')]
]
choice_for_result_preview = ReplyKeyboardMarkup(
    keyboard=choice_for_result_preview_kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете пункт из списка 📜'
    )

show_more_result_kb = [
    [InlineKeyboardButton(text='Подробнее 🔎', callback_data='show_more_test_result')]
]
show_more_result = InlineKeyboardMarkup(
    inline_keyboard=show_more_result_kb
)

async def markup_for_choice_for_now_test(visible_result: bool, bool_test_result: False or list):
    choice_for_now_test_kb = [
    [InlineKeyboardButton(text='Предпросмотр теста 📢', callback_data='preview_for_now_test')]
]
    if visible_result:
        choice_for_now_test_kb.append([InlineKeyboardButton(text='Скрыть подробные результаты', callback_data='make_invisible_result_for_now_test')])
    else:
        choice_for_now_test_kb.append([InlineKeyboardButton(text='Открыть подробные результаты', callback_data='make_visible_result_for_now_test')])
    if bool_test_result is False:
        choice_for_now_test_kb.append([InlineKeyboardButton(text='Удалить тест', callback_data='delete_now_test')])
    choice_for_now_test = InlineKeyboardMarkup(
        inline_keyboard=choice_for_now_test_kb
    )
    return choice_for_now_test

back_for_now_test_kb = [
    [InlineKeyboardButton(text='Назад', callback_data='back_for_now_test')]
    
]
back_for_now_test = InlineKeyboardMarkup(
    inline_keyboard=back_for_now_test_kb
)

choice_for_delete_now_test_kb = [
    [InlineKeyboardButton(text='Да', callback_data='confirmed_delete_now_test'),
     InlineKeyboardButton(text='Отмена', callback_data='back_from_delete_now_test')]
]
choice_for_delete_now_test = InlineKeyboardMarkup(
    inline_keyboard=choice_for_delete_now_test_kb
)


show_more_for_now_test_result_kb = [
    [InlineKeyboardButton(text='Смотреть подробнее', callback_data='show_more_for_now_test_result')]
]
show_more_for_now_test_result = InlineKeyboardMarkup(
    inline_keyboard=show_more_for_now_test_result_kb
)