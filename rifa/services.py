from db.conexion import session_dependency
from entities.Rifa import Rifa
from sqlmodel import select
from . import models
from .. import entities

def obtener_rifas(session: session_dependency):
    rifas = session.exec(select(Rifa)).all()
    if not rifas:
        raise ValueError("No se encontraron rifas")
    list_rifas = [models.RifaResponse(rifa) for rifa in rifas]
    return models.RifaResponse(rifas)

def obtener_rifa(session: session_dependency, id: int):
    rifa = session.get(Rifa, id)
    if not rifa:
        raise ValueError(f"No se encontro la rifa con id{id}")
    return rifa

def crear_rifa(session: session_dependency, rifa: models.Rifa):

    session.add(rifa)
    session.commit()
    session.refresh(rifa)
    return models.RifaResponse(rifa)

def finalizar_rifa(session: session_dependency, id: int):
    rifa = session.get(Rifa, id)
    if not rifa and rifa.is_active == False:
        raise ValueError("No se pudo finalizar la rifa")
    rifa.is_active = False
    session.add(rifa)
    session.commit()
    session.refresh(rifa)
    return rifa

def agregar_numero_especial(session: session_dependency, numero_especial: models.Numero_especial):
    id_rifa = numero_especial.id_rifa
    rifa = session.get(Rifa, id_rifa)
    # Validamos que exista la rifa y este activa
    if not rifa or rifa.is_active == False:
        raise ValueError(f"No se pudo agregar el numero especial a la rifa con id : {id_rifa}")
    # Consultamos los numeros especiales que pertenecen a la rifa    
    numeros_especiales = session.exec(select(entities.Numero).where(entities.Numero.id_rifa == id_rifa)).all()
    # Validamos que la rifa no tenga un numero especial con el mismo numero
    for numero in numeros_especiales:
        if numero.numero == numero_especial.numero:
            raise ValueError(f"Ya existe un numero especial con el numero {numero_especial.numero}")
    session.add(numero_especial)
    session.commit()
    session.refresh(numero_especial)
    return numero_especial 
 
def obtener_ganador(session: session_dependency, boleta: models.BoletaConsulta):
    boleta_obtenida = session.get(entities.Boleta, boleta.id)
    if not boleta_obtenida:
        raise ValueError(
            f"No se encontro la boleta con el numero {boleta.numero} y rifa {boleta.id_rifa}"
        )
    # Deuda tecnica
    usuario = session.exec(
        select(entities.User).where(entities.User.id == boleta_obtenida.id_usuario)).first()
    if not usuario:
        raise ValueError(
            f"No se encontro el usuario con el id {boleta_obtenida.id_usuario}"
        )
    return usuario

def obtener_rifa_activa_numeros_espciales(session: session_dependency):
    rifa = session.exec(select(Rifa).where(Rifa.is_active == True)).first()

    if not rifa:
        raise ValueError("No se encontro una rifa activa")
    
    return rifa

