from sqlalchemy import select

from src.db import database
from src.db.tables import users_table
from src.models.user import User


class UsersGateway:
    table = users_table
    prim_key = 'user_id'
    model = User

    async def check_user_exists(self, where_clause) -> bool:
        query = select(
            [self.table.c[self.prim_key]]
        ).where(where_clause)

        user = await database.fetch_one(query)
        return user is not None

    async def if_phone_number_exists(self, phone_number: str) -> bool:
        clause = self.table.c.phone_number == phone_number
        return await self.check_user_exists(clause)

    async def insert(self, **fields) -> int:
        query = self.table.insert().values(**fields)
        return await database.execute(query)

    async def get_user_by_cond(self, condition) -> User | None:
        query = self.table.select().where(condition)
        data = await database.fetch_one(query)
        if data:
            return self.model(**data._mapping)

    async def check_user_exists_by_id(self, user_id: int) -> bool:
        return await self.check_user_exists(self.table.c.user_id == user_id)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.get_user_by_cond(self.table.c.user_id == user_id)

    async def get_user_by_phone_number(self, phone_number: str) -> User | None:
        return await self.get_user_by_cond(self.table.c.phone_number == phone_number)
