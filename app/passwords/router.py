from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import UserDep
from app.base.specification import BasicPagination, Sort
from app.passwords.dependencies import PasswordServiceDep, valid_password
from app.passwords.models import Password
from app.passwords.repositories import PasswordCriteria
from app.passwords.schemas import (
    PasswordCreate,
    PasswordDTO,
    PasswordPage,
    PasswordUpdate,
)

router = APIRouter(prefix="/passwords", tags=["Passwords"])


@router.post("", status_code=status.HTTP_201_CREATED, description="Create a new password", response_model=PasswordDTO)
async def create_password(
    create_dto: PasswordCreate,
    user: UserDep,
    service: PasswordServiceDep,
) -> Any:
    return await service.create(user, create_dto)


@router.get(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Get a password by id",
    response_model=PasswordDTO,
)
async def get_password(
    password: Annotated[PasswordDTO, Depends(valid_password)],
) -> Any:
    return password


@router.patch(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Update a password",
    response_model=PasswordDTO,
)
async def patch_password(
    service: PasswordServiceDep,
    update: PasswordUpdate,
    password: Annotated[Password, Depends(valid_password)],
) -> Any:
    return await service.update(password, update)


@router.delete(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Delete a password",
    response_model=PasswordDTO,
)
async def delete_password(
    service: PasswordServiceDep,
    password: Annotated[Password, Depends(valid_password)],
) -> Any:
    return await service.delete(password)


@router.get("", status_code=status.HTTP_200_OK, description="Search for passwords", response_model=PasswordPage)
async def search_password(
    service: PasswordServiceDep,
    user: UserDep,
    criteria: Annotated[PasswordCriteria, Depends()],
    sort: Annotated[Sort, Depends()],
    pagination: Annotated[BasicPagination, Depends()],
) -> Any:
    return await service.search(user, criteria, sort, pagination)
