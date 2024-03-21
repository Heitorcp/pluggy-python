import asyncio
import json
import os

import httpx
from dotenv import load_dotenv

from pypluggy.api.base_api import BaseApi
from pypluggy.api.client import PluggyClient

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

from functools import wraps


def inject_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with httpx.AsyncClient() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper


@inject_session
async def get_api_key(session=None):
    base_api = BaseApi(CLIENT_ID, CLIENT_SECRET, session=session)
    api_key = await base_api.get_api_key()
    print(api_key)


async def fetch_connector(connector_id: int):

    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        connector = await client.fetch_connector(id=connector_id)
        print(connector)


async def fetch_categories(export_to_json: bool = False):

    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        categories = await client.fetch_categories()

        if export_to_json:
            json_str = json.dumps(categories, indent=4)

            with open("categories.json", "w", encoding="utf-8") as json_file:
                json_file.write(json_str)

        print(categories)


async def create_item():
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

        body = {"cpf": "1234567890", "password": "12345"}

        item = await client.create_item(212, None, body=body)


async def retrieve_item(item_id: str):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

        item = await client.fetch_item(id=item_id)

        print(item)


async def validate_parameters(connector_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

        parameters = {"cpf": "1234567890", "password": 123478}

        result = await client.validate_parameters(connector_id, parameters=parameters)

        print(result)


async def delete_item(item_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

        return await client.delete_item(item_id)


async def update_item(item_id):
    try:
        async with httpx.AsyncClient() as session:
            client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
            await client.update_item(item_id)
    except Exception as e:
        raise e


@inject_session
async def retrieve_all_transactions(account_id, export_to_json: bool = True, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    txs = await client.fetch_all_transactions(account_id)
    print(txs)

    if export_to_json:
        with open("transactions.json", "w") as json_file:
            json_str = json.dumps(txs, indent=4)
            json_file.write(json_str)


async def retrieve_accounts(item_id):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        accounts = await client.fetch_accounts(itemId=item_id, type="CREDIT")
        print(accounts)


async def retrieve_account(account_id: str):
    async with httpx.AsyncClient() as session:
        client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
        account = await client.fetch_account(account_id)
        print(account)


@inject_session
async def fetch_transactions(account_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    txs = await client.fetch_transactions(account_id)
    print(txs)


@inject_session
async def fetch_transaction(tx_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    tx = await client.fetch_transaction(tx_id)
    print(tx)


@inject_session
async def fetch_all_transactions(account_id, session=None, export_to_json: bool = False):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    txs = await client.fetch_all_transactions(account_id)
    print(txs)
    if export_to_json:
        json_str = json.dumps(txs, indent=4)
        with open("transactions.json", "w", encoding="utf-8") as f:
            f.write(json_str)
    return


@inject_session
async def update_txs_category(tx_id, category_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    try:
        await client.update_transaction_category(tx_id, category_id)
    except BaseException as e:
        print(f"An Exception occured {e}")
        raise e


@inject_session
async def fetch_opportunities(item_id: str, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    options = {"page": 1, "pageSize": 20}

    opportunities = await client.fetch_opportunities(item_id, options)
    print(opportunities)


@inject_session
async def fetch_loans(item_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)
    loans = await client.fetch_loans(item_id)
    print(loans)


@inject_session
async def retrieve_identity(item_id: str, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    identity = await client.fetch_identity_by_item_id(item_id)
    print(identity)


@inject_session
async def retrieve_income_reports(item_id, session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    report = await client.fetch_income_reports(item_id)

    print(report)


@inject_session
async def create_webhook(session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    await client.create_webhook()


if __name__ == "__main__":
    asyncio.run(fetch_connectors())
