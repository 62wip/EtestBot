import asyncio
from aiogram import Bot, Dispatcher
import pymysql

# Импортируем настройки и модули для клавиатур и обработчиков
from config import *
import app.keyboards as kb
from app.handlers import router
from app.database.requests import db, create_all_tables

async def on_startup(dp: Dispatcher) -> None:
    print("Bot is starting up...")
    create_all_tables()

async def on_shutdown(dp: Dispatcher) -> None:
    print("Bot is shutting down...")
    db.close()
    

# Определяем асинхронную функцию main
async def main() -> None:
    # Создаем экземпляр бота с использованием API_TOKEN из настроек
    bot = Bot(token=API_TOKEN)
    # Создаем диспетчер (Dispatcher)
    dp = Dispatcher()
    # Включаем маршрутизатор (router), который будет обрабатывать входящие сообщения
    dp.include_router(router)
    # Запускаем бота в режиме long polling
    await dp.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == '__main__':
    try:
        # Запускаем асинхронную функцию main с использованием asyncio.run()
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Выход')
