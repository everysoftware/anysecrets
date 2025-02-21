from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from frontend.auth.client import AuthClient
from frontend.auth.exceptions import (
    AlreadyLoggedInException,
    RequiresLoginException,
)
from frontend.auth.schemas import SUser


def get_auth_client(request: Request) -> AuthClient:
    return AuthClient(request.cookies)


async def redirect_authenticated(
    client: Annotated[AuthClient, Depends(get_auth_client)],
) -> None:
    user = await client.get_me()

    if user is not None:
        raise AlreadyLoggedInException


async def get_me(
    client: Annotated[AuthClient, Depends(get_auth_client)],
) -> SUser:
    user = await client.get_me()

    if user is None:
        raise RequiresLoginException

    return user


MeDep = Annotated[SUser, Depends(get_me)]
