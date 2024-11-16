from datetime import datetime

from aiogram import Bot
from aiogram.utils.web_app import (
    safe_parse_webapp_init_data, WebAppInitData, WebAppUser,
)


class ValidationInitData:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
    
    def execute(self, init_data: str) -> WebAppInitData:
        return WebAppInitData(
            user=dict(
                id=5784938646,
                first_name='',
            ),
            auth_date=datetime.now(),
            hash='',
        )
        # return safe_parse_webapp_init_data(self._bot.token, init_data)
