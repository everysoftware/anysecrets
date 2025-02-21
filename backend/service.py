from abc import ABC

from backend.db.dependencies import UOWDep
from backend.db.uow import SQLAlchemyUOW


class Service(ABC):
    uow: SQLAlchemyUOW

    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow
