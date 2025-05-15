from ..db.conexion import session_dependency
from ..exceptions import RifaCreationError
from sqlmodel import select
from . import models
from ..entities.Rifa import Rifa
from .. entities.Numero import Numero_especial


def obtener_rifas(session: session_dependency):

    rifas = session.exec(select(Rifa)).all()
    if not rifas:
        raise ValueError("No se encontraron rifas")
    return rifas

def crear_rifa(session: session_dependency, rifa: models.RifaCreate):
    try:
        nueva_rifa = Rifa(**rifa.model_dump())
        session.add(nueva_rifa)
        session.commit()
        session.refresh(nueva_rifa)
        return nueva_rifa
    except Exception as e:
        raise RifaCreationError(error=str(e))

def finalizar_rifa(session: session_dependency, id: int):
    rifa = session.get(Rifa.Rifa, id)
    if not rifa and rifa.is_active == False:
        raise ValueError("No se pudo finalizar la rifa")
    rifa.is_active = False
    session.add(rifa)
    session.commit()
    session.refresh(rifa)
    return rifa


# def obtener_ganador(session: session_dependency, boleta: models.BoletaConsulta):
#     boleta_obtenida = session.get(entities.Boleta, boleta.id)
#     if not boleta_obtenida:
#         raise ValueError(
#             f"No se encontro la boleta con el numero {boleta.numero} y rifa {boleta.id_rifa}"
#         )
#     # Deuda tecnica
#     usuario = session.exec(
#         select(entities.User).where(entities.User.id == boleta_obtenida.id_usuario)
#     ).first()
#     if not usuario:
#         raise ValueError(
#             f"No se encontro el usuario con el id {boleta_obtenida.id_usuario}"
#         )
#     return usuario


def obtener_rifa_activa_numeros_espciales(session: session_dependency):
    rifa = session.exec(select(Rifa).where(Rifa.is_active == True)).first()
    if not rifa:
        raise ValueError("No se encontro una rifa activa")

    numeros_especiales = session.exec(select(Numero_especial).where(Numero_especial.id_rifa == rifa.id)).all()
    numeros = [
        models.Numero_especial(**n.model_dump())
        for n in numeros_especiales
    ]

    print(numeros_especiales)
    print(rifa)
    rifa = models.RifaResponse(
        id=rifa.id,
        premio=rifa.premio,
        tipo=rifa.tipo,
        precio=rifa.precio,
        is_active=rifa.is_active,
        fecha_inicio=rifa.fecha_inicio,
        fecha_fin=rifa.fecha_fin,
        image_premio=rifa.image_premio,
        numeros_especiales=numeros,
    )

    return rifa
