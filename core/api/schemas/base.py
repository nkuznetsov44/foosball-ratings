from marshmallow import fields

from common.schemas import BaseSchema


class BaseSchemaWithId(BaseSchema):
    id = fields.Integer(required=True)
