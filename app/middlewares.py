from typing import Callable, Awaitable, Dict, Any

import pymysql
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.requests import Connection


class DbSession(BaseMiddleware):
    def __init__(self, connection: Connection) -> None:
        super().__init__()
        self.connection = connection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['request'] = self.connection
        return await handler(event, data)