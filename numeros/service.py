from sqlmodel import select
from . import models
from ..db.conexion import session_dependency
from ..entities.Numero import Numero_especial
from ..rifa import services
from ..exceptions import (
    NumeroEspecialCreationError,
    NumeroEspecialNotFoundError,
    NumeroEspecialDeleteError,
)
import random
from ..entities import Rifa
from ..entities.Boleta import Boleta


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
        nuevo_numero_especial = Numero_especial.model_validate(numero_especial)
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


def generarNumero(
    lista_numeros: list[int],
    cantidad_numeros: int,
    lista_numeros_especiales: list[int],
    session: session_dependency,
    cantidad_comprada: int = 3,
) -> int:
    numeros_disponibles = len(lista_numeros) - cantidad_numeros
    if numeros_disponibles < cantidad_comprada:
        raise ValueError("No hay suficientes numeros disponibles para la compra")
    lista_numeros_generados = []
    contador = 0
    contador_premiados = 0
    verificar = services.verificar_rifas_activas(session=session)
    if verificar == False:
        raise ValueError("No se pueden generar numeros, hay mas de una rifa activa")
    while contador < cantidad_comprada:
        numero = random.randint(1, cantidad_numeros)
        if numero not in lista_numeros_generados and numero not in lista_numeros:
            if numero in lista_numeros_especiales and contador_premiados < 1:
                lista_numeros_generados.append(numero)
                contador_premiados += 1
                contador += 1
            else:
                lista_numeros_generados.append(numero)
                contador += 1
    return lista_numeros_generados


def obtener_lista_numeros(
    session: session_dependency, rifa_activa: Rifa.Rifa
) -> list[int]:
    numeros = session.exec(
        select(Boleta.numero).where(Boleta.id_rifa == rifa_activa.id)
    ).all()
    print(numeros)
    return numeros


def obtener_lista_numeros_especiales(
    session: session_dependency, rifa_activa: Rifa.Rifa
) -> list[int]:
    numeros = session.exec(
        select(Numero_especial.numero).where(Numero_especial.id_rifa == rifa_activa.id)
    )
    return numeros


def crear_numero(
    session: session_dependency, usuario: int, rifa: int, lista_numeros: list[int]
) -> list[Boleta]:
    boletas = [
        Boleta(numero=numero, id_rifa=rifa, id_usuario=usuario())
        for numero in lista_numeros
    ]
    session.add_all(boletas)
    session.commit()
    return boletas


# def comprar_boletas()
