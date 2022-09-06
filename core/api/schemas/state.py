from marshmallow import fields
from marshmallow_enum import EnumField

from common.entities.enums import EvksPlayerRank, RatingsStateStatus
from common.schemas.base import BaseSchemaWithID
from common.schemas.entity_schemas import (
    CompetitionWithIDSchema,
    MatchWithIDSchema,
    PlayerStateWithIDSchema,
)


class RatingsStateCompetitionSchema(CompetitionWithIDSchema):  # type: ignore
    class Meta(CompetitionWithIDSchema.Meta):  # type: ignore
        fields = (
            "id",
            "tournament_id",
            "competition_type",
            "external_id",
        )


class RatingsStateMatchSchema(MatchWithIDSchema):  # type: ignore
    class Meta(MatchWithIDSchema.Meta):  # type: ignore
        fields = (
            "id",
            "external_id",
        )


class RatingsStatePlayerStateSchema(PlayerStateWithIDSchema):  # type: ignore
    last_match = fields.Nested(RatingsStateMatchSchema)


class RatingsStateResponseSchema(BaseSchemaWithID):
    # FIXME: replace required with nullable
    previous_state_id = fields.Integer(required=False)
    last_competition = fields.Nested(RatingsStateCompetitionSchema, required=False)
    player_states = fields.Nested(RatingsStatePlayerStateSchema, many=True)
    evks_player_ranks = fields.Dict(
        keys=fields.Integer(), values=fields.Nested(EnumField(EvksPlayerRank))
    )
    status = EnumField(RatingsStateStatus)
