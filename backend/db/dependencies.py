from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from backend.db.connection import session_factory
from backend.db.uow import IUnitOfWork, SQLAlchemyUOW


async def get_uow() -> AsyncIterator[IUnitOfWork]:
    async with SQLAlchemyUOW(session_factory) as uow:
        yield uow


UOWDep = Annotated[SQLAlchemyUOW, Depends(get_uow)]
