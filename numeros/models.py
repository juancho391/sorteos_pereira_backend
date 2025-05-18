from typing import Optional
from sqlmodel import SQLModel


class NumeroEspecialCreate(SQLModel):
    id: Optional[int] = None
    numero: int
    id_rifa: int
    disponible: bool


class Compra(SQLModel):
    nombre_completo: str
    cedula: str
    celular: str
    email: str
    direccion: str
    cantidad_boletas: int
    total: int
