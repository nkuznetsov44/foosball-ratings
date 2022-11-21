import asyncio
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerRequest
from common.interactions.core.client import CoreClientContext
from common.entities.enums import City
from common.entities.player import Player as CorePlayer

from legacy_ratings.secrets import DB_USER, DB_PASSWORD
from legacy_ratings.model import Player


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


async def send_core_request(request: CreatePlayersRequest, host: str, port: int):
    async with CoreClientContext(host=host, port=port) as client:
        return await client.create_players(request)


def send_core_request_sync(
    request: CreatePlayersRequest,
    host: str = "localhost",
    port: int = 8080,
) -> list[CorePlayer]:
    return asyncio.run(send_core_request(request, host, port))


def create_request():
    engine = create_ratings_engine(DB_USER, DB_PASSWORD)
    with sessionmaker(bind=engine)() as session:
        players: list[Player] = session.execute(select(Player)).scalars().all()
        player_requests = []
        for player in players:
            player_requests.append(
                PlayerRequest(
                    external_id=player.id,
                    first_name=player.first_name,
                    last_name=player.last_name,
                    city=City.MOSCOW,  # FIXME
                    is_foreigner=player.foreigner,
                    initial_evks_rating=player.evks_initial_rating,
                    initial_matches_played=player.evks_initial_matches_count,
                    initial_matches_won=player.evks_initial_matches_win,
                )
            )
        return CreatePlayersRequest(players=player_requests)


def main():
    request = create_request()
    send_core_request_sync(request)
    print("Imported players")


if __name__ == "__main__":
    main()
