from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import ClassVar
from itertools import permutations, chain
from common.enums import RatingType
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
)
from core.entities.competition import Competition
from core.entities.match import Match
from core.entities.team import Team
from core.entities.player import Player
from core.exceptions import PlayerStateNotFound


class EvksGameType(Enum):
    QUALIFICATION = "Qualification"
    SET_TO_5 = "EachSetTo5Points"
    OTHER = "Other"


_PlayerId = int
_RatingValue = int


class BaseEvksRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.EVKS
    game_coefficients = ClassVar[dict[EvksGameType, int]]

    def calculate(
        self, match: Match, competition: Competition
    ) -> dict[_PlayerId, _RatingValue]:
        for player in match.players:
            if not self.ratings_state[player]:
                raise PlayerStateNotFound(
                    player_id=player.id, current_state=self.ratings_state
                )

        rw = self._get_team_rating(match.winner_team)
        rl = self._get_team_rating(match.looser_team)

        t = competition.evks_importance_coefficient
        d = self._calculate_reliability_coefficients(match)
        k = self._calculate_base_coefficient(match)

        fraction = 1 / (10 ** ((rl - rw) / 400) + 1)
        base_rating = t * k * (1 - fraction)

        res: dict[_PlayerId, _RatingValue] = {}

        for winner_player in match.winner_team.players:
            r = d[winner_player.id] * base_rating
            r_rounded = self._round_decimal(r)
            res[winner_player.id] = (
                self.ratings_state[winner_player].evks_rating + r_rounded
            )

        for looser_player in match.looser_team.players:
            r = d[looser_player.id] * base_rating
            r_rounded = self._round_decimal(r)
            res[looser_player.id] = (
                self.ratings_state[looser_player].evks_rating - r_rounded
            )

        return res

    def _round_decimal(self, value: Decimal) -> int:
        return int(value.quantize(Decimal("1"), ROUND_HALF_UP))

    def _get_team_rating(self, team: Team) -> Decimal:
        first_player_state = self.ratings_state[team.first_player]
        if team.is_single_player:
            return Decimal(first_player_state.evks_rating)

        second_player_state = self.ratings_state[team.second_player]
        r1, r2 = sorted(
            [first_player_state.evks_rating, second_player_state.evks_rating]
        )
        return Decimal(2 * r2 + r1) / 3

    def _calculate_reliability_coefficients(
        self, match: Match
    ) -> dict[_PlayerId, Decimal]:
        if match.is_singles:
            return self._calculate_singles_reliability_coefficients(match)
        return self._calculate_doubles_reliability_coefficients(match)

    def _calculate_singles_reliability_coefficients(
        self, match: Match
    ) -> dict[_PlayerId, Decimal]:
        match_players_states = [self.ratings_state[player] for player in match.players]
        assert (
            len(match_players_states) == 2
        ), "Match player states must be of len 2 for a singles match"

        res: dict[_PlayerId, Decimal] = {}
        for player_state, opp_state in permutations(match_players_states):
            if player_state.is_evks_rating_active == opp_state.is_evks_rating_active:
                res[player_state.player.id] = Decimal(1)
            elif (
                player_state.is_evks_rating_active
                and not opp_state.is_evks_rating_active
            ):
                res[player_state.player.id] = Decimal("0.5")
            elif (
                not player_state.is_evks_rating_active
                and opp_state.is_evks_rating_active
            ):
                res[player_state.player.id] = Decimal(2)
            else:
                raise ValueError()
        return res

    def _calculate_doubles_reliability_coefficients(
        self, match: Match
    ) -> dict[Player, Decimal]:
        res: dict[_PlayerId, Decimal] = {}

        for team, opp_team in permutations([match.first_team, match.second_team]):
            team_states = [self.ratings_state[player] for player in team.players]
            opp_states = [self.ratings_state[opp] for opp in opp_team.players]

            for player_state, partner_state in permutations(team_states):
                if player_state.is_evks_rating_active:
                    if all(
                        [
                            plr.is_evks_rating_active
                            for plr in chain(opp_states, [partner_state])
                        ]
                    ):
                        res[player_state.player.id] = Decimal(1)
                    else:
                        # Рейтинг игрока актуальный, а рейтинг хотя бы
                        # одного другого участника матча предварительный
                        res[player_state.player.id] = Decimal("0.5")
                else:
                    if all(
                        [opp_state.is_evks_rating_active for opp_state in opp_states]
                    ):
                        # Рейтинг игрока предварительный,
                        # а рейтинги обоих соперников актуальные
                        res[player_state.player.id] = Decimal(2)
                    else:
                        res[player_state.player.id] = Decimal(1)
        return res

    def _get_game_type(self, match: Match) -> EvksGameType:
        if match.is_qualification:
            return EvksGameType.QUALIFICATION
        if (
            match.sets[0].first_team_score == 5
            and match.sets[0].second_team_score < 5
            or match.sets[0].first_team_score < 5
            and match.sets[0].second_team_score == 5
        ):
            return EvksGameType.SET_TO_5
        return EvksGameType.OTHER

    def _calculate_base_coefficient(self, match: Match) -> int:
        score_diff = abs(match.first_team_sets_score - match.second_team_sets_score)
        return score_diff * self.game_coefficients[self._get_game_type(match)]


class Pre2018EvksRatingCalculator(BaseEvksRatingCalculator):
    game_coefficients = {
        EvksGameType.QUALIFICATION: 32,
        EvksGameType.SET_TO_5: 24,
        EvksGameType.OTHER: 32,
    }


class EvksRatingCalculator(BaseEvksRatingCalculator):
    game_coefficients = {
        EvksGameType.QUALIFICATION: 16,
        EvksGameType.SET_TO_5: 24,
        EvksGameType.OTHER: 32,
    }
