from abc import ABC
from typing import Any

from frontend.config import settings


class BackendClient(ABC):
    base_url: str = settings.backend_url
    cookies: dict[str, Any]

    def __init__(self, cookies: dict[str, Any]) -> None:
        self.cookies = cookies
