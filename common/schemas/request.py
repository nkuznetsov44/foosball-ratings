from marshmallow import fields

from common.schemas.base import BaseSchema


class PlayerIDSchema(BaseSchema):
    player_id = fields.Integer(required=True)  # FIXME: nullable false


class PlayerCompetitionIDSchema(BaseSchema):
    # FIXME: nullable false
    player_id = fields.Integer(required=True)
    competition_id = fields.Integer(required=True)
