import asyncio
import json

import httpx
from utils import PLUGGY_BANK_CONNECTOR, PLUGGY_BANK_CREDENTIALS

from config import Settings
from pypluggy.api.client import PluggyClient
from pypluggy.api.type.investment import InvestmentType


async def get_investments(
    item_id: str, type: InvestmentType, export_to_json: bool = False
):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        investments = await client.fetch_investments(
            item_id=item_id, type=type
        )

        print('Investments successfully retrieved!\n')
        print(investments)

        if export_to_json:
            with open('investments.json', 'w') as f:
                investments_str = json.dumps(investments)
                f.write(investments)


if __name__ == '__main__':
    asyncio.run(get_investments(item_id='', type=''))
