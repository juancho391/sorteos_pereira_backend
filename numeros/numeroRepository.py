from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from ..db.conexion import session_dependency
from ..entities.Numero import NumeroEspecial
from ..entities.Rifa import Rifa
from .models import NumeroEspecialCreate


class NumeroRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_numero(self, numero: NumeroEspecialCreate) -> NumeroEspecial:
        nuevo_numero = NumeroEspecial.model_validate(numero)
        self.session.add(nuevo_numero)
        self.session.commit()
        self.session.refresh(nuevo_numero)
        return nuevo_numero

    def obtener_numeros(self) -> list[NumeroEspecial]:
        return self.session.exec(select(NumeroEspecial)).all()

    def obtener_numero_id(self, numero_id: int) -> NumeroEspecial:
        return self.session.get(NumeroEspecial, numero_id)

    def obtener_numero_especial_id_rifa(self, id_rifa: int, numero: int):
        return self.session.exec(
            select(NumeroEspecial).where(
                NumeroEspecial.id_rifa == id_rifa, NumeroEspecial.numero == numero
            )
        ).first()

    def obtener_numeros_rifa(self, rifa_activa: Rifa) -> list[int]:
        return self.session.exec(
            select(NumeroEspecial.numero).where(
                NumeroEspecial.id_rifa == rifa_activa.id
            )
        ).all()

    def actualizar_numero(self, numero: int, id_rifa: int):
        numero_obtenido = self.session.exec(
            select(NumeroEspecial).where(
                NumeroEspecial.id_rifa == id_rifa, NumeroEspecial.numero == numero
            )
        ).first()
        numero_obtenido.disponible = False
        self.session.add(numero_obtenido)
        self.session.commit()
        return numero_obtenido


def get_numero_repository(session: session_dependency):
    return NumeroRepository(session=session)


numero_repository_dependency = Annotated[
    NumeroRepository, Depends(get_numero_repository)
]
