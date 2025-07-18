from .db.conexion import create_tables_and_db
from fastapi import FastAPI
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


registrar_routers(app=app)


# @app.on_event("startup")
# def on_startup():
#     create_tables_and_db()
