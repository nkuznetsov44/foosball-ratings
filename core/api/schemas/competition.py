from marshmallow_dataclass import class_schema

from common.entities.competition import Competition
from core.api.schemas.base import BaseSchemaWithId

CompetitionSchema = class_schema(Competition, base_schema=BaseSchemaWithId)
