from typing import Any
from decimal import Decimal
from marshmallow import Schema, fields

from common.utils import DatetimeWithTZ


class MyDecimalField(fields.Decimal):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.pop("as_string", None)
        super().__init__(*args, as_string=True, **kwargs)


class BaseSchema(Schema):
    TYPE_MAPPING = {
        Decimal: MyDecimalField,
        DatetimeWithTZ: fields.DateTime,
    }

    class Meta:
        strict = True
