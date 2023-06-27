from aiogram import types


async def choose_language_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="RU", callback_data="language:RU"),
            types.InlineKeyboardButton(text="EN", callback_data="language:EN")
        ]]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb
