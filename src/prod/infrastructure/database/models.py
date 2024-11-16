from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    func,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from prod.business_logic.enums import TripType, TripStatus


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )


class Trip(Base):
    __tablename__ = "trips"
    
    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    flight_number: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[TripType] = mapped_column(
        Enum(TripType),
        nullable=False,
    )
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    where: Mapped[str] = mapped_column(Text, nullable=False)
    from_where: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
