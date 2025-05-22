from ..db.conexion import session_dependency
from .models import NumeroEspecialCreate
from fastapi import Depends
from typing import Annotated
from ..entities.Numero import Numero_especial
from sqlmodel import select
from ..entities.Rifa import Rifa


class NumeroRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_numero(self, numero: NumeroEspecialCreate) -> Numero_especial:
        nuevo_numero = Numero_especial.model_validate(numero)
        self.session.add(nuevo_numero)
        self.session.commit()
        self.session.refresh(nuevo_numero)
        return nuevo_numero

    def obtener_numeros(self) -> list[Numero_especial]:
        return self.session.exec(select(Numero_especial)).all()

    def obtener_numero_id(self, numero_id: int) -> Numero_especial:
        return self.session.get(Numero_especial, numero_id)

    def obtener_numeros_rifa(self, rifa_activa: Rifa) -> list[int]:
        print("Obtener numeros rifa : NumeroRepository")
        return self.session.exec(
            select(Numero_especial.numero).where(
                Numero_especial.id_rifa == rifa_activa.id
            )
        ).all()


def get_numero_repository(session: session_dependency):
    return NumeroRepository(session=session)


numero_repository_dependency = Annotated[
    NumeroRepository, Depends(get_numero_repository)
]
