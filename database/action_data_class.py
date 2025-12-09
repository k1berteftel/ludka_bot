import datetime
from typing import Literal

from sqlalchemy import select, insert, update, column, text, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.model import (VictoriesTable, TouchesTable, OneTimeLinksIdsTable, AdminsTable, StaticTable)


async def setup_table(sessions: async_sessionmaker):
    async with sessions() as session:
        if not await session.scalar(select(StaticTable)):
            await session.execute(insert(StaticTable))
        await session.commit()


class DataInteraction():
    def __init__(self, session: async_sessionmaker):
        self._sessions = session

    async def add_link(self, link: str):
        async with self._sessions() as session:
            await session.execute(insert(OneTimeLinksIdsTable).values(
                link=link
            ))
            await session.commit()

    async def add_admin(self, user_id: int, name: str):
        async with self._sessions() as session:
            await session.execute(insert(AdminsTable).values(
                user_id=user_id,
                name=name
            ))
            await session.commit()

    async def add_static_value(self, column: str, value: int):
        async with self._sessions() as session:
            await session.execute(update(StaticTable).values(
                {
                    column: getattr(StaticTable, column) + value
                }
            ))
            await session.commit()

    async def add_victory(self, user_id: int, name: str, username: str | None, prize: int):
        async with self._sessions() as session:
            await session.execute(insert(VictoriesTable).values(
                user_id=user_id,
                name=name,
                username=username,
                prize=prize
            ))
            await session.commit()

    async def add_touch(self, user_id: int, emoji: Literal['cube', 'slots', 'darts', 'football', 'bowling', 'basketball'], value: int):
        async with self._sessions() as session:
            await session.execute(insert(TouchesTable).values(
                user_id=user_id,
                emoji=emoji,
                value=value
            ))
            await session.commit()

    async def get_user_touches(self, user_id: int, emoji: Literal['cube', 'slots', 'darts', 'football', 'bowling', 'basketball'], value: int):
        async with self._sessions() as session:
            result = await session.scalars(select(TouchesTable).where(
                and_(
                    TouchesTable.user_id == user_id,
                    TouchesTable.emoji == emoji,
                    TouchesTable.value == value
                )
            ))
        return result.fetchall()

    async def get_static(self):
        async with self._sessions() as session:
            result = await session.scalar(select(StaticTable))
        return result

    async def get_links(self):
        async with self._sessions() as session:
            result = await session.scalars(select(OneTimeLinksIdsTable))
        return result.fetchall()

    async def get_victories(self):
        async with self._sessions() as session:
            result = await session.scalars(select(VictoriesTable))
        return result.fetchall()

    async def get_admins(self):
        async with self._sessions() as session:
            result = await session.scalars(select(AdminsTable))
        return result.fetchall()

    async def del_touches_by_value(self, user_id: int, emoji: Literal['cube', 'slots', 'darts', 'football', 'bowling', 'basketball'], value: int):
        async with self._sessions() as session:
            await session.execute(delete(TouchesTable).where(
                and_(
                    TouchesTable.user_id == user_id,
                    TouchesTable.emoji == emoji,
                    TouchesTable.value == value
                )
            ))
            await session.commit()

    async def del_touch_by_id(self, id: int):
        async with self._sessions() as session:
            await session.execute(delete(TouchesTable).where(TouchesTable.id == id))
            await session.commit()

    async def del_link(self, link_id: str):
        async with self._sessions() as session:
            await session.execute(delete(OneTimeLinksIdsTable).where(OneTimeLinksIdsTable.link == link_id))
            await session.commit()

    async def del_admin(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(delete(AdminsTable).where(AdminsTable.user_id == user_id))
            await session.commit()