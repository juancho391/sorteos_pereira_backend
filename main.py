from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.conexion import create_tables_and_db

from .api import registrar_routers
from .entities import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


registrar_routers(app=app)


# @app.on_event("startup")
# def on_startup():
#     create_tables_and_db()
