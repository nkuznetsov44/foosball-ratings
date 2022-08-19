from dataclasses import dataclass


@dataclass
class CreateTournamentRequest:
    city: str
    name: str
