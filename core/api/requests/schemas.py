from marshmallow import Schema, fields
from marshmallow_dataclass import class_schema

from core.api.requests.player import CreatePlayersRequest
from core.api.requests.competition import CreateCompetitionRequest

from core.entities.competition import Competition
from core.entities.state import PlayerState
from core.entities.player import Player


class BaseSchema(Schema):
    # TYPEMAP common.utils.DatetimeWithTZ -> fields.DateTime
    pass


CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)
PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchema)
PlayerSchema = class_schema(Player, base_schema=BaseSchema)


class GetPlayersResponseSchema(BaseSchema):
    players = fields.List(fields.Nested(PlayerSchema))


class CreatePlayersResponseSchema(BaseSchema):
    players = fields.List(fields.Nested(PlayerStateSchema))


CreateCompetitionRequestSchema = class_schema(
    CreateCompetitionRequest, base_schema=BaseSchema
)
CreateCompetitionResponseSchema = class_schema(Competition, base_schema=BaseSchema)
