from dataclasses import dataclass, field

from common.entities.enums import City


@dataclass
class Player:
    id: int = field(init=False)
    first_name: str
    last_name: str
    city: City

    def __hash__(self) -> int:
        assert self.id is not None, "Can't hash Player with no id"
        return hash(self.id)
