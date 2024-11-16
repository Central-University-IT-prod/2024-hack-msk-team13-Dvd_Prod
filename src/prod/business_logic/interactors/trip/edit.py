from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from prod.business_logic.enums import TripType
from prod.business_logic.protocols import Commitable
from prod.infrastructure.database.gateways.trip import TripGateway


@dataclass
class EditTripInteractor:
    gateway: TripGateway
    commitable: Commitable
    
    async def execute(
        self,
        id: int,
        flight_number: str | None = None,
        type: TripType | None = None,
        price: Decimal | None = None,
        where: str | None = None,
        from_where: str | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> None:
        trip = await self.gateway.with_id(id)
        if flight_number:
            trip.flight_number = flight_number
        if type:
            trip.type = type
        if price:
            trip.price = price
        if where:
            trip.where = where
        if from_where:
            trip.from_where = from_where
        if start_at:
            trip.start_at = start_at
        if end_at:
            trip.end_at = end_at
        
        await self.commitable.commit()
