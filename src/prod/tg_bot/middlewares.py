from aiogram import BaseMiddleware
from aiogram.types import Chat, User as AiogramUser
from sqlalchemy.ext.asyncio import AsyncSession

from prod.infrastructure.database.models import User


class AddUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler,
        event,
        data
    ) -> None:
        user: AiogramUser = data['event_from_user']
        chat: Chat = data['event_chat']
        
        session: AsyncSession = await data['dishka_container'].get(
            AsyncSession
        )
        session.add(
            User(
                tg_id=user.id,
                tg_chat_id=chat.id,
            ),
        )
        a = await handler(event, data)
        await session.commit()
        return a
