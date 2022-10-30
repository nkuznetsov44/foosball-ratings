from datetime import date, datetime, timezone, timedelta

from common.entities.enums import CompetitionType
from storage.legacy_ratings.model import CompetitionType as LegacyCompetitionType


def competition_type_adapter(competition_type: LegacyCompetitionType) -> CompetitionType:
    return {
        LegacyCompetitionType.AD: CompetitionType.AD,
        LegacyCompetitionType.AS: CompetitionType.AS,
        LegacyCompetitionType.AD: CompetitionType.AD,
        LegacyCompetitionType.NS: CompetitionType.NS,
        LegacyCompetitionType.SPS: CompetitionType.SPS,
        LegacyCompetitionType.ND: CompetitionType.ND,
        LegacyCompetitionType.SPD: CompetitionType.SPD,
        LegacyCompetitionType.AS: CompetitionType.AS,
        LegacyCompetitionType.OS: CompetitionType.OS,
        LegacyCompetitionType.OD: CompetitionType.OD,
        LegacyCompetitionType.BD: CompetitionType.BD,
        LegacyCompetitionType.BS: CompetitionType.BS,
        LegacyCompetitionType.MD: CompetitionType.MD,
        LegacyCompetitionType.PRO_AM: CompetitionType.PROAM,
        LegacyCompetitionType.WD: CompetitionType.WD,
        LegacyCompetitionType.WS: CompetitionType.WS,
        LegacyCompetitionType.COD: CompetitionType.COD,
        LegacyCompetitionType.JS: CompetitionType.JS,
        LegacyCompetitionType.JD: CompetitionType.JD,
    }[competition_type]


def date_to_tz_aware_datetime(dt: date) -> datetime:
    return datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=timezone(timedelta(hours=+3), 'MSK'),
    )
