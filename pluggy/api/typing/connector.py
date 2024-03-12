from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

CONNECTOR_TYPES = [
    'PERSONAL_BANK',
    'BUSINESS_BANK',
    'INVOICE',
    'INVESTMENT',
    'TELECOMMUNICATION',
    'DIGITAL_ECONOMY',
    'PAYMENT_ACCOUNT',
    'OTHER',
]

PRODUCT_TYPES = [
    'ACCOUNTS',
    'CREDIT_CARDS',
    'TRANSACTIONS',
    'PAYMENT_DATA',
    'INVESTMENTS',
    'INVESTMENTS_TRANSACTIONS',
    'IDENTITY',
    'BROKERAGE_NOTE',
    'OPPORTUNITIES',
    'PORTFOLIO',
    'INCOME_REPORTS',
    'MOVE_SECURITY',
    'LOANS',
]

CREDENTIAL_TYPES = ['number', 'password', 'text', 'image', 'select']


class ConnectorType(Enum):
    PERSONAL_BANK = 'PERSONAL_BANK'
    BUSINESS_BANK = 'BUSINESS_BANK'
    INVOICE = 'INVOICE'
    INVESTMENT = 'INVESTMENT'
    TELECOMMUNICATION = 'TELECOMMUNICATION'
    DIGITAL_ECONOMY = 'DIGITAL_ECONOMY'
    PAYMENT_ACCOUNT = 'PAYMENT_ACCOUNT'
    OTHER = 'OTHER'


class CredentialType(Enum):
    number = 'number'
    password = 'password'
    text = 'text'
    image = 'image'
    select = 'select'


class ProductType(Enum):
    ACCOUNTS = 'ACCOUNTS'
    CREDIT_CARDS = 'CREDIT_CARDS'
    TRANSACTIONS = 'TRANSACTIONS'
    PAYMENT_DATA = 'PAYMENT_DATA'
    INVESTMENTS = 'INVESTMENTS'
    INVESTMENTS_TRANSACTIONS = 'INVESTMENTS_TRANSACTIONS'
    IDENTITY = 'IDENTITY'
    BROKERAGE_NOTE = 'BROKERAGE_NOTE'
    OPPORTUNITIES = 'OPPORTUNITIES'
    PORTFOLIO = 'PORTFOLIO'
    INCOME_REPORTS = 'INCOME_REPORTS'
    MOVE_SECURITY = 'MOVE_SECURITY'
    LOANS = 'LOANS'


class HealthStatus(Enum):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    UNSTABLE = 'UNSTABLE'


class HealthStage(Enum):
    BETA = 'BETA'
    NULL = None


@dataclass
class CredentialSelectOption:
    value: str
    label: str


@dataclass
class ConnectorCredential:
    # parameter label that describes it
    label: str
    # parameter key name
    name: str
    # type of parameter to create the form
    type: Optional[CredentialType]
    # If parameter is used for MFA.
    mfa: Optional[bool]
    # If parameter is image, base64 string is provided
    data: Optional[str]
    # Assistive information to help the user provide us the credential
    assistiveText: Optional[str]
    # Available options if credential is of type 'select'
    options: Optional[CredentialSelectOption]
    # Regex to validate input
    validation: Optional[str]
    # Error message of input validation on institution language
    validationMessage: Optional[str]
    # Input's placeholder for help
    placeholder: Optional[str]
    # Is this credential optional?
    optional: Optional[bool]
    # Applies to MFA credential only - Detailed information that includes details/hints that the user should be aware of
    instructions: Optional[str]
    # Parameter expiration date, input value should be submitted before this date.
    expiresAt: Optional[datetime]


@dataclass
class ConnectorHealthDetails:
    status: HealthStatus
    stage: Optional[HealthStage]
    details: Optional[str]


@dataclass
class Connector:
    # Primary identifier of the connector
    id: int
    # Financial institution name
    name: str
    # Url of the institution that the connector represents
    institutionUrl: str
    # Image url of the institution.
    imageUrl: str
    # Primary color of the institution
    primaryColor: str
    # Type of the connector
    type: ConnectorType
    # Country of the institution
    country: str
    # List of parameters needed to execute the connector
    credentials: ConnectorCredential
    # Has MFA steps
    hasMFA: bool
    # If true, connector has an Oauth login
    oauth: bool
    # (only for OAuth connector) this URL is used to connect the user and on success it will redirect to create the new item
    oauthUrl: Optional[str]
    # object with information that descirbes current state of the institution connector
    health: ConnectorHealthDetails
    # Indicates that the connector is Open Finance
    isOpenFinance: bool
    # Indicates that the connector is sandbox
    isSandbox: bool
    # Indicates that the connector supports Payment Initiation
    supportsPaymentInitiation: bool
    # Url where user can reset their account password
    resetPasswordUrl: Optional[str]
    # list of products supported by the institution
    products: ProductType
    # Connector creation date
    createdAt: datetime


@dataclass
class ConnectorFilters:
    # Connector´s name or alike name
    name: Optional[str]
    # list of countries to filter available connectors
    countries: Optional[str]
    # list of types to filter available connectors
    types: Optional[ConnectorType]
    # recovers sandbox connectors. Default: false
    sandbox: Optional[bool]
    # filters in (true) or out (false) open finance connectors. Default: undefined
    isOpenFinance: Optional[bool]
    # filters in (true) or out (false) payment initiation connectors. Default: undefined
    supportsPaymentInitiation: Optional[bool]
