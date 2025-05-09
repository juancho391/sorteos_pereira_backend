from fastapi import APIRouter, Depends
from schemas.Rifa_schema import Rifa
from models.rifa_service import RifaService
from db.conexion import session_dependency

admin_router = APIRouter()


# Endpoint para iniciar sesion como admin
@admin_router.post("/login")
def loginAdmin():
    pass


# Ednpoint para crear rifa
@admin_router.post("/rifas")
def crear_rifa(rifa: Rifa, session: session_dependency):
    return RifaService(session=session).crear_rifa(rifa=rifa)
