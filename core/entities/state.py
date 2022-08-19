from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean, JSON
from common.enums import RatingType, EvksPlayerRank
from core.storage.mapping import mapper_registry
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition


@mapper_registry.mapped
@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""

    __table__ = Table(
        "player_states",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("previous_state_id", Integer, ForeignKey("player_states.id")),
        Column("player_id", Integer, ForeignKey("players.id")),
        Column("matches_won", Integer),
        Column("last_match_id", Integer, ForeignKey("matches.id")),
        Column("ragings", JSON),
        Column("is_evks_rating_active", Boolean),
    )

    id: Optional[int] = field(init=False)
    previous_state_id: Optional[int]
    player: Player
    matches_played: int  # суммарное количество матчей, сыгранное к этому моменту
    matches_won: int
    last_match: Optional[
        Match
    ]  # optional for players initial state where no matches were played
    ratings: dict[RatingType, int]
    is_evks_rating_active: bool

    @property
    def evks_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.EVKS)

    @property
    def cumulative_rating(self) -> Optional[int]:
        return self.rating.get(RatingType.CUMULATIVE)


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    id: Optional[int] = field(init=False)
    previous_state_id: Optional[int]
    player_states: set[PlayerState]
    player_evks_ranks: dict[int, EvksPlayerRank]  # maps player_id -> EvksPlayerRank
    last_competition: Optional[
        Competition
    ]  # optional for initial state where no competition were played

    def lookup_player_state(self, player: Player) -> Optional[PlayerState]:
        return next(
            filter(lambda ps: ps.player.id == player.id, self.player_states), None
        )
