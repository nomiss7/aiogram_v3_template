from dataclasses import dataclass
from enum import Enum, unique

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


@dataclass
class Command:
    name: str
    description: str

    def to_bot_command(self) -> BotCommand:

        return BotCommand(command=self.name, description=self.description)


@unique
class BaseCommandList(Enum):

    def __str__(self) -> str:
        return self.value.name

    def __call__(self, *args, **kwargs) -> Command:
        return self.value


class Commands(BaseCommandList):

    start = Command(name='start', description='Start Bot')


async def set_bot_commands(bot: Bot) -> None:

    commands: list[BotCommand] = [command().to_bot_command() for command in Commands]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )