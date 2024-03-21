import asyncio
import json

import httpx

from config import Settings
from pypluggy.api.client import PluggyClient


async def get_accounts_info(item_id: str, export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        accounts = await client.fetch_accounts(item_id, type='BANK')
        print(accounts)

        if export_to_json:
            with open('accounts.json', 'w') as f:
                account_str = json.dumps(accounts, indent=4)
                f.write(account_str)


async def get_account_info(account_id: str, export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        accounts = await client.fetch_account(account_id, type='BANK')
        print(accounts)

        if export_to_json:
            with open('account.json', 'w') as f:
                account_str = json.dumps(accounts, indent=4)
                f.write(account_str)


if __name__ == '__main__':
    asyncio.run(get_accounts_info(item_id='', export_to_json=True))
