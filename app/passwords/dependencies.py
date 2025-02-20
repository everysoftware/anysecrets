from typing import Annotated

from fastapi import Depends

from app.auth.dependencies import UserDep
from app.base.types import UUID
from app.exceptions import NotEnoughRights
from app.passwords.exceptions import PasswordNotFound
from app.passwords.models import Password
from app.passwords.service import PasswordUseCases

PasswordServiceDep = Annotated[PasswordUseCases, Depends()]


async def valid_password(
    service: PasswordServiceDep,
    user: UserDep,
    password_id: UUID,
) -> Password:
    password = await service.get(password_id)
    if password is None:
        raise PasswordNotFound()
    if password.user_id != user.id and not user.is_superuser:
        raise NotEnoughRights()
    return password
