from dataclasses import dataclass
from typing import Optional

from pypluggy.api.type.common import PageResponse


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
