import json as json
from typing import Any, Optional, TypedDict, Union

import httpx
import requests

from pypluggy.api.type.common import PageResponse

from .config import Config

QueryParameters = dict[str, Union[int, list[int], str, list[str], bool]]


class ClientParams(TypedDict):
    client_id: str
    client_secret: str
    base_url: Optional[str]


class BaseApi:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: httpx.AsyncClient,
        base_url: str = None,
        api_key: Optional[str] = None,
    ):

        # Initializes the Client Session for Async Requests
        self.session = session

        # Validate client_id and client_secret
        if not client_id or not client_secret:
            raise ValueError("Missing authorization for API communication")

        # Set base_url to PLUGGY_API_URL if not provided
        self.base_url = Config.PLUGGY_API_URL

        # Set other attributes
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.default_headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def map_to_query_string(self, params: dict[str, QueryParameters]) -> str:
        if not params:
            return ""

        query = "&".join([f"{key}={params[key]}" for key in params if params[key] is not None])
        return f"?{query}" if query else ""

    async def get_api_key(self) -> str:

        if self.api_key is not None:
            return self.api_key

        json_data = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }

        url = f"{self.base_url}/auth"

        try:
            response = await self.session.post(url, json=json_data, headers=self.default_headers)
            if response.status_code == 200:
                self.api_key = json.loads(response.text)["apiKey"]
                return self.api_key
        except BaseException as e:
            raise e

    async def create_get_request(
        self, endpoint: str, params: Optional[QueryParameters] = None
    ) -> PageResponse:

        try:
            api_key = await self.get_api_key()
            url = f"{self.base_url}/{endpoint}"

            if params:
                url = f"{self.base_url}/{endpoint}/{self.map_to_query_string(params)}"

            response = await self.session.get(url, headers={**self.default_headers, "X-API-KEY": api_key})
            response.raise_for_status()

            return response.json()

        except httpx.HTTPError as error:
            print(f"[Pluggy SDK] HTTP request failed: {error}")
            raise error
        except Exception as error:
            print(f"[Pluggy SDK] Error: {error}")
            raise error

    async def create_post_request(
        self,
        endpoint: str,
        params: Optional[QueryParameters],
        body: Optional[dict[str, object]],
    ):
        return await self.create_mutation_request(endpoint=endpoint, params=params, body=body, method="POST")

    async def create_put_request(
        self,
        endpoint: str,
        params: Optional[QueryParameters],
        body: Optional[dict[str, object]],
    ):
        return await self.create_mutation_request("PUT", endpoint, params, body)

    async def create_patch_request(
        self,
        endpoint: str,
        params: Optional[QueryParameters] = None,
        body: Optional[dict[str, object]] = None,
    ):
        return await self.create_mutation_request("PATCH", endpoint, params, body)

    async def create_delete_request(
        self,
        endpoint: str,
        params: Optional[QueryParameters] = None,
        body: Optional[dict[str, object]] = None,
    ):
        return await self.create_mutation_request("DELETE", endpoint, params, body)

    async def create_mutation_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        body: Optional[dict[str, Any]] = None,
    ) -> Any:
        api_key = await self.get_api_key()
        url = f"{self.base_url}/{endpoint}{self.map_to_query_string(params)}"

        try:
            if body:
                body = {key: value for key, value in body.items() if value is not None}

                response = await self.session.request(
                    method,
                    url,
                    headers={**self.default_headers, "X-API-KEY": api_key},
                    json=body,
                )

                response.raise_for_status()

                return response.json()

        except requests.HTTPError as error:
            print(f"[Pluggy SDK] HTTP request failed: {error.response.text}")
            raise error
        except Exception as error:
            print(f"[Pluggy SDK] Error: {error}")
            raise error
