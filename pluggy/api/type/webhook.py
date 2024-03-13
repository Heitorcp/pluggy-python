from dataclasses import dataclass
from datetime import date as Date
from typing import Literal, Optional, Union

from .execution import TriggeredBy

WEBHOOK_EVENTS = [
    'item/created',
    'item/updated',
    'item/error',
    'item/deleted',
    'item/waiting_user_input',
    'item/login_succeeded',
    'connector/status_updated',
    'transactions/deleted',
    'all',
]

# Type of events that can be subscribed
WebhookEvent = Literal[
    'item/created',
    'item/updated',
    'item/error',
    'item/deleted',
    'item/waiting_user_input',
    'item/login_succeeded',
    'connector/status_updated',
    'transactions/deleted',
    'all',
]


@dataclass
class Webhook:
    # Primary identifier of the entity
    id: str
    # Url where notifications of events will be sent
    url: str
    # Type of event subscribed
    event: WebhookEvent
    # Time of the creation of the webhook
    createdAt: Date
    # Time of last time the webhook was updated
    # (note: if it was never updated it will be equal to createdAt)
    updatedAt: Date
    # Time of when the webhook was disabled
    disabledAt: Date | None


@dataclass
class CreateWebhook:
    # Type of event subscribed
    event: WebhookEvent
    # Url where notifications of events will be sent
    url: str
    # Object to specify headers in your webhook notifications
    headers: Optional[dict[str, str]] | None


# @dataclass
class UpdateWebhook(CreateWebhook):
    # Boolean to enable or disable the webhook
    enabled: Optional[bool]


@dataclass
class Error:
    code: str
    message: str


@dataclass
class Data:
    status: str


@dataclass
class WebhookEventPayload:
    id: str
    eventId: str
    event: Union[
        Literal[
            'item/created',
            'item/updated',
            'item/waiting_user_input',
            'item/login_succeeded',
            'item/deleted',
        ],
        Literal['item/error'],
        Literal['connector/status_updated'],
        Literal['transactions/deleted'],
    ]
    itemId: str
    error: Optional[Error] = None
    triggeredBy: Optional[TriggeredBy] = None
    data: Optional[Data] = None
    clientId: Optional[str] = None
    accountId: Optional[str] = None
    transactionIds: Optional[list[str]] = None
