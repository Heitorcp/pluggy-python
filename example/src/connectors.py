import asyncio
import json

import httpx
from utils import PLUGGY_BANK_CONNECTOR

from config import Settings
from pypluggy.api.client import PluggyClient


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


async def fetch_connector(conenctor_id: str):

    try:
        async with httpx.AsyncClient() as session:
            client = PluggyClient(
                Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
            )

            connector = await client.fetch_connector(conenctor_id)

            print('Connector successfully retrieved!')
            print(connector)

    except Exception as e:
        raise e


if __name__ == '__main__':
    asyncio.run(fetch_connector(conenctor_id=PLUGGY_BANK_CONNECTOR))
