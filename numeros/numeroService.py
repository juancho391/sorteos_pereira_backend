from fastapi import Depends
from typing import Annotated
from .models import NumeroEspecialCreate
from ..exceptions import (
    NumeroEspecialCreationError,
    NumeroEspecialNotFoundError,
    NumeroEspecialDeleteError,
)
from ..entities import Rifa
from .numeroRepository import numero_repository_dependency


class NumeroService:

    def __init__(self, numero_repository: numero_repository_dependency):
        self.numero_repository = numero_repository

    def crear_numero_especial(self, numero_especial: NumeroEspecialCreate):
        try:
            numeros_especiales_existentes = self.numero_repository.obtener_numeros()
            for numero in numeros_especiales_existentes:
                if (
                    numero.numero == numero_especial.numero
                    and numero.id_rifa == numero_especial.id_rifa
                ):
                    raise NumeroEspecialCreationError(
                        error="El numero ya existe en la rifa"
                    )
            return self.numero_repository.crear_numero(numero=numero_especial)
        except Exception as e:
            raise NumeroEspecialCreationError(error=str(e))

    def obtener_numeros_especiales(self):
        numeros_especiales = self.numero_repository.obtener_numeros()
        if not numeros_especiales:
            raise []
        return numeros_especiales

    def obtener_numeros_rifa(self, rifa_activa: Rifa.Rifa):
        numeros_especiales = self.numero_repository.obtener_numeros_rifa(
            rifa_activa=rifa_activa
        )
        if not numeros_especiales:
            return []
        return numeros_especiales


def get_numero_service(numero_repository: numero_repository_dependency):
    return NumeroService(numero_repository=numero_repository)


numero_service_dependency = Annotated[NumeroService, Depends(get_numero_service)]
