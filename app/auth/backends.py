from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from app.auth.models import User
from app.config import settings

cookie_transport = CookieTransport(cookie_max_age=settings.app.auth_token_lifetime, cookie_secure=False)


def get_jwt_strategy() -> JWTStrategy[User, int]:
    return JWTStrategy(
        secret=settings.app.auth_secret,
        lifetime_seconds=settings.app.auth_token_lifetime,
    )


cookie_jwt_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
