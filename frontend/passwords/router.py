import datetime
from typing import Annotated
from uuid import UUID

import humanize
from fastapi import APIRouter, Depends, Path, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse

from frontend.auth.dependencies import get_me
from frontend.passwords.client import PasswordClient
from frontend.passwords.dependencies import get_password_client
from frontend.templating import templates

router = APIRouter(tags=["Passwords"], dependencies=[Depends(get_me)])


@router.get("/passwords/add")
def add_password(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("passwords/creation.html", {"request": request})


@router.get("/passwords/{item_id}")
async def get_password(
    request: Request,
    client: Annotated[PasswordClient, Depends(get_password_client)],
    item_id: UUID = Path(),
) -> HTMLResponse:
    password = await client.get_password(item_id)
    info = password.model_dump(mode="json")
    info["updated_at_human"] = humanize.naturaltime(password.updated_at, when=datetime.datetime.utcnow())
    return templates.TemplateResponse("passwords/view.html", {"request": request, "password": info})


@router.get("/passwords/{item_id}/edit")
async def edit_password(
    request: Request,
    client: Annotated[PasswordClient, Depends(get_password_client)],
    item_id: UUID = Path(),
) -> HTMLResponse:
    password = await client.get_password(item_id)
    return templates.TemplateResponse("passwords/editing.html", {"request": request, "password": password})


@router.get("/passwords")
async def get_passwords(
    request: Request,
    client: Annotated[PasswordClient, Depends(get_password_client)],
    q: str = Query(""),
) -> HTMLResponse:
    page = await client.get_passwords(q=q)
    response = templates.TemplateResponse(
        "passwords/pagination.html",
        {"request": request, "passwords": page.items, "query": q},
    )
    return response
