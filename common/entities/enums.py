from enum import Enum, unique


@unique
class City(Enum):
    MOSCOW = "Moscow"
    SAINT_PETERSBURG = "SaintPeresburg"
    KALININGRAD = "Kaliningrad"
    NOVOSIBIRSK = "Novosibirsk"
    TOMSK = "Tomsk"
    EKATERINBURG = "Ekaterinburg"
    YAROSLAVL = "Yaroslavl"
    TULA = "Tula"


@unique
class RatingType(Enum):
    EVKS = "EVKS"
    CUMULATIVE = "Cumulative"


@unique
class CompetitionType(Enum):
    OS = "Open Singles"
    OD = "Open Dobules"
    WS = "Women Singles"
    WD = "Women Doubles"
    MS = "Men Singles"
    MD = "Men Doubles"
    AS = "Amateur Singles"
    AD = "Amateur Doubles"
    NS = "Novice Singles"
    ND = "Novice Doubles"
    SPS = "Semi-pro Singles"
    SPD = "Semi-pro Doubles"
    BS = "Beginner Singles"
    BD = "Beginner Doubles"
    JS = "Junior Singles"
    JD = "Junior Doubles"
    COD = "Classic Open Doubles"
    MIXED = "Mixed Doubles"
    PROAM = "Pro-Am"


@unique
class EvksPlayerRank(Enum):
    BEGINNER = "Beginner"
    NOVICE = "Novice"
    AMATEUR = "Amateur"
    SEMIPRO = "Semipro"
    PRO = "Pro"
    MASTER = "Master"


@unique
class RatingsStateStatus(Enum):
    PUBLISHED = "Published"
    READY_TO_PUBLISH = "ReadyToPublish"
    ROLLED_BACK = "RolledBack"
