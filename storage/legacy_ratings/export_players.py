from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerRequest
from common.interactions.core.requests.schemas import CreatePlayersRequestSchema
from common.entities.enums import City

from storage.legacy_ratings.secrets import DB_USER, DB_PASSWORD
from storage.legacy_ratings.model import Player


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


def main():
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
                    initial_evks_rating=player.evks_initial_rating,
                    initial_matches_played=player.evks_initial_matches_count,
                    initial_matches_won=player.evks_initial_matches_win,
                )
            )
        request = CreatePlayersRequest(players=player_requests)
        request_data = CreatePlayersRequestSchema().dumps(request)
        print(request_data)


if __name__ == "__main__":
    main()
