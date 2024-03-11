from typing import Dict, Optional
import httpx
from .base_api import BaseApi
from .typing.auth import ConnectTokenOptions
from .typing.connector import ConnectorFilters
from .typing.account import AccountType, Account
from .typing.transaction import TransactionFilters, Transaction
from .typing.common import PageResponse, PageFilters 
from .typing.category import Category
from .typing.item import Parameters, CreateItemOptions, Item
from .typing.opportunity import Opportunity, OpportunityType, OpportunityFilters
from .typing.validation import ValidationResult
from .typing.investment import Investment, InvestmentTransaction, InvestmentType, InvestmentsFilters
from .typing.loans import Loan
from .typing.identity import IdentityResponse 
from .typing.webhook import Webhook, CreateWebhook, UpdateWebhook, WebhookEvent
from .typing.income_report import IncomeReport


class PluggyClient(BaseApi):
    def __init__(self, client_id: str, client_secret: str, session: httpx.AsyncClient, base_url: str = None, api_key: str | None = None):
        super().__init__(client_id, client_secret, session, base_url, api_key) 

    async def fetch_connectors(self, options: ConnectorFilters = {}):
        """"Fetch all available connectors""" 
        return await self.create_get_request('connectors', options) 
    
    async def fetch_connector(self, id:int):
        """Fetch a single connector""" 
        return await self.create_get_request(endpoint=f'connectors/{id}') 
    
    async def create_item(self, connector_id:int, params: Optional[Dict[str,str]], body: Optional[Dict[str,str]], options: Optional[str]=None):
        """Creates an item 
        
        Parameters
        ----------
        * connector_id (int): The Connector's id 
        * parameters: A map of name and value for the needed credentials 
        * options Options available to set to the item 

        Returns
        ------- 
        * Item: a item object
        """

        body = {"parameters":{
        key : value for key, value in body.items() if value is not None
        },
        "connectorId":connector_id} 

        return await self.create_post_request(endpoint='items', params=None, body=body)

    async def fetch_item(self, id:int):
        """Retreives a specific Item by its ID"""
        return await self.create_get_request(f'items/{id}')  
    
    async def validate_parameters(self, id: int, parameters: Parameters) -> ValidationResult: 
        """Check that connector parameters are valid

        Parameters
        ----------
        * id (int): The Connector ID
        * parameters (Parameters): A map of name and value for the credentials to be validated

        Returns
        ------- 
        * ValidationResult: An object with the info of which parameters are wrong
        """
        return await self.create_post_request(f'connectors/{id}/validate', None, parameters)

    async def delete_item(self, id: str):
        """Deletes an Item by its ID""" 
        return await self.create_delete_request(f'items/{id}') 

    async def update_item(self, id: str, parameters: Optional[Dict[str, str]] = None, options: Optional[CreateItemOptions] = None) -> Item:
        """Updates an item

        Parameters
        ----------
        * id (str): The Item ID
        * parameters (Optional[Dict[str, str]]): A map of name and value for the credentials to be updated.
        If none submitted, an Item update will be attempted with the latest used credentials.
        * options (Optional[CreateItemOptions]): Options available to set to the item

        Returns
        ------- 
        * Item: An item object
        """
        return await self.create_patch_request(f'items/{id}', None, {'id': id, 'parameters': parameters, 'options': options})

    async def update_item_mfa(self, id: str, parameters: object):
        """This endpoint receives an object with the MFA parameter name (aka 'token') as key.
        This name is obtained from parameter field in an item in USER_WAITING_INPUT status.

        Parameters
        ----------
        * id (str): Item Id
        """
        return await self.create_post_request(f'items/{id}/mfa', None, parameters)

    async def fetch_accounts(self, item_id: str, type: Optional[AccountType] = None): 
        """Fetch accounts

        Parameters
        ----------
        * item_id (str): The item id
        * type (Optional[AccountType]): Account type

        Returns
        -------
        * PageResponse: Paged response of accounts
        """
        params = {'itemId': item_id, 'type': type}
        return await self.create_get_request(endpoint='accounts', params=params) 

    async def fetch_account(self, id: str) -> Account:
        """Fetch a single account

        Parameters
        ----------
        * id (str): Account Id 

        Returns
        ------- 
        * Account: An account object 
        """
        return await self.create_get_request(endpoint=f'accounts/{id}') 

    async def fetch_transactions(self, account_id: str, options: TransactionFilters = {}) -> PageResponse:
        """Fetch transactions from an account"""  
        return await self.create_get_request(endpoint='transactions', params={**options, 'accountId': account_id})

    async def fetch_all_transactions(self, account_id: str) -> list[Transaction]:
        """Fetch all transactions from an account

        Parameters
        ----------
        * account_id (str): The account id

        Returns
        -------
        * list: An array of transactions
        """
        MAX_PAGE_SIZE = 500
        
        result = await self.fetch_transactions(account_id, options={'pageSize': MAX_PAGE_SIZE})

        if result['totalPages'] == 1:
            return result['results'] 
        
        else: 
            transactions = []
            page = 1

            while page < result['totalPages']: 
                paginated_transaction = await self.fetch_transactions(account_id, options={'page': page})
                transactions.extend(paginated_transaction)
                page += 1

            return transactions 

    async def update_transaction_category(self, id: str, category_id: str) -> Transaction:
        """Post user category for transaction""" 
        return await self.create_patch_request(f'transactions/{id}', None, {'categoryId': category_id})

    async def fetch_transaction(self, id: str) -> Transaction:
        """Fetch a single transaction

        Parameters
        ----------
        * id (str): The transaction Id 

        Returns
        -------
        * Transaction: A Transaction object
        """
        return await self.create_get_request(f'transactions/{id}') 

    async def fetch_investments(self, item_id: str, type: InvestmentType, options: InvestmentsFilters = {}) -> PageResponse:
        """Fetch Investments from an Item 

        Parameters
        ----------
        * item_id (str): The Item Id

        Returns
        -------
        * PageResponse: Paged response of investments
        """
        return await self.create_get_request('investments', {'options': options, 'itemId': item_id, 'type': type})

    async def fetch_investment(self, id: str) -> Investment:
        """Fetch a single investment

        Parameters
        ----------
        * id (str): The investment id

        Returns
        -------
        * Investment: An investment object
        """
        return await self.create_get_request(f'investments/{id}') 

    async def fetch_investment_transactions(self, investment_id: str, options: TransactionFilters = {}) -> PageResponse:
        """Fetch transactions from an investment

        Parameters
        ----------
        * investment_id (str): The investment id
        * options (TransactionFilters): Transaction options to filter

        Returns
        -------
        * PageResponse[List[InvestmentTransaction]]: Object which contains the transactions list and related paging data
        """
        return await self.createGetRequest(f'investments/{investment_id}/transactions', {'options': options, 'investmentId': investment_id})

    async def fetch_opportunities(self, item_id: str, options: OpportunityFilters = {}) -> PageResponse:
        """Fetch opportunities from an Item 

        Parameters
        ----------
        * item_id (str): The Item id
        * options (OpportunityFilters): Request search filters

        Returns
        -------
        * PageResponse: Paged response of opportunities
        """
        return await self.create_get_request('opportunities', {'options': options, 'itemId': item_id}) 

    async def fetch_loans(self, item_id: str, options: PageFilters = {}) -> PageResponse:
        """Fetch loans from an Item

        Parameters
        ----------
        * item_id (str): The Item id
        * options (PageFilters): Request search filters

        Returns
        -------
        * PageResponse: Paged response of loans
        """
        return await self.create_get_request('loans', {'options': options, 'itemId': item_id})

    async def fetch_loan(self, id: str) -> Loan:
        """Fetch loan by id

        Parameters
        ----------
        * id (str): The Loan id

        Returns
        -------
        * Loan: Loan object, if found
        """
        return await self.create_get_request(f'loans/{id}') 

    async def fetch_identity(self, id: str) -> IdentityResponse:
        """Fetch the identity resource

        Returns
        -------
        * IdentityResponse: An identity object
        """
        return await self.create_get_request(f'identity/{id}')

    async def fetch_identity_by_item_id(self, item_id: str) -> IdentityResponse:
        """Fetch the identity resource by its Item ID

        Parameters
        ----------
        * item_id (str): The Item ID

        Returns
        -------
        * IdentityResponse: An identity object
        """
        return await self.create_get_request(f'identity?itemId={item_id}')

    async def fetch_categories(self) -> PageResponse:
        """Fetch all available categories
        
        Returns
        -------
        * PageResponse: A page response of categories
        """
        return await self.create_get_request('categories') 

    async def fetch_category(self, id: str) -> Category:
        """Fetch a single category
        
        Parameters
        ----------
        * id (str): The category ID

        Returns
        -------
        * Category: A category object
        """
        return await self.create_get_request(f'categories/{id}') 

    async def fetch_webhooks(self) -> PageResponse:
        """Fetch all available webhooks 

        Returns
        -------
        * PageResponse[Webhook]: A paging response of webhooks
        """
        return await self.create_get_request('webhooks') 

    async def fetch_webhook(self, id: str) -> Webhook:
        """Fetch a single webhook

        Parameters
        ----------
        * id (str): The webhook ID

        Returns
        -------
        * Webhook: A webhook object
        """
        return await self.create_get_request(f'webhooks/{id}') 

    async def create_webhook(self, event: WebhookEvent, url: str, headers: Optional[Dict[str, str]] = None) -> Webhook:
        """Creates a webhook.
        
        Parameters
        ----------
        * event (WebhookEvent): The event to listen for.
        * url (str): The URL where notifications will be received.
        * headers (Optional[Dict[str, str]], optional): The headers to send with the webhook.
            
        Returns
        -------
        * Webhook: The created webhook object.
        """
        return await self.create_post_request('webhooks', None, {'event': event, 'url': url, 'headers': headers}) 

    async def update_webhook(self, id: str, updated_webhook_params: UpdateWebhook) -> Webhook:
        """Updates a webhook.
        
        Parameters
        ----------
        * id (str): The webhook ID
        * updated_webhook_params (UpdateWebhook): The webhook parameters to update
            
        Returns
        -------
        * Webhook: The updated webhook
        """
        return await self.create_patch_request(f'webhooks/{id}', None, updated_webhook_params)  

    async def delete_webhook(self, id: str) -> None: 
        """Deletes a webhook"""
        return await self.create_delete_request(f'webhooks/{id}') 

    async def fetch_income_reports(self, item_id: str) -> PageResponse:
        """Fetches all income reports for the past years provided by the Financial Institution.

        Parameters
        ----------
        * item_id (str): The Item ID to fetch income reports for. 

        Returns
        -------
        * PageResponse: Paged response of income reports.
        """
        return await self.create_get_request('income-reports', params={'itemId': item_id})

    async def create_connection_token(self, item_id: str, options: Optional[ConnectTokenOptions]) -> str:
        """Creates a connection token that can be used as an API key to connect items from the frontend. 

        Parameters
        ----------
        * item_id (str): The Item ID.
        * options (Optional[ConnectTokenOptions]): Additional options for the connection token.

        Returns
        -------
        * str: Access token to connect items with restricted access
        """
        return await self.create_post_request('connect_token', None, {'itemId': item_id, 'options': options})
