from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.legacy_ratings.secrets import DB_USER, DB_PASSWORD


def create_ratings_engine(username, password):
    return create_engine(f"mysql+pymysql://{username}:{password}@localhost/ratings")


def ratings_session():
    engine = create_ratings_engine(DB_USER, DB_PASSWORD)
    return sessionmaker(bind=engine)()
