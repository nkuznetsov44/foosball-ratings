from dataclasses import dataclass
from entities import Match, Competition


class Event:
    pass


@dataclass
class ProcessMatchEvent(Event):
    match: Match


@dataclass
class ProcessCompetitionEvent(Event):
    competition: Competition
