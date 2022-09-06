from marshmallow import fields
from marshmallow_enum import EnumField

from common.entities.enums import EvksPlayerRank, RatingsStateStatus
from common.schemas.base import BaseSchema
from common.schemas.entity_schemas import (
    CompetitionSchema,
    MatchSchema,
    PlayerStateSchema,
)


class RatingsStateCompetitionSchema(CompetitionSchema):  # type: ignore
    class Meta(CompetitionSchema.Meta):  # type: ignore
        fields = (
            "id",
            "tournament_id",
            "competition_type",
            "external_id",
        )


class RatingsStateMatchSchema(MatchSchema):  # type: ignore
    class Meta(MatchSchema.Meta):  # type: ignore
        fields = (
            "id",
            "external_id",
        )


class RatingsStatePlayerStateSchema(PlayerStateSchema):  # type: ignore
    last_match = fields.Nested(RatingsStateMatchSchema)


class RatingsStateResponseSchema(BaseSchema):
    id = fields.Integer(required=True, allow_none=False)
    previous_state_id = fields.Integer(allow_none=True)
    last_competition = fields.Nested(RatingsStateCompetitionSchema, allow_none=True)
    player_states = fields.Nested(
        RatingsStatePlayerStateSchema, many=True
    )  # TODO: fixme
    evks_player_ranks = fields.Dict(
        keys=fields.Integer(), values=fields.Nested(EnumField(EvksPlayerRank))
    )
    status = EnumField(RatingsStateStatus)
