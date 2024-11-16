from typing import AsyncIterable

from dishka import AnyOf, provide, provide_all, Provider, Scope
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

from prod.business_logic.protocols import Commitable
from prod.config import DATABASE_URL
from prod.infrastructure.database.gateways.trip import TripGateway
from prod.infrastructure.database.gateways.user import UserGateway


class DatabaseProvider(Provider):
    scope = Scope.REQUEST
    
    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterable[async_sessionmaker[AsyncSession]]:
        engine = create_async_engine(DATABASE_URL, echo=True)
        maker = async_sessionmaker(
            bind=engine,
            expire_on_commit=True,
            autoflush=True
        )
        yield maker
        await engine.dispose(True)
    
    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, Commitable]]:
        async with pool() as session:
            await session.begin()
            yield session
    
    gateways = provide_all(UserGateway, TripGateway)
