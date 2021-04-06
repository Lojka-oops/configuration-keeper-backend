from datetime import datetime
from typing import List

from databases import Database
from databases.backends.postgres import Record
from sqlalchemy import desc, func, select, and_

from models.variables import variables_table
from .base_service import BaseService
from schemas.variable_schemas import VariableCreateSchema


class VariableService(BaseService):
    """Service for working with variable entities

    """

    def __init__(self, database: Database) -> None:
        """Construct a new :class: `VariableService`

        :param `database` - an instance of `databases.Database` 
        for asynchronous work with database

        """

        self.database = database

    async def create(
        self, 
        data: VariableCreateSchema
    ) -> Record:
        """Creates a new variable according to the passed data

        :param `data` -  an instance of `VariableCreateSchema`
        which provide data to create an variable

        :return an instance of `databases.backends.postgres.Record`
        which provide base variable data

        """

        async with self.database.transaction():
            query = (variables_table.insert()
                .values(
                    name=data.name,
                    value=data.value,
                    env_id=data.env_id,
                    created_at=datetime.now()
                )
                .returning(
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at,
                    variables_table.c.deleted_at,
                    variables_table.c.is_deleted
                )
            )

            return await self.database.fetch_one(query)

    async def update(
        self,
        id: int,
        data: VariableCreateSchema
    ) -> Record:
        """Updates an variable according to the passed data

        :param `id` - identifier of variable

        :param `data` - an instance of `VariableCreateSchema`
        which provide data to update an variable

        :return an instance of `databases.backends.postgres.Record`
        which provide base variable data

        """

        async with self.database.transaction():
            query = (
                variables_table.update()
                .where(variables_table.c.id == id)
                .values(
                    name=data.name,
                    value=data.value,
                    updated_at=datetime.now()
                )
                .returning(
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at,
                    variables_table.c.deleted_at,
                    variables_table.c.is_deleted
                )
            )
            
            return await self.database.fetch_one(query)

    async def delete(self, id: int):
        """Deletes an variable according passed variable identifier

        :param `id` - identifier of variable

        """

        async with self.database.transaction():
            query = (
                variables_table.update()
                .where(variables_table.c.id == id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            await self.database.execute(query)

    async def get_list(
        self,
        env_id: int,
        page: int = None,
        per_page: int = None
    ) -> List[Record]:
        """Selects all variables for environment from the database

        :param `env_id` - environment identifier

        :param `page` - page number

        :param `per_page` - number of entities on one page

        :return list of `databases.backends.postgres.Record`
        which provide base variable data

        """

        query = (
            select(
                [
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at,
                    variables_table.c.deleted_at,
                    variables_table.c.is_deleted
                ]
            )
            .select_from(variables_table)
            .where(
                and_(
                    variables_table.c.env_id == env_id,
                    variables_table.c.is_deleted == False
                )
            )
            .order_by(desc(variables_table.c.created_at))
        )

        if page and per_page:
            offset = (page - 1) * per_page
            query = query.limit(per_page).offset(offset)

        return await self.database.fetch_all(query)

    async def get_count(self, env_id: int) -> int:
        """Count variables in the database

        :param `env_id` - environment identifier

        :return count of not deleted variables

        """

        query = (
            select([func.count()])
            .select_from(variables_table)
            .where(
                and_(
                    variables_table.c.env_id == env_id,
                    variables_table.c.is_deleted == False
                )
            )
        )
        
        return await self.database.fetch_val(query)

    async def delete_by_env_id(self, env_id):
        """Deletes all variables by environmetn identifier

        :param `env_id` - identifier of environment

        """

        async with self.database.transaction():
            query = (
                variables_table.update()
                .where(variables_table.c.env_id == env_id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            await self.database.execute(query)
