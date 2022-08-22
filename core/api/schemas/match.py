from marshmallow_dataclass import class_schema
from core.api.schemas.base import BaseSchemaWithId
from core.entities.match import Match


MatchSchema = class_schema(Match, base_schema=BaseSchemaWithId)
