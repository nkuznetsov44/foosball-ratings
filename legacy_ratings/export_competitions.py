import asyncio
from decimal import Decimal
from sqlalchemy import select

from common.entities.match import GrandFinalOptions
from common.entities.player import Player as CorePlayer
from common.entities.tournament import Tournament as CoreTournament
from common.entities.ratings_state import RatingsState
from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
    CompetitionTeam,
    CompetitionMatch,
    CompetitionMatchSet,
)
from common.interactions.core.client import CoreClientContext

from legacy_ratings.engine import ratings_session
from legacy_ratings.model import Competition, Match
from legacy_ratings.adapters import (
    competition_type_adapter,
    date_to_tz_aware_datetime,
)


async def get_core_players(host, port):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.get_players()


def get_core_players_sync(host="localhost", port=8080) -> list[CorePlayer]:
    return asyncio.run(get_core_players(host, port))


async def get_core_tournaments(host, port):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.get_tournaments()


def get_core_tournaments_sync(host="localhost", port=8080) -> list[CoreTournament]:
    return asyncio.run(get_core_tournaments(host, port))


async def send_core_request(request: CreateCompetitionRequest, host: str, port: int):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.create_competition(request)


def send_core_request_sync(
    request: CreateCompetitionRequest,
    host: str = "localhost",
    port: int = 8080,
) -> RatingsState:
    return asyncio.run(send_core_request(request, host, port))


def get_grandfinal_options(match: Match) -> GrandFinalOptions:
    if match.team1_max_sets or match.team2_max_sets:
        return GrandFinalOptions(
            sets_winner_bracket=max(match.team1_max_sets, match.team2_max_sets),
            sets_looser_bracket=min(match.team1_max_sets, match.team2_max_sets),
        )


def create_competition_request(
    competition_id: int,
    core_players: list[CorePlayer],
    core_tournaments: list[CoreTournament],
) -> CreateCompetitionRequest:
    player_ids_map = {player.external_id: player.id for player in core_players}

    stmt = select(Competition).where(Competition.id == competition_id)
    with ratings_session() as session:
        competition: Competition = session.execute(stmt).scalar_one()
        core_tournament = next(
            filter(
                lambda trmt: trmt.external_id == competition.tournament_id,
                core_tournaments,
            ),
        )
        teams = [
            CompetitionTeam(
                external_id=team.id,
                competition_place=team.position,
                competition_order=team.order,
                first_player_id=player_ids_map[team.player1_id],
                second_player_id=player_ids_map[team.player2_id]
                if team.player2_id is not None
                else None,
            )
            for team in competition.teams
        ]
        matches = [
            CompetitionMatch(
                external_id=match.id,
                first_team_external_id=match.team1_id,
                second_team_external_id=match.team2_id,
                order=match.order,
                force_qualification=False,
                is_forfeit=match.forfeit,
                grand_final_options=get_grandfinal_options(match),
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
        ]
        return CreateCompetitionRequest(
            tournament_id=core_tournament.id,
            external_id=competition.id,
            competition_type=competition_type_adapter(competition.type),
            order=competition.order,
            evks_importance=Decimal(competition.importance).quantize(Decimal("1.00")),
            cumulative_coefficient=(
                Decimal(competition.accumulative).quantize(Decimal("1.00"))
                if competition.accumulative
                else Decimal("0.00")
            ),
            start_datetime=date_to_tz_aware_datetime(competition.date),
            end_datetime=date_to_tz_aware_datetime(competition.date),
            teams=teams,
            matches=matches,
        )


def get_competitions(start_date=None, start_order=None) -> list[Competition]:
    stmt = select(Competition.id)
    if start_date:
        stmt = stmt.where(Competition.date >= start_date)

    if start_order:
        stmt = stmt.where(Competition.order >= start_order)

    stmt = stmt.order_by(Competition.date.asc(), Competition.order.asc())

    with ratings_session() as session:
        return session.execute(stmt).scalars().all()


def export_competitions(competitions: list[Competition]):
    core_players = get_core_players_sync()
    core_tournaments = get_core_tournaments_sync()
    for competition_id in competitions:
        print(f"Importing competition with external_id={competition_id}")
        request = create_competition_request(
            competition_id,
            core_players,
            core_tournaments,
        )
        send_core_request_sync(request)
        print(f"Imported {request.competition_type} with external_id={request.external_id}")


def main():
    competitions = get_competitions(
        # start_date=datetime(year=2020, month=12, day=6),
        # start_order=2,
    )
    export_competitions(competitions)


if __name__ == "__main__":
    main()
