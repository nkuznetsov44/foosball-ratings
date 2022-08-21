from typing import Sequence, Optional
from common.enums import EvksPlayerRank
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.state import PlayerState, RatingsState
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition
from common.enums import RatingType
from core.exceptions import PlayerStateAlreadyExists


class BasePlayerStateAction(AbstractAction):
    async def _save_player_state(self, player_state: PlayerState) -> PlayerState:
        async with self._make_db_session()() as session:
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
        if self._ratings_state.lookup_player_state(self._player):
            raise PlayerStateAlreadyExists(
                player=self._player, current_state=self._ratings_state
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
        self._current_player_state = self._ratings_state.lookup_player_state(player)

    async def run(self) -> PlayerState:
        assert self._ratings.get(RatingType.EVKS) is not None
        assert self._ratings.get(RatingType.CUMULATIVE) is not None

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


class CreateRatingsStateAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        player_states: Sequence[PlayerState],
        last_competition: Competition,
    ) -> None:
        super().__init__(context)
        self._player_states = player_states
        self._last_competition = last_competition

    def _get_evks_player_rank(self, player_state: PlayerState) -> EvksPlayerRank:
        # TODO: реализовать логику перехода между рангами после категории
        pass

    async def run(self) -> RatingsState:
        raise NotImplementedError()  # TODO: implement
