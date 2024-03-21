from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pypluggy.api.type.common import CurrencyCode

ACCOUNT_TYPES = ['BANK', 'CREDIT']


class AccountType(Enum):
    BANK = 'BANK'
    CREDIT = 'CREDIT'


ACCOUNT_SUBTYPES = ['SAVINGS_ACCOUNT', 'CHECKING_ACCOUNT', 'CREDIT_CARD']


class AccountSubtype(Enum):
    SAVINGS_ACCOUNT = 'SAVINGS_ACCOUNT'
    CHECKING_ACCOUNT = 'CHECKING_ACCOUNT'
    CREDIT_CARD = 'CREDIT_CARD'


@dataclass
class BankData:
    # primary identifier of the account to make bank transfers
    transferNumber: str | None
    # available balance of the account
    closingBalance: float | None
    # Automatically invested balance
    automaticallyInvestedBalance: float | None


@dataclass
class CreditData:
    # Credit card end user's level
    level: str | None
    # Credit card brand, ie. Mastercard, Visa
    brand: str | None
    # Current balance close date
    balanceCloseDate: datetime | None
    # Current balance due date
    balanceDueDate: datetime | None
    # Available credit limit to use.
    availableCreditLimit: float | None
    # Current balance in foreign currency
    balanceForeignCurrency: float | None
    # Current balance minimum payment due
    minimumPayment: float | None
    # Maximum credit card limit.
    creditLimit: float | None


@dataclass
class Account:
    # Primary identifier of the account
    id: str
    # Primary identifier of the Item
    itemId: str
    # Type of the account
    type: AccountType
    # Sub type of the account
    subtype: AccountSubtype
    # Account's financial institution number
    number: str
    # Current balance of the account
    balance: float
    # Account's name or description
    name: str
    # Account's name provided by the institution based on the level of client.
    marketingName: str | None
    # Account's owner´s fullname
    owner: str | None
    # Account's owner´s tax number
    taxNumber: str | None
    # ISO Currency code of the account's amounts
    currencyCode: CurrencyCode
    # Account related bank data, when account is BANK type
    bankData: BankData | None
    # Account related credit data, when account is CREDIT type
    creditData: CreditData | None
