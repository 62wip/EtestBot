from typing import Any
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command

import app.keyboards as kb

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: Message):
    # Отправляем сообщение в ответ на команду /start
    await message.answer(f'Здравствуй,<u>{message.from_user.first_name}</u>! Это бот создан специально для <i>создания/решения тестов</i> онлайн. Чтобы узнать, как пользоваться ботом <i>пропиши команду</i> /how_to_use', parse_mode="HTML")

# Обработчик команды /how_to_use
@router.message(Command('how_to_use'))
async def how_to_use_command(message: Message):
    # Отправляем сообщение в ответ на команду /how_to_use
    await message.answer('''1. Чтобы посмотреть статистику или изметить профиль, пропишите /my_profile
2. Если вы хотите создать тест, пропришите /create_test
3. Eсли вы хотите пройти тест, пропришите /solve_test и введите код теста(его можно получить у создателя теста)
4. Прописав /my_test, вы сможете увидеть все созданные вами тесты
5. Прописав /my_result, вы сможете увидеть все результаты тестов, которые вы решали
6. Прописав /feedback, вы сможите оставить обратую связь''', parse_mode="HTML")

# Обработчик команды /my_profile
@router.message(Command('my_profile'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /my_profile
    await message.answer('my_profile', parse_mode="HTML")

# Обработчик команды /create_test
@router.message(Command('create_test'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /create_test
    await message.answer('create_test', parse_mode="HTML")

# Обработчик команды /solve_test
@router.message(Command('solve_test'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /solve_test
    await message.answer('solve_test', parse_mode="HTML")

# Обработчик команды /my_test
@router.message(Command('my_test'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /my_test
    await message.answer('my_test', parse_mode="HTML")

# Обработчик команды /my_result
@router.message(Command('my_result'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /my_result
    await message.answer('my_result', parse_mode="HTML")

# Обработчик команды /feedback
@router.message(Command('feedback'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /feedback
    await message.answer('feedback', parse_mode="HTML")