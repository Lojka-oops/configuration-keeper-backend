from datetime import datetime
from typing import Callable, TypeVar

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
        """
        """

        updated_data = []
        update_date = datetime.now()

        for key, old_value in entity_old_data.items():
            if hasattr(entity_new_data, key):
                new_value = getattr(entity_new_data, key)

                if new_value != old_value:
                    updated_data.append(
                        {
                            'entity_id': entity_id,
                            'entity_type': entity_type,
                            'field': key,
                            'old_value': old_value,
                            'new_value': new_value,
                            'created_at': update_date
                        }
                    )

        for data in updated_data:
            await self.create(data)

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

    async def update(self, id: int, data: BaseSchema) -> BaseSchema:
        raise NotImplementedError('Change history entity can\'t be updated!')

    async def delete(self, id: int) -> None:
        raise NotImplementedError('Change history entity can\'t be deleted!')
