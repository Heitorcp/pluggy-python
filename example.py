from pluggy.api.client import PluggyClient 
from pluggy.api.baseApi import BaseApi
import asyncio
import httpx
import os 
import json
from dotenv import load_dotenv

load_dotenv() 

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

from functools import wraps

def inject_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with httpx.AsyncClient() as session:
            kwargs['session'] = session
            return await func(*args, **kwargs)
    return wrapper

@inject_session
async def get_api_key(session=None):
    base_api = BaseApi(CLIENT_ID, CLIENT_SECRET, session=session) 
    api_key = await base_api.getApiKey() 
    print(api_key)

async def fetch_connectors(export_to_json:bool = False):
    """
    Example script fetching Pluggy's Connectors
    """
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
        connectors = await client.fetchConnectors()

        if export_to_json:
            json_str = json.dumps(connectors, indent=4) 

            with open('connectors.json', 'w') as json_file:
                json_file.write(json_str)

        print(connectors) 

async def fetch_connector(connector_id:int):
    """
    Example script fetching Pluggy's Connector by Id
    """
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
        connector = await client.fetchConnector(id=connector_id) 
        print(connector)

async def fetch_categories(export_to_json:bool=False):
    """
    Example script fetching Pluggy's Categories
    """
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        categories =  await client.fetchCategories()

        if export_to_json:
            json_str = json.dumps(categories, indent=4) 

            with open('categories.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json_str)

        print(categories)  

async def create_item():
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
        
        body = {
            "cpf":"1234567890",
            "password":"12345"
        }

        item = await client.createItem(212, None, body=body)  

async def retrieve_item(item_id:str):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 

        item = await client.fetchItem(id=item_id)  

        print(item)

async def validate_parameters(connector_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 

        parameters =  {
            "cpf":"1234567890",
            "password":123478
        } 

        result = await client.validateParameters(connector_id, parameters=parameters) 

        print(result) 

async def delete_item(item_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 

        return await client.deleteItem(item_id)  
    
async def update_item(item_id):
    try:
        async with httpx.AsyncClient() as session:
            client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
            await client.updateItem(item_id)
    except Exception as e:
        raise e

@inject_session
async def retrieve_all_transactions(account_id, export_to_json:bool = True, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    txs = await client.fetchAllTransactions(account_id) 
    print(txs) 

    if export_to_json:
        with open('transactions.json', 'w') as json_file:
            json_str = json.dumps(txs, indent=4) 
            json_file.write(json_str)  

async def retrieve_accounts(item_id): 
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        accounts = await client.fetchAccounts(itemId=item_id, type='CREDIT') 
        print(accounts) 

async def retrieve_account(account_id:str):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
        account = await client.fetchAccount(account_id) 
        print(account) 

@inject_session
async def fetch_transactions(account_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    txs = await client.fetchTransactions(account_id) 
    print(txs)

@inject_session
async def fetch_transaction(tx_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    tx = await client.fetchTransaction(tx_id) 
    print(tx)

@inject_session
async def fetch_all_transactions(account_id, session=None, export_to_json:bool=False):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    txs = await client.fetchAllTransactions(account_id) 
    print(txs) 
    if export_to_json:
        json_str = json.dumps(txs, indent=4) 
        with open('transactions.json', 'w', encoding='utf-8') as f:
            f.write(json_str) 
    return

@inject_session
async def update_txs_category(tx_id, category_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    try:
        await client.updateTransactionCategory(tx_id, category_id) 
    except BaseException as e:
        print(f"An Exception occured {e}")
        raise e

@inject_session 
async def fetch_opportunities(item_id:str, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    options = {'page':1, 'pageSize':20}

    opportunities = await client.fetchOpportunities(item_id, options) 
    print(opportunities) 

@inject_session
async def fetch_loans(item_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 
    loans = await client.fetchLoans(item_id) 
    print(loans)  

@inject_session 
async def retrieve_identity(item_id: str, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    identity = await client.fetchIdentityByItemId(item_id) 
    print(identity)  

@inject_session
async def retrieve_income_reports(item_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session) 

    report = await client.fetch_income_reports(item_id) 

    print(report)

if __name__ == "__main__":
    asyncio.run(fetch_connectors())