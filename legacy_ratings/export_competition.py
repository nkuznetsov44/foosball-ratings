import asyncio
from decimal import Decimal
from sqlalchemy import select

from common.entities.player import Player
from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
    CompetitionTeam,
    CompetitionMatch,
    CompetitionMatchSet,
)
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.client import CoreClientContext

from legacy_ratings.engine import ratings_session
from legacy_ratings.model import Competition
from legacy_ratings.adapters import (
    competition_type_adapter,
    date_to_tz_aware_datetime,
)


async def get_core_players(host, port):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.get_players()


def get_core_players_sync(host="localhost", port=8080) -> list[Player]:
    return asyncio.run(get_core_players(host, port))


async def send_core_request(request: CreateCompetitionRequest, host: str, port: int):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.create_competition(request)


def send_core_request_sync(
    request: CreateCompetitionRequest,
    host: str = "localhost",
    port: int = 8080,
) -> RatingsStateResponse:
    return asyncio.run(send_core_request(request, host, port))


def create_competition_request(core_tournament_id, competition_id):
    core_players = get_core_players_sync()
    player_ids_map = {player.external_id: player.id for player in core_players}

    stmt = select(Competition).where(Competition.id == competition_id)
    with ratings_session() as session:
        competition: Competition = session.execute(stmt).scalar_one()
        return CreateCompetitionRequest(
            tournament_id=core_tournament_id,
            external_id=competition.id,
            competition_type=competition_type_adapter(competition.type),
            evks_importance=Decimal(competition.importance).quantize(Decimal("1.00")),
            start_datetime=date_to_tz_aware_datetime(competition.date),
            end_datetime=date_to_tz_aware_datetime(competition.date),
            teams=[
                CompetitionTeam(
                    external_id=team.id,
                    competition_place=team.position,
                    first_player_id=player_ids_map[team.player1_id],
                    second_player_id=player_ids_map[team.player2_id]
                    if team.player2_id is not None
                    else None,
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
                for match in sorted(competition.matches, key=lambda m: m.order)
            ],
        )


def get_tournament_competition_ids(legacy_tournament_id) -> list[int]:
    stmt = (
        select(Competition.id)
        .where(Competition.tournament_id == legacy_tournament_id)
        .order_by(Competition.order.asc())
    )
    with ratings_session() as session:
        return [row[0] for row in session.execute(stmt).all()]


def main():
    core_tournament_id = 2
    legacy_tournament_id = 2
    for competition_id in get_tournament_competition_ids(legacy_tournament_id):
        print(f"Importing competition with external_id={competition_id}")
        request = create_competition_request(core_tournament_id, competition_id)
        send_core_request_sync(request)
        print(
            f"Imported {request.competition_type} with "
            f"external_id={request.competition_type.id}"
        )


if __name__ == "__main__":
    main()
