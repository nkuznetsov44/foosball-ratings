from marshmallow import fields
from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.entities.ratings_state import RatingsState, PlayerStateSet
from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.tournament import Tournament
from common.entities.player_state import PlayerState
from common.entities.match import Match, MatchSet, MatchWithRelated
from common.entities.team import Team


PlayerSchema = class_schema(Player, base_schema=BaseSchema)

PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchema)

MatchSchema = class_schema(Match, base_schema=BaseSchema)

MatchSetSchema = class_schema(MatchSet, base_schema=BaseSchema)

MatchWithRelatedSchema = class_schema(MatchWithRelated, base_schema=BaseSchema)

TournamentSchema = class_schema(Tournament, base_schema=BaseSchema)

TeamSchema = class_schema(Team, base_schema=BaseSchema)

CompetitionSchema = class_schema(Competition, base_schema=BaseSchema)


class PlayerStateSetField(fields.Nested):
    def __init__(self, **kwargs):  # type: ignore
        if "many" in kwargs:
            kwargs.pop("many")
        super().__init__(PlayerStateSchema, many=True, **kwargs)

    def _serialize(self, nested_obj: PlayerStateSet, attr, obj, **kwargs):  # type: ignore
        return super()._serialize(nested_obj.to_list(), attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, partial=None, **kwargs):  # type: ignore
        lst_values = super()._deserialize(value, attr, data, partial, **kwargs)
        return PlayerStateSet(lst_values)


class _RatingsStateBaseSchema(BaseSchema):
    TYPE_MAPPING = BaseSchema.TYPE_MAPPING | {
        PlayerStateSet: PlayerStateSetField,
    }


RatingsStateSchema = class_schema(RatingsState, base_schema=_RatingsStateBaseSchema)
