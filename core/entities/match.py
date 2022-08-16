from typing import Optional
from dataclasses import dataclass
from common.utils import DatetimeWithTZ
from core.entities.player import Player


@dataclass
class Team:
    id: int
    first_player: Player
    second_player: Optional[Player]  # None for singles

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
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def first_team_sets_score(self) -> int:
        return len(filter(MatchSet.is_first_team_win, self.sets))
    
    @property
    def second_team_sets_score(self) -> int:
        return len(self.sets) - self.first_team_sets_score

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_sets_score > self.second_team_sets_score
