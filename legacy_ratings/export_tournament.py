from sqlalchemy import select

from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.requests.schemas import CreateTournamentRequestSchema
from common.entities.enums import City

from legacy_ratings.engine import ratings_session
from legacy_ratings.model import Tournament


def main():
    tournament_id = 1
    stmt = select(Tournament).where(Tournament.id == tournament_id)
    with ratings_session() as session:
        tournament: Tournament = session.execute(stmt).scalar_one()
        request = CreateTournamentRequest(
            external_id=tournament.id,
            city=City.MOSCOW,  # FIXME
            name=tournament.name,
            url=None,
        )
    request_data = CreateTournamentRequestSchema().dumps(request)
    print(request_data)


if __name__ == "__main__":
    main()
