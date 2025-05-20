from ..db.conexion import session_dependency
from ..exceptions import (
    RifaCreationError,
    BoletaNotFoundError,
    UserNotFoundError,
    RifaNotFoundError,
)
from sqlmodel import select
from . import models
from ..entities.Rifa import Rifa
from ..entities.Boleta import Boleta
from ..entities.User import Users
from ..numeros.service import obtener_numero_boletas_vendidas


def obtener_rifas(session: session_dependency):
    rifas = session.exec(select(Rifa)).all()
    if not rifas:
        raise ValueError("No se encontraron rifas")
    return rifas


def crear_rifa(session: session_dependency, rifa: models.RifaCreate):
    try:
        nueva_rifa = Rifa.model_validate(rifa)
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


def obtener_ganador(session: session_dependency, boleta: models.BoletaConsulta):
    boleta_obtenida = session.exec(
        select(Boleta).where(
            Boleta.numero == boleta.numero, Boleta.id_rifa == boleta.id_rifa
        )
    ).first()
    if not boleta_obtenida:
        raise BoletaNotFoundError(numero=boleta.numero)
    usuario = session.exec(
        select(Users).where(Users.id == boleta_obtenida.id_usuario)
    ).first()
    if not usuario:
        raise UserNotFoundError()
    return usuario


def obtener_rifa_activa_numeros_espciales(session: session_dependency):
    rifa = session.exec(select(Rifa).where(Rifa.is_active == True)).first()
    if not rifa:
        raise RifaNotFoundError()
    boletas_vendidas = obtener_numero_boletas_vendidas(session=session, id_rifa=rifa.id)
    rifa_response = models.RifaResponse(
        id=rifa.id,
        premio=rifa.premio,
        tipo=rifa.tipo,
        is_active=rifa.is_active,
        fecha_inicio=rifa.fecha_inicio,
        fecha_fin=rifa.fecha_fin,
        image_premio=rifa.image_premio,
        precio=rifa.precio,
        numeros_especiales=rifa.numeros_especiales,
        boletas_vendidas=boletas_vendidas,
    )

    return rifa_response


def verificar_rifas_activas(session: session_dependency):

    rifas = session.exec(select(Rifa).where(Rifa.is_active == True)).all()

    return True if len(rifas) > 1 else False
