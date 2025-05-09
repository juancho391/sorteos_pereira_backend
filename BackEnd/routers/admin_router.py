from fastapi import APIRouter, Depends
from schemas.Rifa_schema import Rifa
from models.rifa_model import RifaService
from db.conexion import session_dependency
from fastapi.responses import JSONResponse

admin_router = APIRouter()


# Endpoint para iniciar sesion como admin
@admin_router.post("/login")
def loginAdmin():
    pass


# Ednpoint para crear rifa
@admin_router.post("/rifa")
def crear_rifa(rifa: Rifa, session: session_dependency):
    return RifaService(session=session).crear_rifa(rifa=rifa)


@admin_router.put("rifa/{id}")
def finalizar_rifa(id: int, session: session_dependency):
    return RifaService(session=session).finalizar_rifa(id=id)
