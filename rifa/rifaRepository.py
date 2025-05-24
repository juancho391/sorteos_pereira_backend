from ..db.conexion import session_dependency
from .models import RifaCreate
from ..entities.Rifa import Rifa
from sqlmodel import select
from fastapi import Depends
from typing import Annotated


class RifaRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_rifa(self, rifa: RifaCreate):
        nueva_rifa = Rifa.model_validate(rifa)
        self.session.add(nueva_rifa)
        self.session.commit()
        self.session.refresh(nueva_rifa)
        return nueva_rifa

    def obtener_rifas(self):
        # Obtenemos las rifas con el numero de boletas que se han vendido haciendo un join entre rifa y boleta
        return self.session.exec(select(Rifa)).all()

    def obtener_rifa_activa(self):
        return self.session.exec(select(Rifa).where(Rifa.is_active == True)).first()

    def obtener_rifas_activas(self):
        return self.session.exec(select(Rifa).where(Rifa.is_active == True)).all()

    def obtener_rifa_id(self, rifa_id: int):
        rifa = self.session.get(Rifa, rifa_id)
        return rifa

    def actualizar_rifa(self, rifa: Rifa):
        self.session.add(rifa)
        self.session.commit()
        self.session.refresh(rifa)
        return rifa


def get_rifa_repository(session_dependency: session_dependency):
    return RifaRepository(session=session_dependency)


rifa_repository_dependency = Annotated[RifaRepository, Depends(get_rifa_repository)]
