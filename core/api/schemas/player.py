from marshmallow import fields
from marshmallow_dataclass import class_schema

from common.entities.player import Player
from common.entities.state import PlayerState
from common.schemas import BaseSchema
from core.api.requests.player import CreatePlayersRequest
from core.api.schemas.base import BaseSchemaWithId


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True)


PlayerSchema = class_schema(Player, base_schema=BaseSchemaWithId)
PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchemaWithId)


class GetPlayersResponseSchema(BaseSchema):
    players = fields.List(fields.Nested(PlayerSchema))


CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)
