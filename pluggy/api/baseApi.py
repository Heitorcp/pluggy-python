import json as Json
import requests
from .config import Config
from typing import Any, Optional, Dict, Union, List
from pluggy.api.protocols.common import PageResponse
import httpx
from typing import TypedDict

QueryParameters = Dict[str, Union[int, List[int], str, List[str], bool]]

class clientParams(TypedDict):
    clientId : str 
    clientsecret: str 
    baseUrl: Optional[str]  

class BaseApi:

    def __init__(self, clientId: str, clientSecret: str, session:httpx.AsyncClient, baseUrl: str = None, apiKey:Optional[str] = None):
        
        #Initializes the Client Session for Async Requests 
        self.session = session

        # Validate clientId and clientSecret
        if not clientId or not clientSecret:
            raise ValueError("Missing authorization for API communication")

        # Set baseUrl to PLUGGY_API_URL if not provided
        self.baseUrl = Config.PLUGGY_API_URL

        # Set other attributes
        self.apiKey = apiKey
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.defaultHeaders = {
                "accept":"application/json",
                "content-type":"application/json"
            }

    def maptoQueryString(self, params:Dict[str, object]) -> str:
        if not params:
            return '' 
        
        query = '&'.join([f"{key}={params[key]}" for key in params if params[key] is not None]) 
        return f"?{query}" if query else ''

    async def getApiKey(self) -> str:

        if self.apiKey is not None:
            return self.apiKey
        
        json = {
            "clientId": self.clientId,
            "clientSecret": self.clientSecret
        }

        url = f"{self.baseUrl}/auth"

        try:
            response = await self.session.post(url, json=json, headers=self.defaultHeaders)
            if response.status_code == 200:
                self.apiKey = Json.loads(response.text)["apiKey"] 
                return self.apiKey
        except BaseException as e:
            raise e
        
    async def createGetRequest(self, endpoint:str, params:Optional[QueryParameters]=None) -> PageResponse:

        try:
            apiKey = await self.getApiKey()
            url = f"{self.baseUrl}/{endpoint}"

            if params:
                url = f"{self.baseUrl}/{endpoint}/{self.maptoQueryString(params)}"

            response = await self.session.get(url, headers={
                **self.defaultHeaders,
                'X-API-KEY':apiKey
            })
            response.raise_for_status() 

            return response.json()
                
        except httpx.HTTPError as error:
            print(f"[Pluggy SDK] HTTP request failed: {error.response.text}")
            raise error 
        except Exception as error:
            print(f"[Pluggy SDK] Error: {error}")
            raise error
        
    async def createPostRequest(self, endpoint:str, params:Optional[QueryParameters], body:Optional[Dict[str, object]]):
        return  await self.createMutationRequest(endpoint=endpoint, params=params, body=body, method='POST')

    async def createPutRequest(self, endpoint:str, params:Optional[QueryParameters], body:Optional[Dict[str, object]]):
        return  await self.createMutationRequest(endpoint, params, body, method='PUT')

    async def createPatchRequest(self, endpoint:str, params:Optional[QueryParameters]=None, body:Optional[Dict[str, object]]=None):
        return  await self.createMutationRequest('PATCH', endpoint, params, body)

    async def createDeleteRequest(self, endpoint:str, params:Optional[QueryParameters] = None, body:Optional[Dict[str, object]] = None):
        return  await self.createMutationRequest('DELETE',endpoint, params, body)

    async def createMutationRequest(self, method:str, endpoint:str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Any:
        apiKey = await self.getApiKey()
        url = f"{self.baseUrl}/{endpoint}{self.maptoQueryString(params)}"

        try:
            if body:
                body = {key: value for key, value in body.items() if value is not None}

                response = await self.session.request(method, url, headers={
                    **self.defaultHeaders,
                    'X-API-KEY': apiKey
                }, json=body)

                response.raise_for_status()

                return response.json()
            
        except requests.HTTPError as error:
            print(f"[Pluggy SDK] HTTP request failed: {error.response.text}")
            raise error
        except Exception as error:
            print(f"[Pluggy SDK] Error: {error}")
            raise error