from app.base.specification import Criteria
from app.db.repository import SQLAlchemyRepository
from app.passwords.models import Password


class PasswordCriteria(Criteria):
    name_contains: str | None = None


class PasswordRepository(SQLAlchemyRepository[Password]):
    model_type = Password
