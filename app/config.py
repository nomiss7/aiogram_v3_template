import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_PASSWORD: str


@dataclass
class TgBot:
    token: str
    parse_mode: str
    admin_id: int
    use_nats: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            parse_mode=tg_bot.get("parse_mode"),
            admin_id=tg_bot.getint("admin_id"),
            use_nats=tg_bot.getboolean("use_nats"),

        ),
        db=DbConfig(
            POSTGRES_DB=config["db"].get("POSTGRES_DB"),
            POSTGRES_USER=config["db"].get("POSTGRES_USER"),
            POSTGRES_HOST=config["db"].get("POSTGRES_HOST"),
            POSTGRES_PORT=config["db"].get("POSTGRES_PORT"),
            POSTGRES_PASSWORD=config["db"].get("POSTGRES_PASSWORD"),
        ),
    )
