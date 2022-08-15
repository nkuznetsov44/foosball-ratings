from dataclasses import dataclass


@dataclass
class Player:
    id: int
    first_name: str
    last_name: str

    def __hash__(self) -> int:
        return hash(self.id)
