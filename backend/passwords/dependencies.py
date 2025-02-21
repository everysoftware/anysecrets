from typing import Annotated

from fastapi import Depends

from backend.auth.dependencies import UserDep
from backend.base.types import UUID
from backend.exceptions import NotEnoughRights
from backend.passwords.exceptions import PasswordNotFound
from backend.passwords.models import Password
from backend.passwords.service import PasswordUseCases

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
