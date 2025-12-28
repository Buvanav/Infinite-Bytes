# database.py
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine  # ✅ need these imports

sqlite_file_name = "finbridge.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    from models import Worker  # ensure models are imported/registered
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
