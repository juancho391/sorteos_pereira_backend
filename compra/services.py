from . import models
import requests
from dotenv import load_dotenv
import os
from ..numeros import service
from pprint import pprint as pp
from ..Correos.service import send_email
from ..db.conexion import session_dependency

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def crear_preferencia():
    pass


async def check_payment_status(payment_id: str, session: session_dependency):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    print("status de la compra y la informacion de la compra")
    data = response.json()
    pp(data)
    status = data.get("status")
    cantidad = data["additional_info"]["items"][0]["quantity"]
    if status == "approved":
        boletas_generados = service.generar_compra_boletas(
            session=session, cantidad_comprada=int(cantidad)
        )
        nombre = data["additional_info"]["payer"]["first_name"]
        numeros = str()
        for numero in boletas_generados:
            numeros += f" {numero} "

        body = f"Hola {nombre} estos son los numeros con los que participaras en el sorteo: {numeros}"
        # send_email(
        #     subject="Boletas compradas", body=body, to_email="jhostinposada7@gmail.com"
        # )
        print(body)
    elif status == "rejected":
        return models.PagoResponse(status=status)
