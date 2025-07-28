import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()


db_user = os.getenv("DATABASE_USER")
db_password = os.getenv("DATABASE_PASSWORD")
db_port = os.getenv("DATABASE_PORT")
db_host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
ambiente = os.getenv("AMBIENTE")

sqlite_name = "db_test.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

if ambiente == "test":
    db_url = sqlite_url


def get_engine(db_url: str = db_url):
    return create_engine(db_url)


def create_tables_and_db():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session


session_dependency = Annotated[Session, Depends(get_session)]
