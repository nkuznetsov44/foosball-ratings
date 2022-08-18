from sqlalchemy import create_engine
from core.storage.mapping import mapper_registry

from core.entities.player import Player  # noqa
from core.entities.match import Match, Team, MatchSet  # noqa


if __name__ == "__main__":
    engine = create_engine("postgresql://ratings:ratings@localhost:5432/ratings_core")
    mapper_registry.metadata.create_all(engine)
    print("Created schema")