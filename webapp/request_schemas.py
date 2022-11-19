from marshmallow import fields
from marshmallow_enum import EnumField

from common.schemas.base import BaseSchema
from common.entities.enums import RatingType


class RatingsStateRequestSchema(BaseSchema):
    active_only = fields.Boolean(required=False, allow_none=False)
    rating_type = EnumField(RatingType, required=False)
