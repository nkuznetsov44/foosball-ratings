from marshmallow import fields
from marshmallow_dataclass import class_schema

from common.schemas import BaseSchema
from common.entities.competition import Competition
from common.entities.tournament import Tournament
from common.entities.player import Player


PlayerSchema = class_schema(Player, base_schema=BaseSchema)


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer()


class PlayerCompetitionIDSchema(BaseSchema):
    player_id = fields.Integer()
    competition_id = fields.Integer()


class PlayersResponseSchema(BaseSchema):
    players = fields.Nested(PlayerSchema, many=True)


TournamentSchema = class_schema(Tournament, base_schema=BaseSchema)
CompetitionSchema = class_schema(Competition, base_schema=BaseSchema)


class CompetitionTournamentSchema(TournamentSchema):
    class Meta:
        fields = (
            "id",
            "name",
            "city",
            "url",
        )


class PlayerCompetitionSchema(CompetitionSchema):
    tournament = fields.Nested(CompetitionTournamentSchema)


class PlayerCompetitionsResponseSchema(BaseSchema):
    competitions = fields.Nested(PlayerCompetitionSchema, many=True)
