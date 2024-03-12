from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, TypedDict

from pluggy.api.typing.common import CurrencyCode, PageFilters

"""
  TYPE: TransactionType
 * The direction of the transaction.
 * If DEBIT money going out of the account.
 * If CREDIT money going into the account.

"""
TRANSACTION_TYPES = ['DEBIT', 'CREDIT']

TransactionType = Literal['DEBIT', 'CREDIT']


class TransactionStatus(Enum):
    PENDING = 'PENDING'
    POSTED = 'POSTED'


DOCUMENT_TYPES = ['CPF', 'CNPJ']


class DocumentTypes(Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'


@dataclass
class TransactionPaymentParticipantDocument:
    # document number
    value: str
    # Type of document provided, ie. CPF / CNPJ
    type: Optional[DocumentTypes]


@dataclass
class TransactionPaymentParticipant:
    # Document number object
    documentNumber: Optional[TransactionPaymentParticipantDocument]
    # Name of the participant
    name: Optional[str]
    # Number of the account
    accountNumber: Optional[str]
    # Number of the agency / branch
    branchNumber: Optional[str]
    # Number of the bank
    routingNumber: Optional[str]


@dataclass
class TransactionPaymentData:
    # The identity of the sender of the transfer */
    payer: Optional[TransactionPaymentParticipant]
    # The identity of the receiver of the transfer */
    receiver: Optional[TransactionPaymentParticipant]
    # String submitted by the receiver associated with the payment when generating the payment request.
    # * i.e., When generating a Pix QR code, the receiver creates the request using their internal reference identifier.
    # * This way, when the payment is done, they can map the payment to their internal reference.
    receiverReferenceId: Optional[str]
    # Identifier for the transaction provided by the institution */
    paymentMethod: Optional[str]
    # The type of transfer used "PIX", "TED", "DOC". */
    referenceNumber: Optional[str]
    # The payer description / motive of the transfer */
    reason: Optional[str]


@dataclass
class TransactionMerchantData:
    # Name of the merchant
    name: str
    # Legal business name of the merchant
    businessName: str
    # Cnpj number associated to the merchant
    cnpj: str
    # Cnae number associated to the merchant
    cnae: Optional[str]
    # Category of the merchant
    category: Optional[str]


@dataclass
class CreditCardMetadata:
    # The number of the installment
    installmentNumber: Optional[int]
    # The total number of installments
    totalInstallments: Optional[int]
    # The amount of the installment
    totalAmount: Optional[int]
    # The MCC code of the counterpart
    payeeMCC: Optional[int]
    # The original date of the purchase
    purchaseDate: Optional[datetime]


class TransactionFilters(TypedDict):
    pageFilters: PageFilters
    to: Optional[str] = None
    from_: Optional[str] = None


class Transaction(TypedDict):
    # Primary identifier of the transaction
    id: str
    # Primary identifier of the Account
    accountId: str
    # Date of the transaction that was made.
    date: datetime
    # Transaction original description
    description: str
    # If available, raw description provided by the financial institution
    descriptionRaw: str | None
    # Transation type of movement
    type: TransactionType
    # Amount of the transaction
    amount: float
    # Amount of the transaction in account's currency
    amountInAccountCurrency: float | None
    # Current balance of the trasaction, after transaction was made.
    balance: float
    # ISO Currency code of the Transaction
    currencyCode: CurrencyCode
    # Assigned category of the transaction.
    category: str | None
    # Status of the transaction, default to `POSTED`
    status: Optional[TransactionStatus]
    # Code provided by the financial institution for the transaction type, not unique.
    providerCode: Optional[str]
    # Additional data related to payment or transfers
    paymentData: Optional[TransactionPaymentData]
    # Additional data related to credit card transaction
    creditCardMetadata: CreditCardMetadata | None
    # Additional data related to the merchant associated to the transaction
    merchant: Optional[TransactionMerchantData]
