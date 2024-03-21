import asyncio 
import json 
from config import Settings
import httpx

from pypluggy.api.client import PluggyClient


async def fetch_categories(export_to_json: bool = False):

    async with httpx.AsyncClient() as session:
        client = PluggyClient(
            Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session
        )
        categories = await client.fetch_categories()

        if export_to_json:
            json_str = json.dumps(categories, indent=4)

            with open("categories.json", "w", encoding="utf-8") as json_file:
                json_file.write(json_str)

        print(categories)

if __name__ == "__main__":
    asyncio.run(fetch_categories(export_to_json=True))
