from .db.conexion import create_tables_and_db
from fastapi import FastAPI, Depends
from .entities import *
from fastapi.middleware.cors import CORSMiddleware
from .api import registrar_routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(numero_router.numero_router, prefix="/api")

registrar_routers(app=app)


# @app.on_event("startup")
# def on_startup():
#     # create_tables_and_db()
#     pass
