import asyncio
import sys

from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from prod.config import TOKEN_BOT
from prod.di.build_container import build_container
from prod.tg_bot import handlers
from prod.tg_bot.middlewares import AddUserMiddleware


async def main() -> None:
    bot = Bot(TOKEN_BOT)
    
    container = build_container(bot)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    setup_dishka(container, dp)
    
    dp.message.middleware(AddUserMiddleware())
    
    try:
        await dp.start_polling(bot)
    finally:
        await container.close()


if 'win' in sys.platform:
    from asyncio import WindowsSelectorEventLoopPolicy
    
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

print('run backend')
asyncio.run(main())
