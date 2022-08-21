from typing import Any
from enum import Enum
import json
from datetime import datetime


class DatetimeWithTZ(datetime):
    pass


def enum_by_value_json_serializer(obj: Any):
    if isinstance(obj, Enum):
        return obj.name
    return json.dumps(obj)
