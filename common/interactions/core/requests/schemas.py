from marshmallow import fields
from marshmallow_dataclass import class_schema
from common.interactions.core.requests.ratings_state import RatingsStateResponse

from common.schemas.base import BaseSchema
from common.interactions.core.requests.player_competition_matches import (
    PlayerCompetitionMatchesResponse,
)
from common.interactions.core.requests.player import CreatePlayersRequest
from common.interactions.core.requests.tournament import CreateTournamentRequest


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)


class PlayerCompetitionIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)
    competition_id = fields.Integer(required=True, allow_none=False)


PlayerCompetitionMatchesResponseSchema = class_schema(
    PlayerCompetitionMatchesResponse, base_schema=BaseSchema
)

CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)

CreateTournamentRequestSchema = class_schema(
    CreateTournamentRequest, base_schema=BaseSchema
)

RatingsStateResponseSchema = class_schema(RatingsStateResponse, base_schema=BaseSchema)
