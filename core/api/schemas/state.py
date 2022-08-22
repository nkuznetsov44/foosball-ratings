from marshmallow import fields
from marshmallow_dataclass import class_schema
from marshmallow_enum import EnumField
from core.api.schemas.base import BaseSchemaWithId
from core.api.schemas.competition import CompetitionSchema
from core.api.schemas.match import MatchSchema
from core.entities.state import PlayerState
from common.enums import EvksPlayerRank


PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchemaWithId)


class RatingsStateCompetitionSchema(CompetitionSchema):
    class Meta:
        fields = (
            "id",
            "tournament_id",
            "competition_type",
            "evks_importance_coefficient",
            "start_datetime",
            "end_datetime",
            "external_id",
        )


class RatingsStateMatchSchema(MatchSchema):
    class Meta:
        fields = (
            "id",
            "external_id",
            "force_qualification",
            "start_datetime",
            "end_datetime",
        )


class RatingsStatePlayerStateSchema(PlayerStateSchema):
    last_match = fields.Nested(RatingsStateMatchSchema)


class RatingsStateResponseSchema(BaseSchemaWithId):
    previous_state_id = fields.Integer(required=False)
    last_competition = fields.Nested(RatingsStateCompetitionSchema, required=False)
    player_states_list = fields.List(fields.Nested(RatingsStatePlayerStateSchema))
    evks_player_ranks = fields.Dict(
        keys=fields.Integer(), values=EnumField(EvksPlayerRank)
    )
