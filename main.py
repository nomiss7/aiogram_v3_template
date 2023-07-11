import asyncio
import logging
import asyncpg

import nats
from nats_fsm.Entry import NATSFSMStorage

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from middlewares.language import LanguageMiddleware
from config import load_config
from middlewares.db import DbMiddleware
from navigation.commands import set_bot_commands
from handlers import commands
from db.create_tables import create_table


class App:
    def __init__(self, config):

        self.config = config
        self.bot = Bot(
            self.config.tg_bot.token,
            parse_mode=self.config.tg_bot.parse_mode
        )
        self.pool = None
        self.storage = None
        self.dp = None

    async def create_storage(self):
        if self.config.tg_bot.use_nats:
            nc = await nats.connect(servers=["nats://nats:4222"])
            js = nc.jetstream()
            kv_states = await js.key_value('fsm_states_aiogram')
            kv_data = await js.key_value('fsm_data_aiogram')

            storage = NATSFSMStorage(nc, kv_states, kv_data)
        else:
            storage = MemoryStorage()

        return storage

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            database=self.config.db.POSTGRES_DB,
            user=self.config.db.POSTGRES_USER,
            host=self.config.db.POSTGRES_HOST,
            port=self.config.db.POSTGRES_PORT,
            password=self.config.db.POSTGRES_PASSWORD,
        )
        await create_table(self.pool)

    async def setup_dispatcher(self):
        self.storage = await self.create_storage()
        self.dp = Dispatcher(bot=self.bot, storage=self.storage)
        self.dp.include_router(commands.router)
        self.dp.message.middleware(DbMiddleware(self.pool))
        self.dp.callback_query.middleware(DbMiddleware(self.pool))
        self.dp.message.middleware(LanguageMiddleware(self.pool))
        self.dp.callback_query.middleware(LanguageMiddleware(self.pool))

    async def start(self):
        await self.create_pool()
        await set_bot_commands(bot=self.bot)
        await self.setup_dispatcher()

        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.dp.storage.close()
            await self.bot.session.close()


def load_app(config_file):
    config = load_config(config_file)
    return App(config)


def run_app(bot):
    try:
        asyncio.run(bot.start())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")

    app = load_app("data.ini")
    run_app(app)
