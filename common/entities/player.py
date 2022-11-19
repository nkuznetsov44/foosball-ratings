from typing import Optional
from dataclasses import dataclass

from common.entities.enums import City


@dataclass
class Player:
    id: int
    first_name: str
    last_name: str
    city: City
    is_foreigner: bool = False
    external_id: Optional[int] = None

    def __hash__(self) -> int:
        assert self.id is not None, "Can't hash Player with no id"
        return hash(self.id)
