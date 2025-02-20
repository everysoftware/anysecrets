from pydantic import Field

from app.base.schemas import BaseModel, EntityDTO
from app.base.specification import Page


class PasswordBase(BaseModel):
    name: str = Field(min_length=1, max_length=128, examples=["Facebook"])
    url: str = Field("", max_length=256, examples=["https://facebook.com"])
    note: str = Field("", max_length=256, examples=["Sample comment"])


class PasswordDTO(EntityDTO, PasswordBase):
    user_id: int
    username: str
    password: str


class PasswordCreate(PasswordBase):
    username: str = Field(min_length=1, max_length=128, examples=["user@example.com"])
    password: str = Field(min_length=1, max_length=128, examples=["qwerty123"])


class PasswordUpdate(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=128, examples=["user@example.com"])
    password: str | None = Field(None, min_length=1, max_length=128, examples=["qwerty123"])
    name: str | None = Field(None, min_length=1, max_length=128, examples=["Facebook"])
    url: str | None = Field(None, max_length=256, examples=["https://facebook.com"])
    note: str | None = Field(None, max_length=256, examples=["Sample comment"])


class PasswordItem(PasswordDTO):
    password: str = Field(exclude=True)


class PasswordPage(Page[PasswordItem]):
    pass
