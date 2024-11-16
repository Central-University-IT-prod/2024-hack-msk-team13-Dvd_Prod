from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from prod.infrastructure.database.gateways.trip import TripGateway


class TripDeletedError(Exception):
    pass


@dataclass
class SoftDeleteTripInteractor:
    gateway: TripGateway
    session: AsyncSession
    
    async def execute(self, id: int) -> None:
        trip = await self.gateway.with_id(id)
        if trip.deleted_at:
            raise TripDeletedError
        
        trip.deleted_at = datetime.now()
        await self.session.commit()
