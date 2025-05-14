from sqlmodel import select
from . import models
from ..db.conexion import session_dependency
from ..entities.Numero import Numero_especial
from ..exceptions import (
    NumeroEspecialCreationError,
    NumeroEspecialNotFoundError,
    NumeroEspecialDeleteError,
)


def obtener_numeros_especiales(session: session_dependency):
    numeros_especiales = session.exec(select(Numero_especial)).all()
    return numeros_especiales


def crear_numero_especial(
    numero_especial: models.NumeroEspecialCreate, session: session_dependency
):
    try:
        numeros_especiales_existentes = obtener_numeros_especiales(session=session)
        for numero_especial_existente in numeros_especiales_existentes:
            if (
                numero_especial_existente.numero == numero_especial.numero
                and numero_especial_existente.id_rifa == numero_especial.id_rifa
            ):
                raise NumeroEspecialCreationError(
                    error=f"Ya existe un numero especial {numero_especial.numero} en la rifa con id {numero_especial.id_rifa}"
                )
        nuevo_numero_especial = Numero_especial(**numero_especial.model_dump())
        session.add(nuevo_numero_especial)
        session.commit()
        session.refresh(nuevo_numero_especial)
        return nuevo_numero_especial
    except Exception as e:
        raise NumeroEspecialCreationError(error=str(e))


def obtener_numero_especial(id: int, session: session_dependency):
    numero_especial = session.exec(
        select(Numero_especial).where(Numero_especial.id == id)
    ).first()
    if Numero_especial is None:
        raise NumeroEspecialNotFoundError(id=id)

    return numero_especial


def cambiar_disponibilidad_numero_especial(
    numero_especial: Numero_especial, session: session_dependency, disponible: bool
):
    try:
        numero_especial_db = obtener_numero_especial(
            id=numero_especial.id, session=session
        )
        if not numero_especial_db:
            raise NumeroEspecialNotFoundError(id=numero_especial.id)
        numero_especial_db.disponible = disponible
        session.add(numero_especial_db)
        session.commit()
        session.refresh(numero_especial_db)
        return numero_especial_db
    except Exception as e:
        raise NumeroEspecialCreationError(error=str(e))


def eliminar_numero_especial(numero: int, id_rifa: int, session: session_dependency):
    try:
        numero_especial_db = session.exec(
            select(Numero_especial).where(
                Numero_especial.id_rifa == id_rifa, Numero_especial.numero == numero
            )
        ).first()
        if not numero_especial_db:
            raise NumeroEspecialDeleteError(error="El numero especial no existe")
        session.delete(numero_especial_db)
        session.commit()
        return True
    except Exception as e:
        raise NumeroEspecialDeleteError(error=str(e))
