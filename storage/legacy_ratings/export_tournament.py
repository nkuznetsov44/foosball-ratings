from decimal import Decimal
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from common.interactions.core.requests.tournament import (
    TeamReq,
    MatchSetReq,
    MatchReq,
    CompetitionReq,
    CreateTournamentRequest,
)
from common.interactions.core.requests.schemas import CreateTournamentRequestSchema
from common.entities.enums import City, CompetitionType

from storage.legacy_ratings.secrets import DB_USER, DB_PASSWORD
from storage.legacy_ratings.model import (
    Tournament,
    CompetitionType as LegacyCompetitionType
)


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


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


def main():
    stmt = select(Tournament).where(Tournament.id == 1)
    engine = create_ratings_engine(DB_USER, DB_PASSWORD)
    with sessionmaker(bind=engine)() as session:
        tournament: Tournament = session.execute(stmt).scalar_one()
        request = CreateTournamentRequest(
            external_id=tournament.id,
            city=City.MOSCOW,
            name=tournament.name,
            evks_importance=Decimal('0.75'),
            url=None,
            competitions=[
                CompetitionReq(
                    external_id=competition.id,
                    competition_type=competition_type_adapter(competition.type),
                    start_datetime=competition.date,
                    end_datetime=competition.date,
                    teams=[
                        TeamReq(
                            external_id=team.id,
                            competition_place=team.position,
                            first_player_id=team.player1_id,
                            second_player_id=team.player2_id,
                        )
                        for team in competition.teams
                    ],
                    matches=[
                        MatchReq(
                            external_id=match.id,
                            first_team_external_id=match.team1_id,
                            second_team_external_id=match.team2_id,
                            force_qualification=False,
                            start_datetime=competition.date,
                            end_datetime=competition.date,
                            sets=[
                                MatchSetReq(
                                    external_id=mset.id,
                                    order=mset.order,
                                    first_team_score=mset.team1_score,
                                    second_team_score=mset.team2_score,
                                )
                                for mset in match.sets
                            ]
                        )
                        for match in competition.matches
                    ],
                )
                for competition in tournament.competitions
            ]
        )
    request_data = CreateTournamentRequestSchema().dumps(request)
    print(request_data)


if __name__ == "__main__":
    main()
