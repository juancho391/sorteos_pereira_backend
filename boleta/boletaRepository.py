from ..db.conexion import session_dependency
from ..entities.Boleta import Boleta
from typing import Annotated
from fastapi import Depends
from sqlmodel import select


class BoletaRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_boleta(self, boleta: Boleta):
        nueva_boleta = Boleta.model_validate(boleta)
        self.session.add(nueva_boleta)
        self.session.commit()
        self.session.refresh(nueva_boleta)
        return nueva_boleta

    def obtener_boletas_rifa(self, id_rifa: int):
        self.session.exec(select(Boleta.numero).where(Boleta.id_rifa == id_rifa)).all()

    def crear_boletas(
        self, usuario_id: int, rifa_id: int, lista_numeros: list[int]
    ) -> list[Boleta]:
        boletas = [
            Boleta(numero=numero, id_rifa=rifa_id, id_usuario=usuario_id)
            for numero in lista_numeros
        ]
        self.session.add_all(boletas)
        self.session.commit()
        return boletas

    def obtener_boleta_numero_rifa(self, id_rifa: int, numero: int):
        boleta_obtenida = self.session.exec(
            select(Boleta).where(Boleta.numero == numero, Boleta.id_rifa == id_rifa)
        ).first()
        return boleta_obtenida


def get_boleta_repository(session: session_dependency):
    return BoletaRepository(session=session)


boleta_repository_dependency = Annotated[
    BoletaRepository, Depends(get_boleta_repository)
]
