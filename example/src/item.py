import asyncio 
import httpx 
from config import Settings

from pluggy.api.client import PluggyClient 
from utils import PLUGGY_BANK_CREDENTIALS, PLUGGY_BANK_CONNECTOR

#Using Pluggy Sandbox to create an item
async def create_item():
    
        async with httpx.AsyncClient() as session:
            client = PluggyClient(Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session)

            body = PLUGGY_BANK_CREDENTIALS

            try:

                item = await client.create_item(PLUGGY_BANK_CONNECTOR, None, body=body)
                if item:
                    print("Item created successfully") 
                    print(item) 

            except Exception as e:
                raise e 
            
async def retrieve_item():
     
    async with httpx.AsyncClient() as session:
        client = PluggyClient(Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session) 

        try:
            #created a sandbox item
            item = await client.create_item(PLUGGY_BANK_CONNECTOR, None, body = PLUGGY_BANK_CREDENTIALS) 

            #fetch the sadbox item 
            fetch_item = await client.fetch_item(item['id']) 

            if fetch_item:
                print("Item retrieved successfully!", fetch_item)

        except Exception as e:
            raise e

async def delete_item():

    async with httpx.AsyncClient() as session:
        client = PluggyClient(Settings.CLIENT_ID, Settings.CLIENT_SECRET, session=session) 

        try:
            #created a sandbox item for example
            item = await client.create_item(PLUGGY_BANK_CONNECTOR, None, body = PLUGGY_BANK_CREDENTIALS) 

            #fetch the sadbox item 
            deleted_item = await client.delete_item(item['id']) 

            if deleted_item:
                print("Item retrieved successfully!", fetch_item)

        except Exception as e:
            raise e

if __name__ == "__main__":
    asyncio.run(retrieve_item())

