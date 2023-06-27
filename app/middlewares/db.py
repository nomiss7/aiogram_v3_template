from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
import asyncpg
from aiogram.types import TelegramObject

from app.db.database import Database


class DbMiddleware(BaseMiddleware):
    def __init__(self, pool: asyncpg.pool.Pool):
        super().__init__()
        self.pool = pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        async with self.pool.acquire() as conn:
            data["db"] = Database(conn)
            return await handler(event, data)
