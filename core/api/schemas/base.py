from marshmallow import Schema, fields


class BaseSchema(Schema):
    # TYPEMAP common.utils.DatetimeWithTZ -> fields.DateTime
    pass


class BaseSchemaWithId(BaseSchema):
    id = fields.Integer(required=True)
