from typing import Optional
from core.actions.abstract_action import AbstractAction
from core.entities.state import EvksPlayerRank


class CreatePlayerAction(AbstractAction):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        initial_evks_rating: Optional[int],
        initial_evks_rank: Optional[EvksPlayerRank]
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.initial_evks_rating = initial_evks_rating
        self.initial_evks_rank = initial_evks_rank
