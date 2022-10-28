import json
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
from common.entities.enums import City

from storage.legacy_ratings.secrets import DB_USER, DB_PASSWORD
from storage.legacy_ratings.model import Tournament


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


def main():
    stmt = select(Tournament).where(Tournament.id == 1)
    engine = create_ratings_engine(DB_USER, DB_PASSWORD)
    with sessionmaker(bind=engine)() as session:
        tournament = session.execute(stmt).scalar_one()
        print(tournament)


if __name__ == "__main__":
    main()
