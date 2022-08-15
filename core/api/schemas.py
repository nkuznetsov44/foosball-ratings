from marshmallow_dataclass import class_schema
from marshmallow import Schema, fields
from core.entities import MatchSet


class PlayerRequestSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    sex = fields.String()


MatchSetRequestSchema = class_schema(MatchSet)


class MatchRequestSchema(Schema):
    first_player_id = fields.Integer()
    second_player_id = fields.Integer()
    sets = fields.List(fields.Nested(MatchSetRequestSchema))
    start_time = fields.DateTime()
    end_time = fields.DateTime()


class CompetitionRequestSchema(Schema):
    matches = fields.List(fields.Nested(MatchRequestSchema))
