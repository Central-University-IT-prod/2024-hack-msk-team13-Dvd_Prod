from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from prod.infrastructure.database.gateways.user import UserGateway


@dataclass
class AddUserInteractor:
    gateway: UserGateway
    session: AsyncSession
    
    async def execute(
        self,
        tg_id: int,
        tg_chat_id: int,
    ) -> None:
        await self.gateway.add(
            tg_id=tg_id,
            tg_chat_id=tg_chat_id,
        )
        await self.session.commit()
