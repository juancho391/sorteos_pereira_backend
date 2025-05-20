import requests
from dotenv import load_dotenv
import os
from ..numeros import service
from pprint import pprint as pp
from ..Correos.service import send_email
from ..db.conexion import session_dependency
from .models import PagoResponse
import httpx
from . import models
from ..users.services import crearUser, obtenerUsuario
from ..users.models import UserCreate
from ..entities.Compra import Compra

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


async def crear_preferencia(compra: models.Compra):
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
        "notification_url": "https://5e64-2800-484-a71d-5400-580d-c94b-21a3-a47e.ngrok-free.app/compra/webhook/mercadopago",  # Webhook
        "metadata": {
            "compra_id": compra.id_rifa,
            "email": compra.email,
            "telefono": compra.telefono_celular,
            "cedula": compra.cedula,
            "direccion": compra.direccion,
            "nombre": compra.nombre_completo,
        },
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


def crear_compra(compra: models.CompraCreate, session: session_dependency):
    nueva_compra = Compra.model_validate(compra)
    session.add(nueva_compra)
    session.commit()
    session.refresh(nueva_compra)
    return nueva_compra


async def check_payment_status(payment_id: str, session: session_dependency):
    # Verificamos el estado de la compra en mercadopago
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    # Realizamos la peticion
    response = requests.get(url, headers=headers)

    data = response.json()
    status = data.get("status")

    if status == "approved":
        cantidad = int(data["additional_info"]["items"][0]["quantity"])
        email = data["metadata"]["email"]
        celular = data["metadata"]["telefono"]
        cedula = data["metadata"]["cedula"]
        direccion = data["metadata"]["direccion"]
        total = int(data["transaction_details"]["total_paid_amount"])
        id_rifa = int(data["metadata"]["compra_id"])
        nombre = data["metadata"]["nombre"]

        # Generamos las boletas
        boletas_generados = service.generar_compra_boletas(
            session=session, cantidad_comprada=int(cantidad)
        )
        # Obtenemos el usuario y Verificamos si el usuario existe
        usuario = obtenerUsuario(session=session, cedula=cedula)
        if not usuario:
            # si no existe lo creamos
            print("Ingreso user", usuario)
            usuario = UserCreate(
                nombre=nombre,
                email=email,
                celular=celular,
                cedula=cedula,
                direccion=direccion,
            )
            usuario = crearUser(session=session, user_compra=usuario)

        # Guardamos las boletas en la bd
        service.crear_numero(
            session=session,
            usuario_id=usuario.id,
            rifa=id_rifa,
            lista_numeros=boletas_generados,
        )
        # Creamos la Compra
        nueva_compra = models.CompraCreate(
            id_rifa=id_rifa, cantidad=cantidad, total=total, id_usuario=usuario.id
        )
        # Guardamos laa compra en la bd
        compra = crear_compra(compra=nueva_compra, session=session)
        numeros = str()
        for numero in boletas_generados:
            numeros += f" {numero} "

        # Cuerpo del mensaje del correo
        body = f"Hola {nombre} estos son los numeros con los que participaras en el sorteo: {numeros}"
        # Mandemos emensaje al correo
        send_email(
            subject="Boletas compradas", body=body, to_email="jhostinposada7@gmail.com"
        )
