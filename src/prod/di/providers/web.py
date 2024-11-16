from aiogram import Bot
from dishka import from_context, provide, Provider, Scope

from prod.infrastructure.validation_init_data import ValidationInitData


class WebProvider(Provider):
    scope = Scope.REQUEST
    
    provides = (
        provide(ValidationInitData)
        + from_context(Bot, scope=Scope.APP)
    )
