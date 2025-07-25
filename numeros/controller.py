from fastapi import APIRouter

from . import models
from .numeroService import numero_service_dependency

router_numeros = APIRouter(tags=["Numeros"])


# Endpoint para crear numero especial
@router_numeros.post("/numero_especial", response_model=models.NumeroEspecialResponse)
def crear_numero_especial(
    numero_especial: models.NumeroEspecialCreate,
    numero_service: numero_service_dependency,
):
    return numero_service.crear_numero_especial(numero_especial=numero_especial)
