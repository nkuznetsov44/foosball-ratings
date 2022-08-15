from marshmallow_dataclass import class_schema
from marshmallow_enum import EnumField
from marshmallow import Schema, fields
from core.entities.match import MatchSet
from core.entities.competition import CompetitionType


MatchSetSchema = class_schema(MatchSet)


class TeamSchema(Schema):
    first_player_id: fields.Integer()
    second_player_id: fields.Integer(required=False)


class MatchSchema(Schema):
    first_team = fields.Nested(TeamSchema)
    second_team = fields.Nested(TeamSchema)
    sets = fields.List(fields.Nested(MatchSetSchema))
    start_time = fields.DateTime()
    end_time = fields.DateTime()


class CompetitionRequestSchema(Schema):
    competition_type = EnumField(CompetitionType)
    matches = fields.List(fields.Nested(MatchSchema))
