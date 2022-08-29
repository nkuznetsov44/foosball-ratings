from marshmallow_dataclass import class_schema

from common.entities.match import Match
from core.api.schemas.base import BaseSchemaWithId

MatchSchema = class_schema(Match, base_schema=BaseSchemaWithId)
