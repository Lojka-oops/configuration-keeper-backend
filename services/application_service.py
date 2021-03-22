from datetime import datetime
from typing import List

from databases import Database
from sqlalchemy import desc, func, select

from models.applications import applications_table
from schemas import applications_schemas
from .base_service import BaseService
from .environment_service import EnvironmentService


class ApplicationService(BaseService):
    """Service for working with application entities

    """

    def __init__(
        self,
        database: Database,
        env_service: EnvironmentService
    ) -> None:
        """Construct a new :class: `ApplicationService`

        :param `database` - an instance of `databases.Database` 
        for asynchronous work with database

        """

        self.database = database
        self.env_service = env_service

    async def create(
        self, 
        data: applications_schemas.ApplicationCreateSchema
    ) -> applications_schemas.ApplicationSchema:
        """Creates a new application according to the passed data

        :param `data` -  an instance of `applications_schemas.ApplicationCreateSchema`
        which provide data to create an application

        :return an instance of `applications_schemas.ApplicationSchema`
        which provide application data

        """

        async with self.database.transaction():
            query = (applications_table.insert()
                .values(
                    name=data.name,
                    description=data.description,
                    created_at=datetime.now()
                )
                .returning(
                    applications_table.c.id,
                    applications_table.c.name,
                    applications_table.c.description,
                    applications_table.c.created_at,
                    applications_table.c.updated_at,
                    applications_table.c.deleted_at,
                    applications_table.c.is_deleted
                )
            )

            return await self.database.fetch_one(query)

    async def update(
        self,
        id: int,
        data: applications_schemas.ApplicationCreateSchema
    ) -> applications_schemas.ApplicationSchema:
        """Updates an application according to the passed data

        :param `id` - identifier of application

        :param `data` - an instance of `applications_schemas.ApplicationCreateSchema`
        which provide data to update an application

        :return an instance of `applications_schemas.ApplicationSchema`
        which provide application data

        """

        async with self.database.transaction():
            query = (
                applications_table.update()
                .where(applications_table.c.id == id)
                .values(
                    name=data.name,
                    description=data.description,
                    updated_at=datetime.now()
                )
                .returning(
                    applications_table.c.id,
                    applications_table.c.name,
                    applications_table.c.description,
                    applications_table.c.created_at,
                    applications_table.c.updated_at,
                    applications_table.c.deleted_at,
                    applications_table.c.is_deleted
                )
            )

            return await self.database.fetch_one(query)

    async def delete(self, id: int) -> None:
        """Deletes an application according passed application identifier

        :param `id` - identifier of application

        """

        async with self.database.transaction():
            query = (
                applications_table.update()
                .where(applications_table.c.id == id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            await self.database.execute(query)
            await self.env_service.delete_envs_for_app(id)

    async def get_apps(
        self,
        page: int,
        per_page: int
    ) -> List[applications_schemas.ApplicationSchema]:
        """Selects all applications from the database

        :param `page` - page number

        :param `per_page` - number of entities on one page

        :return list of `applications_schemas.ApplicationSchema`
        which provide application data

        """

        offset = (page - 1) * per_page
        query = (
            select(
                [
                    applications_table.c.id,
                    applications_table.c.name,
                    applications_table.c.description,
                    applications_table.c.created_at,
                    applications_table.c.updated_at,
                    applications_table.c.deleted_at,
                    applications_table.c.is_deleted
                ]
            )
            .select_from(applications_table)
            .where(applications_table.c.is_deleted == False)
            .order_by(desc(applications_table.c.created_at))
            .limit(per_page)
            .offset(offset)
        )

        return await self.database.fetch_all(query)

    async def get_apps_count(self) -> int:
        """Count applications in the database

        :return count of not deleted applications

        """

        query = (
            select([func.count()])
            .select_from(applications_table)
            .where(applications_table.c.is_deleted == False)
        )
        
        return await self.database.fetch_val(query)
