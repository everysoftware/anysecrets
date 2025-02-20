from abc import ABC

from app.db.dependencies import UOWDep
from app.db.uow import SQLAlchemyUOW


class Service(ABC):
    uow: SQLAlchemyUOW

    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow
