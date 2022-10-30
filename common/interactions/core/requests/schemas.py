from marshmallow import fields
from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.requests.player_competition_matches import (
    PlayerCompetitionMatchesResponse,
)
from common.interactions.core.requests.player import CreatePlayersRequest
from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.requests.competition import (
    CompetitionResponse,
    CreateCompetitionRequest,
)


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)


class PlayerCompetitionIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)
    competition_id = fields.Integer(required=True, allow_none=False)


class TournamentIDSchema(BaseSchema):
    tournament_id = fields.Integer(requried=True, allow_nonw=False)


class TournamentCompetitionIDSchema(BaseSchema):
    tournament_id = fields.Integer(requried=True, allow_nonw=False)
    competition_id = fields.Integer(required=True, allow_none=False)


PlayerCompetitionMatchesResponseSchema = class_schema(
    PlayerCompetitionMatchesResponse, base_schema=BaseSchema
)

CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)

CreateTournamentRequestSchema = class_schema(
    CreateTournamentRequest, base_schema=BaseSchema
)

CreateCompetitionRequestSchema = class_schema(
    CreateCompetitionRequest, base_schema=BaseSchema
)

RatingsStateResponseSchema = class_schema(RatingsStateResponse, base_schema=BaseSchema)

CompetitionResponseSchema = class_schema(CompetitionResponse, base_schema=BaseSchema)
