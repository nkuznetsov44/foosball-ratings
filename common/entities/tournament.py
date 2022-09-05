from typing import Optional
from dataclasses import dataclass, field

from common.entities.enums import City


@dataclass
class Tournament:
    id: int = field(init=False)
    name: str
    city: City
    url: Optional[str]
    external_id: Optional[int] = None
