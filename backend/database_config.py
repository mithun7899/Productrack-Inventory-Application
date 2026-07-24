from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://mithun:12345678@localhost:5432/productrack"

engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)