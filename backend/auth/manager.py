from fastapi_users import BaseUserManager, IntegerIDMixin

from backend.auth.models import User
from backend.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.app.auth_secret
    verification_token_secret = settings.app.auth_secret
