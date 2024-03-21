import asyncio
import json

import httpx

from config import Settings
from pluggy.api.client import PluggyClient


async def fetch_connectors(export_to_json: bool = False):

    try:

        async with httpx.AsyncClient() as session:
            client = PluggyClient(
                Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
            )
            connectors = await client.fetch_connectors()

            print(connectors)

            if export_to_json:
                json_str = json.dumps(connectors, indent=4)

                with open('connectors.json', 'w') as json_file:
                    json_file.write(json_str)

    except Exception as e:
        raise e


async def fetch_connector(connector_id: int):

    try:
        async with httpx.AsyncClient() as session:
            client = PluggyClient(
                Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
            )
            connector = await client.fetch_connector(id=connector_id)

            print(connector)
    except:
        pass


if __name__ == '__main__':
    asyncio.run(fetch_connectors(export_to_json=True))
