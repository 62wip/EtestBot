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
    await message.answer('1', parse_mode="HTML")

# Обработчик команды /how_to_use
@router.message(Command('how_to_use'))
async def how_to_use_command(message: Message):
    # Отправляем сообщение в ответ на команду /how_to_use
    await message.answer('2', parse_mode="HTML")

# Обработчик команды /commands
@router.message(Command('commands'))
async def commands_command(message: Message):
    # Отправляем сообщение в ответ на команду /commands
    await message.answer('3', parse_mode="HTML")