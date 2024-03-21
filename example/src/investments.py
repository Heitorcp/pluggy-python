import asyncio
import json

import httpx
from utils import PLUGGY_BANK_CONNECTOR, PLUGGY_BANK_CREDENTIALS

from config import Settings
from pluggy.api.client import PluggyClient


async def get_investments(export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        # Criando um Item usando a SandBox
        body = PLUGGY_BANK_CREDENTIALS
        item = await client.create_item(PLUGGY_BANK_CONNECTOR, None, body)

        investments = await client.fetch_investments(
            item_id=item['id'], type='EQUITY'
        )

        print('Investments successfully retrieved!')
        print(investments)

        if export_to_json:
            with open('investments.json', 'w') as f:
                investments_str = json.dumps(investments)
                f.write(investments)


if __name__ == '__main__':
    asyncio.run(get_investments())
