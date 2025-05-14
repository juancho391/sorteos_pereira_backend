from fastapi import APIRouter
from . import service
from ..entities.Numero import Numero_especial
from . import models
from ..db.conexion import session_dependency
from ..auth.service import Usuario_actual

router_numero_especial = APIRouter(tags=["Numero especial"])

# Endpoint para crear numero especial


@router_numero_especial.post("/")
def crear_numero_especial(
    numero_especial: models.NumeroEspecialCreate, sesesion: session_dependency
):
    return service.crear_numero_especial(
        numero_especial=numero_especial, session=sesesion
    )


# Endpoint para eliminar un numero especial


@router_numero_especial.delete("/{numero}/{id_rifa}")
def eliminar_numero_especial(numero: int, id_rifa: int, sesesion: session_dependency):
    return service.eliminar_numero_especial(
        numero=numero, session=sesesion, id_rifa=id_rifa
    )
