from sqlalchemy import Select

from backend.base.models import Entity
from backend.base.specification import Filter, Specification
from backend.db.repository import SQLAlchemyRepository
from backend.passwords.models import Password


class PasswordFilter(Filter):
    name_contains: str | None = None


class SearchPasswordSpec(Specification):
    user_id: int

    def to_expression[T](self, stmt: Select[T], model_type: type[Entity]) -> Select[T]:
        return stmt.where(model_type.user_id == self.user_id)


class PasswordRepository(SQLAlchemyRepository[Password]):
    model_type = Password
