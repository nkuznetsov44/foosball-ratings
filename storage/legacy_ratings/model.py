from typing import Optional
from enum import Enum, unique
from dataclasses import dataclass, field
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import registry, relationship


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Player:
    __tablename__ = "players"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    first_name: str = field(metadata={"sa": sa.Column(sa.String(255))})
    last_name: str = field(metadata={"sa": sa.Column(sa.String(255))})
    itsf_first_name: Optional[str] = field(metadata={"sa": sa.Column(sa.String(255), nullable=True)})
    itsf_last_name: Optional[str] = field(metadata={"sa": sa.Column(sa.String(255), nullable=True)})
    itsf_license: int = field(metadata={"sa": sa.Column(sa.Integer)})
    itsf_rating: Optional[int] = field(metadata={"sa": sa.Column(sa.Integer, nullable=True)})
    evks_initial_rating: int = field(metadata={"sa": sa.Column(sa.Integer)})
    evks_initial_matches_count: int = field(metadata={"sa": sa.Column(sa.Integer)})
    evks_initial_matches_win: int = field(metadata={"sa": sa.Column(sa.Integer)})
    foreigner: bool = field(metadata={"sa": sa.Column(sa.Boolean)})


@mapper_registry.mapped
@dataclass
class Team:
    __tablename__ = "teams"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    competition_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("competitions.id"))})
    player1_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("players.id"))})
    player2_id: Optional[int] = field(metadata={"sa": sa.Column(sa.ForeignKey("players.id"), nullable=True)})
    position: int = field(metadata={"sa": sa.Column(sa.Integer)})
    order: int = field(metadata={"sa": sa.Column(sa.Integer)})

    player1: Player = field(
        metadata={"sa": relationship(Player, uselist=False, primaryjoin="Team.player1_id == Player.id")}
    )
    player2: Optional[Player] = field(
        metadata={"sa": relationship(Player, uselist=False, primaryjoin="Team.player2_id == Player.id")}
    )


@mapper_registry.mapped
@dataclass
class MatchSet:
    __tablename__ = "sets"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    match_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("matches.id"))})
    team1_score: int = field(metadata={"sa": sa.Column(sa.Integer)})
    team2_score: int = field(metadata={"sa": sa.Column(sa.Integer)})
    order: int = field(metadata={"sa": sa.Column(sa.Integer)})


@mapper_registry.mapped
@dataclass
class Match:
    __tablename__ = "matches"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    competition_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("competitions.id"))})
    team1_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("teams.id"))})
    team2_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("teams.id"))})
    order: int = field(metadata={"sa": sa.Column(sa.Integer)})
    forfeit: bool = field(metadata={"sa": sa.Column(sa.Boolean)})
    team1_max_sets: Optional[int] = field(metadata={"sa": sa.Column(sa.Integer, nullable=True)})
    team2_max_sets: Optional[int] = field(metadata={"sa": sa.Column(sa.Integer, nullable=True)})

    team1: Team = field(
        metadata={"sa": relationship(Team, uselist=False, primaryjoin="Match.team1_id == Team.id")},
    )
    team2: Team = field(
        metadata={"sa": relationship(Team, uselist=False, primaryjoin="Match.team2_id == Team.id")},
    )
    sets: list[MatchSet] = field(default_factory=list, metadata={"sa": relationship(MatchSet)})


@unique
class CompetitionType(Enum):
    AD = 'ad'
    NS = 'ns'
    SPS = 'sps'
    ND = 'nd'
    SPD = 'spd'
    AS = 'as'
    OS = 'os'
    OD = 'od'
    BD = 'bd'
    BS = 'bs'
    MD = 'md'
    PRO_AM = 'pro-am'
    WD = 'wd'
    WS = 'ws'
    COD = 'cod'
    JS = 'js'
    JD = 'jd'


@mapper_registry.mapped
@dataclass
class Competition:
    __tablename__ = "competitions"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    tournament_id: int = field(metadata={"sa": sa.Column(sa.ForeignKey("tournaments.id"))})
    type: CompetitionType = field(metadata={"sa": sa.Enum(CompetitionType)})
    name: Optional[str] = field(metadata={"sa": sa.Column(sa.String(255), nullable=True)})
    date: datetime = field(metadata={"sa": sa.Column(sa.Date)})
    order: int = field(metadata={"sa": sa.Column(sa.Integer)})
    importance: float = field(metadata={"sa": sa.Column(sa.Float)})
    accumulative: Optional[float] = field(metadata={"sa": sa.Column(sa.Float, nullable=True)})
    disable: Optional[bool] = field(metadata={"sa": sa.Column(sa.Float, nullable=True)})

    teams: list[Team] = field(default_factory=list, metadata={"sa": relationship(Team)})
    matches: list[Match] = field(default_factory=list, metadata={"sa": relationship(Match)})


@mapper_registry.mapped
@dataclass
class Tournament:
    __tablename__ = "tournaments"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": sa.Column(sa.Integer, primary_key=True)})
    name: str = field(metadata={"sa": sa.Column(sa.String(255))})

    competitions: list[Competition] = field(
        default_factory=list,
        metadata={"sa": relationship(Competition)},
    )
