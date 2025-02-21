from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse, Response

from frontend.auth.client import AuthClient
from frontend.auth.dependencies import get_auth_client, redirect_authenticated
from frontend.templating import templates

router = APIRouter(tags=["Auth"])


@router.get("/", dependencies=[Depends(redirect_authenticated)])
def onboarding(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth/onboarding.html", {"request": request})


@router.get("/register", dependencies=[Depends(redirect_authenticated)])
def register(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth/registration.html", {"request": request})


@router.get("/login", dependencies=[Depends(redirect_authenticated)])
def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/logout")
async def logout(
    client: Annotated[AuthClient, Depends(get_auth_client)],
) -> Response:
    await client.logout()
    response = RedirectResponse("/login", status.HTTP_307_TEMPORARY_REDIRECT)
    response.delete_cookie("fastapiusersauth")
    return response
