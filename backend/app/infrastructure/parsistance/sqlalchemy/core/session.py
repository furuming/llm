from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )

    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )