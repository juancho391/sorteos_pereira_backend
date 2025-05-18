from datetime import date
from typing import Optional
from sqlmodel import SQLModel


class Numero_especial(SQLModel):
    id: int
    numero: int
    id_rifa: int
    disponible: bool | None = True


class RifaCreate(SQLModel):
    id: Optional[int] = None
    premio: str
    tipo: str
    is_active: Optional[bool] = True
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    image_premio: Optional[str] = None
    precio: int


class RifaResponse(SQLModel):
    id: int
    premio: str
    tipo: str
    is_active: bool
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    image_premio: str
    precio: int
    numeros_especiales: list[Numero_especial] = []
    boletas_vendidas: Optional[int] = 0


class BoletaConsulta(SQLModel):
    numero: int
    id_rifa: int
