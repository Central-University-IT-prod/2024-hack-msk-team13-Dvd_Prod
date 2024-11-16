from datetime import datetime
from decimal import Decimal
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel
from starlette.responses import Response

from prod.business_logic.enums import TripType
from prod.business_logic.interactors.trip.add import (
    AddTripInteractor,
    TicketNotValidatedError,
)
from prod.business_logic.interactors.trip.edit import EditTripInteractor
from prod.business_logic.interactors.trip.soft_delete import \
    SoftDeleteTripInteractor
from prod.infrastructure.database.gateways.trip import TripGateway
from prod.infrastructure.database.gateways.user import UserGateway
from prod.infrastructure.validation_init_data import ValidationInitData


router = APIRouter(route_class=DishkaRoute)


class AddTripSchema(BaseModel):
    init_data: str
    
    flight_number: str
    type: TripType
    price: Decimal
    where: str
    from_where: str
    start_at: datetime
    end_at: datetime


@router.post('/trip')
async def add_trip(
    schema: AddTripSchema,
    gateway: FromDishka[UserGateway],
    validation: FromDishka[ValidationInitData],
    interactor: FromDishka[AddTripInteractor],
) -> Response:
    init_data = validation.execute(schema.init_data)
    user = await gateway.with_tg_id(init_data.user.id)
    try:
        await interactor.execute(
            flight_number=schema.flight_number,
            type=schema.type,
            user_id=user.id,
            price=schema.price,
            where=schema.where,
            from_where=schema.from_where,
            start_at=schema.start_at,
            end_at=schema.end_at,
        )
    except TicketNotValidatedError:
        return Response(
            status_code=400,
            content='ticket not validate',
        )
    return Response(status_code=200)


class InitDataSchema(BaseModel):
    init_data: str


class TripSchema(BaseModel):
    id: int
    flight_number: str | None
    type: TripType
    user_id: int
    price: Decimal
    where: str
    from_where: str
    deleted_at: datetime | None
    start_at: datetime
    end_at: datetime


@router.get('/trips', response_model=list[TripSchema])
async def get_trips(
    raw_init_data: Annotated[InitDataSchema, Query(alias='init_data')],
    user_gateway: FromDishka[UserGateway],
    trip_gateway: FromDishka[TripGateway],
    validation: FromDishka[ValidationInitData],
) -> list[TripSchema]:
    init_data = validation.execute(raw_init_data)
    
    user = await user_gateway.with_tg_id(init_data.user.id)
    trips = await trip_gateway.with_user_id(
        user.id,
        including_deleted=False,
    )
    return [
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
            end_at=trip.end_at,
            start_at=trip.start_at,
        ) for trip in trips
    ]



@router.delete('/trip/{id}')
async def delete_trip(
    schema: InitDataSchema,
    interactor: FromDishka[SoftDeleteTripInteractor],
    id: Annotated[int, Path()],
) -> None:
    await interactor.execute(id)


class PutTripSchema(BaseModel):
    init_data: str
    
    id: int
    
    flight_number: str | None = None
    type: TripType | None = None
    price: Decimal | None = None
    where: str | None = None
    from_where: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


@router.put('/trip/{id}')
async def put_trip(
    schema: PutTripSchema,
    interactor: FromDishka[EditTripInteractor],
) -> None:
    await interactor.execute(
        id=schema.id,
        flight_number=schema.flight_number,
        type=schema.type,
        price=schema.price,
        where=schema.where,
        from_where=schema.from_where,
        start_at=schema.start_at,
        end_at=schema.end_at,
    )
