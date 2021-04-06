from abc import abstractmethod, ABC
from typing import List

from schemas.base_schema import BaseSchema


class BaseService(ABC):

    @abstractmethod
    async def create(self, data: BaseSchema) -> BaseSchema: pass

    @abstractmethod
    async def update(self, id: int, data: BaseSchema) -> BaseSchema: pass

    @abstractmethod
    async def delete(self, id: int) -> None: pass
