from sqlalchemy import create_engine

from storage.tables import metadata_obj


DB_HOST = 'localhost'
DB_PORT = 6432


def create_schema(engine):
    metadata_obj.create_all(engine)


if __name__ == "__main__":
    engine = create_engine(f"postgresql://ratings:ratings@{DB_HOST}:{DB_PORT}/ratings_core", echo=True)
    create_schema(engine)
    print("Created schema")
