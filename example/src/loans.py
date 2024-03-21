import asyncio
import json

import httpx
from utils import PLUGGY_BANK_CONNECTOR, PLUGGY_BANK_CREDENTIALS

from config import Settings
from pluggy.api.client import PluggyClient


async def get_loans(export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )

        # Criando um Item usando a SandBox
        body = PLUGGY_BANK_CREDENTIALS
        item = await client.create_item(PLUGGY_BANK_CONNECTOR, None, body)

        loans = await client.fetch_loans(item_id=item['id'])

        print('Loans successfully retrieved!')
        print(loans)

        if export_to_json:
            with open('loans.json', 'w') as f:
                investments_str = json.dumps(loans)
                f.write(loans)


if __name__ == '__main__':
    asyncio.run(get_loans())
