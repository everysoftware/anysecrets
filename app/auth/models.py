from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base.models import AuditMixin, BaseOrm


class User(BaseOrm, AuditMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    name: Mapped[str]

    if not TYPE_CHECKING:
        id: Mapped[int] = mapped_column(Identity(), primary_key=True)
        email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
        hashed_password: Mapped[str] = mapped_column(String(length=1024))
        is_active: Mapped[bool] = mapped_column(default=1)
        is_superuser: Mapped[bool] = mapped_column(default=0)
        is_verified: Mapped[bool] = mapped_column(default=0)
