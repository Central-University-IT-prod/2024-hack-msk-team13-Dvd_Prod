from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from prod.business_logic.enums import TripType, TripStatus
from prod.business_logic.protocols import Commitable
from prod.infrastructure.database.gateways.trip import TripGateway


class TicketNotValidatedError(Exception):
    pass


@dataclass
class AddTripInteractor:
    gateway: TripGateway
    commitable: Commitable
    
    async def execute(
        self,
        user_id: int,
        price: Decimal,
        type: TripType,
        where: str,
        from_where: str,
        start_at: datetime,
        end_at: datetime,
        flight_number: str | None = None,
    ) -> None:
        await self.gateway.add(
            user_id=user_id,
            flight_number=flight_number,
            price=price,
            type=type,
            where=where,
            from_where=from_where,
            status=TripStatus.UPCOMING,
            end_at=end_at,
            start_at=start_at,
        )
        await self.commitable.commit()
