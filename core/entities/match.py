from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Boolean,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from core.storage.mapping import mapper_registry
from common.utils import DatetimeWithTZ
from core.entities.team import Team
from core.entities.player import Player


@mapper_registry.mapped
@dataclass
class MatchSet:
    __table__ = Table(
        "sets",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("external_id", Integer, nullable=True),
        Column("match_id", Integer, ForeignKey("matches.id")),
        Column("order", Integer),
        Column("first_team_score", Integer),
        Column("second_team_score", Integer, nullable=True),
    )

    __table_args__ = (UniqueConstraint("match_id", "external_id"),)

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


@mapper_registry.mapped
@dataclass
class Match:
    __table__ = Table(
        "matches",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("external_id", Integer, nullable=True),
        Column("competition_id", Integer, ForeignKey("competitions.id")),
        Column("first_team_id", Integer, ForeignKey("teams.id")),
        Column("second_team_id", Integer, ForeignKey("teams.id")),
        Column("start_datetime", DateTime(timezone=True)),
        Column("end_datetime", DateTime(timezone=True)),
        Column("force_qualification", Boolean),
    )

    __mapper_args__ = {
        "properties": {
            "first_team": relationship(
                Team,
                uselist=False,
                primaryjoin="Match.first_team_id == Team.id",
            ),
            "second_team": relationship(
                Team,
                uselist=False,
                primaryjoin="Match.second_team_id == Team.id",
            ),
            "sets": relationship(MatchSet),
        }
    }

    __table_args__ = (UniqueConstraint("competition_id", "external_id"),)

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
