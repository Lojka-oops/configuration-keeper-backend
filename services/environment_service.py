from datetime import datetime
from typing import List

from databases import Database
from sqlalchemy import desc, func, select, and_

from models.environments import environments_table
from schemas import environments_schemas
from .base_service import BaseService
from .variable_service import VariableService


class EnvironmentService(BaseService):
    """Service for working with environment entities

    """

    def __init__(
        self,
        database: Database,
        var_service: VariableService
    ) -> None:
        """Construct a new :class: `EnvironmentService`

        :param `database` - an instance of `databases.Database` 
        for asynchronous work with database

        :param `var_service` - an instance of `services.VariableService` 
        for work with variables entity

        """

        self.database = database
        self.var_service = var_service

    async def create(
        self,
        data: environments_schemas.EnvironmentCreateSchema
    ) -> environments_schemas.EnvironmentSchema:
        """Creates a new environment according to the passed data

        :param `data` -  an instance of `environments_schemas.EnvironmentCreateSchema`
        which provide data to create an environment

        :return an instance of `environments_schemas.EnvironmentSchema`
        which provide base environment data

        """

        async with self.database.transaction():
            query = (environments_table.insert()
                .values(
                    name=data.name,
                    description=data.description,
                    app_id=data.app_id,
                    created_at=datetime.now()
                )
                .returning(
                    environments_table.c.id,
                    environments_table.c.name,
                    environments_table.c.code,
                    environments_table.c.description,
                    environments_table.c.created_at,
                    environments_table.c.updated_at,
                    environments_table.c.deleted_at,
                    environments_table.c.is_deleted
                )
            )

            return await self.database.fetch_one(query)
    
    async def update(
        self,
        id: int,
        data: environments_schemas.EnvironmentCreateSchema
    ) -> environments_schemas.EnvironmentSchema:
        """Updates an environment according to the passed data

        :param `id` - identifier of environment

        :param `data` - an instance of `environments_schemas.EnvironmentCreateSchema`
        which provide data to update an environment

        :return an instance of `environments_schemas.EnvironmentSchema`
        which provide base environment data

        """

        async with self.database.transaction():
            query = (
                environments_table.update()
                .where(environments_table.c.id == id)
                .values(
                    name=data.name,
                    description=data.description,
                    updated_at=datetime.now()
                )
                .returning(
                    environments_table.c.id,
                    environments_table.c.name,
                    environments_table.c.code,
                    environments_table.c.description,
                    environments_table.c.created_at,
                    environments_table.c.updated_at,
                    environments_table.c.deleted_at,
                    environments_table.c.is_deleted
                )
            )

            return await self.database.fetch_one(query)

    async def delete(self, id: int) -> None:
        """Deletes an environment according passed environment identifier

        :param `id` - identifier of environment

        """

        async with self.database.transaction():
            query = (
                environments_table.update()
                .where(environments_table.c.id == id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            await self.database.execute(query)
            await self.var_service.delete_vars_for_env(id)

    async def get_envs(
        self,
        app_id: int,
        page: int,
        per_page: int
    ) -> List[environments_schemas.EnvironmentSchema]:
        """Selects all environments for application from the database

        :param `app_id` - application identifier

        :param `page` - page number

        :param `per_page` - number of entities on one page

        :return list of `environments_schemas.EnvironmentSchema`
        which provide base environment data

        """

        offset = (page - 1) * per_page
        query = (
            select(
                [
                    environments_table.c.id,
                    environments_table.c.name,
                    environments_table.c.code,
                    environments_table.c.description,
                    environments_table.c.created_at,
                    environments_table.c.updated_at,
                    environments_table.c.deleted_at,
                    environments_table.c.is_deleted
                ]
            )
            .select_from(environments_table)
            .where(
                and_(
                    environments_table.c.app_id == app_id,
                    environments_table.c.is_deleted == False
                )
            )
            .order_by(desc(environments_table.c.created_at))
            .limit(per_page)
            .offset(offset)
        )

        return await self.database.fetch_all(query)

    async def get_env_by_code(
        self, 
        code: str
    ) -> dict:
        """Selects an environment from the database 
        that matches the passed code

        :param `code` - unique code of environment

        :return dictionary with two fields `id` and `name`

        """

        query = (
            select(
                [
                    environments_table.c.id,
                    environments_table.c.name
                ]
            )
            .select_from(environments_table)
            .where(
                and_(
                    environments_table.c.code == code,
                    environments_table.c.is_deleted == False
                )
            )
        )
        
        return await self.database.fetch_one(query)

    async def get_envs_count(self, app_id: int) -> int:
        """Count environments in the database

        :param `app_id` - application identifier

        :return count of not deleted environments

        """

        query = (
            select([func.count()])
            .select_from(environments_table)
            .where(
                and_(
                    environments_table.c.app_id == app_id,
                    environments_table.c.is_deleted == False
                )
            )
        )
        
        return await self.database.fetch_val(query)

    async def delete_envs_for_app(self, app_id):
        """Deletes all environments by application identifier

        :param `app_id` - identifier of application

        """

        async with self.database.transaction():
            query = (
                environments_table.update()
                .where(environments_table.c.app_id == app_id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
                .returning(
                    environments_table.c.id,
                )
            )
            updated_envs = await self.database.fetch_all(query)

        for env in updated_envs:
            await self.var_service.delete_vars_for_env(env['id'])
