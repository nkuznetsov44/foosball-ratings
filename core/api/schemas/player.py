from marshmallow_dataclass import class_schema
from marshmallow import fields
from common.schemas import BaseSchema
from core.api.schemas.base import BaseSchemaWithId
from core.entities.player import Player
from core.entities.state import PlayerState
from core.api.requests.player import CreatePlayersRequest


PlayerSchema = class_schema(Player, base_schema=BaseSchemaWithId)
PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchemaWithId)


class GetPlayersResponseSchema(BaseSchema):
    players = fields.List(fields.Nested(PlayerSchema))


CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)


class CreatePlayersResponseSchema(BaseSchema):
    player_states = fields.List(fields.Nested(PlayerStateSchema))
