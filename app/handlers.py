from uuid import uuid4
import re
from datetime import datetime

from typing import Any
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery 
from aiogram.filters import Filter, Command

import app.keyboards as kb
from app.state import Form
from app.database.requests import Connection
from app.database.models import *
from config import TG_ID


router = Router()
connection = Connection()
data_for_show_result = {}

async def check_first_use(message, state: FSMContext) -> None:
    if connection.checking_first_use(message.from_user.id):
        await message.answer('Вижу ты тут <u>новенький</u>, позволь узнать твои данные, которые <b>будут отображаться у других пользователей</b>!', parse_mode="HTML")
        await message.answer('Укажите свое <i>ФИО</i>.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_fio) # Устанавливаем состояние ожидания ФИО

async def message_for_profile(user_id: int) -> str:
    user_data = connection.select_for_user_class(user_id)
    answer = f'''<u><b>Ваш профиль</b></u>:
<i>ФИО(отображаемое имя)</i>: {user_data.fio}
<i>Телеграм ID:</i> {user_data.user_id}\n'''
    if user_data.status == 'T':
        answer += '<i>Статус</i>: Преподователь'
    elif user_data.status == 'S':
        answer += f'<i>Статус</i>: Ученик\n<i>Группа/класс</i>: {user_data.group}'
    return answer

async def message_for_test_preview(user_id: int, state: FSMContext) -> str:
    context_data = await state.get_data()
    user_data = connection.select_for_user_class(user_id)
    answer = f'''<b><u>Предпосмотр теста</u></b>:

<b>Тест "{context_data.get('test_name')}"</b>
'''
    if context_data.get('test_subject') != None:
        answer += f'<i>Предмет</i>: {context_data.get("test_subject")}\n'
    answer += f'''<i>Автор</i>: {user_data.fio}

<u>Вопросы:</u>
'''
    for i in range(len(context_data.get('questions'))):
        answer += f'<b>{i + 1}.</b> {context_data.get("questions")[i]}\n'
        for g in range(len(context_data.get('answers')[i])):
            if context_data.get('right_answers')[i] == g + 1:
                answer += '✔️'
            else:
                answer += ' '
            answer += f' <i>{g + 1})</i> {context_data.get("answers")[i][g]}\n'
            
    return answer

async def message_for_finded_test(test: Test):
    answer = f'''<u>Тест найден</u>

<b>Тест "{test.test_name}"</b>
'''
    if test.subject_name != None:
        answer += f'<i>Предмет</i>: {test.subject_name}\n'
    test_author = connection.select_for_user_class(test.creator_user_id)
    answer += f'''<i>Автор</i>: {test_author.fio}
Время создания: {str(test.creation_time)}

<u>Вопросы:</u>
'''
    for i in range(len(test.all_questions)):
        answer += f'<b>{i + 1}.</b> {test.all_questions[i]}\n'
        for g in range(len(test.all_answers[i])):
            answer += f' <i>{g + 1})</i> {test.all_answers[i][g]}\n'
    return answer

async def message_for_result_review(state: FSMContext) -> str:
    context_data = await state.get_data()
    test:Test = context_data.get('test')
    answer = f'''<b><u>Предпосмотр решения</u></b>:

<b>Тест "{test.test_name}"</b>

<u>Ответы на вопросы:</u>
'''
    for i in range(len(test.all_questions)):
        answer += f'<b>{i + 1}.</b> {test.all_questions[i]}\n'
        for g in range(len(test.all_answers[i])):
            if context_data.get('test_result')[i][0] == 1:
                if test.right_answers[i] == g + 1:
                    answer += '✔️'
                else:
                    answer += ' '
            else:
                if context_data.get('test_result')[i][1] == g + 1:
                    answer += '✔️'
                else:
                    answer += ' '
            answer += f'<i>{g + 1})</i> {test.all_answers[i][g]}\n'
    return answer

async def message_for_answer_question(now_question: int, test: Test) -> str:
    answer = f'<i>Вопрос №{now_question + 1}</i>\n{test.all_questions[now_question]}\n'
    for i in range(len(test.all_answers[now_question])):
        answer += f' {i + 1}) {test.all_answers[now_question][i]}\n'
    return answer

async def message_for_show_more_test_result(test: Test, test_result: TestResult) -> str:
    user_data = connection.select_for_user_class(test.creator_user_id)
    answer = f'<b>Результаты теста "{test.test_name}"</b>\n'
    if test.subject_name != None:
        answer += f'<i>Предмет:</i> {test.subject_name}\n'
    answer += f'''<i>Автор</i>: {user_data.fio}

<u>Ответы на вопросы:</u>
'''
    for i in range(len(test.all_questions)):
        answer += f'<b>{i + 1}.</b> {test.all_questions[i]}\n'
        for g in range(len(test.all_answers[i])):
            if test.right_answers[i] == g + 1:
                answer += '✔️'
            elif [k[1] for k in test_result.answers_with_mistakes if i + 1 == k[0]] == [g + 1]:
                answer += '❌'
            else:
                answer += ' '
            answer += f'<i>{g + 1})</i> {test.all_answers[i][g]}\n'
    return answer


# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext) -> None:
    # Отправляем сообщение в ответ на команду /start
    await message.answer(f'Здравствуй, <u>{message.from_user.first_name}</u>! Это бот создан специально для <i>создания/решения тестов</i> онлайн.', parse_mode="HTML")
    await check_first_use(message, state)

# Обработчик команды /how_to_use
@router.message(Command('how_to_use'))
async def how_to_use_command(message: Message) -> None:
    # Отправляем сообщение в ответ на команду /how_to_use
    await message.answer('''1. Чтобы посмотреть статистику или изметить профиль, пропишите /my_profile
2. Если вы хотите создать тест, пропришите /create_test
3. Eсли вы хотите пройти тест, пропришите /solve_test и введите код теста(его можно получить у создателя теста)
4. Прописав /my_test, вы сможете увидеть все созданные вами тесты
5. Прописав /my_result, вы сможете увидеть все результаты тестов, которые вы решали
6. Прописав /feedback, вы сможите оставить обратую связь''', parse_mode="HTML")

# Обработчик команды /my_profile
@router.message(Command('my_profile'))
async def my_profile_command(message: Message, state: FSMContext) -> None:
    user_data = connection.select_for_user_class(message.from_user.id)
    if user_data.status == 'T':
        markup = kb.edit_my_profile_for_teacher
        await state.set_state(Form.waiting_for_update_for_teacher)
    elif user_data.status == 'S':
        markup = kb.edit_my_profile_for_student
        await state.set_state(Form.waiting_for_update_for_student)
    answer_text = await message_for_profile(message.from_user.id)
    # Отправляем сообщение в ответ на команду /my_profile
    await message.answer(answer_text, parse_mode="HTML", reply_markup=markup)

# Обработчик команды /create_test
@router.message(Command('create_test'))
async def create_test_command(message: Message, state: FSMContext) -> None:
    # Отправляем сообщение в ответ на команду /create_test
    await message.answer('Введите название <i>теста</i>', parse_mode="HTML")
    await state.set_state(Form.waiting_for_test_name)

# Обработчик команды /solve_test
@router.message(Command('solve_test'))
async def solve_test_command(message: Message, state: FSMContext) -> None:
    # Отправляем сообщение в ответ на команду /solve_test
    await message.answer('Введите ключ теста', parse_mode="HTML")
    await state.set_state(Form.waiting_for_test_key)

# Обработчик команды /my_test
@router.message(Command('my_test'))
async def my_test_command(message: Message) -> None:
    # Отправляем сообщение в ответ на команду /my_test
    await message.answer('my_test', parse_mode="HTML")

# Обработчик команды /my_result
@router.message(Command('my_result'))
async def my_result_command(message: Message) -> None:
    # Отправляем сообщение в ответ на команду /my_result
    await message.answer('my_result', parse_mode="HTML")

# Обработчик команды /feedback
@router.message(Command('feedback'))
async def feedback_command(message: Message, state: FSMContext) -> None:
    # Отправляем сообщение в ответ на команду /feedback
    await message.answer('Напишите сообщение для <i>обратной связи</i>. Чтобы отменить отправку нажмите на кнопку <b>Отмена</b>', parse_mode="HTML", reply_markup=kb.cancel_for_feedback)
    await state.set_state(Form.waiting_for_feedback)

@router.message(Form. waiting_for_set_fio)
async def set_fio_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажите <u>ФИО</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form. waiting_for_set_fio) # Устанавливаем состояние ожидания ФИО
    else:
        await state.update_data(fio=message.text)
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Теперь укажите <i>кто ты</i>.', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_status)  # Устанавливаем состояние ожидания статуса

@router.message(Form.waiting_for_set_status)
async def set_status_state(message: Message, state: FSMContext) -> None:
    if message.text == 'Преподаватель':
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Регестрация завершена. Чтобы узнать, как пользоваться ботом <i>пропиши команду</i> /how_to_use', parse_mode="HTML")
        await state.clear()
        user = User(message.from_user.id, message.from_user.username, context_data.get('fio'), 'T', None)
        connection.insert_new_user_id(user)

    elif message.text == 'Ученик':
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Осталось установить <i>группу или класс</i>.', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_group) # Устанавливаем состояние ожидания группы
    else:
        await message.answer(f'Укажите ваш <u>статус</u>', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_status) # Устанавливаем состояние ожидания статуса

@router.message(Form.waiting_for_set_group)
async def set_group_state(message: Message, state: FSMContext) -> None:    
    if message.text[0] == '/':
        await message.answer('Укажите <u>группу/класс</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_group) # Устанавливаем состояние ожидания группы
    else:
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Регестрация завершена. Чтобы узнать, как пользоваться ботом <i>пропиши команду</i> /how_to_use', parse_mode="HTML")
        await state.clear()
        user = User(message.from_user.id, message.from_user.username, context_data.get('fio'), 'S', message.text)
        connection.insert_new_user_id(user)

@router.message(Form.waiting_for_feedback)
async def feedback_state(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.text == 'Отмена':
        await message.answer('<i>Отправка отменена</i>', parse_mode="HTML")
    else:
        await message.answer('<i>Ваше сообщение передано</i>', parse_mode="HTML")
        await bot.send_message(chat_id=TG_ID, text=f'user_id: {message.from_user.id}\nusername: {message.from_user.username}\nfirst_name: {message.from_user.first_name}\nТекст: {message.text}', parse_mode="HTML")
    await state.clear()

@router.message(Form.waiting_for_update_for_teacher, F.text.in_(kb.text_for_edit_my_profile_for_teacher))
async def update_for_teacher_state(message: Message, state: FSMContext) -> None:
    if message.text == 'ФИО':
        await message.answer('Укажите свое новое <i>ФИО</i>.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    elif message.text == 'Статус':
        await message.answer(f'Укажите свой новый статус', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_update_status)

@router.message(Form.waiting_for_update_for_student, F.text.in_(kb.text_for_edit_my_profile_for_student))
async def update_for_student_state(message: Message, state: FSMContext) -> None:
    if message.text == 'ФИО':
        await message.answer('Укажите свое новое <i>ФИО</i>', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    elif message.text == 'Статус':
        await message.answer(f'Укажите свой новый статус', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_update_status)
    elif message.text == 'Группа':
        await message.answer(f'Укажите свою новую группу', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_group)

@router.message(Form.waiting_for_update_fio)
async def update_fio_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажите <u>ФИО</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    else:
        connection.update_fio_for_my_profile(message.from_user.id, message.text)
        await message.answer('Отлично, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await message.answer(await message_for_profile(user_id=message.from_user.id), parse_mode="HTML")
        await state.clear()

@router.message(Form.waiting_for_update_status, F.text.in_(kb.text_for_set_status))
async def update_status_state(message: Message, state: FSMContext) -> None:
    if message.text == 'Преподаватель':
        connection.update_status_for_my_profile(message.from_user.id, 'T')
        await message.answer('Отлично, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await message.answer(await message_for_profile(user_id=message.from_user.id), parse_mode="HTML")
        await state.clear()
    elif message.text == 'Ученик':
        connection.update_status_for_my_profile(message.from_user.id, 'S')
        await message.answer('Отлично, теперь укажите вашу группу/класс', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_group)

@router.message(Form.waiting_for_update_group)
async def update_group_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажите <u>группу/класс</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    else:
        connection.update_group_for_my_profile(message.from_user.id, message.text)
        await message.answer('Отлично, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await message.answer(await message_for_profile(user_id=message.from_user.id), parse_mode="HTML")
        await state.clear()

@router.message(Form.waiting_for_test_name)
async def set_test_name_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Введите <u>названиие теста</u>, а не команду.', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_name)
    else:
        await state.update_data(test_name=message.text)
        await message.answer('Отлично, теперь укажите дисциплину теста <i>(если ее нет, укажите "-")</i>', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_subject)

@router.message(Form.waiting_for_test_subject)
async def set_test_subject_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажите <u>дисциплину теста или "-"</u>, а не команду.', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_name)
    elif message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
        await state.clear()
    else:
        if message.text == '-':
            await state.update_data(test_subject=None)
        else:
            await state.update_data(test_subject=message.text)
        await state.update_data(questions=[], answers=[], right_answers=[])
        await message.answer('Отлично, теперь отправьте 1-й вопрос', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_question)

@router.message(Form.waiting_for_test_question)
async def set_test_question_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Отправьте <u>вопрос для теста/u>, а не команду.', parse_mode="HTML", reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_question_name)
    elif message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
        await state.clear()
    elif message.text == 'Предпросмотр':
        answer_text = await message_for_test_preview(message.from_user.id, state)
        await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.choice_for_test_preview)
        await state.set_state(Form.waiting_for_test_preview)
    else:
        context_data = await state.get_data()
        await state.update_data(questions=[*context_data.get('questions'), message.text])
        await message.answer('''Отлично, теперь отправьте варианты ответа в формате:
1) Вариант
!2) Вариант
3) Вариант
4) Вариант
(вослицательный знак означает правильный вариант ответа)''', parse_mode="HTML", reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_answer)

@router.message(Form.waiting_for_test_answer)
async def set_test_answer_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Отправьте <u>ответы на вопросы для теста/u>, а не команду.', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_answer)
    elif message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
    else:
        var = message.text.split('\n')
        answers = []
        right_answer = []
        for i in range(len(var)):
            if var[i][0] == '!':
                right_answer.append(i + 1)
            if ') ' in var[i]:
                answers.append(var[i].split(') ', maxsplit=1)[1])
        if len(right_answer) != 1 or len(var) != len(answers) or len(var) < 2 or '' in answers or ' ' in answers:
            await message.answer('''<u>Пожалуйста</u>, отправьте варианты ответа в формате:
1) Вариант
!2) Вариант
3) Вариант
4) Вариант
(вослицательный знак означает правильный вариант ответа)''', parse_mode="HTML")
            await state.set_state(Form.waiting_for_test_answer)
        else:
            context_data = await state.get_data()
            await state.update_data(answers=[*context_data.get('answers'), answers], right_answers=[*context_data.get('right_answers'), right_answer[0]])
            await message.answer(f'Отлично, теперь отправьте {len(context_data.get("questions")) + 1}-й вопрос', parse_mode="HTML",  reply_markup=kb.set_question_for_test)
            await state.set_state(Form.waiting_for_test_question)

@router.message(Form.waiting_for_test_preview, F.text.in_(kb.text_for_choice_for_test_preview))
async def set_chocie_after_priview(message: Message, state: FSMContext) -> None:
    if message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
        await state.clear()
    elif message.text == 'Удалить вопрос':
        await message.answer(f'Укажите <i>номер</i> вопроса, который вы <u>хотите удалить</u>', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_del_question)
    elif message.text == 'Добавить вопрос':
        context_data = await state.get_data()
        await message.answer(f'Отлично, теперь отправьте {len(context_data.get("questions")) + 1}-й вопрос', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
        await state.set_state(Form.waiting_for_test_question)
    elif message.text == 'Опубликовать тест':
        await message.answer('Осталось совсем <i>чуть-чуть</i>, выберете, будут ли видны пользователям их результаты после прохождения теста', parse_mode="HTML", reply_markup=kb.choosing_visible_result)
        
@router.message(Form.waiting_for_del_question)
async def set_test_answer_state(message: Message, state: FSMContext) -> None:
    if message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
        await state.clear()
    elif message.text == 'Предпросмотр':
        answer_text = await message_for_test_preview(message.from_user.id, state)
        await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.choice_for_test_preview)
        await state.set_state(Form.waiting_for_test_preview)
    else:
        try:
            context_data = await state.get_data()
            await state.update_data(questions=context_data.get('questions').pop(int(message.text) - 1), answers=context_data.get('answers').pop(int(message.text) - 1), right_answers=context_data.get('right_answers').pop(int(message.text) - 1))
            await message.answer(f'Вопрос №{message.text} <i>удален</i> из теста', parse_mode="HTML",  reply_markup=kb.set_question_for_test)
            if len(context_data.get('questions')) == 0:
                await message.answer('Отлично, теперь отправьте 1-й вопрос', parse_mode="HTML",  reply_markup=kb.cancel_for_create_test)
                await state.set_state(Form.waiting_for_test_question)
            else:
                answer_text = await message_for_test_preview(message.from_user.id, state)
                await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.choice_for_test_preview)
                await state.set_state(Form.waiting_for_test_preview)
        except (TypeError, IndexError):
            await message.answer(f'Укажите существующий номер вопроса без посторонних знаков (<i>только число</i>)', parse_mode="HTML",  reply_markup=kb.set_question_for_test)
            await state.set_state(Form.waiting_for_del_question)

@router.message(Form.waiting_for_test_preview, F.text.in_(kb.text_for_choosing_visible_result))
async def set_choosing_visible_result(message: Message, state: FSMContext) -> None:
    if message.text == 'Отмена':
        await message.answer('Вы отменили <u>создание теста</u>', parse_mode="HTML")
        await state.clear()
    elif message.text == 'Да':
        visible_result = True
    elif message.text == 'Нет':
        visible_result = False
    context_data = await state.get_data()
    key = uuid4()
    test = Test(None, message.from_user.id, datetime.now(), key, context_data.get('test_name'), context_data.get('subject_name'), context_data.get('questions'), context_data.get('answers'), context_data.get('right_answers'), visible_result)
    connection.insert_new_test(test)
    await message.answer(f'Тест "{context_data.get("test_name")}" создан\nЧтобы пройти тест вставте данный ключ после комадны /solve_test (вы не можете пройти свой-же тест):', parse_mode="HTML")
    await message.answer(str(key), parse_mode="HTML")
    await state.clear()

@router.message(Form.waiting_for_test_key)
async def start_solving_test(message: Message, state: FSMContext) -> None:
    try:
        solving_test = connection.select_for_test_class_by_uuid(UUID(message.text))
        if solving_test == False:
            await message.answer('Пожалуйста, введите <i>ключ</i> от существующего теста', parse_mode="HTML")
            await state.set_state(Form.waiting_for_test_key)
        elif solving_test.creator_user_id == message.from_user.id:
           await message.answer('Вы не можете пройти свой же <u>тест</u>', parse_mode="HTML")
           await state.clear()
        # TODO: проверка на наличие прошлого релузьтата этого же теста
        elif type(connection.select_for_test_result_by_user_id_and_test_id(message.from_user.id, solving_test.test_id)) == TestResult:
            await state.update_data(test=solving_test, now_question=0, test_result=[])
            answer_text = await message_for_finded_test(solving_test)
            await message.answer(answer_text, parse_mode="HTML")
            await message.answer('Вы <u>уже проходили</u> этот тест. Хотите пройти его еще раз?\n*<i>Результат этой попытки не заменит прошлую</i>', parse_mode="HTML", reply_markup=kb.start_solve_test)
            await state.set_state(Form.waiting_for_start_test)
        else:
            await state.update_data(test=solving_test, now_question=0, test_result=[])
            answer_text = await message_for_finded_test(solving_test)
            await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.start_solve_test)
            await state.set_state(Form.waiting_for_start_test)

    except ValueError:
        await message.answer('Пожалуйста, введите <i>ключ</i> от существующего теста', parse_mode="HTML")
        await state.set_state(Form.waiting_for_start_test)

@router.message(Form.waiting_for_start_test, F.text.in_(kb.text_for_start_solve_test))
async def start_solving_test(message: Message, state: FSMContext) -> None:
    if message.text == 'Отмена':
        await message.answer('Вы отказались от <u>прохождения теста</u>', parse_mode="HTML")
        await state.clear()
    else:
        context_data = await state.get_data()
        test:Test = context_data.get('test')
        await state.update_data(now_question=1)
        answer_markup = kb.markup_for_answers(test.all_answers[0])
        answer_text = await message_for_answer_question(0, test)
        await message.answer(answer_text, parse_mode="HTML", reply_markup=answer_markup)
        await state.set_state(Form.waiting_for_solve_question)

@router.message(Form.waiting_for_solve_question)
async def solving_question(message: Message, state: FSMContext) -> None:
    context_data = await state.get_data()
    test:Test = context_data.get('test')
    form_answer = True
    variant = message.text.split(' ', 1)[1]
    if variant not in test.all_answers[context_data.get('now_question') - 1]:
        answer_markup = kb.markup_for_answers(test.all_answers[context_data.get('now_question') - 1])
        answer_text = await message_for_answer_question(context_data.get("now_question") - 1, test)
        
        await message.answer(f'Пожалуйста, выберете <i>пункт из списка</i>\n{answer_text}', parse_mode="HTML", reply_markup=answer_markup)
        await state.set_state(Form.waiting_for_solve_question)
        form_answer = False
    elif variant == test.all_answers[context_data.get('now_question') - 1][test.right_answers[context_data.get('now_question') - 1] - 1]:
        await state.update_data(test_result=[*context_data.get('test_result'), [1]])
    else:
        await state.update_data(test_result=[*context_data.get('test_result'), [0, test.all_answers[context_data.get('now_question') - 1].index(variant) + 1]])
    if len(test.all_questions) > context_data.get('now_question') and form_answer:
        answer_markup = kb.markup_for_answers(test.all_answers[context_data.get('now_question')])
        answer_text = await message_for_answer_question(context_data.get("now_question"), test)
        await message.answer(answer_text, parse_mode="HTML", reply_markup=answer_markup)
        await state.update_data(now_question=context_data.get("now_question") + 1)
        await state.set_state(Form.waiting_for_solve_question)
    elif form_answer:
        answer_text = await message_for_result_review(state)
        await message.answer(f'Вы <i>ответили</i> на все вопросы', parse_mode="HTML")
        await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.choice_for_result_preview)
        await state.set_state(Form.waiting_for_result_preview_aftermath)

@router.message(Form.waiting_for_result_preview_aftermath, F.text.in_(kb.text_for_choice_for_result_preview))
async def result_preview_aftermath(message: Message, state: FSMContext) -> None:
    if message.text == 'Отмена':
        await message.answer('Вы отказались от <u>прохождения теста</u>', parse_mode="HTML")
        await state.clear()
    elif message.text == 'Изменить ответ':
        await message.answer('Напишите <i>номер вопроса</i> ответ в котором вы хотите изменить', parse_mode="HTML")
        await state.set_state(Form.waiting_for_edit_answers)
    elif message.text == 'Завершить тест':
        context_data = await state.get_data()
        test:Test = context_data.get('test')
        context_test_result = context_data.get('test_result')
        test_result = TestResult(test.test_id, message.from_user.id, datetime.now(), context_test_result.count([1]), len(test.all_questions), [[i + 1, context_test_result[i][1]] for i in range(len(context_test_result)) if context_test_result[i][0] == 0])
        connection.insert_new_test_result(test_result)
        if test.visible_result:
            data_for_show_result[message.from_user.id] = [test, test_result]
            await message.answer(f'Тест "{test.test_name}" успешно <u>пройден</u>\n\n<u>Результаты:</u>\n{test_result.count_correct_answers}/{test_result.count_answers_in_total} - {test_result.procent_of_right()}%\n<b>Рекомендуемая оценка:</b> {test_result.recomend_mark()}', parse_mode="HTML" , reply_markup=kb.show_more_result)
            #
        else:
            await message.answer(f'Тест "{test.test_name}" успешно <u>пройден</u>\nК сожелению доступ полным к результату был ограничен автором. Он сможет открыть доступ позже.\n\n<u>Результаты:</u>\n{test_result.count_correct_answers}/{test_result.count_answers_in_total} - {test_result.procent_of_right()}%\n<b>Рекомендуемая оценка:</b> {test_result.recomend_mark()}', parse_mode="HTML")
        await state.clear()

@router.message(Form.waiting_for_edit_answers)
async def edit_answer(message: Message, state: FSMContext) -> None:
    try:
        context_data = await state.get_data()
        test:Test = context_data.get('test')
        answer_markup = kb.markup_for_answers(test.all_answers[int(message.text) - 1])
        answer_text = await message_for_answer_question(int(message.text) - 1, test)
        await message.answer(answer_text, parse_mode="HTML",  reply_markup=answer_markup)
        await state.update_data(now_edit_question=int(message.text))
        await state.set_state(Form.waiting_for_edit_answers_result)
    except (TypeError, IndexError):
        await message.answer(f'Укажите существующий номер вопроса без посторонних знаков (<i>только число</i>)', parse_mode="HTML",  reply_markup=kb.set_question_for_test)
        await state.set_state(Form.waiting_for_edit_answers)

@router.message(Form.waiting_for_edit_answers_result)
async def edit_answer(message: Message, state: FSMContext) -> None:
    context_data = await state.get_data()
    test:Test = context_data.get('test')
    form_answer = True
    variant = message.text.split(' ', 1)[1]
    if variant not in test.all_answers[context_data.get('now_edit_question') - 1]:
        answer_markup = kb.markup_for_answers(test.all_answers[context_data.get('now_edit_question') - 1])
        answer_text = await message_for_answer_question(context_data.get("now_edit_question") - 1, test)
        await message.answer(answer_text, parse_mode="HTML", reply_markup=answer_markup)
        await state.set_state(Form.waiting_for_edit_answers)
        form_answer = False
    elif variant == test.all_answers[context_data.get('now_edit_question') - 1][test.right_answers[context_data.get('now_edit_question') - 1] - 1]:
        test_result = context_data.get('test_result')
        test_result[context_data.get('now_edit_question') - 1] = [1]
        await state.update_data(test_result=test_result)
    else:
        test_result = context_data.get('test_result')
        test_result[context_data.get('now_edit_question') - 1] = [0, test.all_answers[context_data.get('now_edit_question') - 1].index(variant) + 1]
        await state.update_data(test_result=test_result)
    if form_answer:
        answer_text = await message_for_result_review(state)
        await message.answer(f'Ответ <i>изменен</i>', parse_mode="HTML")
        await message.answer(answer_text, parse_mode="HTML", reply_markup=kb.choice_for_result_preview)
        await state.set_state(Form.waiting_for_result_preview_aftermath)

@router.callback_query(F.data == 'show_more_test_result')
async def show_more_result(callback: CallbackQuery):
    answer_text = await message_for_show_more_test_result(data_for_show_result[callback.from_user.id][0], data_for_show_result[callback.from_user.id][1])
    await callback.message.edit_text(answer_text, parse_mode="HTML")