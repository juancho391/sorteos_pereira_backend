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
    data = compra.model_dump_json()
    preferencia = {
        "items": [
            {
                "title": "Boleta para el sorteo",
                "quantity": compra.cantidad,
                "currency_id": "COP",
                "unit_price": compra.precio,
            }
        ],
        "payer": {"name": compra.nombre_completo, "email": compra.email},
        "back_urls": {
            "success": "https://localhost:3000/aprobado",
            "failure": "https://localhost:3000/denegado",
            "pending": "https://localhost:3000/pendiente",
        },
        "auto_return": "approved",
        "notification_url": "https://7b4d-181-49-85-222.ngrok-free.app/compra/webhook/mercadopago",  # Webhook
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.mercadopago.com/checkout/preferences",
            json=preferencia,
            headers=headers,
        )

    if response.status_code == 201:
        init_point = response.json()["init_point"]
        return models.CompraResponse(init_point=init_point)
    raise Exception("Error al crear la compra")


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
