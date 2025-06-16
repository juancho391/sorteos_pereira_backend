import requests
from dotenv import load_dotenv
import os
from typing import Annotated
from fastapi import Depends
from ..Correos.service import send_email
from .compraRepository import compra_repository_depedency
import httpx
from . import models
from ..users.services import user_service_dependency
from ..users.models import UserCreate
from ..utils.generar_numeros import generador_numeros_dependency
from ..boleta.boletaService import boleta_service_dependency

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


class CompraService:
    def __init__(
        self,
        compra_repository: compra_repository_depedency,
        usuario_service: user_service_dependency,
        generador_numeros: generador_numeros_dependency,
        boleta_service: boleta_service_dependency,
    ):
        self.compra_repository = compra_repository
        self.usuario_service = usuario_service
        self.generador_numeros = generador_numeros
        self.boleta_service = boleta_service

    def crear_compra(self, compra: models.CompraCreate):
        nueva_compra = self.compra_repository.crear_compra(compra=compra)
        if not nueva_compra:
            with open("log.txt", "a") as f:
                f.write(
                    f"Error al crear la compra: {compra.id_rifa} - {compra.cantidad} - {compra.id_usuario}\n"
                )
        return nueva_compra

    async def crear_preferencia(self, compra: models.CompraCreate):
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
            "notification_url": "https://c77e-2800-484-a71d-5400-7090-5cfb-5db6-ea84.ngrok-free.app/compra/webhook/mercadopago",  # Webhook
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

    async def check_payment_status(
        self,
        payment_id: str,
    ):
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
            numeros_generados = self.generador_numeros.generar_compra_boletas(
                cantidad_comprada=cantidad, id_rifa=id_rifa
            )

            # Verificamos si el usuario existe
            usuario = self.usuario_service.obtener_usuario_cedula(cedula=cedula)
            if not usuario:
                # si no existe lo creamos
                usuario = UserCreate(
                    nombre=nombre,
                    email=email,
                    celular=celular,
                    cedula=cedula,
                    direccion=direccion,
                )
                usuario = self.usuario_service.crear_usuario(usuario=usuario)

            # Guardamos las boletas en la bd
            self.boleta_service.crear_boletas(
                usuario_id=usuario.id,
                rifa_id=id_rifa,
                lista_numeros=numeros_generados,
            )
            # Creamos la Compra
            nueva_compra = models.CompraCreate(
                id_rifa=id_rifa, cantidad=cantidad, total=total, id_usuario=usuario.id
            )
            # Guardamos laa compra en la bd
            compra = self.crear_compra(compra=nueva_compra)
            numeros = str()
            for numero in numeros_generados:
                numeros += f" {numero} "

            # Cuerpo del mensaje del correo
            body = f"Hola {nombre} estos son los numeros con los que participaras en el sorteo: {numeros}"
            # Mandamos mensaje al correo
            send_email(
                subject="Boletas compradas",
                body=body,
                to_email=email,
            )
            return True


def get_compra_service(
    compra_repository: compra_repository_depedency,
    usuario_service: user_service_dependency,
    generador_numeros: generador_numeros_dependency,
    boleta_service: boleta_service_dependency,
):
    return CompraService(
        compra_repository=compra_repository,
        usuario_service=usuario_service,
        generador_numeros=generador_numeros,
        boleta_service=boleta_service,
    )


compra_service_dependency = Annotated[CompraService, Depends(get_compra_service)]
