from starlette.requests import Request

from frontend.passwords.client import PasswordClient


def get_password_client(request: Request) -> PasswordClient:
    return PasswordClient(request.cookies)
