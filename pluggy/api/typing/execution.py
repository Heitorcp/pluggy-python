from enum import auto, Enum
from dataclasses import dataclass
from typing import Dict, Optional, Literal

TriggeredBy = Literal['CLIENT' , 'USER' , 'SYNC' , 'INTERNAL'] 

CONNECTOR_EXECUTION_STATUSES = [
  'LOGIN_IN_PROGRESS',
  'WAITING_USER_INPUT',
  'WAITING_USER_ACTION',
  'LOGIN_MFA_IN_PROGRESS',
  'ACCOUNTS_IN_PROGRESS',
  'TRANSACTIONS_IN_PROGRESS',
  'PAYMENT_DATA_IN_PROGRESS',
  'CREDITCARDS_IN_PROGRESS',
  'INVESTMENTS_IN_PROGRESS',
  'INVESTMENTS_TRANSACTIONS_IN_PROGRESS',
  'OPPORTUNITIES_IN_PROGRESS',
  'IDENTITY_IN_PROGRESS',
  'PORTFOLIO_IN_PROGRESS',
  'INCOME_REPORTS_IN_PROGRESS',
  'LOANS_IN_PROGRESS',
] 

class ConnectorExecutionStatus(Enum):
    LOGIN_IN_PROGRESS = auto()
    WAITING_USER_INPUT = auto()
    WAITING_USER_ACTION = auto()
    LOGIN_MFA_IN_PROGRESS = auto()
    ACCOUNTS_IN_PROGRESS = auto()
    TRANSACTIONS_IN_PROGRESS = auto()
    PAYMENT_DATA_IN_PROGRESS = auto()
    CREDITCARDS_IN_PROGRESS = auto()
    INVESTMENTS_IN_PROGRESS = auto()
    INVESTMENTS_TRANSACTIONS_IN_PROGRESS = auto()
    OPPORTUNITIES_IN_PROGRESS = auto()
    IDENTITY_IN_PROGRESS = auto()
    PORTFOLIO_IN_PROGRESS = auto()
    INCOME_REPORTS_IN_PROGRESS = auto()
    LOANS_IN_PROGRESS = auto() 

EXECUTION_ERROR_CODES = [
  'INVALID_CREDENTIALS',
  'ALREADY_LOGGED_IN',
  'UNEXPECTED_ERROR',
  'INVALID_CREDENTIALS_MFA',
  'SITE_NOT_AVAILABLE',
  'ACCOUNT_LOCKED',
  'ACCOUNT_CREDENTIALS_RESET',
  'CONNECTION_ERROR',
  'ACCOUNT_NEEDS_ACTION',
  'USER_AUTHORIZATION_PENDING',
  'USER_AUTHORIZATION_NOT_GRANTED',
  'USER_NOT_SUPPORTED',
  'USER_INPUT_TIMEOUT',
]

class ExecutionErrorCode(Enum):
    INVALID_CREDENTIALS = auto()
    ALREADY_LOGGED_IN = auto()
    UNEXPECTED_ERROR = auto()
    INVALID_CREDENTIALS_MFA = auto()
    SITE_NOT_AVAILABLE = auto()
    ACCOUNT_LOCKED = auto()
    ACCOUNT_CREDENTIALS_RESET = auto()
    CONNECTION_ERROR = auto()
    ACCOUNT_NEEDS_ACTION = auto()
    USER_AUTHORIZATION_PENDING = auto()
    USER_AUTHORIZATION_NOT_GRANTED = auto()
    USER_NOT_SUPPORTED = auto()
    USER_INPUT_TIMEOUT = auto()

EXECUTION_FINISHED_STATUSES = EXECUTION_ERROR_CODES + ['MERGE_ERROR','ERROR','SUCCESS','PARTIAL_SUCCESS']

class ExecutionFinishedStatus(Enum):
    INVALID_CREDENTIALS = auto()
    ALREADY_LOGGED_IN = auto()
    UNEXPECTED_ERROR = auto()
    INVALID_CREDENTIALS_MFA = auto()
    SITE_NOT_AVAILABLE = auto()
    ACCOUNT_LOCKED = auto()
    ACCOUNT_CREDENTIALS_RESET = auto()
    CONNECTION_ERROR = auto()
    ACCOUNT_NEEDS_ACTION = auto()
    USER_AUTHORIZATION_PENDING = auto()
    USER_AUTHORIZATION_NOT_GRANTED = auto()
    USER_NOT_SUPPORTED = auto()
    USER_INPUT_TIMEOUT = auto()
    MERGE_ERROR = auto()
    ERROR = auto()
    SUCCESS = auto()
    PARTIAL_SUCCESS = auto()


EXECUTION_STATUSES = [
    'CREATING',
    'CREATE_ERROR',
    'CREATED'] + CONNECTOR_EXECUTION_STATUSES + EXECUTION_FINISHED_STATUSES

class ExecutionStatus(Enum):
    CREATING = auto()
    CREATE_ERROR = auto()
    CREATED = auto()
    LOGIN_IN_PROGRESS = auto()
    WAITING_USER_INPUT = auto()
    WAITING_USER_ACTION = auto()
    LOGIN_MFA_IN_PROGRESS = auto()
    ACCOUNTS_IN_PROGRESS = auto()
    TRANSACTIONS_IN_PROGRESS = auto()
    PAYMENT_DATA_IN_PROGRESS = auto()
    CREDITCARDS_IN_PROGRESS = auto()
    INVESTMENTS_IN_PROGRESS = auto()
    INVESTMENTS_TRANSACTIONS_IN_PROGRESS = auto()
    OPPORTUNITIES_IN_PROGRESS = auto()
    IDENTITY_IN_PROGRESS = auto()
    PORTFOLIO_IN_PROGRESS = auto()
    INCOME_REPORTS_IN_PROGRESS = auto()
    LOANS_IN_PROGRESS = auto()
    INVALID_CREDENTIALS = auto()
    ALREADY_LOGGED_IN = auto()
    UNEXPECTED_ERROR = auto()
    INVALID_CREDENTIALS_MFA = auto()
    SITE_NOT_AVAILABLE = auto()
    ACCOUNT_LOCKED = auto()
    ACCOUNT_CREDENTIALS_RESET = auto()
    CONNECTION_ERROR = auto()
    ACCOUNT_NEEDS_ACTION = auto()
    USER_AUTHORIZATION_PENDING = auto()
    USER_AUTHORIZATION_NOT_GRANTED = auto()
    USER_NOT_SUPPORTED = auto()
    USER_INPUT_TIMEOUT = auto()
    MERGE_ERROR = auto()
    ERROR = auto()
    SUCCESS = auto()
    PARTIAL_SUCCESS = auto() 


@dataclass
class ExecutionErrorResult:
    # The specific execution error code 
    code: ExecutionErrorCode
    # A human-readable, short description of the error 
    message: str
    # The exact error message returned by the institution, if any was provided. 
    providerMessage: Optional[str]
    # Unstructured properties that provide additional context/information of the error.
    # Used for some specific cases only, such as Caixa PF & PJ.
    # @see https://docs.pluggy.ai/docs/errors-validations for more info. 
    attributes: Optional[Dict[str,str]]