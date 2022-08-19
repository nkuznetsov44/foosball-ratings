from marshmallow_dataclass import class_schema
from core.api.schemas.base import BaseSchema, BaseSchemaWithId
from core.entities.tournament import Tournament


TournamentSchema = class_schema(Tournament, base_schema=BaseSchemaWithId)
CreateTournamentRequestSchema = class_schema(Tournament, base_schema=BaseSchema)
