from dataclasses import dataclass
from datetime import date
from enum import Enum, auto
from typing import Dict, List, Literal, Optional, TypeVar

from .connector import Connector, ConnectorCredential, ProductType
from .execution import ExecutionErrorResult, ExecutionStatus

ITEM_STATUSES = [
    'UPDATED',
    'UPDATING',
    'WAITING_USER_INPUT',
    'WAITING_USER_ACTION',
    'MERGING',
    'LOGIN_ERROR',
    'OUTDATED',
]

"""
 * The current Item status.
 *  UPDATED: The last sync process has completed successfully and all new data is available to collect.
 *  UPDATING: An update process is in progress and will be updated soon.
 *  WAITING_USER_INPUT: The connection requires user's input to continue the sync process, this is common for MFA authentication connectors
 *  LOGIN_ERROR: The connection must be updated to execute again, it won't trigger updates until the parameters are updated.
 *  OUTDATED: The parameters were correctly validated but there was an error in the last execution. It can be retried.
"""


class ItemStatus(Enum):
    UPDATED = auto()
    UPDATING = auto()
    WAITING_USER_INPUT = auto()
    WAITING_USER_ACTION = auto()
    MERGING = auto()
    LOGIN_ERROR = auto()
    OUTDATED = auto()


ITEM_PRODUCT_STEP_WARNING_CODES = ['001']


class ItemProductStepWarningCode(Enum):
    ITEM_PRODUCT_STEP_WARNING_CODES = '001'


@dataclass
class ItemProductStepWarning:
    # The specific warning code
    code: ItemProductStepWarningCode
    # Human readable message that explains the warning
    message: str
    # Related error message exactly as found in the institution (if any).
    providerMessage: Optional[str]


@dataclass
class ItemProductState:
    # Whether product was collected in this last execution or not */
    isUpdated: bool
    # Date when product was last collected for this Item, null if it has never been. */
    lastUpdatedAt: date | None
    # If product was not collected, this field will provide more detailed info about the reason. */
    warnings: Optional[List[ItemProductStepWarning]]


@dataclass
class ItemProductsStatusDetail:

    """
    * Only available when item.status is 'PARTIAL_SUCCESS'.
    * Provides fine-grained information, per product, about their latest collection state.

    * If a product was not requested at all, its entry will be null.
    * If it was requested, it's entry will reflect if it has been collected or not.
    *  If collected, isUpdated will be true, and lastUpdatedAt will be the Date when it happened
    *  If not collected, isUpdated will be false, and lastUpdatedAt will be null it wasn't ever collected before, or the previous date if it was.
    """

    # Collection details for 'ACCOUNTS' product, or null if it was not requested at all. */
    accounts: ItemProductState | None
    # Collection details for 'CREDIT_CARDS' product, or null if it was not requested at all. */
    creditCards: ItemProductState | None
    # Collection details for account 'TRANSACTIONS' product, or null if it was not requested at all. */
    transactions: ItemProductState | None
    # Collection details for 'INVESTMENTS' product, or null if it was not requested at all. */
    investments: ItemProductState | None
    # Collection details for 'INESTMENT_TRANSACTIONS' product, or null if it was not requested at all. */
    investmentTransactions: ItemProductState | None
    # Collection details for 'IDENTITY' product, or null if it was not requested at all. */
    identity: ItemProductState | None
    # Collection details for 'PAYMENT_DATA' product, or null if it was not requested at all. */
    paymentData: ItemProductState | None
    # Collection details for 'INCOME_REPORT' product, or null if it was not requested at all. */
    incomeReports: ItemProductState | None
    # Collection details for 'PORTFOLIO' product, or null if it was not requested at all. */
    portfolio: ItemProductState | None
    # Collection details for 'LOAN' product, or null if it was not requested at all. */
    loans: ItemProductState | None
    # Collection details for 'OPPORTUNITIES' product, or null if it was not requested at all. */
    opportunities: ItemProductState | None


@dataclass
class UserAction:
    # Human readble instructions that explains the user action to be done. */
    instructions: str
    # Type of user action to be done */
    type: Literal['qr', 'authorize-access']
    # Unstructured properties that provide additional context of the user action. */
    attributes: Dict[str, str]
    # Parameter expiration date, action should be done before this time. */
    expiresAt: date


@dataclass
class Item:
    # primary identifier of the Item
    id: str
    # Connector's associated with item
    connector: Connector
    # Current status of the item
    status: ItemStatus
    # If status is 'PARTIAL_SUCCESS', this field will provide more detailed info about which products have been recovered or failed.
    statusDetail: ItemProductsStatusDetail | None
    # Item error details, if finished in an error status
    error: ExecutionErrorResult | None
    # Current execution status of item.
    executionStatus: ExecutionStatus
    # Date of the first connection
    createdAt: date
    # Date of last item related data update
    updatedAt: date
    # Last connection sync date with the institution.
    lastUpdatedAt: date | None
    # In case of MFA connections, extra parameter will be available.
    parameter: ConnectorCredential | None
    # Url where notifications will be sent at any item's event
    webhookUrl: str | None
    # A unique identifier for the User, to be able to identify it on your app
    clientUserId: str | None
    # Useful info when item execution status is "WAITING_USER_ACTION"
    userAction: UserAction | None
    # The number of consecutive failed login attempts for this item.
    consecutiveFailedLoginAttempts: float
    # The date when the next Pluggy's auto-sync update will be attempted (if item is updatable).
    nextAutoSyncAt: date | None


@dataclass
class CreateItemOptions:
    # Url where notifications will be sent at any item's event
    webhookUrl: Optional[str]
    # A unique identifier for the User, to be able to identify it on your app
    clientUserId: Optional[str]
    #
    # Products to include in item execution and collection steps. Optional.
    # If not specified, all products available to your subscription level will be collected.
    #
    products: Optional[List[ProductType]]


# The Item Create/Update parameters object to submit, which contains the needed user credentials.
Parameters = Dict[str, str]
