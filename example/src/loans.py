import asyncio
import json

import httpx

from config import Settings
from pypluggy.api.client import PluggyClient


async def get_loans(item_id: str, export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        loans = await client.fetch_loans(item_id=item_id)

        print('Loans successfully retrieved!')
        print(loans)

        if export_to_json:
            with open('loans.json', 'w') as f:
                loans_str = json.dumps(loans)
                f.write(loans_str)


if __name__ == '__main__':
    asyncio.run(get_loans(item_id=''))
