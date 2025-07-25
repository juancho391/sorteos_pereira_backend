from datetime import date
from typing import Optional

from sqlmodel import SQLModel

from ..entities.Boleta import Boleta


class NumeroEspecial(SQLModel):
    id: int
    numero: int
    id_rifa: int
    disponible: bool | None = True


class RifaBAse(SQLModel):
    id: int | None = None


class RifaCreate(SQLModel):
    premio: str
    tipo: str
    image_premio: Optional[str] = None
    precio: int


class RifaResponse(RifaCreate):
    id: int
    is_active: bool
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    precio: int
    numeros_especiales: list[NumeroEspecial] = []
    boletas: list[Boleta] = []
