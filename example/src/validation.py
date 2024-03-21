import asyncio

import httpx
from utils import PLUGGY_BANK_CONNECTOR, PLUGGY_BANK_CREDENTIALS

from config import Settings
from pypluggy.api.client import PluggyClient


async def validate_parameters(connector_id, parameters: dict):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        result = await client.validate_parameters(
            connector_id, parameters=parameters
        )

        print(result)


if __name__ == '__main__':
    asyncio.run(
        validate_parameters(PLUGGY_BANK_CONNECTOR, PLUGGY_BANK_CREDENTIALS)
    )
