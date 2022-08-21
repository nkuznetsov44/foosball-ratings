from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from core.storage.mapping import mapper_registry
from core.entities.player import Player


@mapper_registry.mapped
@dataclass
class Team:
    __table__ = Table(
        "teams",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("competition_id", Integer, ForeignKey("competitions.id")),
        Column("external_id", Integer, nullable=True),
        Column("competition_place", Integer),
        Column("first_player_id", Integer, ForeignKey("players.id")),
        Column("second_player_id", Integer, ForeignKey("players.id"), nullable=True),
    )

    __table_args__ = (UniqueConstraint("competition_id", "external_id"),)

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
    competition_id: int = field(init=False)
    competition_place: int
    first_player: Player
    second_player: Optional[Player]  # None for singles
    external_id: Optional[int] = None

    @property
    def is_single_player(self) -> bool:
        return self.second_player is None

    @property
    def players(self) -> list[Player]:
        if self.second_player:
            return [self.first_player, self.second_player]
        return [self.first_player]
