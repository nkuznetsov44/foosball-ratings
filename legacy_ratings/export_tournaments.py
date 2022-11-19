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


def export_tournaments(city: City = City.MOSCOW):
    stmt = select(Tournament)
    with ratings_session() as session:
        tournaments: list[Tournament] = session.execute(stmt).scalars().all()
        for tournament in tournaments:
            request = CreateTournamentRequest(
                external_id=tournament.id,
                city=city,
                name=tournament.name,
                url=None,
            )
            core_tournament = send_core_request_sync(request)
            print(f"Imported tournament {core_tournament}")


def main():
    export_tournaments()


if __name__ == "__main__":
    main()
