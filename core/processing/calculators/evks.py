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
from core.entities.state import PlayerState
from core.exceptions import PlayerStateNotFound


class EvksGameType(Enum):
    QUALIFICATION = "Qualification"
    SET_TO_5 = "EachSetTo5Points"
    OTHER = "Other"


class BaseEvksRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.EVKS
    game_coefficients = ClassVar[dict[EvksGameType, int]]

    def calculate(self, match: Match, competition: Competition) -> dict[Player, int]:
        match_players_states = self._get_match_participants_states(match)

        rw = self._get_team_rating(match.winner_team, match_players_states)
        rl = self._get_team_rating(match.looser_team, match_players_states)

        t = competition.evks_importance_coefficient
        d = self._calculate_reliability_coefficients(match, match_players_states)
        k = self._calculate_base_coefficient(match)

        fraction = 1 / (10 ** ((rl - rw) / 400) + 1)
        base_rating = t * k * (1 - fraction)

        res: dict[Player, int] = {}

        for winner_player in match.winner_team.players:
            r = d[winner_player] * base_rating
            r_rounded = self._round_decimal(r)
            res[winner_player] = (
                match_players_states[winner_player].evks_rating + r_rounded
            )

        for looser_player in match.looser_team.players:
            r = d[looser_player] * base_rating
            r_rounded = self._round_decimal(r)
            res[looser_player] = (
                match_players_states[looser_player].evks_rating - r_rounded
            )

        return res

    def _round_decimal(self, value: Decimal) -> int:
        return int(value.quantize(Decimal("1"), ROUND_HALF_UP))

    def _get_player_state(self, player: Player) -> PlayerState:
        player_state = self.ratings_state.lookup_player_state(player)
        if not player_state:
            raise PlayerStateNotFound(player, self.ratings_state)
        return player_state

    def _get_match_participants_states(self, match: Match) -> dict[Player, PlayerState]:
        players = list(chain(match.first_team.players, match.second_team.players))
        player_states = map(self._get_player_state, players)
        return dict(zip(players, player_states))

    def _get_team_rating(
        self, team: Team, player_states: dict[Player, PlayerState]
    ) -> Decimal:
        first_player_state = player_states[team.first_player]
        if team.is_single_player:
            return Decimal(first_player_state.evks_rating)

        second_player_state = player_states[team.second_player]
        r1, r2 = sorted(
            [first_player_state.evks_rating, second_player_state.evks_rating]
        )
        return Decimal(2 * r2 + r1) / 3

    def _calculate_reliability_coefficients(
        self, match: Match, match_players_states: dict[Player, PlayerState]
    ) -> dict[Player, Decimal]:
        if match.is_singles:
            return self._calculate_singles_reliability_coefficients(
                match_players_states
            )
        return self._calculate_doubles_reliability_coefficients(
            match, match_players_states
        )

    def _calculate_singles_reliability_coefficients(
        self, match_players_states: dict[Player, PlayerState]
    ) -> dict[Player, Decimal]:
        res: dict[Player, Decimal] = {}

        for player_state, opp_state in permutations(match_players_states.values()):
            if player_state.is_evks_rating_active == opp_state.is_evks_rating_active:
                res[player_state.player] = Decimal(1)
            elif (
                player_state.is_evks_rating_active
                and not opp_state.is_evks_rating_active
            ):
                res[player_state.player] = Decimal("0.5")
            elif (
                not player_state.is_evks_rating_active
                and opp_state.is_evks_rating_active
            ):
                res[player_state.player] = Decimal(2)
            else:
                raise ValueError()
        return res

    def _calculate_doubles_reliability_coefficients(
        self, match: Match, match_players_states: dict[Player, PlayerState]
    ) -> dict[Player, Decimal]:
        res: dict[Player, Decimal] = {}

        for team, opp_team in permutations([match.first_team, match.second_team]):
            team_states = map(match_players_states.get, team.players)
            opp_states = map(match_players_states.get, opp_team.players)

            for player_state, partner_state in permutations(team_states):
                if player_state.is_evks_rating_active:
                    if all(
                        [
                            plr.is_evks_rating_active
                            for plr in chain(opp_states, [partner_state])
                        ]
                    ):
                        res[player_state.player] = Decimal(1)
                    else:
                        # Рейтинг игрока актуальный, а рейтинг хотя бы
                        # одного другого участника матча предварительный
                        res[player_state.player] = Decimal("0.5")
                else:
                    if all(
                        [opp_state.is_evks_rating_active for opp_state in opp_states]
                    ):
                        # Рейтинг игрока предварительный,
                        # а рейтинги обоих соперников актуальные
                        res[player_state.player] = Decimal(2)
                    else:
                        res[player_state.player] = Decimal(1)
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
