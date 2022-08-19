from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.storage.mapping import mapper_registry
from common.utils import DatetimeWithTZ
from core.entities.player import Player


@mapper_registry.mapped
@dataclass
class Team:
    __table__ = Table(
        "teams",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("first_player_id", Integer, ForeignKey("players.id")),
        Column("second_player_id", Integer, ForeignKey("players.id"), nullable=True),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "first_player": relationship(
                Player, uselist=False, primaryjoin="Team.first_player_id == Player.id"
            ),
            "second_player": relationship(
                Player, uselist=False, primaryjoin="Team.second_player_id == Player.id"
            ),
        }
    }

    id: int = field(init=False)
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


@mapper_registry.mapped
@dataclass
class MatchSet:
    __table__ = Table(
        "sets",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("match_id", Integer, ForeignKey("matches.id")),
        Column("order", Integer),
        Column("first_team_score", Integer),
        Column("second_team_score", Integer, nullable=True),
    )

    id: int = field(init=False)
    order: int
    first_team_score: int
    second_team_score: int

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_score > self.second_team_score


@mapper_registry.mapped
@dataclass
class Match:
    __table__ = Table(
        "matches",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("first_team_id", Integer, ForeignKey("teams.id")),
        Column("second_team_id", Integer, ForeignKey("teams.id")),
        Column("start_datetime", DateTime(timezone=True)),
        Column("end_datetime", DateTime(timezone=True)),
        Column("force_qualification", Boolean),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "first_team": relationship(
                "Team", primaryjoin="Match.first_team_id == Team.id"
            ),
            "second_team": relationship(
                "Team", primaryjoin="Match.second_team_id == Team.id"
            ),
            "sets": relationship("MatchSet"),
        }
    }

    id: Optional[int] = field(init=False)
    first_team: Team
    second_team: Team
    sets: list[MatchSet]
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    force_qualification: Optional[bool] = False

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
