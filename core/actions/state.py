from typing import Sequence, Optional
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.state import PlayerState, RatingsState, EvksPlayerRank
from core.entities.player import Player
from core.entities.match import Match
from core.entities.rating import RatingType
from core.exceptions import PlayerStateAlreadyExists


class BasePlayerStateAction(AbstractAction):
    async def _save_player_state(self, player_state: PlayerState) -> PlayerState:
        async with self.context.db.acquire() as conn:
            await conn.execute(
                PlayerState.table()
                .insert()
                .values(
                    player_id=player_state.player.id,
                    matches_played=player_state.matches_played,
                    matches_won=player_state.matches_won,
                    last_match_id=player_state.last_match,
                    ratings=player_state.ratings,  # TODO: fixme
                    is_evks_rating_active=player_state.is_evks_rating_active,
                )
            )

        # TODO: implement insert returning id
        player_state.id = player_state_id
        return player_state


class CreateInitialPlayerStateAction(BasePlayerStateAction):
    INITIAL_RATING_VALUES = {
        RatingType.EVKS: 1100,
        RatingType.CUMULATIVE: 0,
    }

    def __init__(
        self,
        *,
        player: Player,
        context: ActionContext,
        rating_values: Optional[dict[RatingType, int]],
        matches_played: Optional[int],
        matches_won: Optional[int],
        is_evks_rating_active: Optional[bool],
    ):
        super().__init__(context)
        self._player = player
        self._rating_values = rating_values
        self._matches_played = matches_played
        self._matches_won = matches_won
        self._is_evks_rating_active = is_evks_rating_active

    async def run(self) -> PlayerState:
        if self.context.ratings_state.lookup_player_state(self._player):
            raise PlayerStateAlreadyExists(
                player=self._player, current_state=self.context.ratings_state
            )

        matches_played = self._matches_played or 0
        is_evks_rating_active = self._is_evks_rating_active or (matches_played > 10)

        return await self._save_player_state(
            PlayerState(
                player=self.player,
                matches_played=matches_played,
                matches_won=self.matches_won or 0,
                last_match=None,
                ratings=self._rating_values or self.INITIAL_RATING_VALUES,
                is_evks_rating_active=is_evks_rating_active,
            )
        )


class CreatePlayerStateAction(BasePlayerStateAction):
    def __init__(
        self,
        *,
        player: Player,
        context: ActionContext,
        last_match: Match,
        rating_values: dict[RatingType, int],
    ) -> None:
        super().__init__(context)
        self._player = player
        self._last_match = last_match
        self._rating_values = rating_values
        self._current_player_state = self.context.ratings_state.lookup_player_state(
            player
        )

    async def run(self) -> PlayerState:
        if (
            self._last_match.start_datetime
            < self.context.ratings_state.last_competition.end_datetime
        ):
            raise NotImplementedError(
                f"Match {self._last_match} starts before last processed competition "
                f"{self.context.ratings_state.last_competition}. "
                "Processing competitions in not historical order is not implemented."
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
                player=self._player,
                matches_played=new_matches_played,
                matches_won=new_matches_won,
                last_match=self._last_match,
                ratings=self._rating_values,
                is_evks_rating_active=is_evks_rating_active,
            )
        )


class CreateRatingsStateAction(AbstractAction):
    def __init__(
        self, current_state: RatingsState, new_player_states: Sequence[PlayerState]
    ) -> None:
        self.current_state = current_state
        self.new_player_states = new_player_states

    def _get_player_evks_rank(self, player_state: PlayerState) -> EvksPlayerRank:
        # реализовать логику перехода между рангами после категории
        pass

    async def run(self) -> RatingsState:
        pass
