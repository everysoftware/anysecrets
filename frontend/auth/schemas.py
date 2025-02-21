import datetime

from frontend.schemas import SBase


class SUser(SBase):
    id: int
    email: str
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime
