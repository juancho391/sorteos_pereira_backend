from typing import Optional

from sqlmodel import SQLModel


class NumeroEspecialCreate(SQLModel):
    numero: int
    id_rifa: int
    disponible: Optional[bool] = True


class NumeroEspecialResponse(NumeroEspecialCreate):
    id: int


class Compra(SQLModel):
    nombre_completo: str
    cedula: str
    celular: str
    email: str
    direccion: str
    cantidad_boletas: int
    total: int
