from abc import abstractmethod, ABC

from schemas.base_schema import BaseSchema


class BaseService(ABC):

    @abstractmethod
    async def create(self, data: BaseSchema) -> BaseSchema:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, id: int, data: BaseSchema) -> BaseSchema:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError()
