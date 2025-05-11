from fastapi import APIRouter
from db.conexion import session_dependency
from services.Rifa_service import RifaService
from schemas.Rifa_schema import RifaResponse


main_router = APIRouter()


@main_router.get("/rifa")
def obtener_rifa(session: session_dependency):
    try:
        rifa = RifaService(session=session).obtener_rifa_activa_con_numeros_especiales()
        return rifa
    except ValueError as e:
        return {"message": str(e)}
