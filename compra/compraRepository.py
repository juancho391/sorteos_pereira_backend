from ..db.conexion import session_dependency
from .models import CompraCreate
from ..entities.Compra import Compra
from typing import Annotated
from fastapi import Depends


class CompraRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_compra(self, compra: CompraCreate):
        nueva_compra = Compra.model_validate(compra)
        self.session.add(nueva_compra)
        self.session.commit()
        self.session.refresh(nueva_compra)
        return nueva_compra


def get_compra_repository(session: session_dependency):
    return CompraRepository(session=session)


compra_repository_depedency = Annotated[
    CompraRepository, Depends(get_compra_repository)
]
