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
        get_opportunities(item_id='')
    )
