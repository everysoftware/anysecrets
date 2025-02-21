from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles

from frontend.auth.exceptions import (
    AlreadyLoggedInException,
    RequiresLoginException,
)
from frontend.auth.router import router as auth_router
from frontend.passwords.router import router as passwords_router
from frontend.users.router import router as users_router

routers = [auth_router, passwords_router, users_router]

app = FastAPI(title="Secrets | Frontend")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(RequiresLoginException)
async def requires_login_handler(_request: Request, _exc: RequiresLoginException) -> Response:
    return RedirectResponse(url="/login")


@app.exception_handler(AlreadyLoggedInException)
async def already_logged_in_handler(_request: Request, _exc: AlreadyLoggedInException) -> Response:
    return RedirectResponse(url="/passwords")


for router in routers:
    app.include_router(router)


@app.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hc", include_in_schema=False)
def hc() -> dict[str, str]:
    return {"status": "ok"}
