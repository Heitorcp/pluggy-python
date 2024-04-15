import asyncio
import json

import httpx

from config import Settings
from pypluggy.api.client import PluggyClient


async def get_all_transactions(account_id: str, export_to_json: bool = False):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        txs = await client.fetch_all_transactions(account_id)
        print(txs)

    if export_to_json:
        with open('transactions.json', 'w') as json_file:
            json_str = json.dumps(txs, indent=4)
            json_file.write(json_str)


async def update_txs_category(transaction_id, category_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        try:
            await client.update_transaction_category(
                transaction_id, category_id
            )
            print('Transaction category successfully updated.')
        except BaseException as e:
            print(f'An Exception occured {e}')
            raise e


if __name__ == '__main__':
    asyncio.run(update_txs_category(tx_id='', category_id=''))
