from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.base.models import Entity
from app.base.specification import Page, Specification
from app.base.types import UUID

T = TypeVar("T", bound=Entity)


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, model: T) -> T: ...

    @abstractmethod
    async def get(self, id: UUID) -> T | None: ...

    @abstractmethod
    async def get_one(self, id: UUID) -> T: ...

    @abstractmethod
    async def find(self, *spec: Specification) -> T | None: ...

    @abstractmethod
    async def find_one(self, *spec: Specification) -> T: ...

    @abstractmethod
    async def remove(self, model: T) -> T: ...

    @abstractmethod
    async def get_many(self, *spec: Specification) -> Page[T]: ...
