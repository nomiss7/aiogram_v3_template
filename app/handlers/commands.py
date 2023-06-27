from datetime import datetime
from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from app.lexicon.lexicon import phrases

from app.keyboards.inline.languages_kb import choose_language_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, language, db):
    language = 'EN' if language is None else language
    if not await db.sql_get_user_id(user_id=message.from_user.id):
        await db.sql_create_user(user_id=message.from_user.id,
                                 lexicon=language,
                                 datetime=str(datetime.now()))
    await message.answer(text=phrases['start'][language],
                         reply_markup=await choose_language_kb())


@router.callback_query(Text(startswith="language:"))
async def cmd_start(call: CallbackQuery, db):
    lexicon = call.data.split(":")[1]
    await db.sql_update_language(user_id=call.from_user.id,
                                 lexicon=lexicon)
    await call.message.edit_text(text=phrases['language_changed'][lexicon])
