import asyncio
import json

import httpx

from config import Settings
from pluggy.api.client import PluggyClient


async def retrieve_identity(item_id: str, export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        identity = await client.fetch_identity_by_item_id(item_id)
        print(identity)

    if export_to_json:
        with open('identity.json', 'w') as f:
            identity_str = json.dumps(identity, indent=4)
            f.write(identity_str)


if __name__ == '__main__':
    asyncio.run(retrieve_identity(item_id='', export_to_json=False))
