from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.entities.enums import RatingsStateStatus
from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.tournament import Tournament
from common.entities.player_state import PlayerState
from common.entities.match import Match
from common.entities.team import Team


CompetitionSchema = class_schema(Competition, base_schema=BaseSchema)

PlayerSchema = class_schema(Player, base_schema=BaseSchema)

PlayerStateSchema = class_schema(PlayerState, base_schema=BaseSchema)

MatchSchema = class_schema(Match, base_schema=BaseSchema)

TournamentSchema = class_schema(Tournament, base_schema=BaseSchema)

TeamSchema = class_schema(Team, base_schema=BaseSchema)

class RatingsStateSchema(BaseSchema):
    id = fields.Integer()
    previous_state_id = fields.Integer(allow_none=True)
    last_competition = fields.Nested(CompetitionSchema, allow_none=True)
    player_states = fields.Nested(PlayerStateSchema, many=True)
    status = EnumField(RatingsStateStatus)
