from typing import Optional
from datetime import date
from dataclasses import dataclass


@dataclass
class Referee:
    id: int
    first_name: str
    last_name: str
    first_name_en: str
    last_name_en: str
    email: Optional[str]
    languages: list[str]
    city: str  # FIXME
    rank: str  # FIXME
    rank_update: date
    photo: Optional[str]
    is_active: bool
    user: Optional[int]
