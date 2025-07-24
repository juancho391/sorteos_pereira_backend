from typing import Annotated

from fastapi import Depends

from ..entities import Rifa
from ..exceptions import (
    NumeroEspecialCreationError,
)
from .models import NumeroEspecialCreate
from .numeroRepository import numero_repository_dependency


class NumeroService:

    def __init__(self, numero_repository: numero_repository_dependency):
        self.numero_repository = numero_repository

    def crear_numero_especial(self, numero_especial: NumeroEspecialCreate):
        try:
            numero_especial_db = self.numero_repository.obtener_numeros_numero_idRifa(
                id_rifa=numero_especial.id_rifa, numero=numero_especial.numero
            )
            if numero_especial_db:
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

    def cambiar_disponibilidad_numero_especial(self, numero: int, id_rifa: int):
        return self.numero_repository.actualizar_numero(numero=numero, id_rifa=id_rifa)


def get_numero_service(numero_repository: numero_repository_dependency):
    return NumeroService(numero_repository=numero_repository)


numero_service_dependency = Annotated[NumeroService, Depends(get_numero_service)]
