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

async def check_first_use(message, state: FSMContext) -> None:
    if connection.checking_first_use(message.from_user.id):
        await message.answer('Вижу ты тут <u>новенький</u>, позволь узнать твои данные, которые <b>будут отображаться у других пользователей</b>!', parse_mode="HTML")
        await message.answer('Укажи свое <i>ФИО</i>.', parse_mode="HTML")
        await state.set_state(Form. waiting_for_set_fio) # Устанавливаем состояние ожидания ФИО
        



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
    user_data = connection.select_for_my_profile(message.from_user.id)
    text = f'''<u><b>Ваш профиль</b></u>:
<i>ФИО(отображаемое имя)</i>: {user_data.fio}
<i>Телеграм ID:</i> {user_data.user_id}\n'''
    if user_data.status == 'T':
        text += '<i>Статус</i>: Преподователь'
        markup = kb.edit_my_profile_for_teacher
        await state.set_state(Form.waiting_for_update_for_teacher)
    elif user_data.status == 'S':
        text += f'<i>Статус</i>: Ученик\n<i>Группа/класс</i>: {user_data.group}'
        markup = kb.edit_my_profile_for_student
        await state.set_state(Form.waiting_for_update_for_student)
    # Отправляем сообщение в ответ на команду /my_profile
    await message.answer(text, parse_mode="HTML", reply_markup=markup)

# Обработчик команды /create_test
@router.message(Command('create_test'))
async def create_test_command(message: Message) -> None:
    # Отправляем сообщение в ответ на команду /create_test
    await message.answer('create_test', parse_mode="HTML")

# Обработчик команды /solve_test
@router.message(Command('solve_test'))
async def solve_test_command(message: Message) -> None:
    # Отправляем сообщение в ответ на команду /solve_test
    await message.answer('solve_test', parse_mode="HTML")

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
async def fio_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажи <u>ФИО</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form. waiting_for_set_fio) # Устанавливаем состояние ожидания ФИО
    else:
        await state.update_data(fio=message.text)
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Теперь укажи <i>кто ты</i>.', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_status)  # Устанавливаем состояние ожидания статуса

@router.message(Form.waiting_for_set_status)
async def status_state(message: Message, state: FSMContext) -> None:
    if message.text == 'Преподаватель':
        await state.update_data(status='T')
        await state.update_data(group=None)
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Регестрация завершена. Чтобы узнать, как пользоваться ботом <i>пропиши команду</i> /how_to_use', parse_mode="HTML")
        await state.clear()
        user = User(message.from_user.id, message.from_user.username, context_data.get('fio'), context_data.get('status'),context_data.get('group'))
    elif message.text == 'Ученик':
        await state.update_data(status='S')
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Осталось установить <i>группу или класс</i>.', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_group) # Устанавливаем состояние ожидания группы
    else:
        await message.answer(f'Укажите ваш <u>статус</u>', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_set_status) # Устанавливаем состояние ожидания статуса

@router.message(Form.waiting_for_set_group)
async def group_state(message: Message, state: FSMContext) -> None:    
    if message.text[0] == '/':
        await message.answer('Укажи <u>группу/класс</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_group) # Устанавливаем состояние ожидания группы
    else:
        await state.update_data(group=message.text)
        context_data = await state.get_data()
        await message.answer(f'Отлично, <u>{context_data.get("fio")}</u>! Регестрация завершена. Чтобы узнать, как пользоваться ботом <i>пропиши команду</i> /how_to_use', parse_mode="HTML")
        await state.clear()
        user = User(message.from_user.id, message.from_user.username, context_data.get('fio'), context_data.get('status'),context_data.get('group'))
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
        await message.answer('Укажи свое новое <i>ФИО</i>.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    elif message.text == 'Статус':
        await message.answer(f'Укажи свой новый статус', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_update_status)

@router.message(Form.waiting_for_update_for_student, F.text.in_(kb.text_for_edit_my_profile_for_student))
async def update_for_student_state(message: Message, state: FSMContext) -> None:
    if message.text == 'ФИО':
        await message.answer('Укажи свое новое <i>ФИО</i>', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    elif message.text == 'Статус':
        await message.answer(f'Укажи свой новый статус', parse_mode="HTML", reply_markup=kb.set_status)
        await state.set_state(Form.waiting_for_update_status)
    elif message.text == 'Группа':
        await message.answer(f'Укажи свою новую группу', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_group)

@router.message(Form.waiting_for_update_fio)
async def update_fio_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажи <u>ФИО</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    else:
        connection.update_fio_for_my_profile(message.from_user.id, message.text)
        await message.answer('Отличино, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await my_profile_command(message, state)
        await state.clear()

@router.message(Form.waiting_for_update_status, F.text.in_(kb.text_for_set_status))
async def update_status_state(message: Message, state: FSMContext) -> None:
    if message.text == 'Преподаватель':
        connection.update_status_for_my_profile(message.from_user.id, 'T')
        await message.answer('Отличино, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await my_profile_command(message, state)
        await state.clear()
    elif message.text == 'Ученик':
        connection.update_status_for_my_profile(message.from_user.id, 'S')
        await message.answer('Отличино, теперь укажите вашу группу/класс', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_group)

@router.message(Form.waiting_for_update_group)
async def update_group_state(message: Message, state: FSMContext) -> None:
    if message.text[0] == '/':
        await message.answer('Укажи <u>группу/класс</u>, а не команду.', parse_mode="HTML")
        await state.set_state(Form.waiting_for_update_fio)
    else:
        connection.update_group_for_my_profile(message.from_user.id, message.text)
        await message.answer('Отличино, <u>данные сохранены</u>, теперь ваш профиль выглядит так:', parse_mode="HTML")
        await my_profile_command(message, state)
        await state.clear()