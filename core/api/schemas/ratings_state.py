from marshmallow import fields
from marshmallow_enum import EnumField

from common.entities.enums import EvksPlayerRank, RatingsStateStatus
from common.schemas.base import BaseSchema
from common.entities.schemas import (
    CompetitionSchema,
    MatchSchema,
    PlayerStateSchema,
)


# TODO:
# Refactor to common/interactions/core/requests/ratings_state/RatingsStateResponse
# and create RatingsStateResponse with marshmallow_dataclass


class CompetitionSchema_(CompetitionSchema):  # type: ignore
    class Meta(CompetitionSchema.Meta):  # type: ignore
        fields = (
            "id",
            "tournament_id",
            "competition_type",
            "external_id",
        )


class MatchSchema_(MatchSchema):  # type: ignore
    class Meta(MatchSchema.Meta):  # type: ignore
        fields = (
            "id",
            "external_id",
        )


class PlayerStateSchema_(PlayerStateSchema):  # type: ignore
    last_match = fields.Nested(MatchSchema_)

    class Meta(PlayerStateSchema.Meta):  # type: ignore
        fields = (
            "player",
            "matches_played",
            "matches_won",
            "ratings",
            "is_evks_rating_active",
        )


class RatingsStateResponseSchema(BaseSchema):
    id = fields.Integer(required=True, allow_none=False)
    previous_state_id = fields.Integer(allow_none=True)
    last_competition = fields.Nested(CompetitionSchema_, allow_none=True)
    player_states = fields.Nested(PlayerStateSchema_, many=True)  # TODO: fixme
    evks_player_ranks = fields.Dict(
        keys=fields.Integer(), values=fields.Nested(EnumField(EvksPlayerRank))
    )
    status = EnumField(RatingsStateStatus)
