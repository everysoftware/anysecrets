from typing import Any

from fastapi import APIRouter, Depends

from backend.auth.auth_router import router as auth_router
from backend.auth.dependencies import current_user
from backend.auth.user_router import router as users_router
from backend.passwords.router import router as passwords_router

unprotected_router = APIRouter()
unprotected_router.include_router(auth_router)

protected_router = APIRouter(dependencies=[Depends(current_user)])

protected_router.include_router(users_router)
protected_router.include_router(passwords_router)

main_router = APIRouter()


@main_router.get("/hc", include_in_schema=False)
def hc() -> dict[str, Any]:
    return {"status": "ok"}


@main_router.get("/exc", include_in_schema=False)
def exc() -> None:
    raise Exception("test exception")


main_router.include_router(unprotected_router)
main_router.include_router(protected_router)
