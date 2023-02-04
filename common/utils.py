from datetime import datetime
import re


class DatetimeWithTZ(datetime):
    pass


_camel_to_snake_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name: str) -> str:
    return _camel_to_snake_pattern.sub("_", name).lower()
