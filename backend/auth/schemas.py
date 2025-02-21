import datetime

from fastapi_users import schemas
from pydantic import EmailStr, Field

from backend.base.schemas import BaseModel


class SUserRead(BaseModel, schemas.BaseUser[int]):
    id: int
    email: EmailStr
    hashed_password: str = Field(exclude=True)
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SUserCreate(BaseModel, schemas.BaseUserCreate):
    name: str
    email: EmailStr
    password: str = Field(
        min_length=1,
        max_length=128,
        examples=["changeme"],
    )


class SUserUpdate(BaseModel, schemas.BaseUserUpdate):
    name: str | None = None
    password: str | None = None
