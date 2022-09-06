from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.tournament import Tournament
from common.entities.state import PlayerState
from common.entities.state import RatingsState
from common.entities.match import Match


CompetitionSchema = class_schema(Competition, base_schema=BaseSchema)

PlayerSchema = class_schema(Player, base_schema=BaseSchema)

PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchema)

MatchSchema = class_schema(Match, base_schema=BaseSchema)

TournamentSchema = class_schema(Tournament, base_schema=BaseSchema)

RatingsStateSchema = class_schema(RatingsState, base_schema=BaseSchema)
