from typing import Annotated

from fastapi import Depends

from ..exceptions import (
    RifaCreationError,
    RifaIDNotFoundError,
    RifaNotFoundError,
    RifasNotFoundError,
)
from ..utils.s3 import upload_image
from .models import RifaCreate
from .rifaRepository import rifa_repository_dependency


class RifaService:
    def __init__(self, repository: rifa_repository_dependency):
        self.repository = repository

    def crear_rifa(self, rifa: RifaCreate, image):
        try:
            image_url = upload_image(file=image)
            rifa.image_premio = image_url
            return self.repository.crear_rifa(rifa=rifa)
        except Exception as e:
            raise RifaCreationError(error=str(e))

    def obtener_rifas(self):
        rifas = self.repository.obtener_rifas()
        if not rifas:
            raise RifasNotFoundError()
        return rifas

    def obtener_rifa_activa(self):
        rifa = self.repository.obtener_rifa_activa()
        if not rifa:
            raise RifaNotFoundError()
        return rifa

    def obtener_rifa_id(self, rifa_id: int):
        rifa = self.repository.obtener_rifa_id(rifa_id=rifa_id)
        if not rifa or not rifa.is_active:
            raise RifaIDNotFoundError(id=rifa_id)
        return rifa

    def desactivar_rifa(self, rifa_id: int):
        rifa = self.repository.obtener_rifa_id(rifa_id=rifa_id)
        if not rifa:
            raise RifaIDNotFoundError(id=rifa_id)
        rifa.is_active = False
        return self.repository.actualizar_rifa(rifa=rifa)

    def verificar_rifas_activas(self):
        rifas = self.repository.obtener_rifas_activas()
        return True if len(rifas) > 1 else False


def get_rifa_service(rifa_repository_dependency: rifa_repository_dependency):
    return RifaService(repository=rifa_repository_dependency)


rifa_service_dependency = Annotated[RifaService, Depends(get_rifa_service)]
