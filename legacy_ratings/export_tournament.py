import asyncio
from sqlalchemy import select

from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.client import CoreClientContext
from common.entities.enums import City
from common.entities.tournament import Tournament as CoreTournament

from legacy_ratings.engine import ratings_session
from legacy_ratings.model import Tournament


async def send_core_request(request: CreateTournamentRequest, host: str, port: int):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.create_tournament(request)


def send_core_request_sync(
    request: CreateTournamentRequest,
    host: str = "localhost",
    port: int = 8080,
) -> CoreTournament:
    return asyncio.run(send_core_request(request, host, port))


def export_tournament(tournament_id: int, city: City = City.MOSCOW) -> CoreTournament:
    stmt = select(Tournament).where(Tournament.id == tournament_id)
    with ratings_session() as session:
        tournament: Tournament = session.execute(stmt).scalar_one()
        request = CreateTournamentRequest(
            external_id=tournament.id,
            city=City.MOSCOW,  # FIXME
            name=tournament.name,
            url=None,
        )
    return send_core_request_sync(request)


def main():
    tournament_id = 1
    tournament = export_tournament(tournament_id)
    print(f"Imported tournament {tournament}")


if __name__ == "__main__":
    main()
