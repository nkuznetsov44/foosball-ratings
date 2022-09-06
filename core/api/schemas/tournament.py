from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from core.api.requests.tournament import CreateTournamentRequest


CreateTournamentRequestSchema = class_schema(
    CreateTournamentRequest, base_schema=BaseSchema
)
