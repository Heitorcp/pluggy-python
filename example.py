import asyncio
import json
import os

import httpx
from dotenv import load_dotenv

from pypluggy.api.base_api import BaseApi
from pypluggy.api.client import PluggyClient

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
async def create_webhook(session=None):
    client = PluggyClient(CLIENT_ID, CLIENT_SECRET, session=session)

    await client.create_webhook()
