from typing import Optional
from dataclasses import dataclass

from common.entities.enums import City


@dataclass
class Tournament:
    id: int
    name: str
    city: City
    url: Optional[str]
    external_id: Optional[int] = None
