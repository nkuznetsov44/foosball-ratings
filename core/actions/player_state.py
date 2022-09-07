from typing import Optional

from common.entities.enums import RatingType
from common.entities.match import Match, MatchUtils
from common.entities.player import Player
from common.entities.player_state import PlayerState
from core.actions.abstract_action import AbstractAction
from core.exceptions import (
    PlayerStateAlreadyExists,
    PlayerStateNotFound,
    PlayerStateSequenceError,
)


class CreateInitialPlayerStateAction(AbstractAction[PlayerState]):
    INITIAL_RATING_VALUES = {
        RatingType.EVKS: 1100,
        RatingType.CUMULATIVE: 0,
    }

    def __init__(
        self,
        *,
        player: Player,
        evks_rating: Optional[int],
        cumulative_rating: Optional[int],
        matches_played: Optional[int],
        matches_won: Optional[int],
        is_evks_rating_active: Optional[bool],
    ):
        self.player = player
        self.evks_rating = evks_rating
        self.cumulative_rating = cumulative_rating
        self.matches_played = matches_played
        self.matches_won = matches_won
        self.is_evks_rating_active = is_evks_rating_active

    async def handle(self) -> PlayerState:
        ratings_state = await self.storage.ratings_states.get_actual()

        if ratings_state[self.player]:
            raise PlayerStateAlreadyExists(
                player_id=self.player.id, current_state=ratings_state
            )

        matches_played = self.matches_played or 0
        is_evks_rating_active = self.is_evks_rating_active or (matches_played > 10)

        ratings: dict[RatingType, int] = {}
        if self.evks_rating:
            ratings[RatingType.EVKS] = self.evks_rating
        if self.cumulative_rating:
            ratings[RatingType.CUMULATIVE] = self.cumulative_rating

        ratings = ratings | self.INITIAL_RATING_VALUES

        return await self.storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=None,
                player=self.player,
                matches_played=matches_played,
                matches_won=self.matches_won or 0,
                last_match=None,
                ratings=ratings,
                is_evks_rating_active=is_evks_rating_active,
            )
        )


class CreatePlayerStateAction(AbstractAction[PlayerState]):
    def __init__(
        self,
        *,
        player: Player,
        last_match: Match,
        ratings: dict[RatingType, int],
    ) -> None:
        self.player = player
        self.last_match = last_match
        self.ratings = ratings

    async def handle(self) -> PlayerState:
        assert (
            self.ratings.get(RatingType.EVKS) is not None
        ), "Need EVKS rating value to create player state"
        assert (
            self.ratings.get(RatingType.CUMULATIVE) is not None
        ), "Need Cumulative rating value to create player state"

        ratings_state = await self.storage.ratings_states.get_actual()

        current_player_state = ratings_state[self.player]

        if not current_player_state:
            raise PlayerStateNotFound(
                player_id=self.player.id, current_state=ratings_state
            )

        if current_player_state.last_match and self.last_match.is_before(
            current_player_state.last_match
        ):
            raise PlayerStateSequenceError(
                match_id=self.last_match.id,
                last_match_id=current_player_state.last_match.id,
                current_state=ratings_state,
            )

        new_matches_played = current_player_state.matches_played + 1

        last_match_sets = await self.storage.sets.find_by_match(self.last_match.id)
        last_match_winner_team, _ = MatchUtils.get_winner_team_and_score(
            self.last_match, last_match_sets
        )

        new_matches_won = current_player_state.matches_won
        if self.player in last_match_winner_team.players:
            new_matches_won = new_matches_won + 1

        # TODO: implement logic of player become inactive
        # after 1Y of no matches played and active after first
        # competition played after being inactive
        is_evks_rating_active = new_matches_played > 10

        return await self.storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=current_player_state.id,
                player=self.player,
                matches_played=new_matches_played,
                matches_won=new_matches_won,
                last_match=self.last_match,
                ratings=self.ratings,
                is_evks_rating_active=is_evks_rating_active,
            )
        )
