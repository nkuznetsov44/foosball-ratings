from sqlalchemy import create_engine

from storage.tables import metadata_obj


def create_schema(engine):
    metadata_obj.create_all(engine)


if __name__ == "__main__":
    engine = create_engine(
        "postgresql://ratings:ratings@localhost:5432/ratings_core", echo=True
    )
    create_schema(engine)
    print("Created schema")
