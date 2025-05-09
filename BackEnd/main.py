from db.conexion import create_tables_and_db
from routers import main_router, admin_router
from fastapi import FastAPI, Depends
from schemas.User_schema import Users
from schemas.Rifa_schema import Rifa
from schemas.Boleta_schema import Boleta
from schemas.Numero_schemna import Numero_especial

app = FastAPI()

# app.include_router(numero_router.numero_router, prefix="/api")
app.include_router(admin_router.rifa_router, prefix="/api/admin")
app.include_router(main_router.user_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    create_tables_and_db()
