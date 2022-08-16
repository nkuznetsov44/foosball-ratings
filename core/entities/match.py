from typing import Optional
from dataclasses import dataclass
from common.utils import DatetimeWithTZ
from core.entities.player import Player


@dataclass
class Team:
    id: int
    first_player: Player
    second_player: Optional[Player]  # None for singles

    @property
    def is_single_player(self) -> bool:
        return self.second_player is None

    @property
    def players(self) -> list[Player]:
        if self.second_player:
            return [self.first_player, self.second_player]
        return [self.first_player]

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class MatchSet:
    id: int
    first_team_score: int
    second_team_score: int

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_score > self.second_team_score


@dataclass
class Match:
    id: int
    first_team: Team
    second_team: Team
    sets: list[MatchSet]
    force_qualification: Optional[bool]
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_qualification(self) -> bool:
        if self.force_qualification is not None:
            return self.force_qualification

        return len(self.sets) == 1 and (
            (self.sets[0].first_team_score == 7 and self.sets[0].second_team_score < 7)
            or (
                self.sets[0].first_team_score < 7
                and self.sets[0].second_team_score == 7
            )
        )

    @property
    def is_singles(self) -> bool:
        return self.first_team.is_single_player

    @property
    def first_team_sets_score(self) -> int:
        return len(filter(MatchSet.is_first_team_win, self.sets))

    @property
    def second_team_sets_score(self) -> int:
        return len(self.sets) - self.first_team_sets_score

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_sets_score > self.second_team_sets_score
