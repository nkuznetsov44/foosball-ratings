from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema, BaseSchemaWithID
from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.tournament import Tournament
from common.entities.state import PlayerState
from common.entities.state import RatingsState
from common.entities.match import Match


CompetitionSchema = class_schema(Competition, base_schema=BaseSchema)
CompetitionWithIDSchema = class_schema(Competition, base_schema=BaseSchemaWithID)

PlayerSchema = class_schema(Player, base_schema=BaseSchema)
PlayerWithIDSchema = class_schema(Player, base_schema=BaseSchemaWithID)

PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchema)
PlayerStateWithIDSchema = class_schema(PlayerState, base_schema=BaseSchemaWithID)

MatchSchema = class_schema(Match, base_schema=BaseSchema)
MatchWithIDSchema = class_schema(Match, base_schema=BaseSchemaWithID)

TournamentSchema = class_schema(Tournament, base_schema=BaseSchema)
TournamentWithIDSchema = class_schema(Tournament, base_schema=BaseSchemaWithID)

RatingsStateSchema = class_schema(RatingsState, base_schema=BaseSchema)
RatingsStateWithIDSchema = class_schema(RatingsState, base_schema=BaseSchemaWithID)
