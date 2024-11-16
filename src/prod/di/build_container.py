from aiogram import Bot
from dishka import AsyncContainer, make_async_container

from prod.di.providers.database import DatabaseProvider
from prod.di.providers.interactor import InteractorProvider
from prod.di.providers.web import WebProvider


def build_container(bot: Bot) -> AsyncContainer:
    container = make_async_container(
        WebProvider(),
        DatabaseProvider(),
        InteractorProvider(),
        context={
            Bot: bot,
        }
    )
    return container
