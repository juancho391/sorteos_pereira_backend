from fastapi import APIRouter, Depends
from schemas.User_schema import Users, UserResponse
from models.User_services import User_Services
from db.conexion import session_dependency

user_router = APIRouter()


@user_router.get("/users")
def obtener_users(session: session_dependency) -> list[Users]:
    return User_Services(session=session).obtener_usuarios()


@user_router.post("/crearuser", response_model=UserResponse)
def create_user(user: Users, session: session_dependency) -> Users:
    return User_Services(session=session).crear_usuario(user=user)


# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str


# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]

# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @app.post("/heroes/")
# def create_hero(hero: Hero, session: SessionDep) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero
