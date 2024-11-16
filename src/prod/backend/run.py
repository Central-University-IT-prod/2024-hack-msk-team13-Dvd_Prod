import asyncio
import sys

import uvicorn
from aiogram import Bot
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.starlette import setup_dishka
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from prod.backend.routes import metrics, stats, trip
from prod.config import TOKEN_BOT
from prod.di.build_container import build_container


async def lifespan(app: FastAPI) -> None:
    yield
    await app.state.bot.session.close()
    await app.state.dishka_container.close()


def main() -> None:
    app = FastAPI(
        lifespan=lifespan,
        swagger_ui_parameters={"syntaxHighlight": False},
        root_path="/api",
    )
    
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=["prod.bijouterieshop.ru"],
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    
    router = APIRouter(route_class=DishkaRoute)
    router.include_router(trip.router)
    router.include_router(stats.router)
    router.include_router(metrics.router)
    
    app.include_router(router)
    bot = Bot(TOKEN_BOT)
    
    container = build_container(bot)
    app.state.bot = bot
    setup_dishka(container, app)
    return app


if 'win' in sys.platform:
    from asyncio import WindowsSelectorEventLoopPolicy
    
    
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

print('run backend')
uvicorn.run(
    main(),
    host="0.0.0.0",
    port=8000,
    lifespan="on",
)
