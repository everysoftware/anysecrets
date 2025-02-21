from urllib.parse import urlencode
from uuid import UUID

import aiohttp
from starlette import status

from frontend.client import BackendClient
from frontend.passwords.schemas import SPasswordPage, SPasswordRead


class PasswordClient(BackendClient):
    async def get_password(self, item_id: UUID) -> SPasswordRead:
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(
                f"{self.base_url}/passwords/{item_id}",
            ) as response:
                if response.status != status.HTTP_200_OK:
                    response_text = await response.text()
                    raise Exception(response_text)

                response_json = await response.json()
                response_schema = SPasswordRead.model_validate(response_json)

                return response_schema

    async def get_passwords(self, q: str = "", limit: int = 100) -> SPasswordPage:
        params = urlencode({"name_contains": q, "limit": limit})
        url = f"{self.base_url}/passwords?{params}"
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    response_text = await response.text()
                    raise Exception(response_text)

                response_json = await response.json()
                response_schema = SPasswordPage.model_validate(response_json)

                return response_schema
