import asyncio

import httpx

from config import Settings
from pluggy.api.base_api import BaseApi


async def auth_user() -> str:
    async with httpx.AsyncClient() as session:
        base_api = BaseApi(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        token = await base_api.get_api_key()

        print('User Authentication was successful!')
        print(f"Here's your X-API-TOKEN:\n{token}")


if __name__ == '__main__':
    asyncio.run(auth_user())
