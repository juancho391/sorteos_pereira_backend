from fastapi import APIRouter, Request

from . import models
from .services import compra_service_dependency

router_compra = APIRouter(tags=["compra"])


# Endpoint para crear una compra
@router_compra.post("/")
async def crear_compra(
    compra: models.CompraRequest, compra_service: compra_service_dependency
):
    return await compra_service.crear_preferencia(compra=compra)


# Endpoint paraa recibir la notificacion de la compra
@router_compra.post("/webhook/mercadopago", status_code=200)
async def mercadopago_webhook(
    request: Request, compra_service: compra_service_dependency
):
    data = await request.json()
    payment_id = data.get("data", {}).get("id")
    if payment_id:
        return await compra_service.check_payment_status(payment_id=payment_id)
    return {"mensaje": "no payment_id"}
