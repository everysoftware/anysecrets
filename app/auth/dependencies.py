from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.models import User
from app.db.connection import session_factory

from .backends import cookie_jwt_backend
from .manager import UserManager
from .schemas import SUserRead


async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase[User, int], None]:
    async with session_factory() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: Annotated[SQLAlchemyUserDatabase[User, int], Depends(get_user_db)],
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [cookie_jwt_backend],
)

current_user = fastapi_users.current_user()


def get_current_user(user: User = Depends(current_user)) -> SUserRead:
    return SUserRead.model_validate(user)


UserDep = Annotated[SUserRead, Depends(get_current_user)]
