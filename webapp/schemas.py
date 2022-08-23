from marshmallow import fields
from marshmallow_dataclass import class_schema
from common.schemas import BaseSchema
from webapp.entities.player import Player
from webapp.entities.competition import Competition, Tournament


PlayerSchema = class_schema(Player, base_schema=BaseSchema)


class PlayerIdSchema(BaseSchema):
    player_id = fields.Integer()


class PlayerCompetitionIdSchema(BaseSchema):
    player_id = fields.Integer()
    competition_id = fields.Integer()


class GetPlayersResponseSchema(BaseSchema):
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


class GetPlayerCompetitionsResponseSchema(BaseSchema):
    competitions = fields.Nested(PlayerCompetitionSchema, many=True)
