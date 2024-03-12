from dataclasses import dataclass
from typing import Optional, TypedDict


class ConnectTokenOptions(TypedDict):
    # Url where notifications will be sent at any item's event
    webhookUrl: Optional[str]
    # A unique identifier of the user, usually used the UserId of your app
    clientUserId: Optional[str]
