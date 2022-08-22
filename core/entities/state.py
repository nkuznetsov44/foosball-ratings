from typing import Optional, Union, Any
from dataclasses import dataclass, field
from sqlalchemy import types, Table, Column, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from common.enums import RatingType, EvksPlayerRank
from core.storage.mapping import mapper_registry
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition


_RatingValue = int


class _RatingsJSON(types.TypeDecorator):
    impl = JSON

    def process_bind_param(
        self, value: dict[RatingType, _RatingValue], _: Any
    ) -> dict[str, int]:
        return {key.name: val for key, val in value.items()}

    def process_result_value(
        self, value: dict[str, int], _: Any
    ) -> dict[RatingType, _RatingValue]:
        return {RatingType[key]: val for key, val in value.items()}


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
        Column("matches_played", Integer),
        Column("matches_won", Integer),
        Column("last_match_id", Integer, ForeignKey("matches.id")),
        Column("ratings", _RatingsJSON),
        Column("is_evks_rating_active", Boolean),
    )

    __mapper_args__ = {
        "properties": {
            "player": relationship(Player, uselist=False),
            "last_match": relationship(Match, uselist=False),
        },
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
        return self.ratings.get(RatingType.CUMULATIVE)

    def __hash__(self) -> int:
        assert self.id is not None, "Can't hash PlayerState with no id"
        return hash(self.id)


_PlayerId = int
PlayerStates = dict[_PlayerId, PlayerState]


association_table = Table(
    "ratings_state_player_states",
    mapper_registry.metadata,
    Column("player_state_id", ForeignKey("player_states.id")),
    Column("ratings_state_id", ForeignKey("ratings_states.id")),
)


class _EvksPlayerRanksJSON(types.TypeDecorator):
    impl = JSON

    def process_bind_param(
        self, value: dict[_PlayerId, EvksPlayerRank], _: Any
    ) -> dict[int, str]:
        return {key: val.name for key, val in value.items()}

    def process_result_value(
        self, value: dict[int, str], _: Any
    ) -> dict[_PlayerId, EvksPlayerRank]:
        return {key: EvksPlayerRank[val] for key, val in value.items()}


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
        Column("evks_player_ranks", _EvksPlayerRanksJSON),
        Column("last_competition_id", Integer, ForeignKey("competitions.id")),
    )

    __mapper_args__ = {
        "properties": {
            "player_states": relationship(
                PlayerState,
                secondary=association_table,
                collection_class=attribute_mapped_collection("player_id"),
            ),
            "last_competition": relationship(Competition, uselist=False),
        }
    }

    id: int = field(init=False)
    previous_state_id: Optional[int]
    last_competition: Optional[Competition]
    player_states: PlayerStates
    evks_player_ranks: dict[_PlayerId, EvksPlayerRank]

    @property
    def player_states_list(self) -> list[PlayerState]:
        return list(self.player_states.values())

    def __getitem__(self, item: Union[_PlayerId, Player]) -> Optional[PlayerState]:
        if isinstance(item, Player):
            player_id = item.id
            if player_id is None:
                raise KeyError(f"Can't get player state for player with no id {item}")
        elif isinstance(item, _PlayerId):
            player_id = item
        else:
            raise KeyError(f"Incorrect player state key type {type(item)}")
        return self.player_states.get(player_id)

    def dirty_copy(self) -> "RatingsState":
        """Returns a dirty shallow copy of self"""
        return RatingsState(
            previous_state_id=self.previous_state_id,
            player_states=self.player_states.copy(),
            evks_player_ranks=self.evks_player_ranks.copy(),
            last_competition=self.last_competition,
        )
