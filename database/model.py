import datetime
from typing import Literal

from sqlalchemy import BigInteger, VARCHAR, ForeignKey, DateTime, Boolean, Column, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class VictoriesTable(Base):
    __tablename__ = 'winners'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)
    username: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    prize: Mapped[int] = mapped_column(Integer, default=0)
    create: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())


class TouchesTable(Base):
    __tablename__ = 'touches'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    emoji: Mapped[Literal['cube', 'slots', 'darts', 'football', 'bowling', 'basketball']] = mapped_column(VARCHAR)
    value: Mapped[int] = mapped_column(Integer)


class AdminsTable(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)


class OneTimeLinksIdsTable(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)


class StaticTable(Base):
    __tablename__ = 'static'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    payouts: Mapped[int] = mapped_column(Integer, default=0)
    spent: Mapped[int] = mapped_column(Integer, default=0)

