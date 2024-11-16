from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from prod.business_logic.enums import TripType, TripStatus
from prod.infrastructure.database.models import Trip


class TripGateway:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def add(
        self,
        user_id: int,
        flight_number: str | None,
        price: Decimal,
        status: TripStatus,
        type: TripType,
        where: str,
        start_at: datetime,
        end_at: datetime,
        from_where: str,
    ) -> None:
        self._session.add(
            Trip(
                flight_number=flight_number,
                status=status,
                user_id=user_id,
                price=price,
                where=where,
                from_where=from_where,
                type=type,
                end_at=end_at,
                start_at=start_at,
            ),
        )
    
    async def with_id(self, data: int) -> Trip:
        stmt = select(Trip).where(Trip.id == data)
        result = await self._session.execute(stmt)
        scalar = result.scalar()
        if scalar is None:
            raise ValueError('Not found trip %r' % data)
        return scalar
    
    async def quick_trips(self) -> list[Trip]:
        stmt = (
            select(Trip)
            .where(
                Trip
            )
        )
    
    async def with_user_id(
        self,
        user_id: int,
        including_deleted: bool,
    ) -> list[Trip]:
        stmt = (
            select(Trip)
            .where(Trip.user_id == user_id)
            .order_by(Trip.created_at)
        )
        if not including_deleted:
            stmt.where(Trip.deleted_at.is_(None))
        
        result = await self._session.execute(stmt)
        scalars = result.scalars().all()
        return scalars
    
    async def get_all(self) -> list[Trip]:
        stmt = select(Trip)
        result = await self._session.execute(stmt)
        scalars = result.scalars().all()
        return scalars
    
