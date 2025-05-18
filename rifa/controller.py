from fastapi import APIRouter, UploadFile, File, Form
from . import services
from . import models
from ..db.conexion import session_dependency
from ..s3.service import upload_image
from ..auth import service
from ..entities.Rifa import Rifa
from . import models
from typing import Optional
from .models import RifaCreate

router_rifa = APIRouter(tags=["Rifa"])


# Ednpoint para obtener todas las rifas
@router_rifa.get("/", response_model=list[models.RifaResponse])
def obtener_rifas(session: session_dependency, usuario_actual: service.Usuario_actual):
    return services.obtener_rifas(session=session)


# Ednpoint para crear una rifa
@router_rifa.post("/")
def crear_rifa(
    session: session_dependency,
    usuario_actual: service.Usuario_actual,
    premio: str = Form(...),
    tipo: str = Form(...),
    precio: int = Form(...),
    image: UploadFile = File(...),
    is_active: Optional[bool] = Form(True),
):

    image_url = upload_image(file=image)

    rifa = RifaCreate(
        premio=premio,
        tipo=tipo,
        is_active=is_active,
        precio=precio,
        image_premio=image_url,
    )
    return services.crear_rifa(session=session, rifa=rifa)


@router_rifa.get("/activa", response_model=models.RifaResponse)
def obtener_rifa(session: session_dependency):
    return services.obtener_rifa_activa_numeros_espciales(session=session)


@router_rifa.put("/{id}/desactivar")
def finalizar_rifa(id: int, session: session_dependency):
    return services.finalizar_rifa(session=session, id=id)


@router_rifa.get("/ganador")
def obtener_ganador(session: session_dependency, boleta: models.BoletaConsulta):
    return services.obtener_ganador(session=session, boleta=boleta)
