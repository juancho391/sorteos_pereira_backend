from db.conexion import create_tables_and_db
from routers import user_router, rifa_router
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from typing import Annotated
from schemas.User_schema import Users
from schemas.Rifa_schema import Rifa
from schemas.Boleta_schema import Boleta
from schemas.Numero_schemna import Numero_especial

app = FastAPI()

# app.include_router(numero_router.numero_router, prefix="/api")
app.include_router(user_router.user_router, prefix="/api")
app.include_router(rifa_router.rifa_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    create_tables_and_db()


# def create_user(user: Users, session=Session(con.engine)):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# def get_users(session=Session(con.engine)):
#     statement = select(Users)
#     users = session.exec(statement).all()
#     return users


# usuario1 = Users(
#     cedula="12345678",
#     email="jorge@hotmail.com",
#     nombre="jorge",
#     direccion="calle 12",
#     celular=12345678,
# )


# create_user(usuario1)
# print(get_users())
