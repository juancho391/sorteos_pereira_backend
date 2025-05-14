from fastapi import APIRouter
from schemas.Rifa_schema import Rifa
from schemas.Numero_schemna import Numero_especial
from services.Rifa_service import RifaService
from db.conexion import session_dependency
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.Boleta_schema import BoletaConsulta
from schemas.User_schema import UserResponse ,UserAdminLogin
from services import user_services

router_rifa = APIRouter()

@router_rifa.put("/rifa/{id}/desactivar")
def finalizar_rifa(id: int, session: session_dependency):
    try:
        rifa_finalazada = RifaService(session=session).finalizar_rifa(id=id)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Rifa finalizada con exito",
                "rifa": jsonable_encoder(rifa_finalazada),
            },
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@router_rifa.get("/rifa")
def obtener_rifas(session: session_dependency):
    try:
        rifas = RifaService(session=session).obtener_rifas()
        return JSONResponse(
            status_code=200,
            content={
                "message": "Rifas obtenidas con exito",
                "rifas": jsonable_encoder(rifas),
            },
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@router_rifa.post("/rifa/numero_especial")
def crear_numero_especial(
    numero_especial: Numero_especial, session: session_dependency
):
    try:
        numero_creado = RifaService(session=session).agregar_numero_especial(
            numero_especial=numero_especial
        )
        return JSONResponse(
            status_code=201,
            content={
                "message": "Numero especial creado con exito",
                "numero": jsonable_encoder(numero_creado),
            },
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@router_rifa.post("/rifa/ganador", response_model=UserResponse)
def obtener_ganador(
    boleta: BoletaConsulta,
    session: session_dependency,
):
    try:
        ganador = RifaService(session=session).obtener_ganador(boleta=boleta)
        return ganador
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

