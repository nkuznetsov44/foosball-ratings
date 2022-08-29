from typing import Any

from sqlalchemy import JSON
from sqlalchemy.types import TypeDecorator

from common.entities.enums import EvksPlayerRank, RatingType

_RatingValue = int
_PlayerId = int


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


class EvksPlayerRanksJSON(TypeDecorator):
    impl = JSON

    def process_bind_param(
        self, value: dict[_PlayerId, EvksPlayerRank], _: Any
    ) -> dict[int, str]:
        return {key: val.name for key, val in value.items()}

    def process_result_value(
        self, value: dict[int, str], _: Any
    ) -> dict[_PlayerId, EvksPlayerRank]:
        return {key: EvksPlayerRank[val] for key, val in value.items()}
