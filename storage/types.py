from typing import Any, Optional

from sqlalchemy import JSON
from sqlalchemy.types import TypeDecorator
from marshmallow_dataclass import class_schema

from common.entities.enums import RatingType
from common.entities.match import GrandFinalOptions


_RatingValue = int


class RatingsJSON(TypeDecorator):
    impl = JSON

    def process_bind_param(
        self, value: dict[RatingType, _RatingValue], _: Any
    ) -> dict[str, int]:
        return {key.name: val for key, val in value.items()}

    def process_result_value(
        self, value: dict[str, int], _: Any
    ) -> dict[RatingType, _RatingValue]:
        return {RatingType[key]: val for key, val in value.items()}


class GrandFinalOptionsJSON(TypeDecorator):
    impl = JSON
    schema = class_schema(GrandFinalOptions)

    def process_bind_param(
        self, value: Optional[GrandFinalOptions], _: Any
    ) -> Optional[dict[str, Any]]:
        if value is None:
            return None
        return self.schema().dump(value)

    def process_result_value(
        self, value: dict[str, Any], _: Any
    ) -> Optional[GrandFinalOptions]:
        if value is None:
            return None
        return self.schema().load(value)
