from sqlmodel import SQLModel, Field
from typing import Optional


class Compra(SQLModel):
    id_rifa: int
    nombre_completo: str
    telefono_celular: str
    email: str
    cantidad: int
    precio: int


class CompraResponse(SQLModel):
    init_point: str


class PagoResponse(SQLModel):
    status: str
