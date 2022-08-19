from enum import Enum


class City(Enum):
    MOSCOW = 'Moscow'
    SAINT_PETERSBURG = 'SaintPeresburg'
    KALININGRAD = 'Kaliningrad'
    NOVOSIBIRSK = 'Novosibirsk'
    TOMSK = 'Tomsk'
    EKATERINBURG = 'Ekaterinburg'
    YAROSLAVL = 'Yaroslavl'
    TULA = 'Tula'


class RatingType(Enum):
    EVKS = "EVKS"
    CUMULATIVE = "Cumulative"


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
    COD = "Classic Open Doubles"
    MIXED = "Mixed Doubles"
    PROAM = "Pro-Am"


class EvksPlayerRank(Enum):
    BEGINNER = "Beginner"
    NOVICE = "Novice"
    AMATEUR = "Amateur"
    SEMIPRO = "Semipro"
    PRO = "Pro"
    MASTER = "Master"
