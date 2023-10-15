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
    await bot.delete_webhook(drop_pending_updates=True) 
    # Создаем экземпляр бота с использованием API_TOKEN из настроек
    bot = Bot(token=API_TOKEN)
    # Создаем диспетчер (Dispatcher)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # Включаем маршрутизатор (router), который будет обрабатывать входящие сообщения
    dp.include_router(router)
    # Запускаем бота в режиме long polling
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        # Запускаем асинхронную функцию main с использованием asyncio.run()
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Выход')
