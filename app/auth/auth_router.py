from fastapi import APIRouter

from app.auth.backends import cookie_jwt_backend
from app.auth.dependencies import fastapi_users
from app.auth.schemas import SUserCreate, SUserRead

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(SUserRead, SUserCreate),
)
router.include_router(fastapi_users.get_auth_router(cookie_jwt_backend))
