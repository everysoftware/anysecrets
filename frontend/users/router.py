from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from frontend.auth.dependencies import MeDep, get_me
from frontend.templating import templates

router = APIRouter(tags=["Users"], dependencies=[Depends(get_me)])


@router.get("/me")
def show_me(request: Request, user: MeDep) -> HTMLResponse:
    return templates.TemplateResponse(
        "users/me.html",
        {"request": request, "user": user.model_dump(mode="json")},
    )
