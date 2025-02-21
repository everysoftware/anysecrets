from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from backend.base.models import Entity
from backend.base.specification import Page, Specification
from backend.base.types import UUID

T = TypeVar("T", bound=Entity)


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, model: T) -> T: ...

    @abstractmethod
    async def get(self, ident: UUID) -> T | None: ...

    @abstractmethod
    async def get_one(self, ident: UUID) -> T: ...

    @abstractmethod
    async def find(self, *spec: Specification) -> T | None: ...

    @abstractmethod
    async def find_one(self, *spec: Specification) -> T: ...

    @abstractmethod
    async def remove(self, model: T) -> T: ...

    @abstractmethod
    async def get_many(self, *spec: Specification) -> Page[T]: ...
