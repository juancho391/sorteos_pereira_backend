from sqlmodel import SQLModel, Field
from typing import Optional


class CompraRequest(SQLModel):
    id_rifa: int
    nombre_completo: str
    telefono_celular: str
    direccion: str
    cedula: str
    email: str
    cantidad: int
    precio: int


class CompraCreate(SQLModel):
    id_rifa: int
    id_usuario: int
    cantidad: int
    total: int


class CompraResponse(SQLModel):
    init_point: str


class PagoResponse(SQLModel):
    status: str
