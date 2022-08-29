from sqlalchemy import create_engine

from storage.tables import metadata_obj

if __name__ == "__main__":
    engine = create_engine(
        "postgresql://ratings:ratings@localhost:5432/ratings_core", echo=True
    )
    metadata_obj.create_all(engine)
    print("Created schema")
