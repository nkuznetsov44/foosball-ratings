from typing import Optional, Sequence
from dataclasses import dataclass

from common.utils import DatetimeWithTZ
from common.entities.competition import Competition
from common.entities.team import Team
from common.entities.player import Player


@dataclass
class Match:
    id: int
    competition: Competition
    order: int
    first_team: Team
    second_team: Team
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    force_qualification: Optional[bool] = None
    external_id: Optional[int] = None

    @property
    def players(self) -> list[Player]:
        return self.first_team.players + self.second_team.players

    @property
    def is_singles(self) -> bool:
        return self.first_team.is_single_player

    def is_before(self, other: "Match") -> bool:
        return self.end_datetime < other.start_datetime


@dataclass
class MatchSet:
    id: int
    match: Match
    order: int
    first_team_score: int
    second_team_score: int
    external_id: Optional[int] = None

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_score > self.second_team_score


class MatchUtils:
    @classmethod
    def is_qualification(cls, match: Match, match_sets: Sequence[MatchSet]) -> bool:
        return (
            match.force_qualification
            or len(match_sets) == 1
            and (
                (
                    match_sets[0].first_team_score == 7
                    and match_sets[0].second_team_score < 7
                )
                or (
                    match_sets[0].first_team_score < 7
                    and match_sets[0].second_team_score == 7
                )
            )
        )

    @classmethod
    def get_winner_team_and_score(
        cls,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> tuple[Team, int]:
        first_team_score, second_team_score = cls.get_teams_scores(match_sets)

        # TODO: get max_sets from cls.match implement grand final and other formats
        if first_team_score > second_team_score:
            return match.first_team, first_team_score
        return match.second_team, second_team_score

    @classmethod
    def get_looser_team_and_score(
        cls,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> tuple[Team, int]:
        first_team_score, second_team_score = cls.get_teams_scores(match_sets)

        # TODO: get max_sets from cls.match implement grand final and other formats
        if first_team_score > second_team_score:
            return match.second_team, second_team_score
        return match.first_team, first_team_score

    @classmethod
    def get_teams_scores(cls, match_sets: Sequence[MatchSet]) -> tuple[int, int]:
        first_team_score = len([mset for mset in match_sets if mset.is_first_team_win])
        second_team_score = len(match_sets) - first_team_score
        return first_team_score, second_team_score
