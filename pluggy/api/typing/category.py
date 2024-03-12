from dataclasses import dataclass
from typing import Generic, Optional

from pluggy.api.typing.common import PageResponse


@dataclass
class Category(PageResponse):
    # primary identifier of the category
    id: str
    # Category's name or description.
    description: str
    # Parent category hierachy primary identifier
    parentId: Optional[str]
    # Parent category hierachy name or description
    parentDescription: Optional[str]
