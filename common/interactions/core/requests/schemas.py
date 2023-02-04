from marshmallow import fields
from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.interactions.core.requests.player import CreatePlayersRequest
from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
)


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)


class PlayerCompetitionIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)
    competition_id = fields.Integer(required=True, allow_none=False)


class TournamentIDSchema(BaseSchema):
    tournament_id = fields.Integer(requried=True, allow_none=False)


class TournamentCompetitionIDSchema(BaseSchema):
    tournament_id = fields.Integer(requried=True, allow_none=False)
    competition_id = fields.Integer(required=True, allow_none=False)


CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)

CreateTournamentRequestSchema = class_schema(CreateTournamentRequest, base_schema=BaseSchema)

CreateCompetitionRequestSchema = class_schema(CreateCompetitionRequest, base_schema=BaseSchema)
