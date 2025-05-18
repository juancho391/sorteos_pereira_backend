from fastapi import APIRouter
from . import service
from . import models
from ..db.conexion import session_dependency
from ..auth.service import Usuario_actual


router_numeros = APIRouter(tags=["Numeros"])

# Endpoint para crear numero especial


@router_numeros.post("/numero_especial")
def crear_numero_especial(
    numero_especial: models.NumeroEspecialCreate, sesesion: session_dependency
):
    return service.crear_numero_especial(
        numero_especial=numero_especial, session=sesesion
    )


@router_numeros.delete("/{numero}/{id_rifa}")
def eliminar_numero_especial(numero: int, id_rifa: int, sesesion: session_dependency):
    return service.eliminar_numero_especial(
        numero=numero, session=sesesion, id_rifa=id_rifa
    )


# @router_numeros.post("/compra")
# def comprar_boletas(compra: models.Compra, sesesion: session_dependency):
