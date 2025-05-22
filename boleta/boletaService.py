from .boletaRepository import boleta_repository_dependency
from ..entities.Boleta import Boleta
from typing import Annotated
from fastapi import Depends
from ..exceptions import BoletasCreationError, BoletaNotFoundError


class BoletaService:
    def __init__(self, boleta_repository: boleta_repository_dependency):
        self.boleta_repository = boleta_repository

    def crear_boleta(self, boleta: Boleta):
        return self.boleta_repository.crear_boleta(boleta=boleta)

    def obtener_boletas_vendidas(self, id_rifa: int):
        numeros = self.boleta_repository.obtener_boletas_rifa(id_rifa=id_rifa)
        if not numeros:
            return []
        return numeros

    def crear_boletas(
        self, usuario_id: int, rifa_id: int, lista_numeros: list[int]
    ) -> list[Boleta]:
        boletas = self.boleta_repository.crear_boletas(
            usuario_id=usuario_id, rifa_id=rifa_id, lista_numeros=lista_numeros
        )
        if not boletas:
            raise BoletasCreationError(error="No se pudieron crear las boletas")
        return boletas

    def obtener_ganador(self, id_rifa: int, numero: int):
        boleta_obtenida = self.boleta_repository.obtener_boleta_numero_rifa(
            id_rifa=id_rifa, numero=numero
        )
        if not boleta_obtenida:
            raise BoletaNotFoundError(numero=numero)
        return boleta_obtenida


def get_boleta_service(boleta_repository: boleta_repository_dependency):
    return BoletaService(boleta_repository=boleta_repository)


boleta_service_dependency = Annotated[BoletaService, Depends(get_boleta_service)]
