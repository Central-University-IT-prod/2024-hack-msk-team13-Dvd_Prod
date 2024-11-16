from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from prod.infrastructure.database.models import User


class UserGateway:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def add(
        self,
        tg_id: int,
        tg_chat_id: int,
    ) -> None:
        self._session.add(
            User(
                tg_id=tg_id,
                tg_chat_id=tg_chat_id,
            ),
        )
    
    async def with_tg_id(self, tg_id: int) -> User:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await self._session.execute(stmt)
        scalar = result.scalar()
        if scalar is None:
            raise ValueError()
        return scalar
    
    async def get_all(self) -> list[User]:
        stmt = select(User)
        result = await self._session.execute(stmt)
        return result.scalars().all()
