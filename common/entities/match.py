from typing import Optional
from dataclasses import dataclass, field

from common.utils import DatetimeWithTZ
from common.entities.team import Team
from common.entities.player import Player


@dataclass
class MatchSet:
    id: int = field(init=False)
    match_id: int = field(init=False)
    order: int
    first_team_score: int
    second_team_score: int
    external_id: Optional[int] = None

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_score > self.second_team_score


@dataclass
class Match:
    id: int = field(init=False)
    competition_id: int = field(init=False)
    first_team: Team
    second_team: Team
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    sets: list[MatchSet]
    force_qualification: Optional[bool] = False
    external_id: Optional[int] = None

    @property
    def is_qualification(self) -> bool:
        return (
            self.force_qualification
            or len(self.sets) == 1
            and (
                (
                    self.sets[0].first_team_score == 7
                    and self.sets[0].second_team_score < 7
                )
                or (
                    self.sets[0].first_team_score < 7
                    and self.sets[0].second_team_score == 7
                )
            )
        )

    @property
    def is_singles(self) -> bool:
        return self.first_team.is_single_player

    @property
    def first_team_sets_score(self) -> int:
        return len([s for s in self.sets if s.is_first_team_win])

    @property
    def second_team_sets_score(self) -> int:
        return len(self.sets) - self.first_team_sets_score

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_sets_score > self.second_team_sets_score

    @property
    def winner_team(self) -> Team:
        if self.is_first_team_win:
            return self.first_team
        return self.second_team

    @property
    def looser_team(self) -> Team:
        if self.is_first_team_win:
            return self.second_team
        return self.first_team

    @property
    def players(self) -> list[Player]:
        return self.first_team.players + self.second_team.players

    def is_before(self, other: "Match") -> bool:
        return self.end_datetime < other.start_datetime
