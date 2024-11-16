from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from prod.business_logic.enums import TripType
from prod.infrastructure.database.gateways.trip import TripGateway


router = APIRouter(route_class=DishkaRoute)


class TripSchema(BaseModel):
    id: int
    flight_number: str | None
    type: TripType
    user_id: int
    price: Decimal
    where: str
    from_where: str
    deleted_at: datetime | None


class MetricSchema(BaseModel):
    active_users_per_day: int
    active_users_per_month: int
    count_trips: dict[TripType, int]
    top_identical_tickets: list[TripSchema]


@router.get('/metrics')
async def get_metrics(
    gateway: FromDishka[TripGateway],
) -> MetricSchema:
    trips = await gateway.get_all()
    
    now = datetime.now()
    
    active_users_per_month = 0
    active_users_per_day = 0
    count_trips = defaultdict(int)
    top_identical_tickets = defaultdict(lambda: [0, None])
    
    for trip in trips:
        created_at: datetime = trip.created_at
        
        if created_at.month == now.month:
            active_users_per_month += 1
        if created_at.day == now.day:
            active_users_per_day += 1
        
        count_trips[trip.type] += 1
        top_identical_ticket = top_identical_tickets[hash((trip.where, trip.from_where))]
        top_identical_ticket[0] += 1
        top_identical_ticket[1] = trip
    
    return MetricSchema(
        active_users_per_day=active_users_per_day,
        active_users_per_month=active_users_per_month,
        count_trips=count_trips,
        top_identical_tickets=[
            TripSchema(
                id=trip.id,
                user_id=trip.user_id,
                flight_number=trip.flight_number,
                status=trip.status,
                type=trip.type,
                price=trip.price,
                where=trip.where,
                from_where=trip.from_where,
                deleted_at=trip.deleted_at,
            ) for count, trip in list(sorted(top_identical_tickets.values()))[:3]
        ],
    )
