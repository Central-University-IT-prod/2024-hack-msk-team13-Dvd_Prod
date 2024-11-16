import asyncio

from aiogram import Bot
from dishka import AsyncContainer

from prod.config import TOKEN_BOT
from prod.di.build_container import build_container


async def departure_soon(
    container: AsyncContainer,
) -> None:
    pass


async def main():
    bot = Bot(TOKEN_BOT)
    container = build_container(bot)
    
    try:
        await asyncio.gather(departure_soon(container))
    finally:
        await container.close()
        await bot.session.close()


asyncio.run(main())
