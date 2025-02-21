from typing import Any

import aiohttp
from starlette import status

from frontend.auth.schemas import SUser
from frontend.client import BackendClient


class AuthClient(BackendClient):
    async def get_me(self) -> SUser | None:
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(
                f"{self.base_url}/users/me",
            ) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                response_json = await response.json()
                response_schema = SUser.model_validate(response_json)

                return response_schema

    async def logout(self) -> dict[str, Any] | None:
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(
                f"{self.base_url}/auth/logout",
            ) as response:
                return response.cookies
