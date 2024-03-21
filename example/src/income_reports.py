import asyncio
import json

import httpx

from config import Settings
from pypluggy.api.client import PluggyClient


async def get_income_report(item_id: str, export_to_json: bool = False):

    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        report = await client.fetch_income_reports(item_id)

        if export_to_json:
            json_str = json.dumps(report, indent=4)

            with open(
                'income_report.json', 'w', encoding='utf-8'
            ) as json_file:
                json_file.write(json_str)

        print(report)


if __name__ == '__main__':
    asyncio.run(get_income_report(item_id=''))
