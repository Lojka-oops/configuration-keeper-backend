from datetime import datetime
from typing import List

from databases import Database
from sqlalchemy import desc, func, select, and_

from models.variables import variables_table
from schemas import variables_schemas


class VariableService():
    """Service for working with variable entities

    """

    def __init__(self, database: Database) -> None:
        """Construct a new :class: `VariableService`

        :param `database` - an instance of `databases.Database` 
        for asynchronous work with database

        """

        self.database = database

    async def create_var(
        self, 
        var: variables_schemas.VariableCreateSchema
    ) -> variables_schemas.VariableBaseSchema:
        """Creates a new variable according to the passed data

        :param `app` -  an instance of `variables_schemas.VariableCreateSchema`
        which provide data to create an variable

        :return an instance of `variables_schemas.VariableBaseSchema`
        which provide base variable data

        """

        async with self.database.transaction():
            query = (variables_table.insert()
                .values(
                    name=var.name,
                    value=var.value,
                    env_id=var.env_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                .returning(
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at
                )
            )

            return await self.database.fetch_one(query)

    async def get_vars(
        self,
        env_id: int,
        page: int = None,
        per_page: int = None
    ) -> List[variables_schemas.VariableBaseSchema]:
        """Selects all variables for environment from the database

        :param `env_id` - environment identifier

        :param `page` - page number

        :param `per_page` - number of entities on one page

        :return list of `variables_schemas.VariableBaseSchema`
        which provide base variable data

        """

        query = (
            select(
                [
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at
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

    async def get_vars_count(self, env_id: int) -> int:
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

    async def update_var(
        self,
        var_id: int,
        var: variables_schemas.VariableCreateSchema
    ) -> variables_schemas.VariableBaseSchema:
        """Updates an variable according to the passed data

        :param `var_id` - identifier of variable

        :param `var` - an instance of `variables_schemas.VariableCreateSchema`
        which provide data to update an variable

        :return an instance of `variables_schemas.VariableBaseSchema`
        which provide base variable data

        """

        async with self.database.transaction():
            query = (
                variables_table.update()
                .where(variables_table.c.id == var_id)
                .values(
                    name=var.name,
                    value=var.value,
                    updated_at=datetime.now()
                )
                .returning(
                    variables_table.c.id,
                    variables_table.c.name,
                    variables_table.c.value,
                    variables_table.c.created_at,
                    variables_table.c.updated_at
                )
            )
            
            return await self.database.fetch_one(query)

    async def delete_var(self, var_id: int):
        """Deletes an variable according passed variable identifier

        :param `var_id` - identifier of variable

        """

        async with self.database.transaction():
            query = (
                variables_table.update()
                .where(variables_table.c.id == var_id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            await self.database.execute(query)

    async def delete_vars_for_env(self, env_id):
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
