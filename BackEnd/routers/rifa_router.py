from fastapi import APIRouter
from db.conexion import session_dependency
from models.rifa_service import RifaService
from schemas.Rifa_schema import Rifa

rifa_router = APIRouter()


@rifa_router.post("/rifas")
def crear_rifa(rifa: Rifa, session: session_dependency):
    return RifaService(session=session).crear_rifa(rifa=rifa)
