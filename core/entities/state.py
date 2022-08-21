from typing import Optional, NoReturn
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
from common.enums import RatingType, EvksPlayerRank
from core.storage.mapping import mapper_registry
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition


_RatingValue = int


@mapper_registry.mapped
@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""

    __table__ = Table(
        "player_states",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "previous_state_id", Integer, ForeignKey("player_states.id"), nullable=True
        ),
        Column("player_id", Integer, ForeignKey("players.id")),
        Column("matches_won", Integer),
        Column("last_match_id", Integer, ForeignKey("matches.id")),
        Column("ratings", JSON),
        Column("is_evks_rating_active", Boolean),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "player": relationship(Player, uselist=False),
        }
    }

    id: int = field(init=False)
    previous_state_id: Optional[int]
    player: Player
    matches_played: int
    matches_won: int
    last_match: Optional[Match]
    ratings: dict[RatingType, _RatingValue]
    is_evks_rating_active: bool

    @property
    def evks_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.EVKS)

    @property
    def cumulative_rating(self) -> Optional[int]:
        return self.rating.get(RatingType.CUMULATIVE)

    def __hash__(self) -> int:
        assert self.id is not None
        return hash(self.id)


_PlayerId = int


association_table = Table(
    "ratings_state_player_states",
    mapper_registry.metadata,
    Column("player_state_id", ForeignKey("player_states.id")),
    Column("ratings_state_id", ForeignKey("ratings_states.id")),
)


@mapper_registry.mapped
@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    __table__ = Table(
        "ratings_states",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "previous_state_id", Integer, ForeignKey("ratings_states.id"), nullable=True
        ),
        Column("evks_player_ranks", JSON),
        Column("last_competition_id", Integer, ForeignKey("competitions.id")),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "player_states": relationship(
                PlayerState, secondary=association_table, collection_class=set
            ),
        }
    }

    id: int = field(init=False)
    previous_state_id: Optional[int]
    last_competition: Optional[Competition]
    player_states: set[PlayerState]
    evks_player_ranks: dict[_PlayerId, EvksPlayerRank]

    def lookup_player_state(self, player: Player) -> Optional[PlayerState]:
        return next(
            filter(lambda ps: ps.player.id == player.id, self.player_states), None
        )

    def dirty_copy(self) -> "DirtyRatingsState":
        return DirtyRatingsState.from_state(self)


class DirtyRatingsState(RatingsState):
    READ_FROM_DIRTY_STATE = ValueError("Read from dirty state")

    @property
    def id(self) -> NoReturn:
        raise self.READ_FROM_DIRTY_STATE

    @property
    def previous_state_id(self) -> NoReturn:
        raise self.READ_FROM_DIRTY_STATE

    @property
    def evks_player_ranks(self) -> NoReturn:
        raise self.READ_FROM_DIRTY_STATE

    @property
    def last_competition(self) -> NoReturn:
        raise self.READ_FROM_DIRTY_STATE

    @classmethod
    def from_state(cls, state: RatingsState) -> "DirtyRatingsState":
        return DirtyRatingsState(
            previous_state_id=None,
            player_states=state.player_states.copy(),  # a shallow copy of player states
            evks_player_ranks={},
            last_competition=None,
        )
