from datetime import datetime
from typing import List

from databases import Database
from databases.backends.postgres import Record
from sqlalchemy import desc, func, select, and_, Table
from pydantic import BaseModel

from models.change_history import change_history_table
from schemas.base_schemas import BaseSchema
from .base_service import BaseService


class ChangeHistoryService(BaseService):
    """Service for working with change history entities

    """

    def __init__(
        self,
        database: Database
    ) -> None:
        """Construct a new :class: `ChangeHistoryService`

        :param `database` - an instance of `databases.Database` 
        for asynchronous work with database

        """

        self.database = database

    async def make_history(
        self,
        entity_id: int,
        entity_type: str,
        entity_new_data: BaseModel,
        entity_old_data: BaseModel
    ) -> None:
        """Compares old and new entity data and create change history entity
        for each difference

        :param `entity_id` - entity id

        :param `entity_type` - type of entity (Application, Environment, Variable)

        :param `entity_new_data` - entity new data

        :param `entity_old_data` - entity old data

        """

        update_date = datetime.now()

        for key, old_value in entity_old_data.items():
            if hasattr(entity_new_data, key):
                new_value = getattr(entity_new_data, key)

                if new_value != old_value:
                    await self.create(
                        {
                            'entity_id': entity_id,
                            'entity_type': entity_type,
                            'field': key,
                            'old_value': old_value,
                            'new_value': new_value,
                            'created_at': update_date
                        }
                    )

    async def create(
        self,
        data: dict
    ) -> None:
        """Creates a new change history record according to the passed data

        :param `data` - dictionary which provide data to create an application

        """

        async with self.database.transaction():
            query = (
                change_history_table.insert()
                .values(**data)
            )
            await self.database.execute(query)

    async def get_list(
        self,
        entity_type: str, 
        entity_id: int,
        page: int,
        per_page: int
    ) -> List[Record]:
        """Selects change history for entity from the database

        :param `entity_type` - entity type

        :param `entity_id` - entity identifier

        :param `page` - page number

        :param `per_page` - number of entities on one page

        :return list of `databases.backends.postgres.Record`
        which provide change history data for specific entity

        """

        offset = (page - 1) * per_page
        query = (
            select(
                [
                    change_history_table.c.id,
                    change_history_table.c.entity_type,
                    change_history_table.c.entity_id,
                    change_history_table.c.field,
                    change_history_table.c.old_value,
                    change_history_table.c.new_value,
                    change_history_table.c.created_at
                ]
            )
            .select_from(change_history_table)
            .where(
                and_(
                    change_history_table.c.entity_id == entity_id,
                    change_history_table.c.entity_type == entity_type
                )
            )
            .order_by(desc(change_history_table.c.created_at))
            .limit(per_page)
            .offset(offset)
        )

        return await self.database.fetch_all(query)

    async def get_count(
        self,
        entity_type: str, 
        entity_id: int
    ) -> int:
        """Count change history entities in the database

        :param `entity_type` - entity type

        :param `entity_id` - entity identifier

        :return count of change history entities

        """

        query = (
            select([func.count()])
            .select_from(change_history_table)
            .where(
                and_(
                    change_history_table.c.entity_id == entity_id,
                    change_history_table.c.entity_type == entity_type
                )
            )
        )
        
        return await self.database.fetch_val(query)

    async def update(self, id: int, data: BaseSchema) -> BaseSchema:
        raise NotImplementedError('Change history entity can\'t be updated!')

    async def delete(self, id: int) -> None:
        raise NotImplementedError('Change history entity can\'t be deleted!')
