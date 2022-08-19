from marshmallow_dataclass import class_schema
from core.api.schemas.base import BaseSchema, BaseSchemaWithId
from core.api.requests.competition import CreateCompetitionRequest
from core.entities.competition import Competition


CompetitionSchema = class_schema(Competition, base_schema=BaseSchemaWithId)

CreateCompetitionRequestSchema = class_schema(
    CreateCompetitionRequest, base_schema=BaseSchema
)
