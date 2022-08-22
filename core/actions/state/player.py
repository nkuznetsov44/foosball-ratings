from typing import Optional
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.state import PlayerState
from core.entities.player import Player
from core.entities.match import Match
from common.enums import RatingType
from core.exceptions import (
    PlayerStateAlreadyExists,
    PlayerStateNotFound,
    PlayerStateSequenceError,
)


class BasePlayerStateAction(AbstractAction):
    async def _save_player_state(self, player_state: PlayerState) -> PlayerState:
        async with self.make_db_session()() as session:
            session.add(player_state)
            await session.commit()
            assert player_state.id is not None
            return player_state


class CreateInitialPlayerStateAction(BasePlayerStateAction):
    INITIAL_RATING_VALUES = {
        RatingType.EVKS: 1100,
        RatingType.CUMULATIVE: 0,
    }

    def __init__(
        self,
        *,
        context: ActionContext,
        player: Player,
        evks_rating: Optional[int],
        cumulative_rating: Optional[int],
        matches_played: Optional[int],
        matches_won: Optional[int],
        is_evks_rating_active: Optional[bool],
    ):
        super().__init__(context)
        self._player = player
        self._evks_rating = evks_rating
        self._cumulative_rating = cumulative_rating
        self._matches_played = matches_played
        self._matches_won = matches_won
        self._is_evks_rating_active = is_evks_rating_active

    async def run(self) -> PlayerState:
        if self.ratings_state[self._player]:
            raise PlayerStateAlreadyExists(
                player_id=self._player.id, current_state=self.ratings_state
            )

        matches_played = self._matches_played or 0
        is_evks_rating_active = self._is_evks_rating_active or (matches_played > 10)

        ratings: dict[RatingType, int] = {}
        if self._evks_rating:
            ratings[RatingType.EVKS] = self._evks_rating
        if self._cumulative_rating:
            ratings[RatingType.CUMULATIVE] = self._cumulative_rating

        ratings = ratings | self.INITIAL_RATING_VALUES

        return await self._save_player_state(
            PlayerState(
                previous_state_id=None,
                player=self._player,
                matches_played=matches_played,
                matches_won=self._matches_won or 0,
                last_match=None,
                ratings=ratings,
                is_evks_rating_active=is_evks_rating_active,
            )
        )


class CreatePlayerStateAction(BasePlayerStateAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        player: Player,
        last_match: Match,
        ratings: dict[RatingType, int],
    ) -> None:
        super().__init__(context)
        self._player = player
        self._last_match = last_match
        self._ratings = ratings
        self._current_player_state = self.ratings_state[player]

    async def run(self) -> PlayerState:
        assert (
            self._ratings.get(RatingType.EVKS) is not None
        ), "Need EVKS rating value to create player state"
        assert (
            self._ratings.get(RatingType.CUMULATIVE) is not None
        ), "Need Cumulative rating value to create player state"

        if not self._current_player_state:
            raise PlayerStateNotFound(
                player_id=self._player.id, current_state=self.ratings_state
            )

        if self._current_player_state.last_match and self._last_match.is_before(
            self._current_player_state.last_match
        ):
            raise PlayerStateSequenceError(
                match_id=self._last_match.id, current_state=self.ratings_state
            )

        new_matches_played = self._current_player_state.matches_played + 1

        new_matches_won = self._current_player_state.matches_won
        if self._player in self._last_match.winner_team.players:
            new_matches_won = new_matches_won + 1

        # TODO: implement logic of player become inactive
        # after 1Y of no matches played and active after first
        # competition played after being inactive
        is_evks_rating_active = new_matches_played > 10

        return await self._save_player_state(
            PlayerState(
                previous_state_id=self._current_player_state.id,
                player=self._player,
                matches_played=new_matches_played,
                matches_won=new_matches_won,
                last_match=self._last_match,
                ratings=self._ratings,
                is_evks_rating_active=is_evks_rating_active,
            )
        )