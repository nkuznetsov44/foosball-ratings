import json
from sqlalchemy import create_engine, text
from storage.legacy_ratings.secrets import DB_USER, DB_PASSWORD

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerReq
from common.interactions.core.requests.schemas import CreatePlayersRequestSchema
from common.entities.enums import City


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


def main():
    engine = create_ratings_engine(DB_USER, DB_PASSWORD)
    with engine.connect() as connection:
        result = connection.execute(text(
            "select"
            "   id,"
            "   first_name,"
            "   last_name,"
            "   evks_initial_rating,"
            "   evks_initial_matches_count,"
            "   evks_initial_matches_win "
            "from players"
        ))
        player_reqs = []
        for player in result:
            player_reqs.append(
                PlayerReq(
                    external_id=player["id"],
                    first_name=player["first_name"],
                    last_name=player["last_name"],
                    city=City.MOSCOW,  # FIXME
                    initial_evks_rating=player["evks_initial_rating"],
                    initial_matches_played=player["evks_initial_matches_count"],
                    initial_matches_won=player["evks_initial_matches_win"],
                )
            )
        request = CreatePlayersRequest(player_reqs)
        request_data = CreatePlayersRequestSchema().dump(request)
        request_json = json.dumps(request_data, indent=4, ensure_ascii=False)
        print(request_json)


if __name__ == "__main__":
    main()
