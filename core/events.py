from dataclasses import dataclass
from enum import Enum
from storage.model import Competition, Match


class Event:
    pass


@dataclass
class CreateMatchEvent(Event):
    match: Match
    is_processed: bool = False


class CreateCompetitionStatus(Enum):
    PROCESSING = 'PROCESSING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'


@dataclass
class CreateCompetitionEvent(Event):
    competition: Competition
    status: CreateCompetitionStatus = CreateCompetitionStatus.PROCESSING
