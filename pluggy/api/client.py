from typing import Dict, Optional
import httpx
from .baseApi import BaseApi
from .protocols.auth import ConnectTokenOptions
from .protocols.connector import ConnectorFilters
from .protocols.account import AccountType, Account
from .protocols.transaction import TransactionFilters, Transaction
from .protocols.common import PageResponse, PageFilters 
from .protocols.category import Category
from .protocols.item import Parameters, CreateItemOptions, Item
from .protocols.opportunity import Opportunity, OpportunityType, OpportunityFilters
from .protocols.validation import ValidationResult
from .protocols.investment import Investment, InvestmentTransaction, InvestmentType, InvestmentsFilters
from .protocols.loans import Loan
from .protocols.identity import IdentityResponse 
from .protocols.webhook import Webhook, CreateWebhook, UpdateWebhook, WebhookEvent
from .protocols.income_report import IncomeReport


class PluggyClient(BaseApi):
    def __init__(self, clientId: str, clientSecret: str, session: httpx.AsyncClient, baseUrl: str = None, apiKey: str | None = None):
        super().__init__(clientId, clientSecret, session, baseUrl, apiKey) 

    async def fetchConnectors(self, options:ConnectorFilters = {}):
        """"Fetch all available connectors""" 
        return await self.createGetRequest('connectors', options) 
    
    async def fetchConnector(self, id:int):
        """Fetch a single connector""" 
        return await self.createGetRequest(endpoint=f'connectors/{id}') 
    
    async def createItem(self, connectorId:int, params: Optional[Dict[str,str]], body:Optional[Dict[str,str]], options: Optional[str]=None):
            
        body = {"parameters":{
        key : value for key, value in body.items() if value is not None
        },
        "connectorId":connectorId} 

        return await self.createPostRequest(endpoint='items', params=None, body=body)

    async def fetchItem(self, id:int):
        """Retreives a specific Item by its ID"""
        return await self.createGetRequest(f'items/{id}')  
    
    async def validateParameters(self, id:int, parameters: Parameters) -> ValidationResult: 
        """
        Check that connector parameters are valid
        
        :param str id: The Connector ID
        :param dict parameters: A dictionary of name and value for the credentials to be validated
        :return: an object with the info of which parameters are wrong
        :rtype: ValidationResult
        """
        return await self.createPostRequest(f'connectors/{id}/validate', None, parameters)
    
    ###TEST HERE
    async def deleteItem(self, id:str):
        """Deletes an Item by its ID""" 
        return await self.createDeleteRequest(f'items/{id}') 

    ###TEST HERE
    async def updateItem(self, id:str, parameters:Optional[Dict[str, str]]=None, options: Optional[CreateItemOptions]=None) -> Item:
        """
        Updates an item

        Parameters
        ----------
        id -- The Item ID
        parameters (Optional) -- A map of name and value for the credentials to be updated.
        if none submitted, an Item update will be attempted with the latest used credentials.
        
        Returns
        ------- 
        Item: an item object
        """
        return await self.createPatchRequest(f'items/{id}', None, {'id':id, 'parameters':parameters, 'options': options})
    
    async def updateItemMFA(self, id:str, parameters:object):
        """
        This endpoint receives an object with the MFA parameter name (aka 'token') as key.
        This name is obtained from parameter field in an item in USER_WAITING_INPUT status. 

        Args:
            - id (str) : item Id
        """
        return await self.createPostRequest(f'items/{id}/mfa', None, parameters)

    async def fetchAccounts(self, itemId:str, type:Optional[AccountType]=None): 
        params = {'itemId':itemId, 'type':type}
        return await self.createGetRequest(endpoint='accounts', params=params) 
    
    async def fetchAccount(self, id:str) -> Account:
        """
        Fetch a single account
        
        Args:
            - id(str) : Account Id 

        Returns
        ------- 
        Account: An account object 
        """
        return await self.createGetRequest(endpoint=f'accounts/{id}') 
    
    async def fetchTransactions(self, accountId:str, options:TransactionFilters = {}) -> PageResponse:
        """Fetch transactions from an account"""  
        return await self.createGetRequest(endpoint='transactions', params={**options, 'accountId':accountId})

    async def fetchAllTransactions(self, accountId:str) -> list[Transaction]:
        """
        Fetch all transactions from an account

        Parameters
        ----------
        account_id(str): The account id

        Returns
        -------
        List : An array of transactions
        """

        MAX_PAGE_SIZE = 500
        
        result = await self.fetchTransactions(accountId, options={'pageSize': MAX_PAGE_SIZE})

        if result['totalPages'] == 1:
            return result['results'] 
        
        else: 
            transactions = []

            page = 1

            while page < result['totalPages']: 

                paginatedTransaction = await self.fetchTransactions(accountId, options={'page': page})

                print(paginatedTransaction['results'])

                transactions.extend(paginatedTransaction)

                page+=1

            return transactions 

    async def updateTransactionCategory(self, id:str, categoryId:str) -> Transaction:
        """Post user category for transaction""" 
        return await self.createPatchRequest(f'transactions/{id}', None, {'categoryId':categoryId})
 
    async def fetchTransaction(self, id:str) -> Transaction:
        """
        Fetch a single transaction
        
        Parameters
        ----------
        id : The transaction Id 

        Returns
        -------
        Transaction: a Transaction object
        """
        return await self.createGetRequest(f'transactions/{id}') 

    async def fetchInvestments(self, item_id:str, type:InvestmentType, options:InvestmentsFilters = {}) -> PageResponse:
        """
        Fetch Investments from an Item 

        Parameters
        ----------
        item_id: the Item Id

        Returns
        -------
        PageResponse(Investment): paged response of investments
        """

        return await self.createGetRequest('investments', {'options': options, 'itemId':item_id, 'type':type})

    async def fetchInvestment(self, id:str) -> Investment:
        """
        Fetch a single investment

        Parameters
        ----------
        id: the investment id

        Returns
        -------
        Investment: an investment object
        """
        return await self.createGetRequest(f'investments/{id}') 
    
    async def fetchInvestmentTransactions(self, investment_id:str, options:TransactionFilters = {}) -> PageResponse:

        """
        Fetch transactions from an investment

        Parameters
        ----------
        investment_id: the investment id
        options[TransactionsFilters]: Transaction options to filter

        Returns
        -------
        PageResponse[List[InvestmentTransaction]] object which contains the transactions list and related paging data
        """

        return await self.createGetRequest(f'investments/{investment_id}/transactions', {
            'options':options, 'investmentId':investment_id
        })
    
    async def fetchOpportunities(self, item_id:str, options: OpportunityFilters = {}) -> PageResponse:
        """
        Fetch opportunities from an Item 

        Parameters
        ----------
        item_id: the Item id
        options: request search filters

        Returns
        -------
        PageResponse paged response of opportunities
        """
        return await self.createGetRequest('oportunities', {'options':options, 'itemId':item_id}) 

    async def fetchLoans(self, item_id:str, options: PageFilters = {}) -> PageResponse:
        """
        Fetch loans from an Item

        Parameters
        ----------
        item_id: the Item id
        options: request search filters

        Returns
        -------
        PageResponse: paged response of loans
        """

        return await self.createGetRequest('loans', {'options':options, 'itemId':item_id})
    
    async def fetchLoan(self, id:str) -> Loan:
        """
        Fetch loan by id

        Parameters
        ----------
        id: the Loan id

        Returns
        -------
        Loan - loan object, if found
        """
        return await self.createGetRequest(f'loans/{id}') 
    
    async def fetchIdentity(self, id:str) -> IdentityResponse:
        """
        Fetch the identity resource

        Returns
        -------
        IdentityResponse - an identity object
        """
        return await self.createGetRequest(f'identity/{id}')
    
    async def fetchIdentityByItemId(self, item_id:str) -> IdentityResponse:
        """
        Fetch the identity resource by it's Item ID

        Returns
        -------
        IdentityResponse - an identity object
        """
        return await self.createGetRequest(f'identity?itemId={item_id}')

    async def fetchCategories(self) -> PageResponse:
        """Fetch all available categories
        
        Returns
        -------
        Category - a page response of categories
        """
        return await self.createGetRequest('categories') 
    
    async def fetchCategory(self, id:str) -> Category:
        """Fetch a simgle category
        
        Parameters
        ----------
        id: the category id

        Returns
        -------
        Category - a category object
        """
        return await self.createGetRequest(f'categories/{id}') 
    
    async def fetchWebhooks(self) -> PageResponse:
        """ 
        Fetch all available webhooks 

        Returns
        -------
        PageResponse[Webhook] - a paging response of a webhook
        """
        return await self.createGetRequest('webhooks') 
    
    async def fetchWebhook(self, id:str) -> Webhook:
        """ 
        Fetch a single webhook

        Returns
        -------
        Webhook - a webhook object
        """
        return await self.createGetRequest(f'webhooks/{id}') 
    
    async def createWebHook(self, event:WebhookEvent, url: str, headers:Optional[Dict[str, str]] = None) -> Webhook:
        """
        Creates a Webhook.
        
        Args:
            webhook_params (dict): The webhook parameters to create, including:
                - url (str): The URL where notifications will be received.
                - event (str): The event to listen for.
                - headers (Optional[dict], optional): The headers to send with the webhook.
                
        Returns:
            Webhook: The created webhook object.
        """
        return await self.createPostRequest('webhooks', None, {'event':event, 'url':url, 'headers':headers}) 
    
    async def update_webhook(self, id:str, updated_webhook_params: UpdateWebhook) -> Webhook:
        """
        Updates a Webhook.
        
        Args:
            - id (str): The Webhook ID
            - updatedWebhookParams - The webhook params to update
            
        Returns:
            Webhook: The webhook updated
        """
        return await self.createPatchRequest(f'webhooks/{id}', None, updated_webhook_params)  
    
    async def delete_webhook(self, id:str) -> None: 
        """
        Deletes a Webhook
        """
        return await self.createDeleteRequest(f'webhooks/{id}') 
    
    async def fetch_income_reports(self, item_id:str) -> PageResponse:
        """
        Fetches all income reports for the past years provided by the Financial Institution.

        Args:
            - item_id (str): The Item ID to fetch income reports for. 
        Returns:
            - PageResponse: Paged response of income reports.
        """
        return await self.createGetRequest('income-reports', params={'itemId':item_id})

    async def create_connection_token(self, item_id:str, options: Optional[ConnectTokenOptions]) -> str:
        """
        Creates a connect token that can be used as API KEY to connect items from the Frontend. 

        Returns
        -------
        (str) - Access token to connect items with restrict access
        """
        return await self.createPostRequest('connect_token', None, {'itemId':item_id, 'options':options})