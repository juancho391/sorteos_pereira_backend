from fastapi import APIRouter
from . import services
from . import models
from ..db.conexion import session_dependency
from fastapi.encoders import jsonable_encoder
from ..auth import service

router_rifa = APIRouter(tags=["Rifa"])


# Ednpoint para obtener todas las rifas
@router_rifa.get("/")
def obtener_rifas(session: session_dependency, usuario_actual: service.Usuario_actual):
    return services.obtener_rifas(session=session)


# Ednpoint para crear una rifa
@router_rifa.post("/")
def crear_rifa(
    rifa: models.RifaCreate,
    session: session_dependency,
    usuario_actual: service.Usuario_actual,
):
    return services.crear_rifa(session=session, rifa=rifa)

@router_rifa.get("/activa")
def obtener_rifa(session: session_dependency, response_model=models.RifaResponse):
    return services.obtener_rifa_activa_numeros_espciales(session=session)


@router_rifa.put("/{id}/desactivar")
def finalizar_rifa(id: int, session: session_dependency, response_model=models.RifaResponse):
    return services.finalizar_rifa(session=session, id=id)



# @router_rifa.put("/rifa/{id}/desactivar")
# def finalizar_rifa(
#     id: int, session: session_dependency, usuario_actual: service.Usuario_actual
# ):
#     try:
#         rifa_finalazada = services.RifaService(session=session).finalizar_rifa(id=id)
#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "Rifa finalizada con exito",
#                 "rifa": jsonable_encoder(rifa_finalazada),
#             },
#         )
#     except ValueError as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})


# @router_rifa.post("/rifa/numero_especial")
# def crear_numero_especial(
#     numero_especial: Numero_especial, session: session_dependency
# ):
#     try:
#         numero_creado = services.RifaService(session=session).agregar_numero_especial(
#             numero_especial=numero_especial
#         )
#         return JSONResponse(
#             status_code=201,
#             content={
#                 "message": "Numero especial creado con exito",
#                 "numero": jsonable_encoder(numero_creado),
#             },
#         )
#     except ValueError as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})


# @router_rifa.post("/rifa/ganador", response_model=UserResponse)
# def obtener_ganador(
#     boleta: BoletaConsulta,
#     session: session_dependency,
# ):
#     try:
#         ganador = services.RifaService(session=session).obtener_ganador(boleta=boleta)
#         return ganador
#     except ValueError as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})
