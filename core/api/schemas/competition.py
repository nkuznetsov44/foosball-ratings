from marshmallow_dataclass import class_schema
from core.api.schemas.base import BaseSchemaWithId
from core.entities.competition import Competition


CompetitionSchema = class_schema(Competition, base_schema=BaseSchemaWithId)
