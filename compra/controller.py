from fastapi import APIRouter, Request
import json
from . import models
from . import services
from dotenv import load_dotenv
import os
import httpx
from ..db.conexion import session_dependency
import requests

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

router_compra = APIRouter(tags=["compra"])


# Endpoint para crear una compra
@router_compra.post("/")
async def crear_compra(compra: models.Compra):
    return await services.crear_preferencia(compra=compra)


# Endpoint paraa recibir la notificacion de la compra
@router_compra.post("/webhook/mercadopago", status_code=200)
async def mercadopago_webhook(request: Request, session: session_dependency):
    data = await request.json()
    payment_id = data.get("data", {}).get("id")
    if payment_id:
        return await services.check_payment_status(
            payment_id=payment_id, session=session
        )
    return {"mensaje": "no payment_id"}
