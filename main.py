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
<<<<<<< HEAD
#     # create_tables_and_db()
#     pass
=======
#     create_tables_and_db()
>>>>>>> a7283cb1e9b654b83d8400f62715692a43c676ad
