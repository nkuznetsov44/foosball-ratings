from typing import Optional
from dataclasses import dataclass
from storage.model import Player, Match, Competition


@dataclass
class PlayerState:
    id: int
    player: Player
    last_match: Optional[Match]  # optional for players initial state where no matches were played
    rating: int


@dataclass
class RatingState:
    id: int
    player_states: set[PlayerState]
    last_competition_id: Optional[Competition]  # optional for initial state where no competition were played

    def lookup_player_state(self, Player) -> PlayerState:
        # looks up player state from rating state
        pass
