import datetime
from uuid import UUID

from frontend.schemas import SBase, SPage


class SPasswordRead(SBase):
    id: UUID
    user_id: int
    name: str
    username: str
    password: str
    url: str = ""
    note: str = ""
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SPasswordItem(SBase):
    id: UUID
    name: str
    username: str
    url: str = ""


class SPasswordPage(SPage[SPasswordItem]):
    pass
