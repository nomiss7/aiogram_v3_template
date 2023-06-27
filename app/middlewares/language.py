import logging
from typing import Any, Callable, Awaitable

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class LanguageMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        try:
            async with self.pool.acquire() as conn:
                language = await conn.fetchval("SELECT lexicon FROM user_info WHERE user_id = $1", user_id)
                data['language'] = language
        except Exception as e:
            logger.exception("Error fetching language from database")
            data['language'] = None

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        await self.on_pre_process_message(event, data)
        return await handler(event, data)
