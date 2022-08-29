from typing import Optional
from dataclasses import dataclass, field

from common.entities.enums import City
from common.entities.competition import Competition


@dataclass
class Tournament:
    id: int = field(init=False)
    name: str
    city: City
    url: Optional[str]
    competitions: list[Competition]
    external_id: Optional[int] = None
