import asyncio

import httpx

from config import Settings
from pypluggy.api.client import PluggyClient


async def get_opportunities(item_id: str):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        try:
            opportunities = await client.fetch_opportunities(item_id=item_id)
            print(f'Opportunities successfully retrieved!\n')
            print(opportunities)

        except Exception as e:
            raise e


if __name__ == '__main__':
    asyncio.run(
        get_opportunities(item_id='f2213b33-b1db-4f56-8d8e-f38b053e7cb3')
    )
