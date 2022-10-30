from decimal import Decimal
from sqlalchemy import select

from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
    CompetitionTeam,
    CompetitionMatch,
    CompetitionMatchSet,
)
from common.interactions.core.requests.schemas import CreateCompetitionRequestSchema

from storage.legacy_ratings.engine import ratings_session
from storage.legacy_ratings.model import Competition
from storage.legacy_ratings.adapters import (
    competition_type_adapter,
    date_to_tz_aware_datetime,
)


def main():
    tournament_id = 1  # internal id
    competition_id = 1
    stmt = select(Competition).where(Competition.id == competition_id)
    with ratings_session() as session:
        competition: Competition = session.execute(stmt).scalar_one()
        request = CreateCompetitionRequest(
            tournament_id=tournament_id,
            external_id=competition.id,
            competition_type=competition_type_adapter(competition.type),
            evks_importance=Decimal(competition.importance).quantize(Decimal("1.00")),
            start_datetime=date_to_tz_aware_datetime(competition.date),
            end_datetime=date_to_tz_aware_datetime(competition.date),
            teams=[
                CompetitionTeam(
                    external_id=team.id,
                    competition_place=team.position,
                    first_player_id=team.player1_id,  # FIXME: this is external id
                    second_player_id=team.player2_id,  # FIXME: this is external id
                )
                for team in competition.teams
            ],
            matches=[
                CompetitionMatch(
                    external_id=match.id,
                    first_team_external_id=match.team1_id,
                    second_team_external_id=match.team2_id,
                    force_qualification=False,
                    start_datetime=date_to_tz_aware_datetime(competition.date),
                    end_datetime=date_to_tz_aware_datetime(competition.date),
                    sets=[
                        CompetitionMatchSet(
                            external_id=mset.id,
                            order=mset.order,
                            first_team_score=mset.team1_score,
                            second_team_score=mset.team2_score,
                        )
                        for mset in match.sets
                    ],
                )
                for match in competition.matches
            ],
        )
    request_data = CreateCompetitionRequestSchema().dumps(request)
    print(request_data)


if __name__ == "__main__":
    main()
