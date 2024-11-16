from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from prod.config import WEB_APP_URL


router = Router()

START_TEXT = 'Перейди по ссылке, чтобы зайти на наш WebApp.'
START_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="WebApp",
                web_app=WebAppInfo(url=WEB_APP_URL),
            ),
        ],
    ],
)


@router.message(CommandStart())
async def start(event: Message) -> None:
    # await event.answer(START_TEXT, reply_markup=START_KEYBOARD)
    await event.answer(START_TEXT)
