from dataclasses import dataclass, field
from typing import Optional
from common.entities.enums import City


@dataclass
class CreateTournamentRequest:
    external_id: Optional[int]
    city: City
    name: str
    url: Optional[str]
