from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow_dataclass import class_schema

from common.schemas.base import BaseSchema
from common.entities.enums import RatingType

from webapp.requests.ratings_state import RatingsStateResponse


class RatingsStateRequestSchema(BaseSchema):
    active_only = fields.Boolean(required=True, allow_none=False)
    rating_type = EnumField(RatingType, required=True)


RatingsStateResponseSchema = class_schema(RatingsStateResponse, base_schema=BaseSchema)
