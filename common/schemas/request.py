from marshmallow import fields

from common.schemas.base import BaseSchema


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)


class PlayerCompetitionIDSchema(BaseSchema):
    player_id = fields.Integer(required=True, allow_none=False)
    competition_id = fields.Integer(required=True, allow_none=False)
