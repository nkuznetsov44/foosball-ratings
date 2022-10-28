from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from itertools import chain, permutations
from typing import ClassVar, Sequence

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet, MatchUtils
from common.entities.team import Team
from core.exceptions import PlayerStateNotFound
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
    RatingCalculationResult,
)


class EvksGameType(Enum):
    QUALIFICATION = "Qualification"
    SET_TO_5 = "EachSetTo5Points"
    OTHER = "Other"


PlayerValueMap = dict[int, Decimal]


class BaseEvksRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.EVKS
    game_coefficients = ClassVar[dict[EvksGameType, int]]

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult:
        for player in match.players:
            try:
                self.ratings_state.player_states[player]
            except KeyError:
                raise PlayerStateNotFound(
                    player_id=player.id, current_state=self.ratings_state
                )

        winner_team, winner_team_score = MatchUtils.get_winner_team_and_score(
            match, match_sets
        )
        looser_team, looser_team_score = MatchUtils.get_looser_team_and_score(
            match, match_sets
        )

        rw = self._get_team_rating(winner_team)
        rl = self._get_team_rating(looser_team)

        t = competition.evks_importance_coefficient
        d = self._calculate_reliability_coefficients(match)
        k = self._calculate_base_coefficient(
            match=match,
            match_sets=match_sets,
            winner_team_score=winner_team_score,
            looser_team_score=looser_team_score,
        )

        fraction = 1 / (10 ** ((rl - rw) / 400) + 1)
        base_rating = t * k * (1 - fraction)

        res: RatingCalculationResult = RatingCalculationResult()

        for winner_player in winner_team.players:
            r = d[winner_player.id] * base_rating
            r_rounded = self._round_decimal(r)
            res[winner_player.id] = r_rounded

        for looser_player in looser_team.players:
            r = d[looser_player.id] * base_rating
            r_rounded = self._round_decimal(r)
            res[looser_player.id] = -r_rounded

        return res

    def _round_decimal(self, value: Decimal) -> int:
        return int(value.quantize(Decimal("1"), ROUND_HALF_UP))

    def _get_team_rating(self, team: Team) -> Decimal:
        first_player_state = self.ratings_state.player_states[team.first_player]
        if team.is_single_player:
            return Decimal(first_player_state.evks_rating)

        second_player_state = self.ratings_state.player_states[team.second_player]
        r1, r2 = sorted(
            [first_player_state.evks_rating, second_player_state.evks_rating]
        )
        return Decimal(2 * r2 + r1) / 3

    def _calculate_reliability_coefficients(self, match: Match) -> PlayerValueMap:
        if match.is_singles:
            return self._calculate_singles_reliability_coefficients(match)
        return self._calculate_doubles_reliability_coefficients(match)

    def _calculate_singles_reliability_coefficients(self, match: Match) -> PlayerValueMap:
        match_players_states = [
            self.ratings_state.player_states[player] for player in match.players
        ]
        assert (
            len(match_players_states) == 2
        ), "Match player states must be of len 2 for a singles match"

        res: PlayerValueMap = {}
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

    def _calculate_doubles_reliability_coefficients(self, match: Match) -> PlayerValueMap:
        res: PlayerValueMap = {}

        for team, opp_team in permutations([match.first_team, match.second_team]):
            team_states = [
                self.ratings_state.player_states[player] for player in team.players
            ]
            opp_states = [
                self.ratings_state.player_states[opp] for opp in opp_team.players
            ]

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

    def _get_game_type(
        self, match: Match, match_sets: Sequence[MatchSet]
    ) -> EvksGameType:
        if MatchUtils.is_qualification(match, match_sets):
            return EvksGameType.QUALIFICATION
        if (
            match_sets[0].first_team_score == 5
            and match_sets[0].second_team_score < 5
            or match_sets[0].first_team_score < 5
            and match_sets[0].second_team_score == 5
        ):
            return EvksGameType.SET_TO_5
        return EvksGameType.OTHER

    def _calculate_base_coefficient(
        self,
        *,
        match: Match,
        match_sets: Sequence[MatchSet],
        winner_team_score: int,
        looser_team_score: int,
    ) -> int:
        # TODO: implement grandfinals and other formats
        score_diff = winner_team_score - looser_team_score
        return (
            score_diff * self.game_coefficients[self._get_game_type(match, match_sets)]
        )


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
