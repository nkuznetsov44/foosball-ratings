from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from core.api.requests.player import CreatePlayersRequest


CreatePlayersRequestSchema = class_schema(CreatePlayersRequest, base_schema=BaseSchema)
