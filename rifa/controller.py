from fastapi import APIRouter, File, Form, UploadFile

from ..auth.service import Usuario_actual
from ..boleta.boletaService import boleta_service_dependency
from ..users.models import User
from ..users.services import user_service_dependency
from . import models
from .models import RifaCreate
from .service import rifa_service_dependency

router_rifa = APIRouter(tags=["Rifa"])


# Ednpoint para obtener todas las rifas
@router_rifa.get("/", response_model=list[models.RifaResponse])
def obtener_rifas(
    rifa_service: rifa_service_dependency, usuario_actual: Usuario_actual
):
    return rifa_service.obtener_rifas()


# Ednpoint para crear una rifa
@router_rifa.post("/")
def crear_rifa(
    usuario_actual: Usuario_actual,
    rifa_service: rifa_service_dependency,
    premio: str = Form(...),
    tipo: str = Form(...),
    precio: int = Form(...),
    image: UploadFile = File(...),
):
    rifa = RifaCreate(premio=premio, tipo=tipo, precio=precio)
    return rifa_service.crear_rifa(rifa=rifa, image=image)


@router_rifa.get("/activa", response_model=models.RifaResponse)
def obtener_rifa(rifa_service: rifa_service_dependency):
    return rifa_service.obtener_rifa_activa()


@router_rifa.patch("/{id}/desactivar")
def finalizar_rifa(
    id: int, rifa_service: rifa_service_dependency, usuario_actual: Usuario_actual
):
    return rifa_service.desactivar_rifa(rifa_id=id)


@router_rifa.get("/{id}/{numero}/", response_model=User)
def obtener_ganador(
    id: int,
    numero: int,
    boleta_service: boleta_service_dependency,
    user_service: user_service_dependency,
    usuario_actual: Usuario_actual,
):
    boleta_otbtenida = boleta_service.obtener_ganador(id_rifa=id, numero=numero)
    return user_service.obtener_usuario_id(id_user=boleta_otbtenida.id_usuario)
