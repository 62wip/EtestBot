from functools import partial

import asyncio
from aiogram import Bot, Dispatcher
import pymysql

# Импортируем настройки и модули для клавиатур и обработчиков
from config import *
import app.keyboards as kb
from app.handlers import router
from app.database.requests import Connection

async def on_startup(dp: Dispatcher, connection: Connection) -> None:
    print("Bot is starting up...")
    connection.create_all_tables()

async def on_shutdown(dp: Dispatcher, connection: Connection) -> None:
    print("Bot is shutting down...")
    connection.db.close()
    

# Определяем асинхронную функцию main
async def main() -> None:
    # Создаем экземпляр бота с использованием API_TOKEN из настроек
    bot = Bot(token=API_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True) 
    # Создаем диспетчер (Dispatcher)
    dp = Dispatcher()
    connection = Connection()
    # Включаем маршрутизатор (router), который будет обрабатывать входящие сообщения
    dp.include_router(router)
    dp.startup.register(partial(on_startup, dp, connection))
    dp.shutdown.register(partial(on_shutdown, dp, connection))
    # Запускаем бота в режиме long polling
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        # Запускаем асинхронную функцию main с использованием asyncio.run()
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Exit successful.')
