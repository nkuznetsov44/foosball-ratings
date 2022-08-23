from marshmallow import Schema, fields
from marshmallow_dataclass import class_schema
from webapp.entities.player import Player
from webapp.entities.competition import Competition


PlayerSchema = class_schema(Player)


class PlayerIdSchema(Schema):
    player_id = fields.Integer()


class PlayerCompetitionIdSchema(Schema):
    player_id = fields.Integer()
    competition_id = fields.Integer()


class GetPlayersResponseSchema(Schema):
    players = fields.Nested(PlayerSchema, many=True)


CompetitionSchema = class_schema(Competition)


class GetPlayerCompetitionsResponseSchema(Schema):
    competitions = fields.Nested(CompetitionSchema, many=True)
