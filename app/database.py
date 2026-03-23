from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import get_settings

settings = get_settings()

# SQLAlchemy 2.x requires "postgresql://" — Render provides "postgres://"
db_url = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    metadata = MetaData(schema="rick_and_morty")
