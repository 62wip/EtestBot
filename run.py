import asyncio
from aiogram import Bot, Dispatcher
import pymysql

db = pymysql.connect()

# Импортируем настройки и модули для клавиатур и обработчиков
import config
import app.keyboards as kb
from app.handlers import router

# Определяем асинхронную функцию main
async def main():
    # Создаем экземпляр бота с использованием API_TOKEN из настроек
    bot = Bot(token=config.API_TOKEN)
    # Создаем диспетчер (Dispatcher)
    dp = Dispatcher()
    # Включаем маршрутизатор (router), который будет обрабатывать входящие сообщения
    dp.include_router(router)
    # Запускаем бота в режиме long polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        # Запускаем асинхронную функцию main с использованием asyncio.run()
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Выход')
