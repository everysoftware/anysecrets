from app.auth.schemas import SUserRead
from app.base.specification import Specification
from app.base.types import UUID
from app.passwords.models import Password
from app.passwords.schemas import (
    PasswordCreate,
    PasswordItem,
    PasswordPage,
    PasswordUpdate,
)
from app.service import Service


class PasswordUseCases(Service):
    async def create(self, user: SUserRead, create_dto: PasswordCreate) -> Password:
        password = Password(user_id=user.id, **create_dto.model_dump(exclude={"username", "password"}))
        password.set_sensitive(create_dto.username, create_dto.password)
        await self.uow.passwords.add(password)
        await self.uow.commit()
        return password

    async def get(self, password_id: UUID) -> Password | None:
        return await self.uow.passwords.get(password_id)

    async def get_one(self, password_id: UUID) -> Password:
        password = await self.get(password_id)
        if password is None:
            raise ValueError("Password not found")
        return password

    async def update(self, password: Password, update_dto: PasswordUpdate) -> Password:
        password.merge_model(update_dto, exclude={"username", "password"})
        password.update_sensitive(update_dto.username, update_dto.password)
        await self.uow.commit()
        return password

    async def delete(self, password: Password) -> Password:
        password = await self.uow.passwords.remove(password)
        await self.uow.commit()
        return password

    async def search(self, user: SUserRead, *spec: Specification) -> PasswordPage:
        page = await self.uow.passwords.get_many(*spec)
        items = [PasswordItem.model_validate(i) for i in page.items]
        return PasswordPage(items=items)
