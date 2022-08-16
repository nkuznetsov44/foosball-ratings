from typing import Sequence, Optional
from core.actions.abstract_action import AbstractAction
from core.entities.state import PlayerState, RatingsState, EvksPlayerRank
from core.entities.player import Player
from core.entities.match import Match
from core.entities.rating import RatingType


class CreatePlayerStateAction(AbstractAction):
    def __init__(
        self,
        *,
        player: Player,
        last_match: Optional[Match],
        rating_values: Optional[dict[RatingType, int]],
        initial_evks_rating: Optional[int],
    ) -> None:
        self.player = player
        self.last_match = last_match
        self.rating_values = rating_values
        self.initial_evks_rating = initial_evks_rating

    async def run(self) -> PlayerState:
        # реализовать универсальный метод создания PlayerState
        # как для нового игрока, так и для обновления рейтинга существующего игрока
        pass


class CreateRatingsStateAction(AbstractAction):
    def __init__(
        self,
        current_state: RatingsState,
        new_player_states: Sequence[PlayerState]
    ) -> None:
        self.current_state = current_state
        self.new_player_states = new_player_states

    def _get_player_evks_rank(self, player_state: PlayerState) -> EvksPlayerRank:
        # реализовать логику перехода между рангами после категории
        pass

    async def run(self) -> RatingsState:
        pass
