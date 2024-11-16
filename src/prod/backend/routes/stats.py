from decimal import Decimal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from prod.business_logic.enums import TripStatus
from prod.infrastructure.database.gateways.trip import TripGateway
from prod.infrastructure.database.gateways.user import UserGateway
from prod.infrastructure.validation_init_data import ValidationInitData


router = APIRouter(route_class=DishkaRoute)


class GetStatsSchema(BaseModel):
    init_data: str


class StatsSchema(BaseModel):
    count_cities_visited: int
    amount_money_spent: Decimal
    count_upcoming_trips: int


@router.post('/stats', response_model=StatsSchema)
async def get_stats(
    schema: GetStatsSchema,
    trip_gateway: FromDishka[TripGateway],
    user_gateway: FromDishka[UserGateway],
    validation: FromDishka[ValidationInitData],
) -> StatsSchema:
    init_data = validation.execute(schema.init_data)
    user = await user_gateway.with_tg_id(init_data.user.id)
    trips = await trip_gateway.with_user_id(user.id, True)
    
    count_upcoming_trips = 0
    count_cities_visited = 0
    amount_money_spent = Decimal(0)
    
    for trip in trips:
        if trip.status == TripStatus.UPCOMING:
            count_upcoming_trips += 1
        if trip.status == TripStatus.CANCELED:
            count_cities_visited += 1
        amount_money_spent += trip.price
    
    return StatsSchema(
        count_cities_visited=count_cities_visited,
        count_upcoming_trips=count_upcoming_trips,
        amount_money_spent=amount_money_spent,
    )
    
