from marshmallow_dataclass import class_schema
from common.schemas import BaseSchema
from core.api.schemas.base import BaseSchemaWithId
from core.api.requests.tournament import CreateTournamentRequest
from core.entities.tournament import Tournament


TournamentSchema = class_schema(Tournament, base_schema=BaseSchemaWithId)
CreateTournamentRequestSchema = class_schema(
    CreateTournamentRequest, base_schema=BaseSchema
)
