from marshmallow_dataclass import class_schema

from common.entities.tournament import Tournament
from common.schemas import BaseSchema
from core.api.requests.tournament import CreateTournamentRequest
from core.api.schemas.base import BaseSchemaWithId

TournamentSchema = class_schema(Tournament, base_schema=BaseSchemaWithId)
CreateTournamentRequestSchema = class_schema(
    CreateTournamentRequest, base_schema=BaseSchema
)
